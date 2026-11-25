#!/usr/bin/env node
/**
 * 推送到云电脑（auto-publish）。config.json 与本脚本同目录。
 *
 *   node push-to-cloud.js <instanceId|-> html <HTML文件> [categoryId] [publishMode] [targetScope] [idsOrNamesCSV]
 *   node push-to-cloud.js <instanceId|-> img '<JSON/URL/本地路径>' <title> [description|content.html] [publishMode] [targetScope] [idsOrNamesCSV]
 *   node push-to-cloud.js <instanceId|-> video '<URL/本地路径/JSON>' <title> [description] [publishMode] [targetScope] [idsOrNamesCSV]
 *   node push-to-cloud.js <instanceId|-> list-targets [categoryId]
 *   node push-to-cloud.js <instanceId|-> resolve <categoryId> <名称> [prefer]
 *
 * instanceId 为 "-" / default / 空：使用 config.instances 中 selected:true 的实例。
 * categoryId：article（默认）| newspic | video
 * publishMode：draft（默认）| publish | default
 * targetScope：all（默认）| environment | account
 *   environment / account 的末参可为 id，或账号名 / 环境名（自动 resolve）
 * prefer（resolve）：auto（默认）| account | environment | instance
 * 未传 targetScope 时默认 all。
 * description：分享摘要 / 内容描述（与 auto-publish / design 前端字段一致）；html 模式从 meta description 抽取。
 *
 * 本地图片/视频会先 prepareMediaUpload 直传 CloudBase，再把公网 URL 交给 sendToCloud。
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const DEFAULT_API = 'https://api.pcloud.ac.cn/openAccessService';
const DIR = __dirname;
const TARGET_SCOPES = new Set(['all', 'environment', 'account']);
const PUBLISH_MODES = new Set(['draft', 'publish', 'default']);

function readJson(name) {
  const p = path.join(DIR, name);
  if (!fs.existsSync(p)) throw new Error('缺少: ' + p);
  return JSON.parse(fs.readFileSync(p, 'utf8').trim());
}

function titleFromHtml(html) {
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (titleMatch) {
    const raw = titleMatch[1].replace(/<[^>]+>/g, '').trim();
    if (raw) return raw;
  }
  const hMatch = html.match(/<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/i);
  if (hMatch) {
    const raw = hMatch[1].replace(/<[^>]+>/g, '').trim();
    if (raw) return raw;
  }
  return '未命名';
}

/** 从 HTML 取 description（meta / lead），与 design 前端 extractDescriptionFromHtml 对齐 */
function descriptionFromHtml(html) {
  if (!html || typeof html !== 'string') return '';
  const meta =
    html.match(
      /<meta\b[^>]*\bname\s*=\s*["']description["'][^>]*\bcontent\s*=\s*["']([^"']*)["'][^>]*>/i
    ) ||
    html.match(
      /<meta\b[^>]*\bcontent\s*=\s*["']([^"']*)["'][^>]*\bname\s*=\s*["']description["'][^>]*>/i
    );
  if (meta && meta[1]) {
    const t = String(meta[1]).replace(/<[^>]+>/g, '').trim();
    if (t) return t.slice(0, 500);
  }
  const lead = html.match(
    /<p\b[^>]*class=["'][^"']*autopub-article-description[^"']*["'][^>]*>([\s\S]*?)<\/p>/i
  );
  if (lead && lead[1]) {
    const t = String(lead[1]).replace(/<[^>]+>/g, '').trim();
    if (t) return t.slice(0, 500);
  }
  return '';
}

/**
 * 可选描述参数：若下一项是 publishMode / targetScope 则视为未传。
 * 返回 { description, nextIndex }
 */
function takeOptionalDescriptionArg(argv, startIdx) {
  const raw = argv[startIdx];
  if (raw == null || String(raw).trim() === '') {
    return { description: '', nextIndex: startIdx };
  }
  const s = String(raw).trim();
  if (isPublishModeToken(s) || isScopeToken(s)) {
    return { description: '', nextIndex: startIdx };
  }
  return { description: s, nextIndex: startIdx + 1 };
}

function postJson(apiBase, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(apiBase);
    const lib = u.protocol === 'http:' ? http : https;
    const data = Buffer.from(JSON.stringify(body), 'utf8');
    const req = lib.request(
      {
        hostname: u.hostname,
        port: u.port || (u.protocol === 'http:' ? 80 : 443),
        path: u.pathname + u.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': data.length,
        },
        timeout: 120000,
      },
      (res) => {
        let raw = '';
        res.on('data', (c) => (raw += c));
        res.on('end', () => {
          let parsed = null;
          try {
            parsed = raw ? JSON.parse(raw) : {};
          } catch (e) {
            return reject(new Error('非 JSON 响应: ' + raw.slice(0, 200)));
          }
          resolve({ status: res.statusCode, body: parsed });
        });
      }
    );
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('timeout'));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function putFile(uploadUrl, headers, filePath) {
  return new Promise((resolve, reject) => {
    const u = new URL(uploadUrl);
    const lib = u.protocol === 'http:' ? http : https;
    const stat = fs.statSync(filePath);
    const reqHeaders = {
      ...(headers || {}),
      'Content-Length': stat.size,
    };
    const req = lib.request(
      {
        hostname: u.hostname,
        port: u.port || (u.protocol === 'http:' ? 80 : 443),
        path: u.pathname + u.search,
        method: 'PUT',
        headers: reqHeaders,
        timeout: 600000,
      },
      (res) => {
        let raw = '';
        res.on('data', (c) => (raw += c));
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ status: res.statusCode });
          } else {
            reject(
              new Error(
                '上传失败 HTTP ' +
                  res.statusCode +
                  ': ' +
                  String(raw || '').slice(0, 300)
              )
            );
          }
        });
      }
    );
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('upload timeout'));
    });
    req.on('error', reject);
    fs.createReadStream(filePath).pipe(req);
  });
}

