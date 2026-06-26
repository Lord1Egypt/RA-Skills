import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  connectOpenClawBrowser,
  createPreparedPage,
  disconnectBrowser,
  waitForNewPage,
  DEFAULT_BROWSER_URL,
} from './lib/openclaw-browser.mjs';
import { createRecorder, ensureDir, stopRecorder } from './lib/recorder.mjs';
import { clickByPoint, humanMove, humanType, smoothScrollTo, clearFocusedInput } from './lib/human-actions.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_ROOT = path.resolve(__dirname, '..');
const WORKSPACE_ROOT = process.env.OPENCLAW_WORKSPACE || path.resolve(SKILL_ROOT, '..', '..');
const DEFAULT_MEDIA_DIR = path.join(WORKSPACE_ROOT, 'media');

function usage() {
  console.error('Usage: node scripts/run-recording.mjs <plan.json>');
  process.exit(1);
}

function slugify(value) {
  return String(value || 'recording')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80) || 'recording';
}

function timestampForFile(date = new Date()) {
  return date.toISOString().replace(/[:.]/g, '-');
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function summarizePlan(plan) {
  return {
    title: plan?.meta?.title || null,
    outputBasename: plan?.meta?.outputBasename || null,
    stepCount: Array.isArray(plan?.steps) ? plan.steps.length : 0,
  };
}

function buildPaths(plan) {
  const baseName = slugify(plan?.meta?.outputBasename || plan?.meta?.title || 'browser-demo');
  const stamp = timestampForFile();
  const mediaDir = path.resolve(plan?.meta?.outputDir || DEFAULT_MEDIA_DIR);
  ensureDir(mediaDir);
  return {
    mediaDir,
    videoPath: path.join(mediaDir, `${baseName}-${stamp}.mp4`),
    debugPath: path.join(mediaDir, `${baseName}-${stamp}.json`),
  };
}

async function waitForFunctionValue(page, fn, args = [], options = {}) {
  const { timeout = 20000, polling = 200 } = options;
  const handle = await page.waitForFunction(fn, { timeout, polling }, ...args);
  return await handle.jsonValue();
}

async function resolveTarget(page, target) {
  if (!target) {
    throw new Error('Missing step target');
  }

  if (typeof target.x === 'number' && typeof target.y === 'number') {
    return {
      source: 'point',
      x: target.x,
      y: target.y,
      rect: {
        x: target.x,
        y: target.y,
        width: 0,
        height: 0,
      },
    };
  }

  const match = await page.evaluate((target) => {
    const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
    const candidates = [...document.querySelectorAll(target.selector || 'a,button,input,textarea,[role="button"],h1,h2,h3,h4,h5,h6,div,span')];

    const filtered = candidates
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const text = normalize(el.innerText || el.textContent || el.getAttribute('aria-label') || el.getAttribute('placeholder'));
        return {
          tag: el.tagName,
          text,
          href: el.href || null,
          selectorMatch: target.selector ? el.matches(target.selector) : false,
          rect: {
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height,
          },
        };
      })
      .filter((item) => item.rect.width > 0 && item.rect.height > 0);

    const visible = filtered.filter((item) => item.rect.y + item.rect.height > 0 && item.rect.y < window.innerHeight);
    const pool = visible.length ? visible : filtered;
    const matches = pool.filter((item) => {
      if (target.tag && item.tag !== String(target.tag).toUpperCase()) return false;
      if (target.href && item.href !== target.href) return false;
      if (target.text && item.text !== target.text) return false;
      if (target.textIncludes && !item.text.includes(target.textIncludes)) return false;
      return true;
    });

    const candidate = matches[target.index || 0] || null;
    if (!candidate) return null;

    return {
      ...candidate,
      x: candidate.rect.x + candidate.rect.width / 2 + (target.offsetX || 0),
      y: candidate.rect.y + candidate.rect.height / 2 + (target.offsetY || 0),
    };
  }, target);

  if (!match) {
    throw new Error(`Failed to resolve target: ${JSON.stringify(target)}`);
  }

  return {
    source: 'dom',
    ...match,
  };
}

async function maybeWaitForUrl(page, step) {
  if (step.waitForUrlIncludes) {
    await page.waitForFunction(
      (needle) => location.href.includes(needle),
      { timeout: step.timeoutMs || 30000 },
      step.waitForUrlIncludes
    );
  }

  if (step.waitForUrlEquals) {
    await page.waitForFunction(
      (url) => location.href === url,
      { timeout: step.timeoutMs || 30000 },
      step.waitForUrlEquals
    );
  }
}

