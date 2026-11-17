const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { spawnSync } = require('node:child_process');
const lib = require('../src/index.js');

const python3Available = spawnSync('python3', ['-c', 'import zipfile'], { stdio: 'ignore' }).status === 0;

const jpg = Buffer.from([0xff,0xd8,0xff,0xe0,1,2,3,4,0xff,0xd9]);
const png = Buffer.from([0x89,0x50,0x4e,0x47,0x0d,0x0a,0x1a,0x0a,1,2,3]);
const mp4 = Buffer.from([0,0,0,20,0x66,0x74,0x79,0x70,0x69,0x73,0x6f,0x6d,0,0,0,0,0,0,0,0]);
const publicDns = async () => [{ address: '93.184.216.34', family: 4 }];

function streamOf(buf, chunk = 3) {
  let off = 0;
  return new ReadableStream({
    pull(controller) {
      if (off >= buf.length) {
        controller.close();
        return;
      }
      controller.enqueue(buf.subarray(off, off + chunk));
      off += chunk;
    }
  });
}
function res({ status = 200, url = 'https://instacognito.com/media?id=rotated', body = jpg, headers = { 'content-type': 'image/jpeg' } } = {}) {
  const lower = Object.fromEntries(Object.entries(headers).map(([k, v]) => [k.toLowerCase(), String(v)]));
  if (!lower['content-length']) lower['content-length'] = String(body.length);
  return { status, ok: status >= 200 && status < 300, url, headers: { get: k => lower[String(k).toLowerCase()] || null }, body: streamOf(body) };
}
async function tmp() { return await fsp.mkdtemp(path.join(os.tmpdir(), 'frameferry-test-')); }
async function readJson(file) { return JSON.parse(await fsp.readFile(file, 'utf8')); }
async function readManifest(out) { return readJson(path.join(out, '.frameferry', 'example', 'manifest.json')); }
async function readStatus(out) { return readJson(path.join(out, '.frameferry', 'example', 'status.json')); }
function section(category, items, extra = {}) {
  return { category, status: 'COMPLETE', items, ...extra };
}
function countNamedTests(text) {
  return [...text.matchAll(/test\('([^']+)'/g)].map(m => m[1]);
}

test('normalizes real provider carousel: one card per slide with same shortcode becomes multiple media', () => {
  const raw = [
    { shortcode: 'CAR', href: 'https://instacognito.com/media?id=1' },
    { shortcode: 'CAR', href: 'https://instacognito.com/media?id=2' },
    { shortcode: 'OTHER', href: 'https://instacognito.com/media?id=3' },
    { shortcode: 'CAR', carouselIndex: 1, href: 'https://instacognito.com/media?id=dup' }
  ];
  const n = lib.normalizeItems(raw);
  assert.equal(n.uniquePostCount, 2);
  assert.deepEqual(n.items.map(i => i.stableId), ['CAR-0', 'CAR-1', 'OTHER-0']);
});

test('repeat-page cards dedupe before assigning carousel indices', () => {
  const page = [
    { shortcode: 'CAR', href: 'https://instacognito.com/media?id=one', type: 'photo' },
    { shortcode: 'CAR', href: 'https://instacognito.com/media?id=two', type: 'photo' },
    { shortcode: 'OTHER', href: 'https://instacognito.com/media?id=three', type: 'photo' }
  ];
  const n = lib.normalizeItems([...page, ...page]);
  assert.deepEqual(n.items.map(i => i.stableId), ['CAR-0', 'CAR-1', 'OTHER-0']);
});

test('malformed dates are preserved instead of becoming invalid watermark', () => {
  assert.equal(lib.parseDateText(['views', 'not a date'].join('\n')), 'not a date');
});

test('reported count parser uses POSTS adjacency, not max followers/header integers', () => {
  assert.equal(lib.parseReportedTotal('Followers 125,000 Following 12 POSTS 68'), 68);
  assert.equal(lib.parseReportedTotal('68 posts 125,000 followers'), 68);
  assert.equal(lib.parseReportedTotal(['68', 'posts', '680.2k', 'followers', '656', 'following'].join('\n')), 68);
  assert.equal(lib.parseReportedTotal('125,000 followers only'), null);
});

test('unknown denom cannot claim complete and advertised shortfall is partial', async () => {
  assert.equal(lib.decideOutcome({ reportedTotal: null, uniquePostCount: 10, failed: 0 }).status, 'ACTION_REQUIRED');
  assert.equal(lib.decideOutcome({ reportedTotal: 20, uniquePostCount: 12, failed: 0 }).status, 'PARTIAL');
  const d = await tmp();
  const out = path.join(d, 'out');
  const unknown = await lib.archiveProfile({
    handle: 'example',
    output: out,
    reportedTotal: null,
    items: [{ shortcode: 'A', href: 'https://instacognito.com/media?id=a' }],
    dnsLookup: publicDns,
    fetchImpl: async () => res(),
    delayMs: 0
  });
  assert.equal(unknown.status, 'ACTION_REQUIRED');
  const short = await lib.archiveProfile({
    handle: 'example',
    output: out,
    mode: 'sync',
    reportedTotal: 3,
    noGrowth: true,
    items: [{ shortcode: 'A', href: 'https://instacognito.com/media?id=rotated' }],
    dnsLookup: publicDns,
    fetchImpl: async () => res(),
    delayMs: 0
  });
  assert.equal(short.status, 'PARTIAL');
  assert.match(short.sections[0].reason, /shortfall|no new cards/i);
});

test('provider URL validation rejects non-provider and non-https', () => {
  assert.throws(() => lib.validateProviderMediaUrl('http://instacognito.com/media?id=x'), /media URL/);
  assert.throws(() => lib.validateProviderMediaUrl('https://evil.test/media?id=x'), /media URL/);
  assert.doesNotThrow(() => lib.validateProviderMediaUrl('https://instacognito.com/media?id=x'));
});

test('redirect SSRF private hosts, mapped hex IPv6, CGNAT, and DNS failures are rejected', async () => {
  await assert.rejects(() => lib.validateRedirectTarget('https://127.0.0.1/x'), /private/);
  await assert.rejects(() => lib.validateRedirectTarget('https://localhost/x'), /private/);
  await assert.rejects(() => lib.validateRedirectTarget('https://example.com/x', async () => { throw new Error('dns down'); }), /failed closed/);
  assert.equal(lib.isPrivateIp('100.64.0.1'), true);
  assert.equal(lib.isPrivateIp('::ffff:127.0.0.1'), true);
  assert.equal(lib.isPrivateIp('0:0:0:0:0:ffff:7f00:1'), true);
});

test('handle traversal and output symlink are rejected', async () => {
  assert.throws(() => lib.validateHandle('../bad'), /handle/);
  const d = await tmp();
  const target = path.join(d, 'target');
  const link = path.join(d, 'link');
  await fsp.mkdir(target);
  await fsp.symlink(target, link);
  await assert.rejects(() => lib.safeOutputRoot(link), /symlink/);
});

test('download streams to .part, sha receipt, magic beats content type, and redacts signed urls', async () => {
  const d = await tmp();
  const root = await lib.safeOutputRoot(path.join(d, 'out'));
  const paths = lib.profilePaths(root, 'example');
  const item = { shortcode: 'ABC', carouselIndex: 0, href: 'https://instacognito.com/media?id=fixture-redacted-token', type: 'photo' };
  const got = await lib.downloadOne(item, paths, { dnsLookup: publicDns, fetchImpl: async () => res({ body: png, headers: { 'content-type': 'image/jpeg' } }), runId: 'r1' });
  assert.equal(got.receipt.bytes, png.length);
  assert.match(got.receipt.path, /.png$/);
  assert.match(got.receipt.sha256, /^[a-f0-9]{64}$/);
  assert.equal(fs.readdirSync(paths.mediaDir).some(n => n.endsWith('.part')), false);
  assert.equal(lib.redactSignedUrls(item.href), '[REDACTED instacognito media URL]');
});

test('HTML/truncation/oversize fail before unbounded buffering', async () => {
  const d = await tmp();
  const root = await lib.safeOutputRoot(path.join(d, 'out'));
  const paths = lib.profilePaths(root, 'example');
  const item = { shortcode: 'ABC', carouselIndex: 0, href: 'https://instacognito.com/media?id=x' };
  await assert.rejects(() => lib.downloadOne(item, paths, { dnsLookup: publicDns, fetchImpl: async () => res({ body: Buffer.from('<html></html>'), headers: { 'content-type': 'text/html' } }) }), /HTML/);
  await assert.rejects(() => lib.downloadOne(item, paths, { dnsLookup: publicDns, fetchImpl: async () => res({ headers: { 'content-type': 'image/jpeg', 'content-length': '999999' } }), maxBytes: 10 }), /exceeds/);
  await assert.rejects(() => lib.downloadOne(item, paths, { dnsLookup: publicDns, fetchImpl: async () => res({ headers: { 'content-type': 'image/jpeg', 'content-length': '99' } }) }), /length/);
});

test('429 Retry-After beyond budget persists DEFERRED and preserves prior completed evidence', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  const okItem = { shortcode: 'A', href: 'https://instacognito.com/media?id=a' };
  await lib.archiveProfile({ handle: 'example', output: out, reportedTotal: 1, items: [okItem], dnsLookup: publicDns, fetchImpl: async () => res(), delayMs: 0 });
  const deferItem = { shortcode: 'B', href: 'https://instacognito.com/media?id=b' };
  await assert.rejects(() => lib.archiveProfile({
    handle: 'example',
    output: out,
    reportedTotal: 2,
    items: [okItem, deferItem],
    dnsLookup: publicDns,
    fetchImpl: async url => url.includes('b') ? res({ status: 429, headers: { 'retry-after': '120', 'content-type': 'image/jpeg' } }) : res(),
    remainingMs: 1000,
    maxTimeMs: 1000,
    delayMs: 0
  }), err => err.code === 'DEFERRED');
  const status = await readStatus(out);
  const manifest = await readManifest(out);
  assert.equal(status.status, 'DEFERRED');
  assert.ok(status.retryAt);
  assert.equal(Object.keys(manifest.completed).length, 1);
});

