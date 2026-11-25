import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { buildSearchExtractExpression as search, buildDetailExtractExpression as detail } from '../scripts/extract.mjs';

// Tiny in-memory DOM fixture for read-only extraction tests, not a production parser.
class Text {
  constructor(text) { this.nodeType = 3; this.nodeValue = text; }
  get textContent() { return this.nodeValue; }
}
class Element {
  constructor(tag, attrs = {}, children = []) { this.nodeType = 1; this.tagName = tag.toUpperCase(); this.attrs = attrs; this.childNodes = []; for (const c of children) this.append(c); }
  append(c) { if (typeof c === 'string') c = new Text(c); c.parentElement = this; this.childNodes.push(c); return this; }
  getAttribute(k) { return Object.hasOwn(this.attrs, k) ? this.attrs[k] : null; }
  get className() { return this.attrs.class || ''; } get id() { return this.attrs.id || ''; } get hidden() { return Object.hasOwn(this.attrs, 'hidden'); }
  get textContent() { return this.childNodes.map(c => c.textContent).join(''); }
  get innerText() { if (!this.getClientRects().length) return ''; return this.childNodes.map(c => c.nodeType === 3 ? c.textContent : c.innerText).join(' '); }
  getClientRects() { return this.hidden || this.attrs.style === 'display:none' ? [] : [{}]; }
  matches(selector) { return selector.split(',').some(s => match(this, s.trim())); }
  closest(selector) { for (let n = this; n?.nodeType === 1; n = n.parentElement) if (n.matches(selector)) return n; return null; }
  querySelectorAll(selector) { const out = []; const walk = n => { for (const c of n.childNodes || []) if (c.nodeType === 1) { if (c.matches(selector)) out.push(c); walk(c); } }; walk(this); return out; }
}
function compound(node, selector) {
  const tag = selector.match(/^[a-zA-Z][a-zA-Z0-9-]*/)?.[0]; if (tag && node.tagName !== tag.toUpperCase()) return false;
  for (const m of selector.matchAll(/\.([a-zA-Z0-9_-]+)|#([a-zA-Z0-9_-]+)|\[([^\]=*^\s]+)([*^]?=)?(?:"([^"]*)"|'([^']*)'|([^\]]*))?\]/g)) {
    if (m[1] && !node.className.split(/\s+/).includes(m[1])) return false;
    if (m[2] && node.id !== m[2]) return false;
    if (m[3]) { const val = node.getAttribute(m[3]); if (val === null) return false; const wanted = m[5] ?? m[6] ?? m[7] ?? ''; if (m[4] === '=' && val !== wanted) return false; if (m[4] === '*=' && !val.includes(wanted)) return false; if (m[4] === '^=' && !val.startsWith(wanted)) return false; }
  }
  return true;
}
function match(node, selector) {
  const tokens = selector.replaceAll('>', ' > ').trim().split(/\s+/); let i = tokens.length - 1;
  if (!compound(node, tokens[i])) return false;
  while (--i >= 0) {
    if (tokens[i] === '>') { node = node.parentElement; if (!node || !compound(node, tokens[--i])) return false; }
    else { let parent = node.parentElement; while (parent && !compound(parent, tokens[i])) parent = parent.parentElement; if (!parent) return false; node = parent; }
  }
  return true;
}
const el = (tag, attrs, ...children) => new Element(tag, attrs, children.flat());
function evaluate(expression, children, { url = 'https://www.bing.com/search?q=geo', title = '搜索', readyState = 'complete', head = [] } = {}) {
  const body = el('body', {}, children); const document = new Element('html', {}, [el('head', {}, head), body]); document.body = body; document.title = title; document.readyState = readyState;
  Object.defineProperty(document, 'cookie', { get() { throw new Error('cookie read forbidden'); } });
  const context = { document, location: { href: url }, URL, atob, Uint8Array, TextDecoder,
    getComputedStyle: n => ({ display: n.attrs.style === 'display:none' ? 'none' : 'block', visibility: 'visible' }),
    fetch: () => { throw new Error('network forbidden'); } };
  for (const key of ['localStorage', 'sessionStorage']) Object.defineProperty(context, key, { get() { throw new Error('storage read forbidden'); } });
  return JSON.parse(JSON.stringify(vm.runInNewContext(expression, context, { timeout: 1000 })));
}
const bingCard = (href, title = '实际文章', extra = []) => el('li', { class: 'b_algo' }, el('h2', {}, el('a', { href }, title)), ...extra);

test('Bing tracking URL is decoded as UTF-8; advertisements, navigation and nested duplicates are excluded', () => {
  const target = 'https://example.com/中文?q=GEO'; const redirect = 'https://www.bing.com/ck/a?u=a1' + Buffer.from(target).toString('base64url');
  const card = bingCard(redirect, '正文标题', [el('p', { class: 'snippet' }, '摘要')]);
  const r = evaluate(search('bing'), [el('header', {}, el('a', { href: 'https://example.com/nav' }, '导航')), card, bingCard('https://ads.example/a', '广告', []).append(el('span', {}, '')), el('li', { class: 'b_ad' }, bingCard('https://ads.example/b')), bingCard(redirect)]);
  assert.equal(r.items[0].url, new URL(target).href); assert.equal(r.items.filter(i => i.url === new URL(target).href).length, 1);
  assert.ok(!r.items.some(i => i.url.endsWith('/nav') || i.url === 'https://ads.example/b')); assert.equal(r.readyState, 'complete');
});

test('Bili real-content routes retain a full title attribute while author links are ignored', () => {
  const url = 'https://www.bilibili.com/video/BV1abcDEF123?vd_source=abc';
  const r = evaluate(search('bili'), [el('div', { class: 'bili-video-card' }, el('a', { href: 'https://space.bilibili.com/123' }, '作者主页'), el('a', { href: url, title: '完整 GEO 教程' }, el('h3', {}, 'GEO ', el('em', {}, '教程'))), el('a', { href: url }, '封面'))], { url: 'https://search.bilibili.com/all?keyword=geo' });
  assert.equal(r.items.length, 1); assert.equal(r.items[0].title, '完整 GEO 教程'); assert.equal(r.items[0].url, url); assert.equal(r.items[0].contentType, 'video');
});

test('XHS signed href is preserved privately and nested/repeated cards do not duplicate the note', () => {
  const href = '/explore/0123456789abcdef01234567?xsec_token=private-value&xsec_source=pc_search';
  const r = evaluate(search('xhs'), [el('section', { class: 'note-item' }, el('section', { class: 'note-item' }, el('a', { href, title: '经验<em>分享</em>' }, '经验分享')), el('a', { href: '/user/profile/0123456789abcdef01234567' }, '作者')), el('section', { class: 'note-item' }, el('a', { href: href.replace('private-value', 'another-value') }, '经验分享'))], { url: 'https://www.xiaohongshu.com/search_result?keyword=geo' });
  assert.equal(r.items.length, 1); assert.equal(r.items[0].title, '经验分享'); assert.ok(r.items[0].url.includes('xsec_token=private-value'));
});

test('visible captcha or login overlays suppress underlying results; hidden dialogs and header login do not', () => {
  for (const [text, flag] of [['请完成安全验证', 'captcha'], ['请先登录后搜索', 'loginRequired']]) {
    const r = evaluate(search('bing'), [bingCard('https://example.com/a'), el('div', { role: 'dialog' }, text)]);
    assert.equal(r.state[flag], true); assert.deepEqual(r.items, []); assert.equal(r.state.empty, false);
  }
  const r = evaluate(search('bing'), [el('header', {}, '登录'), bingCard('https://example.com/captcha-guide', '如何使用 captcha'), el('div', { role: 'dialog', style: 'display:none' }, '请先登录')]);
  assert.equal(r.items.length, 1); assert.equal(r.state.loginRequired, false); assert.equal(r.state.captcha, false);
});

test('empty results, loading and Google challenge are distinct states', () => {
  const empty = evaluate(search('bing'), [el('main', {}, '没有找到相关结果')]); assert.equal(empty.state.empty, true); assert.equal(empty.state.loading, false);
  const loading = evaluate(search('bing'), [el('main', {}, '加载中…')], { readyState: 'interactive' }); assert.equal(loading.state.loading, true); assert.equal(loading.state.empty, false);
  const captcha = evaluate(search('google'), [el('main', {}, 'Our systems have detected unusual traffic')], { url: 'https://www.google.com/sorry/index', title: 'Google' }); assert.equal(captcha.state.captcha, true); assert.deepEqual(captcha.items, []);
});

test('site index keeps the requested host boundary after a Google redirect', () => {
  const r = evaluate(search('site:example.com'), [bingCard('https://www.google.com/url?q=' + encodeURIComponent('https://docs.example.com/guide')), bingCard('https://example.com.evil.invalid/fake')], { url: 'https://www.google.com/search?q=site:example.com' });
  assert.equal(r.items.length, 1); assert.equal(r.items[0].url, 'https://docs.example.com/guide');
});

test('GitHub author profiles and star navigation are not code/repository results', () => {
  const r = evaluate(search('github'), [el('div', { class: 'repo-list-item' }, el('a', { href: '/owner' }, 'owner'), el('a', { href: '/owner/repo', title: 'owner/repo' }, 'repo'), el('a', { href: '/owner/repo/stargazers' }, 'stars'))], { url: 'https://github.com/search?q=geo&type=repositories' });
  assert.deepEqual(r.items.map(i => i.url), ['https://github.com/owner/repo']);
});

test('detail extracts primary article text rather than page navigation and sidebars', () => {
  const body = '正文事实与实际步骤。'.repeat(20);
  const r = evaluate(detail('csdn'), [el('header', {}, '站点导航和登录'), el('main', {}, el('article', {}, el('h1', {}, '文章题目'), el('div', { id: 'content_views' }, el('p', {}, body), el('aside', {}, '侧栏推荐不可进入正文'), el('footer', {}, '页脚推荐不可进入正文')))), el('aside', {}, '侧栏')], { url: 'https://blog.csdn.net/user/article/details/1234', head: [el('link', { rel: 'canonical', href: '/user/article/details/1234' })] });
  assert.ok(r.text.includes(body)); assert.ok(!/导航|侧栏|页脚/.test(r.text)); assert.equal(r.canonicalUrl, r.url); assert.equal(r.readyState, 'complete');
});

test('unsupported detail page does not treat its body navigation as article content or invent a canonical /null', () => {
  const r = evaluate(detail('site:example.com'), [el('header', {}, '只有菜单'), el('nav', {}, '首页产品登录')], { url: 'https://example.com/page' });
  assert.equal(r.text, ''); assert.equal(r.canonicalUrl, 'https://example.com/page');
});

test('detail overlay is blocking even when there is visible background article text', () => {
  const r = evaluate(detail('zhihu'), [el('article', {}, '背景文章。'.repeat(40)), el('div', { class: 'login-container' }, '扫码登录后查看内容')], { url: 'https://www.zhihu.com/question/123' });
  assert.equal(r.state.loginRequired, true); assert.equal(r.text, '');
});

test('bounded extraction leaves DOM and private APIs alone', () => {
  const r = evaluate(search('bing', { limit: 1, maxText: 45 }), [bingCard('https://example.com/a', '文章标题', [el('div', { class: 'b_caption' }, el('p', {}, '摘要'.repeat(100)))]), bingCard('https://example.com/b')]);
  assert.equal(r.items.length, 1); assert.ok(r.items.reduce((n, i) => n + i.title.length + i.snippet.length + (i.author?.length || 0) + (i.publishedAt?.length || 0) + i.metrics.raw.length, 0) <= 45);
  const d = evaluate(detail('site:example.com', { maxText: 40 }), [el('article', {}, '正文'.repeat(100))], { url: 'https://example.com/a' }); assert.ok(d.text.length <= 40);
  for (const opts of [{ limit: -1 }, { maxText: 0 }, { limit: '10' }]) assert.throws(() => search('bing', opts), { code: 'invalid_extract_options' });
});

test('a video duration is not a publication date and missing redirect targets are rejected', () => {
  const r = evaluate(search('bilibili'), [el('div', { class: 'bili-video-card' }, el('a', { href: 'https://www.bilibili.com/video/BV123abc456', title: '教程' }, '教程'), el('span', { class: 'time' }, '03:20'))], { url: 'https://search.bilibili.com/all?keyword=geo' });
  assert.equal(r.items[0].publishedAt, null);
  const redirect = evaluate(search('google'), [bingCard('https://www.google.com/url'), bingCard('https://www.google.com/url?q=javascript:alert(1)')], { url: 'https://www.google.com/search?q=geo' });
  assert.deepEqual(redirect.items, []);
});

test('XHS live DOM shape prefers the signed title search_result route over an empty explore or cover anchor', () => {
  const id = '0123456789abcdef01234567'; const href = '/search_result/' + id + '?xsec_token=fixture-only-not-a-real-token';
  const card = el('section', { class: 'note-item' }, el('a', { href: '/explore/' + id, style: 'display:none' }), el('a', { href, class: 'cover mask' }), el('div', { class: 'footer' }, el('a', { href, class: 'title' }, el('span', {}, '真实卡片 ', el('em', {}, '标题'))), el('a', { href: '/user/profile/' + id, class: 'author' }, el('div', { class: 'name' }, '演示作者')), el('div', { class: 'name-time-wrapper' }, el('div', { class: 'time' }, '昨天'))));
  const unsignedDuplicate = el('section', { class: 'note-item' }, el('a', { href: '/explore/' + id, title: '旧无签名图锚' }, '旧无签名图锚'));
  const r = evaluate(search('xiaohongshu'), [unsignedDuplicate, card], { url: 'https://www.xiaohongshu.com/search_result?keyword=geo' });
  assert.equal(r.items.length, 1); assert.equal(r.items[0].title, '真实卡片 标题');
  assert.equal(r.items[0].url, 'https://www.xiaohongshu.com' + href); assert.equal(r.items[0].author, '演示作者'); assert.equal(r.items[0].publishedAt, '昨天');
});

test('Google regional opaque goto and first-party content survive while root/account/search navigation is excluded', () => {
  const card = (href, title) => el('div', { class: 'MjjYud' }, el('a', { href }, el('h3', {}, title)));
  const wrapper = 'https://www.google.com.hk/goto?url=fixture-opaque-value';
  const cloud = 'https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide?hl=zh-cn';
  const developer = 'https://codelabs.developers.google.com/draw-a-website-gemini?hl=zh-cn';
  const baijiahao = 'https://baijiahao.baidu.com/s?id=123456789';
  const r = evaluate(search('google'), [card(wrapper, '不透明跳转结果'), card(cloud, 'Google Cloud 文档'), card(developer, '开发者教程'), card(baijiahao, '百家号正文'), card('https://www.google.com.hk/', '搜索首页'), card('https://www.google.com.hk/search?q=other', '更多搜索'), card('https://accounts.google.com/', 'Google 账号'), card('https://consent.google.com/m', '同意选项')], { url: 'https://www.google.com.hk/search?q=geo' });
  assert.deepEqual(r.items.map(i => i.url), [wrapper, cloud, developer, baijiahao]);
});

test('Google url unwraps only explicit HTTPS targets and preserves an opaque wrapper without fabricating a relative destination', () => {
  const card = (href, title) => el('div', { class: 'MjjYud' }, el('a', { href }, el('h3', {}, title)));
  const target = 'https://developers.google.com/search/docs?hl=zh-cn';
  const opaque = 'https://www.google.com.hk/url?url=fixture-opaque-value';
  const r = evaluate(search('google'), [card('https://www.google.com/url?q=' + encodeURIComponent(target), '明确目标'), card(opaque, '不透明目标'), card('https://www.google.com/url', '无目标'), card('https://www.google.com.hk/goto?url=javascript%3Aalert(1)', '无效协议')], { url: 'https://www.google.com.hk/search?q=geo' });
  assert.deepEqual(r.items.map(i => i.url), [target, opaque]);
  assert.ok(!r.items.some(i => i.url === 'https://www.google.com.hk/fixture-opaque-value'));
});

test('web result evidence excludes bare accessibility/footer links without blocking support content with a real heading', () => {
  const help = 'https://support.google.com/websearch/answer/181196';
  const result = 'https://support.google.com/websearch/answer/2466433';
  const r = evaluate(search('google'), [el('div', { class: 'MjjYud' }, el('a', { href: help }, '无障碍功能帮助')), el('a', { href: 'https://example.com/menu' }, '普通链接'), el('div', { class: 'MjjYud' }, el('a', { href: result }, el('h3', {}, '有标题的 Google 帮助结果')))], { url: 'https://www.google.com.hk/search?q=geo' });
  assert.deepEqual(r.items.map(i => i.url), [result]);
  const bing = evaluate(search('bing'), [el('li', { class: 'b_algo' }, el('a', { href: 'https://example.com/bing' }, '有效卡片')), el('a', { href: 'https://example.com/menu' }, '菜单')]);
  assert.deepEqual(bing.items.map(i => i.url), ['https://example.com/bing']);
  const baidu = evaluate(search('baidu'), [el('div', { class: 'result c-container' }, el('h3', {}, el('a', { href: 'https://www.baidu.com/link?url=fixture-opaque' }, '百度结果')))], { url: 'https://www.baidu.com/s?wd=geo' });
  assert.equal(baidu.items.length, 1);
});

test('cross-engine contentType follows the actual result URL, with article/post exceptions and unknown wrappers retained', () => {
  const cases = [
    ['https://www.youtube.com/watch?v=abc123_xyz', 'video'],
    ['https://www.youtube.com/shorts/abc123_xyz', 'video'],
    ['https://www.bilibili.com/video/BV123abc456', 'video'],
    ['https://www.bilibili.com/read/cv123456', 'article'],
    ['https://www.bilibili.com/opus/12345678', 'post'],
    ['https://www.douyin.com/video/12345678', 'video'],
    ['https://www.douyin.com/note/12345678', 'post'],
    ['https://www.google.com.hk/goto?url=fixture-opaque', 'article'],
    ['https://example.com/video/not-a-known-platform', 'article']
  ];
  const cards = cases.map(([href]) => el('div', { class: 'MjjYud' }, el('a', { href }, el('h3', {}, href))));
  const r = evaluate(search('google'), cards, { url: 'https://www.google.com.hk/search?q=video' });
  assert.deepEqual(r.items.map(i => [i.url, i.contentType]), cases);
});

test('engine-origin YouTube detail uses its visible description and video metadata, not a larger generic main', () => {
  const description = '视频页面实际可见的简短说明，未观看或转录视频。';
  const r = evaluate(detail('google'), [el('main', {}, el('p', {}, '其他区域文字不作为视频说明。'.repeat(20)), el('ytd-watch-metadata', {}, el('h1', {}, '实际视频标题'), el('div', { id: 'description-inline-expander' }, description)))], { url: 'https://www.youtube.com/watch?v=abc123_xyz', title: 'YouTube' });
  assert.equal(r.contentType, 'video'); assert.equal(r.text, description); assert.equal(r.title, '实际视频标题');
});

test('engine-origin Bili detail selects native description while read/opus and unknown wrappers are never mislabeled video', () => {
  const description = 'B站视频页面的实际说明。';
  const r = evaluate(detail('bing'), [el('main', {}, el('p', {}, '推荐列表不可代替说明。'.repeat(20)), el('h1', { class: 'video-title' }, '视频题目'), el('div', { class: 'video-desc-container' }, description))], { url: 'https://www.bilibili.com/video/BV123abc456' });
  assert.equal(r.contentType, 'video'); assert.equal(r.text, description); assert.equal(r.title, '视频题目');
  for (const [url, expected] of [['https://www.bilibili.com/read/cv123456', 'article'], ['https://www.bilibili.com/opus/12345678', 'post'], ['https://www.douyin.com/note/12345678', 'post'], ['https://www.google.com.hk/goto?url=fixture-opaque', 'article']]) {
    const page = evaluate(detail('youtube'), [el('article', {}, '实际页面文字。'.repeat(20))], { url });
    assert.equal(page.contentType, expected);
  }
});

test('observed Sina K article container is reusable and excludes navigation, sidebars, recommendations and ad blocks', () => {
  const body = '离线夹具的文章事实与说明。'.repeat(12);
  const r = evaluate(detail('google'), [el('div', { id: 'article_content', class: 'article-content' }, el('h1', {}, '夹具文章标题'), el('div', { id: 'article', class: 'article' }, el('header', {}, '导航不可进入正文'), el('p', {}, body), el('aside', {}, '侧栏不可进入正文'), el('div', { class: 'recommend-list' }, '推荐不可进入正文'), el('div', { 'data-ad-slot': 'fixture-only' }, '广告不可进入正文'), el('footer', {}, '页尾不可进入正文')), el('div', { class: 'article-content-right' }, '更长的外框信息不属于文章。'.repeat(30)))], { url: 'https://k.sina.com.cn/article_fixture.html', head: [el('meta', { property: 'article:published_time', content: '2026-01-02T03:04:05+08:00' })] });
  assert.equal(r.text, body); assert.equal(r.publishedAt, '2026-01-02T03:04:05+08:00');
  assert.deepEqual(r.extraction, { contentSelector: '#article.article', primaryContent: true, textLength: body.length });
});

test('Sina finance artibody retains a short actual article and reads a date outside the body without using a sidebar date', () => {
  const body = '这是刻意少于八十字的夹具正文。';
  const r = evaluate(detail('bing'), [el('aside', {}, el('span', { class: 'date' }, '错误侧栏日期')), el('div', { class: 'article-header' }, el('h1', {}, '短文章'), el('span', { class: 'date' }, '2026-01-02 03:04')), el('div', { id: 'artibody' }, el('p', {}, body)), el('main', {}, '大块模板或周边文字不代替短正文。'.repeat(20))], { url: 'https://finance.sina.com.cn/tech/fixture.shtml' });
  assert.equal(r.text, body); assert.equal(r.title, '短文章'); assert.equal(r.publishedAt, '2026-01-02 03:04');
  assert.deepEqual(r.extraction, { contentSelector: '#artibody', primaryContent: true, textLength: body.length });
});

test('Sina adapter is host-scoped and missing primary content does not promote body into an article', () => {
  const nodes = [el('div', { id: 'article', class: 'article' }, '不在已适配主机上的同名容器。'.repeat(10))];
  const r = evaluate(detail('google'), nodes, { url: 'https://finance.sina.com.cn.evil.example/fixture' });
  assert.equal(r.text, ''); assert.deepEqual(r.extraction, { contentSelector: null, primaryContent: false, textLength: 0 });
});

test('well-known captcha path on any domain and a visible standalone challenge are blocking, not empty or delayed article content', () => {
  const url = 'https://news.example/.well-known/captcha?request=fixture-only';
  const r = evaluate(detail('google'), [el('article', {}, '背景文字不得在验证页面交付。'.repeat(10))], { url, title: '站点' });
  assert.equal(r.state.captcha, true); assert.equal(r.state.empty, false); assert.equal(r.state.loading, false); assert.equal(r.text, ''); assert.equal(r.extraction.primaryContent, false); assert.equal(r.extraction.textLength, 0);
  const listing = evaluate(search('bing'), [bingCard('https://example.com/result')], { url });
  assert.equal(listing.state.captcha, true); assert.deepEqual(listing.items, []);
  const visible = evaluate(detail('google'), [el('main', {}, 'Please complete the security check to continue.')], { url: 'https://news.example/check', title: '站点' });
  assert.equal(visible.state.captcha, true); assert.equal(visible.text, '');
  const hidden = evaluate(detail('google'), [el('article', {}, '可见文章内容。'.repeat(20)), el('div', { style: 'display:none' }, 'Please complete the security check to continue.')], { url: 'https://news.example/article' });
  assert.equal(hidden.state.captcha, false); assert.equal(hidden.extraction.primaryContent, true);
});

test('native short video description retains its primary selector and does not become a longer generic article', () => {
  const description = '可见视频说明，未观看视频。';
  const r = evaluate(detail('google'), [el('main', {}, '周边模板文字。'.repeat(80), el('div', { id: 'description-inline-expander' }, description))], { url: 'https://www.youtube.com/watch?v=fixture123' });
  assert.equal(r.contentType, 'video'); assert.equal(r.text, description);
  assert.deepEqual(r.extraction, { contentSelector: '#description-inline-expander', primaryContent: true, textLength: description.length });
});


test('observed Weibo permalink timestamps use visible post text as the result title without taking author navigation', () => {
  const r = evaluate(search('weibo'), [el('div', { class: 'card-wrap', 'data-mid': '123' },
    el('a', { href: 'https://weibo.com/12345678', class: 'name' }, '演示作者'),
    el('p', { class: 'txt' }, '用 Manim 制作 AI 动画的实际步骤与经验'),
    el('p', { class: 'from' }, el('a', { href: 'https://weibo.com/12345678/Abcdef123' }, '今天 08:10')))], { url: 'https://s.weibo.com/weibo?q=Manim' });
  assert.equal(r.items.length, 1); assert.equal(r.items[0].title, '用 Manim 制作 AI 动画的实际步骤与经验');
  assert.equal(r.items[0].publishedAt, '今天 08:10'); assert.equal(r.items[0].author, '演示作者');
});


test('observed Baidu realtime aggregate heading is navigation while inner titled news and Baijiahao content remain candidates', () => {
  const wrapper = 'https://www.baidu.com/link?url=fixture-aggregate';
  const news = 'https://www.baidu.com/link?url=fixture-real-news';
  const r = evaluate(search('baidu'), [el('div', { class: 'result-op c-container', tpl: 'rel_base_realtime' },
    el('h3', { class: 'cosc-title' }, el('a', { href: wrapper }, '演示查询的最新相关信息')),
    el('div', { class: 'weak-content_fixture' }, el('a', { href: news }, el('h3', {}, '实际新闻标题'), el('span', {}, '新闻摘要'))),
    el('a', { href: 'https://www.baidu.com/link?url=fixture-more' }, '查看更多')),
    el('div', { class: 'result c-container' }, el('h3', {}, el('a', { href: 'https://baijiahao.baidu.com/s?id=123456789' }, '百家号原文')))], { url: 'https://www.baidu.com/s?wd=demo' });
  assert.deepEqual(r.items.map(x => x.title), ['实际新闻标题', '百家号原文']);
  assert.deepEqual(r.items.map(x => x.url), [news, 'https://baijiahao.baidu.com/s?id=123456789']);
});

test('observed Zhihu no-content wording is empty but X onboarding is a login boundary rather than an unexpected search page', () => {
  const empty = evaluate(search('zhihu'), [el('main', {}, '未搜索到相关内容，提问快速获得回答')], { url: 'https://www.zhihu.com/search?type=content&q=Manim' });
  assert.equal(empty.state.empty, true); assert.equal(empty.state.loginRequired, false);
  const x = evaluate(search('x'), [el('main', {}, '看看正在发生什么 请从下方选择一项 使用手机继续 使用 Google 继续 电子邮箱或用户名 继续', el('input', { name: 'username_or_email' }))], { url: 'https://x.com/i/jf/onboarding/web' });
  assert.equal(x.state.loginRequired, true); assert.equal(x.state.empty, false); assert.deepEqual(x.items, []);
});


test('actual Zhihu signFlowModal takes priority over background empty wording; hidden login UI does not', () => {
  const modal = style => el('div', { class: 'Modal signFlowModal', ...(style ? {style} : {}) }, el('form', { class: 'SignFlow Login-content' }, '验证码登录密码登录 登录/注册', el('input', { type: 'tel', name: 'username' })));
  const options = { url: 'https://www.zhihu.com/search?type=content&q=Manim' };
  const blocked = evaluate(search('zhihu'), [el('main', {}, '未搜索到相关内容，提问快速获得回答'), modal()], options);
  assert.equal(blocked.state.loginRequired, true); assert.equal(blocked.state.empty, false); assert.deepEqual(blocked.items, []);
  const hidden = evaluate(search('zhihu'), [el('main', {}, '未搜索到相关内容，提问快速获得回答'), modal('display:none')], options);
  assert.equal(hidden.state.loginRequired, false); assert.equal(hidden.state.empty, true);
});


test('observed Toutiao double public jump unwraps native aID articles without treating foreign results, user pages or trending searches as native content', () => {
  const wrap = target => 'https://sou.toutiao.com/search/jump?url=' + encodeURIComponent(target) + '&aid=24';
  const article = 'https://www.toutiao.com/a1234567890123456789/';
  const card = (href, title) => el('div', { class: 'result-content' }, el('div', { class: 'cs-header' }, el('a', { href }, title)));
  const r = evaluate(search('toutiao'), [card(wrap(wrap(article)).replace('https://sou.', 'https://so.'), 'Manim 实际文章'),
    card(wrap('https://www.bilibili.com/video/BV123abc456'), '外站视频'), card(wrap('https://www.toutiao.com/c/user/123/'), '作者页'),
    card(wrap('https://so.toutiao.com/search/?keyword=hot'), '头条热榜'), card(wrap('fixture-opaque'), '不透明参数'), card(wrap('javascript:alert(1)'), '不安全目标')], { url: 'https://so.toutiao.com/search/?keyword=Manim' });
  assert.deepEqual(r.items.map(x => [x.title,x.url,x.contentType]), [['Manim 实际文章', article, 'article']]);
});


test('observed Toutiao trending article links are excluded while separate native video grid cells remain results', () => {
  const wrap = target => 'https://sou.toutiao.com/search/jump?url=' + encodeURIComponent(target);
  const r = evaluate(search('toutiao'), [el('div', { class: 'result-content' },
    el('div', { class: 'cs-header' }, '头条热榜'), el('a', { href: wrap('https://www.toutiao.com/a1234567890123456789/') }, '不相关热榜')),
    el('div', { class: 'result-content' },
      el('div', { class: 'cs-grid-cell' }, el('a', { href: wrap('https://www.toutiao.com/video/1234567890123456789/') }, 'Manim 视频一')),
      el('div', { class: 'cs-grid-cell' }, el('a', { href: wrap('https://www.toutiao.com/video/2234567890123456789/') }, 'Manim 视频二')))], { url: 'https://so.toutiao.com/search/?dvpf=pc&keyword=Manim' });
  assert.deepEqual(r.items.map(x => x.title), ['Manim 视频一', 'Manim 视频二']);
});


test('visible Douyin cards without href yield titles-only evidence at the actual search URL, never invented video or modal links', () => {
  const url = 'https://www.douyin.com/search/Manim?type=general';
  const card = (id, title, hidden = false) => el('div', { id: 'waterfall_item_' + id }, el('div', { class: 'search-result-card', ...(hidden ? {style:'display:none'} : {}) },
    el('div', { class: 'BjLsdJMi' }, title), el('div', {}, '@演示作者 · 7月14日'), el('span', {}, '542'), el('span', {}, '01:40')));
  const r = evaluate(search('douyin', {limit:2}), [el('nav', {}, '不可当正文'), card('1234567890123456789', 'Manim 可视化教程'), card('1234567890123456789', '同卡重复'), card('2234567890123456789', '第二条实际标题'), card('3234567890123456789', '隐藏标题', true)], {url});
  assert.equal(r.items.length, 2); assert.equal(r.diagnostics.cardCount, 3);
  assert.deepEqual(r.items.map(x => x.domContentId), ['1234567890123456789','2234567890123456789']);
  for(const item of r.items){assert.equal(item.url,url);assert.equal(item.linkStatus,'search_page_only');assert.equal(item.contentType,'search-card');assert.ok(!/modal_id|\/video\//.test(item.url));}
  assert.equal(r.items[0].title,'Manim 可视化教程');assert.equal(r.items[0].author,'演示作者');assert.equal(r.items[0].publishedAt,'7月14日');assert.equal(r.items[0].metrics.raw,'542');
  assert.equal(r.state.empty,false);
});

test('Douyin titles-only fallback never supplants a real content href, promotes an invalid DOM id, or bypasses a visible challenge', () => {
  const textCard = id => el('div', {id}, el('div', {class:'search-result-card'}, el('div', {class:'BjLsdJMi'}, '只有搜索卡片文字')));
  const options={url:'https://www.douyin.com/search/Manim?type=general'};
  const real=evaluate(search('douyin'),[textCard('waterfall_item_1234567890123456789'),el('div',{'data-e2e':'search-card'},el('a',{href:'/video/2234567890123456789'},el('span',{'data-e2e':'video-desc'},'真实直链标题')))],options);
  assert.equal(real.items.length,1);assert.equal(real.items[0].url,'https://www.douyin.com/video/2234567890123456789');assert.equal(real.items[0].linkStatus,undefined);
  const invalid=evaluate(search('douyin'),[textCard('waterfall_item_unverified')],options);assert.deepEqual(invalid.items,[]);
  const blocked=evaluate(search('douyin'),[textCard('waterfall_item_1234567890123456789'),el('div',{role:'dialog'},'请完成安全验证')],options);assert.equal(blocked.state.captcha,true);assert.deepEqual(blocked.items,[]);
});
