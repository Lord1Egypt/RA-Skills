#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = new URL('..', import.meta.url).pathname;
const DEFAULT_BASE_DIR = '/tmp/douyin-persona-usage-in-plan-stability';

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
          // Ignore non-JSON fragments.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function readJson(path, fallback = null) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function personaState(round) {
  const fields = {
    name: `张琳${round}`,
    sex: '女',
    work_year: '8',
    bissiness: '宠物保险顾问服务',
    advantage: '熟悉理赔流程，能把复杂条款讲清楚',
    segment: '一二线城市新手养宠家庭',
    trials: '亲和、专业、说话直接',
    cases: '服务过300多个养宠家庭，处理过多类理赔咨询',
    demand: '通过抖音建立专业信任，引导客户咨询宠物保险',
    taboos: '不夸大收益，不承诺一定理赔，表达要合规清晰',
  };
  return {
    version: 1,
    status: 'confirmed',
    fields,
    draft: null,
    confirmed: {
      generatedAt: new Date().toISOString(),
      confirmedAt: new Date().toISOString(),
      source: 'fixture',
      fields,
      summary: {
        personaId: `${fields.name}-宠物保险`,
        coreIdentity: '8年宠物保险顾问',
        audience: fields.segment,
        tone: fields.trials,
        value: fields.advantage,
        primaryPlatform: '抖音',
        slogan: '宠物险少踩坑',
      },
      strategy: '围绕宠物保险理赔坑、条款误区、新手养宠家庭决策焦虑展开。',
      marketing: '内容要聚焦新手养宠家庭，表达专业、直接、亲和，不夸大承诺。',
      contentRules: {
        pillars: ['理赔避坑', '条款拆解', '新手投保误区'],
        interactionTone: fields.trials,
        compliance: fields.taboos,
      },
    },
    history: [],
  };
}

function fixtureData() {
  return {
    works: [
      {
        fields: {
          标题: '宠物险理赔被拒的3个原因 #宠物险 #保险',
          播放量: 1200,
          点赞量: 88,
          评论量: 12,
          分享量: 6,
          '2秒跳出率%': 22,
          '5秒完播率%': 48,
        },
      },
      {
        fields: {
          标题: '新手养猫怎么买保险 #宠物险',
          播放量: 900,
          点赞量: 61,
          评论量: 9,
          分享量: 3,
          '2秒跳出率%': 28,
          '5秒完播率%': 42,
        },
      },
    ],
    daily: [
      {
        fields: {
          同步时间: '2026-05-20 10:00:00',
          总粉丝量: 100,
          昨日播放量: 2100,
          周期投稿量: 2,
          条均点击率: '8%',
          条均5s完播率: '45%',
          条均2s跳出率: '25%',
          条均播放时长: '8',
          建议摘要: '宠物险避坑类内容表现较好。',
        },
      },
    ],
    log: [
      {
        fields: {
          同步时间: '2026-05-20 10:00:00',
          近N天: 90,
          作品数: 2,
        },
      },
    ],
  };
}

function runRound(round, baseDir) {
  const stateDir = join(baseDir, `round-${round}`);
  rmSync(stateDir, { recursive: true, force: true });
  mkdirSync(stateDir, { recursive: true });
  const personaPath = join(stateDir, 'persona-state.json');
  const fixturePath = join(stateDir, 'bitable-fixture.json');
  const outputPath = join(stateDir, 'plan.json');
  writeFileSync(personaPath, `${JSON.stringify(personaState(round), null, 2)}\n`);
  writeFileSync(fixturePath, `${JSON.stringify(fixtureData(), null, 2)}\n`);
  const result = spawnSync(process.execPath, [
    'scripts/douyin-next-video-plan-from-bitable.js',
    '--fixture-json',
    fixturePath,
    '--persona-state',
    personaPath,
    '--days',
    '90',
    '--output',
    outputPath,
  ], {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 180000,
    env: {
      ...process.env,
      DOUYIN_MONITOR_STATE_DIR: stateDir,
      DOUYIN_PERSONA_STATE_PATH: personaPath,
      DOUYIN_NEXT_VIDEO_PLAN_LLM: 'off',
    },
  });
  const payload = parseJsonObjects(`${result.stderr || ''}${result.stdout || ''}`).at(-1) || readJson(outputPath, {});
  const text = JSON.stringify(payload);
  const issues = [];
  if (result.status !== 0 || payload?.ok !== true) issues.push('command_failed');
  if (!payload.personaUsed) issues.push('persona_not_used');
  if (!/宠物保险|宠物险/.test(text)) issues.push('business_missing');
  if (!/新手养宠家庭|养宠/.test(text)) issues.push('audience_missing');
  if (!/亲和|专业|直接/.test(text)) issues.push('tone_missing');
  if (!payload.plan?.digitalHumanInput?.scriptText) issues.push('script_missing');
  return { round, ok: issues.length === 0, issues, outputPath, payload };
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
  const failed = results.filter((item) => !item.ok);
  const summary = {
    ok: failed.length === 0,
    rounds,
    passed: results.length - failed.length,
    failed: failed.length,
    failures: failed.map((item) => ({ round: item.round, issues: item.issues })),
  };
  const reportPath = join(baseDir, `persona-usage-in-plan-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
