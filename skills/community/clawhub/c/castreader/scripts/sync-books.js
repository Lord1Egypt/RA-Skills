#!/usr/bin/env node

/**
 * sync-books.js — List synced books and read book content
 *
 * Usage:
 *   node scripts/sync-books.js --list
 *     List all synced books from ~/castreader-library/books/
 *     Output: { books: [{ id, title, author, language, totalChapters, totalCharacters, source }] }
 *
 *   node scripts/sync-books.js --book <id>
 *     Read a book's full text. The <id> is the EXACT folder name from --list output.
 *     Output: { title, author, language, totalChapters, totalCharacters, fullText, chapters: [{ title, text }] }
 *
 *   node scripts/sync-books.js --book <id> --chapter <num>
 *     Read a single chapter (1-based).
 *     Output: { title, author, chapter: { number, title, text }, totalChapters }
 *
 *   node scripts/sync-books.js --book <id> --audio
 *     Generate audio for the full book.
 *     Output: { audioFile, fileSizeBytes }
 *
 *   node scripts/sync-books.js --book <id> --chapter <num> --audio
 *     Generate audio for a single chapter.
 *     Output: { audioFile, fileSizeBytes }
 *
 * IMPORTANT: The <id> must be the EXACT string from --list output (e.g. "儒林外史-dc532c705c6d3edc5503acc").
 * Do NOT use partial IDs or strip any prefix.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const LIBRARY_ROOT = path.join(os.homedir(), 'castreader-library');
const BOOKS_DIR = path.join(LIBRARY_ROOT, 'books');

const API_URL = process.env.CASTREADER_API_URL || 'https://api.castreader.ai';
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

function listBooks() {
  if (!fs.existsSync(BOOKS_DIR)) {
    console.log(JSON.stringify({ books: [] }));
    return;
  }

  const entries = fs.readdirSync(BOOKS_DIR, { withFileTypes: true });
  const books = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const metaPath = path.join(BOOKS_DIR, entry.name, 'meta.json');
    if (fs.existsSync(metaPath)) {
      try {
        const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
        books.push({
          id: entry.name,
          title: meta.title,
          author: meta.author,
          language: meta.language,
          totalChapters: meta.totalChapters,
          totalCharacters: meta.totalCharacters,
          source: meta.source,
          syncedAt: meta.syncedAt,
        });
      } catch { /* skip corrupted */ }
    }
  }

  console.log(JSON.stringify({ books }, null, 2));
}

function readBook(bookId, chapterNum) {
  const bookDir = path.join(BOOKS_DIR, bookId);

  if (!fs.existsSync(bookDir)) {
    console.error(`Error: Book not found at ${bookDir}`);
    console.error('Use --list to see available books and their exact IDs.');
    process.exit(1);
  }

  const metaPath = path.join(bookDir, 'meta.json');
  if (!fs.existsSync(metaPath)) {
    console.error(`Error: meta.json not found in ${bookDir}`);
    process.exit(1);
  }

  const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));

  if (chapterNum !== undefined) {
    // Read single chapter — try both zero-padded and unpadded filenames
    const padded = String(chapterNum).padStart(2, '0');
    let chapterFile = path.join(bookDir, `chapter-${padded}.md`);
    if (!fs.existsSync(chapterFile)) {
      chapterFile = path.join(bookDir, `chapter-${chapterNum}.md`);
    }
    if (!fs.existsSync(chapterFile)) {
      console.error(`Error: Chapter ${chapterNum} not found. Available: 1-${meta.totalChapters}`);
      process.exit(1);
    }
    const text = fs.readFileSync(chapterFile, 'utf-8');
    // Extract chapter title from first line (# Title)
    const firstLine = text.split('\n')[0];
    const chTitle = firstLine.startsWith('# ') ? firstLine.slice(2).trim() : `Chapter ${chapterNum}`;

    return {
      title: meta.title,
      author: meta.author,
      language: meta.language,
      chapter: { number: chapterNum, title: chTitle, text },
      totalChapters: meta.totalChapters,
    };
  }

  // Read full book
  const fullPath = path.join(bookDir, 'full.md');
  if (fs.existsSync(fullPath)) {
    const fullText = fs.readFileSync(fullPath, 'utf-8');
    return {
      title: meta.title,
      author: meta.author,
      language: meta.language,
      totalChapters: meta.totalChapters,
      totalCharacters: meta.totalCharacters,
      fullText,
    };
  }

  // Fallback: concatenate chapters
  const chapters = [];
  for (let i = 1; i <= meta.totalChapters; i++) {
    const padded = String(i).padStart(2, '0');
    let chFile = path.join(bookDir, `chapter-${padded}.md`);
    if (!fs.existsSync(chFile)) chFile = path.join(bookDir, `chapter-${i}.md`);
    if (fs.existsSync(chFile)) {
      const text = fs.readFileSync(chFile, 'utf-8');
      const firstLine = text.split('\n')[0];
      const chTitle = firstLine.startsWith('# ') ? firstLine.slice(2).trim() : `Chapter ${i}`;
      chapters.push({ title: chTitle, text });
    }
  }

  return {
    title: meta.title,
    author: meta.author,
    language: meta.language,
    totalChapters: meta.totalChapters,
    totalCharacters: meta.totalCharacters,
    fullText: chapters.map(c => c.text).join('\n\n---\n\n'),
    chapters,
  };
}

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--list')) {
    listBooks();
    return;
  }

  const bookIdx = args.indexOf('--book');
  if (bookIdx === -1 || !args[bookIdx + 1]) {
    console.error('Usage:');
    console.error('  node scripts/sync-books.js --list');
    console.error('  node scripts/sync-books.js --book <id> [--chapter <num>] [--audio]');
    process.exit(1);
  }

  const bookId = args[bookIdx + 1];
  const chapterIdx = args.indexOf('--chapter');
  const chapterNum = chapterIdx !== -1 ? parseInt(args[chapterIdx + 1], 10) : undefined;
  const wantAudio = args.includes('--audio');

  const result = readBook(bookId, chapterNum);

  if (wantAudio) {
    const text = chapterNum !== undefined ? result.chapter.text : result.fullText;
    const label = chapterNum !== undefined
      ? `chapter-${chapterNum}`
      : 'full';
    const outputDir = path.join('/tmp', `castreader-book-${bookId.replace(/[^a-zA-Z0-9-]/g, '_')}`);
    fs.mkdirSync(outputDir, { recursive: true });
    const audioFile = path.join(outputDir, `${label}.mp3`);

    process.stderr.write(`Generating audio for ${text.length} chars...\n`);
    const audio = await generateTTS(text, result.language);
    fs.writeFileSync(audioFile, audio);

    console.log(JSON.stringify({
      title: result.title,
      audioFile: path.resolve(audioFile),
      fileSizeBytes: audio.length,
    }));
  } else {
    console.log(JSON.stringify(result, null, 2));
  }
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