test('429 within budget waits and retries same provider URL', async () => {
  const d = await tmp();
  const root = await lib.safeOutputRoot(path.join(d, 'out'));
  const paths = lib.profilePaths(root, 'example');
  const item = { shortcode: 'ABC', href: 'https://instacognito.com/media?id=x' };
  let calls = 0;
  const fetchImpl = async () => {
    calls++;
    return calls === 1 ? res({ status: 429, headers: { 'retry-after': '0', 'content-type': 'image/jpeg' } }) : res();
  };
  const got = await lib.downloadOne(item, paths, { dnsLookup: publicDns, fetchImpl, remainingMs: 1000, runId: 'r' });
  assert.equal(calls, 2);
  assert.equal(got.receipt.bytes, jpg.length);
});

test('sync reuses verified receipts: second run same IDs rotated URLs performs zero fetches', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  let calls = 0;
  const items1 = [{ shortcode: 'A', href: 'https://instacognito.com/media?id=oldA' }, { shortcode: 'B', href: 'https://instacognito.com/media?id=oldB' }];
  await lib.archiveProfile({ handle: 'example', output: out, mode: 'full', reportedTotal: 2, items: items1, dnsLookup: publicDns, fetchImpl: async () => { calls++; return res(); }, delayMs: 0 });
  calls = 0;
  const items2 = [{ shortcode: 'A', href: 'https://instacognito.com/media?id=newA' }, { shortcode: 'B', href: 'https://instacognito.com/media?id=newB' }];
  const s2 = await lib.archiveProfile({ handle: 'example', output: out, mode: 'sync', reportedTotal: 2, items: items2, dnsLookup: publicDns, fetchImpl: async () => { calls++; return res(); }, delayMs: 0 });
  assert.equal(s2.status, 'COMPLETE');
  assert.equal(s2.reusedCount, 2);
  assert.equal(calls, 0);
});

test('corrupted completed file is retried and repaired', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  let calls = 0;
  const item = { shortcode: 'A', href: 'https://instacognito.com/media?id=a' };
  await lib.archiveProfile({ handle: 'example', output: out, reportedTotal: 1, items: [item], dnsLookup: publicDns, fetchImpl: async () => { calls++; return res(); }, delayMs: 0 });
  await fsp.writeFile(path.join(out, 'media', 'example', 'A-0.jpg'), Buffer.from('bad'));
  calls = 0;
  const s = await lib.archiveProfile({ handle: 'example', output: out, mode: 'sync', reportedTotal: 1, items: [{ shortcode: 'A', href: 'https://instacognito.com/media?id=rotated' }], dnsLookup: publicDns, fetchImpl: async () => { calls++; return res(); }, delayMs: 0 });
  assert.equal(s.status, 'COMPLETE');
  assert.equal(calls, 1);
});

test('failed manifest entries do not persist signed URLs while fresh overlap retries', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  const item = { shortcode: 'A', href: 'https://instacognito.com/media?id=fixture-redacted' };
  await lib.archiveProfile({ handle: 'example', output: out, reportedTotal: 1, items: [item], dnsLookup: publicDns, fetchImpl: async () => res({ body: Buffer.from('bad'), headers: { 'content-type': 'image/jpeg' } }), delayMs: 0 });
  let manifest = await readManifest(out);
  assert.equal(JSON.stringify(manifest.failed).includes('media?id='), false);
  assert.equal(Object.keys(manifest.failed).length, 1);
  await lib.archiveProfile({ handle: 'example', output: out, reportedTotal: 1, items: [item], dnsLookup: publicDns, fetchImpl: async () => res(), delayMs: 0 });
  manifest = await readManifest(out);
  assert.equal(Object.keys(manifest.failed).length, 0);
});

