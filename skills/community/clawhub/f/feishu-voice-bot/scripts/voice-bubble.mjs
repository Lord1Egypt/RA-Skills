#!/usr/bin/env node
/**
 * Feishu Voice Bubble Generator
 * 
 * Usage: node voice-bubble.mjs "要转换的文字" [--voice zh-CN-XiaoxiaoNeural] [--output /tmp/voice.ogg]
 * 
 * Steps: edge-tts → mp3 → ffmpeg → ogg/opus
 * Output: OGG/Opus file ready for feishu message tool
 */

import { execSync } from 'child_process';
import { existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help')) {
  console.log(`Usage: node voice-bubble.mjs "文字" [options]

Options:
  --voice, -v    Voice ID (default: zh-CN-XiaoxiaoNeural)
  --output, -o   Output path (default: /tmp/voice-bubble-<timestamp>.ogg)
  --rate, -r     Speech rate (e.g., +10%, -20%)
  --help         Show this help

Examples:
  node voice-bubble.mjs "你好陛下"
  node voice-bubble.mjs "Hello" --voice en-US-AriaNeural`);
  process.exit(0);
}

// Parse args
const text = args.find(a => !a.startsWith('--'));
if (!text) {
  console.error('Error: No text provided');
  process.exit(1);
}

function getArg(flag, fallback) {
  const idx = args.indexOf(flag);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}

const voice = getArg('--voice', getArg('-v', 'zh-CN-XiaoxiaoNeural'));
const rate = getArg('--rate', getArg('-r', 'default'));
const output = getArg('--output', getArg('-o', `/tmp/voice-bubble-${Date.now()}.ogg`));

// Paths
const EDGE_TTS_SCRIPT = join(process.env.HOME, '.openclaw/workspace/skills/edge-tts/scripts/tts-converter.js');
const tmpMp3 = `/tmp/voice-bubble-${Date.now()}.mp3`;

// Verify edge-tts exists
if (!existsSync(EDGE_TTS_SCRIPT)) {
  console.error(`Error: edge-tts not found at ${EDGE_TTS_SCRIPT}`);
  process.exit(1);
}

try {
  // Step 1: Generate MP3
  console.error(`Generating audio: "${text.slice(0, 30)}${text.length > 30 ? '...' : ''}"`);
  console.error(`  Voice: ${voice}`);
  execSync(`node "${EDGE_TTS_SCRIPT}" "${text.replace(/"/g, '\\"')}" --voice ${voice} --rate ${rate} --output "${tmpMp3}"`, {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  if (!existsSync(tmpMp3)) {
    console.error('Error: TTS generation failed — no output file');
    process.exit(1);
  }

  // Step 2: Convert to OGG/Opus
  console.error('Converting to OGG/Opus...');
  execSync(`ffmpeg -i "${tmpMp3}" -c:a libopus -b:a 32k "${output}" -y`, {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  if (!existsSync(output)) {
    console.error('Error: ffmpeg conversion failed');
    process.exit(1);
  }

  // Step 3: Output path for message tool
  console.log(output);
  console.error(`Done: ${output}`);

} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
