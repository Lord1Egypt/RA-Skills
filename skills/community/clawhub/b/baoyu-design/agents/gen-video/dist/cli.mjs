#!/usr/bin/env node

// src/cli.ts
import { existsSync, readFileSync } from "node:fs";
import { resolve as resolve2 } from "node:path";
import { spawn as spawn2 } from "node:child_process";

// src/orchestrator/run.ts
import { stat } from "node:fs/promises";

// src/orchestrator/encode.ts
import { spawn } from "node:child_process";
function buildFfmpegArgs(o) {
  const scale = `scale=${o.width}:${o.height}:flags=lanczos`;
  const base = ["-y", "-f", "image2pipe", "-c:v", "png", "-r", String(o.fps), "-i", "pipe:0"];
  if (o.format === "webm") {
    return [
      ...base,
      "-vf",
      scale,
      "-c:v",
      "libvpx-vp9",
      "-b:v",
      "0",
      "-crf",
      String(o.crf),
      "-pix_fmt",
      "yuv420p",
      "-r",
      String(o.fps),
      o.outPath
    ];
  }
  if (o.format === "gif") {
    return [
      ...base,
      "-vf",
      `${scale},split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5`,
      "-r",
      String(o.fps),
      o.outPath
    ];
  }
  return [
    ...base,
    "-vf",
    scale,
    "-c:v",
    "libx264",
    "-preset",
    "slow",
    "-crf",
    String(o.crf),
    "-pix_fmt",
    "yuv420p",
    "-movflags",
    "+faststart",
    "-r",
    String(o.fps),
    o.outPath
  ];
}
var FfmpegEncoder = class {
  child;
  stderr = "";
  exited;
  constructor(opts) {
    this.child = spawn("ffmpeg", buildFfmpegArgs(opts), { stdio: ["pipe", "ignore", "pipe"] });
    this.child.stderr?.on("data", (d) => {
      this.stderr += d.toString();
      if (this.stderr.length > 8e3) this.stderr = this.stderr.slice(-8e3);
    });
    this.child.stdin?.on("error", () => {
    });
    this.exited = new Promise((resolve3, reject) => {
      this.child.on("error", reject);
      this.child.on("close", (code) => {
        if (code === 0) resolve3();
        else {
          const tail = this.stderr.trim().split("\n").slice(-3).join(" ");
          reject(new Error(`ffmpeg exited with code ${code}: ${tail}`));
        }
      });
    });
  }
  async writeFrame(buf) {
    const stdin = this.child.stdin;
    if (!stdin.write(buf)) {
      await new Promise((resolve3) => stdin.once("drain", resolve3));
    }
  }
  async finish() {
    this.child.stdin.end();
    await this.exited;
  }
  destroy() {
    try {
      this.child.kill("SIGKILL");
    } catch {
    }
  }
};

// src/orchestrator/output.ts
import { mkdir } from "node:fs/promises";
import { join, resolve } from "node:path";

// src/orchestrator/filename.ts
function safeBasename(filename, fallback) {
  const cleaned = (filename ?? "").normalize("NFC").replace(/[^\p{L}\p{N}\-_. ]/gu, "_").replace(/\s+/g, " ").replace(/^[.\s]+|[.\s]+$/g, "");
  return cleaned || fallback;
}

// src/orchestrator/output.ts
async function resolveOutputPath(outDir, filename, format) {
  const ext = format === "webm" ? "webm" : format === "gif" ? "gif" : "mp4";
  const base = safeBasename(filename, "video").replace(new RegExp(`\\.${ext}$`, "i"), "") || "video";
  const name = `${base}.${ext}`;
  const dir = resolve(outDir);
  await mkdir(dir, { recursive: true });
  return join(dir, name);
}

// src/orchestrator/errors.ts
function stringifyError(err) {
  if (err instanceof Error) return err.message;
  try {
    return String(err);
  } catch {
    return "unknown error";
  }
}
function timeoutHint(message, phase) {
  if (!/timed?\s*out|timeout/i.test(message)) return "";
  if (phase === "bridge") {
    return ". The page never exposed the timeline bridge \u2014 confirm the URL serves the animation, that animations.jsx loaded, and that bridgeGlobal matches the page's global.";
  }
  if (phase === "encode") {
    return ". ffmpeg stalled while encoding \u2014 confirm ffmpeg is healthy and the output directory is writable.";
  }
  return ". Frame capture stalled \u2014 the animation may be too heavy per frame; try a lower fps or deviceScaleFactor.";
}

