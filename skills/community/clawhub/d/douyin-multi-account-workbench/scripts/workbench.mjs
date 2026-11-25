import { access, mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const SKILLS_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

export const TASK_TO_SKILL = {
  'hot-topic': 'douyin-live-hot-free',
  diagnosis: 'douyin-account-diagnosis',
  'comment-insights': 'douyin-comment-insights-free',
  'competitor-research': 'douyin-competitor-research-free',
  script: 'builtin-script-draft'
};

export const OPTIONAL_SKILLS = [
  'douyin-live-hot-free',
  'douyin-account-diagnosis',
  'douyin-comment-insights-free',
  'douyin-competitor-research-free'
];

// Keep the old export name for callers that used the previous package API.
export const REQUIRED_SKILLS = OPTIONAL_SKILLS;

export const DEPENDENCY_INSTALLS = {
  'douyin-live-hot-free': {
    repository: 'https://github.com/xxjrq/douyin-live-hot-free',
    installCommand: 'npx skills add xxjrq/douyin-live-hot-free'
  },
  'douyin-account-diagnosis': {
    repository: 'https://github.com/xxjrq/douyin-account-diagnosis',
    installCommand: 'npx skills add xxjrq/douyin-account-diagnosis'
  },
  'douyin-comment-insights-free': {
    repository: 'https://github.com/xxjrq/douyin-comment-insights-free',
    installCommand: 'npx skills add xxjrq/douyin-comment-insights-free'
  },
  'douyin-competitor-research-free': {
    repository: 'https://github.com/xxjrq/douyin-competitor-research-free',
    installCommand: 'npx skills add xxjrq/douyin-competitor-research-free'
  }
};

export const ATOMIC_SCRIPTS = {
  'douyin-live-hot-free': 'scripts/douyin-live-hot-free.mjs',
  'douyin-account-diagnosis': 'scripts/diagnose.mjs',
  'douyin-comment-insights-free': 'scripts/douyin-comment-insights-free.mjs',
  'douyin-competitor-research-free': 'scripts/douyin-competitor-research-free.mjs'
};

export function dependencyRoot(rootDir = process.env.CODEX_SKILLS_DIR || process.env.SKILL_FACTORY_SKILLS_DIR || SKILLS_ROOT) {
  return path.resolve(rootDir);
}

export async function dependencyStatus(rootDir = dependencyRoot()) {
  const root = dependencyRoot(rootDir);
  const status = {};
  for (const skill of REQUIRED_SKILLS) {
    const dir = path.join(root, skill);
    try {
      await access(path.join(dir, 'SKILL.md'));
      await access(path.join(dir, ATOMIC_SCRIPTS[skill]));
      status[skill] = { installed: true, dir, script: path.join(dir, ATOMIC_SCRIPTS[skill]), ...DEPENDENCY_INSTALLS[skill] };
    } catch {
      status[skill] = { installed: false, dir, script: path.join(dir, ATOMIC_SCRIPTS[skill]), ...DEPENDENCY_INSTALLS[skill] };
    }
  }
  return status;
}

export async function validateDependencies(rootDir = dependencyRoot()) {
  const mapped = new Set(Object.values(TASK_TO_SKILL));
  for (const dependency of REQUIRED_SKILLS) {
    if (!mapped.has(dependency)) throw new Error(`缺少原子 Skill 依赖映射：${dependency}`);
  }
  const status = await dependencyStatus(rootDir);
  // Atomic Skills are optional. The caller reports missing task dependencies
  // and continues with tasks whose dependencies are installed.
  return status;
}

export function buildScriptDraft(account, input = {}, results = []) {
  const topic = String(input.topic || input.hotTopic || input.brief || '根据公开内容研究结果整理一个可验证的抖音选题').trim();
  const suggestions = results.flatMap((item) => item.result?.topicSuggestions || item.result?.differentiationOpportunities || []).filter(Boolean);
  const lead = suggestions[0];
  return {
    title: String(lead?.title || `${topic.slice(0, 22)}：${account.id || account.accountId || '账号'}的可执行思路`).slice(0, 34),
    hook: lead?.hook || `如果你也在做${topic}，先看这一个具体动作。`,
    body: [lead?.observation ? `先展示公开样本里的${lead.observation}。` : '先展示公开页面能看到的事实或动作。', lead?.action ? `再把它改成自己的动作：${lead.action}。` : '再说明为什么值得尝试，并标出需要自己核验的部分。', '最后给出一个账号可以马上执行的小步骤。'],
    cta: '收藏这条，按自己的素材实测一次。',
    evidencePolicy: '只使用当前账号公开页面证据，不复制他人原文，不承诺流量或收益。',
    accountId: account.id || account.accountId
  };
}

export function validateInput(input) {
  if (!input || !Array.isArray(input.accounts) || input.accounts.length === 0) throw new Error('accounts 必须是非空数组');
  const ids = new Set();
  const browsers = new Set();
  for (const account of input.accounts) {
    if (!account || !account.id || !account.accountUrl || !account.browserId) throw new Error('每个账号必须有 id、accountUrl、browserId');
    if (ids.has(account.id)) throw new Error(`重复账号 id：${account.id}`);
    if (browsers.has(account.browserId)) throw new Error(`重复 browserId：${account.browserId}`);
    ids.add(account.id);
    browsers.add(account.browserId);
  }
  const tasks = input.tasks || ['hot-topic', 'diagnosis', 'comment-insights', 'competitor-research', 'script'];
  if (!Array.isArray(tasks) || tasks.some((task) => !TASK_TO_SKILL[task])) throw new Error('tasks 只允许 hot-topic、diagnosis、comment-insights、competitor-research、script');
  return {
    schemaVersion: '1.0',
    mode: input.mode === 'mock' ? 'mock' : 'real',
    accounts: input.accounts,
    tasks,
    topic: input.topic || null,
    hotTopic: input.hotTopic || null,
    keyword: input.keyword || null,
    keywords: Array.isArray(input.keywords) ? input.keywords : [],
    workUrl: input.workUrl || null,
    snapshotFixture: input.snapshotFixture || null,
    audience: input.audience || null,
    niche: input.niche || null,
    sampleLimit: input.sampleLimit || 8,
    limit: input.limit || 10,
    works: Array.isArray(input.works) ? input.works : []
  };
}

export function createExecutionPlan(input) {
  const normalized = validateInput(input);
  return normalized.accounts.map((account) => ({
    accountId: account.id,
    browserId: account.browserId,
    accountUrl: account.accountUrl,
    session: `douyin-workbench-${account.id}`,
    groupTitle: `Douyin Workbench · ${account.id}`,
      tasks: normalized.tasks.map((task) => ({ task, skill: TASK_TO_SKILL[task], mode: normalized.mode }))
  }));
}

export function aggregateResults(input, results, timestamps = {}) {
  const plan = createExecutionPlan(input);
  const resultMap = new Map((results || []).map((result) => [result.accountId, result]));
  const accounts = plan.map((entry) => {
    const result = resultMap.get(entry.accountId);
    const status = result?.status || 'failed';
    return {
      id: entry.accountId,
      browserId: entry.browserId,
      status,
      results: result?.results || [],
      evidence: result?.evidence || [],
      error: result?.error || null,
      session: entry.session,
      scriptDraft: result?.scriptDraft || buildScriptDraft(entry, input)
    };
  });
  return {
    schemaVersion: '1.0',
    mode: input.mode === 'mock' ? 'mock' : 'real',
    startedAt: timestamps.startedAt || new Date().toISOString(),
    finishedAt: timestamps.finishedAt || new Date().toISOString(),
    accounts,
    summary: {
      total: accounts.length,
      completed: accounts.filter((account) => account.status === 'completed').length,
      partial: accounts.filter((account) => account.status === 'partial').length,
      needsUserAction: accounts.filter((account) => account.status === 'needs_user_action').length,
      failed: accounts.filter((account) => account.status === 'failed').length,
      unavailableTasks: accounts.reduce((total, account) => total + account.results.filter((result) => result.status === 'unavailable').length, 0)
    },
    limitations: input.mode === 'mock' ? ['本次结果来自 mock fixture，不代表线上平台数据。'] : []
  };
}

export function renderMarkdown(report) {
  const lines = [
    '# 抖音多账号内容协同报告',
    '',
    `模式：${report.mode}；账号：${report.summary.total}；完成：${report.summary.completed}；部分：${report.summary.partial}；需处理：${report.summary.needsUserAction}；失败：${report.summary.failed}`,
    ''
  ];
  for (const account of report.accounts) {
    lines.push(`## ${account.id}`, '', `- browserId：${account.browserId}`, `- 状态：${account.status}`, `- session：${account.session}`);
    if (account.results.length) lines.push(`- 子任务：${account.results.map((result) => result.task || result.skill || 'unknown').join('、')}`);
    if (account.evidence.length) lines.push(`- 证据数量：${account.evidence.length}`);
    if (account.error) lines.push(`- 错误：${account.error}`);
    for (const result of account.results.filter((item) => item.status === 'unavailable')) {
      lines.push(`- 不可用任务：${result.task} 需要未安装的 ${result.skill}。安装：${result.installCommand}（${result.repository}）`);
    }
    if (account.scriptDraft) {
      lines.push(`- 脚本标题：${account.scriptDraft.title}`, `- 开场钩子：${account.scriptDraft.hook}`, `- 正文：${account.scriptDraft.body.join(' ')}`, `- 行动引导：${account.scriptDraft.cta}`);
    }
    lines.push('');
  }
  if (report.limitations.length) lines.push('## 局限', ...report.limitations.map((item) => `- ${item}`), '');
  return `${lines.join('\n')}\n`;
}

function parseArgs(argv) {
  const [verb = 'help', ...rest] = argv;
  const options = {};
  for (let index = 0; index < rest.length; index += 1) {
    const flag = rest[index];
    if (!flag.startsWith('--')) throw new Error(`不支持参数：${flag}`);
    const key = flag.slice(2).replaceAll('-', '_');
    const value = rest[index + 1];
    if (!value || value.startsWith('--')) throw new Error(`参数 ${flag} 缺少值`);
    options[key] = value;
    index += 1;
  }
  return { verb, options };
}

export async function listConnectedBrowsers({ baseUrl = process.env.EASY_WEBBRIDGE_URL || 'http://127.0.0.1:17777', tokenFile = process.env.EASY_WEBBRIDGE_TOKEN_FILE || path.join(process.env.HOME || '', '.easy-webbridge', 'bridge-token') } = {}) {
  let token = '';
  try { token = (await readFile(tokenFile, 'utf8')).trim(); } catch { throw new Error('找不到 Easy WebBridge Token 文件'); }
  if (!token) throw new Error('Easy WebBridge Token 文件为空');
  const response = await fetch(`${baseUrl.replace(/\/$/, '')}/v1/browsers`, { headers: { Accept: 'application/json', Authorization: `Bearer ${token}` } });
  if (!response.ok) throw new Error(`Easy WebBridge 浏览器列表失败（HTTP ${response.status}）`);
  const body = await response.json();
  return (Array.isArray(body.browsers) ? body.browsers : []).filter((browser) => browser?.online && browser.browserId).map((browser) => ({ browserId: browser.browserId, displayName: browser.displayName || browser.browser || browser.browserId, browser: browser.browser || null }));
}

async function bridgeCommand(browserId, action, args, session) {
  const baseUrl = (process.env.EASY_WEBBRIDGE_URL || 'http://127.0.0.1:17777').replace(/\/$/, '');
  const tokenFile = process.env.EASY_WEBBRIDGE_TOKEN_FILE || path.join(process.env.HOME || '', '.easy-webbridge', 'bridge-token');
  let token = '';
  try { token = (await readFile(tokenFile, 'utf8')).trim(); } catch { throw new Error('找不到 Easy WebBridge Token 文件'); }
  const response = await fetch(`${baseUrl}/v1/browsers/${encodeURIComponent(browserId)}/commands`, { method: 'POST', headers: { Accept: 'application/json', 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify({ action, args: { ...args, session }, timeoutMs: 20_000 }) });
  if (!response.ok) throw new Error(`Easy WebBridge 命令失败（HTTP ${response.status}）`);
  const body = await response.json();
  return body.result;
}

async function collectAccountWorks(account, input) {
  if (input.mode === 'mock') return input.works || [];
  const session = account.session;
  const navigation = await bridgeCommand(account.browserId, 'navigate', { url: account.accountUrl, newTab: true, active: true, groupTitle: account.groupTitle }, session);
  const tabId = navigation?.tabId || navigation?.id;
  if (!tabId) throw new Error('账号页导航未返回 tabId');
  await new Promise((resolve) => setTimeout(resolve, 1200));
  const page = await bridgeCommand(account.browserId, 'evaluate', { tabId, code: `(() => { const text = document.body?.innerText || ''; const blocked = /登录|验证码|安全验证|风控|访问受限/i.test(text); const links = [...document.querySelectorAll('a[href*="/video/"],a[href*="/note/"]')]; return { blocked, sourceUrl: location.href, works: links.slice(0, 30).map((a) => ({ url: new URL(a.href, location.href).href, title: a.innerText.trim() || null })).filter((item) => item.url) }; })()` }, session);
  if (page?.blocked) throw new Error('账号页需要登录或验证');
  if (!Array.isArray(page?.works)) throw new Error('账号页没有可见作品样本');
  return page.works.map((work) => ({ ...work, sourceUrl: page.sourceUrl }));
}

async function runAtomic(task, account, input, outputDir, dependencyMap) {
  if (task === 'script') return { task, status: 'completed', result: buildScriptDraft(account, input) };
  const skill = TASK_TO_SKILL[task];
  const dependency = dependencyMap[skill];
  if (!dependency?.installed) return {
    task,
    skill,
    status: 'unavailable',
    error: `依赖未安装：${skill}`,
    installCommand: dependency?.installCommand || null,
    repository: dependency?.repository || null
  };
  const accountId = account.accountId || account.id;
  const taskDir = path.join(outputDir, accountId, task);
  await mkdir(taskDir, { recursive: true });
  const childEnv = { ...process.env, EASY_WEBBRIDGE_SESSION: account.session, EASY_WEBBRIDGE_GROUP_TITLE: account.groupTitle };
  try {
    if (task === 'hot-topic') {
      const keyword = String(input.keyword || input.topic || 'AI工具').trim();
      await execFileAsync(process.execPath, [dependency.script, 'search', '--keyword', keyword, '--browser-id', account.browserId, '--limit', String(input.limit || 10), '--output', taskDir], { timeout: 120_000, env: childEnv });
    } else if (task === 'competitor-research') {
      const requestPath = path.join(taskDir, 'request.json');
      const request = { runtime: input.mode === 'mock' ? 'mock' : 'easy-webbridge', accountAlias: accountId, accountUrl: account.accountUrl, keywords: input.keywords || [], sampleLimit: Math.min(20, Math.max(1, input.sampleLimit || 8)), browserId: account.browserId, audience: input.audience, niche: input.niche };
      await writeFile(requestPath, `${JSON.stringify(request, null, 2)}\n`);
      if (request.runtime === 'mock' && input.snapshotFixture) {
        await execFileAsync(process.execPath, [dependency.script, 'collect', '--request', requestPath, '--input', input.snapshotFixture, '--output', taskDir], { timeout: 120_000, env: childEnv });
      } else {
        await execFileAsync(process.execPath, [dependency.script, 'collect', '--request', requestPath, '--output', taskDir], { timeout: 120_000, env: childEnv });
      }
      await execFileAsync(process.execPath, [dependency.script, 'analyze', '--snapshot', path.join(taskDir, 'research-snapshot.json'), '--output', taskDir], { timeout: 120_000, env: childEnv });
    } else if (task === 'diagnosis') {
      const inputPath = path.join(taskDir, 'request.json');
      const works = await collectAccountWorks(account, input);
      await writeFile(inputPath, `${JSON.stringify({ mode: input.mode, accountUrl: account.accountUrl, browserId: account.browserId, works }, null, 2)}\n`);
      const result = await execFileAsync(process.execPath, [dependency.script, inputPath], { timeout: 120_000, env: childEnv });
      await writeFile(path.join(taskDir, 'account-diagnosis.json'), result.stdout);
    } else if (task === 'comment-insights') {
      if (!input.workUrl) return { task, status: 'needs_user_action', error: 'comment-insights 需要 workUrl' };
      await execFileAsync(process.execPath, [dependency.script, 'analyze', '--url', input.workUrl, '--browser-id', account.browserId, '--output', taskDir], { timeout: 120_000, env: childEnv });
    }
    const outputFiles = { 'hot-topic': 'search-results.json', 'competitor-research': 'competitor-research.json', diagnosis: 'account-diagnosis.json', 'comment-insights': 'douyin-comment-insights.json' };
    let result = null;
    if (outputFiles[task]) {
      try { result = JSON.parse(await readFile(path.join(taskDir, outputFiles[task]), 'utf8')); } catch { result = null; }
      if (!result) return { task, skill, status: 'failed', error: `缺少或无法读取预期结果：${outputFiles[task]}` };
    }
    return { task, skill, status: 'completed', outputDir: taskDir, evidence: [taskDir], result };
  } catch (error) {
    const message = String(error?.message || error).replace(/Bearer\s+[^\s]+/gi, 'Bearer [redacted]');
    const status = /登录|验证码|风控|安全验证|访问受限|需要.*处理|未登录|权限不足/i.test(message) ? 'needs_user_action' : 'failed';
    return { task, skill, status, error: message };
  }
}

export async function runWorkbench(input, { outputDir, rootDir, runAtoms = true } = {}) {
  if (!outputDir) throw new Error('outputDir is required');
  const normalized = validateInput(input);
  const dependencies = await validateDependencies(rootDir);
  const plan = createExecutionPlan(normalized);
  const startedAt = new Date().toISOString();
  const accounts = await Promise.all(plan.map(async (entry) => {
    const results = [];
    try {
      if (runAtoms) {
        // 同一 browserId 复用同一标签组并串行操作；不同账号在外层并行。
        for (const item of entry.tasks) results.push(await runAtomic(item.task, entry, normalized, outputDir, dependencies));
      } else {
        results.push(...entry.tasks.map((item) => ({ task: item.task, skill: item.skill, status: 'completed', mode: 'mock' })));
      }
    } finally {
      if (runAtoms && normalized.mode === 'real') {
        try { await bridgeCommand(entry.browserId, 'close_session', {}, entry.session); } catch { /* 保留原始任务结果 */ }
      }
    }
    const failed = results.filter((result) => result.status === 'failed');
    const needsUserAction = results.filter((result) => result.status === 'needs_user_action');
    const completed = results.filter((result) => result.status === 'completed');
    const unavailable = results.filter((result) => result.status === 'unavailable');
    const status = failed.length && completed.length || needsUserAction.length && completed.length || unavailable.length ? 'partial' : failed.length ? 'failed' : needsUserAction.length ? 'needs_user_action' : 'completed';
    return { accountId: entry.accountId, status, results, evidence: results.flatMap((result) => result.evidence || []), scriptDraft: buildScriptDraft(entry, normalized, results), error: failed[0]?.error || needsUserAction[0]?.error || unavailable[0]?.error || null };
  }));
  const usedTitles = new Set();
  for (let index = 0; index < accounts.length; index += 1) {
    const account = accounts[index];
    const draft = account.scriptDraft;
    const baseTitle = draft.title;
    const title = usedTitles.has(baseTitle) ? `${baseTitle.slice(0, 26)}｜${account.accountId}专属角度` : baseTitle;
    usedTitles.add(title);
    account.scriptDraft = { ...draft, title, differentiation: { comparedWith: accounts.slice(0, index).map((item) => item.accountId), selectedAngle: index ? `${account.accountId} 使用与前序账号不同的切入角度` : `${account.accountId} 作为首个基准角度` } };
  }
  const report = aggregateResults(normalized, accounts, { startedAt, finishedAt: new Date().toISOString() });
  await mkdir(outputDir, { recursive: true });
  await writeFile(path.join(outputDir, 'multi-account-workbench.json'), `${JSON.stringify(report, null, 2)}\n`);
  await writeFile(path.join(outputDir, 'multi-account-workbench.md'), renderMarkdown(report));
  return report;
}

async function main(argv = process.argv.slice(2)) {
  const { verb, options } = parseArgs(argv);
  if (verb === 'list') {
    console.log(JSON.stringify({ status: 'success', browsers: await listConnectedBrowsers() }, null, 2));
    return;
  }
  if (verb === 'dependencies') {
    console.log(JSON.stringify({ status: 'success', dependencies: await dependencyStatus(options.root_dir || dependencyRoot()) }, null, 2));
    return;
  }
  if (verb === 'plan') {
    const input = JSON.parse(await readFile(options.input, 'utf8'));
    console.log(JSON.stringify({ status: 'success', plan: createExecutionPlan(input) }, null, 2));
    return;
  }
  if (verb === 'run') {
    if (!options.input || !options.output) throw new Error('run 需要 --input 和 --output');
    const input = JSON.parse(await readFile(options.input, 'utf8'));
    const report = await runWorkbench(input, { outputDir: options.output, rootDir: options.root_dir || dependencyRoot() });
    console.log(JSON.stringify({ status: 'success', output: options.output, summary: report.summary }, null, 2));
    return;
  }
  console.log('用法：node scripts/workbench.mjs dependencies [--root-dir skills-dir]\n      node scripts/workbench.mjs plan --input request.json\n      node scripts/workbench.mjs run --input request.json --output output-dir');
}

if (import.meta.url === `file://${process.argv[1]}`) main().catch((error) => { console.error(error.message); process.exit(1); });
