import puppeteer from 'puppeteer';
import { spawn, execSync, spawnSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import os from 'os';

const args = process.argv.slice(2);
const isPortrait = args.includes('--portrait') || args.includes('portrait');
const skipCompress = args.includes('--no-compress') || args.includes('--skip-compress');
const projectId = args.find(arg => !arg.startsWith('--') && arg !== 'portrait');
const runIdArg = args.find(arg => arg.startsWith('--run-id='))?.split('=')[1];

if (!projectId) {
  console.error('Usage: npm run render <projectId> [--portrait] [--no-compress] [--run-id=<id>]');
  console.error('Example: npm run render agentSaasPromoVideo');
  console.error('Options:');
  console.error('  --portrait        Render in portrait mode (1080x1920)');
  console.error('  --no-compress     Skip video compression after rendering');
  console.error('  --run-id=<id>     Optional run id for unique output names');
  process.exit(1);
}

const WIDTH = isPortrait ? 1080 : 1920;
const HEIGHT = isPortrait ? 1920 : 1080;
const FPS = 30;
const BASE_PORT = 5175;
const orientation = isPortrait ? 'portrait' : 'landscape';

function createRunId() {
  const now = new Date();
  const ts = [
    now.getFullYear().toString(),
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0'),
    String(now.getHours()).padStart(2, '0'),
    String(now.getMinutes()).padStart(2, '0'),
    String(now.getSeconds()).padStart(2, '0')
  ].join('');
  return ts;
}

const runId = (runIdArg || process.env.RENDER_RUN_ID || createRunId()).replace(/[^a-zA-Z0-9._-]/g, '_');
const renderSuffix = `${orientation}-${runId}`;

const OUTPUT_DIR = path.resolve(process.cwd(), 'public', 'video');
const FRAMES_DIR = path.join(OUTPUT_DIR, `frames-${projectId}-${renderSuffix}`);
const FINAL_VIDEO = path.join(OUTPUT_DIR, `render-${projectId}-${renderSuffix}.mp4`);

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

if (fs.existsSync(FRAMES_DIR)) {
  fs.rmSync(FRAMES_DIR, { recursive: true, force: true });
}
fs.mkdirSync(FRAMES_DIR, { recursive: true });

function detectBrowserExecutable() {
  if (process.env.PUPPETEER_EXECUTABLE_PATH) return process.env.PUPPETEER_EXECUTABLE_PATH;

  const platform = os.platform();
  const arch = os.arch();

  // For x64 architecture, let Puppeteer handle it automatically
  if (arch === 'x64') return undefined;

  if (platform === 'darwin') {
    // macOS browser detection
    const macCandidates = [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
      '/usr/local/bin/chromium',
      '/usr/local/bin/google-chrome',
      '/opt/homebrew/bin/chromium',
      '/opt/homebrew/bin/google-chrome'
    ];

    for (const path of macCandidates) {
      try {
        if (fs.existsSync(path)) {
          console.log(`Found browser: ${path}`);
          return path;
        }
      } catch { }
    }

    // Try using which command for Homebrew installations
    const brewCandidates = [
      'chromium',
      'google-chrome',
      'brave-browser'
    ];

    for (const name of brewCandidates) {
      try {
        const result = execSync(`which ${name}`, { encoding: 'utf-8' }).trim();
        if (result) {
          console.log(`Found browser via which: ${result}`);
          return result;
        }
      } catch { }
    }
  } else {
    // Linux browser detection
    const linuxCandidates = [
      'brave-browser',
      'chromium-browser',
      'chromium',
      'google-chrome',
      'google-chrome-stable'
    ];

    for (const name of linuxCandidates) {
      try {
        const result = execSync(`which ${name}`, { encoding: 'utf-8' }).trim();
        if (result) {
          console.log(`Found browser: ${result}`);
          return result;
        }
      } catch { }
    }
  }

  console.warn('No suitable browser found, using Puppeteer default');
  return undefined;
}

async function findFreePort(startPort: number): Promise<number> {
  const { createServer } = await import('net');
  return new Promise((resolve, reject) => {
    const server = createServer();
    server.listen(startPort, () => {
      const port = (server.address() as any).port;
      server.close(() => resolve(port));
    });
    server.on('error', () => {
      findFreePort(startPort + 1).then(resolve).catch(reject);
    });
  });
}

async function main() {
  // Load project config to check expected audio count
  const projectConfigPath = path.resolve(process.cwd(), 'public', 'projects', `${projectId}.json`);

  if (!fs.existsSync(projectConfigPath)) {
    console.error(`❌ Project config not found: ${projectConfigPath}`);
    process.exit(1);
  }

  const projectConfig = JSON.parse(fs.readFileSync(projectConfigPath, 'utf-8'));
  const expectedAudioCount = projectConfig.clips.filter((c: any) => c.type !== 'transition' && c.speech).length;

  // Check if audio exists
  const audioDir = path.resolve(process.cwd(), 'public', 'projects', projectId, 'audio');
  const existingAudioFiles = fs.existsSync(audioDir)
    ? fs.readdirSync(audioDir).filter(f => f.endsWith('.mp3'))
    : [];

  const needsGeneration = existingAudioFiles.length < expectedAudioCount;

  if (needsGeneration) {
    console.log(`\n⚠️  Audio files incomplete for project "${projectId}"`);
    console.log(`   Expected: ${expectedAudioCount} files, Found: ${existingAudioFiles.length} files`);
    console.log(`📢 Generating audio using TTS...\n`);

    try {
      execSync(`npm run generate-audio ${projectId}`, { stdio: 'inherit' });
      console.log(`\n✅ Audio generation completed!\n`);
    } catch (error: any) {
      console.error(`\n❌ Failed to generate audio:`, error.message);
      console.error(`\nPlease run manually: npm run generate-audio ${projectId}`);
      process.exit(1);
    }
  } else {
    console.log(`✅ Audio files complete for project "${projectId}" (${existingAudioFiles.length}/${expectedAudioCount})`);
  }

  const PORT = await findFreePort(BASE_PORT);
  const BASE_URL = `http://localhost:${PORT}/?record=true&orientation=${orientation}&project=${projectId}`;

  console.log(`Starting Vite server on port ${PORT}...`);
  console.log(`Render run id: ${runId}`);
  console.log(`Frames dir: ${FRAMES_DIR}`);
  console.log(`Final video: ${FINAL_VIDEO}`);
  const server = spawn('npm', ['run', 'dev', '--', '--port', String(PORT)], {
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: true
  });

  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Server start timeout')), 20000);

    server.stdout?.on('data', (data) => {
      if (data.toString().includes('Local:') || data.toString().includes('ready in')) {
        clearTimeout(timeout);
        resolve();
      }
    });

    server.stderr?.on('data', (data) => {
      const msg = data.toString();
      if (msg.includes('EADDRINUSE')) {
        clearTimeout(timeout);
        reject(new Error(`Port ${PORT} is already in use`));
      }
    });
  });

  console.log('Launching browser for frame-by-frame rendering...');
  const executablePath = detectBrowserExecutable();
  const browser = await puppeteer.launch({
    headless: true,
    ...(executablePath ? { executablePath } : {}),
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      `--window-size=${WIDTH},${HEIGHT}`,
      '--ignore-gpu-blocklist',
      '--enable-gpu',
      '--enable-accelerated-2d-canvas',
      '--use-gl=egl',
      '--disable-dev-shm-usage',
      '--hide-scrollbars',
      '--mute-audio',
    ],
    defaultViewport: null
  });

  const page = await browser.newPage();
  page.setDefaultTimeout(180000);
  await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });

  console.log(`Navigating to ${BASE_URL}...`);
  await page.goto(BASE_URL, { waitUntil: 'domcontentloaded' });

  console.log('Waiting for app to be ready...');
  await Promise.race([
    page.waitForFunction(() => typeof (window as any).seekTo === 'function', { timeout: 30000 }),
    page.waitForSelector('.ready-to-record', { timeout: 30000 })
  ]);

  // Wait for audioInitialized to be set (record mode auto-initializes it)
  await page.waitForFunction(() => {
    // Check that renderState is actually computing (not empty)
    const seekTo = (window as any).seekTo;
    if (typeof seekTo !== 'function') return false;
    // Try seeking to 0 and check if the DOM has media content
    seekTo(0);
    return true;
  }, { timeout: 10000 });

  // Small wait for React to re-render after audioInitialized
  await new Promise(r => setTimeout(r, 500));

  // Prepare app for deterministic rendering
  await page.evaluate(() => {
    (window as any).suppressTTS = true;
  });

  const totalDuration = await page.evaluate(() => {
    return (window as any).getTotalDuration();
  });

  if (totalDuration === 0) {
    console.error('Project has 0 duration. Check your project config.');
    await browser.close();
    server.kill();
    process.exit(1);
  }

  console.log(`Total duration: ${totalDuration.toFixed(2)}s. Starting frame capture...`);
  const totalFrames = Math.ceil(totalDuration * FPS);

  for (let i = 0; i <= totalFrames; i++) {
    const time = i / FPS;

    await page.evaluate(`(async (t) => {
      document.documentElement.style.setProperty('--t', String(t));
      if (typeof window.seekTo === 'function') {
        window.seekTo(t);
        
        const iframes = Array.from(document.querySelectorAll('iframe'));
        if (iframes.length === 0) return;

        await Promise.all(iframes.map(iframe => {
          return new Promise((resolve) => {
            const handler = (event) => {
              if (event.data && event.data.type === 'iframeSynced') {
                window.removeEventListener('message', handler);
                resolve();
              }
            };
            window.addEventListener('message', handler);
            setTimeout(resolve, 500);
            try {
              iframe.contentWindow.document?.documentElement?.style?.setProperty('--t', String(t));
              iframe.contentWindow.postMessage({ type: 'seek', time: t }, '*');
            } catch (e) {
              resolve();
            }
          });
        }));
      } else {
        throw new Error('window.seekTo is not available');
      }
    })(${time})`);

    // Wait for React to paint the final state
    await new Promise(r => setTimeout(r, 100));

    if (i % 10 === 0) {
      process.stdout.write(`\rRendering frame ${i}/${totalFrames} (${((i / totalFrames) * 100).toFixed(1)}%)`);
    }

    const framePath = path.join(FRAMES_DIR, `frame-${String(i).padStart(5, '0')}.jpg`);
    await page.screenshot({
      path: framePath,
      type: 'jpeg',
      quality: 95,
      optimizeForSpeed: true
    });
  }

  process.stdout.write('\n');
  console.log('Capture complete. Closing browser...');

  const audioLog = await page.evaluate(() => {
    return (window as any).getAudioLog ? (window as any).getAudioLog() : [];
  });

  await browser.close();
  server.kill();

  if (audioLog.length === 0) {
    console.warn('No audio log found. Rendering video without audio...');
  }

  console.log('Assembling video with ffmpeg...');
  await assembleVideo(audioLog);

  console.log('\n🎬 Render pipeline completed!');
}