// src/validate/validate.ts
function validate(f) {
  const flags = [];
  if (f.duration <= 0) {
    flags.push({
      kind: "zero_duration",
      message: "Resolved animation duration was 0 \u2014 pass an explicit duration (seconds) in the config, or expose bridge.duration. Only a single frame was rendered."
    });
  }
  if (!f.fontsReady) {
    flags.push({
      kind: "fonts_timeout",
      message: "document.fonts.ready did not resolve within 8s \u2014 frames may use fallback fonts. Check that font URLs are reachable."
    });
  }
  if (!f.captureActive && !f.hasFallback) {
    flags.push({
      kind: "capture_mode_off",
      message: "Capture mode did not engage and no hideSelectors/resetTransformSelector fallback was given \u2014 frames may include the scrubber and letterboxing. Load the page with ?capture, re-copy starter-components/animations.jsx, or pass hideSelectors + resetTransformSelector."
    });
  }
  if (f.frameCount >= 8 && f.duplicateFrames > f.frameCount * 0.85) {
    flags.push({
      kind: "duplicate_frames",
      message: `${f.duplicateFrames}/${f.frameCount} frames were identical to their predecessor \u2014 almost nothing changed across the timeline, so seeking likely isn't advancing (wrong bridgeGlobal, or setTime isn't wired) or the page is static. (Some duplicate frames are normal during deliberate held beats.)`
    });
  }
  return flags;
}