test('live lock rejects alive PID and stale lock recovers', async () => {
  const d = await tmp();
  const root = await lib.safeOutputRoot(path.join(d, 'out'));
  const paths = lib.profilePaths(root, 'example');
  await fsp.mkdir(paths.stateDir, { recursive: true });
  await fsp.writeFile(paths.lock, JSON.stringify({ pid: process.pid, host: os.hostname(), runId: 'alive' }));
  await assert.rejects(() => lib.withLock(paths, 'r', async () => {}), /locked/);
  await fsp.writeFile(paths.lock, JSON.stringify({ pid: 99999999, host: os.hostname(), runId: 'stale' }));
  await lib.withLock(paths, 'r2', async () => 42);
  assert.equal(fs.existsSync(paths.lock), false);
});

test('secret redaction removes signed provider URLs from status-shaped text', () => {
  const redacted = lib.redactSignedUrls('failed https://instacognito.com/media?id=abcDEF123 more');
  assert.equal(redacted.includes('abcDEF123'), false);
  assert.equal(redacted.includes('media?id='), false);
});

test('CDP attach rejects non-loopback remote targets', async () => {
  await assert.rejects(() => lib.archiveProfile({ handle: 'example', output: path.join(os.tmpdir(), 'nope'), attachCdp: 'http://192.168.1.2:9222' }), /CDP|loopback/);
});

test('network timeout is capped by remaining maxTimeMs, not user larger networkTimeoutMs', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  const started = Date.now();
  const fetchImpl = async (_url, opts) => new Promise((_resolve, reject) => {
    opts.signal.addEventListener('abort', () => reject(Object.assign(new Error('aborted'), { name: 'AbortError' })), { once: true });
  });
  const s = await lib.archiveProfile({ handle: 'example', output: out, reportedTotal: 1, items: [{ shortcode: 'A', href: 'https://instacognito.com/media?id=slow' }], dnsLookup: publicDns, fetchImpl, maxTimeMs: 40, networkTimeoutMs: 5000, delayMs: 0 });
  assert.equal(s.status, 'PARTIAL');
  assert.ok(Date.now() - started < 1500);
});

test('profile extraction accepts a caller supplied timeout', async () => {
  let gotTimeout;
  const fakePage = { locator() { return { first() { return { innerText: async (opts) => { gotTimeout = opts.timeout; return 'POSTS 7'; } }; } }; } };
  assert.equal(await lib.extractReportedTotalFromPage(fakePage, 23), 7);
  assert.equal(gotTimeout, 23);
});

test('CLI doctor parses --attach-cdp without swallowing it as handle, and bad flags fail', () => {
  const bin = path.join(__dirname, '..', 'bin', 'frameferry.js');
  const bad = spawnSync(process.execPath, [bin, 'doctor', '--attach-cdp', 'http://192.168.1.2:9222'], { encoding: 'utf8' });
  assert.equal(bad.status, 1);
  assert.match(bad.stdout, /"cdpOk": false/);
  const miss = spawnSync(process.execPath, [bin, 'archive', 'example', '--max-pages'], { encoding: 'utf8' });
  assert.equal(miss.status, 1);
  assert.match(miss.stderr, /requires a value/);
  const unknown = spawnSync(process.execPath, [bin, 'doctor', '--bogus', 'value'], { encoding: 'utf8' });
  assert.equal(unknown.status, 1);
  assert.match(unknown.stderr, /not valid/);
  const inapplicable = spawnSync(process.execPath, [bin, 'doctor', '--output', 'x'], { encoding: 'utf8' });
  assert.equal(inapplicable.status, 1);
  assert.match(inapplicable.stderr, /not valid/);
});

test('actual Playwright DOM fixture models real carousel cards and profile-section POSTS parsing', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no existing chromium binary; not downloading'); return; }
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    const page = await browser.newPage();
    await page.setContent('<header>Followers 125,000</header><section id="profile-section"><span>125,000 followers</span><b>2 POSTS</b></section><div id="post-container"><article class="post-card"><div class="post-image" data-type="image"></div><div class="post-content"><p>Caption</p><a class="content-download-btn" href="https://instacognito.com/media?id=one">d</a></div><div class="post-footer"><div class="icon-group likes-trigger" data-id="CAR"><span>5</span></div><div class="icon-group comments-trigger" data-id="CAR"><span>1</span></div><div class="icon-group"><span>2024-01-01</span></div></div></article><article class="post-card"><div class="post-image" data-type="image"></div><div class="post-content"><p>Caption 2</p><a class="content-download-btn" href="https://instacognito.com/media?id=two">d</a></div><div class="post-footer"><div class="icon-group likes-trigger" data-id="CAR"><span>2</span></div><div class="icon-group comments-trigger" data-id="CAR"><span>0</span></div><div class="icon-group"><span>2024-01-01</span></div></div></article><article class="post-card"><div class="post-image" data-type="video"></div><div class="post-content"><p>Third</p><a class="content-download-btn" href="https://instacognito.com/media?id=three">d</a></div><div class="post-footer"><div class="icon-group likes-trigger" data-id="OTHER"><span>7</span></div><div class="icon-group"><span>2024-01-02</span></div></div></article></div>');
    const total = await lib.extractReportedTotalFromPage(page);
    const got = await lib.extractItemsFromPage(page, { category: 'posts', mediaTypes: ['image', 'video'], reportedTotal: total });
    assert.equal(total, 2);
    assert.equal(got.uniquePostCount, 2);
    assert.deepEqual(got.items.map(i => i.stableId), ['CAR-0', 'CAR-1', 'OTHER-0']);
  } finally {
    await browser.close();
  }
});

test('partial dates without explicit year preserve raw text', () => {
  assert.equal(lib.parseDateText(['views', '23 August'].join('\n')), '23 August');
  assert.match(lib.parseDateText(['views', '23 August 2024'].join('\n')), /^2024-/);
});

test('foreign-host and EPERM locks fail closed', async () => {
  const d = await tmp();
  const root = await lib.safeOutputRoot(path.join(d, 'out'));
  const paths = lib.profilePaths(root, 'example');
  await fsp.mkdir(paths.stateDir, { recursive: true });
  await fsp.writeFile(paths.lock, JSON.stringify({ pid: 99999999, host: 'other-host', runId: 'foreign' }));
  await assert.rejects(() => lib.withLock(paths, 'r', async () => {}), /another or unknown host/);
  await fsp.writeFile(paths.lock, JSON.stringify({ pid: 12345, host: os.hostname(), runId: 'eperm' }));
  const originalKill = process.kill;
  process.kill = () => { const e = new Error('no permission'); e.code = 'EPERM'; throw e; };
  try {
    await assert.rejects(() => lib.withLock(paths, 'r2', async () => {}), /locked by alive pid/);
  } finally {
    process.kill = originalKill;
  }
});

test('internal state/media/receipt symlink components are rejected', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  await fsp.mkdir(out, { recursive: true });
  await fsp.mkdir(path.join(d, 'elsewhere'));
  await fsp.symlink(path.join(d, 'elsewhere'), path.join(out, 'media'));
  await assert.rejects(() => lib.archiveProfile({ handle: 'example', output: out, reportedTotal: 1, items: [{ shortcode: 'A', href: 'https://instacognito.com/media?id=x' }], dnsLookup: publicDns, fetchImpl: async () => res(), delayMs: 0 }), /internal directory path contains symlink/);
});

