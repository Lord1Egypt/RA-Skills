#!/usr/bin/env node
'use strict';
/**
 * cli.js — B站视频稿互动数采集 CLI (能力: b_collect, 自包含)。
 *
 * 输入 B站视频链接 → 平台调度内网浏览器节点打开视频页解析 SSR
 * window.__INITIAL_STATE__ (videoData + stat) → 拿到七项互动数
 * (播放/弹幕/评论/收藏/投币/分享/点赞) + 标题/简介/UP主信息。
 *
 * 计费: 1 视频 = 1 点数; 稿件删除/私密不返还, 服务侧失败全额返还。
 *
 * 输出规约 (对齐 ks-collect): stdout 只输出 JSON, 提示走 stderr。
 * 退出码: 0 成功 / 1 参数错误 / 2 认证失败 / 3 点数不足 / 4 网络错误 / 5 其它。
 *
 * 命令: version / register --link / login --link / submit / query / quota /
 *       export / logout / config
 */
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { ApiClient, BizError, allowInsecureTls } = require('./src/client');
const { loadConfig, saveConfig, resolveConfig, maskToken, configPaths, DEFAULT_BASE_URL } = require('./src/config');
const {
  UsageError, printOk, printFail, exitWithError, pollTask, parsePositiveNumber,
} = require('./src/output');

const CAPABILITY = 'b_collect';
const MIN_BATCH = 1;
const MAX_BATCH = 50;
const VERSION = '1.0.0';
const DOWNLOAD_TIMEOUT_MS = 60000; // 导出文件下载超时 (放宽于 API 15s, 防半开连接永久挂起)

// ---------------------------------------------------------------- 参数解析

const VALUE_FLAGS = new Set(['file', 'interval', 'timeout', 'token', 'base-url', 'access-token', 'out']);
const MULTI_FLAGS = new Set(['url']);
const BOOL_FLAGS = new Set(['wait', 'help', 'link', 'check', 'force', 'version']);

function camel(s) {
  return s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

function parseArgs(argv) {
  const opts = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    let arg = argv[i];
    if (!arg.startsWith('-')) {
      positional.push(arg);
      continue;
    }
    if (!arg.startsWith('--')) throw new UsageError(`未知参数: ${arg}`);
    let inline;
    const eq = arg.indexOf('=');
    if (eq > 2) {
      inline = arg.slice(eq + 1);
      arg = arg.slice(0, eq);
    }
    const name = arg.slice(2);
    if (VALUE_FLAGS.has(name)) {
      const value = inline !== undefined ? inline : argv[++i];
      if (value === undefined) throw new UsageError(`缺少参数值: ${arg}`);
      opts[camel(name)] = value;
    } else if (MULTI_FLAGS.has(name)) {
      const value = inline !== undefined ? inline : argv[++i];
      if (value === undefined) throw new UsageError(`缺少参数值: ${arg}`);
      (opts[camel(name)] = opts[camel(name)] || []).push(value);
    } else if (BOOL_FLAGS.has(name)) {
      if (inline !== undefined) throw new UsageError(`参数 ${arg} 不接受值`);
      opts[camel(name)] = true;
    } else {
      throw new UsageError(`未知参数: ${arg}`);
    }
  }
  const cmd = positional.shift() || '';
  return { cmd, args: positional, opts };
}