// src/orchestrator/run.ts
var SETUP_RACE_MS = 8e3;
async function waitForSetup(driver, bridgeGlobal) {
  return await driver.page.evaluate(
    async ({ g, timeout }) => {
      const deadline = Date.now() + timeout;
      const get = () => window[g];
      while (Date.now() < deadline) {
        const b2 = get();
        if (b2 && typeof b2.setTime === "function") break;
        await new Promise((r) => setTimeout(r, 50));
      }
      const b = get();
      const hasBridge = !!(b && typeof b.setTime === "function");
      let fontsReady = false;
      try {
        const remaining = Math.max(0, deadline - Date.now());
        await Promise.race([
          document.fonts.ready.then(() => {
            fontsReady = true;
          }),
          new Promise((r) => setTimeout(r, remaining))
        ]);
      } catch {
        fontsReady = true;
      }
      let bridgeDuration = null;
      let captureActive = false;
      if (hasBridge && b) {
        try {
          const d = b.duration;
          if (typeof d === "number" && isFinite(d)) bridgeDuration = d;
        } catch {
        }
        try {
          captureActive = !!b.captureActive;
        } catch {
        }
      }
      return { hasBridge, fontsReady, bridgeDuration, captureActive };
    },
    { g: bridgeGlobal, timeout: SETUP_RACE_MS }
  );
}
async function applyChromeFallback(driver, hide, reset, width, height) {
  await driver.page.evaluate(
    ({ hide: hide2, reset: reset2, w, h }) => {
      const style = document.createElement("style");
      let css = "*{transition:none !important;}";
      for (const sel of hide2) css += `${sel}{display:none !important;}`;
      if (reset2) {
        css += `${reset2}{transform:none !important;box-shadow:none !important;width:${w}px !important;height:${h}px !important;}`;
      }
      style.setAttribute("data-genvideo", "1");
      style.textContent = css;
      document.head.appendChild(style);
      if (reset2) {
        const el = document.querySelector(reset2);
        const parent = el && el.parentElement;
        if (parent) {
          parent.style.setProperty("align-items", "flex-start", "important");
          parent.style.setProperty("justify-content", "flex-start", "important");
          parent.style.setProperty("overflow", "visible", "important");
        }
      }
      document.documentElement.style.background = "transparent";
      document.body.style.background = "transparent";
    },
    { hide, reset, w: width, h: height }
  );
  await driver.page.evaluate(
    () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(() => r())))
  );
}
function quickHash(buf) {
  let v = 5381;
  const mid = buf.length >> 1;
  const end = Math.min(buf.length, mid + 4096);
  for (let i = mid; i < end; i++) v = (v << 5) + v + buf[i] | 0;
  return v >>> 0;
}
async function runGenVideo(input, driver, outDir) {
  const fps = Math.max(1, Math.round(input.fps ?? 30));
  const format = input.format ?? "mp4";
  const crf = input.crf ?? 18;
  const bridgeGlobal = input.bridgeGlobal ?? "__animStage";
  const setup = await waitForSetup(driver, bridgeGlobal);
  if (!setup.hasBridge) {
    throw new Error(
      `genVideo: no timeline bridge at window.${bridgeGlobal}. The page must expose a bridge with setTime()/duration \u2014 re-copy starter-components/animations.jsx (it registers window.__animStage), or set bridgeGlobal to the page's global (e.g. "__ahe").${timeoutHint("timed out", "bridge")}`
    );
  }
  await driver.page.evaluate((g) => {
    const b = window[g];
    try {
      b?.setPlaying?.(false);
    } catch {
    }
  }, bridgeGlobal);
  const duration = input.duration ?? setup.bridgeDuration ?? 0;
  const startMs = Math.max(0, input.startMs ?? 0);
  const endMs = input.endMs ?? duration * 1e3;
  const totalMs = Math.max(0, endMs - startMs);
  const frameCount = Math.max(1, Math.round(totalMs / 1e3 * fps));
  const hasFallback = (input.hideSelectors?.length ?? 0) > 0 || !!input.resetTransformSelector;
  if (!setup.captureActive && hasFallback) {
    await applyChromeFallback(
      driver,
      input.hideSelectors ?? [],
      input.resetTransformSelector ?? null,
      input.width,
      input.height
    );
  }
  const outPath = await resolveOutputPath(outDir, input.filename, format);
  const encoder = new FfmpegEncoder({
    format,
    width: input.width,
    height: input.height,
    fps,
    crf,
    outPath
  });
  let prevHash = -1;
  let dupCount = 0;
  try {
    for (let i = 0; i < frameCount; i++) {
      const tSec = (startMs + i * 1e3 / fps) / 1e3;
      await driver.seek(bridgeGlobal, tSec);
      const buf = await driver.screenshotBuffer();
      const h = quickHash(buf);
      if (i > 0 && h === prevHash) dupCount++;
      prevHash = h;
      await encoder.writeFrame(buf);
    }
  } catch (err) {
    encoder.destroy();
    const msg = stringifyError(err);
    throw new Error(`genVideo: frame capture failed: ${msg}${timeoutHint(msg, "capture")}`);
  }
  try {
    await encoder.finish();
  } catch (err) {
    const msg = stringifyError(err);
    throw new Error(`genVideo: ffmpeg failed: ${msg}${timeoutHint(msg, "encode")}`);
  }
  const { size } = await stat(outPath);
  const validation = validate({
    fontsReady: setup.fontsReady,
    captureActive: setup.captureActive,
    hasFallback,
    duplicateFrames: dupCount,
    frameCount,
    duration
  });
  return {
    file: outPath,
    result: {
      bytes: size,
      frames: frameCount,
      fps,
      duration,
      width: input.width,
      height: input.height,
      validation,
      warnings: []
    }
  };
}

// src/orchestrator/driver.ts
var PlaywrightDriver = class _PlaywrightDriver {
  browser;
  context;
  page;
  constructor(browser, context, page) {
    this.browser = browser;
    this.context = context;
    this.page = page;
  }
  static async launch(url, opts) {
    const { chromium } = await import("playwright");
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: opts.width, height: opts.height },
      deviceScaleFactor: opts.deviceScaleFactor ?? 2
    });
    const page = await context.newPage();
    page.setDefaultTimeout(opts.timeout ?? 3e4);
    await page.goto(url, { waitUntil: "load", timeout: opts.timeout ?? 3e4 });
    return new _PlaywrightDriver(browser, context, page);
  }
  /** Raw full-viewport PNG bytes (fed straight to ffmpeg's stdin). */
  async screenshotBuffer() {
    return await this.page.screenshot({ type: "png" });
  }
  /** Drive the timeline bridge to time `t` (seconds), then settle two rAFs. */
  async seek(bridgeGlobal, t) {
    await this.page.evaluate(
      ({ g, time }) => {
        const b = window[g];
        if (b && typeof b.setTime === "function") b.setTime(time);
        return new Promise(
          (r) => requestAnimationFrame(() => requestAnimationFrame(() => r()))
        );
      },
      { g: bridgeGlobal, time: t }
    );
  }
  async close() {
    try {
      await this.context.close();
    } catch {
    }
    try {
      await this.browser.close();
    } catch {
    }
  }
};