test('pagination waits for delayed growth after explicit center scroll of already-visible last card', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no existing chromium binary; not downloading'); return; }
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    const page = await browser.newPage();
    await page.setContent(`<div id="post-container"><article class="post-card"><span data-id="P1"></span><a class="content-download-btn" href="https://instacognito.com/media?id=one">d</a></article></div><script>window.scrollCalls=[]; Element.prototype.scrollIntoView=function(opts){ window.scrollCalls.push(opts); setTimeout(()=>{ if(!document.querySelector('[data-id=P2]')) document.querySelector('#post-container').insertAdjacentHTML('beforeend','<article class="post-card"><span data-id="P2"></span><a class="content-download-btn" href="https://instacognito.com/media?id=two">d</a></article>'); }, 1100); };</script>`);
    const before = await lib.getRenderedCardState(page);
    const started = Date.now();
    const after = await lib.scrollLastCardCenterAndWaitForGrowth(page, before, { started, maxTimeMs: 7000, growthWaitMs: 5000 });
    const elapsed = Date.now() - started;
    assert.equal(after.grew, true);
    assert.ok(elapsed < 4200, 'settled before full growth window; elapsed=' + elapsed);
    assert.deepEqual(after.ids, ['P1', 'P2']);
    const calls = await page.evaluate(() => window.scrollCalls);
    assert.equal(calls[0].block, 'center');
  } finally {
    await browser.close();
  }
});

test('pagination no-growth waits only bounded budget before declaring no growth', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no existing chromium binary; not downloading'); return; }
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    const page = await browser.newPage();
    await page.setContent('<div id="post-container"><article class="post-card"><span data-id="ONLY"></span><a class="content-download-btn" href="https://instacognito.com/media?id=one">d</a></article></div>');
    const before = await lib.getRenderedCardState(page);
    const started = Date.now();
    const after = await lib.scrollLastCardCenterAndWaitForGrowth(page, before, { started, maxTimeMs: 5000, growthWaitMs: 400 });
    assert.equal(after.grew, false);
    assert.ok(Date.now() - started >= 350);
    assert.ok(Date.now() - started < 2000);
  } finally {
    await browser.close();
  }
});

test('pagination waits for partial batch to settle and recenters current last card', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no existing chromium binary; not downloading'); return; }
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    const page = await browser.newPage();
    await page.setContent(`<div id="post-container"><article class="post-card"><span data-id="P1"></span><a class="content-download-btn" href="https://instacognito.com/media?id=one">d</a></article></div><div id="loader" aria-busy="true"></div><script>window.scrollCalls=[]; Element.prototype.scrollIntoView=function(opts){ window.scrollCalls.push({opts, at: Date.now(), last: this.querySelector('[data-id]')?.getAttribute('data-id')}); if(!window.started){ window.started=1; setTimeout(()=>document.querySelector('#post-container').insertAdjacentHTML('beforeend','<article class="post-card"><span data-id="P2"></span><a class="content-download-btn" href="https://instacognito.com/media?id=two">d</a></article>'), 500); setTimeout(()=>{ document.querySelector('#post-container').insertAdjacentHTML('beforeend','<article class="post-card"><span data-id="P3"></span><a class="content-download-btn" href="https://instacognito.com/media?id=three">d</a></article>'); document.querySelector('#loader').remove(); }, 1300); } };</script>`);
    const before = await lib.getRenderedCardState(page);
    const started = Date.now();
    const after = await lib.scrollLastCardCenterAndWaitForGrowth(page, before, { started, maxTimeMs: 6000, growthWaitMs: 5000, settleMs: 700, recenterEveryMs: 600, maxRecenters: 3, targetUniqueCount: 3 });
    assert.equal(after.grew, true);
    assert.deepEqual(after.ids, ['P1', 'P2', 'P3']);
    const calls = await page.evaluate(() => window.scrollCalls);
    assert.ok(calls.length >= 2 && calls.length <= 3);
    assert.equal(calls[0].opts.block, 'center');
  } finally {
    await browser.close();
  }
});

test('pagination centers the provider top-level sentinel, not a trailing carousel child card', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no existing chromium binary; not downloading'); return; }
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    // Provider shape: R() appends each post's carousel slides as SIBLING .post-cards that inherit
    // the parent's data-id, and Te() observes only the last post's TOP-LEVEL card with a 200px
    // rootMargin. data-marker is test-only and is what distinguishes parent from slide, since the
    // provider renders byte-identical markup for both.
    const card = (marker, id, media) => '<article class="post-card" data-marker="' + marker + '"><span class="likes-trigger" data-id="' + id + '"><span>5</span></span><a class="content-download-btn" href="https://instacognito.com/media?id=' + media + '">d</a></article>';
    const lead = Array.from({ length: 8 }, (_, i) => card('lead', 'P' + (i + 1), 'lead' + i)).join('');
    const carousel = card('parent', 'PLAST', 'slide0') + Array.from({ length: 6 }, (_, i) => card('slide', 'PLAST', 'slide' + (i + 1))).join('');
    const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
    await page.setContent('<style>body{margin:0}#post-container{display:block}.post-card{display:block;height:300px;box-sizing:border-box;border:1px solid #ccc}</style><div id="post-container">' + lead + carousel + '</div><script>(function(){ const orig = Element.prototype.scrollIntoView; window.scrollCalls = []; Element.prototype.scrollIntoView = function(opts){ const tag = this.querySelector("[data-id]"); window.scrollCalls.push({ block: opts && opts.block, marker: this.getAttribute("data-marker"), id: tag ? tag.getAttribute("data-id") : null, index: Array.prototype.indexOf.call(document.querySelectorAll("#post-container .post-card"), this) }); return orig.call(this, opts); }; window.paginationFires = 0; const sentinel = document.querySelector(\'#post-container .post-card[data-marker="parent"]\'); const io = new IntersectionObserver(function(entries){ if (!entries[0].isIntersecting) return; io.disconnect(); window.paginationFires++; document.getElementById("post-container").insertAdjacentHTML("beforeend", \'<article class="post-card" data-marker="next"><span class="likes-trigger" data-id="PNEXT"><span>1</span></span><a class="content-download-btn" href="https://instacognito.com/media?id=next">d</a></article>\'); }, { rootMargin: "200px" }); io.observe(sentinel); })();</script>');

    // Precondition: the sentinel must start below viewport height + rootMargin, or the observer
    // fires on observe() and the negative half of this test proves nothing.
    const geometry = await page.evaluate(() => {
      const cards = [...document.querySelectorAll('#post-container .post-card')];
      const parent = document.querySelector('#post-container .post-card[data-marker="parent"]');
      return { parentIndex: cards.indexOf(parent), lastIndex: cards.length - 1, parentTop: parent.getBoundingClientRect().top, lastTop: cards[cards.length - 1].getBoundingClientRect().top, viewport: window.innerHeight };
    });
    assert.equal(geometry.parentIndex, 8);
    assert.equal(geometry.lastIndex, 14, 'sentinel must sit 6 slides above the final DOM card');
    assert.ok(geometry.parentTop > geometry.viewport + 200, 'sentinel must start outside viewport + rootMargin; top=' + geometry.parentTop);
    await page.waitForTimeout(250);
    assert.equal(await page.evaluate(() => window.paginationFires), 0, 'observer must not fire on load');

    // The pre-fix target: centering the final DOM card, which is the last carousel slide.
    await page.evaluate(() => { const cards = document.querySelectorAll('#post-container .post-card'); cards[cards.length - 1].scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'instant' }); });
    await page.waitForTimeout(500);
    assert.equal(await page.evaluate(() => window.paginationFires), 0, 'centering the last carousel slide must not reach the provider sentinel');
    assert.equal((await lib.getRenderedCardState(page)).count, 15, 'no growth from scrolling the wrong card');

    await page.evaluate(() => { window.scrollCalls = []; });
    const before = await lib.getRenderedCardState(page);
    assert.deepEqual(before.ids, ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'PLAST']);
    const started = Date.now();
    const after = await lib.scrollLastCardCenterAndWaitForGrowth(page, before, { started, maxTimeMs: 12000, growthWaitMs: 6000, settleMs: 500, maxRecenters: 1 });
    assert.equal(after.grew, true, 'centering the top-level sentinel must trigger provider pagination');
    assert.equal(after.sentinelIndex, 8);
    assert.equal(after.sentinelId, 'PLAST');
    assert.ok(after.ids.includes('PNEXT'), 'new batch must be observed: ' + JSON.stringify(after.ids));
    assert.equal(after.count, 16);
    assert.equal(await page.evaluate(() => window.paginationFires), 1);
    const calls = await page.evaluate(() => window.scrollCalls);
    assert.equal(calls.length, 1);
    assert.equal(calls[0].block, 'center');
    assert.equal(calls[0].id, 'PLAST');
    assert.equal(calls[0].marker, 'parent', 'must center the top-level sentinel, not a carousel slide; centered a ' + calls[0].marker);
    assert.equal(calls[0].index, 8);
  } finally {
    await browser.close();
  }
});

