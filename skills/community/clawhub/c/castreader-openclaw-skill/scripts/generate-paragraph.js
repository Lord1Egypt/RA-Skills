#!/usr/bin/env node

/**
 * generate-paragraph.js — Generate audio for a single paragraph by index
 *
 * Usage:
 *   node generate-paragraph.js <extract-json-file> <paragraph-index>
 *
 * The extract-json-file is the output of extract.js (saved to a file).
 * paragraph-index is 1-based (1 = first paragraph).
 *
 * Output:
 *   Writes <index>.mp3 next to the extract JSON file.
 *   Prints JSON to stdout: { index, totalParagraphs, text, audioFile, fileSizeBytes }
 *
 * Environment variables:
 *   CASTREADER_API_URL  — TTS API endpoint (default: http://api.castreader.ai:8123)
 *   CASTREADER_VOICE    — TTS voice (default: af_heart)
 *   CASTREADER_SPEED    — Playback speed (default: 1.5)
 */

const fs = require('fs');
const path = require('path');

const API_URL = process.env.CASTREADER_API_URL || 'http://api.castreader.ai:8123';
const API_KEY = process.env.CASTREADER_API_KEY || '';
const VOICE = process.env.CASTREADER_VOICE || 'af_heart';
const SPEED = parseFloat(process.env.CASTREADER_SPEED || '1.5');
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 2000;

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function generateTTS(text, language) {
  const audioChunks = [];
  let remaining = text;

  while (remaining && remaining.trim().length > 0) {
    const body = {
      model: 'kokoro',
      input: remaining,
      voice: VOICE,
      response_format: 'mp3',
      return_timestamps: true,
      speed: SPEED,
      stream: false,
      language: language || 'en',
    };

    let data = null;
    let lastError = null;

    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
      try {
        const headers = { 'Content-Type': 'application/json', accept: 'application/json' };
        if (API_KEY) headers['Authorization'] = `Bearer ${API_KEY}`;

        const response = await fetch(`${API_URL}/api/captioned_speech_partly`, {
          method: 'POST',
          headers,
          body: JSON.stringify(body),
        });

        if (!response.ok) {
          const errText = await response.text().catch(() => '');
          lastError = new Error(`HTTP ${response.status}: ${errText}`);
          if (response.status >= 502 && response.status <= 504 && attempt < MAX_RETRIES) {
            await sleep(RETRY_DELAY_MS * attempt);
            continue;
          }
          throw lastError;
        }

        data = await response.json();
        break;
      } catch (err) {
        lastError = err;
        if (attempt < MAX_RETRIES && err.message?.includes('fetch')) {
          await sleep(RETRY_DELAY_MS * attempt);
          continue;
        }
        throw err;
      }
    }

    if (!data || (!data.audio && !data.audioUrl)) {
      throw lastError || new Error('No audio data received');
    }

    const audioBase64 = data.audio || data.audioUrl?.replace(/^data:audio\/\w+;base64,/, '');
    if (audioBase64) {
      audioChunks.push(Buffer.from(audioBase64, 'base64'));
    }

    remaining = data.unprocessed_text || '';
  }

  return Buffer.concat(audioChunks);
}

async function main() {
  const extractFile = process.argv[2];
  const paraIndex = parseInt(process.argv[3] || '1', 10);

  if (!extractFile || !fs.existsSync(extractFile)) {
    console.error('Usage: node generate-paragraph.js <extract-json-file> <paragraph-index>');
    console.error('  extract-json-file: path to the JSON output from extract.js');
    console.error('  paragraph-index: 1-based paragraph number');
    process.exit(1);
  }

  const extract = JSON.parse(fs.readFileSync(extractFile, 'utf-8'));

  if (!extract.success || !extract.paragraphs?.length) {
    console.error('Extract file has no paragraphs');
    process.exit(1);
  }

  const total = extract.paragraphs.length;

  if (paraIndex < 1 || paraIndex > total) {
    console.error(`Paragraph index ${paraIndex} out of range (1-${total})`);
    process.exit(1);
  }

  const text = extract.paragraphs[paraIndex - 1];
  if (!text || text.trim().length === 0) {
    console.error(`Paragraph ${paraIndex} is empty`);
    process.exit(1);
  }

  const outputDir = path.dirname(extractFile);
  const paddedIndex = String(paraIndex).padStart(3, '0');
  const audioFile = path.join(outputDir, `${paddedIndex}.mp3`);

  const audio = await generateTTS(text, extract.language);
  fs.writeFileSync(audioFile, audio);

  console.log(JSON.stringify({
    index: paraIndex,
    totalParagraphs: total,
    title: extract.title,
    language: extract.language,
    text: text.trim(),
    audioFile: path.resolve(audioFile),
    fileSizeBytes: audio.length,
  }));
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
