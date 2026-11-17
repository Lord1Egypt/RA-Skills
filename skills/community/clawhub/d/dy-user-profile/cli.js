#!/usr/bin/env node
'use strict';
/**
 * cli.js — 抖音用户主页视频采集 CLI (能力: dy_profile, 自包含)。
 *
 * 输入抖音用户主页链接 → 平台调度内网浏览器节点拟人滚动主页
 * (滚动 [data-e2e="user-post-list"], max_cursor 翻页), 拦截官方
 * /aweme/v1/web/aweme/post/ 接口响应采集视频列表
 * (文案/互动数/封面/发布时间/视频链接)。
 *
 * 计费 (对齐 xhs_profile 口径):
 *   一页 (约 20 条) = 5 点数;
 *   预扣 页数 × 5; 结算按实采 ceil(实采条数/20) × 5 退差额
 *   (不满 20 条零头按一页计); 零结果/采集失败/主页不可见 → 全额返还。
 *
 * 输出规约 (对齐 xhs-profile): stdout 只输出 JSON, 提示走 stderr。
 * 退出码: 0 成功 / 1 参数错误 / 2 认证失败 / 3 点数不足 / 4 网络错误 / 5 其它。
 *
 * 命令: version / register --link|--check / login --link|--check / collect /
 *       query / export / quota / logout / config
 */
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { ApiClient, BizError, allowInsecureTls } = require('./src/client');
const { loadConfig, saveConfig, resolveConfig, maskToken, configPaths, DEFAULT_BASE_URL } = require('./src/config');
const {
  UsageError, printOk, printFail, exitWithError, pollTask, parsePositiveNumber,
} = require('./src/output');

const CAPABILITY = 'dy_profile';
const VERSION = '1.0.0';
const MAX_PAGES = 10;         // 单任务采集页数上限 (服务端 profile.max_pages)
const DEFAULT_PAGES = 1;
const BILL_UNIT = 20;         // 计费粒度: 一页的视频数 (约 18-20 条)
const DEFAULT_PRICE = 5;      // capability_prices 兜底价 (读不到时)
const DOWNLOAD_TIMEOUT_MS = 60000;

// ---------------------------------------------------------------- 参数解析

const VALUE_FLAGS = new Set(['url', 'pages', 'interval', 'timeout', 'token', 'base-url', 'access-token', 'out']);
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

const USAGE = `抖音用户主页视频采集 CLI (主页链接, 采集其视频作品列表)

用法: node cli.js <命令> [参数]

命令:
  register --link                   生成注册二维码/链接（推荐；注册即送 10 点数）
  register --check --access-token <串>  用户完成注册后确认并保存 token
  login --link                      生成登录二维码/链接（推荐）
  login --check --access-token <串> 用户完成授权后确认并保存 token

  collect --url <主页链接> [--pages N] [--wait] [--timeout 秒] [--force]
                                    提交主页采集任务（每任务 1 个用户, 1~10 页, 每页约 20 条；
                                    主页链接支持 douyin.com/user/<sec_uid> 直链与 v.douyin.com
                                    短链（短链由采集节点浏览器打开后自动还原）；
                                    --force 跳过 24h 内容去重强制重提；
                                    --wait 等待结果, 默认超时 600s）
  query <task_id> [--wait]          查询任务状态与结果
  export <task_id> [--wait] [--out <文件路径>]
                                    导出任务结果 CSV（保留 7 天）

  quota                             查询点数与个人信息
  logout                            登出当前账号
  config set base-url <url>         设置后端服务地址
  config set insecure true|false    忽略 HTTPS 证书校验（自签证书时开）
  config show                       查看当前配置（token 脱敏）
  version                           显示版本

计费: 一页（约 20 条）= 5 点数；预扣 页数×5、结算按实采量退差（零头按一页计）；
零结果/采集失败/主页不可见 → 全额返还。

全局参数: --token <token>（临时覆盖）  --base-url <url>（默认 ${DEFAULT_BASE_URL}）`;

// ---------------------------------------------------------------- 公共

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

/** 读能力价格 (免登录接口); 读不到按 5 兜底, 不阻塞提交。 */
async function fetchPrice(baseUrl) {
  try {
    const client = new ApiClient({ baseUrl });
    const data = await client.request('GET', '/platform/capabilities');
    const cap = ((data && data.items) || []).find((c) => c.name === CAPABILITY);
    if (cap && Number(cap.price) > 0) return { price: Number(cap.price), cap };
    return { price: DEFAULT_PRICE, cap: null };
  } catch {
    return { price: DEFAULT_PRICE, cap: null };
  }
}