test('pagination follows the observed sentinel when the last post and its slides carry no data-id', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no existing chromium binary; not downloading'); return; }
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    // A zero-engagement post renders no .likes-trigger and no .comments-trigger, so neither it
    // nor its carousel slides carry a data-id anywhere. Every markup-based heuristic is blind
    // here; only the element the provider actually observes identifies the sentinel.
    const idCard = (marker, id, media) => '<article class="post-card" data-marker="' + marker + '"><span class="likes-trigger" data-id="' + id + '"><span>5</span></span><a class="content-download-btn" href="https://instacognito.com/media?id=' + media + '">d</a></article>';
    const blankCard = (marker, media) => '<article class="post-card" data-marker="' + marker + '"><a class="content-download-btn" href="https://instacognito.com/media?id=' + media + '">d</a></article>';
    const lead = Array.from({ length: 8 }, (_, i) => idCard('lead', 'P' + (i + 1), 'lead' + i)).join('');
    const carousel = blankCard('parent', 'slide0') + Array.from({ length: 6 }, (_, i) => blankCard('slide', 'slide' + (i + 1))).join('');
    const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
    // The fixture wraps IntersectionObserver first and only then lets the "provider" build its
    // observer, exactly the ordering scrapeWithPlaywright establishes between goto and search.
    await page.setContent('<style>body{margin:0}#post-container{display:block}.post-card{display:block;height:300px;box-sizing:border-box;border:1px solid #ccc}</style><div id="post-container">' + lead + carousel + '</div><script>(function(){ const attr = "data-ff-pagination-sentinel"; const Native = window.IntersectionObserver; function Probed(cb, opts){ const o = new Native(cb, opts); const nat = o.observe.bind(o); o.observe = function(target){ for (const m of document.querySelectorAll("[" + attr + "]")) m.removeAttribute(attr); target.setAttribute(attr, "1"); return nat(target); }; return o; } Probed.prototype = Native.prototype; window.IntersectionObserver = Probed; const orig = Element.prototype.scrollIntoView; window.scrollCalls = []; Element.prototype.scrollIntoView = function(opts){ window.scrollCalls.push({ block: opts && opts.block, marker: this.getAttribute("data-marker"), index: Array.prototype.indexOf.call(document.querySelectorAll("#post-container .post-card"), this) }); return orig.call(this, opts); }; window.paginationFires = 0; const sentinel = document.querySelector(\'#post-container .post-card[data-marker="parent"]\'); const io = new IntersectionObserver(function(entries){ if (!entries[0].isIntersecting) return; io.disconnect(); window.paginationFires++; document.getElementById("post-container").insertAdjacentHTML("beforeend", \'<article class="post-card" data-marker="next"><span class="likes-trigger" data-id="PNEXT"><span>1</span></span><a class="content-download-btn" href="https://instacognito.com/media?id=next">d</a></article>\'); }, { rootMargin: "200px" }); io.observe(sentinel); })();</script>');

    const setup = await page.evaluate(() => {
      const cards = [...document.querySelectorAll('#post-container .post-card')];
      const marked = document.querySelector('[data-ff-pagination-sentinel]');
      return { markedMarker: marked && marked.getAttribute('data-marker'), markedIndex: cards.indexOf(marked), lastIndex: cards.length - 1, markedTop: marked.getBoundingClientRect().top, viewport: window.innerHeight, idsPresent: cards.filter(c => c.querySelector('[data-id]')).length };
    });
    assert.equal(setup.markedMarker, 'parent', 'observe() must mark the element the provider watches');
    assert.equal(setup.markedIndex, 8);
    assert.equal(setup.lastIndex, 14, 'sentinel must sit 6 slides above the final DOM card');
    assert.equal(setup.idsPresent, 8, 'only the 8 lead posts carry a data-id');
    assert.ok(setup.markedTop > setup.viewport + 200, 'sentinel must start outside viewport + rootMargin; top=' + setup.markedTop);
    await page.waitForTimeout(250);
    assert.equal(await page.evaluate(() => window.paginationFires), 0, 'observer must not fire on load');

    // Both markup heuristics land here: with no data-id anywhere in the trailing run, the id-run
    // rule degrades to the last card, which is a slide six cards below the real sentinel.
    await page.evaluate(() => { const cards = document.querySelectorAll('#post-container .post-card'); cards[cards.length - 1].scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'instant' }); });
    await page.waitForTimeout(500);
    assert.equal(await page.evaluate(() => window.paginationFires), 0, 'centering the last slide must not reach the provider sentinel');
    assert.equal((await lib.getRenderedCardState(page)).count, 15, 'no growth from scrolling the wrong card');

    await page.evaluate(() => { window.scrollCalls = []; });
    const before = await lib.getRenderedCardState(page);
    assert.deepEqual(before.ids, ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']);
    const started = Date.now();
    const after = await lib.scrollLastCardCenterAndWaitForGrowth(page, before, { started, maxTimeMs: 12000, growthWaitMs: 6000, settleMs: 500, maxRecenters: 1 });
    assert.equal(after.grew, true, 'centering the observed sentinel must trigger provider pagination');
    assert.equal(after.sentinelSource, 'observed');
    assert.equal(after.sentinelIndex, 8);
    assert.equal(after.sentinelId, null, 'the sentinel legitimately has no data-id here');
    assert.ok(after.ids.includes('PNEXT'), 'new batch must be observed: ' + JSON.stringify(after.ids));
    assert.equal(after.count, 16);
    assert.equal(await page.evaluate(() => window.paginationFires), 1);
    const calls = await page.evaluate(() => window.scrollCalls);
    assert.equal(calls.length, 1);
    assert.equal(calls[0].block, 'center');
    assert.equal(calls[0].marker, 'parent', 'must center the observed sentinel, not a slide; centered a ' + calls[0].marker);
  } finally {
    await browser.close();
  }
});

