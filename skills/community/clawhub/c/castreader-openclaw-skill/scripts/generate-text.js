#!/usr/bin/env node

/**
 * generate-text.js — Generate audio from a text file
 *
 * Usage:
 *   node scripts/generate-text.js <text-file> [language]
 *
 * Reads text from file, generates TTS audio, writes MP3 next to it.
 * Prints JSON: { audioFile, fileSizeBytes }
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
  const textFile = process.argv[2];
  const language = process.argv[3] || 'en';

  if (!textFile || !fs.existsSync(textFile)) {
    console.error('Usage: node scripts/generate-text.js <text-file> [language]');
    process.exit(1);
  }

  const text = fs.readFileSync(textFile, 'utf-8').trim();
  if (!text) {
    console.error('Text file is empty');
    process.exit(1);
  }

  const audioFile = textFile.replace(/\.[^.]+$/, '') + '.mp3';

  const audio = await generateTTS(text, language);
  fs.writeFileSync(audioFile, audio);

  console.log(JSON.stringify({
    audioFile: path.resolve(audioFile),
    fileSizeBytes: audio.length,
  }));
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