const USAGE = `B站视频稿互动数采集 CLI (播放/弹幕/评论/收藏/投币/分享/点赞)

用法: node cli.js <命令> [参数]

命令:
  register --link                   生成注册二维码/链接（推荐；注册即送 10 点数）
  register --check --access-token <串>  用户完成注册后确认并保存 token
  login --link                      生成登录二维码/链接（推荐）
  login --check --access-token <串> 用户完成授权后确认并保存 token
  submit --url <视频链接> [--url ...] [--file <路径>] [--wait] [--interval 秒] [--timeout 秒] [--force]
                                    提交采集任务（1~50 条；--file 按行读取, 忽略空行与 # 注释；
                                    支持 bilibili.com/video/<BV号> 与 /video/av<数字> 直链、
                                    b23.tv 短链（短链由采集节点浏览器打开后自动还原）；
                                    --force 跳过 24h 内容去重强制重提）
  query <task_id> [--wait]          查询任务状态与结果
  export <task_id> [--wait] [--out <文件路径>] [--timeout 秒]
                                    导出任务结果 CSV（保留 7 天；--wait 等待生成, 默认超时 300s）
  quota                             查询点数与个人信息
  logout                            登出当前账号
  config set base-url <url>         设置后端服务地址
  config set insecure true|false    忽略 HTTPS 证书校验（自签证书时开）
  config show                       查看当前配置（token 脱敏）
  version                           显示版本

计费: 1 条视频 = 1 点数；无效链接不扣费；稿件删除/私密不返还，服务侧失败全额返还。

全局参数: --token <token>（临时覆盖）  --base-url <url>（默认 ${DEFAULT_BASE_URL}）`;

// ---------------------------------------------------------------- 各命令

function requireToken(cfg) {
  if (!cfg.token) throw new BizError(1002, '未登录：缺少 token');
}

async function cmdSessionLink(cfg, scene) {
  const client = new ApiClient({ baseUrl: cfg.baseUrl });
  const data = await client.createCliSession();
  const isRegister = scene === 'register';
  const pageUrl = cfg.baseUrl + (isRegister ? data.register_path : data.login_path);
  const qrUrl = cfg.baseUrl + (isRegister ? data.register_qr_path : data.qr_path);
  const action = isRegister ? '注册' : '登录';
  process.stderr.write(
    `请把下面这段${action}引导原样发给用户：\n` +
    '----\n' +
    (isRegister
      ? '需要先注册账号（注册即送 10 免费点数，不注册无法使用采集服务）。请用手机扫码或打开链接注册：\n\n'
      : '需要先登录。请用手机扫码或打开链接登录账号：\n\n') +
    `${action}方式（二选一）\n` +
    `二维码图片：${qrUrl}\n` +
    `${action}链接：${pageUrl}\n` +
    `access_token（${action}后校验用）：${data.access_token}\n` +
    `扫码/${action}完成后告诉我一声，我会执行校验并保存凭证：\n\n` +
    `node cli.js ${scene} --check --access-token "${data.access_token}"\n` +
    '----\n');
  printOk({
    qr_url: qrUrl,
    [isRegister ? 'register_url' : 'login_url']: pageUrl,
    access_token: data.access_token,
    expires_in: data.expires_in,
  });
}

async function cmdSessionCheck(cfg, opts, scene) {
  const action = scene === 'register' ? '注册' : '登录';
  const accessToken = opts.accessToken;
  if (!accessToken || !/^[0-9a-f]{16,64}$/.test(accessToken)) {
    throw new UsageError(`${scene} --check 需要 --access-token（${scene} --link 下发的十六进制串）`);
  }
  const client = new ApiClient({ baseUrl: cfg.baseUrl });
  const data = await client.checkCliSession(accessToken);
  if (data.status === 'pending') {
    printFail('LOGIN_PENDING', `用户尚未完成${action}，请提醒用户完成扫码/链接${action}后再执行本命令`);
    process.exit(2);
  }
  if (data.status !== 'ready' || !data.token) {
    printFail('LOGIN_EXPIRED', `${action}会话已过期或已使用，请重新执行 ${scene} --link 发起${action}`);
    process.exit(2);
  }
  saveConfig({ base_url: cfg.baseUrl, token: data.token });
  process.stderr.write(`${action}成功，token 已保存到配置文件\n`);
  printOk({ phone: data.phone, quota_balance: data.quota_balance });
}

function collectUrls(opts) {
  const urls = [...(opts.url || [])];
  if (opts.file) {
    let content;
    try {
      content = fs.readFileSync(opts.file, 'utf8');
    } catch {
      throw new UsageError(`无法读取文件: ${opts.file}`);
    }
    for (const line of content.split(/\r?\n/)) {
      const s = line.trim();
      if (!s || s.startsWith('#')) continue;
      urls.push(s);
    }
  }
  if (urls.length < MIN_BATCH) throw new UsageError('请通过 --url 或 --file 提供至少 1 条 B站视频链接');
  if (urls.length > MAX_BATCH) throw new UsageError(`超出单次批量上限（${MAX_BATCH} 条），当前 ${urls.length} 条`);
  return urls;
}