/**
 * 本地校验主页链接 (口径对齐服务端 app/parsers/dy_urls.py parse_dy_user_url):
 * - v.douyin.com 短链放行 (节点浏览器阶段还原);
 * - douyin.com/user/<sec_uid> 直链放行 (self 除外);
 * - iesdouyin.com/share/user/<uid> 分享页放行;
 * - 视频链接提示改用 dy-collect / dy-comments。
 */
function validateProfileUrl(url) {
  const u = String(url || '').trim();
  if (!u) throw new UsageError('需要 --url <抖音用户主页链接>（douyin.com/user/<sec_uid> 或 v.douyin.com 短链）');
  if (u.length > 2048) throw new UsageError('链接过长（上限 2048 字符）');
  let p;
  try {
    p = new URL(u);
  } catch {
    throw new UsageError('链接格式不合法（需 http(s):// 开头的完整 URL）');
  }
  const host = p.hostname.toLowerCase();
  if (host === 'v.douyin.com') return u;
  if (host === 'douyin.com' || host === 'www.douyin.com' || host === 'www.iesdouyin.com') {
    const m = p.pathname.match(/^\/user\/([0-9A-Za-z_-]{8,128})\/?$/);
    if (m) {
      if (m[1] === 'self') {
        throw new UsageError('不支持 self 主页（请提供目标用户的 /user/<sec_uid> 链接）');
      }
      return u;
    }
    if (p.pathname.match(/^\/share\/user\/(\d{5,32})\/?$/)) return u;
    if (p.pathname.match(/^\/(?:share\/)?(?:video|note)\/\d{15,20}\/?$/)) {
      throw new UsageError('这是视频链接（单篇互动数请用 dy-collect skill，评论请用 dy-comments skill）；主页采集需要 /user/<sec_uid> 链接');
    }
    throw new UsageError('无法提取用户 ID（需 douyin.com/user/<sec_uid> 主页链接）');
  }
  throw new UsageError(`不是抖音主页链接（域名 ${host}）`);
}

// ---------------------------------------------------------------- 整单模式

async function cmdCollect(opts) {
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const profileUrl = validateProfileUrl(opts.url);

  if (opts.pages !== undefined && !/^\d+$/.test(String(opts.pages))) {
    throw new UsageError(`--pages 需为正整数（1~${MAX_PAGES}）`);
  }
  const pages = opts.pages !== undefined
    ? Math.max(1, Math.min(parseInt(opts.pages, 10), MAX_PAGES))
    : DEFAULT_PAGES;

  // 提交前读价格, 本地透出预估点数 (免登录接口, 失败兜底 5)
  const { price } = await fetchPrice(cfg.baseUrl);
  const estimatedPoints = pages * price;

  const items = [{ id: 1, payload: { profile_url: profileUrl, pages } }];
  // 幂等键按参数派生: 同参数重试复用同键 (服务端幂等, 不重复扣费);
  // --force 时混入时间戳生成新键 (服务端同时跳过 24h 去重)
  const idemSource = `${profileUrl}|${pages}` + (opts.force ? `|#force:${Date.now()}` : '');
  const idempotencyKey = crypto.createHash('sha256').update(idemSource).digest('hex').slice(0, 32);

  process.stderr.write(
    `提交抖音主页采集任务: url="${profileUrl}" 页数=${pages} (约 ${pages * BILL_UNIT} 条)\n` +
    `计费: 预扣 ${pages}×${price}=${estimatedPoints} 点 (每页约 ${BILL_UNIT} 条=${price} 点), ` +
    `按实采量结算退差, 零结果/失败/主页不可见全额返还 (幂等键 ${idempotencyKey}${opts.force ? ', force' : ''})...\n`);

  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });
  const data = await client.submitTask(CAPABILITY, items, idempotencyKey, !!opts.force);

  // submit 响应补充本地预估信息, 供 agent 汇报
  const enriched = { ...data, estimated_points: estimatedPoints, price_per_page: price };
  if (!opts.wait) {
    printOk(enriched);
    return;
  }
  process.stderr.write(`任务已创建 task_id=${data.task_id}，等待节点采集（每页约 5-10 秒）...\n`);
  const task = await pollTask(client, data.task_id, {
    intervalSec: parsePositiveNumber(opts.interval, 'interval', 5),
    timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 600),
  });
  process.stderr.write(
    `任务完成: status=${task.status}，实采 ${(task.items && task.items[0] && task.items[0].result
      && task.items[0].result.collected_count) || 0} 条，` +
    `请查看 result 里的 settle_charged(实收点数)/refunded_diff(退差点数) 如实汇报给用户。\n`);
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
    intervalSec: parsePositiveNumber(opts.interval, 'interval', 5),
    timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 600),
  });
  printOk(task);
}