// src/cli.ts
var SETUP_HINT = "cd <skill>/agents/gen-video && npm install && npx playwright install chromium\n  (ffmpeg must also be on PATH: `brew install ffmpeg` on macOS, `apt install ffmpeg` on Linux)";
function usage(msg) {
  process.stderr.write(
    `${msg}

Usage: gen-video --url <servedAnimationUrl> --config <jsonPath|-> [--out <dir>]
`
  );
  process.exit(64);
}
function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--url") out.url = argv[++i];
    else if (a === "--config") out.config = argv[++i];
    else if (a === "--out") out.out = argv[++i];
    else if (a === "-h" || a === "--help") usage("gen-video");
    else usage(`Unknown argument: ${a}`);
  }
  if (!out.url) usage("Missing --url");
  if (!out.config) usage("Missing --config");
  if (!/^https?:\/\//i.test(out.url)) {
    usage("--url must be an http(s) URL (multi-file animations need a served origin, not file://)");
  }
  return out;
}
async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}
function withCaptureParam(url, param) {
  try {
    const u = new URL(url);
    u.searchParams.set(param, "1");
    return u.toString();
  } catch {
    return url;
  }
}
function ffmpegAvailable() {
  return new Promise((resolve3) => {
    const child = spawn2("ffmpeg", ["-version"], { stdio: "ignore" });
    child.on("error", () => resolve3(false));
    child.on("close", (code) => resolve3(code === 0));
  });
}
async function preflight() {
  const major = parseInt(process.versions.node.split(".")[0] ?? "0", 10);
  if (major < 18) {
    process.stderr.write(`gen-video: node >= 18 required (found ${process.versions.node}).
`);
    process.exit(1);
  }
  let pw;
  try {
    pw = await import("playwright");
  } catch {
    process.stderr.write(`gen-video: playwright is not installed.
One-time setup:
  ${SETUP_HINT}
`);
    process.exit(1);
  }
  let exe = "";
  try {
    exe = pw.chromium.executablePath();
  } catch {
  }
  if (!exe || !existsSync(exe)) {
    process.stderr.write(`gen-video: Chromium browser is not installed.
One-time setup:
  ${SETUP_HINT}
`);
    process.exit(1);
  }
  if (!await ffmpegAvailable()) {
    process.stderr.write(
      `gen-video: ffmpeg is not installed or not on PATH.
One-time setup:
  brew install ffmpeg   # macOS
  apt install ffmpeg    # Debian/Ubuntu
`
    );
    process.exit(1);
  }
}
async function main() {
  const args = parseArgs(process.argv.slice(2));
  await preflight();
  const raw = args.config === "-" ? await readStdin() : readFileSync(resolve2(args.config), "utf8");
  let input;
  try {
    input = JSON.parse(raw);
  } catch (err) {
    usage(`--config is not valid JSON: ${err instanceof Error ? err.message : String(err)}`);
  }
  if (!input || typeof input.width !== "number" || typeof input.height !== "number") {
    usage("config must include numeric width and height");
  }
  const captureParam = input.captureParam ?? "capture";
  const url = withCaptureParam(args.url, captureParam);
  const driver = await PlaywrightDriver.launch(url, {
    width: input.width,
    height: input.height,
    deviceScaleFactor: input.deviceScaleFactor ?? 2
  });
  try {
    const { result, file } = await runGenVideo(input, driver, args.out ?? process.cwd());
    process.stdout.write(
      JSON.stringify({
        ok: true,
        file,
        frames: result.frames,
        fps: result.fps,
        duration: result.duration,
        width: result.width,
        height: result.height,
        bytes: result.bytes,
        flags: result.validation.map((v) => ({ code: v.kind, message: v.message })),
        warnings: result.warnings
      }) + "\n"
    );
    process.exit(0);
  } catch (err) {
    process.stdout.write(
      JSON.stringify({ ok: false, error: err instanceof Error ? err.message : String(err) }) + "\n"
    );
    process.exit(1);
  } finally {
    await driver.close();
  }
}
main().catch((err) => {
  process.stdout.write(
    JSON.stringify({ ok: false, error: err instanceof Error ? err.message : String(err) }) + "\n"
  );
  process.exit(1);
});
