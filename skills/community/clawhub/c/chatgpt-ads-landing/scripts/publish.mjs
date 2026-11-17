#!/usr/bin/env node
/**
 * (Optional) Deploy a chatgpt-ads-landing page to a compatible hosting platform and run its landing-page audit — through
 * the platform's open API (api-key from a device-code login; set BV_API_BASE and BV_APP_ID first), no manual zip upload.
 *
 *   node publish.mjs login  [--app-id <id>] [--api-base <url>]
 *   node publish.mjs whoami | logout
 *   node publish.mjs deploy <repo> <slug> [--remark <text>] [--keep-password] [--no-wait] [--dry-run]
 *   node publish.mjs audit  <url> [--site <site_id>] [--countries US,GB] [--lang zh-CN] [--out <file>]
 *   node publish.mjs ship   <repo> <slug> [deploy options] [audit options]      deploy, then audit
 *
 * deploy
 *   - site known (page.json deploy.siteId, or found by page.json url) → package.js (must pass)
 *     → upload dist/<slug>/ to the STS staging dir → UpdateSite(pending_dir) = 部署新版本
 *   - no site yet → package.js --force → upload → CreateSite → write site_url + siteId into
 *     page.json → package.js (must pass now) → upload → UpdateSite. One command replaces the
 *     two manual uploads of the first deploy.
 *   - 加密访问 is always switched off (OAI-AdsBot must be able to fetch the page) unless
 *     --keep-password; the platform clears it anyway when password_enabled is omitted.
 *   - waits until the live index.html equals dist/<slug>/index.html.
 *
 * audit
 *   async_job gpt_landing_audit (same job as the 体检 page) → poll → print the report grouped
 *   by basis (OpenAI 官方 / 法规 / 培训框架) and save the full JSON. It does not test pixel
 *   delivery or the consent flow — run verify.mjs for those.
 *
 * Env: BV_API_BASE, BV_APP_ID, BV_API_KEY (overrides the stored key), BV_CREDENTIALS.
 * Exit code 1 on any failure (and for audit: verdict not_recommended).
 */
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { extname, join, relative, resolve } from 'node:path';
import {
  api, ApiError, clearCredentials, cosPut, deviceLogin, readCredentials, sleep,
} from './lib/platform.mjs';

// ---------- args ----------
const argv = process.argv.slice(2);
const cmd = argv[0];
const opt = (name) => { const i = argv.indexOf(name); return i === -1 ? undefined : argv[i + 1]; };
const flag = (name) => argv.includes(name);
const VALUE_OPTS = ['--app-id', '--api-base', '--remark', '--site', '--countries', '--lang', '--out', '--timeout'];
const positional = argv.slice(1).filter((a, i, all) => !a.startsWith('--') && !VALUE_OPTS.includes(all[i - 1]));

const USAGE = `usage:
  publish.mjs login  [--app-id <id>] [--api-base <url>]
  publish.mjs whoami | logout
  publish.mjs deploy <repo> <slug> [--remark <text>] [--keep-password] [--no-wait] [--dry-run]
  publish.mjs audit  <url> [--site <site_id>] [--countries US,GB] [--lang zh-CN] [--out <file>]
  publish.mjs ship   <repo> <slug> [deploy + audit options]`;

// ---------- platform rules (hosting-platform upload rules) ----------
const CONTENT_TYPES = {
  html: 'text/html; charset=utf-8', htm: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8',
  js: 'text/javascript; charset=utf-8', mjs: 'text/javascript; charset=utf-8', json: 'application/json; charset=utf-8',
  map: 'application/json; charset=utf-8', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif',
  svg: 'image/svg+xml', webp: 'image/webp', ico: 'image/x-icon', bmp: 'image/bmp', woff: 'font/woff', woff2: 'font/woff2',
  ttf: 'font/ttf', eot: 'application/vnd.ms-fontobject', otf: 'font/otf', mp4: 'video/mp4', webm: 'video/webm',
  mp3: 'audio/mpeg', wav: 'audio/wav', txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8',
  pdf: 'application/pdf',
};
const MAX_BYTES = 50 * 1024 * 1024;
const PLACEHOLDER = /REPLACE/;

