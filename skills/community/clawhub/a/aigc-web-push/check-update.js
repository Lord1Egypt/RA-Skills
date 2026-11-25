#!/usr/bin/env node
/**
 * 推送前对照远端最新版；若落后则提示 Agent 询问用户是否升级，不自动覆盖本地文件。
 * 网络失败不阻断推送；确认落后时由 push.js 暂停，待用户决定后再继续。
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const SKILL_SLUG = 'aigc-web-push';
const REGISTRY = 'https://clawhub.ai';
const CHECK_TTL_MS = 24 * 60 * 60 * 1000;
const REQUEST_TIMEOUT_MS = 12_000;

function skillDir() {
  return __dirname;
}

function readText(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8').trim();
  } catch {
    return '';
  }
}

function readLocalVersion(dir) {
  try {
    const pkg = JSON.parse(
      fs.readFileSync(path.join(dir, 'package.json'), 'utf8')
    );
    const v = pkg && String(pkg.version || '').trim();
    if (v) return v;
  } catch {
    /* fall through */
  }
  return readText(path.join(dir, 'VERSION')) || '0.0.0';
}

function parseSemver(v) {
  const m = String(v || '')
    .trim()
    .replace(/^v/i, '')
    .match(/^(\d+)\.(\d+)\.(\d+)/);
  if (!m) return null;
  return [Number(m[1]), Number(m[2]), Number(m[3])];
}

function cmpSemver(a, b) {
  const pa = parseSemver(a);
  const pb = parseSemver(b);
  if (!pa || !pb) return 0;
  for (let i = 0; i < 3; i++) {
    if (pa[i] !== pb[i]) return pa[i] < pb[i] ? -1 : 1;
  }
  return 0;
}

function isDesignSourceTree(dir) {
  const norm = path.resolve(dir).replace(/\\/g, '/');
  return /\/design\/public\/aigc-web-push\/?$/.test(norm);
}

function readAutoUpdateFlag(dir) {
  try {
    const cfg = JSON.parse(fs.readFileSync(path.join(dir, 'config.json'), 'utf8'));
    if (cfg && cfg.autoUpdate === false) return false;
  } catch {
    /* no config or invalid — allow check */
  }
  return true;
}

function readCheckCache(dir) {
  try {
    return JSON.parse(fs.readFileSync(path.join(dir, '.update-check'), 'utf8'));
  } catch {
    return null;
  }
}

function writeCheckCache(dir, data) {
  try {
    fs.writeFileSync(
      path.join(dir, '.update-check'),
      JSON.stringify({ ...data, checkedAt: Date.now() }, null, 2) + '\n',
      'utf8'
    );
  } catch (err) {
    console.warn('[aigc-web-push] 无法写入 .update-check:', err.message);
  }
}

function requestBuffer(urlString, redirects = 0) {
  return new Promise((resolve, reject) => {
    if (redirects > 5) {
      reject(new Error('too many redirects'));
      return;
    }
    const u = new URL(urlString);
    const lib = u.protocol === 'http:' ? http : https;
    const req = lib.request(
      {
        protocol: u.protocol,
        hostname: u.hostname,
        port: u.port || (u.protocol === 'http:' ? 80 : 443),
        path: u.pathname + u.search,
        method: 'GET',
        headers: { Accept: '*/*', 'User-Agent': 'aigc-web-push-check-update' },
      },
      (res) => {
        if (
          res.statusCode >= 300 &&
          res.statusCode < 400 &&
          res.headers.location
        ) {
          const next = new URL(res.headers.location, u).toString();
          res.resume();
          resolve(requestBuffer(next, redirects + 1));
          return;
        }
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const buf = Buffer.concat(chunks);
          if (res.statusCode < 200 || res.statusCode >= 300) {
            reject(
              new Error(
                `HTTP ${res.statusCode} ${urlString}: ${buf.toString('utf8').slice(0, 200)}`
              )
            );
            return;
          }
          resolve(buf);
        });
      }
    );
    req.setTimeout(REQUEST_TIMEOUT_MS, () => {
      req.destroy(new Error(`timeout ${REQUEST_TIMEOUT_MS}ms`));
    });
    req.on('error', reject);
    req.end();
  });
}

async function requestJson(urlString) {
  const buf = await requestBuffer(urlString);
  return JSON.parse(buf.toString('utf8'));
}

function skillApi(pathname, query) {
  const u = new URL(`${REGISTRY}/api/v1/skills/${SKILL_SLUG}${pathname}`);
  if (query) {
    for (const [k, v] of Object.entries(query)) {
      if (v != null && v !== '') u.searchParams.set(k, String(v));
    }
  }
  return u.toString();
}

function printOutdatedHint(local, latest) {
  // 给用户看的只问一句；同意/拒绝后的操作见 SKILL.md「版本检查」
  console.warn(
    `[aigc-web-push] 发现新版本 ${local} → ${latest}。请询问用户是否升级本技能。`
  );
}

/**
 * @returns {Promise<{ updated: boolean, outdated?: boolean, skipped?: boolean, from?: string, to?: string, reason?: string }>}
 */
async function ensureUpToDate(options = {}) {
  const dir = options.dir || skillDir();
  const force = options.force === true;

  if (process.env.AIGC_WEB_PUSH_NO_UPDATE === '1') {
    return { updated: false, skipped: true, reason: 'env' };
  }
  if (isDesignSourceTree(dir)) {
    return { updated: false, skipped: true, reason: 'source' };
  }
  if (!readAutoUpdateFlag(dir)) {
    return { updated: false, skipped: true, reason: 'config' };
  }

  const local = readLocalVersion(dir);

  if (!force) {
    const cache = readCheckCache(dir);
    if (
      cache &&
      typeof cache.checkedAt === 'number' &&
      Date.now() - cache.checkedAt < CHECK_TTL_MS
    ) {
      if (cache.latest && cmpSemver(local, cache.latest) < 0) {
        printOutdatedHint(local, cache.latest);
        return { updated: false, outdated: true, from: local, to: cache.latest };
      }
      return { updated: false, skipped: true, reason: 'cache' };
    }
  }

  let latest;
  try {
    const meta = await requestJson(skillApi(''));
    latest = meta && meta.latestVersion && meta.latestVersion.version;
  } catch (err) {
    console.warn('[aigc-web-push] 检查更新失败，继续用当前版本:', err.message);
    return { updated: false, skipped: true, reason: 'network' };
  }

  if (!latest) {
    writeCheckCache(dir, { local, latest: null });
    return { updated: false, skipped: true, reason: 'no-latest' };
  }

  writeCheckCache(dir, { local, latest });

  if (cmpSemver(local, latest) >= 0) {
    return { updated: false, from: local, to: latest };
  }

  printOutdatedHint(local, latest);
  return { updated: false, outdated: true, from: local, to: latest };
}

module.exports = {
  ensureUpToDate,
  readLocalVersion,
  cmpSemver,
  isDesignSourceTree,
};

if (require.main === module) {
  ensureUpToDate({ force: process.argv.includes('--force') })
    .then((r) => {
      console.log(JSON.stringify(r));
      process.exit(r.outdated ? 2 : 0);
    })
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
}
