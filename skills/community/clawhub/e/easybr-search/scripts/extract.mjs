import { getPlatform, listPlatforms } from './platforms.mjs';

// This function is stringified into the page; all helpers must remain inside it.
function extractDOM(profile, mode, limit, maxText, nativeProfiles = []) {
  const clean = value => String(value ?? '').replace(/<\/?(?:em|mark|b|strong)(?:\s[^>]*)?>/gi, '').replace(/\s+/g, ' ').trim();
  const query = (selector, root = document) => { try { return Array.from(root.querySelectorAll(selector)); } catch { return []; } };
  const closest = (node, selector) => { try { return node?.closest?.(selector) || null; } catch { return null; } };
  const visible = node => {
    if (!node || node.hidden || closest(node, '[hidden], [aria-hidden="true"]')) return false;
    if (typeof node.getClientRects === 'function' && node.getClientRects().length === 0) return false;
    if (typeof getComputedStyle === 'function') { const s = getComputedStyle(node); if (s.display === 'none' || s.visibility === 'hidden') return false; }
    return true;
  };
  const value = node => clean(node?.innerText ?? node?.textContent ?? '');
  const first = (selectors, root = document) => {
    for (const selector of selectors || []) { const node = query(selector, root).find(visible); if (node) return node; }
    return null;
  };
  const textOf = (selectors, root) => value(first(selectors, root));
  const url = String(location.href);
  const hostMatches = (hostname, hosts) => hosts.some(h => hostname === h || hostname.endsWith('.' + h));
  const googleDomains = ['google.com', 'google.com.hk', 'google.co.uk', 'google.de', 'google.co.jp'];
  const googleSearchHost = hostname => googleDomains.some(h => hostname === h || hostname === 'www.' + h);
  const bingSearchHost = hostname => ['bing.com', 'www.bing.com', 'cn.bing.com'].includes(hostname);
  const baiduSearchHost = hostname => ['baidu.com', 'www.baidu.com'].includes(hostname);
  const accountHost = hostname => googleDomains.some(h => ['accounts.', 'myaccount.', 'consent.'].some(prefix => hostname === prefix + h)) || hostname === 'passport.baidu.com';
  const googleWrapper = u => googleSearchHost(u.hostname) && ['/goto', '/url'].includes(u.pathname) && !!(u.searchParams.get('url') || u.searchParams.get('q'));
  const parse = href => { if (typeof href !== 'string' || !href.trim()) return null; try { const u = new URL(href, url); return /^https?:$/.test(u.protocol) && !u.username && !u.password ? u : null; } catch { return null; } };
  if (mode === 'detail') {
    const hostname = parse(url)?.hostname || '';
    const native = nativeProfiles.find(p => hostMatches(hostname, p.hosts));
    if (native) profile = native;
  }
  function unwrap(href) {
    let u = parse(href); if (!u) return null;
    if (bingSearchHost(u.hostname) && u.pathname === '/ck/a') {
      const encoded = u.searchParams.get('u');
      if (!encoded) return null;
      let target = encoded;
      if (target.startsWith('a1')) {
        try {
          let b64 = target.slice(2).replaceAll('-', '+').replaceAll('_', '/'); b64 += '='.repeat((4 - b64.length % 4) % 4);
          const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0)); target = new TextDecoder().decode(bytes);
        } catch { return null; }
      }
      u = parse(target); if (!u) return null;
    } else if (googleSearchHost(u.hostname) && ['/url', '/goto'].includes(u.pathname)) {
      const target = u.searchParams.get('q') || u.searchParams.get('url');
      if (!target || /^(?:javascript|data|file|vbscript):/i.test(target.trim())) return null;
      // Only an explicit HTTPS destination is a decoded /url link. Opaque values
      // stay on their actual Google wrapper for normal browser navigation.
      if (u.pathname === '/url' && /^https:\/\//i.test(target)) {
        const direct = parse(target); if (!direct) return null; u = direct;
      }
    } else if (['so.toutiao.com', 'sou.toutiao.com'].includes(u.hostname) && u.pathname === '/search/jump') {
      // Observed public UI wraps direct destinations twice; decode only explicit HTTP(S) URLs.
      for (let i = 0; i < 3 && ['so.toutiao.com', 'sou.toutiao.com'].includes(u.hostname) && u.pathname === '/search/jump'; i++) {
        const target = u.searchParams.get('url');
        if (!target || !/^https?:\/\//i.test(target)) return null;
        u = parse(target); if (!u) return null;
      }
    } else if (u.hostname === 'link.zhihu.com') {
      u = parse(u.searchParams.get('target')); if (!u) return null;
    }
    u.hash = ''; return u;
  }
  const navigation = node => !!closest(node, 'header, nav, footer, aside, [role="navigation"], [role="banner"], [role="complementary"]');
  const ad = node => !!closest(node, '[data-text-ad], [data-ad-slot], [data-ad-client], [aria-label="Ads"], .b_ad, .ads-ad, .search-ad, .ad-banner, .commercial-unit-desktop-top');
  function contentURL(href) {
    const u = unwrap(href); if (!u) return null;
    if (profile.siteDomain) return hostMatches(u.hostname, [profile.siteDomain]) ? u.href : null;
    if (profile.kind === 'web') {
      // Baidu's opaque link route needs a normal browser navigation; do not invent its target.
      if (baiduSearchHost(u.hostname) && u.pathname === '/link' && u.searchParams.get('url')) return u.href;
      if (googleWrapper(u)) return u.href;
      // Search frontends are not their entire parent domains: Google Cloud,
      // developer docs and Baijiahao are content hosts, not search navigation.
      if (googleSearchHost(u.hostname) || bingSearchHost(u.hostname) || baiduSearchHost(u.hostname) || accountHost(u.hostname)) return null;
      if (/\/(?:login|signin|signup|settings)(?:\/|$)/i.test(u.pathname)) return null;
      return u.href;
    }
    if (!hostMatches(u.hostname, profile.hosts)) return null;
    if (!profile.contentPatterns.some(source => new RegExp(source).test(u.href))) return null;
    if (profile.id === 'github' && /\/(?:stargazers|watchers|forks|network|followers|following)(?:\/|$)/.test(u.pathname)) return null;
    return u.href;
  }
  function identity(href) {
    const u = parse(href); if (!u) return href;
    if (profile.id === 'xiaohongshu') { const m = u.pathname.match(/\/(?:explore|discovery\/item|search_result)\/([a-zA-Z0-9]+)/); if (m) return 'xiaohongshu:' + m[1]; }
    if (profile.id === 'youtube') { const id = u.searchParams.get('v') || u.pathname.match(/\/shorts\/([^/]+)/)?.[1] || (u.hostname === 'youtu.be' ? u.pathname.slice(1) : ''); if (id) return 'youtube:' + id; }
    for (const key of [...u.searchParams.keys()]) if (/^(?:utm_|spm|xsec_token$|xsec_source$|vd_source$|is_from_webapp$)/i.test(key)) u.searchParams.delete(key);
    return u.href;
  }
  function typeOf(href) {
    const u = parse(href); if (!u) return 'article';
    const path = u.pathname; const on = hosts => hostMatches(u.hostname, hosts);
    if (on(['youtube.com']) && ((path === '/watch' && /^[a-zA-Z0-9_-]+$/.test(u.searchParams.get('v') || '')) || /^\/(?:shorts|embed|live)\/[a-zA-Z0-9_-]+(?:\/|$)/.test(path))) return 'video';
    if (u.hostname === 'youtu.be' && /^\/[a-zA-Z0-9_-]+\/?$/.test(path)) return 'video';
    if (on(['bilibili.com'])) {
      if (/^\/video\/(?:BV[a-zA-Z0-9]+|av[0-9]+)(?:\/|$)/.test(path)) return 'video';
      if (/^\/read\/cv[0-9]+(?:\/|$)/.test(path)) return 'article';
      if (/^\/opus\/[0-9]+(?:\/|$)/.test(path)) return 'post';
    }
    if (on(['douyin.com'])) {
      if (/^\/video\/[0-9]+(?:\/|$)/.test(path)) return 'video';
      if (/^\/note\/[0-9]+(?:\/|$)/.test(path)) return 'post';
    }
    if (on(['toutiao.com'])) {
      if (/^\/video\/[0-9]+(?:\/|$)/.test(path)) return 'video';
      if (/^\/w\/a[0-9]+(?:\/|$)/.test(path)) return 'post';
    }
    if (on(['xiaohongshu.com']) && /^\/(?:explore|search_result|discovery\/item)\/[a-zA-Z0-9]+(?:\/|$)/.test(path)) return 'post';
    if (on(['x.com', 'twitter.com']) && /^\/[^/]+\/status\/[0-9]+(?:\/|$)/.test(path)) return 'post';
    if (on(['reddit.com']) && /^\/(?:r\/[^/]+\/)?comments\/[a-zA-Z0-9]+(?:\/|$)/.test(path)) return 'post';
    if (on(['weibo.com', 'weibo.cn']) && /^\/(?:[0-9]{4,}\/[a-zA-Z0-9]{5,}|status\/[a-zA-Z0-9]+|detail\/[0-9]+)(?:\/|$)/.test(path)) return 'post';
    if (u.hostname === 'github.com' && /^\/[^/]+\/[^/]+(?:\/|$)/.test(path)) {
      if (/\/issues\/[0-9]+/.test(path)) return 'issue';
      if (/\/pull\/[0-9]+/.test(path)) return 'pull-request';
      if (/\/blob\//.test(path)) return 'code';
      return 'repository';
    }
    // A search engine wrapper or an unknown host does not establish video content.
    return 'article';
  }
  const links = query('a[href]');
  const cardSelector = (profile.selectors.cards || []).join(', ');
  const cards = cardSelector ? query(cardSelector).filter(visible) : [];
  const candidates = [];
  for (const anchor of links.slice(0, 5000)) {
    if (!visible(anchor) || navigation(anchor) || ad(anchor)) continue;
    const href = contentURL(anchor.getAttribute('href')); if (!href) continue;
    const matchedCard = cardSelector && closest(anchor, cardSelector);
    let card = matchedCard || closest(anchor, 'article') || anchor.parentElement || anchor;
    if (ad(card) || !visible(card)) continue;
    const ownHeading = first(['h3', 'h2', 'h4'], anchor) || closest(anchor, 'h3, h2, h4');
    // Baidu realtime modules wrap a search/aggregation heading and several real news links.
    // The module title is navigation; use each inner article anchor as its own card.
    if (profile.id === 'baidu' && closest(anchor, '[tpl="rel_base_realtime"]')) {
      if (!ownHeading || /的最新相关信息$/.test(value(ownHeading))) continue;
      card = anchor;
    }
    // Toutiao also renders a trending list in .result-content. Accept its actual result
    // header or video grid, not every native article link in that sidebar.
    if (profile.id === 'toutiao') {
      const grid = closest(anchor, '.cs-grid-cell');
      if (!ownHeading && !closest(anchor, '.cs-header') && !grid) continue;
      if (grid) card = grid;
    }
    // .MjjYud also wraps Google footers; it alone is not a result card.
    const knownWebCard = profile.id === 'bing' ? closest(anchor, 'li.b_algo') : profile.id === 'baidu' ? matchedCard : closest(anchor, '#search .g');
    if (profile.kind === 'web' && !ownHeading && !knownWebCard) continue;
    const own = clean(anchor.getAttribute('title')) || value(ownHeading) || value(anchor);
    // Microblog permalinks are often the timestamp, while the visible .txt is the post itself.
    const postTitle = profile.id === 'weibo' ? textOf(profile.selectors.title, card).slice(0, 200) : '';
    const title = postTitle || own || textOf(profile.selectors.title, card) || clean(anchor.getAttribute('aria-label'));
    if (!title) continue;
    const score = (profile.id === 'xiaohongshu' && own && parse(href)?.searchParams.has('xsec_token') ? 30 : 0) + (ownHeading ? 20 : 0) + (anchor.getAttribute('title') ? 10 : 0) + (profile.selectors.title.some(sel => { try { return anchor.matches(sel) || !!closest(anchor, sel); } catch { return false; } }) ? 15 : 0) + Math.min(title.length, 200) / 200;
    candidates.push({ anchor, card, href, title, score });
  }
  const byCard = new Map();
  for (const c of candidates) { const old = byCard.get(c.card); if (!old || c.score > old.score) byCard.set(c.card, c); }
  const byContent = new Map();
  for (const c of byCard.values()) { const key = identity(c.href); const old = byContent.get(key); if (!old || c.score > old.score) byContent.set(key, c); }
  const selected = [...byContent.values()];
  const body = value(document.body).slice(0, 100000);
  function pageState(resultCount) {
    const dialogs = query('[role="dialog"], [aria-modal="true"], .login-modal, .login-mask, .login-dialog, .login-container, .passport-login-container').filter(visible);
    const loginWords = /登录后(?:查看|使用|搜索)|请先登录|登录即可|扫码登录|登录小红书|log\s*in to (?:continue|see|search)|sign\s*in to (?:continue|see|search)/i;
    const captchaWords = /安全验证|完成验证|拖动滑块|点击验证|验证您是人类|验证你是真人|人机验证|verify (?:that )?you(?:'re| are) (?:a )?human|unusual traffic|captcha|security verification/i;
    const captchaNodes = query('[id*="captcha"], [class*="captcha"], [id*="verify"], [class*="verify-wrap"], iframe[title*="challenge"], #b_captcha').filter(visible);
    const engineChallenge = hostMatches(parse(url)?.hostname || '', ['google.com', 'google.com.hk', 'bing.com']) && /\/(?:sorry|turing\/captcha)(?:\/|$)/.test(parse(url)?.pathname || '');
    const wellKnownChallenge = /^\/\.well-known\/captcha(?:\/|$)/.test(parse(url)?.pathname || '');
    const visibleChallenge = /^(?:请完成(?:安全|人机)?验证(?:后|以)?继续(?:访问)?|please complete (?:the )?(?:security|human) (?:check|verification) to continue)[.。!！\s]*$/i.test(body);
    const captcha = engineChallenge || wellKnownChallenge || visibleChallenge || /Our systems have detected unusual traffic|请完成下方验证后继续访问/i.test(body) || dialogs.some(n => captchaWords.test(value(n))) || captchaNodes.some(n => captchaWords.test(value(n) || n.getAttribute('title') || '')) || (!resultCount && captchaWords.test(body) && /验证|captcha|traffic|human/i.test(String(document.title)));
    const xOnboarding = hostMatches(parse(url)?.hostname || '', ['x.com', 'twitter.com']) && /^\/i\/(?:jf\/onboarding\/web|flow\/login)(?:\/|$)/.test(parse(url)?.pathname || '');
    const zhihuLogin = hostMatches(parse(url)?.hostname || '', ['zhihu.com']) && query('.signFlowModal').filter(visible).some(n => query('form.SignFlow', n).some(visible) && /验证码登录|密码登录|登录\/注册/.test(value(n)));
    const loginRequired = xOnboarding || zhihuLogin || dialogs.some(n => loginWords.test(value(n))) || /\/(?:login|signin|passport)(?:\/|$)/i.test(parse(url)?.pathname || '') || (/^(?:passport|login|accounts)\./i.test(parse(url)?.hostname || '') && /登录|sign in|log in/i.test(body)) || (!resultCount && loginWords.test(body));
    const blocked = captcha || loginRequired;
    const empty = !blocked && !resultCount && /暂无(?:相关)?(?:内容|结果)|没有找到|未(?:搜索)?到.{0,18}(?:结果|内容)|未找到.{0,18}(?:结果|内容)|无相关结果|no (?:matching )?results|couldn.t find any results/i.test(body);
    const loading = !blocked && !empty && !resultCount && (document.readyState !== 'complete' || query('[aria-busy="true"], [role="progressbar"], .loading-spinner, .skeleton').some(visible) || /^(?:加载中[.。…\s]*|loading[.\s]*)$/i.test(body));
    return { loginRequired, captcha, empty, loading };
  }
  if (mode === 'search') {
    const titleCards = [];
    // Some Douyin search cards expose visible text and a public DOM content ID,
    // but no verified content href. A DOM ID is not proof of a video/modal route.
    const current = parse(url);
    if (profile.id === 'douyin' && !selected.length && current && hostMatches(current.hostname, profile.hosts) && /^\/search(?:\/|$)/.test(current.pathname)) {
      const seen = new Set();
      for (const card of query('.search-result-card').filter(visible)) {
        const id = closest(card, '[id^="waterfall_item_"]')?.id?.match(/^waterfall_item_([0-9]{10,24})$/)?.[1];
        const title = textOf(profile.selectors.title, card);
        if (!id || !title || seen.has(id) || ad(card) || navigation(card)) continue;
        seen.add(id);
        const leaves = query('span, div', card).filter(n => visible(n) && !Array.from(n.childNodes || []).some(child => child.nodeType === 1)).map(value).filter(Boolean);
        const byline = leaves.find(s => /^@/.test(s) && s.length <= 120 && s !== title) || '';
        const author = textOf(profile.selectors.author, card) || byline.split(/\s*[·•]\s*/)[0].replace(/^@/, '');
        const date = first(profile.selectors.publishedAt, card);
        const bylineDate = byline.split(/\s*[·•]\s*/).slice(1).join(' · ');
        const publishedAt = date?.getAttribute('datetime') || value(date) || (/^(?:\d{4}年)?\d{1,2}月\d{1,2}日|^(?:今天|昨天|前天|\d+天前)/.test(bylineDate) ? bylineDate : '');
        const raw = textOf(profile.selectors.metrics, card) || leaves.filter(s => /^[0-9]+(?:\.[0-9]+)?(?:万|亿|[kKmM])?$/.test(s)).slice(0, 4).join(' ');
        titleCards.push({ title, url, linkStatus: 'search_page_only', domContentId: id, snippet: textOf(profile.selectors.snippet, card), author: author || null, publishedAt: publishedAt || null, metrics: { raw }, contentType: 'search-card' });
      }
    }
    const state = pageState(selected.length || titleCards.length); const items = []; let remaining = maxText;
    const take = (s, cap) => { const text = clean(s).slice(0, Math.min(cap, remaining)); remaining -= text.length; return text; };
    if (!state.loginRequired && !state.captcha) for (const c of selected.slice(0, limit)) {
      if (!remaining) break;
      const title = take(c.title, 500); if (!title) break;
      const snippet = take(textOf(profile.selectors.snippet, c.card), 1500);
      const author = take(textOf(profile.selectors.author, c.card), 200);
      const time = first(profile.selectors.publishedAt, c.card);
      const publishedAt = take(time?.getAttribute('datetime') || value(time), 200);
      const raw = take(textOf(profile.selectors.metrics, c.card), 500);
      items.push({ title, url: c.href, snippet, author: author || null, publishedAt: publishedAt || null, metrics: { raw }, contentType: typeOf(c.href) });
    }
    if (!state.loginRequired && !state.captcha && !selected.length) for (const card of titleCards.slice(0, limit)) {
      if (!remaining) break;
      const title = take(card.title, 500); if (!title) break;
      items.push({ ...card, title, snippet: take(card.snippet, 1500), author: take(card.author, 200) || null, publishedAt: take(card.publishedAt, 200) || null, metrics: { raw: take(card.metrics.raw, 500) } });
    }
    return { url, title: clean(document.title), readyState: document.readyState, items, state, diagnostics: { cardCount: cards.length, linkCount: links.length } };
  }
  function readable(node) {
    const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'NAV', 'HEADER', 'FOOTER', 'ASIDE', 'FORM', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA', 'SVG', 'MATH']);
    let result = '';
    function walk(current) {
      if (!current || result.length >= maxText) return;
      if (current.nodeType === 3) { result += String(current.nodeValue ?? current.textContent ?? '').slice(0, maxText - result.length); return; }
      if (current.nodeType !== 1 || skip.has(current.tagName) || !visible(current) || ad(current)) return;
      if (/^(?:navigation|banner|complementary|dialog)$/.test(current.getAttribute('role') || '')) return;
      if (/(?:^|[\s_-])(?:sidebar|recommend(?:ation)?s?|related|breadcrumb|toolbar|share|advertisement|comments?)(?:[\s_-]|$)/i.test((current.className || '') + ' ' + (current.id || ''))) return;
      const block = /^(?:ARTICLE|MAIN|SECTION|DIV|P|PRE|LI|H[1-6]|BLOCKQUOTE|BR|TR)$/.test(current.tagName);
      if (block && result && !result.endsWith('\n')) result += '\n';
      for (const child of current.childNodes || []) walk(child);
      if (block && result && !result.endsWith('\n') && result.length < maxText) result += '\n';
    }
    walk(node); return result.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim().slice(0, maxText);
  }
  // Narrow article adapters observed on these hosts; never fall back to body.
  const articleSelectors = { 'k.sina.com.cn': ['#article.article'], 'finance.sina.com.cn': ['#artibody'] }[parse(url)?.hostname] || [];
  let main = null; let text = ''; let contentSelector = null;
  for (const selector of [...articleSelectors, ...profile.selectors.detail, 'article', '[role="main"]', 'main']) {
    for (const candidate of query(selector).filter(visible)) {
      if (navigation(candidate)) continue;
      const content = readable(candidate); if (content.length > text.length) { main = candidate; text = content; contentSelector = selector; }
    }
    if (text && !['article', '[role="main"]', 'main'].includes(selector)) break;
    if (text.length >= 80) break;
  }
  // A full body fallback could turn an unsupported page's navigation into an article.
  const state = pageState(text ? 1 : 0);
  if (state.loginRequired || state.captcha) text = '';
  const canonical = parse(query('link[rel="canonical"]')[0]?.getAttribute('href'));
  const meta = names => { for (const name of names) { const node = query(`meta[name="${name}"], meta[property="${name}"]`)[0]; const s = clean(node?.getAttribute('content')); if (s) return s; } return ''; };
  const heading = textOf(profile.selectors.detailTitle, main || document) || textOf(profile.selectors.detailTitle) || meta(['og:title']);
  const author = textOf(profile.selectors.author, main || document) || meta(['author', 'article:author']);
  const time = first(profile.selectors.publishedAt, main || document);
  let articleDate = null;
  if (articleSelectors.length) for (const selector of profile.selectors.publishedAt) {
    articleDate = query(selector).find(node => visible(node) && !closest(node, 'nav, aside, footer, [role="navigation"], [role="complementary"], .sidebar, .recommend-list'));
    if (articleDate) break;
  }
  const publishedAt = time?.getAttribute('datetime') || value(time) || meta(['article:published_time', 'datePublished']) || articleDate?.getAttribute('datetime') || value(articleDate);
  const extraction = { contentSelector, primaryContent: !!text, textLength: text.length };
  return { url, readyState: document.readyState, canonicalUrl: canonical?.href || url, title: heading || clean(document.title), text, author: author || null, publishedAt: publishedAt || null, contentType: typeOf(url), state, extraction };
}
function options(value, defaults) {
  const merged = { ...defaults, ...value };
  if (!Number.isInteger(merged.maxText) || merged.maxText < 1 || merged.maxText > 200000 || ('limit' in merged && (!Number.isInteger(merged.limit) || merged.limit < 0 || merged.limit > 100))) {
    const e = new TypeError('maxText must be 1..200000 and limit 0..100.'); e.code = 'invalid_extract_options'; throw e;
  }
  return merged;
}
function expression(id, mode, o) {
  const native = mode === 'detail' ? listPlatforms().filter(p => p.kind !== 'web') : [];
  return `(${extractDOM.toString()})(${JSON.stringify(getPlatform(id))},${JSON.stringify(mode)},${o.limit ?? 0},${o.maxText},${JSON.stringify(native)})`;
}
export function buildSearchExtractExpression(platformId, value = {}) { const o = options(value, { limit: 10, maxText: 12000 }); return expression(platformId, 'search', o); }
export function buildDetailExtractExpression(platformId, value = {}) { const o = options(value, { maxText: 16000 }); return expression(platformId, 'detail', o); }