function resolveInstanceIds(cfg, arg) {
  const list = Array.isArray(cfg.instances) ? cfg.instances : [];
  const a = String(arg || '').trim();
  if (!a || a === '-' || a.toLowerCase() === 'default') {
    const selected = list
      .filter((x) => x && x.selected && x.instanceId)
      .map((x) => x.instanceId);
    if (selected.length) return selected;
    const first = list.find((x) => x && x.instanceId);
    if (first) return [first.instanceId];
    throw new Error('config.json 中无可用 instances，请先运行配置向导');
  }
  const byId = list.find((x) => x && String(x.instanceId) === a);
  if (byId) return [byId.instanceId];
  const q = a.toLowerCase().replace(/\s+/g, '');
  const nameHits = list.filter((x) => {
    if (!x || !x.instanceId) return false;
    const n = String(x.instanceName || '')
      .toLowerCase()
      .replace(/\s+/g, '');
    return n && (n === q || n.includes(q) || q.includes(n));
  });
  if (nameHits.length === 1) return [nameHits[0].instanceId];
  if (nameHits.length > 1) {
    throw new Error(
      '云电脑名称不唯一: ' +
        a +
        ' → ' +
        nameHits.map((x) => x.instanceName + '(' + x.instanceId + ')').join(', ')
    );
  }
  return [a];
}

function readFirstExistingFile(candidates) {
  for (const p of candidates) {
    if (p && fs.existsSync(p) && fs.statSync(p).isFile()) {
      return fs.readFileSync(p, 'utf8');
    }
  }
  return '';
}

function firstExistingPath(candidates) {
  for (const p of candidates) {
    if (p && fs.existsSync(p) && fs.statSync(p).isFile()) return p;
  }
  return '';
}

/** 封面图固定名：cover.png（与云电脑一致） */
function resolveCoverPng(dirs) {
  return firstExistingPath(
    (dirs || []).filter(Boolean).map((dir) => path.join(dir, 'cover.png'))
  );
}

/** 文章封面 HTML：仅在 HTML 所在作品目录查找 */
function resolveCoverHtmlForArticle(htmlPath) {
  const dir = path.dirname(htmlPath);
  const base = path.basename(htmlPath, path.extname(htmlPath));
  return readFirstExistingFile([
    path.join(dir, `${base}_cover.html`),
    path.join(dir, 'cover.html'),
  ]);
}

/** 视频封面 HTML：成片目录及其上一级作品目录 */
function resolveCoverHtmlForVideo(mediaPath) {
  if (!mediaPath) return '';
  const dir = path.dirname(mediaPath);
  const parent = path.dirname(dir);
  return readFirstExistingFile([
    path.join(dir, 'cover.html'),
    path.join(dir, 'video_cover.html'),
    path.join(parent, 'cover.html'),
    path.join(parent, 'video_cover.html'),
  ]);
}