async function executeStep(context, step, index) {
  let { browser, page, interactionLog } = context;
  const note = step.note || null;
  const common = { index, type: step.type, note, url: page.url() };

  if (step.type === 'goto') {
    interactionLog.steps.push({ ...common, url: step.url });
    await page.goto(step.url, {
      waitUntil: step.waitUntil || 'networkidle2',
      timeout: step.timeoutMs || 60000,
    });
    await maybeWaitForUrl(page, step);
    if (step.holdMs) await page.waitForTimeout(step.holdMs);
    return { browser, page, interactionLog };
  }

  if (step.type === 'hold') {
    interactionLog.steps.push({ ...common, ms: step.ms });
    await page.waitForTimeout(step.ms || 1000);
    return { browser, page, interactionLog };
  }

  if (step.type === 'evaluate') {
    interactionLog.steps.push({ ...common, code: step.code });
    await page.evaluate(
      ({ code, args }) => {
        const fn = new Function(`return (${code});`)();
        return fn(args || {});
      },
      { code: step.code, args: step.args || {} }
    );
    if (step.holdMs) await page.waitForTimeout(step.holdMs);
    return { browser, page, interactionLog };
  }

  if (step.type === 'move') {
    if (Array.isArray(step.points) && step.points.length) {
      interactionLog.steps.push({ ...common, points: step.points });
      for (const point of step.points) {
        if (typeof point.x === 'number' && typeof point.y === 'number') {
          await humanMove(page, point.x, point.y, point.steps || step.steps || 24);
        } else {
          const resolved = await resolveTarget(page, point.target || point);
          await humanMove(page, resolved.x, resolved.y, point.steps || step.steps || 24);
        }
        if (point.waitMs) await page.waitForTimeout(point.waitMs);
      }
    } else {
      const resolved = await resolveTarget(page, step.target || step);
      interactionLog.steps.push({ ...common, target: resolved });
      await humanMove(page, resolved.x, resolved.y, step.steps || 24);
    }
    if (step.holdMs) await page.waitForTimeout(step.holdMs);
    return { browser, page, interactionLog };
  }

  if (step.type === 'scroll') {
    let targetY = step.targetY;
    let targetInfo = null;

    if (typeof targetY !== 'number') {
      targetInfo = await waitForFunctionValue(
        page,
        (target, offsetY) => {
          const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
          const nodes = [...document.querySelectorAll(target.selector || 'a,button,input,textarea,[role="button"],h1,h2,h3,h4,h5,h6,div,span')];
          const el = nodes.find((node) => {
            const text = normalize(node.innerText || node.textContent || node.getAttribute('aria-label') || node.getAttribute('placeholder'));
            if (target.tag && node.tagName !== String(target.tag).toUpperCase()) return false;
            if (target.href && node.href !== target.href) return false;
            if (target.text && text !== target.text) return false;
            if (target.textIncludes && !text.includes(target.textIncludes)) return false;
            return true;
          });
          if (!el) return null;
          const rect = el.getBoundingClientRect();
          return {
            targetScrollY: Math.max(0, window.scrollY + rect.y + (offsetY || 0)),
            rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
          };
        },
        [step.target, step.offsetY || 0],
        { timeout: step.timeoutMs || 20000 }
      );
      targetY = targetInfo.targetScrollY;
    }

    interactionLog.steps.push({ ...common, targetY, target: targetInfo || step.target || null });
    await smoothScrollTo(page, targetY, {
      stepY: step.stepY || 96,
      stepWaitMs: step.stepWaitMs,
      durationMs: step.durationMs,
      moveSteps: step.moveSteps || 10,
      anchorX: step.anchorX,
      anchorY: step.anchorY,
    });
    if (step.holdMs) await page.waitForTimeout(step.holdMs);
    return { browser, page, interactionLog };
  }

  if (step.type === 'type') {
    const resolved = await resolveTarget(page, step.target);
    interactionLog.steps.push({ ...common, target: resolved, text: step.text });
    await clickByPoint(page, resolved.x, resolved.y, {
      moveSteps: step.moveSteps || 24,
      holdMs: step.holdMsBeforeType || 70,
    });
    if (step.clear !== false) {
      await clearFocusedInput(page);
      await page.waitForTimeout(120);
    }
    await humanType(page, step.text || '', { delay: step.delay || 120 });
    if (step.submit) await page.keyboard.press('Enter');
    if (step.holdMs) await page.waitForTimeout(step.holdMs);
    return { browser, page, interactionLog };
  }

  if (step.type === 'press') {
    interactionLog.steps.push({ ...common, key: step.key });
    await page.keyboard.press(step.key);
    if (step.holdMs) await page.waitForTimeout(step.holdMs);
    return { browser, page, interactionLog };
  }

  if (step.type === 'click') {
    const resolved = await resolveTarget(page, step.target);
    interactionLog.steps.push({
      ...common,
      target: resolved,
      switchToNewPage: !!step.switchToNewPage,
      waitForNavigation: !!step.waitForNavigation,
    });

    let navigationPromise = null;
    let newPagePromise = null;

    if (step.waitForNavigation) {
      navigationPromise = page.waitForNavigation({
        waitUntil: step.waitUntil || 'networkidle2',
        timeout: step.timeoutMs || 60000,
      });
    }

    if (step.switchToNewPage) {
      newPagePromise = waitForNewPage(browser, {
        width: step.viewport?.width || interactionLog.meta.viewport.width,
        height: step.viewport?.height || interactionLog.meta.viewport.height,
        deviceScaleFactor: interactionLog.meta.viewport.deviceScaleFactor,
        interactionLog,
        timeoutMs: step.timeoutMs || 10000,
      });
    }

    await clickByPoint(page, resolved.x, resolved.y, {
      moveSteps: step.moveSteps || 24,
      holdMs: step.holdMsBeforeUp || 80,
    });

    if (navigationPromise) {
      await navigationPromise;
    }

    if (newPagePromise) {
      const nextPage = await newPagePromise;
      page = nextPage;
      await page.waitForTimeout(step.newPageHoldMs || 800);
    }

    await maybeWaitForUrl(page, step);
    if (step.holdMs) await page.waitForTimeout(step.holdMs);
    return { browser, page, interactionLog };
  }

  throw new Error(`Unsupported step type: ${step.type}`);
}