test('sentinel probe marks each newly observed element, clears the previous one, and still paginates', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no existing chromium binary; not downloading'); return; }
  assert.equal(lib.PAGINATION_SENTINEL_ATTR, 'data-ff-pagination-sentinel', 'fixtures hardcode this attribute; keep them in step');
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
    await page.setContent('<div id="a">a</div><div id="b">b</div><div id="c">c</div>');
    assert.equal(await lib.installPaginationSentinelProbe(page), true);
    assert.equal(await lib.installPaginationSentinelProbe(page), true, 'installing twice must not double-wrap');

    const marks = await page.evaluate(attr => {
      const seen = [];
      const read = () => [...document.querySelectorAll('[' + attr + ']')].map(el => el.id).join(',');
      const first = new IntersectionObserver(() => {}); first.observe(document.getElementById('a')); seen.push(read());
      const second = new IntersectionObserver(() => {}); second.observe(document.getElementById('b')); seen.push(read());
      second.disconnect();
      const third = new IntersectionObserver(() => {}); third.observe(document.getElementById('c')); seen.push(read());
      return seen;
    }, lib.PAGINATION_SENTINEL_ATTR);
    assert.deepEqual(marks, ['a', 'b', 'c'], 'exactly one element is marked at a time and it is the latest observed');

    // The wrapper must not break the observer it wraps: a visible element still fires.
    const fired = await page.evaluate(() => new Promise(resolve => {
      const io = new IntersectionObserver(entries => { if (entries[0].isIntersecting) { io.disconnect(); resolve(true); } });
      io.observe(document.getElementById('a'));
      setTimeout(() => resolve(false), 2000);
    }));
    assert.equal(fired, true, 'wrapped observers must still deliver intersections');
  } finally {
    await browser.close();
  }
});

test('attached browser cleanup disconnects transport without closing external server marker', async () => {
  const events = [];
  const externalServer = { closed: false };
  const page = { close: async () => events.push('page.close') };
  const browser = { close: async () => events.push('browser.close') };
  await lib.cleanupScrapeBrowser(page, browser);
  assert.deepEqual(events, ['page.close', 'browser.close']);
  assert.equal(externalServer.closed, false);
});

test('normalizeItems keeps zero-engagement posts and stories without fake shortcodes', () => {
  const posts = lib.normalizeItems([{ href: 'https://instacognito.com/media?id=zero', mediaType: 'image', dateRaw: '2024-08-23' }], { category: 'posts', mediaTypes: ['image', 'video'] });
  assert.equal(posts.items.length, 1);
  assert.equal(posts.items[0].shortcode, null);
  assert.equal(posts.items[0].stableId, null);
  assert.equal(posts.items[0].identityBasis, 'content-sha256');
  const stories = lib.normalizeItems([{ href: 'https://instacognito.com/media?id=story', mediaType: 'image', captionTruncated: null }], { category: 'stories', mediaTypes: ['image', 'video'] });
  assert.equal(stories.items[0].identityBasis, 'content-sha256');
});

test('extractItemsFromPage understands provider-like posts/stories cards', async (t) => {
  let chromium;
  try { chromium = require('playwright').chromium; } catch { t.skip('playwright package unavailable'); return; }
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!exe || !fs.existsSync(exe)) { t.skip('no chromium binary'); return; }
  const browser = await chromium.launch({ headless: true, executablePath: exe });
  try {
    const page = await browser.newPage();
    await page.setContent('<div id="post-container"><article class="post-card"><div class="post-image" data-type="image"></div><div class="post-content"><p>Hello world</p><a class="content-download-btn" href="https://instacognito.com/media?id=a">d</a></div><div class="post-footer"><div class="icon-group likes-trigger" data-id="CAR"><span>5</span></div><div class="icon-group comments-trigger" data-id="CAR"><span>1</span></div><div class="icon-group"><span>2024-01-01</span></div></div></article><article class="post-card"><div class="post-image" data-type="video"></div><div class="post-content"><p>Zero social proof</p><a class="content-download-btn" href="https://instacognito.com/media?id=b">d</a></div><div class="post-footer"><div class="icon-group"><span>2024-01-02</span></div></div></article></div>');
    const posts = await lib.extractItemsFromPage(page, { category: 'posts', mediaTypes: ['image', 'video'] });
    assert.equal(posts.items.length, 2);
    assert.equal(posts.items[0].stableId, 'CAR-0');
    assert.equal(posts.items[1].stableId, null);
    await page.setContent('<div id="post-container"><article class="post-card"><div class="story-image" data-type="video"></div><div class="post-content"><a class="content-download-btn" href="https://instacognito.com/media?id=s1">d</a></div><div class="post-footer"><div class="icon-group"><span>23 August</span></div></div></article></div>');
    const stories = await lib.extractItemsFromPage(page, { category: 'stories', mediaTypes: ['image', 'video'] });
    assert.equal(stories.items.length, 1);
    assert.equal(stories.items[0].category, 'stories');
    assert.equal(stories.items[0].shortcode, null);
    assert.equal(stories.items[0].mediaType, 'video');
  } finally {
    await browser.close();
  }
});

test('archiveProfile reuses post receipts on stable IDs and rotated URLs', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  let calls = 0;
  await lib.archiveProfile({
    handle: 'example',
    output: out,
    sections: [section('posts', [
      { shortcode: 'A', href: 'https://instacognito.com/media?id=oldA', mediaType: 'image' },
      { shortcode: 'B', href: 'https://instacognito.com/media?id=oldB', mediaType: 'image' }
    ], { reportedTotal: 2 })],
    dnsLookup: publicDns,
    fetchImpl: async () => { calls++; return res(); },
    delayMs: 0
  });
  calls = 0;
  const second = await lib.archiveProfile({
    handle: 'example',
    output: out,
    mode: 'sync',
    sections: [section('posts', [
      { shortcode: 'A', href: 'https://instacognito.com/media?id=newA', mediaType: 'image' },
      { shortcode: 'B', href: 'https://instacognito.com/media?id=newB', mediaType: 'image' }
    ], { reportedTotal: 2 })],
    dnsLookup: publicDns,
    fetchImpl: async () => { calls++; return res(); },
    delayMs: 0
  });
  assert.equal(second.status, 'COMPLETE');
  assert.equal(second.reusedCount, 2);
  assert.equal(calls, 0);
});