/** 有 cover.png 优先，否则 HTML */
function resolveCoverAssets({ kind, anchorPath }) {
  if (kind === 'video') {
    const dir = anchorPath ? path.dirname(anchorPath) : '';
    const parent = dir ? path.dirname(dir) : '';
    const coverImagePath = resolveCoverPng([dir, parent]);
    return {
      coverImagePath,
      coverHtml: coverImagePath ? '' : resolveCoverHtmlForVideo(anchorPath),
    };
  }
  const coverImagePath = resolveCoverPng([path.dirname(anchorPath)]);
  return {
    coverImagePath,
    coverHtml: coverImagePath ? '' : resolveCoverHtmlForArticle(anchorPath),
  };
}

async function buildCoverFields(apiBase, openId, skillKey, assets) {
  const coverImagePath = String(assets?.coverImagePath || '').trim();
  const coverHtml = String(assets?.coverHtml || '').trim();
  if (coverImagePath) {
    return {
      coverImageUrl: await uploadLocalFile(
        apiBase,
        openId,
        skillKey,
        coverImagePath
      ),
    };
  }
  if (coverHtml) return { coverHtml };
  return {};
}

function resolveInputFile(raw) {
  const s = String(raw || '').trim();
  if (!s) return '';
  const candidates = [
    path.isAbsolute(s) ? s : '',
    path.isAbsolute(s) ? '' : path.join(DIR, s),
    path.isAbsolute(s) ? '' : path.resolve(process.cwd(), s),
  ].filter(Boolean);
  for (const p of candidates) {
    if (fs.existsSync(p) && fs.statSync(p).isFile()) return p;
  }
  return '';
}

function looksLikeHttpUrl(s) {
  return /^https?:\/\//i.test(String(s || '').trim());
}

function resolveLocalPath(raw) {
  const s = String(raw || '').trim();
  if (!s || looksLikeHttpUrl(s)) return '';
  return resolveInputFile(s);
}

function parseMediaSourcesArg(arg) {
  let trimmed = String(arg || '').trim();
  if (!trimmed) throw new Error('需要公网 URL、本地文件路径，或 JSON 数组');
  if (looksLikeHttpUrl(trimmed) || resolveLocalPath(trimmed)) {
    return [trimmed];
  }
  try {
    const arr = JSON.parse(trimmed);
    if (Array.isArray(arr) && arr.length) {
      return arr.map((u) => String(u).trim()).filter(Boolean);
    }
  } catch (_) {
    /* fallthrough */
  }
  if (!trimmed.startsWith('[')) trimmed = '[' + trimmed;
  if (!trimmed.endsWith(']')) trimmed = trimmed + ']';
  const arr = JSON.parse(trimmed);
  if (!Array.isArray(arr) || !arr.length) throw new Error('媒体列表无效');
  return arr.map((u) => String(u).trim()).filter(Boolean);
}

