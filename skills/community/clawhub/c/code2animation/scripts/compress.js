import { spawnSync } from 'child_process';
import path from 'path';
import fs from 'fs';

// Logger with levels
const LOG_LEVEL = process.env.LOG_LEVEL || 'info';
const LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };
const currentLevel = LEVELS[LOG_LEVEL] || LEVELS.info;

const log = {
  debug: (...args) => currentLevel <= LEVELS.debug && console.log('[DEBUG]', ...args),
  info: (...args) => currentLevel <= LEVELS.info && console.log('[INFO]', ...args),
  warn: (...args) => currentLevel <= LEVELS.warn && console.warn('[WARN]', ...args),
  error: (...args) => currentLevel <= LEVELS.error && console.error('[ERROR]', ...args),
};

const args = process.argv.slice(2);
const inputFile = args[0];

if (!inputFile) {
  log.error('Usage: node scripts/compress.js <input-video-path> [--crf=23] [--preset=medium]');
  process.exit(1);
}

if (!fs.existsSync(inputFile)) {
  log.error(`File not found: ${inputFile}`);
  process.exit(1);
}

function getArgValue(name, defaultValue) {
  const withEq = args.find(arg => arg.startsWith(`--${name}=`));
  if (withEq) return withEq.slice(`--${name}=`.length);
  const idx = args.indexOf(`--${name}`);
  if (idx !== -1 && args[idx + 1]) return args[idx + 1];
  return defaultValue;
}

// CRF: 18-28 (lower = better quality, larger file)
// Preset: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
const crf = getArgValue('crf', '23');
const preset = getArgValue('preset', 'medium');

const dir = path.dirname(inputFile);
const ext = path.extname(inputFile);
const basename = path.basename(inputFile, ext);
const outputFile = path.join(dir, `${basename}-compressed${ext}`);

log.info(`Compressing: ${inputFile}`);
log.info(`Output: ${outputFile}`);
log.info(`Settings: CRF=${crf}, Preset=${preset}`);

const ffmpegArgs = [
  '-i', inputFile,
  '-c:v', 'libx264',
  '-crf', crf,
  '-preset', preset,
  '-c:a', 'aac',
  '-b:a', '128k',
  '-movflags', '+faststart',
  '-y',
  outputFile
];

const result = spawnSync('ffmpeg', ffmpegArgs, {
  stdio: currentLevel <= LEVELS.debug ? 'inherit' : 'pipe'
});

if (result.status !== 0) {
  log.error(`Compression failed with exit code ${result.status}`);
  process.exit(result.status || 1);
}

const originalSize = fs.statSync(inputFile).size;
const compressedSize = fs.statSync(outputFile).size;
const ratio = ((1 - compressedSize / originalSize) * 100).toFixed(1);

log.info(`✓ Compression complete!`);
log.info(`Original: ${(originalSize / 1024 / 1024).toFixed(2)} MB`);
log.info(`Compressed: ${(compressedSize / 1024 / 1024).toFixed(2)} MB`);
log.info(`Saved: ${ratio}%`);