// ---------------------------------------------------------------- 链接校验（强约束）

// B站 ID 口径 (对齐服务端 app/parsers/b_urls.py, kimi-webbridge 2026-10-16 实测):
//   bvid = BV + 10 位 [0-9A-Za-z]; aid = 纯数字稿件 ID; 短链 b23.tv / bili2233.cn
const _BVID_RE = /^(BV[0-9A-Za-z]{10})$/;
const _SHORT_HOSTS = new Set(['b23.tv', 'www.b23.tv', 'bili2233.cn', 'www.bili2233.cn']);
const _VIDEO_HOSTS = new Set(['bilibili.com', 'www.bilibili.com', 'm.bilibili.com']);
const _SPACE_HOSTS = new Set(['space.bilibili.com']);
// URL 字符黑名单 (同服务端: 引号/尖括号/反引号/反斜杠/空白/控制字符, 防 DOM-XSS 注入链)
const _UNSAFE_URL_RE = /["'<>`\\\x00-\x1f\x7f\s]/;

/**
 * 提交前本地校验链接（不扣费、不发请求），口径对齐服务端 app/parsers/b_urls.py:
 *  1) b23.tv / bili2233.cn 短链直接放行 (bvid/aid 由节点浏览器导航后还原);
 *  2) bilibili.com 需 /video/<BV号> 或 /video/av<数字> (纯数字亦按 aid 处理);
 *  3) UP主主页链接 (space.bilibili.com) 提示改用 b-profile skill; 其它域名一律拒绝。
 */
function validateVideoUrls(urls) {
  const problems = [];
  urls.forEach((raw, i) => {
    const no = i + 1;
    if (typeof raw !== 'string' || raw.length === 0 || raw.length > 2048) {
      problems.push(`第 ${no} 条链接为空或超长（上限 2048 字符）: ${String(raw).slice(0, 80)}`);
      return;
    }
    if (_UNSAFE_URL_RE.test(raw)) {
      problems.push(`第 ${no} 条链接含不允许的字符（引号/尖括号/空白等）: ${raw.slice(0, 80)}`);
      return;
    }
    let u;
    try {
      u = new URL(raw);
    } catch {
      problems.push(`第 ${no} 条链接格式不合法（需 http(s):// 开头的完整 URL）: ${raw}`);
      return;
    }
    const host = u.hostname.toLowerCase();
    if (_SHORT_HOSTS.has(host)) return; // 短链: 节点浏览器阶段还原
    if (_VIDEO_HOSTS.has(host)) {
      const m = u.pathname.match(/^\/video\/([^/?#]+)\/?$/);
      if (m) {
        const slug = m[1] || '';
        if (/^av[0-9]{1,20}$/.test(slug)) return;  // /video/av<数字>
        if (_BVID_RE.test(slug)) return;           // /video/<BV号>
        if (/^[0-9]{1,20}$/.test(slug)) return;    // /video/<纯数字> → 视作 aid
        problems.push(`第 ${no} 条无法识别的视频 ID（需 /video/<BV号> 或 /video/av<数字>）: ${raw}`);
        return;
      }
      if (u.pathname === '/' || u.pathname === '') {
        problems.push(`第 ${no} 条链接缺少视频 ID（需 /video/<BV号> 链接）: ${raw}`);
        return;
      }
      problems.push(`第 ${no} 条无法提取视频 ID（需 /video/<BV号> 链接）: ${raw}`);
      return;
    }
    if (_SPACE_HOSTS.has(host)) {
      problems.push(`第 ${no} 条是 UP主主页链接（主页投稿采集请用 b-profile skill）: ${raw}`);
      return;
    }
    problems.push(`第 ${no} 条不是 B站视频链接（域名 ${host}）: ${raw}`);
  });
  if (problems.length) {
    const msg =
      '链接校验未通过，本次未提交、未扣费。共 ' + problems.length + ' 条问题:\n' +
      problems.map((p) => `  - ${p}`).join('\n') +
      '\n说明: 支持 bilibili.com/video/<BV号>、/video/av<数字> 直链与 b23.tv 短链；' +
      'UP主主页链接请用 b-profile skill，评论采集请用 b-comments skill。';
    throw new UsageError(msg);
  }
}

async function cmdSubmit(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const urls = collectUrls(opts);
  validateVideoUrls(urls);
  const items = urls.map((video_url, i) => ({ id: i + 1, payload: { video_url } }));
  // 幂等键按内容派生: 同批内容重试复用同键 (服务端幂等, 不重复扣费);
  // --force 时混入时间戳生成新键 (服务端同时跳过 24h 去重)
  const idemSource = urls.join('\n') + (opts.force ? `\n#force:${Date.now()}` : '');
  const idempotencyKey = crypto.createHash('sha256').update(idemSource).digest('hex').slice(0, 32);
  process.stderr.write(`提交 ${items.length} 条 B站视频稿采集任务（每条 1 点；幂等键 ${idempotencyKey}${opts.force ? ', force' : ''}）...\n`);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  const data = await client.submitTask(CAPABILITY, items, idempotencyKey, !!opts.force);
  if (!opts.wait) {
    printOk(data);
    return;
  }
  process.stderr.write(`任务已创建 task_id=${data.task_id}，等待结果...\n`);
  const task = await pollTask(client, data.task_id, {
    intervalSec: parsePositiveNumber(opts.interval, 'interval', 2),
    timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 300),
  });
  printOk(task);
}

async function cmdQuery(args, opts) {
  const taskId = args[0];
  if (!taskId) throw new UsageError('query 需要 task_id 参数');
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  if (!opts.wait) {
    printOk(await client.getTask(taskId));
    return;
  }
  const task = await pollTask(client, taskId, {
    intervalSec: parsePositiveNumber(opts.interval, 'interval', 2),
    timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 300),
  });
  printOk(task);
}

async function cmdExport(args, opts) {
  const taskId = args[0];
  if (!taskId) throw new UsageError('export 需要 task_id 参数');
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  const created = await client.createExport(taskId);
  if (!opts.wait) {
    printOk(created);
    return;
  }
  process.stderr.write(`导出任务已创建 export_id=${created.export_id}，等待生成...\n`);
  // 复用 --timeout (默认 300s), 超时报 TIMEOUT 退出码 5 (对齐 pollTask 风格)
  const timeoutSec = parsePositiveNumber(opts.timeout, 'timeout', 300);
  const deadline = Date.now() + timeoutSec * 1000;
  let info;
  for (;;) {
    info = await client.getExport(created.export_id);
    // 终态完备: 只对 pending/running 继续等待, 其余任何状态立即跳出
    if (info.status !== 'pending' && info.status !== 'running') break;
    if (Date.now() + 1000 > deadline) {
      printFail('TIMEOUT', `等待导出超时（${timeoutSec}s），导出仍为 ${info.status} 状态，可稍后重试 export ${taskId}`);
      process.exit(5);
    }
    await new Promise((r) => setTimeout(r, 1000));
  }
  if (info.status !== 'done') {
    printFail('EXPORT_FAILED', `导出未完成 (status=${info.status}), 请稍后重试`);
    process.exit(5);
  }
  // 下载 CSV (复用 token; 带 AbortController 超时)
  const dlCtrl = new AbortController();
  const dlTimer = setTimeout(() => dlCtrl.abort(), DOWNLOAD_TIMEOUT_MS);
  let buf;
  try {
    const res = await fetch(`${cfg.baseUrl}/api/v1/platform/exports/${encodeURIComponent(info.export_id)}/file`,
      { headers: { Authorization: `Bearer ${cfg.token}` }, signal: dlCtrl.signal });
    if (!res.ok) {
      printFail('EXPORT_FAILED', `下载失败 HTTP ${res.status}`);
      process.exit(5);
    }
    buf = Buffer.from(await res.arrayBuffer());
  } catch (err) {
    printFail('EXPORT_FAILED', err && err.name === 'AbortError'
      ? `下载超时（${DOWNLOAD_TIMEOUT_MS / 1000}s），请检查网络后重试 export ${taskId}`
      : `下载失败: ${err && err.message ? err.message : err}`);
    process.exit(5);
  } finally {
    clearTimeout(dlTimer);
  }
  const out = opts.out || `${taskId}_b_videos.csv`;
  // --out 路径兜底: 目录不存在自动创建; 覆盖已有文件时在 stderr 提示
  try {
    fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  } catch { /* 目录已存在 */ }
  if (fs.existsSync(out)) {
    process.stderr.write(`[warn] 目标文件已存在，将覆盖: ${out}\n`);
  }
  fs.writeFileSync(out, buf);
  process.stderr.write(`已下载: ${out}\n`);
  printOk({ export_id: info.export_id, file: out, size: buf.length });
}

async function cmdQuota(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  printOk(await client.profile());
}

async function cmdLogout(opts) {
  const cfg = resolveConfig(opts);
  if (!cfg.token) throw new BizError(1002, '未登录：本地没有已保存的 token');
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  try {
    await client.logout();
  } catch (err) {
    process.stderr.write(`服务端登出异常（已忽略，继续清除本地 token）: ${err.message}\n`);
  }
  saveConfig({ token: '' });
  process.stderr.write('已登出，本地 token 已清除；可执行 login --link 登录其他账号\n');
  printOk({ logged_out: true });
}

async function cmdConfig(args, opts) {
  const sub = args[0];
  if (sub === 'set' && args[1] === 'base-url') {
    const url = args[2];
    if (!url || !/^https?:\/\//.test(url)) throw new UsageError('config set base-url 需要 http(s):// 开头的地址');
    saveConfig({ base_url: url.replace(/\/+$/, '') });
    process.stderr.write(`base_url 已保存到 ${configPaths.configPath}\n`);
    printOk({ base_url: loadConfig().base_url });
    return;
  }
  if (sub === 'set' && args[1] === 'insecure') {
    const v = args[2];
    if (v !== 'true' && v !== 'false') throw new UsageError('config set insecure 需要 true 或 false');
    saveConfig({ insecure: v === 'true' });
    process.stderr.write(`insecure 已保存到 ${configPaths.configPath}\n`);
    printOk({ insecure: loadConfig().insecure === true });
    return;
  }
  if (sub === 'show') {
    const cfg = resolveConfig(opts);
    printOk({
      base_url: cfg.baseUrl,
      insecure: cfg.insecure,
      token: maskToken(cfg.token),
      config_path: configPaths.configPath,
    });
    return;
  }
  throw new UsageError('config 仅支持: config set base-url <url> / config set insecure true|false / config show');
}

// ---------------------------------------------------------------- 入口

async function main() {
  const { cmd, args, opts } = parseArgs(process.argv.slice(2));
  if (opts.version) {
    printOk({ name: 'b-collect', version: VERSION, capability: CAPABILITY });
    return;
  }
  if (opts.help || !cmd) throw new UsageError('缺少命令');
  if (resolveConfig(opts).insecure) allowInsecureTls();
  switch (cmd) {
    case 'version': return printOk({ name: 'b-collect', version: VERSION, capability: CAPABILITY });
    case 'register':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'register');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'register');
      throw new UsageError('register 仅支持 --link / --check (终端注册会被 2003 拒绝)');
    case 'login':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'login');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'login');
      throw new UsageError('login 仅支持 --link / --check (终端登录会被 2003 拒绝)');
    case 'submit': return cmdSubmit(opts);
    case 'query': return cmdQuery(args, opts);
    case 'export': return cmdExport(args, opts);
    case 'quota': return cmdQuota(opts);
    case 'logout': return cmdLogout(opts);
    case 'config': return cmdConfig(args, opts);
    default: throw new UsageError(`未知命令: ${cmd}`);
  }
}

// 接线 USAGE: 参数错误时在 stderr 输出帮助文案
main().catch((e) => exitWithError(e, { usage: USAGE }));
