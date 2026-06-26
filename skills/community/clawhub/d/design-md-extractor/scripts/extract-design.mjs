#!/usr/bin/env node
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { chromium } from 'playwright';

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillDir = resolve(__dirname, '..');
const coreDir = resolve(skillDir, 'lib', 'design-extractor-core');
const require = createRequire(import.meta.url);
const core = require(resolve(coreDir, 'index.js'));
const sampler = require(resolve(coreDir, 'browser-sampler.js'));

const options = parseArgs(process.argv.slice(2));

if (!options.url) {
  fail('Missing --url. Example: node scripts/extract-design.mjs --url https://example.com --out ./design.md');
}

const outPath = resolve(process.cwd(), options.out ?? 'design.md');
const snapshotPath = options.snapshot ? resolve(process.cwd(), options.snapshot) : undefined;
const viewport = parseViewport(options.viewport ?? '1440x900');
const timeoutMs = Number(options.timeout ?? 30000);

const executablePath =
  options['executable-path'] ?? process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ?? findBrowserExecutable();
const browser = await chromium.launch({
  headless: true,
  ...(executablePath ? { executablePath } : {}),
});

try {
  const page = await browser.newPage({ viewport });
  await page.goto(options.url, { waitUntil: 'domcontentloaded', timeout: timeoutMs });
  await page.waitForLoadState('networkidle', { timeout: Math.min(timeoutMs, 10000) }).catch(() => undefined);
  await page.evaluate(() => document.fonts?.ready).catch(() => undefined);

  const rawAnalysis = await page.evaluate(`(${sampler.getBrowserSamplerSource()})()`);
  const snapshot = core.buildDesignSnapshot(rawAnalysis);
  const designMd = core.generateDesignMd(snapshot);

  await writeText(outPath, designMd);

  if (snapshotPath) {
    await writeText(snapshotPath, `${JSON.stringify(snapshot, null, 2)}\n`);
  }

  console.log(JSON.stringify({
    ok: true,
    url: options.url,
    out: outPath,
    snapshot: snapshotPath,
    hostname: snapshot.meta.hostname,
    primary: snapshot.tokens.colors.primary.value,
    visibleElements: snapshot.raw.elementCounts.totalVisible,
  }, null, 2));
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
} finally {
  await browser.close();
}

function parseArgs(args) {
  const parsed = {};

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (!arg.startsWith('--')) continue;

    const key = arg.slice(2);
    const value = args[index + 1];
    if (!value || value.startsWith('--')) {
      parsed[key] = 'true';
      continue;
    }

    parsed[key] = value;
    index += 1;
  }

  return parsed;
}

function parseViewport(value) {
  const match = /^(\d+)x(\d+)$/.exec(value);
  if (!match) {
    fail(`Invalid --viewport "${value}". Expected format like 1440x900.`);
  }

  return {
    width: Number(match[1]),
    height: Number(match[2]),
  };
}

function findBrowserExecutable() {
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  ];

  return candidates.find((candidate) => existsSync(candidate));
}

async function writeText(path, text) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, text, 'utf8');
}

function fail(message) {
  console.error(JSON.stringify({ ok: false, error: message }, null, 2));
  process.exit(1);
}