async function main() {
  const planPath = process.argv[2];
  if (!planPath) usage();

  const absolutePlanPath = path.resolve(process.cwd(), planPath);
  const plan = readJson(absolutePlanPath);
  if (!Array.isArray(plan.steps) || plan.steps.length === 0) {
    throw new Error('Plan must include a non-empty steps array');
  }

  const browserURL = plan?.meta?.browserURL || DEFAULT_BROWSER_URL;
  const viewport = {
    width: plan?.meta?.viewport?.width || 1600,
    height: plan?.meta?.viewport?.height || 1200,
    deviceScaleFactor: plan?.meta?.viewport?.deviceScaleFactor || 1,
  };
  const paths = buildPaths(plan);

  const interactionLog = {
    meta: {
      generatedAt: new Date().toISOString(),
      browserURL,
      viewport,
      plan: summarizePlan(plan),
      outputFiles: {
        videoFileName: path.basename(paths.videoPath),
        debugFileName: path.basename(paths.debugPath),
      },
    },
    steps: [],
  };

  let browser = null;
  let page = null;
  let recorder = null;
  let config = null;

  try {
    browser = await connectOpenClawBrowser(browserURL);
    page = await createPreparedPage(browser, {
      ...viewport,
      interactionLog,
    });

    ({ recorder, config } = createRecorder(page, viewport));
    interactionLog.meta.videoFrame = { ...config.videoFrame };

    await recorder.start(paths.videoPath);

    let state = { browser, page, interactionLog };
    for (let index = 0; index < plan.steps.length; index += 1) {
      state = await executeStep(state, plan.steps[index], index);
    }

    interactionLog.result = {
      ok: true,
      finalUrl: state.page.url(),
      videoPath: paths.videoPath,
      debugPath: paths.debugPath,
    };
    fs.writeFileSync(paths.debugPath, JSON.stringify(interactionLog, null, 2));
    console.log(JSON.stringify(interactionLog.result, null, 2));
  } catch (error) {
    interactionLog.error = {
      message: error.message,
      stack: error.stack,
      currentUrl: page ? page.url() : null,
    };
    fs.writeFileSync(paths.debugPath, JSON.stringify(interactionLog, null, 2));
    console.error(JSON.stringify({
      ok: false,
      videoPath: paths.videoPath,
      debugPath: paths.debugPath,
      error: error.message,
      currentUrl: page ? page.url() : null,
    }, null, 2));
    process.exitCode = 1;
  } finally {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    await stopRecorder(recorder);
    if (page) await page.close().catch(() => {});
    if (browser) await disconnectBrowser(browser);
  }
}

await main();
