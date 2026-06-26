#!/usr/bin/env node
/**
 * Generate opus voice audio using Edge TTS for Feishu voice bubbles.
 *
 * Usage: node gen_voice.js <text> <output_path> [options]
 *
 * Options:
 *   --voice <name>    Voice name (default: zh-CN-XiaoxiaoNeural)
 *   --rate <percent>  Speech rate, e.g. +20% or -10% (default: +0%)
 *   --pitch <percent> Pitch adjustment, e.g. +5% or -5% (default: +0%)
 *   --split <chars>   Auto-split long text at this char count (default: 0 = no split)
 *
 * Examples:
 *   node gen_voice.js "你好世界" output.opus
 *   node gen_voice.js "你好世界" output.opus --voice zh-CN-YunxiNeural --rate +15%
 *   node gen_voice.js "长文本..." output.opus --split 500
 *
 * Output format: webm-24khz-16bit-mono-opus (.opus)
 * No API key required.
 */

const { EdgeTTS } = require('node-edge-tts');
const path = require('path');
const fs = require('fs');

function parseArgs(args) {
  const result = {
    text: '',
    outputPath: '',
    voice: 'zh-CN-XiaoxiaoNeural',
    rate: '+0%',
    pitch: '+0%',
    split: 0,
  };

  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--voice' && args[i + 1]) { result.voice = args[++i]; }
    else if (args[i] === '--rate' && args[i + 1]) { result.rate = args[++i]; }
    else if (args[i] === '--pitch' && args[i + 1]) { result.pitch = args[++i]; }
    else if (args[i] === '--split' && args[i + 1]) { result.split = parseInt(args[++i], 10); }
    else { positional.push(args[i]); }
  }

  result.text = positional[0] || '';
  result.outputPath = positional[1] || '';
  return result;
}

// Split text into chunks at sentence boundaries
function splitText(text, maxChars) {
  if (!maxChars || maxChars <= 0 || text.length <= maxChars) return [text];

  const chunks = [];
  let remaining = text;

  while (remaining.length > 0) {
    if (remaining.length <= maxChars) {
      chunks.push(remaining);
      break;
    }

    // Find best split point: sentence-ending punctuation
    let splitAt = -1;
    const punctuation = ['。', '！', '？', '；', '\n', '.', '!', '?', ';'];
    for (let i = Math.min(maxChars, remaining.length) - 1; i >= maxChars * 0.5; i--) {
      if (punctuation.includes(remaining[i])) {
        splitAt = i + 1;
        break;
      }
    }

    // Fallback: split at comma or space
    if (splitAt === -1) {
      const fallback = ['，', ',', ' ', '、'];
      for (let i = Math.min(maxChars, remaining.length) - 1; i >= maxChars * 0.5; i--) {
        if (fallback.includes(remaining[i])) {
          splitAt = i + 1;
          break;
        }
      }
    }

    // Last resort: hard split
    if (splitAt === -1) splitAt = maxChars;

    chunks.push(remaining.slice(0, splitAt).trim());
    remaining = remaining.slice(splitAt).trim();
  }

  return chunks.filter(c => c.length > 0);
}

async function generateOne(text, outputPath, voice, rate, pitch) {
  const tts = new EdgeTTS();
  const opts = {
    voice,
    outputFormat: 'webm-24khz-16bit-mono-opus',
  };
  if (rate && rate !== '+0%') opts.rate = rate;
  if (pitch && pitch !== '+0%') opts.pitch = pitch;

  await tts.ttsPromise(text, outputPath, opts);
  const stat = fs.statSync(outputPath);
  return stat.size;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.text || !args.outputPath) {
    console.error('Usage: node gen_voice.js <text> <output_path> [--voice name] [--rate +20%] [--pitch -5%] [--split 500]');
    process.exit(1);
  }

  const outputPath = path.resolve(args.outputPath);
  if (!outputPath.endsWith('.opus')) {
    console.error('Warning: output path should end with .opus for Feishu voice bubble support');
  }

  const chunks = splitText(args.text, args.split);

  if (chunks.length === 1) {
    // Single file
    const size = await generateOne(chunks[0], outputPath, args.voice, args.rate, args.pitch);
    console.log(JSON.stringify({
      status: 'ok',
      path: outputPath,
      voice: args.voice,
      rate: args.rate,
      size,
      textLength: args.text.length,
      chunks: 1,
    }));
  } else {
    // Multiple files: output_1.opus, output_2.opus, ...
    const ext = path.extname(outputPath);
    const base = outputPath.slice(0, -ext.length);
    const files = [];

    for (let i = 0; i < chunks.length; i++) {
      const filePath = `${base}_${i + 1}${ext}`;
      const size = await generateOne(chunks[i], filePath, args.voice, args.rate, args.pitch);
      files.push({ path: filePath, size, textLength: chunks[i].length });
    }

    console.log(JSON.stringify({
      status: 'ok',
      voice: args.voice,
      rate: args.rate,
      totalTextLength: args.text.length,
      chunks: chunks.length,
      files,
    }));
  }
}

main().catch((err) => {
  console.error(JSON.stringify({ status: 'error', message: err.message }));
  process.exit(1);
});