// ---------- small helpers ----------
const log = (s = '') => console.log(s);
const die = (msg) => { console.error(`\n✖ ${msg}`); process.exit(1); };
const rootUrl = (u) => String(u || '').replace(/[?#].*$/, '').replace(/\/*$/, '/');
const stamp = () => new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').slice(0, 13);

function pagePaths(repo, slug) {
  const root = resolve(repo);
  const pageJson = join(root, 'pages', slug, 'page.json');
  if (!existsSync(pageJson)) { die(`找不到 ${pageJson}`); }
  return { root, pageJson, dist: join(root, 'dist', slug) };
}
const readPage = (file) => JSON.parse(readFileSync(file, 'utf8'));
const writePage = (file, page) => writeFileSync(file, JSON.stringify(page, null, 2) + '\n');

function runPackage(root, slug, force) {
  log(`\n▶ node scripts/package.js ${slug}${force ? ' --force' : ''}`);
  try {
    execFileSync(process.execPath, [join(root, 'scripts', 'package.js'), slug, ...(force ? ['--force'] : [])],
      { cwd: root, stdio: 'inherit', env: { ...process.env, BV_PUBLISH: '1' } });
  } catch (e) { die('打包未通过，没有部署（看上面 check 的 ❌）'); }
}

function collectFiles(dist) {
  const files = [];
  (function walk(dir) {
    for (const name of readdirSync(dir)) {
      if (name.startsWith('.') || name === '__MACOSX') { continue; }
      const abs = join(dir, name);
      if (statSync(abs).isDirectory()) { walk(abs); continue; }
      const ext = extname(name).slice(1).toLowerCase();
      if (!CONTENT_TYPES[ext]) { die(`${relative(dist, abs)}: 平台不接收 .${ext} 文件`); }
      files.push({ rel: relative(dist, abs).split('\\').join('/'), abs, type: CONTENT_TYPES[ext] });
    }
  })(dist);
  if (!files.some((f) => f.rel === 'index.html')) { die(`${dist} 根目录没有 index.html`); }
  const total = files.reduce((n, f) => n + statSync(f.abs).size, 0);
  if (total > MAX_BYTES) { die(`总大小 ${(total / 1048576).toFixed(1)}MB 超过平台上限 50MB`); }
  return { files, total };
}

/** Upload dist/<slug>/ to a fresh staging dir; returns the dir to pass as pending_dir. */
async function uploadDist(cred, dist) {
  const { files, total } = collectFiles(dist);
  const credential = await api(cred, 'GET', '/v1/site-hosting/site/deploy-credential');
  const prefix = String(credential.dir).replace(/^\/+/, '').replace(/\/+$/, '');
  log(`  上传 ${files.length} 个文件（${(total / 1048576).toFixed(1)}MB）→ ${prefix}/`);
  const queue = [...files];
  let done = 0;
  const worker = async () => {
    for (let f = queue.shift(); f; f = queue.shift()) {
      if (Number(credential.expire) * 1000 < Date.now() + 5000) { throw new Error('上传凭证已过期，重新运行'); }
      const body = readFileSync(f.abs);
      for (let attempt = 0; ; attempt++) {
        try { await cosPut(credential, `${prefix}/${f.rel}`, body, f.type); break; } catch (e) {
          if (attempt >= 2) { throw e; }
          await sleep(1000 * (attempt + 1));
        }
      }
      done++;
    }
  };
  await Promise.all(Array.from({ length: Math.min(4, files.length) }, worker));
  log(`  ✓ ${done}/${files.length} 已上传`);
  return credential.dir;
}

/** Find this page's site: page.json deploy.siteId first, then by its url among the user's sites. */
async function resolveSite(cred, page) {
  if (page.deploy?.siteId) {
    return api(cred, 'GET', '/v1/site-hosting/site/detail', { query: { site_id: page.deploy.siteId } });
  }
  if (!page.url || PLACEHOLDER.test(page.url)) { return null; }
  const host = new URL(page.url).hostname;
  const res = await api(cred, 'GET', '/v1/site-hosting/site/list', { query: { keyword: host.split('.')[0], page_num: 1, page_size: 50 } });
  const hit = (res?.list || res?.items || []).find((s) => rootUrl(s.site_url) === rootUrl(page.url));
  if (!hit) { die(`page.json url ${page.url} 不是当前账号下的站点（可能是别人建的）。用该站点主的账号登录，或清空 url 新建站点`); }
  return api(cred, 'GET', '/v1/site-hosting/site/detail', { query: { site_id: hit.site_id } });
}

async function waitLive(url, indexFile) {
  if (flag('--no-wait')) { return null; }
  const want = readFileSync(indexFile);
  for (let i = 0; i < 18; i++) {
    try {
      const res = await fetch(`${url}?_bv_publish=${Date.now()}`, { cache: 'no-store', headers: { 'cache-control': 'no-cache' } });
      const got = Buffer.from(await res.arrayBuffer());
      if (res.ok && got.equals(want)) { log(`  ✓ 线上 index.html 与 dist 一致（HTTP ${res.status}）`); return true; }
    } catch (e) { /* retry */ }
    await sleep(5000);
  }
  log('  ⚠ 90 秒内线上 index.html 仍与 dist 不一致（可能是 CDN 缓存），用 verify.mjs --dist 再确认');
  return false;
}

function passwordFields(detail, keep) {
  if (keep && detail?.password_enabled) {
    log('  ⚠ --keep-password：加密访问保持开启。OAI-AdsBot 抓不到页面，广告过不了审，投放前必须关');
    return { password_enabled: true, password: detail.password || '' };
  }
  if (detail?.password_enabled) { log('  ⚠ 站点开着加密访问，本次部署会关闭（OAI-AdsBot 必须能访问）'); }
  return { password_enabled: false, password: '' };
}

// ---------- deploy ----------
async function deploy(cred, repo, slug) {
  const { root, pageJson, dist } = pagePaths(repo, slug);
  let page = readPage(pageJson);
  const remark = opt('--remark') || `chatgpt-ads-landing ${slug} ${stamp()}`;
  const site = await resolveSite(cred, page);

  if (flag('--dry-run')) {
    log(site
      ? `将部署新版本到站点 ${site.site_id}（${site.site_url}，当前版本 ${site.version}）`
      : `将新建站点（名称「${page.title || slug}」，子域名前缀 ${slug}），拿到地址后写回 page.json 再部署一次`);
    return null;
  }

  if (!site) {
    log(`\n■ 首次部署：新建站点`);
    runPackage(root, slug, PLACEHOLDER.test(String(page.url || '')));
    const pendingDir = await uploadDist(cred, dist);
    const created = await api(cred, 'POST', '/v1/site-hosting/site', {
      body: {
        name: page.title || slug, subdomain_hint: slug, entry: 'index.html',
        password_enabled: false, password: '', pending_dir: pendingDir, version_remark: `${remark}（首次部署，地址待回填）`,
      },
    });
    const url = rootUrl(created.site_url);
    log(`  ✓ 站点已创建：${url}（site_id ${created.site_id}）`);
    page = readPage(pageJson);
    page.url = url;
    page.deploy = { ...(page.deploy || {}), siteId: String(created.site_id) };
    writePage(pageJson, page);
    log(`  ✓ 已写回 pages/${slug}/page.json：url + deploy.siteId`);

    log(`\n■ 用真实地址重新打包并部署新版本`);
    runPackage(root, slug, false);
    const pendingDir2 = await uploadDist(cred, dist);
    const res = await api(cred, 'PUT', '/v1/site-hosting/site', {
      body: {
        site_id: String(created.site_id), name: page.title || slug, entry: 'index.html',
        password_enabled: false, password: '', pending_dir: pendingDir2, version_remark: remark,
      },
    });
    log(`  ✓ 已部署版本 ${res.version}`);
    await waitLive(url, join(dist, 'index.html'));
    return { url, siteId: String(created.site_id), page };
  }

  log(`\n■ 部署新版本：站点 ${site.site_id}（${site.site_url}，当前版本 ${site.version}）`);
  if (!site.enabled) { log('  ⚠ 站点处于下线状态：部署后仍无法访问，需要在托管平台里上线'); }
  if (!page.deploy?.siteId || !page.url || PLACEHOLDER.test(page.url)) {
    page.url = rootUrl(site.site_url);
    page.deploy = { ...(page.deploy || {}), siteId: String(site.site_id) };
    writePage(pageJson, page);
    log(`  ✓ 已写回 pages/${slug}/page.json：url + deploy.siteId`);
  }
  if (rootUrl(page.url) !== rootUrl(site.site_url)) {
    die(`page.json url（${page.url}）和站点地址（${site.site_url}）不一致，先确认要部署到哪个站点`);
  }
  runPackage(root, slug, false);
  const pendingDir = await uploadDist(cred, dist);
  const res = await api(cred, 'PUT', '/v1/site-hosting/site', {
    body: {
      site_id: String(site.site_id), name: site.name, entry: 'index.html',
      ...passwordFields(site, flag('--keep-password')), pending_dir: pendingDir, version_remark: remark,
    },
  });
  log(`  ✓ 已部署版本 ${res.version}（平台保留最近 3 个版本，可在托管平台一键回滚）`);
  await waitLive(rootUrl(site.site_url), join(dist, 'index.html'));
  return { url: rootUrl(site.site_url), siteId: String(site.site_id), page };
}

// ---------- audit ----------
const DIMENSIONS = {
  crawlability: '① 可抓取', semantic_structure: '② 语义结构', intent_match: '③ 意图匹配',
  credibility: '④ 可信度', conversion_path: '⑤ 转化路径', tech_experience: '⑥ 技术体验',
};
const VERDICTS = {
  recommended: '✅ 建议投放', recommended_with_improvements: '⚠️ 可以投放，建议改进', not_recommended: '❌ 不建议投放',
};
const BASIS = {
  openai_official: 'OpenAI 官方要求', regulation: '投放市场法规（一般做法，非法律意见）', training: '培训框架建议（内部标准，不是 OpenAI 要求）',
};
const STAGES = { fetching: '抓取', rendering: '渲染', evaluating: 'AI 评估', scoring: '评分' };
// Titles mirror gpt_landing_audit/audit/texts.py (zh); unknown codes print as-is.
const ITEM_TITLES = {
  crawl_robots_bots: 'robots.txt 未放行 AI 爬虫', crawl_robots_params: 'robots.txt 屏蔽带参数地址', crawl_sitemap: '没有可访问的 sitemap',
  crawl_no_js_text: '正文依赖 JS 渲染', crawl_adsbot_access: 'OAI-AdsBot 访问被拦截', crawl_no_redirect: '页面跳转到其他站点',
  sem_text_length: '有效正文过少', sem_title: '标题堆砌关键词', sem_fold_image: '首屏以大图为主、文字稀少', sem_jsonld: '缺少结构化数据',
  sem_headings: '标题层级不清晰', intent_user_questions: '用户常问的问题覆盖不足', intent_faq: '没有 FAQ 或问答内容',
  intent_self_centered: '自我介绍类文案过多', cred_claims: '关键主张缺少可验证依据', cred_qualifications: '没有可识别的资质信息',
  cred_privacy: '没有隐私政策', cred_contact: '没有联系方式', cred_sensitive: '命中广告政策敏感品类', conv_three_seconds: '首屏 3 秒看不清',
  conv_primary_cta: '首屏没有明确的行动按钮', conv_not_phone_only: '行动方式只有电话 / 表单', tech_https: 'HTTPS 有问题',
  tech_mobile: '移动端适配不佳', tech_lcp: '首屏加载慢', tech_multilang: '页面语言与投放市场不匹配', tech_no_overlay: '有侵入式弹窗',
};

async function audit(cred, url, { siteId, countries, lang, out }) {
  log(`\n■ GPT 落地页体检：${url}`);
  const payload = { url, language: lang };
  if (siteId) { payload.site_id = String(siteId); }
  if (countries?.length) { payload.target_countries = countries; }
  const sub = await api(cred, 'POST', '/v1/async_job/submit', { body: { job_type: 'gpt_landing_audit', payloads: [payload] } });
  const batchId = sub.batch_id;
  log(`  批次 ${batchId}（可在平台的落地页体检页面查看）`);

  const timeoutMs = Number(opt('--timeout') || 900) * 1000;
  const deadline = Date.now() + timeoutMs;
  let last = '';
  let status;
  while (Date.now() < deadline) {
    status = await api(cred, 'POST', '/v1/async_job/status', { body: { batch_id: batchId } });
    const row = status.items?.[0] || {};
    const line = `${status.status}${row.progress?.stage ? ` · ${STAGES[row.progress.stage] || row.progress.stage} ${row.progress.percent ?? ''}%` : ''}`;
    if (line !== last) { log(`  … ${line}`); last = line; }
    if (['success', 'failed', 'canceled'].includes(status.status)) { break; }
    await sleep(5000);
  }
  const row = status?.items?.[0];
  if (!status || !['success', 'failed', 'canceled'].includes(status.status)) {
    die(`体检 ${timeoutMs / 1000} 秒还没完成（批次 ${batchId}）。稍后在网页上看，或调 /v1/async_job/resume 重新拉起`);
  }
  if (status.status !== 'success') { die(`体检${status.status === 'failed' ? '失败' : '已取消'}：${row?.error || '无原因'}（批次 ${batchId}）`); }

  const detail = await api(cred, 'POST', '/v1/async_job/result', { body: { batch_id: batchId, id: row.id } });
  const report = detail.result;
  const file = out || join(process.cwd(), `gpt-audit-${batchId}.json`);
  mkdirSync(resolve(file, '..'), { recursive: true });
  writeFileSync(file, JSON.stringify({ batch_id: batchId, payload: detail.payload, ...report }, null, 2) + '\n');
  printReport(report);
  log(`\n  完整报告：${file}`);
  return report;
}

function printReport(r) {
  log(`\n  结论：${VERDICTS[r.verdict] || r.verdict}   规则版本 ${r.rubric_version}${r.final_url && rootUrl(r.final_url) !== rootUrl(r.url) ? `   最终地址 ${r.final_url}` : ''}`);
  if (r.network?.exit_country) { log(`  体检出口：${r.network.exit_country}`); }
  if (r.metrics) {
    const m = r.metrics;
    log(`  OAI-AdsBot HTTP ${m.status_code_adsbot ?? '-'} · 浏览器 HTTP ${m.status_code_browser ?? '-'} · 原始 HTML ${m.raw_text_chars ?? '-'} 字 · LCP ${m.lcp_ms ?? '-'}ms`);
  }
  log('');
  for (const d of r.dimensions || []) {
    log(`  ${(DIMENSIONS[d.key] || d.key).padEnd(8, '　')} ${'★'.repeat(d.score)}${'☆'.repeat(5 - d.score)} ${d.score}/5${d.incomplete ? '（有项目跳过）' : ''}  ${d.summary || ''}`);
  }
  const items = (r.dimensions || []).flatMap((d) => (d.items || []).map((i) => ({ ...i, dim: d.key })));
  const issues = items.filter((i) => i.status === 'fail' || i.status === 'warn');
  const skipped = items.filter((i) => i.status === 'skip');
  if (!issues.length) { log('\n  没有不通过或警告的检查项'); }
  for (const basis of ['openai_official', 'regulation', 'training']) {
    const group = issues.filter((i) => i.basis === basis);
    if (!group.length) { continue; }
    log(`\n  【${BASIS[basis]}】`);
    for (const i of group) {
      log(`  ${i.status === 'fail' ? '❌' : '⚠️'} [${i.severity}] ${ITEM_TITLES[i.code] || i.code}  (${i.code})`);
      if (i.evidence) { log(`      证据：${String(i.evidence).replace(/\s+/g, ' ').slice(0, 200)}`); }
      if (i.suggestion) { log(`      建议：${i.suggestion}`); }
    }
  }
  if (skipped.length) { log(`\n  跳过 ${skipped.length} 项：${skipped.map((i) => `${ITEM_TITLES[i.code] || i.code}（${i.evidence || '无原因'}）`).join('；')}`); }
}

// ---------- main ----------
async function main() {
  const cred = readCredentials();
  const countriesOpt = opt('--countries');
  const lang = opt('--lang') || 'zh-CN';

  switch (cmd) {
    case 'login': {
      const c = await deviceLogin({
        apiBase: opt('--api-base'), appId: opt('--app-id'),
        onCode: (code) => {
          log(`\n在浏览器打开下面的链接，确认用户码 ${code.user_code} 后点「同意授权」：\n\n  ${code.verification_url}\n`);
          log(`等待授权…（${Math.round((code.expires_in || 600) / 60)} 分钟内有效）`);
          if (process.platform === 'darwin' && !flag('--no-open')) {
            try { execFileSync('open', [code.verification_url]); } catch (e) { /* print-only */ }
          }
        },
      });
      log(`\n✔ 已登录 ${c.apiBase}${c.expireTime ? `，api-key 有效期至 ${c.expireTime}` : ''}\n  凭证：${readCredentials().file}（仅本人可读）`);
      return;
    }
    case 'logout':
      clearCredentials();
      log('✔ 已删除本机保存的 api-key');
      return;
    case 'whoami':
      log(`api 地址  ${cred.apiBase}\napp_id    ${cred.appId || '（未设置）'}\napi-key   ${cred.apiKey ? `已保存${cred.expireTime ? `，有效期至 ${cred.expireTime}` : ''}` : '未登录'}\n凭证文件  ${cred.file}`);
      if (cred.apiKey) {
        await api(cred, 'GET', '/v1/site-hosting/site/list', { query: { page_num: 1, page_size: 1 } });
        log('✔ api-key 可用（能读取站点列表）');
      }
      return;
    case 'deploy': {
      const [repo, slug] = positional;
      if (!repo || !slug) { die(USAGE); }
      const r = await deploy(cred, repo, slug);
      if (r) { log(`\n✔ 已上线 ${r.url}\n  下一步：node <skill>/scripts/verify.mjs ${r.url} --dist ${join(resolve(repo), 'dist', slug)} --proxy …`); }
      return;
    }
    case 'audit': {
      const [url] = positional;
      if (!url) { die(USAGE); }
      const report = await audit(cred, rootUrl(url), {
        siteId: opt('--site'), countries: countriesOpt ? countriesOpt.split(',').map((s) => s.trim().toUpperCase()) : [], lang, out: opt('--out'),
      });
      if (report.verdict === 'not_recommended') { process.exitCode = 1; }
      return;
    }
    case 'ship': {
      const [repo, slug] = positional;
      if (!repo || !slug) { die(USAGE); }
      const r = await deploy(cred, repo, slug);
      if (!r) { return; }
      const countries = countriesOpt ? countriesOpt.split(',').map((s) => s.trim().toUpperCase()) : Object.keys(r.page.routing?.sites || {});
      const out = opt('--out') || join(resolve(repo), 'out', `${slug}-audit-${stamp()}.json`);
      const report = await audit(cred, r.url, { siteId: r.siteId, countries, lang, out });
      log(`\n✔ 已上线并完成体检：${r.url}\n  Pixel / 各国跳转 / cookie 流程不在体检范围，接着跑：\n  node <skill>/scripts/verify.mjs ${r.url} --dist ${join(resolve(repo), 'dist', slug)} --proxy …`);
      if (report.verdict === 'not_recommended') { process.exitCode = 1; }
      return;
    }
    default:
      die(USAGE);
  }
}

main().catch((e) => die(e instanceof ApiError ? e.message : (e.stack || e.message)));
