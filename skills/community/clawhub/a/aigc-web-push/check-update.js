#!/usr/bin/env node
/**
 * 推送前对齐 ClawHub 最新版（保留 config.json）。
 * 失败开放：网络错误只告警，不阻断推送。
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const SKILL_SLUG = 'aigc-web-push';
const REGISTRY = 'https://clawhub.ai';
const CHECK_TTL_MS = 24 * 60 * 60 * 1000;
const REQUEST_TIMEOUT_MS = 12_000;

const PROTECTED_NAMES = new Set([
  'config.json',
  '.update-check',
  '.git',
  '.gitignore',
]);

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
  // Prefer package.json（各 skill 商店都收 .json）；兼容旧包里的 VERSION
  try {
    const pkg = JSON.parse(
      fs.readFileSync(path.join(dir, 'package.json'), 'utf8')
    );
    const v = pkg && String(pkg.version || '').trim();
    if (v) return v;
  } catch {
    /* fall through */
  }
  const legacy = readText(path.join(dir, 'VERSION'));
  return legacy || '0.0.0';
}

function writeLocalVersion(dir, version) {
  const pkgPath = path.join(dir, 'package.json');
  try {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    pkg.version = version;
    fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n', 'utf8');
    return;
  } catch {
    /* create minimal pin if missing */
  }
  fs.writeFileSync(
    pkgPath,
    JSON.stringify(
      {
        name: 'aigc-web-push',
        private: true,
        version,
        type: 'commonjs',
        description:
          'Local module type pin so push.js stays CommonJS under design/ (not an npm publish).',
      },
      null,
      2
    ) + '\n',
    'utf8'
  );
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
    /* no config or invalid — allow update */
  }
  return true;
}

function readCheckCache(dir) {
  try {
    const j = JSON.parse(fs.readFileSync(path.join(dir, '.update-check'), 'utf8'));
    return j;
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

function safeRelPath(p) {
  const rel = String(p || '').replace(/\\/g, '/').replace(/^\/+/, '');
  if (!rel || rel.includes('..') || path.isAbsolute(rel)) return null;
  const base = path.basename(rel);
  if (PROTECTED_NAMES.has(base) || PROTECTED_NAMES.has(rel)) return null;
  return rel;
}

async function downloadVersionFiles(dir, version) {
  const meta = await requestJson(
    skillApi(`/versions/${encodeURIComponent(version)}`)
  );
  const files = (meta && meta.version && meta.version.files) || [];
  if (!files.length) {
    throw new Error(`版本 ${version} 无文件列表`);
  }

  let written = 0;
  for (const f of files) {
    const rel = safeRelPath(f.path);
    if (!rel) continue;
    const buf = await requestBuffer(
      skillApi('/file', { path: rel, version })
    );
    const dest = path.join(dir, rel);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, buf);
    written += 1;
  }

  // 升级后把 semver 写回 package.json，避免反复全量拉取
  const current = readLocalVersion(dir);
  if (!current || current === '0.0.0' || cmpSemver(current, version) < 0) {
    writeLocalVersion(dir, version);
    written += 1;
  }
  // 清掉旧无扩展名 VERSION（部分商店如腾讯 SkillHub 拒收）
  try {
    fs.unlinkSync(path.join(dir, 'VERSION'));
  } catch {
    /* absent */
  }

  return written;
}

/**
 * @returns {Promise<{ updated: boolean, skipped?: boolean, from?: string, to?: string, reason?: string }>}
 */
async function ensureUpToDate(options = {}) {
  const dir = options.dir || skillDir();
  const force = options.force === true;

  if (process.env.AIGC_WEB_PUSH_NO_UPDATE === '1') {
    return { updated: false, skipped: true, reason: 'env' };
  }
  if (process.env.AIGC_WEB_PUSH_REEXEC === '1') {
    return { updated: false, skipped: true, reason: 'reexec' };
  }
  if (isDesignSourceTree(dir)) {
    return { updated: false, skipped: true, reason: 'source' };
  }
  if (!readAutoUpdateFlag(dir)) {
    return { updated: false, skipped: true, reason: 'config' };
  }

  if (!force) {
    const cache = readCheckCache(dir);
    if (
      cache &&
      typeof cache.checkedAt === 'number' &&
      Date.now() - cache.checkedAt < CHECK_TTL_MS
    ) {
      return { updated: false, skipped: true, reason: 'cache' };
    }
  }

  const local = readLocalVersion(dir);
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

  if (cmpSemver(local, latest) >= 0) {
    writeCheckCache(dir, { local, latest });
    return { updated: false, from: local, to: latest };
  }

  console.log(`[aigc-web-push] 发现新版本 ${local} → ${latest}，正在升级…`);
  try {
    const n = await downloadVersionFiles(dir, latest);
    writeCheckCache(dir, { local: latest, latest, filesWritten: n });
    console.log(`[aigc-web-push] 已升级到 ${latest}（${n} 个文件）`);
    return { updated: true, from: local, to: latest };
  } catch (err) {
    console.warn('[aigc-web-push] 升级失败，继续用当前版本:', err.message);
    return { updated: false, skipped: true, reason: 'download', from: local, to: latest };
  }
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
      process.exit(r.updated ? 0 : 0);
    })
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
}