function parseCsvIds(raw) {
  return String(raw || '')
    .split(/[,，\s]+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function isScopeToken(s) {
  return TARGET_SCOPES.has(String(s || '').trim().toLowerCase());
}

function isPublishModeToken(s) {
  return PUBLISH_MODES.has(String(s || '').trim().toLowerCase());
}

/**
 * 从 argv 尾部解析 [publishMode] [targetScope] [idsCSV]
 * 返回 { publishMode, targetScope, ids, restBefore }
 */
function takeTailTargetArgs(argv, startIdx) {
  const rest = argv.slice(startIdx).map((x) => String(x || '').trim());
  let publishMode = '';
  let targetScope = '';
  let ids = [];
  const consumed = [];

  let i = 0;
  if (rest[i] && isPublishModeToken(rest[i])) {
    publishMode = rest[i].toLowerCase();
    consumed.push(rest[i]);
    i += 1;
  }
  if (rest[i] && isScopeToken(rest[i])) {
    targetScope = rest[i].toLowerCase();
    consumed.push(rest[i]);
    i += 1;
    if (rest[i]) {
      ids = parseCsvIds(rest[i]);
      consumed.push(rest[i]);
      i += 1;
    }
  }

  return {
    publishMode: publishMode || 'draft',
    targetScope,
    ids,
    nextIndex: startIdx + consumed.length,
  };
}

async function resolveNamedQuery(
  apiBase,
  openId,
  skillKey,
  serverInstanceId,
  categoryId,
  prefer,
  query
) {
  const res = await postJson(apiBase, {
    action: 'resolveCloudPublishTarget',
    openId,
    skillKey,
    categoryId: categoryId || 'article',
    prefer: prefer || 'auto',
    query: String(query || '').trim(),
    ...(serverInstanceId ? { serverInstanceId } : {}),
  });
  if (!res.body || res.body.success === false) {
    throw new Error(
      (res.body && res.body.error) ||
        'resolveCloudPublishTarget 失败 HTTP ' + res.status
    );
  }
  return res.body;
}

function printResolveCandidates(body) {
  const list = Array.isArray(body.candidates) ? body.candidates : [];
  console.error(
    (body.message || '目标不唯一或未匹配') +
      '。候选 ' +
      list.length +
      ' 个：'
  );
  for (const c of list) {
    console.error(
      JSON.stringify(
        {
          kind: c.kind,
          match: c.match,
          label: c.label,
          serverInstanceId: c.serverInstanceId,
          instanceName: c.instanceName,
          accountId: c.accountId,
          accountName: c.accountName,
          browserProfileId: c.browserProfileId,
          browserProfileName: c.browserProfileName,
          targetScope: c.targetScope,
        },
        null,
        0
      )
    );
  }
}

async function resolveTargetFromConfigAndArgs(
  cfg,
  apiBase,
  openId,
  skillKey,
  serverInstanceIds,
  scopeArg,
  ids,
  categoryId
) {
  let targetScope = String(scopeArg || '').trim().toLowerCase();
  let receiverAccountIds = [];
  let receiverBrowserProfileIds = [];

  if (!targetScope) {
    targetScope = String(cfg.defaultTargetScope || 'all')
      .trim()
      .toLowerCase();
    if (!TARGET_SCOPES.has(targetScope)) targetScope = 'all';
  } else if (!TARGET_SCOPES.has(targetScope)) {
    throw new Error('targetScope 须为 all | environment | account');
  }

  if (serverInstanceIds.length > 1 && targetScope !== 'all') {
    console.warn('多台云电脑时仅支持 targetScope=all，已强制改为 all');
    targetScope = 'all';
  }

  if (targetScope === 'account' || targetScope === 'environment') {
    if (!ids.length) {
      throw new Error(
        targetScope === 'account'
          ? 'targetScope=account 需要账号 id 或名称（CLI 末参）'
          : 'targetScope=environment 需要环境 id 或名称（CLI 末参）'
      );
    }
    if (serverInstanceIds.length !== 1) {
      throw new Error('指定环境/账号时请只选一台云电脑');
    }
    const prefer = targetScope === 'account' ? 'account' : 'environment';
    const resolvedIds = [];
    for (const token of ids) {
      // id 与名称统一走 resolve（服务端支持精确 id 命中）
      const body = await resolveNamedQuery(
        apiBase,
        openId,
        skillKey,
        serverInstanceIds[0],
        categoryId,
        prefer,
        token
      );
      if (!body.resolved) {
        printResolveCandidates(body);
        const err = new Error('目标无法唯一解析: ' + token);
        err.exitCode = 3;
        throw err;
      }
      if (prefer === 'account') {
        const list = body.receiverAccountIds || [];
        if (!list.length) throw new Error('解析结果缺少 receiverAccountIds');
        resolvedIds.push(...list);
      } else {
        const list = body.receiverBrowserProfileIds || [];
        if (!list.length) {
          throw new Error('解析结果缺少 receiverBrowserProfileIds');
        }
        resolvedIds.push(...list);
      }
      if (
        body.serverInstanceId &&
        body.serverInstanceId !== serverInstanceIds[0]
      ) {
        serverInstanceIds[0] = body.serverInstanceId;
      }
    }
    if (targetScope === 'account') {
      receiverAccountIds = [...new Set(resolvedIds)];
    } else {
      receiverBrowserProfileIds = [...new Set(resolvedIds)];
    }
  }

  return {
    targetScope,
    receiverAccountIds,
    receiverBrowserProfileIds,
    serverInstanceIds,
  };
}

function attachTargetFields(body, target) {
  if (!target || !target.targetScope) return body;
  body.targetScope = target.targetScope;
  if (target.targetScope === 'account' && target.receiverAccountIds.length) {
    body.receiverAccountIds = target.receiverAccountIds;
  }
  if (
    target.targetScope === 'environment' &&
    target.receiverBrowserProfileIds.length
  ) {
    body.receiverBrowserProfileIds = target.receiverBrowserProfileIds;
  }
  return body;
}

async function uploadLocalFile(apiBase, openId, skillKey, filePath) {
  const ext = path.extname(filePath).replace(/^\./, '') || 'bin';
  const prep = await postJson(apiBase, {
    action: 'prepareMediaUpload',
    openId,
    skillKey,
    ext,
    folder: 'aigc-web-push',
  });
  if (!prep.body || prep.body.success === false) {
    throw new Error(
      (prep.body && prep.body.error) ||
        'prepareMediaUpload 失败 HTTP ' + prep.status
    );
  }
  const upload = prep.body.upload || {};
  if (!upload.url || !prep.body.publicUrl) {
    throw new Error('prepareMediaUpload 返回缺少 url / publicUrl');
  }
  console.log('上传本地文件', { filePath, publicUrl: prep.body.publicUrl });
  await putFile(upload.url, upload.headers || {}, filePath);
  return String(prep.body.publicUrl).trim();
}

async function resolveMediaUrls(apiBase, openId, skillKey, sources) {
  const out = [];
  for (const src of sources) {
    if (looksLikeHttpUrl(src)) {
      out.push(src);
      continue;
    }
    const local = resolveLocalPath(src);
    if (!local) {
      throw new Error(
        '找不到本地文件且不是 http(s) URL: ' +
          src +
          '（请提供公网 URL，或传入可读的本地文件路径以便自动上传）'
      );
    }
    out.push(await uploadLocalFile(apiBase, openId, skillKey, local));
  }
  return out;
}

function printUsage() {
  console.error(
    '用法:\n' +
      '  node push-to-cloud.js <instanceId|-> html <file.html> [categoryId] [publishMode] [targetScope] [idsOrNamesCSV]\n' +
      '  node push-to-cloud.js <instanceId|-> img \'<urls|本地|JSON>\' <title> [description|content.html] [publishMode] [targetScope] [idsOrNamesCSV]\n' +
      '  node push-to-cloud.js <instanceId|-> video \'<url|本地|JSON>\' <title> [description] [publishMode] [targetScope] [idsOrNamesCSV]\n' +
      '  node push-to-cloud.js <instanceId|-> list-targets [categoryId]\n' +
      '  node push-to-cloud.js <instanceId|-> resolve <categoryId> <名称> [prefer]'
  );
}

function printFriendlyTargets(data) {
  const profiles = Array.isArray(data.browserProfiles) ? data.browserProfiles : [];
  const accounts = Array.isArray(data.accounts) ? data.accounts : [];
  console.log('serverInstanceId:', data.serverInstanceId || data.instanceId || '');
  console.log('categoryId:', data.categoryId || '');
  console.log('message:', data.message || '');
  console.log('environments (' + profiles.length + '):');
  for (const p of profiles) {
    console.log(
      '  - name=' +
        JSON.stringify(p.name || '') +
        ' id=' +
        p.id +
        (p.accountCount != null ? ' accounts=' + p.accountCount : '')
    );
  }
  console.log('accounts (' + accounts.length + '):');
  for (const a of accounts) {
    console.log(
      '  - name=' +
        JSON.stringify(a.name || '') +
        ' id=' +
        a.id +
        ' contentType=' +
        (a.contentType || '') +
        ' env=' +
        JSON.stringify(a.browserProfileName || a.browserProfileId || '') +
        (a.siteUrl ? ' site=' + a.siteUrl : '')
    );
  }
}

async function listTargets(cfg, apiBase, openId, skillKey, instanceArg, categoryId) {
  const serverInstanceIds = resolveInstanceIds(cfg, instanceArg);
  if (serverInstanceIds.length !== 1) {
    throw new Error('list-targets 请指定单台云电脑（或多台时传明确 instanceId）');
  }
  const res = await postJson(apiBase, {
    action: 'listCloudPublishTargets',
    openId,
    skillKey,
    serverInstanceId: serverInstanceIds[0],
    categoryId: categoryId || 'article',
  });
  if (!res.body || res.body.success === false) {
    console.log('HTTP', res.status, JSON.stringify(res.body, null, 2));
    process.exit(2);
  }
  const data = res.body.data || {};
  printFriendlyTargets({
    ...data,
    categoryId: data.categoryId || categoryId || 'article',
    serverInstanceId: data.serverInstanceId || serverInstanceIds[0],
  });
  console.log('--- raw ---');
  console.log(JSON.stringify(res.body, null, 2));
}

async function resolveTargetCommand(
  cfg,
  apiBase,
  openId,
  skillKey,
  instanceArg,
  categoryId,
  query,
  prefer
) {
  const serverInstanceIds = resolveInstanceIds(cfg, instanceArg);
  const serverInstanceId =
    serverInstanceIds.length === 1 ? serverInstanceIds[0] : '';
  const body = await resolveNamedQuery(
    apiBase,
    openId,
    skillKey,
    serverInstanceId,
    categoryId || 'article',
    prefer || 'auto',
    query
  );
  console.log(JSON.stringify(body, null, 2));
  if (!body.resolved) {
    printResolveCandidates(body);
    process.exit(3);
  }
}

async function main() {
  const cfg = readJson('config.json');
  const openId = String(cfg.openId || '').trim();
  if (!openId) throw new Error('config.json 缺少 openId');
  const skillKey = String(cfg.skillKey || '').trim();
  if (!skillKey) throw new Error('config.json 缺少 skillKey，请重新打开配置向导扫码');
  const apiBase = String(cfg.apiBase || DEFAULT_API).trim() || DEFAULT_API;

  const argv = process.argv.slice(2);
  if (argv.length < 2) {
    printUsage();
    process.exit(1);
  }

  const instanceArg = argv[0];
  const mode = String(argv[1] || '').toLowerCase();
  const serverInstanceIds = resolveInstanceIds(cfg, instanceArg);

  if (mode === 'list-targets' || mode === 'list_targets') {
    const categoryId = String(argv[2] || 'article').trim() || 'article';
    await listTargets(cfg, apiBase, openId, skillKey, instanceArg, categoryId);
    return;
  }

  if (mode === 'resolve') {
    const categoryId = String(argv[2] || 'article').trim() || 'article';
    const query = String(argv[3] || '').trim();
    if (!query) throw new Error('resolve 需要名称：resolve <categoryId> <名称> [prefer]');
    const prefer = String(argv[4] || 'auto').trim() || 'auto';
    await resolveTargetCommand(
      cfg,
      apiBase,
      openId,
      skillKey,
      instanceArg,
      categoryId,
      query,
      prefer
    );
    return;
  }

  let body;
  let activeInstanceIds = serverInstanceIds.slice();
  if (mode === 'html') {
    const file = argv[2];
    if (!file) throw new Error('缺少 HTML 路径');
    const htmlPath = resolveInputFile(file);
    if (!htmlPath) throw new Error('找不到文件: ' + file);
    const content = fs.readFileSync(htmlPath, 'utf8');
    const categoryId = String(argv[3] || 'article').trim() || 'article';
    const tail = takeTailTargetArgs(argv, 4);
    const target = await resolveTargetFromConfigAndArgs(
      cfg,
      apiBase,
      openId,
      skillKey,
      activeInstanceIds,
      tail.targetScope,
      tail.ids,
      categoryId
    );
    activeInstanceIds = target.serverInstanceIds || activeInstanceIds;
    const coverAssets = resolveCoverAssets({ kind: 'article', anchorPath: htmlPath });
    if (!coverAssets.coverImagePath && !coverAssets.coverHtml) {
      const base = path.basename(htmlPath, path.extname(htmlPath));
      console.warn(
        '作品目录下找不到封面（cover.png / ' +
          base +
          '_cover.html / cover.html）（本次跳过封面）'
      );
    }
    const coverFields = await buildCoverFields(
      apiBase,
      openId,
      skillKey,
      coverAssets
    );
    const pushTitle = titleFromHtml(content);
    const pushDescription = descriptionFromHtml(content);
    body = attachTargetFields(
      {
        action: 'sendToCloud',
        openId,
        skillKey,
        serverInstanceIds: activeInstanceIds,
        categoryId,
        title: pushTitle,
        description: pushDescription,
        descriptionProvided: true,
        content,
        publishMode: tail.publishMode,
        ...coverFields,
      },
      target
    );
  } else if (mode === 'img') {
    const sources = parseMediaSourcesArg(argv[2]);
    const title = String(argv[3] || '配图').trim() || '配图';
    let content = '';
    let description = '';
    let nextIdx = 4;
    if (argv[4] && /\.html?$/i.test(String(argv[4]))) {
      const htmlPath = resolveInputFile(argv[4]);
      if (!htmlPath) throw new Error('找不到 HTML: ' + argv[4]);
      content = fs.readFileSync(htmlPath, 'utf8');
      description = descriptionFromHtml(content);
      nextIdx = 5;
    } else {
      const opt = takeOptionalDescriptionArg(argv, 4);
      description = opt.description;
      nextIdx = opt.nextIndex;
    }
    const tail = takeTailTargetArgs(argv, nextIdx);
    const target = await resolveTargetFromConfigAndArgs(
      cfg,
      apiBase,
      openId,
      skillKey,
      activeInstanceIds,
      tail.targetScope,
      tail.ids,
      'newspic'
    );
    activeInstanceIds = target.serverInstanceIds || activeInstanceIds;
    const urls = await resolveMediaUrls(apiBase, openId, skillKey, sources);
    body = attachTargetFields(
      {
        action: 'sendToCloud',
        openId,
        skillKey,
        serverInstanceIds: activeInstanceIds,
        categoryId: 'newspic',
        title,
        description,
        descriptionProvided: true,
        imgUrls: urls,
        publishMode: tail.publishMode,
        ...(content ? { content } : {}),
      },
      target
    );
  } else if (mode === 'video') {
    const sources = parseMediaSourcesArg(argv[2]);
    const title = String(argv[3] || '视频').trim() || '视频';
    const opt = takeOptionalDescriptionArg(argv, 4);
    const description = opt.description;
    const tail = takeTailTargetArgs(argv, opt.nextIndex);
    const target = await resolveTargetFromConfigAndArgs(
      cfg,
      apiBase,
      openId,
      skillKey,
      activeInstanceIds,
      tail.targetScope,
      tail.ids,
      'video'
    );
    activeInstanceIds = target.serverInstanceIds || activeInstanceIds;
    const firstLocal = sources.map((s) => resolveLocalPath(s)).find(Boolean) || '';
    const coverAssets = resolveCoverAssets({ kind: 'video', anchorPath: firstLocal });
    if (!coverAssets.coverImagePath && !coverAssets.coverHtml) {
      console.warn(
        '作品目录下找不到封面（cover.png / cover.html）（本次跳过封面）'
      );
    }
    const urls = await resolveMediaUrls(apiBase, openId, skillKey, sources);
    const coverFields = await buildCoverFields(
      apiBase,
      openId,
      skillKey,
      coverAssets
    );
    body = attachTargetFields(
      {
        action: 'sendToCloud',
        openId,
        skillKey,
        serverInstanceIds: activeInstanceIds,
        categoryId: 'video',
        title,
        description,
        descriptionProvided: true,
        imgUrls: urls,
        publishMode: tail.publishMode,
        ...coverFields,
      },
      target
    );
  } else {
    throw new Error('第二参须为 html、img、video、list-targets 或 resolve');
  }

  console.log('推送到云电脑', {
    apiBase,
    serverInstanceIds: activeInstanceIds,
    categoryId: body.categoryId,
    title: body.title,
    description: body.description || '',
    descriptionProvided: body.descriptionProvided === true,
    targetScope: body.targetScope || 'all',
    receiverAccountIds: body.receiverAccountIds || [],
    receiverBrowserProfileIds: body.receiverBrowserProfileIds || [],
    hasCoverHtml: Boolean(body.coverHtml),
    hasCoverImageUrl: Boolean(body.coverImageUrl),
    imgUrls: body.imgUrls || undefined,
  });

  try {
    const res = await postJson(apiBase, body);
    console.log('HTTP', res.status, JSON.stringify(res.body, null, 2));
    if (!res.body || res.body.success === false) process.exit(2);
    const taskId =
      res.body.taskId ||
      (res.body.results && res.body.results[0] && res.body.results[0].taskId);
    console.log(
      '投递成功（已入队）' +
        (taskId ? ' taskId=' + taskId : '') +
        '。云端执行较慢，到此结束，勿轮询、勿重复推送。'
    );
  } catch (e) {
    if (/timeout/i.test(String(e.message || ''))) {
      console.warn(
        '请求超时：任务可能已投递入队。云端执行较慢，请视为投递成功，勿重复推送。'
      );
      process.exit(0);
    }
    console.error(e);
    process.exit(1);
  }
}

main().catch((e) => {
  if (e && e.exitCode) {
    console.error(e.message || e);
    process.exit(e.exitCode);
  }
  console.error(e);
  process.exit(1);
});