async function cmdExport(args, opts) {
  const taskId = args[0];
  if (!taskId) throw new UsageError('export 需要 task_id 参数');
  const cfg = resolveConfig(opts);
  requireToken(cfg);
  const client = new ApiClient({ baseUrl: cfg.baseUrl, token: cfg.token });

  // --wait: 先等任务终态 (默认 600s)
  if (opts.wait) {
    process.stderr.write(`等待任务 ${taskId} 完成...\n`);
    await pollTask(client, taskId, {
      intervalSec: parsePositiveNumber(opts.interval, 'interval', 5),
      timeoutSec: parsePositiveNumber(opts.timeout, 'timeout', 600),
    });
  }

  const created = await client.createExport(taskId);
  if (!opts.wait) {
    printOk(created);
    return;
  }
  process.stderr.write(`导出任务已创建 export_id=${created.export_id}，等待生成...\n`);
  const timeoutSec = 300;
  const deadline = Date.now() + timeoutSec * 1000;
  let info;
  for (;;) {
    info = await client.getExport(created.export_id);
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
  await downloadToFile(cfg, `${cfg.baseUrl}/api/v1/platform/exports/${encodeURIComponent(info.export_id)}/file`,
    opts.out || `${taskId}_profile_videos.csv`, { export_id: info.export_id });
}

/** 下载文件并落盘, 输出结果 JSON。 */
async function downloadToFile(cfg, url, out, extra) {
  const dlCtrl = new AbortController();
  const dlTimer = setTimeout(() => dlCtrl.abort(), DOWNLOAD_TIMEOUT_MS);
  let buf;
  try {
    const res = await fetch(url,
      { headers: { Authorization: `Bearer ${cfg.token}` }, signal: dlCtrl.signal });
    if (!res.ok) {
      printFail('EXPORT_FAILED', `下载失败 HTTP ${res.status}`);
      process.exit(5);
    }
    buf = Buffer.from(await res.arrayBuffer());
  } catch (err) {
    printFail('EXPORT_FAILED', err && err.name === 'AbortError'
      ? `下载超时（${DOWNLOAD_TIMEOUT_MS / 1000}s），请检查网络后重试`
      : `下载失败: ${err && err.message ? err.message : err}`);
    process.exit(5);
  } finally {
    clearTimeout(dlTimer);
  }
  try {
    fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  } catch { /* 目录已存在 */ }
  if (fs.existsSync(out)) {
    process.stderr.write(`[warn] 目标文件已存在，将覆盖: ${out}\n`);
  }
  fs.writeFileSync(out, buf);
  process.stderr.write(`已下载: ${out}\n`);
  printOk({ ...extra, file: out, size: buf.length });
}

// ---------------------------------------------------------------- 其他

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
    printOk({ name: 'dy-profile', version: VERSION, capability: CAPABILITY });
    return;
  }
  if (opts.help || !cmd) throw new UsageError('缺少命令');
  if (resolveConfig(opts).insecure) allowInsecureTls();
  switch (cmd) {
    case 'version': return printOk({ name: 'dy-profile', version: VERSION, capability: CAPABILITY });
    case 'register':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'register');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'register');
      throw new UsageError('register 仅支持 --link / --check (终端注册会被 2003 拒绝)');
    case 'login':
      if (opts.link) return cmdSessionLink(resolveConfig(opts), 'login');
      if (opts.check) return cmdSessionCheck(resolveConfig(opts), opts, 'login');
      throw new UsageError('login 仅支持 --link / --check (终端登录会被 2003 拒绝)');
    case 'collect': return cmdCollect(opts);
    case 'query': return cmdQuery(args, opts);
    case 'export': return cmdExport(args, opts);
    case 'quota': return cmdQuota(opts);
    case 'logout': return cmdLogout(opts);
    case 'config': return cmdConfig(args, opts);
    default: throw new UsageError(`未知命令: ${cmd}`);
  }
}

main().catch((e) => exitWithError(e, { usage: USAGE }));
