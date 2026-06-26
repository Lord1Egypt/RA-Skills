#!/usr/bin/env node

/**
 * read-url.js — Extract article from URL and generate audio
 *
 * Usage:
 *   node scripts/read-url.js <url> <mode>
 *
 * Modes:
 *   0    — Extract only, no TTS. Returns article info + paragraph texts.
 *   all  — Extract + generate audio for ALL paragraphs (full article).
 *   1-N  — Extract + generate audio for one paragraph (1-based).
 *
 * Output JSON (mode=0):
 *   { title, language, totalParagraphs, totalCharacters, paragraphs[], current: null }
 *
 * Output JSON (mode=all):
 *   { title, language, totalParagraphs, totalCharacters, audioFile, fileSizeBytes }
 *
 * Output JSON (mode=1+):
 *   { title, language, totalParagraphs, totalCharacters, current: { index, text, audioFile, fileSizeBytes }, hasNext }
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

const API_URL = process.env.CASTREADER_API_URL || 'http://api.castreader.ai:8123';
const API_KEY = process.env.CASTREADER_API_KEY || '';
const VOICE = process.env.CASTREADER_VOICE || 'af_heart';
const SPEED = parseFloat(process.env.CASTREADER_SPEED || '1.5');
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 2000;

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function urlHash(url) {
  return crypto.createHash('md5').update(url).digest('hex').slice(0, 10);
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
  const url = process.argv[2];
  const modeArg = process.argv[3] || '1';

  if (!url) {
    console.error('Usage: node scripts/read-url.js <url> <0|all|paragraph-index>');
    process.exit(1);
  }

  // Stable output dir based on URL hash
  const hash = urlHash(url);
  const outputDir = path.join('/tmp', `castreader-${hash}`);
  fs.mkdirSync(outputDir, { recursive: true });

  const extractFile = path.join(outputDir, 'extract.json');

  // Step 1: Extract (or reuse cache)
  let extract;
  if (fs.existsSync(extractFile)) {
    extract = JSON.parse(fs.readFileSync(extractFile, 'utf-8'));
  } else {
    const extractScript = path.resolve(__dirname, 'extract.js');
    const output = execFileSync('node', [extractScript, url], {
      encoding: 'utf-8',
      timeout: 60000,
    });
    extract = JSON.parse(output);
    fs.writeFileSync(extractFile, JSON.stringify(extract, null, 2));
  }

  if (!extract.success || !extract.paragraphs?.length) {
    console.error('No content extracted');
    process.exit(1);
  }

  const total = extract.paragraphs.length;

  // Mode: 0 = extract-only
  if (modeArg === '0') {
    console.log(JSON.stringify({
      title: extract.title,
      language: extract.language,
      totalParagraphs: total,
      totalCharacters: extract.totalCharacters,
      paragraphs: extract.paragraphs.map(p => p.trim()),
      current: null,
    }));
    return;
  }

  // Mode: all = generate audio for entire article
  if (modeArg === 'all') {
    const fullText = extract.paragraphs.join('\n\n');
    const audioFile = path.join(outputDir, 'full.mp3');

    process.stderr.write(`Generating audio for ${total} paragraphs, ${extract.totalCharacters} chars...\n`);
    const audio = await generateTTS(fullText, extract.language);
    fs.writeFileSync(audioFile, audio);

    console.log(JSON.stringify({
      title: extract.title,
      language: extract.language,
      totalParagraphs: total,
      totalCharacters: extract.totalCharacters,
      audioFile: path.resolve(audioFile),
      fileSizeBytes: audio.length,
    }));
    return;
  }

  // Mode: paragraph index (1-based)
  const paraIndex = parseInt(modeArg, 10);

  if (isNaN(paraIndex) || paraIndex < 1 || paraIndex > total) {
    console.error(`Index ${modeArg} out of range (1-${total})`);
    process.exit(1);
  }

  const text = extract.paragraphs[paraIndex - 1];
  const paddedIndex = String(paraIndex).padStart(3, '0');
  const audioFile = path.join(outputDir, `${paddedIndex}.mp3`);

  const audio = await generateTTS(text, extract.language);
  fs.writeFileSync(audioFile, audio);

  console.log(JSON.stringify({
    title: extract.title,
    language: extract.language,
    totalParagraphs: total,
    totalCharacters: extract.totalCharacters,
    current: {
      index: paraIndex,
      text: text.trim(),
      audioFile: path.resolve(audioFile),
      fileSizeBytes: audio.length,
    },
    hasNext: paraIndex < total,
  }));
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
