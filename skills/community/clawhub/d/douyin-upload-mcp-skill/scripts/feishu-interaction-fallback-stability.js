#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = join(dirname(new URL(import.meta.url).pathname), '..');
const DEFAULT_BASE_DIR = '/tmp/douyin-feishu-interaction-fallback-stability';

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

function readJsonl(path) {
  if (!existsSync(path)) return [];
  return readFileSync(path, 'utf8')
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function personaState() {
  const fields = {
    name: '张琳',
    photo: 'https://example.com/person.jpg',
    sex: '女',
    work_year: '8',
    bissiness: '宠物保险顾问服务',
    advantage: '熟悉理赔流程，能把复杂条款讲清楚',
    segment: '新手养宠家庭',
    trials: '亲和、专业、说话直接',
    cases: '服务过300多个养宠家庭',
    demand: '通过抖音建立专业信任',
    taboos: '不夸大收益，不承诺一定理赔',
  };
  return {
    version: 1,
    status: 'confirmed',
    fields,
    confirmed: {
      fields,
      summary: {
        coreIdentity: '8年宠物保险顾问',
        audience: '新手养宠家庭',
        tone: '亲和、专业、说话直接',
        value: '把复杂条款讲清楚',
      },
      strategy: '测试人设战略定位方案',
      marketing: '测试IP营销策划方案',
      confirmedAt: new Date().toISOString(),
    },
  };
}

function pendingReviewMarketingState() {
  const publishText = [
    'tags:#测试#回归',
    '"封面图片": "https://example.com/cover.png"',
    '标题："待审核视频"',
    '"视频地址": "https://example.com/video.mp4"',
  ].join('\n');
  return {
    enabled: true,
    confirmationMode: 'manual',
    publishMode: 'manual_confirm',
    pendingReview: {
      runId: 'pending-review-regression',
      planSource: 'persona_first_video',
      publishText,
      videoUrl: 'https://example.com/video.mp4',
      planTitle: '待审核视频',
      createdAt: new Date().toISOString(),
    },
  };
}

function pendingUpstreamRecoveryState(stateDir) {
  const taskPath = join(stateDir, 'upstream-tasks', 'publish-task-recovery.json');
  const inputPath = join(stateDir, 'upstream-tasks', 'upstream-recovery.json');
  mkdirSync(dirname(taskPath), { recursive: true });
  writeFileSync(taskPath, `${JSON.stringify({
    metadata: { title: '恢复发布任务' },
    media: { videoPath: join(stateDir, 'upstream', 'video.mp4') },
  }, null, 2)}\n`);
  writeFileSync(inputPath, `${JSON.stringify({ title: '恢复发布任务' }, null, 2)}\n`);
  return {
    enabled: true,
    confirmationMode: 'manual',
    publishMode: 'manual_confirm',
    pendingReview: null,
    lastRun: {
      status: 'submitted',
      stage: 'publish_confirmed_video',
      publishPayload: {
        ok: true,
        result: {
          action: 'upstream_task_waiting_login_qr',
          pendingUpstreamTask: {
            taskPath,
            inputPath,
            title: '恢复发布任务',
            videoPath: join(stateDir, 'upstream', 'video.mp4'),
            coverImagePath: null,
          },
        },
      },
    },
  };
}

function runRoute(testCase, round, index, baseDir) {
  const text = testCase.text;
  const stateDir = join(baseDir, `round-${round}-${index}`);
  const logPath = join(stateDir, 'feishu-dry-run.jsonl');
  rmSync(stateDir, { recursive: true, force: true });
  mkdirSync(stateDir, { recursive: true });
  if (/怎么回复客户/.test(text)) {
    writeFileSync(join(stateDir, 'persona-state.json'), `${JSON.stringify(personaState(), null, 2)}\n`);
  }
  if (testCase.pendingReview) {
    writeFileSync(join(stateDir, 'automation-marketing-state.json'), `${JSON.stringify(pendingReviewMarketingState(), null, 2)}\n`);
  }
  if (testCase.pendingUpstreamRecovery) {
    writeFileSync(join(stateDir, 'automation-marketing-state.json'), `${JSON.stringify(pendingUpstreamRecoveryState(stateDir), null, 2)}\n`);
  }
  const result = spawnSync(process.execPath, [
    'scripts/feishu-reply-watcher.js',
    'route-text',
    '--text',
    text,
    '--dry-run',
    '--reset',
  ], {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 900000,
    env: {
      ...process.env,
      DOUYIN_MONITOR_STATE_DIR: stateDir,
      DOUYIN_FEISHU_WATCH_STATE: join(stateDir, 'feishu-reply-watcher-state.json'),
      DOUYIN_PERSONA_STATE_PATH: join(stateDir, 'persona-state.json'),
      DOUYIN_MARKETING_STATE_PATH: join(stateDir, 'automation-marketing-state.json'),
      FEISHU_DRY_RUN: 'true',
      DOUYIN_ROUTE_LIGHT_TEST: 'true',
      FEISHU_DRY_RUN_LOG: logPath,
    },
  });
  return {
    text,
    status: result.status,
    payload: parseJsonObjects(`${result.stderr || ''}${result.stdout || ''}`).at(-1) || null,
    messages: readJsonl(logPath),
    stdoutTail: result.stdout.slice(-1200),
    stderrTail: result.stderr.slice(-1200),
  };
}

const CASES = [
  { text: '同步数据', expect: /数据已更新：近 \d+ 天，作品 \d+ 条。/ },
  { text: '数据报表', expect: /^老板，昨日数据报告如下，请您查收～\n数据报告：已同步近 \d+ 天作品明细/ },
  { text: '生成选题', expectAction: /next_video_plan_light_test/ },
  { text: '回复互动', expect: /^自动回复完成：评论 \d+ 条，私信 \d+ 条。$/ },
  { text: '开启营销', expect: /^老板好~✨ 打造个人IP，最关键的是打造无可替代的差异化人设/ },
  { text: '绑定数字人ID', expect: /^请发送：绑定数字人ID xxxxx$/ },
  { text: '数字人ID：CUSTOMER123456', expect: /^数字人ID已绑定/ },
  { text: '训练数字人', expect: /已确认人设|本人照片链接/ },
  { text: '照片：https://example.com/t.jpg', expect: /已确认人设/ },
  { text: '视频地址：https://example.com/a.mp4', expect: /^发布任务信息不完整，还缺：标题。/ },
  { text: '标题：测试视频', expect: /^发布任务信息不完整，还缺：视频地址。/ },
  {
    text: '发布视频\n标题："待审核视频"\n"视频地址": "https://example.com/video.mp4"',
    pendingReview: true,
    expectAction: /^marketing_video_review_waiting$/,
    expect: /^视频已生成。确认发布请回复：确认发布；需要修改请回复：不通过 \+ 修改意见。$/,
  },
  {
    text: '通过',
    pendingReview: true,
    expectAction: /^marketing_video_review_waiting_explicit_confirm$/,
    expect: /^视频已生成。若确认发布，请回复：确认发布；若需修改，请回复：不通过 \+ 修改意见。$/,
  },
  {
    text: [
      '不通过，开头太短了，请重新生成一个更通顺的版本。',
      '老板，您的视频制作完成！请您审核：',
      '视频标题：待审核视频',
      '视频地址：https://example.com/video.mp4',
      '回复【确认发布】或【不通过】，若不通过，请指出修改建议～',
    ].join('\n'),
    pendingReview: true,
    expectAction: /^marketing_video_regeneration_started_light_test$/,
    expect: /^老板，收到修改意见，正在重新制作视频，请稍等～$/,
  },
  {
    text: '确认发布',
    pendingReview: true,
    expectAction: /^marketing_controller$/,
    expectPayloadAction: /^publish_pending_review_dry_run$/,
    expectNoCustomerText: true,
  },
  {
    text: '已登录',
    pendingUpstreamRecovery: true,
    expectAction: /^publish_upstream_task_dry_run$/,
    expectNoCustomerText: true,
  },
  { text: '怎么回复客户问理赔难不难', expect: /^以“8年宠物保险顾问”的人设来回复：/ },
  { text: '完全看不懂的命令', expect: /^未识别这条指令。/ },
];

function customerText(run) {
  return run.messages.filter((item) => item.type === 'text').map((item) => item.text).join('\n');
}

function validate(run, testCase) {
  const text = customerText(run);
  const issues = [];
  if (run.status !== 0 || run.payload?.ok !== true) issues.push('route_failed');
  if (run.messages.filter((item) => item.type === 'text').length > 1) issues.push('duplicate_text_messages');
  if (/stack|TypeError|ReferenceError|SyntaxError|node:|at\s+\w+/i.test(text)) issues.push('internal_detail_leaked');
  if (testCase.expectNoCustomerText && text) issues.push('unexpected_customer_text');
  if (testCase.expect && !testCase.expect.test(text)) issues.push('unexpected_customer_text');
  if (testCase.expectAction && !testCase.expectAction.test(String(run.payload?.result?.action || ''))) issues.push('unexpected_action');
  if (testCase.expectPayloadAction && !testCase.expectPayloadAction.test(String(run.payload?.result?.payload?.action || ''))) issues.push('unexpected_payload_action');
  if (!text && !testCase.expectAction && !testCase.expectNoCustomerText) issues.push('missing_customer_text');
  return {
    ...run,
    customerText: text,
    expected: String(testCase.expect || testCase.expectAction || ''),
    issues,
    pass: issues.length === 0,
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const rounds = Number(args.rounds || 3);
  const baseDir = args.stateDir || DEFAULT_BASE_DIR;
  rmSync(baseDir, { recursive: true, force: true });
  mkdirSync(baseDir, { recursive: true });
  const results = [];
  for (let round = 1; round <= rounds; round += 1) {
    CASES.forEach((item, index) => {
      results.push(validate(runRoute(item, round, index + 1, baseDir), item));
    });
  }
  const failed = results.filter((item) => !item.pass);
  const summary = {
    ok: failed.length === 0,
    rounds,
    cases: CASES.length,
    total: results.length,
    passed: results.length - failed.length,
    failed: failed.length,
    failures: failed.map((item) => ({
      text: item.text,
      issues: item.issues,
      customerText: item.customerText,
      action: item.payload?.result?.action,
    })),
  };
  const reportPath = join(baseDir, `feishu-interaction-fallback-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