async function assembleVideo(audioLog: Array<{ file: string; startTime: number }>) {
  const tempVideo = path.join(OUTPUT_DIR, `temp_video_${projectId}_${renderSuffix}.mp4`);

  console.log('Step 1: Encoding frames...');
  spawnSync('ffmpeg', [
    '-y',
    '-framerate', String(FPS),
    '-start_number', '0',
    '-i', path.join(FRAMES_DIR, 'frame-%05d.jpg'),
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-r', String(FPS),
    tempVideo
  ], { stdio: 'inherit' });

  if (audioLog.length === 0) {
    console.warn('No audio found, saving video only.');
    fs.renameSync(tempVideo, FINAL_VIDEO);
    fs.rmSync(FRAMES_DIR, { recursive: true, force: true });
    console.log(`\nSuccess! Rendered video saved to: ${FINAL_VIDEO}`);
    return;
  }

  console.log('Step 2: Mixing audio...');
  const inputs = ['-i', tempVideo];
  const filterComplex: string[] = [];
  const audioMap: string[] = [];
  let validAudioCount = 0;

  for (let i = 0; i < audioLog.length; i++) {
    const log = audioLog[i];
    const audioPath = path.join(process.cwd(), 'public', 'projects', log.file);

    if (fs.existsSync(audioPath)) {
      inputs.push('-i', audioPath);
      validAudioCount++;
      const delay = Math.max(0, Math.round(log.startTime * 1000)); // Convert to milliseconds
      filterComplex.push(`[${validAudioCount}:a]adelay=${delay}|${delay}[a${validAudioCount}]`);
      audioMap.push(`[a${validAudioCount}]`);
    }
  }

  if (validAudioCount > 0) {
    filterComplex.push(`${audioMap.join('')}amix=inputs=${validAudioCount}:duration=longest:dropout_transition=0:normalize=0[aout]`);

    const ffmpegArgs = [
      '-y',
      ...inputs,
      '-filter_complex', filterComplex.join(';'),
      '-map', '0:v',
      '-map', '[aout]',
      '-c:v', 'copy',
      '-c:a', 'aac',
      '-b:a', '192k',
      FINAL_VIDEO
    ];

    console.log('Running final ffmpeg mix...');
    spawnSync('ffmpeg', ffmpegArgs, { stdio: 'inherit' });
  } else {
    console.warn('No valid audio files found, copying video only.');
    fs.renameSync(tempVideo, FINAL_VIDEO);
  }

  // Cleanup
  if (fs.existsSync(tempVideo)) fs.unlinkSync(tempVideo);
  fs.rmSync(FRAMES_DIR, { recursive: true, force: true });

  console.log(`\n✅ Rendered video saved to: ${FINAL_VIDEO}`);

  // Compress the video (unless --no-compress flag is set)
  if (!skipCompress) {
    console.log('\n🗜️  Starting video compression...');
    try {
      const compressResult = spawnSync('node', [
        path.join(process.cwd(), 'scripts', 'compress.js'),
        FINAL_VIDEO,
        '--crf=23',
        '--preset=medium'
      ], { stdio: 'inherit' });

      if (compressResult.status === 0) {
        const compressedFile = FINAL_VIDEO.replace('.mp4', '-compressed.mp4');
        console.log(`\n✅ Compressed video saved to: ${compressedFile}`);
      } else {
        console.warn(`\n⚠️  Compression failed, but original video is available at: ${FINAL_VIDEO}`);
      }
    } catch (error: any) {
      console.warn(`\n⚠️  Compression error: ${error.message}`);
      console.log(`Original video is available at: ${FINAL_VIDEO}`);
    }
  } else {
    console.log('\n⏭️  Skipping compression (--no-compress flag set)');
  }
}

main().catch(err => {
  console.error('Render failed:', err);
  process.exit(1);
});