test('stories re-fetch but dedupe after hashing because no stable provider ID exists', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  let calls = 0;
  const fetchImpl = async () => { calls++; return res({ body: png, headers: { 'content-type': 'image/png' } }); };
  await lib.archiveProfile({
    handle: 'example',
    output: out,
    sections: [section('stories', [{ href: 'https://instacognito.com/media?id=story1', mediaType: 'image' }])],
    dnsLookup: publicDns,
    fetchImpl,
    delayMs: 0
  });
  calls = 0;
  const second = await lib.archiveProfile({
    handle: 'example',
    output: out,
    mode: 'sync',
    sections: [section('stories', [{ href: 'https://instacognito.com/media?id=story2', mediaType: 'image' }])],
    dnsLookup: publicDns,
    fetchImpl,
    delayMs: 0
  });
  const manifest = await readManifest(out);
  assert.equal(calls, 1);
  assert.equal(Object.keys(manifest.completed).length, 1);
  assert.equal(second.reusedCount, 1);
});

test('category selection + unavailable section yields honest PARTIAL with section records', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  const result = await lib.archiveProfile({
    handle: 'example',
    output: out,
    categories: 'posts,highlights',
    sections: [
      section('posts', [{ shortcode: 'A', href: 'https://instacognito.com/media?id=a', mediaType: 'image' }], { reportedTotal: 1 }),
      { category: 'highlights', status: 'UNAVAILABLE', reason: 'provider exposed no highlight groups', items: [] }
    ],
    dnsLookup: publicDns,
    fetchImpl: async () => res(),
    delayMs: 0
  });
  assert.equal(result.status, 'PARTIAL');
  assert.equal(result.sections.length, 2);
  assert.equal(result.sections[1].status, 'UNAVAILABLE');
});

test('status and manifest sections never persist signed provider URLs', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  await lib.archiveProfile({
    handle: 'example',
    output: out,
    categories: 'posts,reels',
    sections: [
      section('posts', [{ shortcode: 'A', href: 'https://instacognito.com/media?id=secret-post', mediaType: 'image' }], { reportedTotal: 1 }),
      { category: 'reels', status: 'UNAVAILABLE', reason: 'provider exposed no reels for https://instacognito.com/media?id=secret-reel', items: [] }
    ],
    dnsLookup: publicDns,
    fetchImpl: async () => res(),
    delayMs: 0
  });
  const status = JSON.stringify(await readStatus(out));
  const manifest = JSON.stringify(await readManifest(out));
  assert.equal(status.includes('media?id='), false);
  assert.equal(manifest.includes('media?id='), false);
});

test('legacy post receipts without category still count toward uniquePostCount and export as posts', { skip: !python3Available }, async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  const zipPath = path.join(d, 'legacy.zip');
  await lib.archiveProfile({
    handle: 'example',
    output: out,
    sections: [section('posts', [{ shortcode: 'A', href: 'https://instacognito.com/media?id=a', mediaType: 'image' }], { reportedTotal: 1 })],
    dnsLookup: publicDns,
    fetchImpl: async () => res(),
    delayMs: 0
  });
  const manifestPath = path.join(out, '.frameferry', 'example', 'manifest.json');
  const receiptPath = path.join(out, 'receipts', 'example', 'A-0.json');
  const manifest = await readJson(manifestPath);
  delete manifest.completed['A-0'].category;
  await fsp.writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  const receipt = await readJson(receiptPath);
  delete receipt.category;
  await fsp.writeFile(receiptPath, JSON.stringify(receipt, null, 2) + '\n');
  const rerun = await lib.archiveProfile({
    handle: 'example',
    output: out,
    mode: 'sync',
    sections: [section('posts', [{ shortcode: 'A', href: 'https://instacognito.com/media?id=rotated', mediaType: 'image' }], { reportedTotal: 1 })],
    dnsLookup: publicDns,
    fetchImpl: async () => { throw new Error('should not fetch'); },
    delayMs: 0
  });
  assert.equal(rerun.uniquePostCount, 1);
  await lib.exportProfile({ handle: 'example', output: out, zip: zipPath });
  const py = spawnSync('python3', ['-c', [
    'import json, sys, zipfile',
    'z=zipfile.ZipFile(sys.argv[1])',
    'root=sorted({n.split("/",1)[0] for n in z.namelist()})[0]',
    'idx=json.loads(z.read(root+"/index.json"))',
    'print(idx[0]["category"])'
  ].join('\n'), zipPath], { encoding: 'utf8' });
  assert.equal(py.status, 0, py.stderr);
  assert.equal(py.stdout.trim(), 'posts');
});

test('exportProfile writes ZIP with metadata, checksums, and byte-exact media', { skip: !python3Available }, async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  const zipPath = path.join(d, 'export.zip');
  let call = 0;
  await lib.archiveProfile({
    handle: 'example',
    output: out,
    categories: 'posts,stories',
    sections: [
      section('posts', [{ shortcode: 'A', href: 'https://instacognito.com/media?id=a', mediaType: 'image', captionTruncated: 'caption', dateRaw: '2024-01-01' }], { reportedTotal: 1 }),
      section('stories', [{ href: 'https://instacognito.com/media?id=s', mediaType: 'video', dateRaw: '23 August', highlightGroup: null }])
    ],
    dnsLookup: publicDns,
    fetchImpl: async () => { call++; return call === 1 ? res({ body: jpg }) : res({ body: mp4, headers: { 'content-type': 'video/mp4' } }); },
    delayMs: 0
  });
  const exported = await lib.exportProfile({ handle: 'example', output: out, zip: zipPath });
  assert.equal(exported.totalEntryCount > 0, true);
  const py = spawnSync('python3', ['-c', [
    'import hashlib, json, sys, zipfile',
    'z=zipfile.ZipFile(sys.argv[1])',
    'assert z.testzip() is None',
    'root=sorted({n.split("/",1)[0] for n in z.namelist()})[0]',
    'idx=json.loads(z.read(root+"/index.json"))',
    'sections=json.loads(z.read(root+"/sections.json"))',
    'checks=z.read(root+"/checksums.txt").decode()',
    'assert "media?id=" not in z.read(root+"/sections.json").decode()',
    'assert "media?id=" not in z.read(root+"/manifest.json").decode()',
    'line_map={}',
    'for line in checks.strip().splitlines():',
    '    h,name=line.split("  ",1); line_map[name]=h',
    'for name in ["manifest.json","index.json","sections.json","README.txt"]:',
    '    assert hashlib.sha256(z.read(root+"/"+name)).hexdigest()==line_map[name]',
    'print(json.dumps({"entries": len(z.namelist()), "indexCount": len(idx), "sectionStatuses": [s["status"] for s in sections], "hasChecksums": "media/" in checks}))'
  ].join('\n'), zipPath], { encoding: 'utf8' });
  assert.equal(py.status, 0, py.stderr);
  const info = JSON.parse(py.stdout.trim());
  assert.equal(info.indexCount, 2);
  assert.deepEqual(info.sectionStatuses, ['COMPLETE', 'COMPLETE']);
  assert.equal(info.hasChecksums, true);
});

