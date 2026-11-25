/** Public search routes and DOM hints; configuration is not a live-browser receipt. */
const shared = {
  title: ['h2', 'h3', 'h4', '[data-testid="post-title"]', '[data-e2e="video-desc"]'],
  snippet: ['.snippet', '.description', '.summary', '[data-testid="post-text"]'],
  author: ['[rel="author"]', '[itemprop="author"]', '.author', '.author-name'],
  publishedAt: ['time', '[itemprop="datePublished"]', '.publish-time', '.date'],
  metrics: ['.stats', '.metrics', '[data-e2e="video-like-count"]'],
  detail: ['article', '[role="main"]', 'main'],
  detailTitle: ['h1', '[itemprop="headline"]']
};
function profile(id, label, hosts, kind, searchUrl, contentPatterns, selectors = {}, contentType = 'article') {
  return { id, label, hosts, kind, searchUrl, contentPatterns, contentType,
    selectors: { ...shared, ...selectors }, verification: { status: 'template-only', browserValidated: false } };
}
const profiles = [
  profile('bilibili', '哔哩哔哩', ['bilibili.com', 'b23.tv'], 'social', 'https://search.bilibili.com/all?keyword={query}',
    ['^https?://(?:[a-z0-9-]+\\.)?bilibili\\.com/(?:video/(?:BV[a-zA-Z0-9]+|av[0-9]+)|read/cv[0-9]+|opus/[0-9]+)(?:[/?#]|$)'],
    { cards: ['.bili-video-card', '.video-item', '.video-list-item'], title: ['.bili-video-card__info--tit', '.title', 'h3'],
      snippet: ['.bili-video-card__info--desc', '.des'], author: ['.bili-video-card__info--author', '.up-name'],
      publishedAt: ['.bili-video-card__info--date', '.pubdate'], metrics: ['.bili-video-card__stats', '.so-icon'],
      detail: ['.video-desc-container', '#v_desc', '.opus-module-content', '.article-holder'], detailTitle: ['h1.video-title', 'h1'] }, 'video'),
  profile('xiaohongshu', '小红书', ['xiaohongshu.com'], 'social', 'https://www.xiaohongshu.com/search_result?keyword={query}&source=web_search_result_notes',
    ['^https?://(?:www\\.)?xiaohongshu\\.com/(?:explore|discovery/item|search_result)/[a-zA-Z0-9]{16,}(?:[/?#]|$)'],
    { cards: ['section.note-item', '.note-item'], title: ['.title', '.title span'], snippet: ['.desc'], author: ['.author .name', '.author-wrapper .username', '.name'],
      publishedAt: ['.date', '.publish-time', '.name-time-wrapper .time'], metrics: ['.like-wrapper', '.interactions'], detail: ['#detail-desc', '.note-content', '.note-scroller .content'], detailTitle: ['#detail-title', '.note-content .title'] }, 'post'),
  profile('douyin', '抖音', ['douyin.com'], 'social', 'https://www.douyin.com/search/{query}?type=general',
    ['^https?://(?:www\\.)?douyin\\.com/(?:video|note)/[0-9]+(?:[/?#]|$)', '^https?://(?:www\\.)?douyin\\.com/search/[^#]*[?&]modal_id=[0-9]+(?:&|$)'],
    { cards: ['.search-result-card', '[data-e2e="search-result"]', '[data-e2e="search-card"]', 'li[data-e2e]'], title: ['[data-e2e="video-desc"]', '.BjLsdJMi', '.title'],
      author: ['[data-e2e="search-card-author"]', '[data-e2e="video-author"]'], metrics: ['[data-e2e="video-like-count"]'],
      detail: ['[data-e2e="video-desc"]', '[data-e2e="note-desc"]'], detailTitle: ['h1', '[data-e2e="video-desc"]'] }, 'video'),
  profile('zhihu', '知乎', ['zhihu.com'], 'social', 'https://www.zhihu.com/search?type=content&q={query}',
    ['^https?://(?:www\\.)?zhihu\\.com/(?:question/[0-9]+(?:/answer/[0-9]+)?|answer/[0-9]+)(?:[/?#]|$)', '^https?://zhuanlan\\.zhihu\\.com/(?:p|appview/p)/[0-9]+(?:[/?#]|$)'],
    { cards: ['.SearchResult-Card', '.SearchResult', '.List-item'], title: ['.ContentItem-title', 'h2'], snippet: ['.RichContent-inner', '.RichText'],
      author: ['.AuthorInfo-name', '.UserLink-link'], detail: ['.AnswerItem .RichContent-inner', '.Post-RichText', 'article .RichText'], detailTitle: ['.QuestionHeader-title', '.Post-Title', 'h1'] }),
  profile('csdn', 'CSDN', ['csdn.net'], 'social', 'https://so.csdn.net/so/search?q={query}&t=all',
    ['^https?://blog\\.csdn\\.net/[^/]+/article/details/[0-9]+(?:[/?#]|$)'],
    { cards: ['.search-result-item', '.search-list-item', '.so-item'], title: ['.title', 'h3'], snippet: ['.content', '.desc'], author: ['.author', '.user_name'],
      detail: ['#content_views', '.article_content'], detailTitle: ['#articleContentId', '.title-article', 'h1'] }),
  profile('juejin', '掘金', ['juejin.cn', 'juejin.im'], 'social', 'https://juejin.cn/search?query={query}&type=0',
    ['^https?://(?:www\\.)?juejin\\.(?:cn|im)/post/[0-9]+(?:[/?#]|$)'],
    { cards: ['.entry-list .entry', '.entry', '.search-entry'], title: ['.title', 'h2'], snippet: ['.abstract', '.content-wrapper'], author: ['.user-message .username', '.user-popover'],
      detail: ['.article-content', '.markdown-body'], detailTitle: ['.article-title', 'h1'] }),
  profile('weibo', '微博', ['weibo.com', 'weibo.cn'], 'social', 'https://s.weibo.com/weibo?q={query}',
    ['^https?://(?:www\\.|m\\.)?weibo\\.(?:com|cn)/(?:[0-9]{4,}/[a-zA-Z0-9]{5,}|status/[a-zA-Z0-9]+|detail/[0-9]+)(?:[/?#]|$)'],
    { cards: ['.card-wrap[data-mid]', '.card-wrap', 'article'], title: ['.txt'], snippet: ['.txt'], author: ['.name', '.info .name'],
      publishedAt: ['.from', 'time'], metrics: ['.card-act'], detail: ['.detail_wbtext', '.weibo-text', 'article [class*="text"]'], detailTitle: ['h1'] }, 'post'),
  profile('toutiao', '今日头条', ['toutiao.com'], 'social', 'https://so.toutiao.com/search/?dvpf=pc&keyword={query}',
    ['^https?://(?:www\\.)?toutiao\\.com/(?:article/[0-9]+|a[0-9]+|video/[0-9]+|w/a[0-9]+)(?:[/?#]|$)'],
    { cards: ['.result-content', '.search-result-item', 'article'], title: ['.cs-header', '.title', 'h2', 'h3'], detail: ['.article-content', 'article'], detailTitle: ['h1'] }),
  profile('youtube', 'YouTube', ['youtube.com', 'youtu.be'], 'social', 'https://www.youtube.com/results?search_query={query}',
    ['^https?://(?:www\\.|m\\.)?youtube\\.com/watch\\?[^#]*\\bv=[a-zA-Z0-9_-]+', '^https?://(?:www\\.|m\\.)?youtube\\.com/shorts/[a-zA-Z0-9_-]+(?:[/?#]|$)', '^https?://youtu\\.be/[a-zA-Z0-9_-]+(?:[/?#]|$)'],
    { cards: ['ytd-video-renderer', 'ytd-rich-item-renderer', 'yt-lockup-view-model'], title: ['#video-title', '.yt-lockup-metadata-view-model__title'], snippet: ['#description-text', '.metadata-snippet-text'],
      author: ['ytd-channel-name', '#channel-name'], publishedAt: ['time[datetime]', '#metadata-line .inline-metadata-item:nth-child(2)'], metrics: ['#metadata-line'], detail: ['#description-inline-expander', 'ytd-watch-metadata #description'], detailTitle: ['ytd-watch-metadata h1', 'h1.ytd-watch-metadata', 'h1'] }, 'video'),
  profile('x', 'X', ['x.com', 'twitter.com'], 'social', 'https://x.com/search?q={query}&src=typed_query&f=live',
    ['^https?://(?:www\\.|mobile\\.)?(?:x\\.com|twitter\\.com)/[a-zA-Z0-9_]+/status/[0-9]+(?:[/?#]|$)'],
    { cards: ['article[data-testid="tweet"]'], title: ['[data-testid="tweetText"]'], snippet: ['[data-testid="tweetText"]'], author: ['[data-testid="User-Name"]'],
      metrics: ['[role="group"]'], detail: ['article[data-testid="tweet"] [data-testid="tweetText"]'], detailTitle: ['h1'] }, 'post'),
  profile('reddit', 'Reddit', ['reddit.com'], 'social', 'https://www.reddit.com/search/?q={query}',
    ['^https?://(?:[a-z0-9-]+\\.)?reddit\\.com/(?:r/[^/]+/)?comments/[a-zA-Z0-9]+(?:[/?#]|$)'],
    { cards: ['shreddit-post', '[data-testid="post-container"]', '.search-result', 'article'], title: ['[slot="title"]', 'h3', '[data-testid="post-title"]'],
      author: ['[slot="authorName"]', '[data-testid="post_author_link"]'], detail: ['shreddit-post [slot="text-body"]', '[data-testid="post-content"]', '.usertext-body'], detailTitle: ['shreddit-post h1', 'h1'] }, 'post'),
  profile('github', 'GitHub', ['github.com'], 'code', 'https://github.com/search?q={query}&type=repositories',
    ['^https?://github\\.com/(?!(?:search|topics|collections|features|marketplace|settings|login|signup|orgs|users|sponsors|notifications)(?:/|$))[^/?#]+/[^/?#]+(?:[/?#]|$)'],
    { cards: ['[data-testid="results-list"] > div', '.repo-list-item', '.search-title + div', '.Box-sc-g0xbh4-0'], title: ['.search-title', 'h3'], snippet: ['[data-testid="results-list"] p', 'p'],
      detail: ['article.markdown-body', '.markdown-body', '#readme'], detailTitle: ['h1 strong', 'h1'] }, 'repository'),
  profile('bing', 'Bing', ['bing.com'], 'web', 'https://www.bing.com/search?q={query}', [],
    { cards: ['li.b_algo'], title: ['h2'], snippet: ['.b_caption p', '.b_snippet'], detail: shared.detail }),
  profile('baidu', '百度', ['baidu.com'], 'web', 'https://www.baidu.com/s?wd={query}', [],
    { cards: ['.result.c-container', '.c-container', '.result-op'], title: ['h3'], snippet: ['.c-abstract', '[class*="content-right"]'], detail: shared.detail }),
  profile('google', 'Google', ['google.com', 'google.com.hk', 'google.co.uk', 'google.de', 'google.co.jp'], 'web', 'https://www.google.com/search?q={query}', [],
    { cards: ['#search .g', '.MjjYud', '[data-sokoban-container]'], title: ['h3'], snippet: ['.VwiC3b', '[data-sncf]'], detail: shared.detail })
];
function freeze(value) { if (value && typeof value === 'object') { Object.values(value).forEach(freeze); Object.freeze(value); } return value; }
profiles.forEach(freeze);
const aliases = { bili: 'bilibili', 'b站': 'bilibili', xhs: 'xiaohongshu', '小红书': 'xiaohongshu', twitter: 'x', 'github-code': 'github' };
function fail(code, message) { const e = new Error(message); e.code = code; return e; }
function domainProfile(id) {
  const raw = id.slice(5).trim().toLowerCase();
  if (!raw || /[\s/:?#@\\]/.test(raw)) throw fail('invalid_site_domain', 'Use site:example.com with a hostname only.');
  let hostname;
  try { hostname = new URL('https://' + raw).hostname.replace(/\.$/, ''); } catch { throw fail('invalid_site_domain', 'Invalid site domain.'); }
  if (hostname.length > 253 || !/^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{1,62}$/.test(hostname)) throw fail('invalid_site_domain', 'Use a public DNS domain.');
  return freeze({ ...profile('site:' + hostname, hostname + ' 站内索引', [hostname], 'web', query => 'https://www.google.com/search?q=' + encodeURIComponent('site:' + hostname + ' ' + query), [], { ...shared, cards: ['#search .g', '.MjjYud', '[data-sokoban-container]'], title: ['h3'], snippet: ['.VwiC3b', '[data-sncf]'] }), siteDomain: hostname });
}
export function getPlatform(id) {
  if (typeof id !== 'string' || !id.trim()) throw fail('unknown_platform', 'A platform id is required.');
  const normalized = id.trim().toLowerCase();
  if (normalized.startsWith('site:')) return domainProfile(normalized);
  const found = profiles.find(p => p.id === (aliases[normalized] || normalized));
  if (!found) throw fail('unknown_platform', 'Unknown platform: ' + id);
  return found;
}
export function listPlatforms() { return [...profiles]; }
export function searchURL(id, query) {
  if (typeof query !== 'string' || !query.trim()) throw fail('invalid_query', 'A non-empty query is required.');
  const p = getPlatform(id); return typeof p.searchUrl === 'function' ? p.searchUrl(query.trim()) : p.searchUrl.replaceAll('{query}', encodeURIComponent(query.trim()));
}
export function inferPlatform(value) {
  let url; try { url = new URL(value); } catch { return null; }
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) return null;
  const host = url.hostname.toLowerCase().replace(/\.$/, '');
  const p = profiles.find(p => p.hosts.some(h => host === h || host.endsWith('.' + h)));
  if (p) return p.id;
  try { return domainProfile('site:' + host).id; } catch { return null; }
}
