#!/usr/bin/env node
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = join(dirname(new URL(import.meta.url).pathname), '..');
const DEFAULT_BASE_DIR = '/tmp/douyin-xiaoice-publish-fields-stability';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function parseJsonObjects(text) {
  const objects = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  const raw = String(text || '');
  for (let i = 0; i < raw.length; i += 1) {
    const ch = raw[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        try {
          objects.push(JSON.parse(raw.slice(start, i + 1)));
        } catch {
          // Ignore logs.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function writeInput(path) {
  const input = {
    modelId: 'CVHPZJ4LCGBMNIZULS0',
    title: '自动营销真实稳定性测试3',
    publishTitle: '自动营销真实稳定性测试3',
    videoTitle: '稳定测试',
    visualTitle: '稳定测试',
    coverText: '稳定测试',
    scriptText: '这是第3轮数字人自动化营销真实接口稳定性测试。',
    tags: ['#自动化营销', '#数字人', '#稳定性测试'],
    digitalHumanInput: {
      modelId: 'CVHPZJ4LCGBMNIZULS0',
      title: '自动营销真实稳定性测试3',
      publishTitle: '自动营销真实稳定性测试3',
      videoTitle: '稳定测试',
      visualTitle: '稳定测试',
      coverText: '稳定测试',
      scriptText: '这是第3轮数字人自动化营销真实接口稳定性测试。',
      tags: ['#自动化营销', '#数字人', '#稳定性测试'],
    },
  };
  writeFileSync(path, `${JSON.stringify(input, null, 2)}\n`);
}

function runRound(round, baseDir) {
  const stateDir = join(baseDir, `round-${round}`);
  rmSync(stateDir, { recursive: true, force: true });
  mkdirSync(stateDir, { recursive: true });
  const inputPath = join(stateDir, 'xiaoice-input.json');
  writeInput(inputPath);
  const result = spawnSync(process.execPath, [
    'scripts/xiaoice-video-produce.js',
    'create-and-wait',
    '--input-json',
    inputPath,
    '--dry-run',
    '--fake-video-url',
    'https://example.com/video.mp4',
    '--fake-cover-image-url',
    'https://example.com/cover.png',
  ], {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 180000,
    env: {
      ...process.env,
      DOUYIN_MONITOR_STATE_DIR: stateDir,
    },
  });
  const payload = parseJsonObjects(`${result.stderr || ''}${result.stdout || ''}`).at(-1) || {};
  const title = String(payload.request?.title || '');
  const topic = String(payload.request?.topic || '');
  const publishText = String(payload.publishText || '');
  const issues = [];
  if (result.status !== 0 || payload.ok !== true) issues.push('command_failed');
  if (Array.from(title).length > 8) issues.push('visual_title_too_long');
  if (/发布标题/.test(topic)) issues.push('long_publish_title_in_topic');
  if (!/"封面图片": "https:\/\/example\.com\/cover\.png"/.test(publishText)) issues.push('cover_missing_from_publish_text');
  if (!/"视频地址": "https:\/\/example\.com\/video\.mp4"/.test(publishText)) issues.push('video_missing_from_publish_text');
  if (!/标题："自动营销真实稳定性测试3"/.test(publishText)) issues.push('publish_title_missing');
  return { round, pass: issues.length === 0, issues, payload };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const rounds = Number(args.rounds || 3);
  const baseDir = args.stateDir || DEFAULT_BASE_DIR;
  rmSync(baseDir, { recursive: true, force: true });
  mkdirSync(baseDir, { recursive: true });
  const results = [];
  for (let round = 1; round <= rounds; round += 1) {
    results.push(runRound(round, baseDir));
  }
  const failed = results.filter((item) => !item.pass);
  const summary = {
    ok: failed.length === 0,
    rounds,
    passed: results.length - failed.length,
    failed: failed.length,
    failures: failed.map((item) => ({ round: item.round, issues: item.issues })),
  };
  const reportPath = join(baseDir, `xiaoice-publish-fields-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