test('exportProfile rejects dangerous destinations and symlink ancestors', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  await lib.archiveProfile({
    handle: 'example',
    output: out,
    sections: [section('posts', [{ shortcode: 'A', href: 'https://instacognito.com/media?id=a', mediaType: 'image' }], { reportedTotal: 1 })],
    dnsLookup: publicDns,
    fetchImpl: async () => res(),
    delayMs: 0
  });
  await assert.rejects(() => lib.exportProfile({ handle: 'example', output: out, zip: path.join(out, 'bad.zip') }), /outside the archive root/);
  const parent = path.join(d, 'parent');
  const real = path.join(parent, 'real');
  const link = path.join(parent, 'link');
  await fsp.mkdir(real, { recursive: true });
  await fsp.symlink(real, link);
  await assert.rejects(() => lib.exportProfile({ handle: 'example', output: out, zip: path.join(link, 'bad.zip') }), /symlink/);
  const nested = path.join(d, 'new', 'dir', 'export.zip');
  await lib.exportProfile({ handle: 'example', output: out, zip: nested });
  assert.equal(fs.existsSync(nested), true);
});

test('exportProfile refuses corrupted bytes, stale part files, and zero zip limits', async () => {
  const d = await tmp();
  const out = path.join(d, 'out');
  const zipPath = path.join(d, 'export.zip');
  await lib.archiveProfile({
    handle: 'example',
    output: out,
    sections: [section('posts', [{ shortcode: 'A', href: 'https://instacognito.com/media?id=a', mediaType: 'image' }], { reportedTotal: 1 })],
    dnsLookup: publicDns,
    fetchImpl: async () => res(),
    delayMs: 0
  });
  await fsp.writeFile(zipPath + '.part', 'stale');
  await assert.rejects(() => lib.exportProfile({ handle: 'example', output: out, zip: zipPath }), /temporary .part/);
  await lib.exportProfile({ handle: 'example', output: out, zip: zipPath, overwriteZip: true });
  assert.equal(fs.existsSync(zipPath + '.part'), false);
  await assert.rejects(() => lib.exportProfile({ handle: 'example', output: out, zip: path.join(d, 'zero.zip'), maxZipBytes: 0 }), /positive number/);
  await fsp.writeFile(path.join(out, 'media', 'example', 'A-0.jpg'), Buffer.from('corrupt'));
  await assert.rejects(() => lib.exportProfile({ handle: 'example', output: out, zip: path.join(d, 'corrupt.zip') }), /receipt verification failed/);
});

test('CLI rejects bad category/media-type flags and keeps doctor parsing attach-cdp', () => {
  const bin = path.join(__dirname, '..', 'bin', 'frameferry.js');
  const badCategory = spawnSync(process.execPath, [bin, 'archive', 'example', '--output', 'x', '--categories', 'bogus'], { encoding: 'utf8' });
  assert.equal(badCategory.status, 1);
  assert.match(badCategory.stderr, /categories/);
  const badMedia = spawnSync(process.execPath, [bin, 'archive', 'example', '--output', 'x', '--media-types', 'audio'], { encoding: 'utf8' });
  assert.equal(badMedia.status, 1);
  assert.match(badMedia.stderr, /media-types/);
  const badCdp = spawnSync(process.execPath, [bin, 'doctor', '--attach-cdp', 'http://192.168.1.2:9222'], { encoding: 'utf8' });
  assert.equal(badCdp.status, 1);
  assert.match(badCdp.stdout, /"cdpOk": false/);
});

test('local CLI works from repo path without assuming global frameferry', () => {
  const bin = path.join(__dirname, '..', 'bin', 'frameferry.js');
  const version = spawnSync(process.execPath, [bin, '--version'], { encoding: 'utf8' });
  assert.equal(version.status, 0, version.stderr);
  assert.equal(version.stdout.trim(), lib.VERSION);
  const doctor = spawnSync(process.execPath, [bin, 'doctor'], { encoding: 'utf8' });
  const parsed = JSON.parse(doctor.stdout);
  assert.equal(typeof parsed.node, 'string');
  assert.equal(typeof parsed.playwright, 'boolean');
});

test('content-export branch retains at least the baseline test inventory plus new coverage', async () => {
  const baselineNames = [
    'normalizes real provider carousel: one card per slide with same shortcode becomes multiple media',
    'repeat-page cards dedupe before assigning carousel indices',
    'malformed dates are preserved instead of becoming invalid watermark',
    'reported count parser uses POSTS adjacency, not max followers/header integers',
    'unknown denom cannot claim complete and advertised shortfall is partial',
    'provider URL validation rejects non-provider and non-https',
    'redirect SSRF private hosts, mapped hex IPv6, CGNAT, and DNS failures are rejected',
    'handle traversal and output symlink are rejected',
    'download streams to .part, sha receipt, magic beats content type, and redacts signed urls',
    'HTML/truncation/oversize fail before unbounded buffering',
    '429 Retry-After beyond budget persists DEFERRED and preserves prior completed evidence',
    '429 within budget waits and retries same provider URL',
    'sync reuses verified receipts: second run same IDs rotated URLs performs zero fetches',
    'corrupted completed file is retried and repaired',
    'failed manifest entries do not persist signed URLs while fresh overlap retries',
    'live lock rejects alive PID and stale lock recovers',
    'secret redaction removes signed provider URLs from status-shaped text',
    'CDP attach rejects non-loopback remote targets',
    'network timeout is capped by remaining maxTimeMs, not user larger networkTimeoutMs',
    'profile extraction accepts a caller supplied timeout',
    'CLI doctor parses --attach-cdp without swallowing it as handle, and bad flags fail',
    'actual Playwright DOM fixture models real carousel cards and profile-section POSTS parsing',
    'partial dates without explicit year preserve raw text',
    'foreign-host and EPERM locks fail closed',
    'internal state/media/receipt symlink components are rejected',
    'pagination waits for delayed growth after explicit center scroll of already-visible last card',
    'pagination no-growth waits only bounded budget before declaring no growth',
    'pagination waits for partial batch to settle and recenters current last card',
    'attached browser cleanup disconnects transport without closing external server marker'
  ];
  const current = await fsp.readFile(__filename, 'utf8');
  const newNames = countNamedTests(current);
  for (const name of baselineNames) assert.ok(newNames.includes(name), 'missing baseline test: ' + name);
  assert.ok(newNames.length >= baselineNames.length + 6, 'expected expanded coverage beyond ' + baselineNames.length + ', got ' + newNames.length);
});
