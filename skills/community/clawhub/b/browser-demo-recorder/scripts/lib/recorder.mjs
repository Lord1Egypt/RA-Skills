import fs from 'node:fs';
import { PuppeteerScreenRecorder } from 'puppeteer-screen-recorder';

export function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

export function createRecorderConfig(options = {}) {
  const {
    width = 1600,
    height = 1200,
    fps = 60,
    ffmpegPath = process.env.FFMPEG_PATH || null,
  } = options;

  return {
    followNewTab: true,
    fps,
    ffmpeg_Path: ffmpegPath,
    videoFrame: {
      width,
      height,
    },
    quality: 100,
    videoCrf: 18,
    videoPreset: 'medium',
    videoCodec: 'libx264',
    videoBitrate: 8000,
    autopad: {
      color: 'black',
    },
  };
}

export function createRecorder(page, options = {}) {
  const config = createRecorderConfig(options);
  return {
    recorder: new PuppeteerScreenRecorder(page, config),
    config,
  };
}

export async function stopRecorder(recorder) {
  if (!recorder) return;
  try {
    await recorder.stop();
  } catch {}
}
