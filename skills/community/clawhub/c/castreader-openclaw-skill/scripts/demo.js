#!/usr/bin/env node

/**
 * demo.js — Visual demo of CastReader OpenClaw Skill
 *
 * Simulates a Telegram-style conversation:
 *   User sends URL → Agent extracts → sends paragraph audio + text
 *
 * Usage: node scripts/demo.js [url]
 */

const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const BLUE = '\x1b[34m';
const GREEN = '\x1b[32m';
const CYAN = '\x1b[36m';
const DIM = '\x1b[2m';
const BOLD = '\x1b[1m';
const RESET = '\x1b[0m';
const BG_BLUE = '\x1b[44m\x1b[37m';
const BG_GREEN = '\x1b[42m\x1b[30m';

function sleep(ms) {
  const end = Date.now() + ms;
  while (Date.now() < end) {}
}

function typewrite(text, delay = 30) {
  for (const char of text) {
    process.stdout.write(char);
    sleep(delay);
  }
  console.log();
}

function printUser(text) {
  console.log();
  console.log(`${BG_BLUE} You ${RESET}  ${text}`);
}

function printBot(text) {
  console.log(`${BG_GREEN} CastReader ${RESET}  ${text}`);
}

function printBotTyping() {
  process.stdout.write(`${BG_GREEN} CastReader ${RESET}  ${DIM}typing...${RESET}`);
  sleep(800);
  process.stdout.write('\r\x1b[K');
}

function printDivider() {
  console.log(`${DIM}${'─'.repeat(60)}${RESET}`);
}

async function main() {
  const url = process.argv[2] || 'https://alistapart.com/blog/post/successful-or-unsuccessful-the-post-good-design-vocabulary/';

  console.clear();
  console.log();
  console.log(`${BOLD}  CastReader × OpenClaw — Demo${RESET}`);
  console.log(`${DIM}  Simulating a Telegram conversation${RESET}`);
  printDivider();

  // User sends URL
  sleep(1000);
  printUser(`Read this article for me:`);
  printUser(`${CYAN}${url}${RESET}`);
  console.log();

  sleep(1500);

  // Bot starts extracting
  printBotTyping();
  printBot(`${DIM}Extracting content...${RESET}`);
  console.log();

  // Actually run extract.js
  const extractScript = path.resolve(__dirname, 'extract.js');
  let extractResult;
  try {
    const output = execFileSync('node', [extractScript, url], {
      encoding: 'utf-8',
      timeout: 60000,
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    extractResult = JSON.parse(output);
  } catch (err) {
    printBot(`Sorry, I couldn't extract content from this page.`);
    process.exit(1);
  }

  if (!extractResult.success || !extractResult.paragraphs?.length) {
    printBot(`No readable content found on this page.`);
    process.exit(1);
  }

  sleep(500);
  printBot(`${BOLD}${extractResult.title}${RESET}`);
  printBot(`${DIM}${extractResult.totalParagraphs} paragraphs · ${extractResult.totalCharacters} chars · ${extractResult.language}${RESET}`);
  console.log();
  sleep(1000);

  // Generate audio for first 3 paragraphs (demo)
  const maxParas = Math.min(3, extractResult.paragraphs.length);
  printBot(`${DIM}Generating audio for ${maxParas} paragraphs...${RESET}`);
  console.log();

  const generateScript = path.resolve(__dirname, 'generate-audio.js');
  const outputDir = `/tmp/castreader-demo-${Date.now()}`;
  let manifest;
  try {
    // We'll run generate-audio but only use first few paragraphs
    const output = execFileSync('node', [generateScript, url, outputDir], {
      encoding: 'utf-8',
      timeout: 120000,
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    manifest = JSON.parse(output);
  } catch (err) {
    printBot(`Audio generation failed.`);
    process.exit(1);
  }

  // Display paragraphs as Telegram messages
  const displayCount = Math.min(maxParas, manifest.paragraphs.length);
  for (let i = 0; i < displayCount; i++) {
    const para = manifest.paragraphs[i];
    sleep(1200);
    printBotTyping();

    // Show paragraph text (truncated for display)
    const displayText = para.text.length > 120
      ? para.text.substring(0, 120) + '...'
      : para.text;

    printBot(`${BOLD}[${para.index}/${manifest.totalParagraphs}]${RESET} ${displayText}`);

    if (para.audioFile && fs.existsSync(para.audioFile)) {
      const sizeKB = (para.fileSizeBytes / 1024).toFixed(0);
      printBot(`${GREEN}🔊 ${path.basename(para.audioFile)}${RESET} ${DIM}(${sizeKB} KB)${RESET}`);
    }
    console.log();
  }

  if (manifest.totalParagraphs > displayCount) {
    sleep(800);
    printBot(`${DIM}... and ${manifest.totalParagraphs - displayCount} more paragraphs${RESET}`);
    console.log();
  }

  // Show full audio
  sleep(1000);
  printDivider();
  printBot(`${GREEN}📎 full.mp3${RESET} ${DIM}(${manifest.fullAudioSizeMB} MB — all ${manifest.totalParagraphs} paragraphs combined)${RESET}`);
  console.log();

  // Summary
  sleep(500);
  printDivider();
  console.log();
  console.log(`${BOLD}  Demo complete!${RESET}`);
  console.log(`${DIM}  Audio files saved to: ${outputDir}/${RESET}`);
  console.log(`${DIM}  Play: open ${outputDir}/001.mp3${RESET}`);
  console.log();
}

main();
