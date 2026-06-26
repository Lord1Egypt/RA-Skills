var __defProp = Object.defineProperty;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __publicField = (obj, key, value) => __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
(function() {
  "use strict";
  const MAX_SHADOW_DEPTH = 5;
  const MAX_SAMPLE = 100;
  function hasShadowContent() {
    const all = document.querySelectorAll("*");
    let checked = 0;
    for (let i = 0; i < all.length && checked < MAX_SAMPLE; i++) {
      const el = all[i];
      if (!el.tagName.includes("-")) continue;
      checked++;
      if (el.shadowRoot) return true;
    }
    return false;
  }
  function getParentAcrossShadow(el) {
    const parent = el.parentElement;
    if (parent) return parent;
    const root = el.getRootNode();
    if (root instanceof ShadowRoot && root.host instanceof HTMLElement) {
      return root.host;
    }
    return null;
  }
  function deepQuerySelectorAll(root, selector) {
    const results = [];
    deepQueryRecursive(root, selector, results, 0);
    return results;
  }
  function deepQueryRecursive(root, selector, results, depth) {
    if (depth > MAX_SHADOW_DEPTH) return;
    try {
      const matches = root.querySelectorAll(selector);
      for (let i = 0; i < matches.length; i++) {
        const el = matches[i];
        if (el instanceof HTMLElement) results.push(el);
      }
    } catch {
    }
    let elements;
    try {
      elements = root.querySelectorAll("*");
    } catch {
      return;
    }
    for (let i = 0; i < elements.length; i++) {
      const el = elements[i];
      if (el.shadowRoot) {
        deepQueryRecursive(el.shadowRoot, selector, results, depth + 1);
      }
    }
  }
  class ShadowAwareTreeWalker {
    constructor(root, whatToShow, filter) {
      __publicField(this, "walkerStack");
      __publicField(this, "whatToShow");
      __publicField(this, "filter");
      this.whatToShow = whatToShow;
      this.filter = filter;
      this.walkerStack = [document.createTreeWalker(root, whatToShow, filter)];
    }
    nextNode() {
      while (this.walkerStack.length > 0) {
        const walker = this.walkerStack[this.walkerStack.length - 1];
        const node = walker.nextNode();
        if (node === null) {
          this.walkerStack.pop();
          continue;
        }
        if (node.nodeType === Node.ELEMENT_NODE && this.walkerStack.length <= MAX_SHADOW_DEPTH) {
          const el = node;
          if (el.shadowRoot) {
            const shadowWalker = document.createTreeWalker(
              el.shadowRoot,
              this.whatToShow,
              this.filter
            );
            this.walkerStack.push(shadowWalker);
            continue;
          }
        }
        return node;
      }
      return null;
    }
  }
  let _pageHasShadowContent = false;
  const SKIP_TAGS$1 = /* @__PURE__ */ new Set([
    "SCRIPT",
    "STYLE",
    "NOSCRIPT",
    "SVG",
    "CANVAS",
    "VIDEO",
    "AUDIO",
    "IFRAME",
    "OBJECT",
    "EMBED",
    "INPUT",
    "SELECT",
    "TEXTAREA",
    "BUTTON",
    "IMG",
    "BR",
    "HR"
  ]);
  const NOISE_ANCESTOR_TAGS = /* @__PURE__ */ new Set([
    "NAV",
    "FOOTER",
    "HEADER",
    "ASIDE"
  ]);
  const NOISE_ROLES = /* @__PURE__ */ new Set([
    "navigation",
    "banner",
    "complementary",
    "contentinfo",
    "search",
    "menu",
    "menubar",
    "toolbar"
  ]);
  const NOISE_CLASS_PATTERN = /\b(sidebar|sidenav|side-nav|breadcrumb|toc|table-of-contents|nav-|navigation|menu|toolbar|social|share|sharing|subscribe|subscription|newsletter|signup|sign-up|cookie|consent|popup|modal|overlay|banner|advert|advertisement|ad-|ads-|sponsor|promo|related-posts|related-articles|recommended|disqus|respond|footer|header-|widget|badge|tag-list|categories|pagination|pager|page-nav|copyright|login|log-in|signin|sign-in|skip-link|skip-to|sr-only|visually-hidden|screen-reader|wpadminbar|admin-bar|wp-toolbar|code-block-extension|copy-code-btn|code-tool)\b|\bcomment/i;
  const POSITIVE_CLASS = /article|body|content|entry|hentry|h-entry|main|page|post|text|blog|story/i;
  const NEGATIVE_CLASS = /-ad-|hidden|^hid$|banner|combx|comment|com-|contact|footer|gdpr|masthead|media|meta|outbrain|promo|related|scroll|share|shoutbox|sidebar|skyscraper|sponsor|shopping|tags|widget/i;
  const SKIP_LINK_PATTERN = /^skip to (main )?content|^skip to (site )?search|^skip to navigation|^jump to content|^jump to navigation/i;
  const COPYRIGHT_PATTERN = /^[\s]*[\u00a9©]|^copyright\s|all rights reserved/i;
  const UI_TEXT_PATTERN = /^(sign ?in|sign ?up|log ?in|log ?out|register|subscribe|download|install|try .{0,10} free|get started|learn more|read more|see more|show more|load more|view all|view more|view details|close|dismiss|accept|reject|cancel|submit|save|delete|edit|reply|share|copy|print|follow|unfollow|like|bookmark|continue reading|manage|launch|upvote|more recipients?|post a comment|leave a comment|add a comment|write a review|ask .{0,20} here|登录|注册|订阅|下载|安装|免费试用|开始使用|了解更多|查看更多|显示更多|加载更多|关闭|取消|提交|保存|分享|复制|回复|关注|收藏|复制代码|代码解读|AI代码助手|体验AI代码助手|举报|投诉|收起|展开|点赞|踩|打赏|评论|转发|原创)$/i;
  const CODE_TOOLBAR_PATTERN = /AI代码助手|体验AI|代码解读|复制代码|copy code|view raw|run code|show raw|copy to clipboard|copied!|toggle line numbers/i;
  const ADMIN_ACTION_WORDS = /* @__PURE__ */ new Set([
    "manage",
    "edit",
    "post",
    "logout",
    "login",
    "dashboard",
    "new",
    "settings",
    "appearance",
    "plugins",
    "users",
    "tools",
    "comments",
    "delete",
    "publish",
    "draft",
    "preview",
    "update",
    "view",
    "profile"
  ]);
  const TERMINATION_PATTERNS = [
    // 评论区（最高置信度）
    /^(comments?\s*(\(\d+\))?|leave\s+a\s+(comment|reply)|post\s+a\s+comment|discussion|responses?|\d+\s*(comments?|replies))/i,
    /^(评论|留言|发表评论|写评论|全部评论|最新评论|热门评论|\d+\s*条?(评论|回复|留言))/,
    // 相关推荐
    /^(related\s+(articles?|posts?|stories?|reading|content)|see\s+also|more\s+from|recommended|you\s+(may|might)\s+(also\s+)?like|popular\s+posts?|trending|further\s+reading)/i,
    /^(相关(文章|推荐|阅读|内容)|猜你喜欢|你可能(也|还)?(喜欢|感兴趣)|推荐阅读|热门(文章|推荐)|延伸阅读|更多推荐)/,
    // 分享/订阅
    /^(share\s+this|share\s+on|share\s+via|subscribe\s+to|newsletter|sign\s+up\s+for)/i,
    /^(分享(到|本文|文章)|订阅|关注我们)/,
    // 作者信息
    /^(about\s+the\s+author|author\s+bio|written\s+by|posted\s+by)/i,
    /^(关于作者|作者简介|作者介绍)/
  ];
  const TERMINATION_CLASS_PATTERN = /\b(comments?|disqus|related|recommended|sidebar|sharing|social|newsletter|subscribe|author-bio)\b/i;
  const BLOCK_TAGS = /* @__PURE__ */ new Set([
    "P",
    "DIV",
    "SECTION",
    "ARTICLE",
    "MAIN",
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "LI",
    "BLOCKQUOTE",
    "PRE",
    "TD",
    "TH",
    "FIGCAPTION",
    "DT",
    "DD",
    "FONT",
    "NAV",
    "FOOTER",
    "HEADER",
    "ASIDE"
  ]);
  const EN_STOP_WORDS = /* @__PURE__ */ new Set([
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "can",
    "shall",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "at",
    "by",
    "from",
    "as",
    "into",
    "through",
    "during",
    "it",
    "its",
    "this",
    "that",
    "these",
    "those",
    "he",
    "she",
    "they",
    "we",
    "you",
    "i",
    "me",
    "my",
    "your",
    "his",
    "her",
    "our",
    "their",
    "and",
    "but",
    "or",
    "nor",
    "not",
    "no",
    "so",
    "if",
    "then",
    "than",
    "when",
    "where",
    "which",
    "who",
    "what",
    "how",
    "all",
    "each",
    "every",
    "both",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "only",
    "also"
  ]);
  const ZH_STOP_CHARS = /* @__PURE__ */ new Set([
    "的",
    "了",
    "在",
    "是",
    "我",
    "有",
    "和",
    "就",
    "不",
    "人",
    "都",
    "一",
    "上",
    "也",
    "很",
    "到",
    "说",
    "要",
    "去",
    "你",
    "会",
    "着",
    "看",
    "好",
    "这",
    "他",
    "她",
    "它",
    "们",
    "那",
    "些",
    "被",
    "从",
    "把",
    "与",
    "而",
    "及",
    "对",
    "但"
  ]);
  function getClassWeight(el) {
    let weight = 0;
    const cls = typeof el.className === "string" ? el.className : "";
    const id = el.id || "";
    if (cls) {
      if (NEGATIVE_CLASS.test(cls)) weight -= 25;
      if (POSITIVE_CLASS.test(cls)) weight += 25;
    }
    if (id) {
      if (NEGATIVE_CLASS.test(id)) weight -= 25;
      if (POSITIVE_CLASS.test(id)) weight += 25;
    }
    return weight;
  }
  function linkDensity(el) {
    var _a, _b;
    const totalText = ((_a = el.textContent) == null ? void 0 : _a.trim()) || "";
    if (totalText.length === 0) return 0;
    let linkText = 0;
    const links = el.querySelectorAll("a");
    for (const a of links) {
      const href = a.getAttribute("href");
      const coefficient = href && /^#/.test(href) ? 0.3 : 1;
      linkText += (((_b = a.textContent) == null ? void 0 : _b.trim().length) || 0) * coefficient;
    }
    return linkText / totalText.length;
  }
  function textDensity(el) {
    var _a;
    const chars = ((_a = el.textContent) == null ? void 0 : _a.trim().length) || 0;
    const tags = el.getElementsByTagName("*").length || 1;
    return chars / tags;
  }
  function stopWordDensity(text, lang) {
    if (lang === "zh") {
      const chars = text.split("");
      if (chars.length === 0) return 0;
      const count2 = chars.filter((c) => ZH_STOP_CHARS.has(c)).length;
      return count2 / chars.length;
    }
    const words = text.toLowerCase().split(/\s+/);
    if (words.length === 0) return 0;
    const count = words.filter((w) => EN_STOP_WORDS.has(w)).length;
    return count / words.length;
  }
  function detectLang() {
    var _a, _b;
    const htmlLang = document.documentElement.lang;
    if (htmlLang) {
      const lang = htmlLang.split("-")[0].toLowerCase();
      if (lang === "zh" || lang === "cn") return "zh";
      return lang;
    }
    const sampleText = ((_b = (_a = document.body) == null ? void 0 : _a.textContent) == null ? void 0 : _b.substring(0, 500)) || "";
    const chineseCount = (sampleText.match(/[\u4e00-\u9fa5]/g) || []).length;
    if (chineseCount > sampleText.length * 0.1) return "zh";
    return "en";
  }
  function findContentRoot() {
    var _a, _b, _c, _d, _e, _f, _g;
    if (!document.body) return document.body;
    const scores = /* @__PURE__ */ new Map();
    function initCandidate(el) {
      if (scores.has(el)) return;
      let base = 0;
      const tag = el.tagName;
      if (tag === "DIV") base = 5;
      else if (tag === "PRE" || tag === "TD" || tag === "BLOCKQUOTE") base = 3;
      else if (tag === "ARTICLE") base = 25;
      else if (tag === "MAIN" || tag === "SECTION") base = 15;
      else if (tag === "FORM" || tag === "UL" || tag === "OL" || tag === "DL") base = -3;
      if (el.getAttribute("role") === "main") base += 15;
      base += getClassWeight(el);
      scores.set(el, base);
    }
    const CONTENT_ELEMENT_WEIGHTS = {
      "P": 1,
      "LI": 0.5,
      "H2": 0.5,
      "H3": 0.5,
      "H4": 0.5,
      "H5": 0.5,
      "H6": 0.5,
      "BLOCKQUOTE": 0.75,
      "DD": 0.75,
      "DT": 0.5
    };
    const contentSelector = "p, li, h2, h3, h4, h5, h6, blockquote, dd, dt";
    const contentElements = _pageHasShadowContent ? deepQuerySelectorAll(document, contentSelector) : document.querySelectorAll(contentSelector);
    for (const el of contentElements) {
      const text = ((_a = el.textContent) == null ? void 0 : _a.trim()) || "";
      if (text.length < 25) continue;
      let inNoise = false;
      let check = _pageHasShadowContent ? getParentAcrossShadow(el) : el.parentElement;
      for (let d = 0; d < 4 && check && check !== document.body; d++) {
        if (NOISE_ANCESTOR_TAGS.has(check.tagName)) {
          inNoise = true;
          break;
        }
        const cls = check.className;
        const id = check.id;
        if (cls && typeof cls === "string" && NOISE_CLASS_PATTERN.test(cls)) {
          inNoise = true;
          break;
        }
        if (id && NOISE_CLASS_PATTERN.test(id)) {
          inNoise = true;
          break;
        }
        check = _pageHasShadowContent ? getParentAcrossShadow(check) : check.parentElement;
      }
      if (inNoise) continue;
      const commas = (text.match(/[,，、]/g) || []).length;
      const weight = CONTENT_ELEMENT_WEIGHTS[el.tagName] || 0.5;
      const elScore = (1 + commas + Math.min(Math.floor(text.length / 100), 3)) * weight;
      const parent2 = _pageHasShadowContent ? getParentAcrossShadow(el) : el.parentElement;
      if (parent2 && parent2 !== document.body) {
        initCandidate(parent2);
        scores.set(parent2, (scores.get(parent2) || 0) + elScore);
        const grandparent = _pageHasShadowContent ? getParentAcrossShadow(parent2) : parent2.parentElement;
        if (grandparent && grandparent !== document.body) {
          initCandidate(grandparent);
          scores.set(grandparent, (scores.get(grandparent) || 0) + elScore / 2);
        }
      }
    }
    if (scores.size === 0) {
      return fallbackContentRoot();
    }
    const candidates = [];
    for (const [el, rawScore] of scores) {
      const ld = linkDensity(el);
      const bubbleScore = rawScore * (1 - ld);
      candidates.push({ el, bubbleScore, qualityScore: 0, finalScore: 0 });
    }
    candidates.sort((a, b) => b.bubbleScore - a.bubbleScore);
    const topCandidates = candidates.slice(0, 3).filter((c) => c.bubbleScore > 0);
    if (topCandidates.length === 0) {
      return fallbackContentRoot();
    }
    const lang = detectLang();
    const maxBubble = topCandidates[0].bubbleScore;
    for (const c of topCandidates) {
      const text = ((_b = c.el.textContent) == null ? void 0 : _b.trim()) || "";
      const sw = stopWordDensity(text.substring(0, 2e3), lang);
      const td = textDensity(c.el);
      const ld = linkDensity(c.el);
      c.qualityScore = sw * 0.4 + Math.min(td / 20, 1) * 0.3 + (1 - ld) * 0.3;
      const normBubble = maxBubble > 0 ? c.bubbleScore / maxBubble : 0;
      c.finalScore = normBubble * 0.7 + c.qualityScore * 0.3;
    }
    topCandidates.sort((a, b) => b.finalScore - a.finalScore);
    let bestEl = topCandidates[0].el;
    let bestScore = topCandidates[0].bubbleScore;
    const threshold = Math.max(10, bestScore * 0.2);
    const parent = bestEl.parentElement;
    if (parent && parent !== document.body) {
      let siblingContentCount = 0;
      for (const sibling of parent.children) {
        if (sibling === bestEl || !(sibling instanceof HTMLElement)) continue;
        const sibScore = scores.get(sibling) || 0;
        if (sibScore >= threshold) siblingContentCount++;
        if (sibling.className && sibling.className === bestEl.className) {
          const sibText = ((_c = sibling.textContent) == null ? void 0 : _c.trim().length) || 0;
          if (sibText > 300) siblingContentCount++;
        }
      }
      if (siblingContentCount >= 2) {
        bestEl = parent;
      }
    }
    const rootTextLen = ((_d = bestEl.textContent) == null ? void 0 : _d.trim().length) || 0;
    const bodyTextLen = ((_e = document.body.textContent) == null ? void 0 : _e.trim().length) || 0;
    if (bodyTextLen > 2e3 && rootTextLen < bodyTextLen * 0.3) {
      const semantic = fallbackContentRoot();
      if (semantic !== document.body) {
        const semTextLen = ((_f = semantic.textContent) == null ? void 0 : _f.trim().length) || 0;
        if (semTextLen > rootTextLen * 1.5) {
          bestEl = semantic;
        } else {
          const rootText = ((_g = bestEl.textContent) == null ? void 0 : _g.trim().substring(0, 2e3)) || "";
          const rootSw = stopWordDensity(rootText, lang);
          if (rootSw < 0.1 && semTextLen > rootTextLen) {
            bestEl = semantic;
          }
        }
      } else {
        if (rootTextLen < bodyTextLen * 0.15) {
          bestEl = document.body;
        }
      }
    }
    const bestCls = bestEl.className;
    const bestId = bestEl.id;
    if (NOISE_ANCESTOR_TAGS.has(bestEl.tagName) || bestCls && typeof bestCls === "string" && NOISE_CLASS_PATTERN.test(bestCls) || bestId && NOISE_CLASS_PATTERN.test(bestId)) {
      bestEl = fallbackContentRoot();
    }
    return bestEl;
  }
  function fallbackContentRoot() {
    var _a, _b, _c, _d;
    if (_pageHasShadowContent) {
      const articles = deepQuerySelectorAll(document, "article");
      for (const article of articles) {
        const text = ((_a = article.textContent) == null ? void 0 : _a.trim().length) || 0;
        if (text > 200) return article;
      }
      const mains = deepQuerySelectorAll(document, 'main, [role="main"]');
      for (const main of mains) {
        const text = ((_b = main.textContent) == null ? void 0 : _b.trim().length) || 0;
        if (text > 200) return main;
      }
    } else {
      const article = document.querySelector("article");
      if (article instanceof HTMLElement) {
        const text = ((_c = article.textContent) == null ? void 0 : _c.trim().length) || 0;
        if (text > 200) return article;
      }
      const main = document.querySelector('main, [role="main"]');
      if (main instanceof HTMLElement) {
        const text = ((_d = main.textContent) == null ? void 0 : _d.trim().length) || 0;
        if (text > 200) return main;
      }
    }
    return document.body;
  }
  function findBlockAncestor(node) {
    let current = _pageHasShadowContent ? getParentAcrossShadow(node) : node.parentElement;
    while (current && current !== document.body) {
      if (BLOCK_TAGS.has(current.tagName)) {
        return current;
      }
      current = _pageHasShadowContent ? getParentAcrossShadow(current) : current.parentElement;
    }
    return document.body;
  }
  function isInNoiseAncestor(el, flags) {
    let current = el;
    let depth = 0;
    while (current && current !== document.body && depth < 10) {
      if (NOISE_ANCESTOR_TAGS.has(current.tagName)) return true;
      const role = current.getAttribute("role");
      if (role && NOISE_ROLES.has(role)) return true;
      if (current.getAttribute("aria-hidden") === "true") return true;
      if (current.hasAttribute("hidden")) return true;
      if (flags.useNoiseAncestor && depth < 6) {
        const cls = current.className;
        const id = current.id;
        if (cls && typeof cls === "string" && NOISE_CLASS_PATTERN.test(cls)) return true;
        if (id && NOISE_CLASS_PATTERN.test(id)) return true;
      }
      current = _pageHasShadowContent ? getParentAcrossShadow(current) : current.parentElement;
      depth++;
    }
    return false;
  }
  function detectTerminationPoint(blocks) {
    const goodCountBefore = (idx) => {
      let count = 0;
      for (let i = 0; i < idx; i++) {
        if (blocks[i].classification === "good") count++;
      }
      return count;
    };
    for (let i = 0; i < blocks.length; i++) {
      const block = blocks[i];
      const text = block.text.trim();
      if (text.length > 120) continue;
      let isTermination = TERMINATION_PATTERNS.some((p) => p.test(text));
      if (!isTermination) {
        const el = block.element;
        const cls = el.className;
        const id = el.id;
        if (cls && typeof cls === "string" && TERMINATION_CLASS_PATTERN.test(cls) || id && TERMINATION_CLASS_PATTERN.test(id)) {
          isTermination = true;
        }
        const parent = el.parentElement;
        if (!isTermination && parent) {
          const pCls = parent.className;
          const pId = parent.id;
          if (pCls && typeof pCls === "string" && TERMINATION_CLASS_PATTERN.test(pCls) || pId && TERMINATION_CLASS_PATTERN.test(pId)) {
            isTermination = true;
          }
        }
      }
      if (!isTermination) continue;
      if (goodCountBefore(i) < 3) continue;
      const lookAhead = Math.min(5, blocks.length - i - 1);
      if (lookAhead > 0) {
        let goodAfter = 0;
        for (let j = i + 1; j <= i + lookAhead; j++) {
          if (blocks[j].classification === "good") goodAfter++;
        }
        if (goodAfter > lookAhead * 0.6) continue;
      }
      return i;
    }
    return -1;
  }
  function mergeAdjacentBlocks(blocks) {
    if (blocks.length <= 1) return blocks;
    const SENTENCE_END = /[.!?。！？…；;]\s*$/;
    const HEADING_TAGS = /* @__PURE__ */ new Set(["H1", "H2", "H3", "H4", "H5", "H6"]);
    const CODE_TAGS = /* @__PURE__ */ new Set(["PRE", "CODE"]);
    const CAPTION_TAGS = /* @__PURE__ */ new Set(["FIGCAPTION", "CAPTION"]);
    const LIST_TAGS = /* @__PURE__ */ new Set(["LI", "DT", "DD"]);
    const SEMANTIC_BLOCK_TAGS = /* @__PURE__ */ new Set(["P", "BLOCKQUOTE", "SECTION", "ARTICLE", "TD", "TH"]);
    const MAX_MERGED_LENGTH = 2e3;
    const FRAGMENT_THRESHOLD = 150;
    const TINY_THRESHOLD = 80;
    function nearbyInDom(a, b, maxDepth = 3) {
      const getParent = _pageHasShadowContent ? getParentAcrossShadow : (el) => el.parentElement;
      if (getParent(a) === getParent(b) && getParent(a) !== null) return true;
      const ancestorsA = /* @__PURE__ */ new Set();
      let node = a;
      for (let i = 0; i < maxDepth && node; i++) {
        node = getParent(node);
        if (node) ancestorsA.add(node);
      }
      node = b;
      for (let i = 0; i < maxDepth && node; i++) {
        node = getParent(node);
        if (node && ancestorsA.has(node)) return true;
      }
      return false;
    }
    const result = [];
    let current = { ...blocks[0] };
    for (let i = 1; i < blocks.length; i++) {
      const next = blocks[i];
      const curTag = current.element.tagName;
      const nextTag = next.element.tagName;
      const isHeadingOrCode = HEADING_TAGS.has(curTag) || HEADING_TAGS.has(nextTag) || CODE_TAGS.has(curTag) || CODE_TAGS.has(nextTag) || CAPTION_TAGS.has(curTag) || CAPTION_TAGS.has(nextTag);
      const bothSemanticBlocks = SEMANTIC_BLOCK_TAGS.has(curTag) && SEMANTIC_BLOCK_TAGS.has(nextTag);
      const nearby = nearbyInDom(current.element, next.element);
      const isIncomplete = current.text.length < FRAGMENT_THRESHOLD && !SENTENCE_END.test(current.text);
      const isTiny = current.text.length < TINY_THRESHOLD && !LIST_TAGS.has(curTag) && !SENTENCE_END.test(current.text);
      const nextIsTail = next.text.length < 50 && !LIST_TAGS.has(nextTag);
      const shouldMerge = isIncomplete || isTiny || current.text.length < FRAGMENT_THRESHOLD && nextIsTail;
      const withinLimit = current.text.length + next.text.length + 1 <= MAX_MERGED_LENGTH;
      if (!isHeadingOrCode && !bothSemanticBlocks && nearby && shouldMerge && withinLimit) {
        current = { text: current.text + " " + next.text, element: current.element };
      } else {
        result.push(current);
        current = { ...next };
      }
    }
    result.push(current);
    return result;
  }
  function extractWithFlags(flags) {
    var _a, _b;
    if (!document.body) return [];
    const contentRoot = findContentRoot();
    const lang = detectLang();
    const walkerFilter = {
      acceptNode(node) {
        var _a2;
        if (node.nodeType === Node.ELEMENT_NODE) {
          const el = node;
          if (el.tagName === "BR") return NodeFilter.FILTER_ACCEPT;
          if (SKIP_TAGS$1.has(el.tagName)) return NodeFilter.FILTER_REJECT;
          if (el.tagName === "PRE") return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_SKIP;
        }
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        if (SKIP_TAGS$1.has(parent.tagName)) return NodeFilter.FILTER_REJECT;
        const text = (_a2 = node.textContent) == null ? void 0 : _a2.trim();
        if (!text) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    };
    const walker = _pageHasShadowContent ? new ShadowAwareTreeWalker(contentRoot, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, walkerFilter) : document.createTreeWalker(contentRoot, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, walkerFilter);
    const blockMap = /* @__PURE__ */ new Map();
    const elementVisitOrder = /* @__PURE__ */ new Map();
    let visitCounter = 0;
    let consecutiveBrs = 0;
    let lastBlockAncestor = null;
    let currentNode;
    while (currentNode = walker.nextNode()) {
      if (currentNode.nodeType === Node.ELEMENT_NODE) {
        consecutiveBrs++;
        continue;
      }
      const blockAncestor = findBlockAncestor(currentNode);
      if (!blockAncestor) {
        consecutiveBrs = 0;
        continue;
      }
      const text = ((_a = currentNode.textContent) == null ? void 0 : _a.trim()) || "";
      if (!text) {
        consecutiveBrs = 0;
        continue;
      }
      let groups = blockMap.get(blockAncestor);
      if (!groups) {
        groups = [[]];
        blockMap.set(blockAncestor, groups);
        elementVisitOrder.set(blockAncestor, visitCounter++);
      }
      if (consecutiveBrs >= 2 && blockAncestor === lastBlockAncestor && groups[groups.length - 1].length > 0) {
        groups.push([]);
      }
      groups[groups.length - 1].push(text);
      consecutiveBrs = 0;
      lastBlockAncestor = blockAncestor;
    }
    const preElements = _pageHasShadowContent ? deepQuerySelectorAll(contentRoot, "pre") : contentRoot.querySelectorAll("pre");
    for (const pre of preElements) {
      const el = pre;
      const text = (_b = el.textContent) == null ? void 0 : _b.trim();
      if (!text || text.length < 10) continue;
      if (!blockMap.has(el)) {
        blockMap.set(el, [[text]]);
      }
    }
    const rawBlocks = [];
    for (const [element, groups] of blockMap) {
      if (isInNoiseAncestor(element, flags)) continue;
      if (element.offsetHeight === 0 && element.offsetWidth === 0) continue;
      for (const group of groups) {
        const fullText = group.join(" ").trim();
        if (fullText.length < 10) continue;
        const ld = linkDensity(element);
        if (ld > 0.95) continue;
        if (flags.useShortFilters) {
          if (fullText.length < 50 && SKIP_LINK_PATTERN.test(fullText)) continue;
          if (fullText.length < 150 && COPYRIGHT_PATTERN.test(fullText)) continue;
          if (element === document.body && fullText.length < 100) continue;
          if (fullText.length < 50 && UI_TEXT_PATTERN.test(fullText)) continue;
          if (fullText.length < 100 && CODE_TOOLBAR_PATTERN.test(fullText)) continue;
          if (fullText.length < 80) {
            const words = fullText.toLowerCase().split(/\s+/);
            if (words.length >= 3 && words.every((w) => ADMIN_ACTION_WORDS.has(w))) continue;
          }
        }
        rawBlocks.push({ element, text: fullText });
      }
    }
    const scoredBlocks = rawBlocks.map((block) => {
      const ld = linkDensity(block.element);
      const td = textDensity(block.element);
      const sw = stopWordDensity(block.text, lang);
      const textLen = block.text.length;
      const metrics = { ld, td, sw, textLen };
      let classification;
      const contentScore = Math.min(textLen, 500) / 100 * (1 - ld) * (0.5 + sw * 0.5);
      if (block.element.tagName === "H1" && ld < 0.5) {
        classification = "good";
      } else if (textLen >= 100) {
        if (ld > 0.65 && sw < 0.1) {
          classification = "near-good";
        } else {
          classification = "good";
        }
      } else if (textLen >= 30) {
        if (sw >= 0.25 && ld < 0.5) {
          classification = "short";
        } else if (ld > 0.5 && sw < 0.15) {
          classification = "bad";
        } else if (contentScore < 0.08) {
          classification = "bad";
        } else {
          classification = "near-good";
        }
      } else {
        classification = "near-good";
      }
      return { element: block.element, text: block.text, classification, metrics };
    });
    for (let round = 0; round < 2; round++) {
      for (let i = 0; i < scoredBlocks.length; i++) {
        const block = scoredBlocks[i];
        if (block.classification === "good" || block.classification === "bad") continue;
        const prev = i > 0 ? scoredBlocks[i - 1].classification : "bad";
        const next = i < scoredBlocks.length - 1 ? scoredBlocks[i + 1].classification : "bad";
        if (block.classification === "short") {
          if (prev === "good" || next === "good") {
            block.classification = "good";
          } else if (prev === "bad" && next === "bad") {
            block.classification = "bad";
          }
        } else if (block.classification === "near-good") {
          if (prev === "good" || next === "good") {
            block.classification = "good";
          }
        }
      }
    }
    if (flags.useShortFilters) {
      const termIdx = detectTerminationPoint(scoredBlocks);
      if (termIdx >= 0) {
        for (let i = termIdx; i < scoredBlocks.length; i++) {
          scoredBlocks[i].classification = "bad";
        }
      }
    }
    const filteredBlocks = scoredBlocks.filter(
      (b) => b.classification !== "bad"
    );
    filteredBlocks.sort((a, b) => {
      const orderA = elementVisitOrder.get(a.element);
      const orderB = elementVisitOrder.get(b.element);
      if (orderA !== void 0 && orderB !== void 0) return orderA - orderB;
      const pos = a.element.compareDocumentPosition(b.element);
      if (pos & Node.DOCUMENT_POSITION_FOLLOWING) return -1;
      if (pos & Node.DOCUMENT_POSITION_PRECEDING) return 1;
      return 0;
    });
    const seenTexts = /* @__PURE__ */ new Set();
    const result = [];
    for (const block of filteredBlocks) {
      const textKey = block.text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text: block.text, element: block.element });
    }
    const merged = mergeAdjacentBlocks(result);
    const split = splitLongParagraphs(merged);
    return refineBroadElements(split);
  }
  const MAX_PARA_LENGTH = 500;
  const MIN_SPLIT_LENGTH = 80;
  function splitLongParagraphs(paras) {
    const result = [];
    for (const para of paras) {
      if (para.text.length <= MAX_PARA_LENGTH) {
        result.push(para);
        continue;
      }
      const splits = splitAtSentenceBoundaries(para.text, para.element);
      result.push(...splits);
    }
    return result;
  }
  function splitAtSentenceBoundaries(text, element) {
    const SENT_END = /[。！？!?…；;]+["'"'）)」》〉\]]*/g;
    const pieces = [];
    let currentStart = 0;
    let match;
    while ((match = SENT_END.exec(text)) !== null) {
      const endIdx = match.index + match[0].length;
      const chunkLen = endIdx - currentStart;
      if (chunkLen >= MIN_SPLIT_LENGTH) {
        pieces.push({ text: text.substring(currentStart, endIdx).trim(), element });
        currentStart = endIdx;
      }
    }
    if (currentStart < text.length) {
      const remaining = text.substring(currentStart).trim();
      if (remaining.length > 0) {
        if (pieces.length > 0 && remaining.length < MIN_SPLIT_LENGTH) {
          pieces[pieces.length - 1] = {
            text: pieces[pieces.length - 1].text + remaining,
            element
          };
        } else {
          pieces.push({ text: remaining, element });
        }
      }
    }
    return pieces.length > 0 ? pieces : [{ text, element }];
  }
  const MAX_HIGHLIGHT_HEIGHT = 600;
  function refineBroadElements(paras) {
    return paras.map((para) => {
      const el = para.element;
      if (el.offsetHeight <= MAX_HIGHLIGHT_HEIGHT) return para;
      const needle = para.text.substring(0, 30).replace(/\s+/g, "");
      if (!needle) return para;
      let best = null;
      let bestHeight = el.offsetHeight;
      const descendants = el.querySelectorAll("p, div, section, li, blockquote, dd, dt, td, figcaption");
      for (let i = 0; i < descendants.length; i++) {
        const d = descendants[i];
        const h = d.offsetHeight;
        if (h === 0 || h >= bestHeight) continue;
        const dText = (d.textContent || "").replace(/\s+/g, "");
        if (dText.includes(needle)) {
          best = d;
          bestHeight = h;
        }
      }
      return best ? { text: para.text, element: best } : para;
    });
  }
  function visibleTextBlockExtract() {
    if (!document.body) return [];
    _pageHasShadowContent = hasShadowContent();
    const strict = extractWithFlags({ useNoiseAncestor: true, useShortFilters: true });
    const strictChars = strict.reduce((s, p) => s + p.text.length, 0);
    const relaxShort = extractWithFlags({ useNoiseAncestor: true, useShortFilters: false });
    const relaxShortChars = relaxShort.reduce((s, p) => s + p.text.length, 0);
    const relaxAll = extractWithFlags({ useNoiseAncestor: false, useShortFilters: false });
    const relaxAllChars = relaxAll.reduce((s, p) => s + p.text.length, 0);
    const attempts = [
      { result: strict, totalChars: strictChars, quality: 3 },
      { result: relaxShort, totalChars: relaxShortChars, quality: 2 },
      { result: relaxAll, totalChars: relaxAllChars, quality: 1 }
    ].filter((a) => a.result.length >= 3 && a.totalChars >= 200);
    if (attempts.length === 0) {
      return [strict, relaxShort, relaxAll].sort(
        (a, b) => b.reduce((s, p) => s + p.text.length, 0) - a.reduce((s, p) => s + p.text.length, 0)
      )[0];
    }
    let maxChars = Math.max(...attempts.map((a) => a.totalChars));
    const noiseFilteredMax = Math.max(strictChars, relaxShortChars);
    if (noiseFilteredMax >= 2e3 && relaxAllChars > noiseFilteredMax * 2) {
      maxChars = noiseFilteredMax;
    }
    for (const attempt of attempts) {
      if (attempt.totalChars >= maxChars * 0.9) {
        return attempt.result;
      }
    }
    return attempts.sort((a, b) => b.totalChars - a.totalChars)[0].result;
  }
  function readAllExtract() {
    var _a;
    if (!document.body) return [];
    _pageHasShadowContent = hasShadowContent();
    const walkerFilter = {
      acceptNode(node) {
        var _a2;
        if (node.nodeType === Node.ELEMENT_NODE) {
          const el = node;
          if (el.tagName === "BR") return NodeFilter.FILTER_ACCEPT;
          if (SKIP_TAGS$1.has(el.tagName)) return NodeFilter.FILTER_REJECT;
          if (el.tagName === "PRE") return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_SKIP;
        }
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        if (SKIP_TAGS$1.has(parent.tagName)) return NodeFilter.FILTER_REJECT;
        const text = (_a2 = node.textContent) == null ? void 0 : _a2.trim();
        if (!text) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    };
    const walker = _pageHasShadowContent ? new ShadowAwareTreeWalker(document.body, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, walkerFilter) : document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, walkerFilter);
    const blockMap = /* @__PURE__ */ new Map();
    let consecutiveBrs = 0;
    let lastBlockAncestor = null;
    let currentNode;
    while (currentNode = walker.nextNode()) {
      if (currentNode.nodeType === Node.ELEMENT_NODE) {
        consecutiveBrs++;
        continue;
      }
      const blockAncestor = findBlockAncestor(currentNode);
      if (!blockAncestor) {
        consecutiveBrs = 0;
        continue;
      }
      const text = ((_a = currentNode.textContent) == null ? void 0 : _a.trim()) || "";
      if (!text) {
        consecutiveBrs = 0;
        continue;
      }
      let groups = blockMap.get(blockAncestor);
      if (!groups) {
        groups = [[]];
        blockMap.set(blockAncestor, groups);
      }
      if (consecutiveBrs >= 2 && blockAncestor === lastBlockAncestor && groups[groups.length - 1].length > 0) {
        groups.push([]);
      }
      groups[groups.length - 1].push(text);
      consecutiveBrs = 0;
      lastBlockAncestor = blockAncestor;
    }
    const noiseFlags = { useNoiseAncestor: false };
    const rawBlocks = [];
    for (const [element, groups] of blockMap) {
      if (isInNoiseAncestor(element, noiseFlags)) continue;
      if (element.offsetHeight === 0 && element.offsetWidth === 0) continue;
      for (const group of groups) {
        const fullText = group.join(" ").trim();
        if (fullText.length < 10) continue;
        const ld = linkDensity(element);
        if (ld > 0.95) continue;
        if (fullText.length < 50 && UI_TEXT_PATTERN.test(fullText)) continue;
        if (fullText.length < 50 && SKIP_LINK_PATTERN.test(fullText)) continue;
        rawBlocks.push({ element, text: fullText });
      }
    }
    rawBlocks.sort((a, b) => {
      const pos = a.element.compareDocumentPosition(b.element);
      if (pos & Node.DOCUMENT_POSITION_FOLLOWING) return -1;
      if (pos & Node.DOCUMENT_POSITION_PRECEDING) return 1;
      return 0;
    });
    const seenTexts = /* @__PURE__ */ new Set();
    const result = [];
    for (const block of rawBlocks) {
      const textKey = block.text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text: block.text, element: block.element });
    }
    return refineBroadElements(splitLongParagraphs(result));
  }
  const rules = /* @__PURE__ */ JSON.parse(`[{"id":"baike.baidu.com-general","domain":"baike.baidu.com","pathPattern":"^/item/","contentSelector":".J-lemma-content","paragraphSelector":"[data-tag='paragraph'], [data-tag='header']","excludeSelectors":[".J-supWrap",".J-pgc-after-content",".page-footer-content",".block-item","[data-tag='ref']"],"titleSelector":".J-lemma-title","confidence":0.9,"originalScore":0,"validatedScore":0,"source":"manual","evalRunId":"manual-baike","createdAt":"2026-03-07T00:00:00.000Z","updatedAt":"2026-03-07T00:00:00.000Z","notes":"百度百科词条页。J- 前缀类名是稳定标识。排除脚注(J-supWrap)和底部推荐(block-item)。"},{"id":"thepaper.cn-newsDetail","domain":"thepaper.cn","pathPattern":"^/newsDetail_forward_","contentSelector":"[class*='cententWrap']","paragraphSelector":"p","excludeSelectors":["[class*='copyrightBox']","[class*='recommendsWrap']","[class*='bottomBox']","[class*='commonsider']","[class*='handpick_content']","[class*='image_desc']"],"titleSelector":"h1","confidence":0.9,"originalScore":0,"validatedScore":0,"source":"manual","evalRunId":"manual-thepaper","createdAt":"2026-03-07T00:00:00.000Z","updatedAt":"2026-03-07T00:00:00.000Z","notes":"澎湃新闻文章页。CSS Modules hashed class，用 [class*=] 部分匹配。正文在 cententWrap 内的 <p> 标签。"},{"id":"developer.mozilla.org-general","domain":"developer.mozilla.org","pathPattern":"^/","contentSelector":"main#content .layout__body","paragraphSelector":"p, h1, h2, h3, h4, pre, ul, ol, dl, blockquote, table, .notecard","excludeSelectors":["nav","aside","header","footer",".breadcrumbs",".breadcrumbs-bar",".left-sidebar",".layout__right-sidebar","#main-sidebar",".a11y-menu",".navigation","mdn-search-modal","mdn-placement-top","mdn-placement-bottom",".footer",".layout__header",".page-layout__banner",".page-layout__footer"],"titleSelector":"main#content h1","confidence":0.85,"originalScore":2.3,"validatedScore":8.5,"source":"eval-learn","evalRunId":"manual-cleanup","createdAt":"2026-02-20T17:33:24.695Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"All MDN pages."},{"id":"stackoverflow.com-general","domain":"stackoverflow.com","pathPattern":"^/questions/\\\\d+","contentSelector":"div#mainbar","paragraphSelector":"div.s-prose p, div.s-prose pre, div.s-prose ul, div.s-prose ol, div.s-prose h1, div.s-prose h2, div.s-prose h3, div.s-prose blockquote","excludeSelectors":["div#sidebar","div.post-menu","div.comments-list","div.comment-form","div.vote-cell","div.user-info","div.post-signature","div.js-post-notice","div.related","div.linked","nav","header","footer","div.s-topbar","div#left-sidebar","div.js-post-tag-list-wrapper","div.question-stats","div.d-flex.fw-wrap.gs4.gsy.fd-column.meta-tags","div.copy-snippet","div.js-post-comments-component","div.post-signature",".s-btn","a.js-share-link","button"],"titleSelector":"h1.fs-headline1 a, h1[itemprop='name'] a","confidence":0.7799999999999999,"originalScore":4.95,"validatedScore":7.799999999999999,"source":"eval-learn","evalRunId":"2026-02-21T10-31-50-znfs","createdAt":"2026-02-21T11:11:46.268Z","updatedAt":"2026-02-21T11:11:46.268Z","notes":"Stack Overflow's main content lives in div#mainbar which contains both the question and all answers. The s-prose class wraps the actual formatted content of each post. Excluding sidebar, navigation, vote controls, user cards, comments, and UI buttons will isolate the article text. The title is in an h1 with class fs-headline1 containing an anchor tag. Waiting for answer prose ensures the page is fully loaded before extraction."},{"id":"wxt.dev-general","domain":"wxt.dev","pathPattern":"^/","contentSelector":"div.VPDoc .content main","paragraphSelector":"p, h1, h2, h3, ul, ol, blockquote","excludeSelectors":["header.VPNav","aside.VPSidebar","div.VPLocalNav","footer.VPFooter",".VPSkipLink",".aside",".edit-link",".prev-next","div[class*='tip']",".custom-block.tip > p:first-child"],"titleSelector":"h1","confidence":0.785,"originalScore":5.05,"validatedScore":7.85,"source":"eval-learn","evalRunId":"2026-02-20T16-57-10-shqr","createdAt":"2026-02-20T17:33:24.696Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"VitePress-based docs."},{"id":"rust-lang.github.io-async-book","domain":"rust-lang.github.io","pathPattern":"^/async-book/","contentSelector":"div#content.content","paragraphSelector":"p, h1, h2, h3, li, pre, blockquote","excludeSelectors":["div#mdbook-help-container","div#mdbook-help-popup","nav#sidebar","div#menu-bar","div#search-wrapper","nav.nav-wide-wrapper","div#sidebar-resize-handle"],"titleSelector":"div#content.content h1","confidence":0.81,"originalScore":5.35,"validatedScore":8.1,"source":"eval-learn","evalRunId":"2026-02-20T16-57-10-shqr","createdAt":"2026-02-20T17:33:24.696Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"mdBook-based docs."},{"id":"alistapart.com-articles","domain":"alistapart.com","pathPattern":"^/article/","contentSelector":"article .entry-content","paragraphSelector":"p, h2, h3, blockquote, pre, ul, ol","excludeSelectors":["nav","header","footer",".site-header",".site-footer",".skip-link",".search-form",".widget-area",".banner","aside",".share-this",".article-actions",".translations",".become-patron",".comments-area",".entry-meta",".entry-footer"],"titleSelector":"article h1.entry-title","confidence":0.75,"originalScore":4.2,"validatedScore":7.5,"source":"eval-learn","evalRunId":"2026-02-20T16-57-10-shqr","createdAt":"2026-02-20T17:33:24.696Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"A List Apart articles."},{"id":"en.wikipedia.org-general","domain":"en.wikipedia.org","pathPattern":"^/wiki/","contentSelector":"main#content .mw-parser-output","paragraphSelector":"p, h2, h3, h4","excludeSelectors":[".vector-header-container",".vector-column-start",".mw-footer-container","#mw-navigation",".vector-main-menu-container",".vector-sticky-pinned-container",".mw-portlet-lang","#p-lang-btn",".navbox","div[class*='navbox']",".sidebar","div[class*='sidebar']","table[class*='sidebar']","table.sidebar",".infobox",".reflist",".references",".mw-editsection",".vector-toc","#toc",".toc",".catlinks",".mbox-small",".ambox","div.hatnote",".noprint",".mw-jump-link","style","script"],"titleSelector":"h1#firstHeading","confidence":0.84,"originalScore":2.25,"validatedScore":8.4,"source":"eval-learn","evalRunId":"manual-v4","createdAt":"2026-02-20T18:12:15.504Z","updatedAt":"2026-02-21T12:00:00.000Z","notes":"All EN Wikipedia. p/h only to avoid sidebar noise."},{"id":"zh.wikipedia.org-general","domain":"zh.wikipedia.org","pathPattern":"^/wiki/","contentSelector":"main#content .mw-body-content","paragraphSelector":"p, h2, h3, h4, li, dd","excludeSelectors":[".vector-header-container",".vector-column-start",".mw-footer-container","#mw-navigation",".toc","#toc",".navbox","div[class*='navbox']",".sidebar","div[class*='sidebar']","table[class*='sidebar']",".infobox",".mw-editsection",".reflist",".references",".vector-main-menu-container",".vector-sticky-pinned-container","#siteNotice",".mw-jump-link",".vector-user-links",".catlinks",".printfooter","#p-search",".va-variant-prompt",".vector-sticky-header",".noprint","style","script"],"titleSelector":"h1#firstHeading","confidence":0.855,"originalScore":3,"validatedScore":8.55,"source":"eval-learn","evalRunId":"2026-02-20T17-39-50-uhv1","createdAt":"2026-02-20T18:12:15.504Z","updatedAt":"2026-02-21T12:00:00.000Z","notes":"All ZH Wikipedia. p/h only."},{"id":"react.dev-general","domain":"react.dev","pathPattern":"^/","contentSelector":"article.font-normal.break-words","paragraphSelector":"p, h2, h3, pre, ul, ol","excludeSelectors":["nav",".z-40.sticky","div.fixed.top-0","div.hidden.-mt-16","div.self-stretch.w-full","next-route-announcer"],"titleSelector":"article.font-normal.break-words h1","confidence":0.77,"originalScore":2.25,"validatedScore":7.7,"source":"eval-learn","evalRunId":"2026-02-20T17-39-50-uhv1","createdAt":"2026-02-20T18:12:15.504Z","updatedAt":"2026-02-21T12:00:00.000Z","notes":"All react.dev pages."},{"id":"vite.dev-general","domain":"vite.dev","pathPattern":"^/","contentSelector":"div.VPDoc .content main","paragraphSelector":"p, h1, h2, h3, li, pre, blockquote","excludeSelectors":[".VPSkipLink",".top-banner","nav",".VPNav",".VPSidebar",".VPLocalNav",".VPDocFooter",".carbon-ads",".ads","[class*='carbon']",".pager",".edit-link",".visually-hidden","aside",".VPSidebarItem",".language-selector",".appearance-switch","footer",".last-updated"],"titleSelector":"h1","confidence":0.67,"originalScore":4.05,"validatedScore":6.7,"source":"eval-learn","evalRunId":"2026-02-20T17-39-50-uhv1","createdAt":"2026-02-20T18:12:15.504Z","updatedAt":"2026-02-21T12:00:00.000Z","notes":"VitePress docs. Consolidated from 2 rules."},{"id":"blog.pragmaticengineer.com-posts","domain":"blog.pragmaticengineer.com","pathPattern":"^/","contentSelector":"section#content.post-content","paragraphSelector":"p, h2, h3, li","excludeSelectors":["div.nav.mobile","div.nav-desktop","span.nav-cover","section.authorAndShare","section#newsletter-second","section.author",".subscribe-button","nav","footer"],"titleSelector":"article.post h1","confidence":0.69,"originalScore":4,"validatedScore":6.9,"source":"eval-learn","evalRunId":"2026-02-20T17-39-50-uhv1","createdAt":"2026-02-20T18:12:15.504Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"Ghost-based blog."},{"id":"coolshell.cn-articles","domain":"coolshell.cn","pathPattern":"^/articles/","contentSelector":"article .entry-content","paragraphSelector":"p, h2, h3, pre, ul, ol","excludeSelectors":[".EnlighterJSRAW",".enlighter-toolbar",".enlighter-origin","nav","header#masthead",".site-branding",".nav-searchbox",".post-series",".comments-area","footer",".adsbygoogle",".wp-block-code .toolbar","button",".copy-to-clipboard-container"],"titleSelector":"h1.entry-title","confidence":0.75,"originalScore":3.85,"validatedScore":7.5,"source":"eval-learn","evalRunId":"2026-02-20T17-39-50-uhv1","createdAt":"2026-02-20T18:12:15.504Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"CoolShell WordPress."},{"id":"news.ycombinator.com-items","domain":"news.ycombinator.com","pathPattern":"^/item","contentSelector":"table#hnmain tr:nth-child(3) td","paragraphSelector":".comment .commtext","excludeSelectors":[".navs",".comhead",".votelinks",".hnmore","a.togg",".reply","#pagespace","td.subtext"],"titleSelector":"a.titlelink, span.titleline > a","confidence":0.8550000000000001,"originalScore":4.05,"validatedScore":8.55,"source":"eval-learn","evalRunId":"2026-02-22T04-26-15-dnt1","createdAt":"2026-02-22T04:43:59.365Z","updatedAt":"2026-02-22T04:43:59.365Z","notes":"This is a Hacker News discussion page linking to an external article. The ideal fix would be to follow the external link to blogsystem5.substack.com and extract the article content there. If extracting HN comments is intended, use .comment .commtext to get only comment text bodies and exclude metadata elements like .comhead (username/timestamp), .votelinks, and .reply links. The title selector targets the linked article title in the HN listing."},{"id":"www.joelonsoftware.com-posts","domain":"www.joelonsoftware.com","pathPattern":"^/\\\\d+/\\\\d+/\\\\d+/","contentSelector":"article .entry-content","paragraphSelector":"p, li, h1, h2, h3","excludeSelectors":["header#masthead","footer#colophon",".site-header",".site-footer",".widget-area",".sidebar","nav",".skip-link",".toggle-bar",".toggle-tabs",".post-navigation",".comments-area","#colophon"],"titleSelector":"article .entry-header h1.entry-title","confidence":0.75,"originalScore":4.2,"validatedScore":7.5,"source":"eval-learn","evalRunId":"2026-02-21T02-35-18-cesp","createdAt":"2026-02-21T03:02:38.803Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"Joel on Software."},{"id":"www.liaoxuefeng.com-wiki","domain":"www.liaoxuefeng.com","pathPattern":"^/wiki/","contentSelector":"#gsi-chapter","paragraphSelector":"p, h1, h2, h3, pre, ul, ol, blockquote","excludeSelectors":["#gsi-sidebar","#gsi-index","#gsi-header","#gsi-footer","#gsi-offcanvas","#gsi-search","#comment-thread",".pdf-hidden","template"],"titleSelector":"#gsi-chapter h1","confidence":0.985,"originalScore":2.2,"validatedScore":9.85,"source":"eval-learn","evalRunId":"2026-02-21T02-35-18-cesp","createdAt":"2026-02-21T03:02:38.803Z","updatedAt":"2026-02-21T04:00:00.000Z","notes":"廖雪峰 Vue.js SPA 教程."},{"id":"www.theguardian.com-general","domain":"www.theguardian.com","pathPattern":"^/","contentSelector":"main#maincontent","paragraphSelector":"section.dcr-dqlcr0 ul li","excludeSelectors":["aside.ad-slot-container","div#bannerandheader","header","nav","gu-island","div.top-fronts-banner-ad-container","div.dcr-1e51nvv","span.dcr-12r3co1","div.dcr-1tbbfjt","div.dcr-jphuvb","div.dcr-1eiql86",".js-ad-slot",".ad-slot"],"titleSelector":"div.dcr-ptvyla h2.dcr-1ln6kec","confidence":1,"originalScore":5.75,"validatedScore":10,"source":"eval-learn","evalRunId":"2026-02-22T06-00-17-j74n","createdAt":"2026-02-22T06:27:39.419Z","updatedAt":"2026-02-22T06:27:39.419Z","notes":"The main content is organized in date-sectioned <section> elements with class dcr-dqlcr0 inside main#maincontent. Each section contains <ul> lists of article cards. Targeting list items within these sections captures headlines, summaries, and timestamps in a structured way while excluding ads, navigation, banners, and UI chrome. The date headings inside div#*-title elements can be included as section separators. Excluding dcr-1tbbfjt (ad placeholders), dcr-jphuvb (date label wrappers), and dcr-1eiql86 (pagination/load-more) reduces noise."},{"id":"github.com-repos","domain":"github.com","pathPattern":"^/","contentSelector":"article.markdown-body.entry-content","paragraphSelector":"p, h1, h2, h3, li, pre","excludeSelectors":["nav","header","footer",".sr-only",".flash-container",".js-stale-session-flash",".HeaderMktg","#js-repo-pjax-container .repository-content .file-navigation","table.files",".Box-header"],"titleSelector":"h1 strong a, .js-repo-pjax-container h1 strong","confidence":0.8699999999999999,"originalScore":6.3,"validatedScore":8.7,"source":"eval-learn","evalRunId":"2026-02-22T06-00-17-j74n","createdAt":"2026-02-22T06:27:39.419Z","updatedAt":"2026-02-22T06:27:39.419Z","notes":"The article.markdown-body.entry-content element (2518 chars) contains the actual README content which is the primary article content for this GitHub repo page. Using this selector avoids GitHub navigation UI, file tree tables, and commit history while capturing the meaningful documentation. The title should be extracted from the repo name link in the breadcrumb rather than the generic search H1."},{"id":"web.dev-articles","domain":"web.dev","pathPattern":"^/articles/","contentSelector":"article.devsite-article","paragraphSelector":"p, li, h2, h3","excludeSelectors":["style","script","devsite-cookie-notification-bar","devsite-header","devsite-book-nav",".devsite-sidebar","devsite-footer-promos","devsite-footer-linkboxes","devsite-footer-utility",".devsite-banner",".devsite-page-rating",".devsite-article-meta","devsite-feedback",".nocontent","[data-hide-from-toc]"],"titleSelector":"article.devsite-article h1.devsite-page-title","confidence":0.6699999999999999,"originalScore":5.199999999999999,"validatedScore":6.699999999999999,"source":"eval-learn","evalRunId":"2026-02-21T11-59-20-cij9","createdAt":"2026-02-21T12:22:45.454Z","updatedAt":"2026-02-21T12:22:45.454Z","notes":"The article.devsite-article element (14,309 chars) is the most precise content container, closely matching the main#main-content area but excluding sidebar and navigation. Using it avoids CSS injection, UI chrome, and navigation noise. Excluding style/script tags and devsite-specific UI components (cookie bars, headers, footers, sidebars) will eliminate the CSS code block and collection-management UI. The h1.devsite-page-title within the article provides a clean title. Waiting for article.devsite-article ensures the content is rendered before extraction."},{"id":"danluu.com-general","domain":"danluu.com","pathPattern":"^/","contentSelector":"main","paragraphSelector":"p, h3, ul, ol, table","excludeSelectors":["header","header a","header hr"],"titleSelector":"header strong","confidence":0.6,"originalScore":3.45,"validatedScore":6,"source":"eval-learn","evalRunId":"2026-02-21T09-48-55-ajcl","createdAt":"2026-02-21T10:19:23.245Z","updatedAt":"2026-02-21T12:00:00.000Z","notes":"danluu.com. Generalized. Fixed to relative selectors."},{"id":"www.ruanyifeng.com-blog","domain":"www.ruanyifeng.com","pathPattern":"^/blog/","contentSelector":"article.hentry","paragraphSelector":"p, h2, h3, li, blockquote","excludeSelectors":["article.hentry .asset-meta","article.hentry .asset-footer","div#header","div#footer","div.asset-nav"],"titleSelector":"article.hentry h1, h1.asset-name","confidence":0.9099999999999999,"originalScore":6.55,"validatedScore":9.1,"source":"eval-learn","evalRunId":"2026-02-22T06-30-51-zb9o","createdAt":"2026-02-22T06:58:07.006Z","updatedAt":"2026-02-22T06:58:07.006Z","notes":"The article.hentry element (9084 chars) is the semantic content container and should capture more complete article content than the current extraction. Using it directly avoids navigation and sidebar noise. Excluding meta/footer sub-elements within the article removes publication metadata noise. The paragraph selector targets all meaningful content nodes including list items which are common in this weekly newsletter format. Sponsored content blocks may need additional exclusion by class if identifiable in the DOM."},{"id":"www.cnblogs.com-general","domain":"www.cnblogs.com","pathPattern":"^/","contentSelector":"div#cnblogs_post_body","paragraphSelector":"p, h2, h3, h4, li, pre, blockquote","excludeSelectors":["div#header","div#navigator","div#sideBar","div#footer","div.postDesc","div#post_next_prev","div#author_profile_info","div.blogStats",".cnblogs_code_collapse",".cnblogs_code_hide",".code_copy"],"titleSelector":"h1#cb_post_title_url, div#cb_post_title_url a","confidence":0.75,"originalScore":5.55,"validatedScore":7.5,"source":"manual-fix","evalRunId":"manual-fix-cnblogs-v2","createdAt":"2026-02-21T10:19:23.245Z","updatedAt":"2026-02-23T04:00:00.000Z","notes":"All cnblogs. Includes code blocks (pre) and blockquotes for programming tutorials."},{"id":"smashingmagazine.com-articles","domain":"www.smashingmagazine.com","pathPattern":"^/\\\\d+/\\\\d+/","contentSelector":"article.block.article div.row","paragraphSelector":"p, h2, h3, h4, ul, ol, blockquote, pre","excludeSelectors":["header.global-header","nav",".main-nav",".secondary-nav",".subnav",".article__summary",".author-bio","footer.main-footer","#comments-front-end-performance-2021-free-pdf-checklist",".email-newsletter",".newsletter-signup",".sponsor-message",".back-to-top-wrapper",".cart-wrapper",".article-tags",".share-links","section.article__summary"],"titleSelector":"h1","confidence":0.8699999999999999,"originalScore":6.949999999999999,"validatedScore":8.7,"source":"eval-learn","evalRunId":"2026-02-22T06-30-51-zb9o","createdAt":"2026-02-22T06:58:07.006Z","updatedAt":"2026-02-22T06:58:07.006Z","notes":"The main article content lives inside article.block.article > div.container.article-container > div.row. Excluding navigation, author bio, newsletter, sponsor blocks, comments section, and footer will reduce noise and bring character count closer to the 235K ground truth. The table of contents and download links (paragraphs 13-26) should also be excluded as they are UI navigation elements rather than article prose."},{"id":"36kr.com-articles","domain":"36kr.com","pathPattern":"^/p/","contentSelector":"div.article-content, div.content-wrapper, div.kr-layout-main","paragraphSelector":"p, h2, h3, li","excludeSelectors":["div.kr-header","div.kr-footer","nav","div.assit-wrapper","div.footer-content","a.feedBack","div.phone","div.code","div.top"],"titleSelector":"h1, div.article-title","confidence":0.8,"originalScore":3.25,"validatedScore":8,"source":"manual-v4","evalRunId":"manual-v4","createdAt":"2026-02-21T10:19:23.245Z","updatedAt":"2026-02-21T12:00:00.000Z","notes":"36kr tech articles."},{"id":"docs.anthropic.com-general","domain":"docs.anthropic.com","pathPattern":"^/en/docs/","contentSelector":"article#content-container","paragraphSelector":"p, h1, h2, h3, table, li","excludeSelectors":["header","nav","aside","ol.fixed","div.__variable_8d1da5 > div > header","div.flex-1 > div > div:first-child"],"titleSelector":"article#content-container h1","confidence":0.7699999999999999,"originalScore":2.15,"validatedScore":7.699999999999999,"source":"eval-learn","evalRunId":"2026-02-21T13-02-51-4bnu","createdAt":"2026-02-21T13:28:32.261Z","updatedAt":"2026-02-21T13:28:32.261Z","notes":"The DOM structure shows 'article#content-container' (4502 chars) as the most targeted content element, nested inside 'main#docs-scroll-container'. Using the article element directly avoids the navigation sidebar and header. Excluding nav, header, aside, and fixed-position elements ensures only the substantive documentation content is extracted."},{"id":"www.joshwcomeau.com-general","domain":"www.joshwcomeau.com","pathPattern":"^/","contentSelector":"article","paragraphSelector":"p, h2, h3, pre, li","excludeSelectors":["nav","header","footer","aside","button","[aria-label='Table of contents']"],"titleSelector":"h1","confidence":0.85,"originalScore":4.3,"validatedScore":8.55,"source":"manual-fix","evalRunId":"manual-fix-stable-selectors","createdAt":"2026-02-21T12:52:29.811Z","updatedAt":"2026-02-21T13:30:00.000Z","notes":"Josh Comeau blog. Uses stable semantic article tag (only 1 on page). Removed CSS-in-JS hashed class names that break on redeploy. Broadened pathPattern to all posts."},{"id":"tech.meituan.com-posts","domain":"tech.meituan.com","pathPattern":"^/\\\\d+/\\\\d+/\\\\d+/","contentSelector":"article, .post-content, .article-content, .content","paragraphSelector":"p, h2, h3, h4, pre, li, blockquote","excludeSelectors":["header","nav","footer","aside",".sidebar",".post-meta",".post-tags",".post-nav",".share",".comments",".related-posts"],"titleSelector":"h1, .post-title","confidence":0.75,"originalScore":0,"validatedScore":7.5,"source":"manual-fix","evalRunId":"manual-fix-meituan","createdAt":"2026-02-22T12:00:00.000Z","updatedAt":"2026-02-22T12:00:00.000Z","notes":"Meituan tech blog. SPA — may need DOM stabilization wait."},{"id":"www.theverge.com-general","domain":"www.theverge.com","pathPattern":"^/\\\\d+/","contentSelector":"body","paragraphSelector":"p.duet--article--dangerously-set-cms-markup, p.duet--article--standard-paragraph, h2.duet--article--dangerously-set-cms-markup","excludeSelectors":["nav","header","footer","aside",".duet--layout--rail",".duet--layout--sticky-rail",".duet--article--article-recirc",".duet--recirculation",".duet--ad","[data-analytics-placement='recirc']",".duet--layout--comments",".duet--article--contributors",".duet--cta",".duet--content-cards","[class*='--recirc']","[class*='--newsletter']","[class*='--top-stories']"],"titleSelector":"h1","confidence":0.8,"originalScore":5.5,"validatedScore":8,"source":"manual-v6","evalRunId":"manual-2026-02-25","createdAt":"2026-02-25T00:00:00.000Z","updatedAt":"2026-02-25T00:00:00.000Z","notes":"The Verge uses Next.js with duet-- CSS classes. Article paragraphs use .duet--article--dangerously-set-cms-markup. Recirc/sidebar/ad elements excluded."},{"id":"www.163.com-tech","domain":"www.163.com","pathPattern":"^/tech/article/","contentSelector":"div.post_body","paragraphSelector":"p, h2, h3","excludeSelectors":["div.post_recommends_ulist","div.related_article","div.post_crumb","div.date-source","div#keywords","div.ep-source","div.nph_photo_group","div.comment-list","div.tie-recommend","#endText_tone498","script","style"],"titleSelector":"h1.post_title","confidence":0.8,"originalScore":5,"validatedScore":8,"source":"manual-v6","evalRunId":"manual-2026-02-25","createdAt":"2026-02-25T00:00:00.000Z","updatedAt":"2026-02-25T00:00:00.000Z","notes":"163.com news articles. Content in div.post_content, paragraphs in p tags. Exclude recommendations and related articles."},{"id":"sina.com.cn-article","domain":"finance.sina.com.cn","pathPattern":"^/","contentSelector":"div.article#artibody","paragraphSelector":"p","excludeSelectors":["div#left_hzh_ad","div.show_statement","div#keywords","div.article-editor","script","style"],"titleSelector":"h1.main-title","confidence":0.8,"originalScore":5,"validatedScore":8,"source":"manual-v6","evalRunId":"manual-2026-02-25","createdAt":"2026-02-25T00:00:00.000Z","updatedAt":"2026-02-25T00:00:00.000Z","notes":"Sina Finance articles. #artibody is the universal article body container across all Sina properties. Exclude ads and footer statements."},{"id":"www.zhangxinxu.com-2026-02-21T18-22-35","domain":"www.zhangxinxu.com","pathPattern":"^/wordpress/\\\\d+/\\\\d+/inline-block-space-remove-%E5%8E%BB%E9%99%A4%E9%97%B4%E8%B7%9D/","contentSelector":"div.entry","paragraphSelector":"p, pre, h3, ul, ol, blockquote","excludeSelectors":["div#respond","ol.commentlist","div.navigation","div#sidebar","div#header","div#footbar","div#footer","div#wwLazy","div#wwWatch","dialog#ywOverlay","div#forAnchor"],"titleSelector":"div#post-2357 h1, div.post h1","confidence":0.71,"originalScore":4.199999999999999,"validatedScore":7.1,"source":"eval-learn","evalRunId":"2026-02-21T18-22-35-0i65","createdAt":"2026-02-21T18:38:41.344Z","updatedAt":"2026-02-21T18:38:41.344Z","notes":"The 'div.entry' element (4570 chars) is the most focused content container within 'div#post-2357', containing the article body without comments or navigation. Using it avoids sidebar, comment section, and navigation noise. Excluding respond/commentlist/navigation/sidebar/footer/ads elements ensures clean article-only extraction. The title should be extracted from the post's h1 rather than the page title to avoid site name suffix."},{"id":"www.brendangregg.com-general","domain":"www.brendangregg.com","pathPattern":"^/blog/","contentSelector":"div.post","paragraphSelector":"p, ul, h2","excludeSelectors":["div.nav","div.recent","div.recentmobile","div.navmobile","div.header","div#comments_button","div#comments_content","h1.title","a.extra"],"titleSelector":"h2.big","confidence":0.9099999999999999,"originalScore":4.05,"validatedScore":9.1,"source":"eval-learn","evalRunId":"2026-02-22T04-54-24-ndzz","createdAt":"2026-02-22T05:07:19.569Z","updatedAt":"2026-02-22T05:07:19.569Z","notes":"The DOM structure clearly isolates article content within div.post (7543 chars), which matches the main content area. The nav, recent, recentmobile, and navmobile divs are all sidebar/navigation elements that should be excluded. The article title appears in h2.big within div.site, while h1.title is the site-level heading 'Brendan Gregg's Blog' and should not be used as the article title. Targeting div.post directly avoids all navigation contamination and should capture the complete tools list."},{"id":"www.reddit.com-2026-02-22T05-15-31","domain":"www.reddit.com","pathPattern":"^/r/programming/comments/\\\\d+kj1tu/linus_torvalds_on_good_coding_style/","contentSelector":"main#main-content shreddit-post, main#main-content [data-testid='post-container'], main#main-content .Post","paragraphSelector":"div[data-testid='post-content'], div[slot='text-body'], div.Comment__body","excludeSelectors":["shreddit-async-loader[bundlename='related_posts']","div[data-testid='recommended-posts']","faceplate-ad","div[data-adunit]","div.promotedlink","div[data-testid='post-vote-count']","reddit-header-large","div#reddit-chat","flex-left-nav-container","div.more-posts"],"titleSelector":"h1[slot='title'], shreddit-post h1","confidence":1,"originalScore":3.7,"validatedScore":10,"source":"eval-learn","evalRunId":"2026-02-22T05-15-31-p6nc","createdAt":"2026-02-22T05:38:18.856Z","updatedAt":"2026-02-22T05:38:18.856Z","notes":"Reddit's new Shreddit UI uses web components. The main post content lives inside shreddit-post elements with slot='text-body'. Comments are in separate comment thread components. Excluding ad slots, related posts loaders, and navigation components will eliminate the noise. Waiting for shreddit-post ensures dynamic content is loaded before extraction."},{"id":"www.v2ex.com-2026-02-22T06-00-17","domain":"www.v2ex.com","pathPattern":"^/t/\\\\d+","contentSelector":"#Main .box","paragraphSelector":".topic_content, .subtle .message, .reply_content","excludeSelectors":["#Top","#Leftbar","#Rightbar",".site-nav",".tools","#Bottom",".adsbygoogle","span.ago","span.fade.small","script","style"],"titleSelector":"#Main h1","confidence":1,"originalScore":6,"validatedScore":10,"source":"eval-learn","evalRunId":"2026-02-22T06-30-51-zb9o","createdAt":"2026-02-22T06:58:07.006Z","updatedAt":"2026-02-22T06:58:07.006Z","notes":"V2EX topic pages place the main post in #Main .box with class .topic_content for the body. Addenda (附言) use .subtle .message. Replies use .reply_content. Excluding sidebars (#Leftbar, #Rightbar), navigation, ads, and footer ensures clean extraction. The duplicate issue likely stems from extracting both a container element and its child text node — scoping to specific semantic classes avoids this."},{"id":"draveness.me-2026-02-22T07-30-47","domain":"draveness.me","pathPattern":"^/golang-101/","contentSelector":"div.article-content","paragraphSelector":"p, li, h2, h3, pre, blockquote","excludeSelectors":["header.header","footer.footer","aside","nav#TableOfContents","div.giscus","span.article-date","a.article-tag",".copyright"],"titleSelector":"h1.article-title","confidence":0.86,"originalScore":6.8999999999999995,"validatedScore":8.6,"source":"eval-learn","evalRunId":"2026-02-22T07-30-47-0rch","createdAt":"2026-02-22T08:08:04.102Z","updatedAt":"2026-02-22T08:08:04.102Z","notes":"The main article content is contained within div.article-content inside article.article. Using this specific selector avoids metadata (date, tags), sidebar table of contents, comments (giscus), and footer. The extraction appears to have stopped prematurely, likely due to a rendering or scroll issue — waiting for div.article-content ensures full content is loaded before extraction."},{"id":"juejin.cn-2026-02-22T08-13-51","domain":"juejin.cn","pathPattern":"^/post/[0-9a-f]+","contentSelector":"article.article","paragraphSelector":"p, h1, h2, h3, li, pre, blockquote","excludeSelectors":[".copy-code-btn",".ai-code-assistant",".code-block-extension-header",".byte-tooltip",".global-component-box","nav",".sidebar",".comment-list",".related-entry-list"],"titleSelector":"h1.article-title, article h1","confidence":0.7999999999999999,"originalScore":5.05,"validatedScore":7.999999999999999,"source":"eval-learn","evalRunId":"2026-02-22T08-13-51-29zb","createdAt":"2026-02-22T08:41:25.372Z","updatedAt":"2026-02-22T08:41:25.372Z","notes":"The DOM structure shows 'article.article' at 12184 chars is the best content candidate, closely matching the expected article length. Using it directly avoids navigation, sidebar, and comment noise. The title should be extracted from the H1 element rather than the document title which includes meta description noise. Excluding code-block UI elements prevents '体验AI代码助手 代码解读复制代码' from polluting paragraphs."},{"id":"standardebooks.org-chapters","domain":"standardebooks.org","pathPattern":"^/ebooks/.+/text/","contentSelector":"main section","paragraphSelector":"p, h2, h3","excludeSelectors":["header","footer","nav","[hidden]"],"titleSelector":"main section h2","confidence":0.85,"source":"manual-ebook-v1","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T10:00:00.000Z","notes":"Standard Ebooks chapters. Very clean semantic HTML with epub:type attributes. Content in main > section, paragraphs are plain <p> tags."},{"id":"gushiwen.cn-poems","domain":"gushiwen.cn","pathPattern":"^/shiwenv_","contentSelector":"div.main3 > div.left","paragraphSelector":"#sonsyuanwen div.contson, div.contyishang p","excludeSelectors":["div.tool","div.tool-all","div.tag","div.cankao","div.sonspic","div.lx","div.adsense","div.main_right","p.source","div.yizhu","iframe","audio","script","style"],"titleSelector":"div.sons h1","confidence":0.8,"source":"manual-ebook-v1","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T11:00:00.000Z","notes":"古诗文网 poem pages. Uses #sonsyuanwen div.contson to match ONLY the main poem (not recommended poems). div.contyishang p captures translation/background/appreciation sections."},{"id":"guwendao.net-poems","domain":"guwendao.net","pathPattern":"^/shiwenv_","contentSelector":"div.main3 > div.left","paragraphSelector":"#sonsyuanwen div.contson, div.contyishang p","excludeSelectors":["div.tool","div.tool-all","div.tag","div.cankao","div.sonspic","div.lx","div.adsense","div.main_right","p.source","div.yizhu","iframe","audio","script","style"],"titleSelector":"div.sons h1","confidence":0.8,"source":"manual-ebook-v1","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T11:00:00.000Z","notes":"guwendao.net (gushiwen.cn redirects here via JS). Same selectors as gushiwen.cn rule."},{"id":"zongheng.com-chapters","domain":"zongheng.com","pathPattern":"^/chapter/","contentSelector":".content","paragraphSelector":"p","excludeSelectors":["nav","header","footer",".reader-tools",".reader-setting",".vip-notice",".comment","script","style"],"titleSelector":".title_txtbox, h1","confidence":0.75,"source":"manual-ebook-v1","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T10:00:00.000Z","notes":"纵横中文网 chapter pages. Redirects book.zongheng.com → read.zongheng.com. Content in .content with <p> paragraphs. VIP chapters show preview only."},{"id":"17k.com-chapters","domain":"17k.com","pathPattern":"^/chapter/","contentSelector":"#readArea","paragraphSelector":"p","excludeSelectors":["p.copy","nav","header","footer",".readNav",".chapterNav",".recommend",".comment",".adsbygoogle","script","style"],"titleSelector":"#readArea h1","confidence":0.75,"source":"manual-ebook-v3","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T20:00:00.000Z","notes":"17K novel chapters. Content in <p> tags inside #readArea. Removed div.p from paragraphSelector to avoid matching the parent container."},{"id":"tapas.io-episodes","domain":"tapas.io","pathPattern":"^/episode/","contentSelector":"article, #viewport","paragraphSelector":"p","excludeSelectors":[".dropdown-float",".comment-popup",".js-comment-area",".js-float",".episode-list",".episode-nav","nav","header","footer","script","style"],"titleSelector":".js-ep-title, .viewer__header .title","confidence":0.7,"source":"manual-ebook-v1","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T10:00:00.000Z","notes":"Tapas.io episode pages. SPA with dynamic content loading. Content in article or #viewport container. Excludes episode navigation links and comment areas."},{"id":"wikisource.org-general","domain":"wikisource.org","pathPattern":"^/wiki/","contentSelector":"#mw-content-text .mw-parser-output","paragraphSelector":"p, h2, h3, h4, div.poem p, blockquote","excludeSelectors":["#mw-navigation",".vector-header-container",".vector-column-start",".mw-footer-container",".navbox",".sidebar",".infobox",".reflist",".references",".mw-editsection","#toc",".toc",".catlinks",".noprint",".mw-jump-link",".sistersitebox","table.ambox",".mbox-small","script","style"],"titleSelector":"h1#firstHeading","confidence":0.82,"source":"manual-ebook-v1","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T10:00:00.000Z","notes":"WikiSource pages (all languages). MediaWiki structure similar to Wikipedia. Includes div.poem p for poetry content. Excludes TOC, navboxes, edit links, references."},{"id":"jjwxc.net-chapters","domain":"jjwxc.net","pathPattern":"^/onebook\\\\.php","contentSelector":"div.novelbody","paragraphSelector":"div, p","splitByBr":true,"excludeSelectors":["#lockpage",".readsmall",".noveltitle",".novelinfo",".authorname_append","table.cytable",".noveldesc",".bookmark",".bookmark_save","#bookmark_div",".report","#report_div",".authorword","#author_say",".smallgray",".favorite","nav","header","footer","script","style","noscript"],"titleSelector":"div.noveltext h2","confidence":0.75,"source":"manual-ebook-v2","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T14:00:00.000Z","notes":"晋江文学城 chapter pages. Text in div.novelbody with <br> line breaks. splitByBr creates <span data-cr-para> wrappers for per-paragraph highlighting. Excludes bookmark/report/author-say UI noise."},{"id":"gutenberg.org-books","domain":"gutenberg.org","pathPattern":"^/files/","contentSelector":"body","paragraphSelector":"p, h1, h2, h3, h4, h5","excludeSelectors":["table[summary]",".pgheader",".pglicense","pre.pgheader",".pg-boilerplate","section.pg-boilerplate","script","style"],"titleSelector":"h1, h2.no-break","confidence":0.8,"source":"manual-ebook-v1","createdAt":"2026-02-25T10:00:00.000Z","updatedAt":"2026-02-25T10:00:00.000Z","notes":"Project Gutenberg HTML books. Very long documents (700K+ chars). Flat structure with body > p. Excludes PG boilerplate header/license. Note: may crash eval runner due to extreme length."},{"id":"wattpad.com-chapters","domain":"wattpad.com","pathPattern":"^/\\\\d+","contentSelector":"pre","paragraphSelector":"p","excludeSelectors":["nav","header","footer",".tag-items",".tags",".story-stats",".stats",".author-info",".writer-info",".share-tools",".social-share",".comment-container",".comments",".promoted-stories",".story-promotion","script","style"],"titleSelector":"h1","confidence":0.85,"source":"manual-ebook-v2","createdAt":"2026-02-25T12:00:00.000Z","updatedAt":"2026-02-25T14:00:00.000Z","notes":"Wattpad story chapters. Story text is in <pre> containing <p> paragraphs. The pathPattern matches /12345-story-chapter-name format."},{"id":"webnovel.com-chapters","domain":"webnovel.com","pathPattern":"^/book/","contentSelector":".cha-content .cha-words","paragraphSelector":".cha-paragraph p, p","excludeSelectors":["form.cha-score","div.cha-bts","pirate","div.user-links-wrap","div.tac","div.j_bottom_comment_area","div.g_ad_ph","i.para-comment","i.para-comment_num",".ad",".advertisement","script","style"],"titleSelector":".cha-tit h3, .cha-tit h1","confidence":0.85,"source":"manual-ebook-v2","createdAt":"2026-02-25T18:00:00.000Z","updatedAt":"2026-02-25T20:00:00.000Z","notes":"Webnovel (Qidian International) chapter pages. React SPA with Cloudflare. Content in .cha-words with .cha-paragraph > p structure. Excludes rating form, buttons, anti-piracy watermark, ads, and inline comment icons."},{"id":"perplexity.ai-pages","domain":"perplexity.ai","pathPattern":"^/page/","contentSelector":"main","paragraphSelector":"p, h1, h2, h3, h4, h5, h6, li, blockquote, pre, table","excludeSelectors":["nav","header","footer","button","[role=\\"button\\"]","svg",".sticky","[class*=\\"citation\\"]","[class*=\\"source-\\"]","[class*=\\"related\\"]","[class*=\\"sidebar\\"]","[class*=\\"follow-up\\"]"],"titleSelector":"h1","confidence":0.8,"source":"manual","createdAt":"2026-02-25T18:00:00.000Z","updatedAt":"2026-02-25T18:00:00.000Z","notes":"Perplexity Pages — AI-generated article/report pages."}]`);
  const siteRulesData = {
    rules
  };
  const SKIP_TAGS = ["SCRIPT", "STYLE", "NOSCRIPT", "SVG", "IFRAME", "VIDEO"];
  const VIDEO_PATTERNS = [
    "视频号",
    "点击查看视频",
    "观看视频",
    "已关注",
    "看片可关注",
    "关注公众号"
  ];
  function shouldSkipElement$8(el) {
    if (SKIP_TAGS.includes(el.tagName)) {
      return true;
    }
    if (el.classList.contains("rich_media_meta") || el.classList.contains("rich_media_tool") || el.classList.contains("qr_code_pc") || el.classList.contains("profile_container") || el.classList.contains("video_iframe") || el.classList.contains("mpvideo") || el.classList.contains("js_mpvideo") || el.classList.contains("weapp_display_element") || el.id === "js_profile_qrcode" || el.getAttribute("data-miniprogram-type") || el.getAttribute("data-itemshowtype") === "video") {
      return true;
    }
    return false;
  }
  function isVideoRelatedText(text) {
    if (VIDEO_PATTERNS.some((pattern) => text.includes(pattern))) {
      return true;
    }
    if (text === "关注") return true;
    if (/视频\s*[:：]/.test(text)) return true;
    if (/点击.*播放/.test(text)) return true;
    if (/^[\s\S]*👇[\s\S]*$/.test(text)) return true;
    return false;
  }
  function splitLongParagraphByBr(el, minLength = 300) {
    var _a;
    const text = ((_a = el.textContent) == null ? void 0 : _a.trim()) || "";
    if (text.length < minLength) return [el];
    let target = el;
    let depth = 0;
    while (depth < 3) {
      const hasBrChild = Array.from(target.childNodes).some(
        (n) => n.nodeType === Node.ELEMENT_NODE && n.tagName === "BR"
      );
      if (hasBrChild) break;
      if (target.children.length === 1) {
        target = target.children[0];
        depth++;
      } else {
        break;
      }
    }
    const hasBr = Array.from(target.childNodes).some(
      (n) => n.nodeType === Node.ELEMENT_NODE && n.tagName === "BR"
    );
    if (!hasBr) return [el];
    const groups = [[]];
    for (const child of Array.from(target.childNodes)) {
      if (child.nodeType === Node.ELEMENT_NODE && child.tagName === "BR") {
        if (groups[groups.length - 1].length > 0) {
          groups.push([]);
        }
        continue;
      }
      groups[groups.length - 1].push(child);
    }
    const result = [];
    for (const group of groups) {
      const groupText = group.map((n) => n.textContent || "").join("").trim();
      if (groupText.length < 2) continue;
      if (group.length === 1 && group[0].nodeType === Node.ELEMENT_NODE) {
        result.push(group[0]);
        continue;
      }
      const meaningful = group.filter(
        (n) => {
          var _a2;
          return n.nodeType === Node.ELEMENT_NODE || (((_a2 = n.textContent) == null ? void 0 : _a2.trim()) || "").length > 0;
        }
      );
      if (meaningful.length === 1 && meaningful[0].nodeType === Node.ELEMENT_NODE) {
        result.push(meaningful[0]);
        continue;
      }
      const wrapper = document.createElement("span");
      wrapper.setAttribute("data-cr-split", "true");
      target.insertBefore(wrapper, group[0]);
      for (const node of group) {
        wrapper.appendChild(node);
      }
      result.push(wrapper);
    }
    return result.length > 1 ? result : [el];
  }
  function extractFromElement(element) {
    const paragraphs = [];
    const extractParagraphs = (node) => {
      var _a, _b, _c;
      if (node.nodeType === Node.TEXT_NODE) {
        const text = (_a = node.textContent) == null ? void 0 : _a.trim();
        if (text) {
          return text;
        }
        return "";
      }
      if (node.nodeType !== Node.ELEMENT_NODE) {
        return "";
      }
      const el = node;
      if (shouldSkipElement$8(el)) {
        return "";
      }
      const textContent = ((_b = el.textContent) == null ? void 0 : _b.trim()) || "";
      if (isVideoRelatedText(textContent)) {
        return "";
      }
      if (["P", "DIV", "SECTION"].includes(el.tagName)) {
        const text = Array.from(el.childNodes).map((child) => extractParagraphs(child)).join("").trim();
        if (text) {
          if (text.length > 300 && text.includes("\n")) {
            const subParagraphs = text.split(/\n+/).map((s) => s.trim()).filter((s) => s.length > 0);
            paragraphs.push(...subParagraphs);
          } else {
            paragraphs.push(text);
          }
        }
        return "";
      }
      if (/^H[1-6]$/.test(el.tagName)) {
        const text = (_c = el.textContent) == null ? void 0 : _c.trim();
        if (text) {
          paragraphs.push(text);
        }
        return "";
      }
      if (el.tagName === "BR") {
        return "\n";
      }
      return Array.from(el.childNodes).map((child) => extractParagraphs(child)).join("");
    };
    extractParagraphs(element);
    return paragraphs.join("\n\n");
  }
  const weixinExtractor = {
    siteName: "微信公众号",
    matches: ["mp.weixin.qq.com"],
    /**
     * 微信公众号完全支持高亮
     */
    supportsHighlight() {
      return true;
    },
    extractText() {
      const richMedia = document.querySelector("#js_content, .rich_media_content");
      if (richMedia) {
        return extractFromElement(richMedia);
      }
      return null;
    },
    extractTitle() {
      var _a;
      const titleEl = document.querySelector("#activity-name, .rich_media_title");
      if (titleEl) {
        return ((_a = titleEl.textContent) == null ? void 0 : _a.trim()) || null;
      }
      return document.title || null;
    },
    extractLanguage() {
      const htmlLang = document.documentElement.lang;
      if (htmlLang && htmlLang.startsWith("en")) {
        return "en";
      }
      return "zh";
    },
    /**
     * 提取段落及其 DOM 元素引用（用于直接在原文上高亮）
     */
    extractParagraphsWithElements() {
      var _a;
      console.log("[weixin] 开始提取段落和元素引用...");
      const result = [];
      const richMedia = document.querySelector("#js_content, .rich_media_content");
      if (!richMedia) {
        console.log("[weixin] 未找到正文容器");
        return result;
      }
      console.log("[weixin] 找到正文容器:", richMedia.tagName, richMedia.className);
      const logDomStructure = (el, depth, prefix) => {
        var _a2;
        if (depth > 2) return;
        const text = ((_a2 = el.textContent) == null ? void 0 : _a2.trim()) || "";
        const childCount = el.children.length;
        const childTags = Array.from(el.children).map((c) => c.tagName).join(", ");
        console.log(`[weixin-dom] ${prefix}<${el.tagName}> children=${childCount} textLen=${text.length} childTags=[${childTags}]`);
        if (depth < 2) {
          Array.from(el.children).slice(0, 10).forEach((child, i) => {
            logDomStructure(child, depth + 1, prefix + "  ");
          });
          if (el.children.length > 10) {
            console.log(`[weixin-dom] ${prefix}  ... and ${el.children.length - 10} more children`);
          }
        }
      };
      logDomStructure(richMedia, 0, "");
      const isLeafParagraph = (el) => {
        if (el.children.length === 0) {
          return true;
        }
        return !el.querySelector("p, div, section, h1, h2, h3, h4, h5, h6, ul, ol, li, blockquote");
      };
      const extractParagraphElements = (container) => {
        const paragraphElements2 = [];
        const traverse = (el) => {
          var _a2;
          const skipTags = ["SCRIPT", "STYLE", "NOSCRIPT", "SVG", "IFRAME", "IMG", "VIDEO", "AUDIO", "CANVAS"];
          if (skipTags.includes(el.tagName)) {
            return;
          }
          if (shouldSkipElement$8(el)) {
            return;
          }
          const text = ((_a2 = el.textContent) == null ? void 0 : _a2.trim()) || "";
          if (isVideoRelatedText(text)) {
            return;
          }
          if (["P", "H1", "H2", "H3", "H4", "H5", "H6"].includes(el.tagName)) {
            if (text.length > 0) {
              const splits = splitLongParagraphByBr(el);
              paragraphElements2.push(...splits);
              if (splits.length > 1) {
                console.log("[weixin] 超长段落 (P/H) 拆分为", splits.length, "个子段落:", el.tagName, text.substring(0, 40));
              } else {
                console.log("[weixin] 找到段落 (P/H):", el.tagName, text.substring(0, 40));
              }
            }
            return;
          }
          if (text.length < 10) {
            for (const child of Array.from(el.children)) {
              traverse(child);
            }
            return;
          }
          if (["SECTION", "DIV", "SPAN"].includes(el.tagName)) {
            if (isLeafParagraph(el)) {
              const splits = splitLongParagraphByBr(el);
              paragraphElements2.push(...splits);
              if (splits.length > 1) {
                console.log("[weixin] 超长叶子段落拆分为", splits.length, "个子段落:", el.tagName, text.substring(0, 40));
              } else {
                console.log("[weixin] 找到段落 (叶子):", el.tagName, text.substring(0, 40));
              }
              return;
            }
            const children = Array.from(el.children);
            const maxChildTextLen = Math.max(
              0,
              ...children.map((c) => {
                var _a3;
                return ((_a3 = c.textContent) == null ? void 0 : _a3.trim().length) || 0;
              })
            );
            const hasSemanticChildren = children.some((c) => /^(P|H[1-6])$/.test(c.tagName));
            if (maxChildTextLen < 10 && !hasSemanticChildren && text.length <= 500) {
              paragraphElements2.push(el);
              console.log("[weixin] 找到段落 (碎片文本):", el.tagName, text.substring(0, 40));
              return;
            }
          }
          for (const child of Array.from(el.children)) {
            traverse(child);
          }
        };
        traverse(container);
        return paragraphElements2;
      };
      const paragraphElements = extractParagraphElements(richMedia);
      console.log("[weixin] 找到段落元素数:", paragraphElements.length);
      const seenTexts = /* @__PURE__ */ new Set();
      for (const el of paragraphElements) {
        const text = (_a = el.textContent) == null ? void 0 : _a.trim();
        if (text) {
          const textKey = text.substring(0, 100);
          if (seenTexts.has(textKey)) {
            console.log("[weixin] 跳过重复段落:", text.substring(0, 30));
            continue;
          }
          seenTexts.add(textKey);
          result.push({
            text,
            element: el,
            canHighlight: true
            // 微信公众号支持高亮
          });
          console.log("[weixin] 段落", result.length, ":", text.substring(0, 50));
        }
      }
      console.log("[weixin] 最终提取段落数:", result.length);
      return result;
    }
  };
  var Readability = { exports: {} };
  var hasRequiredReadability$1;
  function requireReadability$1() {
    if (hasRequiredReadability$1) return Readability.exports;
    hasRequiredReadability$1 = 1;
    (function(module) {
      function Readability2(doc, options) {
        if (options && options.documentElement) {
          doc = options;
          options = arguments[2];
        } else if (!doc || !doc.documentElement) {
          throw new Error(
            "First argument to Readability constructor should be a document object."
          );
        }
        options = options || {};
        this._doc = doc;
        this._docJSDOMParser = this._doc.firstChild.__JSDOMParser__;
        this._articleTitle = null;
        this._articleByline = null;
        this._articleDir = null;
        this._articleSiteName = null;
        this._attempts = [];
        this._metadata = {};
        this._debug = !!options.debug;
        this._maxElemsToParse = options.maxElemsToParse || this.DEFAULT_MAX_ELEMS_TO_PARSE;
        this._nbTopCandidates = options.nbTopCandidates || this.DEFAULT_N_TOP_CANDIDATES;
        this._charThreshold = options.charThreshold || this.DEFAULT_CHAR_THRESHOLD;
        this._classesToPreserve = this.CLASSES_TO_PRESERVE.concat(
          options.classesToPreserve || []
        );
        this._keepClasses = !!options.keepClasses;
        this._serializer = options.serializer || function(el) {
          return el.innerHTML;
        };
        this._disableJSONLD = !!options.disableJSONLD;
        this._allowedVideoRegex = options.allowedVideoRegex || this.REGEXPS.videos;
        this._linkDensityModifier = options.linkDensityModifier || 0;
        this._flags = this.FLAG_STRIP_UNLIKELYS | this.FLAG_WEIGHT_CLASSES | this.FLAG_CLEAN_CONDITIONALLY;
        if (this._debug) {
          let logNode = function(node) {
            if (node.nodeType == node.TEXT_NODE) {
              return `${node.nodeName} ("${node.textContent}")`;
            }
            let attrPairs = Array.from(node.attributes || [], function(attr) {
              return `${attr.name}="${attr.value}"`;
            }).join(" ");
            return `<${node.localName} ${attrPairs}>`;
          };
          this.log = function() {
            if (typeof console !== "undefined") {
              let args = Array.from(arguments, (arg) => {
                if (arg && arg.nodeType == this.ELEMENT_NODE) {
                  return logNode(arg);
                }
                return arg;
              });
              args.unshift("Reader: (Readability)");
              console.log(...args);
            } else if (typeof dump !== "undefined") {
              var msg = Array.prototype.map.call(arguments, function(x) {
                return x && x.nodeName ? logNode(x) : x;
              }).join(" ");
              dump("Reader: (Readability) " + msg + "\n");
            }
          };
        } else {
          this.log = function() {
          };
        }
      }
      Readability2.prototype = {
        FLAG_STRIP_UNLIKELYS: 1,
        FLAG_WEIGHT_CLASSES: 2,
        FLAG_CLEAN_CONDITIONALLY: 4,
        // https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeType
        ELEMENT_NODE: 1,
        TEXT_NODE: 3,
        // Max number of nodes supported by this parser. Default: 0 (no limit)
        DEFAULT_MAX_ELEMS_TO_PARSE: 0,
        // The number of top candidates to consider when analysing how
        // tight the competition is among candidates.
        DEFAULT_N_TOP_CANDIDATES: 5,
        // Element tags to score by default.
        DEFAULT_TAGS_TO_SCORE: "section,h2,h3,h4,h5,h6,p,td,pre".toUpperCase().split(","),
        // The default number of chars an article must have in order to return a result
        DEFAULT_CHAR_THRESHOLD: 500,
        // All of the regular expressions in use within readability.
        // Defined up here so we don't instantiate them repeatedly in loops.
        REGEXPS: {
          // NOTE: These two regular expressions are duplicated in
          // Readability-readerable.js. Please keep both copies in sync.
          unlikelyCandidates: /-ad-|ai2html|banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|footer|gdpr|header|legends|menu|related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|ad-break|agegate|pagination|pager|popup|yom-remote/i,
          okMaybeItsACandidate: /and|article|body|column|content|main|shadow/i,
          positive: /article|body|content|entry|hentry|h-entry|main|page|pagination|post|text|blog|story/i,
          negative: /-ad-|hidden|^hid$| hid$| hid |^hid |banner|combx|comment|com-|contact|footer|gdpr|masthead|media|meta|outbrain|promo|related|scroll|share|shoutbox|sidebar|skyscraper|sponsor|shopping|tags|widget/i,
          extraneous: /print|archive|comment|discuss|e[\-]?mail|share|reply|all|login|sign|single|utility/i,
          byline: /byline|author|dateline|writtenby|p-author/i,
          replaceFonts: /<(\/?)font[^>]*>/gi,
          normalize: /\s{2,}/g,
          videos: /\/\/(www\.)?((dailymotion|youtube|youtube-nocookie|player\.vimeo|v\.qq)\.com|(archive|upload\.wikimedia)\.org|player\.twitch\.tv)/i,
          shareElements: /(\b|_)(share|sharedaddy)(\b|_)/i,
          nextLink: /(next|weiter|continue|>([^\|]|$)|»([^\|]|$))/i,
          prevLink: /(prev|earl|old|new|<|«)/i,
          tokenize: /\W+/g,
          whitespace: /^\s*$/,
          hasContent: /\S$/,
          hashUrl: /^#.+/,
          srcsetUrl: /(\S+)(\s+[\d.]+[xw])?(\s*(?:,|$))/g,
          b64DataUrl: /^data:\s*([^\s;,]+)\s*;\s*base64\s*,/i,
          // Commas as used in Latin, Sindhi, Chinese and various other scripts.
          // see: https://en.wikipedia.org/wiki/Comma#Comma_variants
          commas: /\u002C|\u060C|\uFE50|\uFE10|\uFE11|\u2E41|\u2E34|\u2E32|\uFF0C/g,
          // See: https://schema.org/Article
          jsonLdArticleTypes: /^Article|AdvertiserContentArticle|NewsArticle|AnalysisNewsArticle|AskPublicNewsArticle|BackgroundNewsArticle|OpinionNewsArticle|ReportageNewsArticle|ReviewNewsArticle|Report|SatiricalArticle|ScholarlyArticle|MedicalScholarlyArticle|SocialMediaPosting|BlogPosting|LiveBlogPosting|DiscussionForumPosting|TechArticle|APIReference$/,
          // used to see if a node's content matches words commonly used for ad blocks or loading indicators
          adWords: /^(ad(vertising|vertisement)?|pub(licité)?|werb(ung)?|广告|Реклама|Anuncio)$/iu,
          loadingWords: /^((loading|正在加载|Загрузка|chargement|cargando)(…|\.\.\.)?)$/iu
        },
        UNLIKELY_ROLES: [
          "menu",
          "menubar",
          "complementary",
          "navigation",
          "alert",
          "alertdialog",
          "dialog"
        ],
        DIV_TO_P_ELEMS: /* @__PURE__ */ new Set([
          "BLOCKQUOTE",
          "DL",
          "DIV",
          "IMG",
          "OL",
          "P",
          "PRE",
          "TABLE",
          "UL"
        ]),
        ALTER_TO_DIV_EXCEPTIONS: ["DIV", "ARTICLE", "SECTION", "P", "OL", "UL"],
        PRESENTATIONAL_ATTRIBUTES: [
          "align",
          "background",
          "bgcolor",
          "border",
          "cellpadding",
          "cellspacing",
          "frame",
          "hspace",
          "rules",
          "style",
          "valign",
          "vspace"
        ],
        DEPRECATED_SIZE_ATTRIBUTE_ELEMS: ["TABLE", "TH", "TD", "HR", "PRE"],
        // The commented out elements qualify as phrasing content but tend to be
        // removed by readability when put into paragraphs, so we ignore them here.
        PHRASING_ELEMS: [
          // "CANVAS", "IFRAME", "SVG", "VIDEO",
          "ABBR",
          "AUDIO",
          "B",
          "BDO",
          "BR",
          "BUTTON",
          "CITE",
          "CODE",
          "DATA",
          "DATALIST",
          "DFN",
          "EM",
          "EMBED",
          "I",
          "IMG",
          "INPUT",
          "KBD",
          "LABEL",
          "MARK",
          "MATH",
          "METER",
          "NOSCRIPT",
          "OBJECT",
          "OUTPUT",
          "PROGRESS",
          "Q",
          "RUBY",
          "SAMP",
          "SCRIPT",
          "SELECT",
          "SMALL",
          "SPAN",
          "STRONG",
          "SUB",
          "SUP",
          "TEXTAREA",
          "TIME",
          "VAR",
          "WBR"
        ],
        // These are the classes that readability sets itself.
        CLASSES_TO_PRESERVE: ["page"],
        // These are the list of HTML entities that need to be escaped.
        HTML_ESCAPE_MAP: {
          lt: "<",
          gt: ">",
          amp: "&",
          quot: '"',
          apos: "'"
        },
        /**
         * Run any post-process modifications to article content as necessary.
         *
         * @param Element
         * @return void
         **/
        _postProcessContent(articleContent) {
          this._fixRelativeUris(articleContent);
          this._simplifyNestedElements(articleContent);
          if (!this._keepClasses) {
            this._cleanClasses(articleContent);
          }
        },
        /**
         * Iterates over a NodeList, calls `filterFn` for each node and removes node
         * if function returned `true`.
         *
         * If function is not passed, removes all the nodes in node list.
         *
         * @param NodeList nodeList The nodes to operate on
         * @param Function filterFn the function to use as a filter
         * @return void
         */
        _removeNodes(nodeList, filterFn) {
          if (this._docJSDOMParser && nodeList._isLiveNodeList) {
            throw new Error("Do not pass live node lists to _removeNodes");
          }
          for (var i = nodeList.length - 1; i >= 0; i--) {
            var node = nodeList[i];
            var parentNode = node.parentNode;
            if (parentNode) {
              if (!filterFn || filterFn.call(this, node, i, nodeList)) {
                parentNode.removeChild(node);
              }
            }
          }
        },
        /**
         * Iterates over a NodeList, and calls _setNodeTag for each node.
         *
         * @param NodeList nodeList The nodes to operate on
         * @param String newTagName the new tag name to use
         * @return void
         */
        _replaceNodeTags(nodeList, newTagName) {
          if (this._docJSDOMParser && nodeList._isLiveNodeList) {
            throw new Error("Do not pass live node lists to _replaceNodeTags");
          }
          for (const node of nodeList) {
            this._setNodeTag(node, newTagName);
          }
        },
        /**
         * Iterate over a NodeList, which doesn't natively fully implement the Array
         * interface.
         *
         * For convenience, the current object context is applied to the provided
         * iterate function.
         *
         * @param  NodeList nodeList The NodeList.
         * @param  Function fn       The iterate function.
         * @return void
         */
        _forEachNode(nodeList, fn) {
          Array.prototype.forEach.call(nodeList, fn, this);
        },
        /**
         * Iterate over a NodeList, and return the first node that passes
         * the supplied test function
         *
         * For convenience, the current object context is applied to the provided
         * test function.
         *
         * @param  NodeList nodeList The NodeList.
         * @param  Function fn       The test function.
         * @return void
         */
        _findNode(nodeList, fn) {
          return Array.prototype.find.call(nodeList, fn, this);
        },
        /**
         * Iterate over a NodeList, return true if any of the provided iterate
         * function calls returns true, false otherwise.
         *
         * For convenience, the current object context is applied to the
         * provided iterate function.
         *
         * @param  NodeList nodeList The NodeList.
         * @param  Function fn       The iterate function.
         * @return Boolean
         */
        _someNode(nodeList, fn) {
          return Array.prototype.some.call(nodeList, fn, this);
        },
        /**
         * Iterate over a NodeList, return true if all of the provided iterate
         * function calls return true, false otherwise.
         *
         * For convenience, the current object context is applied to the
         * provided iterate function.
         *
         * @param  NodeList nodeList The NodeList.
         * @param  Function fn       The iterate function.
         * @return Boolean
         */
        _everyNode(nodeList, fn) {
          return Array.prototype.every.call(nodeList, fn, this);
        },
        _getAllNodesWithTag(node, tagNames) {
          if (node.querySelectorAll) {
            return node.querySelectorAll(tagNames.join(","));
          }
          return [].concat.apply(
            [],
            tagNames.map(function(tag) {
              var collection = node.getElementsByTagName(tag);
              return Array.isArray(collection) ? collection : Array.from(collection);
            })
          );
        },
        /**
         * Removes the class="" attribute from every element in the given
         * subtree, except those that match CLASSES_TO_PRESERVE and
         * the classesToPreserve array from the options object.
         *
         * @param Element
         * @return void
         */
        _cleanClasses(node) {
          var classesToPreserve = this._classesToPreserve;
          var className = (node.getAttribute("class") || "").split(/\s+/).filter((cls) => classesToPreserve.includes(cls)).join(" ");
          if (className) {
            node.setAttribute("class", className);
          } else {
            node.removeAttribute("class");
          }
          for (node = node.firstElementChild; node; node = node.nextElementSibling) {
            this._cleanClasses(node);
          }
        },
        /**
         * Tests whether a string is a URL or not.
         *
         * @param {string} str The string to test
         * @return {boolean} true if str is a URL, false if not
         */
        _isUrl(str) {
          try {
            new URL(str);
            return true;
          } catch {
            return false;
          }
        },
        /**
         * Converts each <a> and <img> uri in the given element to an absolute URI,
         * ignoring #ref URIs.
         *
         * @param Element
         * @return void
         */
        _fixRelativeUris(articleContent) {
          var baseURI = this._doc.baseURI;
          var documentURI = this._doc.documentURI;
          function toAbsoluteURI(uri) {
            if (baseURI == documentURI && uri.charAt(0) == "#") {
              return uri;
            }
            try {
              return new URL(uri, baseURI).href;
            } catch (ex) {
            }
            return uri;
          }
          var links = this._getAllNodesWithTag(articleContent, ["a"]);
          this._forEachNode(links, function(link) {
            var href = link.getAttribute("href");
            if (href) {
              if (href.indexOf("javascript:") === 0) {
                if (link.childNodes.length === 1 && link.childNodes[0].nodeType === this.TEXT_NODE) {
                  var text = this._doc.createTextNode(link.textContent);
                  link.parentNode.replaceChild(text, link);
                } else {
                  var container = this._doc.createElement("span");
                  while (link.firstChild) {
                    container.appendChild(link.firstChild);
                  }
                  link.parentNode.replaceChild(container, link);
                }
              } else {
                link.setAttribute("href", toAbsoluteURI(href));
              }
            }
          });
          var medias = this._getAllNodesWithTag(articleContent, [
            "img",
            "picture",
            "figure",
            "video",
            "audio",
            "source"
          ]);
          this._forEachNode(medias, function(media) {
            var src = media.getAttribute("src");
            var poster = media.getAttribute("poster");
            var srcset = media.getAttribute("srcset");
            if (src) {
              media.setAttribute("src", toAbsoluteURI(src));
            }
            if (poster) {
              media.setAttribute("poster", toAbsoluteURI(poster));
            }
            if (srcset) {
              var newSrcset = srcset.replace(
                this.REGEXPS.srcsetUrl,
                function(_, p1, p2, p3) {
                  return toAbsoluteURI(p1) + (p2 || "") + p3;
                }
              );
              media.setAttribute("srcset", newSrcset);
            }
          });
        },
        _simplifyNestedElements(articleContent) {
          var node = articleContent;
          while (node) {
            if (node.parentNode && ["DIV", "SECTION"].includes(node.tagName) && !(node.id && node.id.startsWith("readability"))) {
              if (this._isElementWithoutContent(node)) {
                node = this._removeAndGetNext(node);
                continue;
              } else if (this._hasSingleTagInsideElement(node, "DIV") || this._hasSingleTagInsideElement(node, "SECTION")) {
                var child = node.children[0];
                for (var i = 0; i < node.attributes.length; i++) {
                  child.setAttributeNode(node.attributes[i].cloneNode());
                }
                node.parentNode.replaceChild(child, node);
                node = child;
                continue;
              }
            }
            node = this._getNextNode(node);
          }
        },
        /**
         * Get the article title as an H1.
         *
         * @return string
         **/
        _getArticleTitle() {
          var doc = this._doc;
          var curTitle = "";
          var origTitle = "";
          try {
            curTitle = origTitle = doc.title.trim();
            if (typeof curTitle !== "string") {
              curTitle = origTitle = this._getInnerText(
                doc.getElementsByTagName("title")[0]
              );
            }
          } catch (e) {
          }
          var titleHadHierarchicalSeparators = false;
          function wordCount(str) {
            return str.split(/\s+/).length;
          }
          if (/ [\|\-\\\/>»] /.test(curTitle)) {
            titleHadHierarchicalSeparators = / [\\\/>»] /.test(curTitle);
            let allSeparators = Array.from(origTitle.matchAll(/ [\|\-\\\/>»] /gi));
            curTitle = origTitle.substring(0, allSeparators.pop().index);
            if (wordCount(curTitle) < 3) {
              curTitle = origTitle.replace(/^[^\|\-\\\/>»]*[\|\-\\\/>»]/gi, "");
            }
          } else if (curTitle.includes(": ")) {
            var headings = this._getAllNodesWithTag(doc, ["h1", "h2"]);
            var trimmedTitle = curTitle.trim();
            var match = this._someNode(headings, function(heading) {
              return heading.textContent.trim() === trimmedTitle;
            });
            if (!match) {
              curTitle = origTitle.substring(origTitle.lastIndexOf(":") + 1);
              if (wordCount(curTitle) < 3) {
                curTitle = origTitle.substring(origTitle.indexOf(":") + 1);
              } else if (wordCount(origTitle.substr(0, origTitle.indexOf(":"))) > 5) {
                curTitle = origTitle;
              }
            }
          } else if (curTitle.length > 150 || curTitle.length < 15) {
            var hOnes = doc.getElementsByTagName("h1");
            if (hOnes.length === 1) {
              curTitle = this._getInnerText(hOnes[0]);
            }
          }
          curTitle = curTitle.trim().replace(this.REGEXPS.normalize, " ");
          var curTitleWordCount = wordCount(curTitle);
          if (curTitleWordCount <= 4 && (!titleHadHierarchicalSeparators || curTitleWordCount != wordCount(origTitle.replace(/[\|\-\\\/>»]+/g, "")) - 1)) {
            curTitle = origTitle;
          }
          return curTitle;
        },
        /**
         * Prepare the HTML document for readability to scrape it.
         * This includes things like stripping javascript, CSS, and handling terrible markup.
         *
         * @return void
         **/
        _prepDocument() {
          var doc = this._doc;
          this._removeNodes(this._getAllNodesWithTag(doc, ["style"]));
          if (doc.body) {
            this._replaceBrs(doc.body);
          }
          this._replaceNodeTags(this._getAllNodesWithTag(doc, ["font"]), "SPAN");
        },
        /**
         * Finds the next node, starting from the given node, and ignoring
         * whitespace in between. If the given node is an element, the same node is
         * returned.
         */
        _nextNode(node) {
          var next = node;
          while (next && next.nodeType != this.ELEMENT_NODE && this.REGEXPS.whitespace.test(next.textContent)) {
            next = next.nextSibling;
          }
          return next;
        },
        /**
         * Replaces 2 or more successive <br> elements with a single <p>.
         * Whitespace between <br> elements are ignored. For example:
         *   <div>foo<br>bar<br> <br><br>abc</div>
         * will become:
         *   <div>foo<br>bar<p>abc</p></div>
         */
        _replaceBrs(elem) {
          this._forEachNode(this._getAllNodesWithTag(elem, ["br"]), function(br) {
            var next = br.nextSibling;
            var replaced = false;
            while ((next = this._nextNode(next)) && next.tagName == "BR") {
              replaced = true;
              var brSibling = next.nextSibling;
              next.remove();
              next = brSibling;
            }
            if (replaced) {
              var p = this._doc.createElement("p");
              br.parentNode.replaceChild(p, br);
              next = p.nextSibling;
              while (next) {
                if (next.tagName == "BR") {
                  var nextElem = this._nextNode(next.nextSibling);
                  if (nextElem && nextElem.tagName == "BR") {
                    break;
                  }
                }
                if (!this._isPhrasingContent(next)) {
                  break;
                }
                var sibling = next.nextSibling;
                p.appendChild(next);
                next = sibling;
              }
              while (p.lastChild && this._isWhitespace(p.lastChild)) {
                p.lastChild.remove();
              }
              if (p.parentNode.tagName === "P") {
                this._setNodeTag(p.parentNode, "DIV");
              }
            }
          });
        },
        _setNodeTag(node, tag) {
          this.log("_setNodeTag", node, tag);
          if (this._docJSDOMParser) {
            node.localName = tag.toLowerCase();
            node.tagName = tag.toUpperCase();
            return node;
          }
          var replacement = node.ownerDocument.createElement(tag);
          while (node.firstChild) {
            replacement.appendChild(node.firstChild);
          }
          node.parentNode.replaceChild(replacement, node);
          if (node.readability) {
            replacement.readability = node.readability;
          }
          for (var i = 0; i < node.attributes.length; i++) {
            replacement.setAttributeNode(node.attributes[i].cloneNode());
          }
          return replacement;
        },
        /**
         * Prepare the article node for display. Clean out any inline styles,
         * iframes, forms, strip extraneous <p> tags, etc.
         *
         * @param Element
         * @return void
         **/
        _prepArticle(articleContent) {
          this._cleanStyles(articleContent);
          this._markDataTables(articleContent);
          this._fixLazyImages(articleContent);
          this._cleanConditionally(articleContent, "form");
          this._cleanConditionally(articleContent, "fieldset");
          this._clean(articleContent, "object");
          this._clean(articleContent, "embed");
          this._clean(articleContent, "footer");
          this._clean(articleContent, "link");
          this._clean(articleContent, "aside");
          var shareElementThreshold = this.DEFAULT_CHAR_THRESHOLD;
          this._forEachNode(articleContent.children, function(topCandidate) {
            this._cleanMatchedNodes(topCandidate, function(node, matchString) {
              return this.REGEXPS.shareElements.test(matchString) && node.textContent.length < shareElementThreshold;
            });
          });
          this._clean(articleContent, "iframe");
          this._clean(articleContent, "input");
          this._clean(articleContent, "textarea");
          this._clean(articleContent, "select");
          this._clean(articleContent, "button");
          this._cleanHeaders(articleContent);
          this._cleanConditionally(articleContent, "table");
          this._cleanConditionally(articleContent, "ul");
          this._cleanConditionally(articleContent, "div");
          this._replaceNodeTags(
            this._getAllNodesWithTag(articleContent, ["h1"]),
            "h2"
          );
          this._removeNodes(
            this._getAllNodesWithTag(articleContent, ["p"]),
            function(paragraph) {
              var contentElementCount = this._getAllNodesWithTag(paragraph, [
                "img",
                "embed",
                "object",
                "iframe"
              ]).length;
              return contentElementCount === 0 && !this._getInnerText(paragraph, false);
            }
          );
          this._forEachNode(
            this._getAllNodesWithTag(articleContent, ["br"]),
            function(br) {
              var next = this._nextNode(br.nextSibling);
              if (next && next.tagName == "P") {
                br.remove();
              }
            }
          );
          this._forEachNode(
            this._getAllNodesWithTag(articleContent, ["table"]),
            function(table) {
              var tbody = this._hasSingleTagInsideElement(table, "TBODY") ? table.firstElementChild : table;
              if (this._hasSingleTagInsideElement(tbody, "TR")) {
                var row = tbody.firstElementChild;
                if (this._hasSingleTagInsideElement(row, "TD")) {
                  var cell = row.firstElementChild;
                  cell = this._setNodeTag(
                    cell,
                    this._everyNode(cell.childNodes, this._isPhrasingContent) ? "P" : "DIV"
                  );
                  table.parentNode.replaceChild(cell, table);
                }
              }
            }
          );
        },
        /**
         * Initialize a node with the readability object. Also checks the
         * className/id for special names to add to its score.
         *
         * @param Element
         * @return void
         **/
        _initializeNode(node) {
          node.readability = { contentScore: 0 };
          switch (node.tagName) {
            case "DIV":
              node.readability.contentScore += 5;
              break;
            case "PRE":
            case "TD":
            case "BLOCKQUOTE":
              node.readability.contentScore += 3;
              break;
            case "ADDRESS":
            case "OL":
            case "UL":
            case "DL":
            case "DD":
            case "DT":
            case "LI":
            case "FORM":
              node.readability.contentScore -= 3;
              break;
            case "H1":
            case "H2":
            case "H3":
            case "H4":
            case "H5":
            case "H6":
            case "TH":
              node.readability.contentScore -= 5;
              break;
          }
          node.readability.contentScore += this._getClassWeight(node);
        },
        _removeAndGetNext(node) {
          var nextNode = this._getNextNode(node, true);
          node.remove();
          return nextNode;
        },
        /**
         * Traverse the DOM from node to node, starting at the node passed in.
         * Pass true for the second parameter to indicate this node itself
         * (and its kids) are going away, and we want the next node over.
         *
         * Calling this in a loop will traverse the DOM depth-first.
         *
         * @param {Element} node
         * @param {boolean} ignoreSelfAndKids
         * @return {Element}
         */
        _getNextNode(node, ignoreSelfAndKids) {
          if (!ignoreSelfAndKids && node.firstElementChild) {
            return node.firstElementChild;
          }
          if (node.nextElementSibling) {
            return node.nextElementSibling;
          }
          do {
            node = node.parentNode;
          } while (node && !node.nextElementSibling);
          return node && node.nextElementSibling;
        },
        // compares second text to first one
        // 1 = same text, 0 = completely different text
        // works the way that it splits both texts into words and then finds words that are unique in second text
        // the result is given by the lower length of unique parts
        _textSimilarity(textA, textB) {
          var tokensA = textA.toLowerCase().split(this.REGEXPS.tokenize).filter(Boolean);
          var tokensB = textB.toLowerCase().split(this.REGEXPS.tokenize).filter(Boolean);
          if (!tokensA.length || !tokensB.length) {
            return 0;
          }
          var uniqTokensB = tokensB.filter((token) => !tokensA.includes(token));
          var distanceB = uniqTokensB.join(" ").length / tokensB.join(" ").length;
          return 1 - distanceB;
        },
        /**
         * Checks whether an element node contains a valid byline
         *
         * @param node {Element}
         * @param matchString {string}
         * @return boolean
         */
        _isValidByline(node, matchString) {
          var rel = node.getAttribute("rel");
          var itemprop = node.getAttribute("itemprop");
          var bylineLength = node.textContent.trim().length;
          return (rel === "author" || itemprop && itemprop.includes("author") || this.REGEXPS.byline.test(matchString)) && !!bylineLength && bylineLength < 100;
        },
        _getNodeAncestors(node, maxDepth) {
          maxDepth = maxDepth || 0;
          var i = 0, ancestors = [];
          while (node.parentNode) {
            ancestors.push(node.parentNode);
            if (maxDepth && ++i === maxDepth) {
              break;
            }
            node = node.parentNode;
          }
          return ancestors;
        },
        /***
         * grabArticle - Using a variety of metrics (content score, classname, element types), find the content that is
         *         most likely to be the stuff a user wants to read. Then return it wrapped up in a div.
         *
         * @param page a document to run upon. Needs to be a full document, complete with body.
         * @return Element
         **/
        /* eslint-disable-next-line complexity */
        _grabArticle(page) {
          this.log("**** grabArticle ****");
          var doc = this._doc;
          var isPaging = page !== null;
          page = page ? page : this._doc.body;
          if (!page) {
            this.log("No body found in document. Abort.");
            return null;
          }
          var pageCacheHtml = page.innerHTML;
          while (true) {
            this.log("Starting grabArticle loop");
            var stripUnlikelyCandidates = this._flagIsActive(
              this.FLAG_STRIP_UNLIKELYS
            );
            var elementsToScore = [];
            var node = this._doc.documentElement;
            let shouldRemoveTitleHeader = true;
            while (node) {
              if (node.tagName === "HTML") {
                this._articleLang = node.getAttribute("lang");
              }
              var matchString = node.className + " " + node.id;
              if (!this._isProbablyVisible(node)) {
                this.log("Removing hidden node - " + matchString);
                node = this._removeAndGetNext(node);
                continue;
              }
              if (node.getAttribute("aria-modal") == "true" && node.getAttribute("role") == "dialog") {
                node = this._removeAndGetNext(node);
                continue;
              }
              if (!this._articleByline && !this._metadata.byline && this._isValidByline(node, matchString)) {
                var endOfSearchMarkerNode = this._getNextNode(node, true);
                var next = this._getNextNode(node);
                var itemPropNameNode = null;
                while (next && next != endOfSearchMarkerNode) {
                  var itemprop = next.getAttribute("itemprop");
                  if (itemprop && itemprop.includes("name")) {
                    itemPropNameNode = next;
                    break;
                  } else {
                    next = this._getNextNode(next);
                  }
                }
                this._articleByline = (itemPropNameNode ?? node).textContent.trim();
                node = this._removeAndGetNext(node);
                continue;
              }
              if (shouldRemoveTitleHeader && this._headerDuplicatesTitle(node)) {
                this.log(
                  "Removing header: ",
                  node.textContent.trim(),
                  this._articleTitle.trim()
                );
                shouldRemoveTitleHeader = false;
                node = this._removeAndGetNext(node);
                continue;
              }
              if (stripUnlikelyCandidates) {
                if (this.REGEXPS.unlikelyCandidates.test(matchString) && !this.REGEXPS.okMaybeItsACandidate.test(matchString) && !this._hasAncestorTag(node, "table") && !this._hasAncestorTag(node, "code") && node.tagName !== "BODY" && node.tagName !== "A") {
                  this.log("Removing unlikely candidate - " + matchString);
                  node = this._removeAndGetNext(node);
                  continue;
                }
                if (this.UNLIKELY_ROLES.includes(node.getAttribute("role"))) {
                  this.log(
                    "Removing content with role " + node.getAttribute("role") + " - " + matchString
                  );
                  node = this._removeAndGetNext(node);
                  continue;
                }
              }
              if ((node.tagName === "DIV" || node.tagName === "SECTION" || node.tagName === "HEADER" || node.tagName === "H1" || node.tagName === "H2" || node.tagName === "H3" || node.tagName === "H4" || node.tagName === "H5" || node.tagName === "H6") && this._isElementWithoutContent(node)) {
                node = this._removeAndGetNext(node);
                continue;
              }
              if (this.DEFAULT_TAGS_TO_SCORE.includes(node.tagName)) {
                elementsToScore.push(node);
              }
              if (node.tagName === "DIV") {
                var p = null;
                var childNode = node.firstChild;
                while (childNode) {
                  var nextSibling = childNode.nextSibling;
                  if (this._isPhrasingContent(childNode)) {
                    if (p !== null) {
                      p.appendChild(childNode);
                    } else if (!this._isWhitespace(childNode)) {
                      p = doc.createElement("p");
                      node.replaceChild(p, childNode);
                      p.appendChild(childNode);
                    }
                  } else if (p !== null) {
                    while (p.lastChild && this._isWhitespace(p.lastChild)) {
                      p.lastChild.remove();
                    }
                    p = null;
                  }
                  childNode = nextSibling;
                }
                if (this._hasSingleTagInsideElement(node, "P") && this._getLinkDensity(node) < 0.25) {
                  var newNode = node.children[0];
                  node.parentNode.replaceChild(newNode, node);
                  node = newNode;
                  elementsToScore.push(node);
                } else if (!this._hasChildBlockElement(node)) {
                  node = this._setNodeTag(node, "P");
                  elementsToScore.push(node);
                }
              }
              node = this._getNextNode(node);
            }
            var candidates = [];
            this._forEachNode(elementsToScore, function(elementToScore) {
              if (!elementToScore.parentNode || typeof elementToScore.parentNode.tagName === "undefined") {
                return;
              }
              var innerText = this._getInnerText(elementToScore);
              if (innerText.length < 25) {
                return;
              }
              var ancestors2 = this._getNodeAncestors(elementToScore, 5);
              if (ancestors2.length === 0) {
                return;
              }
              var contentScore = 0;
              contentScore += 1;
              contentScore += innerText.split(this.REGEXPS.commas).length;
              contentScore += Math.min(Math.floor(innerText.length / 100), 3);
              this._forEachNode(ancestors2, function(ancestor, level) {
                if (!ancestor.tagName || !ancestor.parentNode || typeof ancestor.parentNode.tagName === "undefined") {
                  return;
                }
                if (typeof ancestor.readability === "undefined") {
                  this._initializeNode(ancestor);
                  candidates.push(ancestor);
                }
                if (level === 0) {
                  var scoreDivider = 1;
                } else if (level === 1) {
                  scoreDivider = 2;
                } else {
                  scoreDivider = level * 3;
                }
                ancestor.readability.contentScore += contentScore / scoreDivider;
              });
            });
            var topCandidates = [];
            for (var c = 0, cl = candidates.length; c < cl; c += 1) {
              var candidate = candidates[c];
              var candidateScore = candidate.readability.contentScore * (1 - this._getLinkDensity(candidate));
              candidate.readability.contentScore = candidateScore;
              this.log("Candidate:", candidate, "with score " + candidateScore);
              for (var t = 0; t < this._nbTopCandidates; t++) {
                var aTopCandidate = topCandidates[t];
                if (!aTopCandidate || candidateScore > aTopCandidate.readability.contentScore) {
                  topCandidates.splice(t, 0, candidate);
                  if (topCandidates.length > this._nbTopCandidates) {
                    topCandidates.pop();
                  }
                  break;
                }
              }
            }
            var topCandidate = topCandidates[0] || null;
            var neededToCreateTopCandidate = false;
            var parentOfTopCandidate;
            if (topCandidate === null || topCandidate.tagName === "BODY") {
              topCandidate = doc.createElement("DIV");
              neededToCreateTopCandidate = true;
              while (page.firstChild) {
                this.log("Moving child out:", page.firstChild);
                topCandidate.appendChild(page.firstChild);
              }
              page.appendChild(topCandidate);
              this._initializeNode(topCandidate);
            } else if (topCandidate) {
              var alternativeCandidateAncestors = [];
              for (var i = 1; i < topCandidates.length; i++) {
                if (topCandidates[i].readability.contentScore / topCandidate.readability.contentScore >= 0.75) {
                  alternativeCandidateAncestors.push(
                    this._getNodeAncestors(topCandidates[i])
                  );
                }
              }
              var MINIMUM_TOPCANDIDATES = 3;
              if (alternativeCandidateAncestors.length >= MINIMUM_TOPCANDIDATES) {
                parentOfTopCandidate = topCandidate.parentNode;
                while (parentOfTopCandidate.tagName !== "BODY") {
                  var listsContainingThisAncestor = 0;
                  for (var ancestorIndex = 0; ancestorIndex < alternativeCandidateAncestors.length && listsContainingThisAncestor < MINIMUM_TOPCANDIDATES; ancestorIndex++) {
                    listsContainingThisAncestor += Number(
                      alternativeCandidateAncestors[ancestorIndex].includes(
                        parentOfTopCandidate
                      )
                    );
                  }
                  if (listsContainingThisAncestor >= MINIMUM_TOPCANDIDATES) {
                    topCandidate = parentOfTopCandidate;
                    break;
                  }
                  parentOfTopCandidate = parentOfTopCandidate.parentNode;
                }
              }
              if (!topCandidate.readability) {
                this._initializeNode(topCandidate);
              }
              parentOfTopCandidate = topCandidate.parentNode;
              var lastScore = topCandidate.readability.contentScore;
              var scoreThreshold = lastScore / 3;
              while (parentOfTopCandidate.tagName !== "BODY") {
                if (!parentOfTopCandidate.readability) {
                  parentOfTopCandidate = parentOfTopCandidate.parentNode;
                  continue;
                }
                var parentScore = parentOfTopCandidate.readability.contentScore;
                if (parentScore < scoreThreshold) {
                  break;
                }
                if (parentScore > lastScore) {
                  topCandidate = parentOfTopCandidate;
                  break;
                }
                lastScore = parentOfTopCandidate.readability.contentScore;
                parentOfTopCandidate = parentOfTopCandidate.parentNode;
              }
              parentOfTopCandidate = topCandidate.parentNode;
              while (parentOfTopCandidate.tagName != "BODY" && parentOfTopCandidate.children.length == 1) {
                topCandidate = parentOfTopCandidate;
                parentOfTopCandidate = topCandidate.parentNode;
              }
              if (!topCandidate.readability) {
                this._initializeNode(topCandidate);
              }
            }
            var articleContent = doc.createElement("DIV");
            if (isPaging) {
              articleContent.id = "readability-content";
            }
            var siblingScoreThreshold = Math.max(
              10,
              topCandidate.readability.contentScore * 0.2
            );
            parentOfTopCandidate = topCandidate.parentNode;
            var siblings = parentOfTopCandidate.children;
            for (var s = 0, sl = siblings.length; s < sl; s++) {
              var sibling = siblings[s];
              var append = false;
              this.log(
                "Looking at sibling node:",
                sibling,
                sibling.readability ? "with score " + sibling.readability.contentScore : ""
              );
              this.log(
                "Sibling has score",
                sibling.readability ? sibling.readability.contentScore : "Unknown"
              );
              if (sibling === topCandidate) {
                append = true;
              } else {
                var contentBonus = 0;
                if (sibling.className === topCandidate.className && topCandidate.className !== "") {
                  contentBonus += topCandidate.readability.contentScore * 0.2;
                }
                if (sibling.readability && sibling.readability.contentScore + contentBonus >= siblingScoreThreshold) {
                  append = true;
                } else if (sibling.nodeName === "P") {
                  var linkDensity2 = this._getLinkDensity(sibling);
                  var nodeContent = this._getInnerText(sibling);
                  var nodeLength = nodeContent.length;
                  if (nodeLength > 80 && linkDensity2 < 0.25) {
                    append = true;
                  } else if (nodeLength < 80 && nodeLength > 0 && linkDensity2 === 0 && nodeContent.search(/\.( |$)/) !== -1) {
                    append = true;
                  }
                }
              }
              if (append) {
                this.log("Appending node:", sibling);
                if (!this.ALTER_TO_DIV_EXCEPTIONS.includes(sibling.nodeName)) {
                  this.log("Altering sibling:", sibling, "to div.");
                  sibling = this._setNodeTag(sibling, "DIV");
                }
                articleContent.appendChild(sibling);
                siblings = parentOfTopCandidate.children;
                s -= 1;
                sl -= 1;
              }
            }
            if (this._debug) {
              this.log("Article content pre-prep: " + articleContent.innerHTML);
            }
            this._prepArticle(articleContent);
            if (this._debug) {
              this.log("Article content post-prep: " + articleContent.innerHTML);
            }
            if (neededToCreateTopCandidate) {
              topCandidate.id = "readability-page-1";
              topCandidate.className = "page";
            } else {
              var div = doc.createElement("DIV");
              div.id = "readability-page-1";
              div.className = "page";
              while (articleContent.firstChild) {
                div.appendChild(articleContent.firstChild);
              }
              articleContent.appendChild(div);
            }
            if (this._debug) {
              this.log("Article content after paging: " + articleContent.innerHTML);
            }
            var parseSuccessful = true;
            var textLength = this._getInnerText(articleContent, true).length;
            if (textLength < this._charThreshold) {
              parseSuccessful = false;
              page.innerHTML = pageCacheHtml;
              this._attempts.push({
                articleContent,
                textLength
              });
              if (this._flagIsActive(this.FLAG_STRIP_UNLIKELYS)) {
                this._removeFlag(this.FLAG_STRIP_UNLIKELYS);
              } else if (this._flagIsActive(this.FLAG_WEIGHT_CLASSES)) {
                this._removeFlag(this.FLAG_WEIGHT_CLASSES);
              } else if (this._flagIsActive(this.FLAG_CLEAN_CONDITIONALLY)) {
                this._removeFlag(this.FLAG_CLEAN_CONDITIONALLY);
              } else {
                this._attempts.sort(function(a, b) {
                  return b.textLength - a.textLength;
                });
                if (!this._attempts[0].textLength) {
                  return null;
                }
                articleContent = this._attempts[0].articleContent;
                parseSuccessful = true;
              }
            }
            if (parseSuccessful) {
              var ancestors = [parentOfTopCandidate, topCandidate].concat(
                this._getNodeAncestors(parentOfTopCandidate)
              );
              this._someNode(ancestors, function(ancestor) {
                if (!ancestor.tagName) {
                  return false;
                }
                var articleDir = ancestor.getAttribute("dir");
                if (articleDir) {
                  this._articleDir = articleDir;
                  return true;
                }
                return false;
              });
              return articleContent;
            }
          }
        },
        /**
         * Converts some of the common HTML entities in string to their corresponding characters.
         *
         * @param str {string} - a string to unescape.
         * @return string without HTML entity.
         */
        _unescapeHtmlEntities(str) {
          if (!str) {
            return str;
          }
          var htmlEscapeMap = this.HTML_ESCAPE_MAP;
          return str.replace(/&(quot|amp|apos|lt|gt);/g, function(_, tag) {
            return htmlEscapeMap[tag];
          }).replace(/&#(?:x([0-9a-f]+)|([0-9]+));/gi, function(_, hex, numStr) {
            var num = parseInt(hex || numStr, hex ? 16 : 10);
            if (num == 0 || num > 1114111 || num >= 55296 && num <= 57343) {
              num = 65533;
            }
            return String.fromCodePoint(num);
          });
        },
        /**
         * Try to extract metadata from JSON-LD object.
         * For now, only Schema.org objects of type Article or its subtypes are supported.
         * @return Object with any metadata that could be extracted (possibly none)
         */
        _getJSONLD(doc) {
          var scripts = this._getAllNodesWithTag(doc, ["script"]);
          var metadata;
          this._forEachNode(scripts, function(jsonLdElement) {
            if (!metadata && jsonLdElement.getAttribute("type") === "application/ld+json") {
              try {
                var content = jsonLdElement.textContent.replace(
                  /^\s*<!\[CDATA\[|\]\]>\s*$/g,
                  ""
                );
                var parsed = JSON.parse(content);
                if (Array.isArray(parsed)) {
                  parsed = parsed.find((it) => {
                    return it["@type"] && it["@type"].match(this.REGEXPS.jsonLdArticleTypes);
                  });
                  if (!parsed) {
                    return;
                  }
                }
                var schemaDotOrgRegex = /^https?\:\/\/schema\.org\/?$/;
                var matches = typeof parsed["@context"] === "string" && parsed["@context"].match(schemaDotOrgRegex) || typeof parsed["@context"] === "object" && typeof parsed["@context"]["@vocab"] == "string" && parsed["@context"]["@vocab"].match(schemaDotOrgRegex);
                if (!matches) {
                  return;
                }
                if (!parsed["@type"] && Array.isArray(parsed["@graph"])) {
                  parsed = parsed["@graph"].find((it) => {
                    return (it["@type"] || "").match(this.REGEXPS.jsonLdArticleTypes);
                  });
                }
                if (!parsed || !parsed["@type"] || !parsed["@type"].match(this.REGEXPS.jsonLdArticleTypes)) {
                  return;
                }
                metadata = {};
                if (typeof parsed.name === "string" && typeof parsed.headline === "string" && parsed.name !== parsed.headline) {
                  var title = this._getArticleTitle();
                  var nameMatches = this._textSimilarity(parsed.name, title) > 0.75;
                  var headlineMatches = this._textSimilarity(parsed.headline, title) > 0.75;
                  if (headlineMatches && !nameMatches) {
                    metadata.title = parsed.headline;
                  } else {
                    metadata.title = parsed.name;
                  }
                } else if (typeof parsed.name === "string") {
                  metadata.title = parsed.name.trim();
                } else if (typeof parsed.headline === "string") {
                  metadata.title = parsed.headline.trim();
                }
                if (parsed.author) {
                  if (typeof parsed.author.name === "string") {
                    metadata.byline = parsed.author.name.trim();
                  } else if (Array.isArray(parsed.author) && parsed.author[0] && typeof parsed.author[0].name === "string") {
                    metadata.byline = parsed.author.filter(function(author) {
                      return author && typeof author.name === "string";
                    }).map(function(author) {
                      return author.name.trim();
                    }).join(", ");
                  }
                }
                if (typeof parsed.description === "string") {
                  metadata.excerpt = parsed.description.trim();
                }
                if (parsed.publisher && typeof parsed.publisher.name === "string") {
                  metadata.siteName = parsed.publisher.name.trim();
                }
                if (typeof parsed.datePublished === "string") {
                  metadata.datePublished = parsed.datePublished.trim();
                }
              } catch (err) {
                this.log(err.message);
              }
            }
          });
          return metadata ? metadata : {};
        },
        /**
         * Attempts to get excerpt and byline metadata for the article.
         *
         * @param {Object} jsonld — object containing any metadata that
         * could be extracted from JSON-LD object.
         *
         * @return Object with optional "excerpt" and "byline" properties
         */
        _getArticleMetadata(jsonld) {
          var metadata = {};
          var values = {};
          var metaElements = this._doc.getElementsByTagName("meta");
          var propertyPattern = /\s*(article|dc|dcterm|og|twitter)\s*:\s*(author|creator|description|published_time|title|site_name)\s*/gi;
          var namePattern = /^\s*(?:(dc|dcterm|og|twitter|parsely|weibo:(article|webpage))\s*[-\.:]\s*)?(author|creator|pub-date|description|title|site_name)\s*$/i;
          this._forEachNode(metaElements, function(element) {
            var elementName = element.getAttribute("name");
            var elementProperty = element.getAttribute("property");
            var content = element.getAttribute("content");
            if (!content) {
              return;
            }
            var matches = null;
            var name = null;
            if (elementProperty) {
              matches = elementProperty.match(propertyPattern);
              if (matches) {
                name = matches[0].toLowerCase().replace(/\s/g, "");
                values[name] = content.trim();
              }
            }
            if (!matches && elementName && namePattern.test(elementName)) {
              name = elementName;
              if (content) {
                name = name.toLowerCase().replace(/\s/g, "").replace(/\./g, ":");
                values[name] = content.trim();
              }
            }
          });
          metadata.title = jsonld.title || values["dc:title"] || values["dcterm:title"] || values["og:title"] || values["weibo:article:title"] || values["weibo:webpage:title"] || values.title || values["twitter:title"] || values["parsely-title"];
          if (!metadata.title) {
            metadata.title = this._getArticleTitle();
          }
          const articleAuthor = typeof values["article:author"] === "string" && !this._isUrl(values["article:author"]) ? values["article:author"] : void 0;
          metadata.byline = jsonld.byline || values["dc:creator"] || values["dcterm:creator"] || values.author || values["parsely-author"] || articleAuthor;
          metadata.excerpt = jsonld.excerpt || values["dc:description"] || values["dcterm:description"] || values["og:description"] || values["weibo:article:description"] || values["weibo:webpage:description"] || values.description || values["twitter:description"];
          metadata.siteName = jsonld.siteName || values["og:site_name"];
          metadata.publishedTime = jsonld.datePublished || values["article:published_time"] || values["parsely-pub-date"] || null;
          metadata.title = this._unescapeHtmlEntities(metadata.title);
          metadata.byline = this._unescapeHtmlEntities(metadata.byline);
          metadata.excerpt = this._unescapeHtmlEntities(metadata.excerpt);
          metadata.siteName = this._unescapeHtmlEntities(metadata.siteName);
          metadata.publishedTime = this._unescapeHtmlEntities(metadata.publishedTime);
          return metadata;
        },
        /**
         * Check if node is image, or if node contains exactly only one image
         * whether as a direct child or as its descendants.
         *
         * @param Element
         **/
        _isSingleImage(node) {
          while (node) {
            if (node.tagName === "IMG") {
              return true;
            }
            if (node.children.length !== 1 || node.textContent.trim() !== "") {
              return false;
            }
            node = node.children[0];
          }
          return false;
        },
        /**
         * Find all <noscript> that are located after <img> nodes, and which contain only one
         * <img> element. Replace the first image with the image from inside the <noscript> tag,
         * and remove the <noscript> tag. This improves the quality of the images we use on
         * some sites (e.g. Medium).
         *
         * @param Element
         **/
        _unwrapNoscriptImages(doc) {
          var imgs = Array.from(doc.getElementsByTagName("img"));
          this._forEachNode(imgs, function(img) {
            for (var i = 0; i < img.attributes.length; i++) {
              var attr = img.attributes[i];
              switch (attr.name) {
                case "src":
                case "srcset":
                case "data-src":
                case "data-srcset":
                  return;
              }
              if (/\.(jpg|jpeg|png|webp)/i.test(attr.value)) {
                return;
              }
            }
            img.remove();
          });
          var noscripts = Array.from(doc.getElementsByTagName("noscript"));
          this._forEachNode(noscripts, function(noscript) {
            if (!this._isSingleImage(noscript)) {
              return;
            }
            var tmp = doc.createElement("div");
            tmp.innerHTML = noscript.innerHTML;
            var prevElement = noscript.previousElementSibling;
            if (prevElement && this._isSingleImage(prevElement)) {
              var prevImg = prevElement;
              if (prevImg.tagName !== "IMG") {
                prevImg = prevElement.getElementsByTagName("img")[0];
              }
              var newImg = tmp.getElementsByTagName("img")[0];
              for (var i = 0; i < prevImg.attributes.length; i++) {
                var attr = prevImg.attributes[i];
                if (attr.value === "") {
                  continue;
                }
                if (attr.name === "src" || attr.name === "srcset" || /\.(jpg|jpeg|png|webp)/i.test(attr.value)) {
                  if (newImg.getAttribute(attr.name) === attr.value) {
                    continue;
                  }
                  var attrName = attr.name;
                  if (newImg.hasAttribute(attrName)) {
                    attrName = "data-old-" + attrName;
                  }
                  newImg.setAttribute(attrName, attr.value);
                }
              }
              noscript.parentNode.replaceChild(tmp.firstElementChild, prevElement);
            }
          });
        },
        /**
         * Removes script tags from the document.
         *
         * @param Element
         **/
        _removeScripts(doc) {
          this._removeNodes(this._getAllNodesWithTag(doc, ["script", "noscript"]));
        },
        /**
         * Check if this node has only whitespace and a single element with given tag
         * Returns false if the DIV node contains non-empty text nodes
         * or if it contains no element with given tag or more than 1 element.
         *
         * @param Element
         * @param string tag of child element
         **/
        _hasSingleTagInsideElement(element, tag) {
          if (element.children.length != 1 || element.children[0].tagName !== tag) {
            return false;
          }
          return !this._someNode(element.childNodes, function(node) {
            return node.nodeType === this.TEXT_NODE && this.REGEXPS.hasContent.test(node.textContent);
          });
        },
        _isElementWithoutContent(node) {
          return node.nodeType === this.ELEMENT_NODE && !node.textContent.trim().length && (!node.children.length || node.children.length == node.getElementsByTagName("br").length + node.getElementsByTagName("hr").length);
        },
        /**
         * Determine whether element has any children block level elements.
         *
         * @param Element
         */
        _hasChildBlockElement(element) {
          return this._someNode(element.childNodes, function(node) {
            return this.DIV_TO_P_ELEMS.has(node.tagName) || this._hasChildBlockElement(node);
          });
        },
        /***
         * Determine if a node qualifies as phrasing content.
         * https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Content_categories#Phrasing_content
         **/
        _isPhrasingContent(node) {
          return node.nodeType === this.TEXT_NODE || this.PHRASING_ELEMS.includes(node.tagName) || (node.tagName === "A" || node.tagName === "DEL" || node.tagName === "INS") && this._everyNode(node.childNodes, this._isPhrasingContent);
        },
        _isWhitespace(node) {
          return node.nodeType === this.TEXT_NODE && node.textContent.trim().length === 0 || node.nodeType === this.ELEMENT_NODE && node.tagName === "BR";
        },
        /**
         * Get the inner text of a node - cross browser compatibly.
         * This also strips out any excess whitespace to be found.
         *
         * @param Element
         * @param Boolean normalizeSpaces (default: true)
         * @return string
         **/
        _getInnerText(e, normalizeSpaces) {
          normalizeSpaces = typeof normalizeSpaces === "undefined" ? true : normalizeSpaces;
          var textContent = e.textContent.trim();
          if (normalizeSpaces) {
            return textContent.replace(this.REGEXPS.normalize, " ");
          }
          return textContent;
        },
        /**
         * Get the number of times a string s appears in the node e.
         *
         * @param Element
         * @param string - what to split on. Default is ","
         * @return number (integer)
         **/
        _getCharCount(e, s) {
          s = s || ",";
          return this._getInnerText(e).split(s).length - 1;
        },
        /**
         * Remove the style attribute on every e and under.
         * TODO: Test if getElementsByTagName(*) is faster.
         *
         * @param Element
         * @return void
         **/
        _cleanStyles(e) {
          if (!e || e.tagName.toLowerCase() === "svg") {
            return;
          }
          for (var i = 0; i < this.PRESENTATIONAL_ATTRIBUTES.length; i++) {
            e.removeAttribute(this.PRESENTATIONAL_ATTRIBUTES[i]);
          }
          if (this.DEPRECATED_SIZE_ATTRIBUTE_ELEMS.includes(e.tagName)) {
            e.removeAttribute("width");
            e.removeAttribute("height");
          }
          var cur = e.firstElementChild;
          while (cur !== null) {
            this._cleanStyles(cur);
            cur = cur.nextElementSibling;
          }
        },
        /**
         * Get the density of links as a percentage of the content
         * This is the amount of text that is inside a link divided by the total text in the node.
         *
         * @param Element
         * @return number (float)
         **/
        _getLinkDensity(element) {
          var textLength = this._getInnerText(element).length;
          if (textLength === 0) {
            return 0;
          }
          var linkLength = 0;
          this._forEachNode(element.getElementsByTagName("a"), function(linkNode) {
            var href = linkNode.getAttribute("href");
            var coefficient = href && this.REGEXPS.hashUrl.test(href) ? 0.3 : 1;
            linkLength += this._getInnerText(linkNode).length * coefficient;
          });
          return linkLength / textLength;
        },
        /**
         * Get an elements class/id weight. Uses regular expressions to tell if this
         * element looks good or bad.
         *
         * @param Element
         * @return number (Integer)
         **/
        _getClassWeight(e) {
          if (!this._flagIsActive(this.FLAG_WEIGHT_CLASSES)) {
            return 0;
          }
          var weight = 0;
          if (typeof e.className === "string" && e.className !== "") {
            if (this.REGEXPS.negative.test(e.className)) {
              weight -= 25;
            }
            if (this.REGEXPS.positive.test(e.className)) {
              weight += 25;
            }
          }
          if (typeof e.id === "string" && e.id !== "") {
            if (this.REGEXPS.negative.test(e.id)) {
              weight -= 25;
            }
            if (this.REGEXPS.positive.test(e.id)) {
              weight += 25;
            }
          }
          return weight;
        },
        /**
         * Clean a node of all elements of type "tag".
         * (Unless it's a youtube/vimeo video. People love movies.)
         *
         * @param Element
         * @param string tag to clean
         * @return void
         **/
        _clean(e, tag) {
          var isEmbed = ["object", "embed", "iframe"].includes(tag);
          this._removeNodes(this._getAllNodesWithTag(e, [tag]), function(element) {
            if (isEmbed) {
              for (var i = 0; i < element.attributes.length; i++) {
                if (this._allowedVideoRegex.test(element.attributes[i].value)) {
                  return false;
                }
              }
              if (element.tagName === "object" && this._allowedVideoRegex.test(element.innerHTML)) {
                return false;
              }
            }
            return true;
          });
        },
        /**
         * Check if a given node has one of its ancestor tag name matching the
         * provided one.
         * @param  HTMLElement node
         * @param  String      tagName
         * @param  Number      maxDepth
         * @param  Function    filterFn a filter to invoke to determine whether this node 'counts'
         * @return Boolean
         */
        _hasAncestorTag(node, tagName, maxDepth, filterFn) {
          maxDepth = maxDepth || 3;
          tagName = tagName.toUpperCase();
          var depth = 0;
          while (node.parentNode) {
            if (maxDepth > 0 && depth > maxDepth) {
              return false;
            }
            if (node.parentNode.tagName === tagName && (!filterFn || filterFn(node.parentNode))) {
              return true;
            }
            node = node.parentNode;
            depth++;
          }
          return false;
        },
        /**
         * Return an object indicating how many rows and columns this table has.
         */
        _getRowAndColumnCount(table) {
          var rows = 0;
          var columns = 0;
          var trs = table.getElementsByTagName("tr");
          for (var i = 0; i < trs.length; i++) {
            var rowspan = trs[i].getAttribute("rowspan") || 0;
            if (rowspan) {
              rowspan = parseInt(rowspan, 10);
            }
            rows += rowspan || 1;
            var columnsInThisRow = 0;
            var cells = trs[i].getElementsByTagName("td");
            for (var j = 0; j < cells.length; j++) {
              var colspan = cells[j].getAttribute("colspan") || 0;
              if (colspan) {
                colspan = parseInt(colspan, 10);
              }
              columnsInThisRow += colspan || 1;
            }
            columns = Math.max(columns, columnsInThisRow);
          }
          return { rows, columns };
        },
        /**
         * Look for 'data' (as opposed to 'layout') tables, for which we use
         * similar checks as
         * https://searchfox.org/mozilla-central/rev/f82d5c549f046cb64ce5602bfd894b7ae807c8f8/accessible/generic/TableAccessible.cpp#19
         */
        _markDataTables(root) {
          var tables = root.getElementsByTagName("table");
          for (var i = 0; i < tables.length; i++) {
            var table = tables[i];
            var role = table.getAttribute("role");
            if (role == "presentation") {
              table._readabilityDataTable = false;
              continue;
            }
            var datatable = table.getAttribute("datatable");
            if (datatable == "0") {
              table._readabilityDataTable = false;
              continue;
            }
            var summary = table.getAttribute("summary");
            if (summary) {
              table._readabilityDataTable = true;
              continue;
            }
            var caption = table.getElementsByTagName("caption")[0];
            if (caption && caption.childNodes.length) {
              table._readabilityDataTable = true;
              continue;
            }
            var dataTableDescendants = ["col", "colgroup", "tfoot", "thead", "th"];
            var descendantExists = function(tag) {
              return !!table.getElementsByTagName(tag)[0];
            };
            if (dataTableDescendants.some(descendantExists)) {
              this.log("Data table because found data-y descendant");
              table._readabilityDataTable = true;
              continue;
            }
            if (table.getElementsByTagName("table")[0]) {
              table._readabilityDataTable = false;
              continue;
            }
            var sizeInfo = this._getRowAndColumnCount(table);
            if (sizeInfo.columns == 1 || sizeInfo.rows == 1) {
              table._readabilityDataTable = false;
              continue;
            }
            if (sizeInfo.rows >= 10 || sizeInfo.columns > 4) {
              table._readabilityDataTable = true;
              continue;
            }
            table._readabilityDataTable = sizeInfo.rows * sizeInfo.columns > 10;
          }
        },
        /* convert images and figures that have properties like data-src into images that can be loaded without JS */
        _fixLazyImages(root) {
          this._forEachNode(
            this._getAllNodesWithTag(root, ["img", "picture", "figure"]),
            function(elem) {
              if (elem.src && this.REGEXPS.b64DataUrl.test(elem.src)) {
                var parts = this.REGEXPS.b64DataUrl.exec(elem.src);
                if (parts[1] === "image/svg+xml") {
                  return;
                }
                var srcCouldBeRemoved = false;
                for (var i = 0; i < elem.attributes.length; i++) {
                  var attr = elem.attributes[i];
                  if (attr.name === "src") {
                    continue;
                  }
                  if (/\.(jpg|jpeg|png|webp)/i.test(attr.value)) {
                    srcCouldBeRemoved = true;
                    break;
                  }
                }
                if (srcCouldBeRemoved) {
                  var b64starts = parts[0].length;
                  var b64length = elem.src.length - b64starts;
                  if (b64length < 133) {
                    elem.removeAttribute("src");
                  }
                }
              }
              if ((elem.src || elem.srcset && elem.srcset != "null") && !elem.className.toLowerCase().includes("lazy")) {
                return;
              }
              for (var j = 0; j < elem.attributes.length; j++) {
                attr = elem.attributes[j];
                if (attr.name === "src" || attr.name === "srcset" || attr.name === "alt") {
                  continue;
                }
                var copyTo = null;
                if (/\.(jpg|jpeg|png|webp)\s+\d/.test(attr.value)) {
                  copyTo = "srcset";
                } else if (/^\s*\S+\.(jpg|jpeg|png|webp)\S*\s*$/.test(attr.value)) {
                  copyTo = "src";
                }
                if (copyTo) {
                  if (elem.tagName === "IMG" || elem.tagName === "PICTURE") {
                    elem.setAttribute(copyTo, attr.value);
                  } else if (elem.tagName === "FIGURE" && !this._getAllNodesWithTag(elem, ["img", "picture"]).length) {
                    var img = this._doc.createElement("img");
                    img.setAttribute(copyTo, attr.value);
                    elem.appendChild(img);
                  }
                }
              }
            }
          );
        },
        _getTextDensity(e, tags) {
          var textLength = this._getInnerText(e, true).length;
          if (textLength === 0) {
            return 0;
          }
          var childrenLength = 0;
          var children = this._getAllNodesWithTag(e, tags);
          this._forEachNode(
            children,
            (child) => childrenLength += this._getInnerText(child, true).length
          );
          return childrenLength / textLength;
        },
        /**
         * Clean an element of all tags of type "tag" if they look fishy.
         * "Fishy" is an algorithm based on content length, classnames, link density, number of images & embeds, etc.
         *
         * @return void
         **/
        _cleanConditionally(e, tag) {
          if (!this._flagIsActive(this.FLAG_CLEAN_CONDITIONALLY)) {
            return;
          }
          this._removeNodes(this._getAllNodesWithTag(e, [tag]), function(node) {
            var isDataTable = function(t) {
              return t._readabilityDataTable;
            };
            var isList = tag === "ul" || tag === "ol";
            if (!isList) {
              var listLength = 0;
              var listNodes = this._getAllNodesWithTag(node, ["ul", "ol"]);
              this._forEachNode(
                listNodes,
                (list) => listLength += this._getInnerText(list).length
              );
              isList = listLength / this._getInnerText(node).length > 0.9;
            }
            if (tag === "table" && isDataTable(node)) {
              return false;
            }
            if (this._hasAncestorTag(node, "table", -1, isDataTable)) {
              return false;
            }
            if (this._hasAncestorTag(node, "code")) {
              return false;
            }
            if ([...node.getElementsByTagName("table")].some(
              (tbl) => tbl._readabilityDataTable
            )) {
              return false;
            }
            var weight = this._getClassWeight(node);
            this.log("Cleaning Conditionally", node);
            var contentScore = 0;
            if (weight + contentScore < 0) {
              return true;
            }
            if (this._getCharCount(node, ",") < 10) {
              var p = node.getElementsByTagName("p").length;
              var img = node.getElementsByTagName("img").length;
              var li = node.getElementsByTagName("li").length - 100;
              var input = node.getElementsByTagName("input").length;
              var headingDensity = this._getTextDensity(node, [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6"
              ]);
              var embedCount = 0;
              var embeds = this._getAllNodesWithTag(node, [
                "object",
                "embed",
                "iframe"
              ]);
              for (var i = 0; i < embeds.length; i++) {
                for (var j = 0; j < embeds[i].attributes.length; j++) {
                  if (this._allowedVideoRegex.test(embeds[i].attributes[j].value)) {
                    return false;
                  }
                }
                if (embeds[i].tagName === "object" && this._allowedVideoRegex.test(embeds[i].innerHTML)) {
                  return false;
                }
                embedCount++;
              }
              var innerText = this._getInnerText(node);
              if (this.REGEXPS.adWords.test(innerText) || this.REGEXPS.loadingWords.test(innerText)) {
                return true;
              }
              var contentLength = innerText.length;
              var linkDensity2 = this._getLinkDensity(node);
              var textishTags = ["SPAN", "LI", "TD"].concat(
                Array.from(this.DIV_TO_P_ELEMS)
              );
              var textDensity2 = this._getTextDensity(node, textishTags);
              var isFigureChild = this._hasAncestorTag(node, "figure");
              const shouldRemoveNode = () => {
                const errs = [];
                if (!isFigureChild && img > 1 && p / img < 0.5) {
                  errs.push(`Bad p to img ratio (img=${img}, p=${p})`);
                }
                if (!isList && li > p) {
                  errs.push(`Too many li's outside of a list. (li=${li} > p=${p})`);
                }
                if (input > Math.floor(p / 3)) {
                  errs.push(`Too many inputs per p. (input=${input}, p=${p})`);
                }
                if (!isList && !isFigureChild && headingDensity < 0.9 && contentLength < 25 && (img === 0 || img > 2) && linkDensity2 > 0) {
                  errs.push(
                    `Suspiciously short. (headingDensity=${headingDensity}, img=${img}, linkDensity=${linkDensity2})`
                  );
                }
                if (!isList && weight < 25 && linkDensity2 > 0.2 + this._linkDensityModifier) {
                  errs.push(
                    `Low weight and a little linky. (linkDensity=${linkDensity2})`
                  );
                }
                if (weight >= 25 && linkDensity2 > 0.5 + this._linkDensityModifier) {
                  errs.push(
                    `High weight and mostly links. (linkDensity=${linkDensity2})`
                  );
                }
                if (embedCount === 1 && contentLength < 75 || embedCount > 1) {
                  errs.push(
                    `Suspicious embed. (embedCount=${embedCount}, contentLength=${contentLength})`
                  );
                }
                if (img === 0 && textDensity2 === 0) {
                  errs.push(
                    `No useful content. (img=${img}, textDensity=${textDensity2})`
                  );
                }
                if (errs.length) {
                  this.log("Checks failed", errs);
                  return true;
                }
                return false;
              };
              var haveToRemove = shouldRemoveNode();
              if (isList && haveToRemove) {
                for (var x = 0; x < node.children.length; x++) {
                  let child = node.children[x];
                  if (child.children.length > 1) {
                    return haveToRemove;
                  }
                }
                let li_count = node.getElementsByTagName("li").length;
                if (img == li_count) {
                  return false;
                }
              }
              return haveToRemove;
            }
            return false;
          });
        },
        /**
         * Clean out elements that match the specified conditions
         *
         * @param Element
         * @param Function determines whether a node should be removed
         * @return void
         **/
        _cleanMatchedNodes(e, filter) {
          var endOfSearchMarkerNode = this._getNextNode(e, true);
          var next = this._getNextNode(e);
          while (next && next != endOfSearchMarkerNode) {
            if (filter.call(this, next, next.className + " " + next.id)) {
              next = this._removeAndGetNext(next);
            } else {
              next = this._getNextNode(next);
            }
          }
        },
        /**
         * Clean out spurious headers from an Element.
         *
         * @param Element
         * @return void
         **/
        _cleanHeaders(e) {
          let headingNodes = this._getAllNodesWithTag(e, ["h1", "h2"]);
          this._removeNodes(headingNodes, function(node) {
            let shouldRemove = this._getClassWeight(node) < 0;
            if (shouldRemove) {
              this.log("Removing header with low class weight:", node);
            }
            return shouldRemove;
          });
        },
        /**
         * Check if this node is an H1 or H2 element whose content is mostly
         * the same as the article title.
         *
         * @param Element  the node to check.
         * @return boolean indicating whether this is a title-like header.
         */
        _headerDuplicatesTitle(node) {
          if (node.tagName != "H1" && node.tagName != "H2") {
            return false;
          }
          var heading = this._getInnerText(node, false);
          this.log("Evaluating similarity of header:", heading, this._articleTitle);
          return this._textSimilarity(this._articleTitle, heading) > 0.75;
        },
        _flagIsActive(flag) {
          return (this._flags & flag) > 0;
        },
        _removeFlag(flag) {
          this._flags = this._flags & ~flag;
        },
        _isProbablyVisible(node) {
          return (!node.style || node.style.display != "none") && (!node.style || node.style.visibility != "hidden") && !node.hasAttribute("hidden") && //check for "fallback-image" so that wikimedia math images are displayed
          (!node.hasAttribute("aria-hidden") || node.getAttribute("aria-hidden") != "true" || node.className && node.className.includes && node.className.includes("fallback-image"));
        },
        /**
         * Runs readability.
         *
         * Workflow:
         *  1. Prep the document by removing script tags, css, etc.
         *  2. Build readability's DOM tree.
         *  3. Grab the article content from the current dom tree.
         *  4. Replace the current DOM tree with the new one.
         *  5. Read peacefully.
         *
         * @return void
         **/
        parse() {
          if (this._maxElemsToParse > 0) {
            var numTags = this._doc.getElementsByTagName("*").length;
            if (numTags > this._maxElemsToParse) {
              throw new Error(
                "Aborting parsing document; " + numTags + " elements found"
              );
            }
          }
          this._unwrapNoscriptImages(this._doc);
          var jsonLd = this._disableJSONLD ? {} : this._getJSONLD(this._doc);
          this._removeScripts(this._doc);
          this._prepDocument();
          var metadata = this._getArticleMetadata(jsonLd);
          this._metadata = metadata;
          this._articleTitle = metadata.title;
          var articleContent = this._grabArticle();
          if (!articleContent) {
            return null;
          }
          this.log("Grabbed: " + articleContent.innerHTML);
          this._postProcessContent(articleContent);
          if (!metadata.excerpt) {
            var paragraphs = articleContent.getElementsByTagName("p");
            if (paragraphs.length) {
              metadata.excerpt = paragraphs[0].textContent.trim();
            }
          }
          var textContent = articleContent.textContent;
          return {
            title: this._articleTitle,
            byline: metadata.byline || this._articleByline,
            dir: this._articleDir,
            lang: this._articleLang,
            content: this._serializer(articleContent),
            textContent,
            length: textContent.length,
            excerpt: metadata.excerpt,
            siteName: metadata.siteName || this._articleSiteName,
            publishedTime: metadata.publishedTime
          };
        }
      };
      {
        module.exports = Readability2;
      }
    })(Readability);
    return Readability.exports;
  }
  var ReadabilityReaderable = { exports: {} };
  var hasRequiredReadabilityReaderable;
  function requireReadabilityReaderable() {
    if (hasRequiredReadabilityReaderable) return ReadabilityReaderable.exports;
    hasRequiredReadabilityReaderable = 1;
    (function(module) {
      var REGEXPS = {
        // NOTE: These two regular expressions are duplicated in
        // Readability.js. Please keep both copies in sync.
        unlikelyCandidates: /-ad-|ai2html|banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|footer|gdpr|header|legends|menu|related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|ad-break|agegate|pagination|pager|popup|yom-remote/i,
        okMaybeItsACandidate: /and|article|body|column|content|main|shadow/i
      };
      function isNodeVisible(node) {
        return (!node.style || node.style.display != "none") && !node.hasAttribute("hidden") && //check for "fallback-image" so that wikimedia math images are displayed
        (!node.hasAttribute("aria-hidden") || node.getAttribute("aria-hidden") != "true" || node.className && node.className.includes && node.className.includes("fallback-image"));
      }
      function isProbablyReaderable(doc, options = {}) {
        if (typeof options == "function") {
          options = { visibilityChecker: options };
        }
        var defaultOptions = {
          minScore: 20,
          minContentLength: 140,
          visibilityChecker: isNodeVisible
        };
        options = Object.assign(defaultOptions, options);
        var nodes = doc.querySelectorAll("p, pre, article");
        var brNodes = doc.querySelectorAll("div > br");
        if (brNodes.length) {
          var set = new Set(nodes);
          [].forEach.call(brNodes, function(node) {
            set.add(node.parentNode);
          });
          nodes = Array.from(set);
        }
        var score = 0;
        return [].some.call(nodes, function(node) {
          if (!options.visibilityChecker(node)) {
            return false;
          }
          var matchString = node.className + " " + node.id;
          if (REGEXPS.unlikelyCandidates.test(matchString) && !REGEXPS.okMaybeItsACandidate.test(matchString)) {
            return false;
          }
          if (node.matches("li p")) {
            return false;
          }
          var textContentLength = node.textContent.trim().length;
          if (textContentLength < options.minContentLength) {
            return false;
          }
          score += Math.sqrt(textContentLength - options.minContentLength);
          if (score > options.minScore) {
            return true;
          }
          return false;
        });
      }
      {
        module.exports = isProbablyReaderable;
      }
    })(ReadabilityReaderable);
    return ReadabilityReaderable.exports;
  }
  var readability;
  var hasRequiredReadability;
  function requireReadability() {
    if (hasRequiredReadability) return readability;
    hasRequiredReadability = 1;
    var Readability2 = requireReadability$1();
    var isProbablyReaderable = requireReadabilityReaderable();
    readability = {
      Readability: Readability2,
      isProbablyReaderable
    };
    return readability;
  }
  var readabilityExports = requireReadability();
  class ReadabilityCache {
    constructor() {
      __publicField(this, "cachedResult", null);
      __publicField(this, "cacheUrl", null);
      __publicField(this, "cacheTimestamp", 0);
      // 缓存有效期（毫秒）：5分钟
      __publicField(this, "CACHE_TTL", 5 * 60 * 1e3);
    }
    /**
     * 获取或执行 Readability 提取
     * 如果缓存有效则直接返回缓存结果
     */
    getOrExtract() {
      const currentUrl = window.location.href;
      const now = Date.now();
      if (this.cacheUrl === currentUrl && this.cachedResult && now - this.cacheTimestamp < this.CACHE_TTL) {
        console.log("[ReadabilityCache] 使用缓存结果");
        return this.cachedResult;
      }
      console.log("[ReadabilityCache] 执行新提取");
      this.cachedResult = this.doExtract();
      this.cacheUrl = currentUrl;
      this.cacheTimestamp = now;
      return this.cachedResult;
    }
    /**
     * 执行实际的 Readability 提取
     */
    doExtract() {
      var _a;
      try {
        const documentClone = document.cloneNode(true);
        const reader = new readabilityExports.Readability(documentClone, {
          // 保留更多内容
          charThreshold: 100
        });
        const article = reader.parse();
        if (!article) {
          console.log("[ReadabilityCache] 解析失败，无法提取内容");
          return null;
        }
        console.log("[ReadabilityCache] 提取成功:", {
          title: article.title,
          length: article.length,
          excerpt: (_a = article.excerpt) == null ? void 0 : _a.substring(0, 50)
        });
        return article;
      } catch (error) {
        console.error("[ReadabilityCache] 提取出错:", error);
        return null;
      }
    }
    /**
     * 使缓存失效
     * 在页面内容发生重大变化时调用
     */
    invalidate() {
      console.log("[ReadabilityCache] 缓存已失效");
      this.cachedResult = null;
      this.cacheUrl = null;
      this.cacheTimestamp = 0;
    }
    /**
     * 检查当前是否有有效缓存
     */
    hasValidCache() {
      const currentUrl = window.location.href;
      const now = Date.now();
      return this.cacheUrl === currentUrl && this.cachedResult !== null && now - this.cacheTimestamp < this.CACHE_TTL;
    }
    /**
     * 获取缓存统计信息（用于调试）
     */
    getStats() {
      return {
        hasCache: this.cachedResult !== null,
        url: this.cacheUrl,
        age: this.cacheTimestamp ? Date.now() - this.cacheTimestamp : -1
      };
    }
  }
  const readabilityCache = new ReadabilityCache();
  function isReaderable() {
    return readabilityExports.isProbablyReaderable(document);
  }
  function extractWithReadability() {
    return readabilityCache.getOrExtract();
  }
  function isJunkText(text) {
    if (/^\s*[.#][\w-]+\s*[{,]/.test(text)) {
      console.log("[isJunkText] 检测到 CSS 选择器开头");
      return true;
    }
    if (/[.#]?[\w-]+\s*\{[^}]*\}/.test(text)) {
      return true;
    }
    const cssPropertyPattern = /[\w-]+\s*:\s*[^;]+;/g;
    const cssMatches = text.match(cssPropertyPattern) || [];
    if (cssMatches.length > 2) {
      return true;
    }
    const cssKeywords = [
      "background-color",
      "background:",
      "font-size",
      "font-family",
      "line-height",
      "margin:",
      "margin-",
      "padding:",
      "padding-",
      "border:",
      "border-",
      "display:",
      "position:",
      "width:",
      "height:",
      "color:rgb",
      "color:#",
      "text-align",
      "text-decoration",
      "overflow:",
      "z-index",
      "opacity:",
      "transform:",
      "transition:",
      "flex:",
      "grid:",
      "qrfullpage"
      // 微信读书特定
    ];
    const lowerText = text.toLowerCase();
    let cssKeywordCount = 0;
    for (const keyword of cssKeywords) {
      if (lowerText.includes(keyword)) {
        cssKeywordCount++;
      }
    }
    if (cssKeywordCount >= 2) {
      console.log("[isJunkText] 检测到 CSS 关键字:", cssKeywordCount);
      return true;
    }
    if (/\.readerChapterContent/i.test(text) || /\.wr_/i.test(text) || /\.ccn-/i.test(text)) {
      console.log("[isJunkText] 检测到微信读书 CSS 类名");
      return true;
    }
    const braceCount = (text.match(/[{}]/g) || []).length;
    if (braceCount > 4) {
      console.log("[isJunkText] 检测到大量花括号:", braceCount);
      return true;
    }
    const uiPatterns = [
      /^JS复制代码/,
      /^复制代码/,
      /^复制$/,
      /^分享$/,
      /^点赞$/,
      /^收藏$/,
      /^关注$/
    ];
    if (uiPatterns.some((pattern) => pattern.test(text.trim()))) {
      return true;
    }
    const cleanText2 = text.replace(/[\s\d\W]/g, "");
    if (cleanText2.length < 5 && text.length > 20) {
      return true;
    }
    return false;
  }
  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  const TEXT_LAYOUT_PROPS = [
    "font-family",
    "font-size",
    "font-weight",
    "font-style",
    "font-variant",
    "font-kerning",
    "font-feature-settings",
    "font-variation-settings",
    "font-optical-sizing",
    "font-stretch",
    "font-synthesis",
    "letter-spacing",
    "word-spacing",
    "line-height",
    "text-indent",
    "text-align",
    "word-break",
    "overflow-wrap",
    "white-space",
    "text-transform",
    "text-rendering",
    "hyphens",
    "-webkit-font-smoothing",
    "direction",
    "writing-mode",
    "tab-size",
    "padding-left",
    "padding-right",
    "padding-top",
    "padding-bottom"
  ];
  function isCanvasDualColumn(container) {
    var _a;
    const canvases = container.querySelectorAll("canvas");
    if (canvases.length >= 2) {
      const r0 = canvases[0].getBoundingClientRect();
      const r1 = canvases[1].getBoundingClientRect();
      if (Math.abs(r0.top - r1.top) < r0.height * 0.5) return true;
    }
    if (canvases.length >= 1) {
      try {
        const raw = document.documentElement.getAttribute("data-castreader-wr-layout");
        if (raw) {
          const data = JSON.parse(raw);
          if (((_a = data.pages) == null ? void 0 : _a.length) >= 2) {
            const txSet = new Set(data.pages.map((p) => p.tx));
            if (txSet.size >= 2) return true;
          }
        }
      } catch {
      }
    }
    return false;
  }
  const TITLE_SELECTORS = [
    ".readerTopBar_title_link",
    ".readerTopBar_title",
    ".readerControls_bookTitle",
    ".bookInfo_title",
    ".chapterTitle",
    "h1.title"
  ];
  const DOM_TEXT_CONTAINER_SELECTORS = [
    ".preRenderContainer",
    // 预渲染容器（包含真实章节 HTML，最可靠）
    ".renderTargetContainer",
    // 渲染目标容器
    ".readerChapterContent",
    // 章节内容
    ".wr_readerContent"
    // WeRead 内容区
  ];
  function findTitle() {
    for (const selector of TITLE_SELECTORS) {
      const element = document.querySelector(selector);
      if (element && element.textContent) {
        return element.textContent.trim();
      }
    }
    return document.title || null;
  }
  function extractParagraphsFromLiveDOM() {
    var _a, _b, _c;
    const result = [];
    const seen = /* @__PURE__ */ new Set();
    const containerSelectors = [
      ".readerChapterContent",
      ".wr_readerContent",
      ".app_content",
      ".readerContent"
    ];
    let contentContainer = null;
    for (const selector of containerSelectors) {
      const el = document.querySelector(selector);
      if (!el) continue;
      const blocks2 = el.querySelectorAll("p, h1, h2, h3, h4, h5, h6, li, blockquote");
      let chineseBlockCount = 0;
      for (const block of blocks2) {
        const text = (_a = block.textContent) == null ? void 0 : _a.trim();
        if (text && /[\u4e00-\u9fa5]{5,}/.test(text)) {
          chineseBlockCount++;
        }
      }
      if (chineseBlockCount >= 3) {
        contentContainer = el;
        console.log("[weread] 找到 DOM 内容容器:", selector, "段落元素:", chineseBlockCount);
        break;
      }
    }
    if (!contentContainer) {
      console.log("[weread] 未找到含段落元素的 DOM 容器");
      return [];
    }
    const blocks = contentContainer.querySelectorAll("p, h1, h2, h3, h4, h5, h6, li, blockquote");
    for (const block of blocks) {
      const text = (_b = block.textContent) == null ? void 0 : _b.trim();
      if (!text || text.length < 5) continue;
      const key = text.substring(0, 100);
      if (seen.has(key)) continue;
      seen.add(key);
      const el = block;
      if (el.offsetParent === null && el.offsetHeight === 0) continue;
      if (!isJunkText(text)) {
        result.push({
          text,
          element: el,
          canHighlight: true
        });
      }
    }
    if (result.length > 0) {
      console.log(
        "[weread] DOM 模式：提取到",
        result.length,
        "个真实段落元素",
        "preview:",
        (_c = result[0]) == null ? void 0 : _c.text.substring(0, 60)
      );
    }
    return result;
  }
  function getCleanTextContent(el) {
    const clone = el.cloneNode(true);
    clone.querySelectorAll("style, script, noscript, link").forEach((s) => s.remove());
    return (clone.textContent || "").trim();
  }
  function extractTextFromDOMContainers() {
    for (const selector of DOM_TEXT_CONTAINER_SELECTORS) {
      const el = document.querySelector(selector);
      if (!el) continue;
      const cleanText2 = getCleanTextContent(el);
      const chineseCount = (cleanText2.match(/[\u4e00-\u9fa5]/g) || []).length;
      if (chineseCount >= 20) {
        console.log("[weread] 容器文本提取:", selector, "中文:", chineseCount);
        const paragraphs = splitIntoParagraphs(cleanText2);
        if (paragraphs.length > 0) return paragraphs;
      }
    }
    return [];
  }
  function splitIntoParagraphs(text) {
    const result = [];
    const seen = /* @__PURE__ */ new Set();
    let normalized = text.replace(/\r\n/g, "\n");
    const parts = normalized.split(/\n\s*\n|\n(?=\u3000)/);
    for (const part of parts) {
      const trimmed = part.replace(/^[\s\u3000]+/, "").replace(/[\s\u3000]+$/, "");
      if (trimmed.length < 5) continue;
      const hasChinese = /[\u4e00-\u9fa5]{3,}/.test(trimmed);
      if (!hasChinese && trimmed.length < 20) continue;
      const key = trimmed.substring(0, 100);
      if (seen.has(key)) continue;
      seen.add(key);
      if (!isJunkText(trimmed)) {
        result.push(trimmed);
      }
    }
    if (result.length <= 1 && text.length > 200) {
      return splitBySentenceGroups(text);
    }
    return result;
  }
  function splitBySentenceGroups(text) {
    const cleanText2 = text.replace(/^[\s\u3000]+/, "").replace(/[\s\u3000]+$/, "");
    const sentences = cleanText2.split(new RegExp("(?<=[。！？])"));
    const result = [];
    let current = "";
    for (const sentence of sentences) {
      const trimmed = sentence.trim();
      if (!trimmed) continue;
      current += trimmed;
      const sentenceCount = (current.match(/[。！？]/g) || []).length;
      if (sentenceCount >= 3 || current.length >= 150) {
        if (current.length >= 10) {
          result.push(current);
        }
        current = "";
      }
    }
    if (current.length >= 10) {
      result.push(current);
    }
    return result;
  }
  function extractFromApiAttribute() {
    const ATTR_NAME = "data-castreader-wr-chapter";
    const raw = document.documentElement.getAttribute(ATTR_NAME);
    if (!raw) {
      console.log("[weread] DOM 属性无 API 数据");
      return [];
    }
    const colonIdx = raw.indexOf(":");
    if (colonIdx === -1) return [];
    try {
      const content = raw.substring(colonIdx + 1);
      console.log("[weread] API 属性内容长度:", content.length, "preview:", content.substring(0, 80));
      const contentChinese = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      const hasHtml = content.includes("<");
      if (contentChinese < 10 && !hasHtml) {
        console.log("[weread] API 属性内容非可读文本（可能是加密数据），跳过");
        return [];
      }
      let paragraphs;
      try {
        const data = JSON.parse(content);
        paragraphs = parseChapterApiResponse(data);
      } catch {
        paragraphs = parseHtmlToParagraphs(content);
      }
      if (paragraphs.length > 0) {
        console.log("[weread] 从 API 拦截属性提取，段落数:", paragraphs.length);
        return paragraphs.map((text) => ({
          text,
          element: document.body,
          canHighlight: false
        }));
      }
    } catch (e) {
      console.error("[weread] 解析 API 属性数据失败:", e);
    }
    return [];
  }
  function parseChapterApiResponse(data) {
    var _a, _b, _c, _d;
    if (!data) return [];
    const possiblePaths = [
      data.chapterContentHtml,
      data.chapterContent,
      data.content,
      data.htmlContent,
      data.html,
      (_a = data.data) == null ? void 0 : _a.chapterContentHtml,
      (_b = data.data) == null ? void 0 : _b.chapterContent,
      (_c = data.data) == null ? void 0 : _c.content,
      (_d = data.data) == null ? void 0 : _d.htmlContent
    ];
    for (const content of possiblePaths) {
      if (content && typeof content === "string" && content.length > 50) {
        if (content.includes("<") || /[\u4e00-\u9fa5]{10,}/.test(content)) {
          const paragraphs = parseHtmlToParagraphs(content);
          if (paragraphs.length > 0) return paragraphs;
        }
      }
    }
    const allStrings = findLongStrings(data);
    for (const str of allStrings) {
      const paragraphs = parseHtmlToParagraphs(str);
      if (paragraphs.length >= 3) return paragraphs;
    }
    return [];
  }
  function findLongStrings(obj, depth = 0) {
    if (depth > 3 || !obj) return [];
    const results = [];
    if (typeof obj === "string" && obj.length > 200) {
      results.push(obj);
    } else if (typeof obj === "object") {
      for (const key of Object.keys(obj)) {
        results.push(...findLongStrings(obj[key], depth + 1));
      }
    }
    return results;
  }
  function parseHtmlToParagraphs(content) {
    var _a, _b, _c, _d;
    const paragraphs = [];
    const seen = /* @__PURE__ */ new Set();
    try {
      if (content.includes("<")) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(content, "text/html");
        for (const fn of doc.querySelectorAll(".reader_footer_note, .js_readerFooterNote, [data-wr-footernote]")) {
          fn.remove();
        }
        const spans = Array.from(doc.querySelectorAll("span"));
        for (const span of spans) {
          if (span.attributes.length > 0 || (((_a = span.textContent) == null ? void 0 : _a.length) ?? 0) > 1) continue;
          if (!span.parentNode) continue;
          let next = span.nextElementSibling;
          while ((next == null ? void 0 : next.tagName) === "SPAN" && next.attributes.length === 0 && (((_b = next.textContent) == null ? void 0 : _b.length) ?? 0) <= 1) {
            span.append(next.textContent ?? "");
            const toRemove = next;
            next = next.nextElementSibling;
            toRemove.remove();
          }
        }
        const blocks = doc.querySelectorAll("p, h1, h2, h3, h4, h5, h6, li, blockquote");
        for (const block of blocks) {
          const text = (_c = block.textContent) == null ? void 0 : _c.trim();
          if (!text || text.length < 5) continue;
          const key = text.substring(0, 100);
          if (seen.has(key)) continue;
          seen.add(key);
          paragraphs.push(text);
        }
        if (paragraphs.length === 0) {
          const fullText = (_d = doc.body.textContent) == null ? void 0 : _d.trim();
          if (fullText && fullText.length > 10) {
            for (const line of fullText.split(/\n+/)) {
              const trimmed = line.trim();
              if (trimmed.length < 5) continue;
              const key = trimmed.substring(0, 100);
              if (seen.has(key)) continue;
              seen.add(key);
              paragraphs.push(trimmed);
            }
          }
        }
      } else {
        for (const line of content.split(/\n+/)) {
          const trimmed = line.trim();
          if (trimmed.length < 5) continue;
          const key = trimmed.substring(0, 100);
          if (seen.has(key)) continue;
          seen.add(key);
          paragraphs.push(trimmed);
        }
      }
    } catch {
      for (const line of content.split(/\n+/)) {
        const trimmed = line.replace(/<[^>]*>/g, "").trim();
        if (trimmed.length >= 5) {
          const key = trimmed.substring(0, 100);
          if (!seen.has(key)) {
            seen.add(key);
            paragraphs.push(trimmed);
          }
        }
      }
    }
    return paragraphs;
  }
  function readFillTextLayout() {
    const LAYOUT_ATTR = "data-castreader-wr-layout";
    const raw = document.documentElement.getAttribute(LAYOUT_ATTR);
    if (!raw) return null;
    try {
      const data = JSON.parse(raw);
      if (data.lines && data.lines.length > 0) {
        const pageInfo = data.pages ? ` pages=[${data.pages.map((p) => `c${p.cIdx}/tx${p.tx}:${p.lines.length}行`).join(",")}]` : "";
        console.log(
          `[weread] fillText 行级数据: ${data.lines.length} 行${pageInfo}`,
          `textLeft=${data.textLeft} textRight=${data.textRight} lineH=${data.lineHeight}`
        );
        return data;
      }
    } catch (e) {
      console.error("[weread] 解析 fillText 布局数据失败:", e);
    }
    return null;
  }
  function sliceParagraphByCleanOffset(paraText, cleanStart, cleanEnd) {
    let cleanIdx = 0;
    let origStart = 0;
    let origEnd = paraText.length;
    let foundStart = cleanStart === 0;
    for (let i = 0; i < paraText.length; i++) {
      if (/\s/.test(paraText[i])) continue;
      if (!foundStart && cleanIdx === cleanStart) {
        origStart = i;
        foundStart = true;
      }
      cleanIdx++;
      if (cleanIdx === cleanEnd) {
        origEnd = i + 1;
        break;
      }
    }
    return paraText.substring(origStart, origEnd).trim();
  }
  function matchFillTextPagesToChapter(chapterParagraphs) {
    var _a, _b;
    const layout = readFillTextLayout();
    if (!(layout == null ? void 0 : layout.pages) || layout.pages.length === 0) {
      console.log("[weread] matchFillTextPages: 无 fillText pages 数据");
      return null;
    }
    let chapterText = "";
    const paraRanges = [];
    for (let pi = 0; pi < chapterParagraphs.length; pi++) {
      const clean2 = chapterParagraphs[pi].replace(/\s/g, "");
      if (clean2.length === 0) continue;
      const start = chapterText.length;
      chapterText += clean2;
      paraRanges.push({ start, end: chapterText.length, idx: pi });
    }
    const canvasContainer = document.querySelector(".wr_canvasContainer");
    let highlightContainer = null;
    const canvasInfo = /* @__PURE__ */ new Map();
    const dpr = window.devicePixelRatio || 1;
    if (canvasContainer) {
      if (getComputedStyle(canvasContainer).position === "static") {
        canvasContainer.style.position = "relative";
      }
      const old = canvasContainer.querySelector(".castreader-wr-highlights");
      if (old) old.remove();
      highlightContainer = document.createElement("div");
      highlightContainer.className = "castreader-wr-highlights";
      highlightContainer.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;";
      canvasContainer.prepend(highlightContainer);
      const canvases = canvasContainer.querySelectorAll("canvas");
      const containerRect = canvasContainer.getBoundingClientRect();
      canvases.forEach((c, i) => {
        const cCanvas = c;
        const scaleX = cCanvas.width > 0 ? cCanvas.offsetWidth * dpr / cCanvas.width : 1;
        const scaleY = cCanvas.height > 0 ? cCanvas.offsetHeight * dpr / cCanvas.height : 1;
        canvasInfo.set(i, {
          offsetLeft: c.getBoundingClientRect().left - containerRect.left,
          offsetTop: c.getBoundingClientRect().top - containerRect.top,
          scaleX,
          scaleY
        });
      });
      console.log(`[weread] canvas 校正:`, [...canvasInfo.entries()].map(
        ([i, info]) => `c${i}: offset=(${Math.round(info.offsetLeft)},${Math.round(info.offsetTop)}) scale=(${info.scaleX.toFixed(2)},${info.scaleY.toFixed(2)})`
      ).join(" | "));
    }
    const result = [];
    const cache = globalThis.__castreader_weread_cache__;
    const hookPositions = (cache == null ? void 0 : cache.paragraphPositions) || [];
    let prevPageEnd = 0;
    const extractPageByLineGrouping = (page, container, cInfo) => {
      var _a2;
      const yGaps = [];
      for (let i = 1; i < page.lines.length; i++) {
        const g = page.lines[i].y - page.lines[i - 1].y;
        if (g > 0) yGaps.push(g);
      }
      yGaps.sort((a, b) => a - b);
      const medianLineGap = yGaps.length > 0 ? yGaps[Math.floor(yGaps.length / 2)] : page.lineHeight || layout.lineHeight;
      const pageLineHeight = page.lineHeight || medianLineGap;
      const q1Idx = Math.max(0, Math.floor(yGaps.length * 0.25));
      const baseGap = yGaps.length > 0 ? yGaps[q1Idx] : medianLineGap;
      const paraGapThreshold = baseGap * 1.3;
      const pTextLeft = page.textLeft ?? layout.textLeft;
      const pTextRight = page.textRight ?? layout.textRight;
      const pFontSize = page.fontSize || pageLineHeight * 0.55;
      const blCorr = pFontSize * 0.88;
      const pad = pFontSize * 0.3;
      const inf = cInfo.get(page.cIdx);
      const lsx = (inf == null ? void 0 : inf.scaleX) ?? 1;
      const lsy = (inf == null ? void 0 : inf.scaleY) ?? 1;
      const lox = (inf == null ? void 0 : inf.offsetLeft) ?? 0;
      const loy = (inf == null ? void 0 : inf.offsetTop) ?? 0;
      const ltxCss = (page.tx || 0) / dpr;
      const pageResult = [];
      let lineTexts = [];
      let pStartY = ((_a2 = page.lines[0]) == null ? void 0 : _a2.y) ?? 0;
      let pEndY = pStartY;
      let lastLineY = pStartY;
      const flushDebug = [];
      const flush = () => {
        if (lineTexts.length === 0) return;
        const t = lineTexts.join("");
        flushDebug.push(`flush:${lineTexts.length}lines,${t.length}ch,"${t.substring(0, 25)}"`);
        if (t.length < 3) {
          lineTexts = [];
          return;
        }
        if (container) {
          const fTop = (pStartY - blCorr) * lsy + loy;
          const fLeft = (pTextLeft + ltxCss - pad) * lsx + lox;
          const fWidth = (pTextRight - pTextLeft + pFontSize + pad) * lsx;
          const fHeight = (pEndY + pageLineHeight - pStartY) * lsy;
          const d = document.createElement("div");
          d.dataset.castreaderOverlay = "weread";
          d.style.cssText = `position:absolute;top:${Math.round(fTop)}px;left:${Math.round(fLeft)}px;width:${Math.round(fWidth)}px;height:${Math.round(fHeight)}px;pointer-events:auto;border-radius:4px;transition:background-color 0.3s ease;`;
          const sp = document.createElement("span");
          sp.textContent = t;
          sp.style.cssText = `font-size:${Math.round(pFontSize * lsy)}px;color:transparent;display:block;position:absolute;top:0;left:0;width:100%;height:100%;overflow:hidden;pointer-events:none;line-height:${pageLineHeight}px;margin:0;padding:0;box-sizing:border-box;`;
          d.appendChild(sp);
          container.appendChild(d);
          pageResult.push({ text: t, element: d, canHighlight: true, textElement: sp });
        } else {
          pageResult.push({ text: t, element: document.body, canHighlight: false });
        }
        lineTexts = [];
      };
      for (const line of page.lines) {
        const gap = line.y - lastLineY;
        if (lineTexts.length > 0 && gap > paraGapThreshold) {
          flush();
          pStartY = line.y;
        }
        lineTexts.push(line.t);
        pEndY = line.y;
        lastLineY = line.y;
      }
      flush();
      try {
        const rawGaps = [];
        for (let i = 1; i < page.lines.length; i++) {
          rawGaps.push((page.lines[i].y - page.lines[i - 1].y).toFixed(1));
        }
        document.documentElement.dataset.castreaderGapDiag = (document.documentElement.dataset.castreaderGapDiag || "") + `c${page.cIdx}:lines=${page.lines.length},q1=${baseGap.toFixed(1)},thr=${paraGapThreshold.toFixed(1)},paras=${pageResult.length},rawGaps=[${rawGaps.join(",")}] | `;
        document.documentElement.dataset.castreaderFlushDiag = (document.documentElement.dataset.castreaderFlushDiag || "") + flushDebug.join(" || ") + " ||| ";
      } catch {
      }
      return pageResult;
    };
    const pageDebugLines = [];
    pageDebugLines.push(`pages=${layout.pages.length}`);
    for (let pi = 0; pi < layout.pages.length; pi++) {
      const p = layout.pages[pi];
      pageDebugLines.push(`p${pi}:c${p.cIdx}/tx${p.tx || 0}/${p.lines.length}行/"${((_b = (_a = p.lines[0]) == null ? void 0 : _a.t) == null ? void 0 : _b.substring(0, 10)) || ""}"`);
    }
    for (const page of layout.pages) {
      const pageText = page.lines.map((l) => l.t.replace(/\s/g, "")).join("");
      if (pageText.length < 5) {
        console.log(`[weread] 页 c${page.cIdx}: 文本太短(${pageText.length}字), 跳过`);
        pageDebugLines.push(`c${page.cIdx}:SHORT(${pageText.length})`);
        continue;
      }
      let hits = 0;
      const checkOffsets = [
        0,
        Math.floor(pageText.length * 0.25),
        Math.floor(pageText.length / 2),
        Math.floor(pageText.length * 0.75),
        Math.max(0, pageText.length - 15)
      ];
      for (const off of checkOffsets) {
        const ck = pageText.substring(off, off + 15);
        if (ck.length >= 8 && chapterText.includes(ck)) hits++;
        if (hits >= 2) break;
      }
      if (hits < 2) {
        console.log(`[weread] 页 c${page.cIdx}: ${pageText.length}字 ✗ 章节不匹配(${hits}/5), 回退行分组`);
        const fallbackParas = extractPageByLineGrouping(page, highlightContainer, canvasInfo);
        result.push(...fallbackParas);
        pageDebugLines.push(`c${page.cIdx}:FALLBACK(hits=${hits},paras=${fallbackParas.length},lH=${fallbackParas.length > 0 ? "ok" : "?"})`);
        continue;
      }
      const searchFloor = Math.max(0, prevPageEnd - 20);
      let matchPos = -1;
      for (const startOff of [0, 10, 20, 40, 80]) {
        for (const keyLen of [30, 20, 12, 8]) {
          if (startOff + keyLen > pageText.length) continue;
          const key = pageText.substring(startOff, startOff + keyLen);
          matchPos = chapterText.indexOf(key, searchFloor);
          if (matchPos >= 0) break;
        }
        if (matchPos >= 0) break;
      }
      if (matchPos < 0) {
        console.log(`[weread] 页 c${page.cIdx}: ${pageText.length}字 ✓ 验证通过但定位失败, 回退行分组`);
        const fallbackParas = extractPageByLineGrouping(page, highlightContainer, canvasInfo);
        result.push(...fallbackParas);
        pageDebugLines.push(`c${page.cIdx}:POS_FAIL(hits=${hits},paras=${fallbackParas.length})`);
        continue;
      }
      let matchEnd = matchPos + pageText.length;
      const endKey = pageText.substring(Math.max(0, pageText.length - 20));
      const endSearchStart = Math.max(matchPos, matchEnd - 30);
      const endMatch = chapterText.indexOf(endKey, endSearchStart);
      if (endMatch >= 0) matchEnd = endMatch + endKey.length;
      prevPageEnd = matchEnd;
      console.log(`[weread] 页 c${page.cIdx}: ${pageText.length}字 ✓ (${hits}/3命中) 范围[${matchPos},${matchEnd}]`);
      pageDebugLines.push(`c${page.cIdx}:MATCH(hits=${hits},range=${matchPos}-${matchEnd})`);
      const pageTexts = [];
      for (const range of paraRanges) {
        if (range.start >= matchEnd || range.end <= matchPos) continue;
        const paraText = chapterParagraphs[range.idx];
        const paraClean = paraText.replace(/\s/g, "");
        const visibleStart = Math.max(0, matchPos - range.start);
        const visibleEnd = Math.min(paraClean.length, matchEnd - range.start);
        let text;
        if (visibleStart === 0 && visibleEnd >= paraClean.length) {
          text = paraText;
        } else {
          text = sliceParagraphByCleanOffset(paraText, visibleStart, visibleEnd);
        }
        if (text.length < 2) continue;
        pageTexts.push(text);
      }
      const pageLineHeight = page.lineHeight || layout.lineHeight;
      const pageTextLeft = page.textLeft ?? layout.textLeft;
      const pageTextRight = page.textRight ?? layout.textRight;
      const info = canvasInfo.get(page.cIdx);
      const sx = (info == null ? void 0 : info.scaleX) ?? 1;
      const sy = (info == null ? void 0 : info.scaleY) ?? 1;
      const ox = (info == null ? void 0 : info.offsetLeft) ?? 0;
      const oy = (info == null ? void 0 : info.offsetTop) ?? 0;
      const txCssOffset = (page.tx || 0) / dpr;
      const pageFontSize = page.fontSize || pageLineHeight * 0.55;
      const baselineCorrection = pageFontSize * 0.88;
      if (highlightContainer && pageTexts.length > 0) {
        const paraBounds = matchParagraphsToLines(pageTexts, page.lines, pageLineHeight);
        const matchedPositions = hookPositions.length > 0 ? matchTextsToPositions(pageTexts, hookPositions) : pageTexts.map(() => null);
        for (let mi = 0; mi < matchedPositions.length; mi++) {
          if (matchedPositions[mi] || hookPositions.length === 0) continue;
          const probe = pageTexts[mi].replace(/\s/g, "").substring(0, 20);
          if (probe.length < 5) continue;
          matchedPositions[mi] = hookPositions.find(
            (p) => p.text.replace(/\s/g, "").includes(probe)
          ) || null;
        }
        console.log(`[weread] 页 c${page.cIdx}/tx${page.tx || 0} overlay: offset=(${Math.round(ox)},${Math.round(oy)}) txCss=${Math.round(txCssOffset)} scale=(${sx.toFixed(2)},${sy.toFixed(2)}) textL=${pageTextLeft} textR=${pageTextRight} lineH=${pageLineHeight} fontSize=${pageFontSize} blCorr=${baselineCorrection.toFixed(1)}`);
        for (let pi = 0; pi < pageTexts.length; pi++) {
          const bounds = paraBounds[pi];
          if (bounds && bounds.startY >= 0 && bounds.endY > bounds.startY) {
            const pad = pageFontSize * 0.3;
            const top = (bounds.startY - baselineCorrection) * sy + oy;
            const left = (pageTextLeft + txCssOffset - pad) * sx + ox;
            const width = (pageTextRight - pageTextLeft + pageFontSize + pad) * sx;
            const height = (bounds.endY - bounds.startY) * sy;
            const div = document.createElement("div");
            div.dataset.castreaderOverlay = "weread";
            div.style.cssText = `
            position:absolute;
            top:${Math.round(top)}px;
            left:${Math.round(left)}px;
            width:${Math.round(width)}px;
            height:${Math.round(height)}px;
            pointer-events:auto;border-radius:4px;
            transition:background-color 0.3s ease;
          `;
            const hookPos = matchedPositions[pi];
            const textSpan = document.createElement("span");
            if ((hookPos == null ? void 0 : hookPos.footnotes) && hookPos.footnotes.length > 0) {
              let html = "";
              let lastIdx = 0;
              for (const fn of hookPos.footnotes) {
                const safeIdx = Math.max(lastIdx, Math.min(fn.charIndex, pageTexts[pi].length));
                if (safeIdx > lastIdx) html += escapeHtml(pageTexts[pi].substring(lastIdx, safeIdx));
                const spacerW = (fn.width * sx).toFixed(1);
                html += `<span style="display:inline-block;width:${spacerW}px"></span>`;
                lastIdx = safeIdx;
              }
              if (lastIdx < pageTexts[pi].length) html += escapeHtml(pageTexts[pi].substring(lastIdx));
              textSpan.innerHTML = html;
            } else {
              textSpan.textContent = pageTexts[pi];
            }
            const textWidth = (width - pad * sx).toFixed(1);
            const leftOffset = (pad * sx).toFixed(1);
            const canvasLH = pageLineHeight;
            let effectiveFontStyle = (hookPos == null ? void 0 : hookPos.fontStyle) || `font-size: ${Math.round(pageFontSize * sy)}px`;
            if (canvasLH > 0) {
              if (effectiveFontStyle.includes("line-height:")) {
                effectiveFontStyle = effectiveFontStyle.replace(
                  /line-height:[^;]+/,
                  `line-height:${canvasLH}px`
                );
              } else {
                effectiveFontStyle += `;line-height:${canvasLH}px`;
              }
            }
            textSpan.style.cssText = `
            ${effectiveFontStyle};
            color: transparent;
            display: block;
            position: absolute;
            top: 0px;
            left: ${leftOffset}px;
            width: ${textWidth}px;
            height: 100%;
            overflow: hidden;
            pointer-events: none;
            margin: 0; padding: 0; box-sizing: border-box;
          `;
            div.appendChild(textSpan);
            const hookW = (hookPos == null ? void 0 : hookPos.width) ? (hookPos.width * sx).toFixed(0) : "N/A";
            const spanDebug = `p${pi}:tw=${textWidth}/hw=${hookW}/lo=${leftOffset}/lh=${canvasLH}/fs=${hookPos ? "hook" : "FALLBACK"}`;
            div.dataset.castreaderSpan = spanDebug;
            highlightContainer.appendChild(div);
            result.push({ text: pageTexts[pi], element: div, canHighlight: true, textElement: textSpan });
          } else {
            result.push({ text: pageTexts[pi], element: document.body, canHighlight: false });
          }
        }
      } else {
        for (const text of pageTexts) {
          result.push({ text, element: document.body, canHighlight: false });
        }
      }
    }
    if (result.length > 0 && highlightContainer) {
      try {
        const calibIdx = result.findIndex((r) => {
          if (!r.textElement || !r.canHighlight) return false;
          const sp = r.textElement;
          return sp.scrollHeight > (layout.lineHeight || 30) * 1.5;
        });
        if (calibIdx >= 0) {
          const calibR = result[calibIdx];
          const sp = calibR.textElement;
          const div = calibR.element;
          const pageForCalib = layout.pages.find((p) => p.lines.length > 0);
          const calibLineH = (pageForCalib == null ? void 0 : pageForCalib.lineHeight) || layout.lineHeight;
          const calibFontSize = (pageForCalib == null ? void 0 : pageForCalib.fontSize) || calibLineH * 0.55;
          const bounds = matchParagraphsToLines(
            [calibR.text],
            (pageForCalib == null ? void 0 : pageForCalib.lines) || layout.lines,
            calibLineH
          )[0];
          if (bounds && bounds.startY >= 0 && bounds.endY > bounds.startY) {
            const expectedLines = Math.round((bounds.endY - bounds.startY) / calibLineH);
            if (expectedLines > 1) {
              const sH = sp.scrollHeight;
              const actualRenderedLineH = sH / expectedLines;
              const lineDrift = actualRenderedLineH - calibLineH;
              if (Math.abs(lineDrift) > 0.05) {
                const correctedLH = (calibLineH - lineDrift).toFixed(2) + "px";
                for (const r of result) {
                  if (r.textElement) {
                    r.textElement.style.lineHeight = correctedLH;
                  }
                }
              }
            }
            const textNode = sp.childNodes[0];
            if ((textNode == null ? void 0 : textNode.nodeType) === Node.TEXT_NODE && textNode.length > 0) {
              const inf = canvasInfo.get((pageForCalib == null ? void 0 : pageForCalib.cIdx) ?? 0);
              const csy = (inf == null ? void 0 : inf.scaleY) ?? 1;
              const coy = (inf == null ? void 0 : inf.offsetTop) ?? 0;
              const blCorr = calibFontSize * 0.88;
              const divExpectedTop = (bounds.startY - blCorr) * csy + coy;
              const canvasCharTopInDiv = (bounds.startY - calibFontSize) * csy + coy - divExpectedTop;
              const range = document.createRange();
              range.setStart(textNode, 0);
              range.setEnd(textNode, 1);
              const charRect = range.getBoundingClientRect();
              const divRect = div.getBoundingClientRect();
              const cssCharTopInDiv = charRect.top - divRect.top;
              const topOffset = canvasCharTopInDiv - cssCharTopInDiv;
              if (Math.abs(topOffset) > 0.3) {
                const topStr = topOffset.toFixed(1) + "px";
                for (const r of result) {
                  if (r.textElement) {
                    r.textElement.style.top = topStr;
                  }
                }
              }
            }
          }
        }
      } catch {
      }
    }
    const hlCount = result.filter((r) => r.canHighlight).length;
    console.log(`[weread] 文本核对: ${result.length} 段落, ${hlCount} 可高亮`);
    for (let i = 0; i < result.length; i++) {
      const r = result[i];
      console.log(`  段落${i}: [${r.text.length}字] hl=${r.canHighlight} "${r.text.substring(0, 60)}${r.text.length > 60 ? "..." : ""}"`);
    }
    try {
      const spanDiags = [];
      for (const r of result) {
        if (r.canHighlight && r.textElement) {
          const sp = r.textElement;
          const sH = sp.scrollHeight;
          const oH = sp.offsetHeight;
          const computedLH = getComputedStyle(sp).lineHeight;
          const computedFS = getComputedStyle(sp).fontSize;
          const computedW = getComputedStyle(sp).width;
          spanDiags.push(`sH=${sH}/oH=${oH}/lh=${computedLH}/fs=${computedFS}/w=${computedW}/top=${sp.style.top}`);
        }
      }
      document.documentElement.dataset.castreaderSpanDebug = spanDiags.join(" | ");
    } catch {
    }
    pageDebugLines.push(`→result=${result.length}`);
    try {
      document.documentElement.dataset.castreaderPageDebug = pageDebugLines.join(" | ");
    } catch {
    }
    return result.length > 0 ? result : null;
  }
  function extractFromFillTextPages() {
    const layout = readFillTextLayout();
    if (!(layout == null ? void 0 : layout.pages) || layout.pages.length === 0) {
      console.log("[weread] extractFromFillTextPages: 无 pages 数据");
      return [];
    }
    const globalLineHeight = layout.lineHeight || 10;
    const result = [];
    const canvasContainer = document.querySelector(".wr_canvasContainer");
    const dpr = window.devicePixelRatio || 1;
    const canvasInfo = /* @__PURE__ */ new Map();
    let highlightContainer = null;
    if (canvasContainer) {
      if (getComputedStyle(canvasContainer).position === "static") {
        canvasContainer.style.position = "relative";
      }
      const old = canvasContainer.querySelector(".castreader-wr-highlights");
      if (old) old.remove();
      highlightContainer = document.createElement("div");
      highlightContainer.className = "castreader-wr-highlights";
      highlightContainer.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;";
      canvasContainer.prepend(highlightContainer);
      const containerRect = canvasContainer.getBoundingClientRect();
      const canvases = canvasContainer.querySelectorAll("canvas");
      canvases.forEach((c, i) => {
        const cCanvas = c;
        const scaleX = cCanvas.width > 0 ? cCanvas.offsetWidth * dpr / cCanvas.width : 1;
        const scaleY = cCanvas.height > 0 ? cCanvas.offsetHeight * dpr / cCanvas.height : 1;
        canvasInfo.set(i, {
          offsetLeft: c.getBoundingClientRect().left - containerRect.left,
          offsetTop: c.getBoundingClientRect().top - containerRect.top,
          scaleX,
          scaleY
        });
      });
    }
    console.log(`[weread] extractFromFillTextPages: ${layout.pages.length} 页, globalLineH=${globalLineHeight}`);
    for (const page of layout.pages) {
      if (page.lines.length === 0) continue;
      const yGaps = [];
      for (let i = 1; i < page.lines.length; i++) {
        const g = page.lines[i].y - page.lines[i - 1].y;
        if (g > 0) yGaps.push(g);
      }
      yGaps.sort((a, b) => a - b);
      const medianLineGap = yGaps.length > 0 ? yGaps[Math.floor(yGaps.length / 2)] : globalLineHeight;
      const pageLineHeight = page.lineHeight || medianLineGap;
      const q1Idx = Math.max(0, Math.floor(yGaps.length * 0.25));
      const baseGap = yGaps.length > 0 ? yGaps[q1Idx] : medianLineGap;
      const paraGapThreshold = baseGap * 1.3;
      const preview = page.lines.slice(0, 3).map((l, i) => `  L${i}: y=${l.y} "${l.t.substring(0, 30)}"`).join("\n");
      console.log(`[weread] page(c${page.cIdx}): ${page.lines.length} 行 lineH=${pageLineHeight} gap=${paraGapThreshold.toFixed(1)}
${preview}`);
      try {
        const gapsSample = yGaps.slice(0, 8).map((g) => g.toFixed(1)).join(",");
        document.documentElement.dataset.castreaderGapDiag = (document.documentElement.dataset.castreaderGapDiag || "") + `c${page.cIdx}:lines=${page.lines.length},q1=${baseGap.toFixed(1)},med=${medianLineGap.toFixed(1)},thr=${paraGapThreshold.toFixed(1)},gaps=[${gapsSample}] | `;
      } catch {
      }
      const pageTextLeft = page.textLeft ?? layout.textLeft;
      const pageTextRight = page.textRight ?? layout.textRight;
      const pageFontSize = page.fontSize || pageLineHeight * 0.55;
      const baselineCorrection = pageFontSize * 0.88;
      const pad = pageFontSize * 0.3;
      const info = canvasInfo.get(page.cIdx);
      const sx = (info == null ? void 0 : info.scaleX) ?? 1;
      const sy = (info == null ? void 0 : info.scaleY) ?? 1;
      const ox = (info == null ? void 0 : info.offsetLeft) ?? 0;
      const oy = (info == null ? void 0 : info.offsetTop) ?? 0;
      const txCssOffset = (page.tx || 0) / dpr;
      let currentLineTexts = [];
      let paraStartY = page.lines[0].y;
      let paraEndY = page.lines[0].y;
      let lastY = page.lines[0].y;
      const flushParagraph = () => {
        if (currentLineTexts.length === 0) return;
        const text = currentLineTexts.join("");
        if (text.length < 3) {
          currentLineTexts = [];
          return;
        }
        if (highlightContainer) {
          const top = (paraStartY - baselineCorrection) * sy + oy;
          const left = (pageTextLeft + txCssOffset - pad) * sx + ox;
          const width = (pageTextRight - pageTextLeft + pageFontSize + pad) * sx;
          const height = (paraEndY + pageLineHeight - paraStartY) * sy;
          const div = document.createElement("div");
          div.dataset.castreaderOverlay = "weread";
          div.style.cssText = `
          position:absolute;
          top:${Math.round(top)}px;
          left:${Math.round(left)}px;
          width:${Math.round(width)}px;
          height:${Math.round(height)}px;
          pointer-events:auto;border-radius:4px;
          transition:background-color 0.3s ease;
        `;
          const textSpan = document.createElement("span");
          textSpan.textContent = text;
          textSpan.style.cssText = `
          font-size: ${Math.round(pageFontSize * sy)}px;
          color: transparent;
          display: block;
          position: absolute;
          top: 0; left: 0;
          width: 100%; height: 100%;
          overflow: hidden;
          pointer-events: none;
          line-height: ${pageLineHeight}px;
          margin: 0; padding: 0; box-sizing: border-box;
        `;
          div.appendChild(textSpan);
          highlightContainer.appendChild(div);
          result.push({ text, element: div, canHighlight: true, textElement: textSpan });
        } else {
          result.push({ text, element: document.body, canHighlight: false });
        }
        currentLineTexts = [];
      };
      for (const line of page.lines) {
        const gap = line.y - lastY;
        if (currentLineTexts.length > 0 && gap > paraGapThreshold) {
          flushParagraph();
          paraStartY = line.y;
        }
        currentLineTexts.push(line.t);
        paraEndY = line.y;
        lastY = line.y;
      }
      flushParagraph();
    }
    if (result.length > 0) {
      console.log(`[weread] fillText 页数据提取: ${layout.pages.length} 页 → ${result.length} 段落`);
      for (let i = 0; i < result.length; i++) {
        const t = result[i].text;
        console.log(`  段落${i}: [${t.length}字] hl=${result[i].canHighlight} "${t.substring(0, 60)}${t.length > 60 ? "..." : ""}"`);
      }
    }
    try {
      const parasSummary = result.map((r, i) => `p${i}:[${r.text.length}字]"${r.text.substring(0, 15)}"`).join(" ");
      document.documentElement.dataset.castreaderFillResult = `pages=${layout.pages.length},paras=${result.length} ${parasSummary}`;
    } catch {
    }
    return result;
  }
  function matchParagraphsToLines(texts, lines, lineHeight) {
    const charToLine = [];
    let fullClean = "";
    for (let li = 0; li < lines.length; li++) {
      const clean2 = lines[li].t.replace(/\s/g, "");
      for (let ci = 0; ci < clean2.length; ci++) {
        charToLine.push(li);
      }
      fullClean += clean2;
    }
    const result = [];
    const startLineIndices = [];
    let searchFrom = 0;
    for (let pi = 0; pi < texts.length; pi++) {
      const paraClean = texts[pi].replace(/\s/g, "");
      const prefix = paraClean.substring(0, 8);
      if (prefix.length < 3) {
        startLineIndices.push(-1);
        continue;
      }
      const pos = fullClean.indexOf(prefix, searchFrom);
      if (pos >= 0) {
        const lineIdx = charToLine[pos];
        startLineIndices.push(lineIdx);
        searchFrom = pos + Math.max(prefix.length, paraClean.length - 20);
      } else {
        startLineIndices.push(-1);
      }
    }
    for (let pi = 0; pi < texts.length; pi++) {
      const startLine = startLineIndices[pi];
      if (startLine < 0) {
        result.push({ startY: -1, endY: -1 });
        continue;
      }
      let nextStartLine = lines.length;
      for (let pj = pi + 1; pj < texts.length; pj++) {
        if (startLineIndices[pj] >= 0) {
          nextStartLine = startLineIndices[pj];
          break;
        }
      }
      const endLine = nextStartLine - 1;
      const startY = lines[startLine].y;
      const endY = lines[Math.min(endLine, lines.length - 1)].y + lineHeight;
      result.push({ startY, endY });
    }
    const matched = startLineIndices.filter((i) => i >= 0).length;
    console.log(
      `[weread] 行级匹配: ${matched}/${texts.length} 段落找到起始行`,
      `| fullClean长度=${fullClean.length}`,
      startLineIndices.slice(0, 5).map((li, pi) => li >= 0 ? `p${pi}→L${li}(Y=${lines[li].y})` : `p${pi}→✗`).join(", ")
    );
    if (matched < texts.length) {
      const misses = startLineIndices.map((li, pi) => li < 0 ? `p${pi}:"${texts[pi].replace(/\s/g, "").substring(0, 12)}"` : null).filter(Boolean).slice(0, 5);
      console.log(`[weread] 未匹配段落:`, misses.join(", "));
    }
    return result;
  }
  function detectCurrentPageColumns(allPositions, containerWidth, canvasContainer, liveTexts) {
    var _a, _b;
    const stride = containerWidth;
    const drawAttr = document.documentElement.getAttribute("data-castreader-wr-draws");
    console.log(`[weread-diag] drawImage attr: ${drawAttr ? `${drawAttr.length}字符` : "无"}`);
    if (drawAttr) {
      try {
        const draws = JSON.parse(drawAttr);
        console.log(
          `[weread-diag] drawImage entries: ${draws.length}`,
          draws.slice(-4).map((d) => `c${d.idx} sx=${d.sx} sw=${d.sw}`).join(" | ")
        );
        const canvas0Draws = draws.filter((d) => d.idx === 0 && d.sw > 100);
        const canvas1Draws = draws.filter((d) => d.idx === 1 && d.sw > 100);
        if (canvas0Draws.length > 0) {
          const lastDraw = canvas0Draws[canvas0Draws.length - 1];
          const dpr = window.devicePixelRatio || 1;
          const sxCss = lastDraw.sx / dpr;
          const startCol = Math.max(0, Math.round(sxCss / stride));
          console.log(
            `[weread] 当前页(drawImage): canvas0 sx=${lastDraw.sx} (CSS ${sxCss.toFixed(0)}) stride=${stride} → col=${startCol}`,
            canvas1Draws.length > 0 ? `canvas1 sx=${canvas1Draws[canvas1Draws.length - 1].sx}` : ""
          );
          return startCol;
        } else {
          console.log("[weread-diag] drawImage: 无 canvas0 有效 draw");
        }
      } catch (e) {
        console.log("[weread] drawImage 数据解析失败:", e);
      }
    }
    const layout = readFillTextLayout();
    if (layout && layout.lines.length >= 3) {
      const result = detectColumnsFromFillTextFragments(layout, allPositions, stride);
      if (result !== null) return result;
      console.log("[weread] fillText 片段匹配失败，尝试其他策略");
    }
    function checkMultiColElement(el, label) {
      const style = getComputedStyle(el);
      const isMultiCol = style.columnWidth !== "auto" || style.columnCount !== "auto" && style.columnCount !== "1";
      if (isMultiCol || el.scrollWidth > stride * 3) {
        let tx = 0;
        if (style.transform && style.transform !== "none") {
          const m = style.transform.match(/matrix\(([^)]+)\)/);
          if (m) {
            const vals = m[1].split(",").map((s) => parseFloat(s.trim()));
            tx = vals[4] || 0;
          }
        }
        if (Math.abs(tx) > 1 || el.scrollLeft > 1) {
          const offset = Math.abs(tx) > 1 ? Math.abs(tx) : el.scrollLeft;
          const startCol = Math.max(0, Math.round(offset / stride));
          console.log(`[weread] 当前页(${label}): tx=${tx} scrollLeft=${el.scrollLeft} → col=${startCol}`);
          return startCol;
        }
        console.log(`[weread] 当前页(${label}): multiCol 存在但无偏移，跳过`);
      }
      if (style.transform && style.transform !== "none") {
        const m = style.transform.match(/matrix\(([^)]+)\)/);
        if (m) {
          const vals = m[1].split(",").map((s) => parseFloat(s.trim()));
          const tx = vals[4] || 0;
          if (Math.abs(tx) > stride) {
            const startCol = Math.max(0, Math.round(Math.abs(tx) / stride));
            console.log(`[weread] 当前页(${label} transform): tx=${tx} → col=${startCol}`);
            return startCol;
          }
        }
      }
      return null;
    }
    for (const sel of [".preRenderContainer", "#preRenderContent"]) {
      const el = document.querySelector(sel);
      if (!el) continue;
      const result = checkMultiColElement(el, sel);
      if (result !== null) return result;
      if (el.parentElement) {
        const parentResult = checkMultiColElement(el.parentElement, `${sel} parent`);
        if (parentResult !== null) return parentResult;
      }
    }
    for (const sel of [".readerChapterContent", ".wr_readerContent"]) {
      const container = document.querySelector(sel);
      if (!container) continue;
      for (const child of Array.from(container.children)) {
        if (!(child instanceof HTMLElement)) continue;
        const result = checkMultiColElement(child, `${sel}>${child.className.substring(0, 20) || child.tagName}`);
        if (result !== null) return result;
      }
    }
    const ancestors = [];
    let p = canvasContainer.parentElement;
    while (p && p !== document.body) {
      ancestors.push(p);
      p = p.parentElement;
    }
    for (const el of ancestors) {
      if (el.scrollLeft > stride * 0.5) {
        const startCol = Math.round(el.scrollLeft / stride);
        console.log(`[weread] 当前页(ancestor scroll): ${el.className.substring(0, 30)} → col=${startCol}`);
        return startCol;
      }
    }
    for (const sel of [".readerChapterContent", ".wr_readerContent"]) {
      const container = document.querySelector(sel);
      if (!container) continue;
      const blocks = container.querySelectorAll("p, h1, h2, h3, h4, h5, h6");
      const domTexts = [];
      for (const block of blocks) {
        const text = (_a = block.textContent) == null ? void 0 : _a.trim();
        if (text && text.length >= 3) domTexts.push(text);
      }
      if (domTexts.length >= 2) {
        const colVotes = matchTextsToColumns(domTexts.slice(0, 50), allPositions, stride);
        if (colVotes.size > 0) {
          const sorted = [...colVotes.entries()].sort((a, b) => b[1] - a[1]);
          const topTwo = sorted.slice(0, 2).reduce((s, [, n]) => s + n, 0);
          const total = sorted.reduce((s, [, n]) => s + n, 0);
          if (total > 0 && topTwo >= total * 0.5) {
            const startCol = Math.min(...sorted.slice(0, 2).map(([col]) => col));
            console.log(
              `[weread] 当前页(hiddenDOM): ${domTexts.length} blocks,`,
              `${sorted.slice(0, 5).map(([c, n]) => `c${c}:${n}`).join(" ")} → col=${startCol}`
            );
            return startCol;
          }
          console.log(`[weread] hiddenDOM 投票分散(${colVotes.size}列): ${sorted.slice(0, 5).map(([c, n]) => `c${c}:${n}`).join(" ")}`);
        }
      }
    }
    const canvasRect = canvasContainer.getBoundingClientRect();
    for (const selector of [".readerChapterContent", ".wr_readerContent", ".readerContent"]) {
      const contentEl = document.querySelector(selector);
      if (!contentEl) continue;
      const blocks = contentEl.querySelectorAll("p, h1, h2, h3, h4, h5, h6");
      const visibleTexts = [];
      for (const block of blocks) {
        const rect = block.getBoundingClientRect();
        if (rect.width > 10 && rect.height > 0 && rect.left < canvasRect.right + 50 && rect.right > canvasRect.left - 50 && rect.top < canvasRect.bottom + 50 && rect.bottom > canvasRect.top - 50) {
          const text = (_b = block.textContent) == null ? void 0 : _b.trim();
          if (text && text.length >= 3) visibleTexts.push(text);
        }
      }
      if (visibleTexts.length >= 2) {
        const colVotes = matchTextsToColumns(visibleTexts.slice(0, 20), allPositions, stride);
        if (colVotes.size > 0) {
          const sorted = [...colVotes.entries()].sort((a, b) => b[1] - a[1]);
          const startCol = Math.min(...sorted.slice(0, 2).map(([col]) => col));
          console.log(`[weread] 当前页(viewport): visible=${visibleTexts.length} ${sorted.map(([c, n]) => `c${c}:${n}`).join(" ")} → col=${startCol}`);
          return startCol;
        }
      }
    }
    const preRender = document.querySelector(".preRenderContainer");
    const preRenderInfo = preRender ? `存在(${preRender.offsetWidth}x${preRender.offsetHeight} scrollW=${preRender.scrollWidth} children=${preRender.children.length})` : "不存在";
    const readerChapter = document.querySelector(".readerChapterContent");
    const rcBlocks = (readerChapter == null ? void 0 : readerChapter.querySelectorAll("p, h1, h2, h3, h4, h5, h6").length) || 0;
    console.log(
      "[weread] 当前页检测全部失败:",
      `
  preRenderContainer: ${preRenderInfo}`,
      `
  readerChapterContent: ${rcBlocks} blocks`,
      `
  ancestors: ${ancestors.map((a) => a.className.substring(0, 20) || a.tagName).join(" > ")}`,
      `
  liveTexts: ${0}`,
      `
  positions: ${allPositions.length}`
    );
    return null;
  }
  function matchTextsToColumns(texts, positions, stride) {
    const colVotes = /* @__PURE__ */ new Map();
    for (const vt of texts) {
      const prefix = vt.replace(/\s/g, "").substring(0, 15);
      if (prefix.length < 3) continue;
      for (const pos of positions) {
        const pClean = pos.text.replace(/\s/g, "");
        if (pClean.startsWith(prefix) || prefix.startsWith(pClean.substring(0, 15))) {
          const col = Math.floor(pos.left / (stride + 1));
          colVotes.set(col, (colVotes.get(col) || 0) + 1);
          break;
        }
      }
    }
    return colVotes;
  }
  function detectColumnsFromFillTextFragments(layout, allPositions, stride) {
    const FRAG_LEN = 8;
    const FRAG_STEP = 6;
    const MAX_FRAGS_PER_PAGE = 40;
    const matchedPositions = /* @__PURE__ */ new Set();
    function matchLinesPerPage(lines, label, maxFrags) {
      const votes = /* @__PURE__ */ new Map();
      let fragCount = 0;
      let matched = 0;
      for (const line of lines) {
        if (fragCount >= maxFrags) break;
        const clean2 = line.t.replace(/\s/g, "");
        if (clean2.length < FRAG_LEN) continue;
        for (let i = 0; i + FRAG_LEN <= clean2.length && fragCount < maxFrags; i += FRAG_STEP) {
          const frag = clean2.substring(i, i + FRAG_LEN);
          fragCount++;
          for (let pi = 0; pi < allPositions.length; pi++) {
            if (matchedPositions.has(pi)) continue;
            const pClean = allPositions[pi].text.replace(/\s/g, "");
            if (pClean.includes(frag)) {
              matchedPositions.add(pi);
              const col = Math.floor(allPositions[pi].left / (stride + 1));
              votes.set(col, (votes.get(col) || 0) + 1);
              matched++;
              break;
            }
          }
        }
      }
      if (fragCount > 0) {
        const sorted = [...votes.entries()].sort((a, b) => b[1] - a[1]);
        console.log(
          `[weread] fillText片段(${label}): ${fragCount} 片段, ${matched} 匹配,`,
          `投票: ${sorted.map(([c, n]) => `col${c}:${n}`).join(" ") || "无"}`
        );
      }
      return { votes, matched, frags: fragCount };
    }
    const pageResults = [];
    const lineSets = layout.pages && layout.pages.length >= 1 ? layout.pages.map((p) => ({ label: `page(c${p.cIdx}/tx${p.tx})`, lines: p.lines })) : [{ label: "merged", lines: layout.lines }];
    for (const { label, lines } of lineSets) {
      const result = matchLinesPerPage(lines, label, MAX_FRAGS_PER_PAGE);
      if (result.matched > 0) {
        pageResults.push({ label, ...result });
      }
    }
    if (pageResults.length === 0) return null;
    const totalMatched = pageResults.reduce((s, pr) => s + pr.matched, 0);
    const totalFrags = pageResults.reduce((s, pr) => s + pr.frags, 0);
    if (totalFrags > 0 && totalMatched < Math.max(5, totalFrags * 0.1)) {
      console.log(`[weread] fillText片段匹配率太低: ${totalMatched}/${totalFrags} (${(totalMatched / totalFrags * 100).toFixed(1)}%), 跳过`);
      return null;
    }
    const colVotes = /* @__PURE__ */ new Map();
    for (const pr of pageResults) {
      const totalVotes = [...pr.votes.values()].reduce((s, n) => s + n, 0);
      const maxVotes = Math.max(...pr.votes.values());
      const concentration = totalVotes > 0 ? maxVotes / totalVotes : 0;
      if (concentration >= 0.4 || totalVotes <= 2) {
        for (const [col, n] of pr.votes) {
          colVotes.set(col, (colVotes.get(col) || 0) + n);
        }
      } else {
        console.log(`[weread] 过滤 garbled 页 ${pr.label}: 集中度=${(concentration * 100).toFixed(0)}% (${totalVotes}票分${pr.votes.size}列)`);
      }
    }
    if (colVotes.size === 0) return null;
    let bestStartCol = -1;
    let bestPairVotes = 0;
    for (const [col, votes] of colVotes) {
      const adjacentVotes = colVotes.get(col + 1) || 0;
      const pairVotes = votes + adjacentVotes;
      if (pairVotes > bestPairVotes) {
        bestPairVotes = pairVotes;
        bestStartCol = col;
      }
    }
    if (bestStartCol >= 0) {
      const sorted = [...colVotes.entries()].sort((a, b) => b[1] - a[1]);
      console.log(
        `[weread] 当前页(fillText片段): ${sorted.slice(0, 5).map(([c, n]) => `col${c}:${n}`).join(" ")}`,
        `→ 最佳相邻对: col${bestStartCol}+${bestStartCol + 1} (${bestPairVotes}票)`
      );
      return bestStartCol;
    }
    return null;
  }
  function filterPositionsToPage(allPositions, startCol, containerWidth) {
    const endCol = startCol + 1;
    const filtered = allPositions.filter((p) => {
      const col = Math.floor(p.left / (containerWidth + 1));
      return col === startCol || col === endCol;
    }).sort((a, b) => {
      const colA = Math.floor(a.left / (containerWidth + 1));
      const colB = Math.floor(b.left / (containerWidth + 1));
      if (colA !== colB) return colA - colB;
      return a.relTop - b.relTop;
    });
    const startColLefts = filtered.filter((p) => Math.floor(p.left / (containerWidth + 1)) === startCol).map((p) => p.left);
    const leftOffset = startColLefts.length > 0 ? Math.min(...startColLefts) : startCol * containerWidth;
    return filtered.map((p) => ({
      ...p,
      left: p.left - leftOffset,
      // 跨列段落的 width 可能 > containerWidth，cap 到单列宽
      width: Math.min(p.width, containerWidth)
    }));
  }
  function createCanvasHighlightOverlays(texts, liveTexts) {
    var _a, _b, _c, _d, _e, _f, _g;
    const canvasContainer = document.querySelector(".wr_canvasContainer");
    if (!(canvasContainer == null ? void 0 : canvasContainer.parentElement)) {
      console.log("[weread] Canvas 高亮：未找到 wr_canvasContainer");
      return [];
    }
    const cache = globalThis.__castreader_weread_cache__;
    try {
      const _ftL = readFillTextLayout();
      const _dbgPath = ((_a = cache == null ? void 0 : cache.paragraphPositions) == null ? void 0 : _a.length) ? "DOM-measured" : ((_b = _ftL == null ? void 0 : _ftL.lines) == null ? void 0 : _b.length) ? "fillText" : "estimated";
      document.documentElement.dataset.castreaderOverlayDebug = JSON.stringify({
        path: _dbgPath,
        cachePositions: ((_c = cache == null ? void 0 : cache.paragraphPositions) == null ? void 0 : _c.length) ?? 0,
        cacheW: (cache == null ? void 0 : cache.containerWidth) ?? null,
        cacheH: (cache == null ? void 0 : cache.containerHeight) ?? null,
        ftLineH: (_ftL == null ? void 0 : _ftL.lineHeight) ?? null,
        ftFontSize: ((_e = (_d = _ftL == null ? void 0 : _ftL.pages) == null ? void 0 : _d[0]) == null ? void 0 : _e.fontSize) ?? null,
        ftLines: ((_f = _ftL == null ? void 0 : _ftL.lines) == null ? void 0 : _f.length) ?? 0
      });
    } catch {
    }
    if ((cache == null ? void 0 : cache.paragraphPositions) && cache.paragraphPositions.length > 0) {
      const positions = cache.paragraphPositions;
      const cw = cache.containerWidth || 0;
      if (isCanvasDualColumn(canvasContainer) && cw > 0) {
        const startCol = detectCurrentPageColumns(positions, cw, canvasContainer);
        if (startCol !== null) {
          const filtered = filterPositionsToPage(positions, startCol, cw);
          if (filtered.length > 0) {
            const filteredTexts = filtered.map((p) => p.text);
            console.log(
              `[weread] 双栏过滤: cols=[${startCol},${startCol + 1}],`,
              `${positions.length} → ${filtered.length} 位置,`,
              `文本: "${(_g = filteredTexts[0]) == null ? void 0 : _g.substring(0, 30)}..."`
            );
            return createDomMeasuredOverlays(
              filteredTexts,
              canvasContainer,
              filtered,
              cache.containerHeight || 0,
              cw,
              { startCol }
            );
          }
        }
      }
      return createDomMeasuredOverlays(texts, canvasContainer, positions, cache.containerHeight || 0, cw);
    }
    const layout = readFillTextLayout();
    if (layout && layout.lines.length > 0) {
      return createFillTextOverlays(texts, canvasContainer, layout);
    }
    console.log("[weread] 无精确数据，使用估算模式");
    return createEstimatedOverlays(texts, canvasContainer);
  }
  function matchTextsToPositions(texts, positions) {
    const stripLeadingPunct = (s) => s.replace(/^[^\p{L}\p{N}]+/u, "");
    const used = /* @__PURE__ */ new Set();
    return texts.map((text) => {
      const cleanText2 = text.replace(/\s/g, "");
      const prefix = cleanText2.substring(0, 12);
      let match = positions.find((p) => {
        if (used.has(p)) return false;
        const pClean = p.text.replace(/\s/g, "");
        return pClean.startsWith(prefix) || prefix.startsWith(pClean.substring(0, 12));
      });
      if (!match) {
        const strippedPrefix = stripLeadingPunct(cleanText2).substring(0, 12);
        if (strippedPrefix.length >= 3) {
          match = positions.find((p) => {
            if (used.has(p)) return false;
            const pStripped = stripLeadingPunct(p.text.replace(/\s/g, ""));
            return pStripped.startsWith(strippedPrefix) || strippedPrefix.startsWith(pStripped.substring(0, 12));
          });
        }
      }
      if (match) used.add(match);
      return match || null;
    });
  }
  function createDomMeasuredOverlays(texts, canvasContainer, positions, containerHeight, containerWidth, pageFilter) {
    var _a, _b, _c, _d, _e, _f, _g, _h;
    const anchor = canvasContainer;
    if (getComputedStyle(anchor).position === "static") {
      anchor.style.position = "relative";
    }
    const canvasW = anchor.offsetWidth || 798;
    const ftLayout = readFillTextLayout();
    const canvasLineH = (ftLayout == null ? void 0 : ftLayout.lineHeight) || 0;
    const canvasEls = anchor.querySelectorAll("canvas");
    if (ftLayout && ftLayout.pages && ftLayout.pages.length > 1) {
      const pageRanges = ftLayout.pages.filter((p) => p.tx < 50).map((p) => {
        const ys = p.lines.map((l) => l.y);
        return { page: p, minY: Math.min(...ys), maxY: Math.max(...ys) };
      }).sort((a, b) => a.minY - b.minY);
      const overlapping = pageRanges.length >= 2 && pageRanges.some((r, i) => i > 0 && r.minY < pageRanges[i - 1].maxY * 0.5);
      if (!overlapping) {
        const mergedLines = [];
        let bestFontSize = ftLayout.fontSize;
        let bestLineHeight = ftLayout.lineHeight;
        for (const { page } of pageRanges) {
          for (const line of page.lines) {
            mergedLines.push({ y: line.y, t: line.t });
          }
          if (page.lineHeight) bestLineHeight = page.lineHeight;
          if (page.fontSize) bestFontSize = page.fontSize;
        }
        mergedLines.sort((a, b) => a.y - b.y);
        ftLayout.lines = mergedLines;
        if (bestLineHeight) ftLayout.lineHeight = bestLineHeight;
        if (bestFontSize) ftLayout.fontSize = bestFontSize;
      } else {
        const primaryPage = pageRanges.sort((a, b) => b.page.lines.length - a.page.lines.length)[0];
        if (primaryPage) {
          ftLayout.lines = primaryPage.page.lines;
          if (primaryPage.page.lineHeight) ftLayout.lineHeight = primaryPage.page.lineHeight;
          if (primaryPage.page.fontSize) ftLayout.fontSize = primaryPage.page.fontSize;
        }
      }
    }
    const cssLineH = (_c = (_b = (_a = positions[0]) == null ? void 0 : _a.fontStyle) == null ? void 0 : _b.match(/line-height:\s*([\d.]+)px/)) == null ? void 0 : _c[1];
    const cssLineHPx = cssLineH ? parseFloat(cssLineH) : 0;
    const lineHeightDiffers = canvasLineH > 0 && cssLineHPx > 0 && Math.abs(canvasLineH - cssLineHPx) > 0.5;
    let ftBounds = null;
    if (lineHeightDiffers && ftLayout && ftLayout.lines.length > 0) {
      ftBounds = matchParagraphsToLines(texts, ftLayout.lines, canvasLineH);
    }
    const isDualColumn2 = isCanvasDualColumn(anchor);
    const canvasCount = isDualColumn2 ? anchor.querySelectorAll("canvas").length : 1;
    const pageWidth = isDualColumn2 ? canvasW / canvasCount : canvasW;
    const scaleX = containerWidth > 0 ? pageWidth / containerWidth : 1;
    let col2Start = containerWidth;
    if (isDualColumn2 && positions.length > 0) {
      const col2Lefts = positions.filter((p) => p.left > containerWidth * 0.5).map((p) => p.left);
      if (col2Lefts.length > 0) {
        col2Start = Math.min(...col2Lefts);
      }
    }
    const oldContainer = anchor.querySelector(".castreader-wr-highlights");
    if (oldContainer) oldContainer.remove();
    const canvasH = anchor.offsetHeight || 1;
    const cache2 = globalThis.__castreader_weread_cache__;
    const nonTextElements = (cache2 == null ? void 0 : cache2.nonTextElements) || [];
    const sortedNtes = [...nonTextElements].sort((a, b) => a.relTop - b.relTop);
    const imageDiffs = [];
    for (const nte of sortedNtes) {
      if (nte.tag !== "img") continue;
      const e = nte;
      const maxW = parseFloat(e.cssMaxWidth) || 0;
      const maxH = parseFloat(e.cssMaxHeight) || 0;
      if (maxW <= 0 || maxH <= 0) continue;
      const cssH = nte.height;
      const imgRenderW = Math.min(maxW, canvasW);
      const canvasH_img = Math.min(maxH * imgRenderW / maxW, cssH);
      const diff = canvasH_img - cssH;
      if (Math.abs(diff) > 0.5) {
        imageDiffs.push({ relTop: nte.relTop, cssH, diff });
      }
    }
    function getImageCorrection(relTop) {
      let correction = 0;
      for (const img of imageDiffs) {
        const boundary = img.relTop + img.cssH;
        if (relTop > boundary) {
          correction += img.diff;
        }
      }
      return correction;
    }
    function getCanvasTop(pos) {
      return pos.relTop * scaleX + (isDualColumn2 ? 0 : getImageCorrection(pos.relTop));
    }
    const highlightContainer = document.createElement("div");
    highlightContainer.className = "castreader-wr-highlights";
    highlightContainer.style.cssText = "position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;";
    anchor.prepend(highlightContainer);
    try {
      const _cssLH = ((_f = (_e = (_d = positions[0]) == null ? void 0 : _d.fontStyle) == null ? void 0 : _e.match(/line-height:\s*([^;]+)/)) == null ? void 0 : _f[1]) || "N/A";
      const _canvasOffsets = Array.from(canvasEls).map((c, i) => `c${i}@${c.offsetTop}h${c.offsetHeight}`).join(",");
      const _ftPages = ((_g = ftLayout == null ? void 0 : ftLayout.pages) == null ? void 0 : _g.map((p) => `c${p.cIdx}:${p.lines.length}L`).join(",")) || "N/A";
      document.documentElement.dataset.castreaderDomDebug = JSON.stringify({
        canvasW,
        canvasH,
        containerW: containerWidth,
        containerH: containerHeight,
        scaleX: +scaleX.toFixed(4),
        canvasLineH,
        cssLineHeight: _cssLH,
        isDual: isDualColumn2,
        positions: positions.length,
        texts: texts.length,
        canvases: canvasEls.length,
        canvasOffsets: _canvasOffsets,
        ftPages: _ftPages,
        ftLinesTotal: (ftLayout == null ? void 0 : ftLayout.lines.length) || 0
      });
    } catch {
    }
    const matchResults = matchTextsToPositions(texts, positions);
    const matchedTotal = matchResults.filter((m) => m !== null).length;
    const ftMatchedTotal = ftBounds ? ftBounds.filter((b) => b.startY >= 0).length : 0;
    try {
      document.documentElement.dataset.castreaderMatchStats = `texts=${texts.length} pos=${positions.length} matched=${matchedTotal} ftMatched=${ftMatchedTotal}`;
    } catch {
    }
    const result = [];
    const overlayDivs = [];
    const firefoxImgs = [];
    let perTextDelta = 0;
    let ffPosSorted = [];
    let ffPrefixHeights = [0];
    if (lineHeightDiffers) {
      let totalImgDelta = 0;
      for (const nte of sortedNtes) {
        if (nte.tag !== "img") continue;
        const e = nte;
        const maxW = parseFloat(e.cssMaxWidth) || 0;
        const maxH = parseFloat(e.cssMaxHeight) || 0;
        if (maxW <= 0 || maxH <= 0) continue;
        const cssH = nte.height;
        const imgRenderW = Math.min(maxW, canvasW);
        const canvasImgH = Math.min(maxH * imgRenderW / maxW, cssH);
        firefoxImgs.push({ boundary: nte.relTop + cssH, cssH, canvasImgH });
        totalImgDelta += canvasImgH - cssH;
      }
      ffPosSorted = [...positions].sort((a, b) => a.relTop - b.relTop);
      const totalTextHeight = ffPosSorted.reduce((sum, p) => sum + p.height, 0);
      const textDelta = canvasH - containerHeight - totalImgDelta;
      perTextDelta = totalTextHeight > 0 ? textDelta / totalTextHeight : 0;
      ffPrefixHeights = [0];
      for (let j = 0; j < ffPosSorted.length; j++) {
        ffPrefixHeights.push(ffPrefixHeights[j] + ffPosSorted[j].height);
      }
    }
    function getFirefoxTop(relTop) {
      let cumTextHeight = 0;
      for (let j = 0; j < ffPosSorted.length; j++) {
        if (ffPosSorted[j].relTop + ffPosSorted[j].height <= relTop) {
          cumTextHeight = ffPrefixHeights[j + 1];
        } else {
          break;
        }
      }
      let imgCorr = 0;
      for (const img of firefoxImgs) {
        if (relTop > img.boundary) {
          imgCorr += img.canvasImgH - img.cssH;
        }
      }
      return relTop + perTextDelta * cumTextHeight + imgCorr;
    }
    try {
      const totalTextH = ffPosSorted.reduce((s, p) => s + p.height, 0);
      document.documentElement.dataset.castreaderMapDiag = `scaleX=${scaleX.toFixed(4)} perTextDelta=${perTextDelta.toFixed(6)} totalTextH=${totalTextH.toFixed(0)} canvasH=${canvasH} containerH=${containerHeight.toFixed(0)} nImgs=${firefoxImgs.length} nPos=${ffPosSorted.length} lineHDiff=${lineHeightDiffers}`;
    } catch {
    }
    for (let i = 0; i < texts.length; i++) {
      const text = texts[i];
      const pos = matchResults[i];
      if (pos) {
        let absTop, absLeft, absWidth, absHeight;
        if (isDualColumn2 && pos.left > col2Start * 0.8) {
          const localLeft = pos.left - col2Start;
          if (lineHeightDiffers) {
            absTop = getFirefoxTop(pos.relTop);
            absHeight = pos.height * (1 + perTextDelta);
          } else {
            absTop = pos.relTop * scaleX;
            absHeight = pos.height * scaleX;
          }
          absLeft = localLeft * scaleX + pageWidth;
          absWidth = pos.width * scaleX;
        } else {
          const leftPad2 = isDualColumn2 ? 0 : 8;
          const cssTop = getCanvasTop(pos);
          if (lineHeightDiffers) {
            absTop = getFirefoxTop(pos.relTop);
            absHeight = pos.height * (1 + perTextDelta);
          } else {
            absTop = cssTop;
            absHeight = pos.height * scaleX;
          }
          absLeft = pos.left * scaleX - leftPad2;
          absWidth = pos.width * scaleX + leftPad2;
        }
        const div = document.createElement("div");
        div.dataset.castreaderOverlay = "weread";
        div.style.cssText = `
        position: absolute;
        top: ${absTop.toFixed(1)}px;
        left: ${absLeft.toFixed(1)}px;
        width: ${absWidth.toFixed(1)}px;
        height: ${absHeight.toFixed(1)}px;
        pointer-events: auto;
        border-radius: 4px;
        transition: background-color 0.3s ease;
      `;
        let textSpan;
        const leftPad = isDualColumn2 ? 0 : 8;
        if (pos.fontStyle && !isDualColumn2) {
          textSpan = document.createElement("span");
          if (pos.footnotes && pos.footnotes.length > 0) {
            let html = "";
            let lastIdx = 0;
            for (let fi = 0; fi < pos.footnotes.length; fi++) {
              const fn = pos.footnotes[fi];
              const safeIdx = Math.max(lastIdx, Math.min(fn.charIndex, text.length));
              if (safeIdx > lastIdx) {
                html += escapeHtml(text.substring(lastIdx, safeIdx));
              }
              const spacerW = (fn.width * scaleX).toFixed(1);
              html += `<span style="display:inline-block;width:${spacerW}px"></span>`;
              lastIdx = safeIdx;
            }
            if (lastIdx < text.length) {
              html += escapeHtml(text.substring(lastIdx));
            }
            textSpan.innerHTML = html;
          } else {
            textSpan.textContent = text;
          }
          const textWidth = (pos.width * scaleX).toFixed(1);
          let effectiveFontStyle = pos.fontStyle;
          if (canvasLineH > 0) {
            effectiveFontStyle = effectiveFontStyle.replace(
              /line-height:[^;]+/,
              `line-height:${canvasLineH}px`
            );
          }
          textSpan.style.cssText = `
          ${effectiveFontStyle};
          color: transparent;
          display: block;
          position: absolute;
          top: 0px;
          left: ${leftPad}px;
          width: ${textWidth}px;
          height: 100%;
          overflow: hidden;
          pointer-events: none;
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        `;
          div.appendChild(textSpan);
        }
        highlightContainer.appendChild(div);
        result.push({ text, element: div, canHighlight: true, textElement: textSpan });
        overlayDivs.push({
          div,
          posIndex: i,
          fTop: canvasH > 0 ? absTop / canvasH : 0,
          fLeft: canvasW > 0 ? absLeft / canvasW : 0,
          fWidth: canvasW > 0 ? absWidth / canvasW : 0,
          fHeight: canvasH > 0 ? absHeight / canvasH : 0,
          textSpan,
          leftPad
        });
      } else {
        result.push({ text, element: document.body, canHighlight: false });
      }
    }
    if (lineHeightDiffers && ftBounds) {
      try {
        const fontSize = (ftLayout == null ? void 0 : ftLayout.fontSize) || 21;
        const calibEntry = overlayDivs.find((e) => {
          if (!e.textSpan) return false;
          const fb = ftBounds[e.posIndex];
          return fb && fb.startY >= 0 && fb.endY - fb.startY > canvasLineH * 1.5;
        });
        if (calibEntry == null ? void 0 : calibEntry.textSpan) {
          const sp = calibEntry.textSpan;
          const fb = ftBounds[calibEntry.posIndex];
          const expectedLines = Math.round((fb.endY - fb.startY) / canvasLineH);
          if (expectedLines > 1) {
            const sH = sp.scrollHeight;
            const actualLineH = sH / expectedLines;
            const lineDrift = actualLineH - canvasLineH;
            if (Math.abs(lineDrift) > 0.05) {
              const correctedLH = (canvasLineH - lineDrift).toFixed(2) + "px";
              for (const entry of overlayDivs) {
                if (entry.textSpan) {
                  entry.textSpan.style.lineHeight = correctedLH;
                }
              }
            }
          }
          const textNode = sp.childNodes[0];
          if ((textNode == null ? void 0 : textNode.nodeType) === Node.TEXT_NODE && textNode.length > 0) {
            const calibPos = matchResults[calibEntry.posIndex];
            const divTop = getFirefoxTop(calibPos.relTop);
            const canvasCharTopInDiv = fb.startY - fontSize - divTop;
            const range = document.createRange();
            range.setStart(textNode, 0);
            range.setEnd(textNode, 1);
            const charRect = range.getBoundingClientRect();
            const divRect = calibEntry.div.getBoundingClientRect();
            const cssCharTopInDiv = charRect.top - divRect.top;
            const topOffset = canvasCharTopInDiv - cssCharTopInDiv;
            if (Math.abs(topOffset) > 0.3) {
              const topStr = topOffset.toFixed(1) + "px";
              for (const entry of overlayDivs) {
                if (entry.textSpan) {
                  entry.textSpan.style.top = topStr;
                }
              }
            }
            document.documentElement.dataset.castreaderCalib = `cssCharTop=${cssCharTopInDiv.toFixed(1)} canvasCharTop=${canvasCharTopInDiv.toFixed(1)} topOffset=${topOffset.toFixed(1)} perTextDelta=${perTextDelta.toFixed(6)} fontSize=${fontSize}`;
          }
        }
      } catch {
      }
    }
    let lastVersion = ((_h = globalThis.__castreader_weread_cache__) == null ? void 0 : _h.positionVersion) || 0;
    let refW = canvasW;
    let stopped = false;
    function recalcFractions(entries, positions2, corrFn, sx, containerW, containerH, dualCol) {
      for (const entry of entries) {
        const pos = positions2[entry.posIndex];
        if (pos) {
          let absTop, absLeft, absWidth, absHeight;
          if (dualCol && pos.left > dualCol.c2Start * 0.8) {
            const localLeft = pos.left - dualCol.c2Start;
            absTop = pos.relTop * sx;
            absLeft = localLeft * sx + dualCol.pageW;
            absWidth = pos.width * sx;
            absHeight = pos.height * sx;
          } else {
            const correction = dualCol ? 0 : corrFn(pos.relTop);
            const leftPad = dualCol ? 0 : 8;
            absTop = pos.relTop * sx + correction;
            absLeft = pos.left * sx - leftPad;
            absWidth = pos.width * sx + leftPad;
            absHeight = pos.height * sx;
          }
          entry.fTop = containerH > 0 ? absTop / containerH : 0;
          entry.fLeft = containerW > 0 ? absLeft / containerW : 0;
          entry.fWidth = containerW > 0 ? absWidth / containerW : 0;
          entry.fHeight = containerH > 0 ? absHeight / containerH : 0;
        }
      }
    }
    function buildCorrectionFn(heightDiff, ntes) {
      if (Math.abs(heightDiff) > 2 && ntes.length > 0) {
        const perEl = heightDiff / ntes.length;
        const sorted = [...ntes].sort((a, b) => a.relTop - b.relTop);
        return (relTop) => {
          let corr = 0;
          for (const nte of sorted) {
            if (relTop > nte.relTop + nte.height) corr += perEl;
          }
          return corr;
        };
      }
      return () => 0;
    }
    function remeasureFromHtml(html, targetWidth, anchor2) {
      var _a2;
      try {
        const temp = document.createElement("div");
        temp.className = "preRenderContainer";
        temp.style.cssText = `
        position: absolute; top: 0; left: 0;
        width: ${targetWidth}px;
        visibility: hidden; opacity: 0; pointer-events: none;
        z-index: -9999; overflow: hidden;
      `;
        const tempContent = document.createElement("div");
        tempContent.id = "preRenderContent";
        tempContent.innerHTML = html;
        temp.appendChild(tempContent);
        const insertParent = anchor2.parentElement || document.body;
        insertParent.appendChild(temp);
        const containerRect = temp.getBoundingClientRect();
        const containerHeight2 = Math.max(containerRect.height, temp.scrollHeight || 0);
        const positions2 = [];
        const pElements = tempContent.querySelectorAll("p, h1, h2, h3, h4, h5, h6");
        for (const p of pElements) {
          const text = (_a2 = p.textContent) == null ? void 0 : _a2.trim();
          if (!text || text.length < 2) continue;
          const r = p.getBoundingClientRect();
          if (r.height <= 0) continue;
          const cs = getComputedStyle(p);
          const fontStyle = TEXT_LAYOUT_PROPS.map((prop) => `${prop}:${cs.getPropertyValue(prop)}`).join(";");
          positions2.push({
            text,
            relTop: r.top - containerRect.top,
            height: r.height,
            left: r.left - containerRect.left,
            width: r.width,
            fontStyle
          });
        }
        temp.remove();
        return { positions: positions2, containerHeight: containerHeight2 };
      } catch (e) {
        console.warn("[weread-diag] remeasureFromHtml failed:", e);
        return null;
      }
    }
    function applyFractions(entries, w, h) {
      for (const e of entries) {
        e.div.style.top = `${(e.fTop * h).toFixed(1)}px`;
        e.div.style.left = `${(e.fLeft * w).toFixed(1)}px`;
        const divW = e.fWidth * w;
        e.div.style.width = `${divW.toFixed(1)}px`;
        e.div.style.height = `${(e.fHeight * h).toFixed(1)}px`;
        if (e.textSpan) {
          e.textSpan.style.width = `${(divW - e.leftPad).toFixed(1)}px`;
        }
      }
    }
    function reattachAndUpdate(versionChanged = false) {
      if (stopped) return;
      const currentAnchor = document.querySelector(".wr_canvasContainer");
      if (!currentAnchor) return;
      const rawW = currentAnchor.offsetWidth;
      const rawH = currentAnchor.offsetHeight;
      if (rawW < 50 || rawH < 50) return;
      if (getComputedStyle(currentAnchor).position === "static") {
        currentAnchor.style.position = "relative";
      }
      let container = currentAnchor.querySelector(".castreader-wr-highlights");
      if (!container) {
        container = document.createElement("div");
        container.className = "castreader-wr-highlights";
        container.style.cssText = "position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;";
        currentAnchor.prepend(container);
      }
      for (const { div } of overlayDivs) {
        if (!div.parentElement || div.parentElement !== container) {
          container.appendChild(div);
        }
      }
      const curW = rawW;
      const curH = rawH;
      const isDualColumnNow = isCanvasDualColumn(currentAnchor);
      const canvasCountNow = isDualColumnNow ? currentAnchor.querySelectorAll("canvas").length : 1;
      const pageWidthNow = isDualColumnNow ? curW / canvasCountNow : curW;
      const c = globalThis.__castreader_weread_cache__;
      const cacheW = (c == null ? void 0 : c.containerWidth) || 1;
      const cacheH = (c == null ? void 0 : c.containerHeight) || 1;
      let filteredPositions = c == null ? void 0 : c.paragraphPositions;
      if (filteredPositions && pageFilter && filteredPositions.length > 0) {
        filteredPositions = filterPositionsToPage(filteredPositions, pageFilter.startCol, cacheW);
      }
      const cacheIsFresh = filteredPositions && filteredPositions.length > 0 && (versionChanged || Math.abs(curW - refW) < 5);
      if (cacheIsFresh && filteredPositions && filteredPositions.length > 0) {
        const sx = cacheW > 0 ? pageWidthNow / cacheW : 1;
        const corrFn = buildCorrectionFn(curH - cacheH, (c == null ? void 0 : c.nonTextElements) || []);
        const newMatch = matchTextsToPositions(texts, filteredPositions);
        let dualCol;
        if (isDualColumnNow) {
          const col2Lefts = filteredPositions.filter((p) => p.left > cacheW * 0.5).map((p) => p.left);
          dualCol = { pageW: pageWidthNow, c2Start: col2Lefts.length > 0 ? Math.min(...col2Lefts) : cacheW };
        }
        recalcFractions(overlayDivs, newMatch, corrFn, sx, curW, curH, dualCol);
        refW = curW;
      } else if (!cacheIsFresh && (c == null ? void 0 : c.preRenderHtml) && !isDualColumnNow) {
        const remeasured = remeasureFromHtml(c.preRenderHtml, curW, currentAnchor);
        if (remeasured && remeasured.positions.length > 0) {
          const corrFn = buildCorrectionFn(curH - remeasured.containerHeight, (c == null ? void 0 : c.nonTextElements) || []);
          const newMatch = matchTextsToPositions(texts, remeasured.positions);
          recalcFractions(overlayDivs, newMatch, corrFn, 1, curW, curH);
          refW = curW;
        }
      }
      applyFractions(overlayDivs, curW, curH);
      refW = curW;
      const hasClickHandlers = overlayDivs.some((e) => e.div.style.cursor === "pointer");
      if (hasClickHandlers) {
        currentAnchor.querySelectorAll("canvas").forEach((c2) => {
          c2.style.setProperty("pointer-events", "none");
        });
      }
    }
    const checkInterval = setInterval(() => {
      const inDom = document.querySelector(".wr_canvasContainer");
      if (!inDom) {
        stopped = true;
        clearInterval(checkInterval);
        return;
      }
      const c = globalThis.__castreader_weread_cache__;
      const currentVersion = (c == null ? void 0 : c.positionVersion) || 0;
      const highlightsInDom = !!document.querySelector(".castreader-wr-highlights");
      const curW = inDom.offsetWidth;
      if (curW < 50) return;
      const sizeChanged = Math.abs(curW - refW) > 2;
      const versionBumped = currentVersion > lastVersion;
      if (!highlightsInDom || versionBumped || sizeChanged) {
        if (versionBumped) lastVersion = currentVersion;
        reattachAndUpdate(versionBumped);
      }
    }, 300);
    return result;
  }
  function createFillTextOverlays(texts, canvasContainer, layout) {
    const anchor = canvasContainer;
    if (getComputedStyle(anchor).position === "static") {
      anchor.style.position = "relative";
    }
    const textLeft = layout.textLeft;
    const textWidth = layout.textRight - layout.textLeft;
    console.log(`[weread] fillText模式: ${layout.lines.length} 行 vs ${texts.length} 段落`);
    const paraBounds = matchParagraphsToLines(texts, layout.lines, layout.lineHeight);
    const oldContainer = anchor.querySelector(".castreader-wr-highlights");
    if (oldContainer) oldContainer.remove();
    const highlightContainer = document.createElement("div");
    highlightContainer.className = "castreader-wr-highlights";
    highlightContainer.style.cssText = "position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;";
    anchor.prepend(highlightContainer);
    const result = [];
    for (let pi = 0; pi < texts.length; pi++) {
      const text = texts[pi];
      const bounds = paraBounds[pi];
      if (bounds && bounds.startY >= 0 && bounds.endY > bounds.startY) {
        const paraHeight = bounds.endY - bounds.startY;
        const div = document.createElement("div");
        div.dataset.castreaderOverlay = "weread";
        div.style.cssText = `
        position: absolute;
        top: ${Math.round(bounds.startY)}px;
        left: ${Math.round(textLeft)}px;
        width: ${Math.round(textWidth)}px;
        height: ${Math.round(paraHeight)}px;
        pointer-events: auto;
        border-radius: 4px;
        transition: background-color 0.3s ease;
      `;
        highlightContainer.appendChild(div);
        result.push({ text, element: div, canHighlight: true });
      } else {
        result.push({ text, element: document.body, canHighlight: false });
      }
    }
    const matched = result.filter((r) => r.canHighlight).length;
    console.log(`[weread] fillText模式: ${matched}/${texts.length} 段落有坐标`);
    return result;
  }
  function createEstimatedOverlays(texts, canvasContainer) {
    const anchor = canvasContainer;
    if (getComputedStyle(anchor).position === "static") {
      anchor.style.position = "relative";
    }
    const canvasW = anchor.offsetWidth || 798;
    const canvasHeight = anchor.offsetHeight;
    const textLeft = Math.round(canvasW * 0.07);
    const textWidth = Math.round(canvasW * 0.86);
    const charWidth = 23;
    const charsPerLine = Math.max(20, Math.floor(textWidth / charWidth));
    const paraLines = texts.map((t) => Math.max(1, Math.ceil(t.length / charsPerLine)));
    const totalTextLines = paraLines.reduce((s, l) => s + l, 0);
    const gapLineCount = 0.8;
    const totalGapLines = Math.max(0, texts.length - 1) * gapLineCount;
    const TITLE_LINES = 8;
    const allLines = TITLE_LINES + totalTextLines + totalGapLines;
    const lineHeight = canvasHeight / allLines;
    const gapHeight = lineHeight * gapLineCount;
    const startY = TITLE_LINES * lineHeight;
    console.log(
      `[weread] 估算模式：charsPerLine=${charsPerLine} lineH=${lineHeight.toFixed(1)}px`,
      `textLines=${totalTextLines} titleLines=${TITLE_LINES} startY=${Math.round(startY)}`
    );
    const oldContainer = anchor.querySelector(".castreader-wr-highlights");
    if (oldContainer) oldContainer.remove();
    const highlightContainer = document.createElement("div");
    highlightContainer.className = "castreader-wr-highlights";
    highlightContainer.style.cssText = "position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;";
    anchor.prepend(highlightContainer);
    let currentY = startY;
    const result = [];
    for (let pi = 0; pi < texts.length; pi++) {
      const text = texts[pi];
      const paraHeight = paraLines[pi] * lineHeight;
      const div = document.createElement("div");
      div.dataset.castreaderOverlay = "weread";
      div.style.cssText = `
      position: absolute;
      top: ${Math.round(currentY)}px;
      left: ${textLeft}px;
      width: ${textWidth}px;
      height: ${Math.round(paraHeight)}px;
      pointer-events: auto;
      border-radius: 4px;
      transition: background-color 0.3s ease;
    `;
      highlightContainer.appendChild(div);
      result.push({ text, element: div, canHighlight: true });
      currentY += paraHeight + gapHeight;
    }
    console.log(
      `[weread] 估算模式：创建 ${result.length} 个定位元素`,
      `最终Y: ${Math.round(currentY)}px / canvasH: ${canvasHeight}px`
    );
    return result;
  }
  function extractFromGlobalCache() {
    var _a;
    const cache = globalThis.__castreader_weread_cache__;
    if (!cache) return [];
    if (cache.apiContent && cache.apiContent.length > 0) {
      console.log("[weread] 从 globalThis 缓存提取，段落数:", cache.apiContent.length);
      return cache.apiContent.map((text) => ({
        text,
        element: document.body,
        canHighlight: false
      }));
    }
    if ((_a = cache.pages) == null ? void 0 : _a.length) {
      const allParagraphs = cache.pages.flatMap((p) => p.paragraphs);
      if (allParagraphs.length > 0) {
        console.log("[weread] 从 globalThis DOM 缓存提取，段落数:", allParagraphs.length);
        return allParagraphs.map((text) => ({
          text,
          element: document.body,
          canHighlight: false
        }));
      }
    }
    return [];
  }
  const wereadExtractor = {
    siteName: "微信读书",
    matches: ["weread.qq.com"],
    supportsHighlight() {
      return true;
    },
    /**
     * 从所有数据源收集段落文本（不含 DOM 元素引用）
     */
    getAllCachedTexts() {
      var _a;
      const cache = globalThis.__castreader_weread_cache__;
      if ((cache == null ? void 0 : cache.apiContent) && cache.apiContent.length > 0) {
        return cache.apiContent;
      }
      if ((_a = cache == null ? void 0 : cache.pages) == null ? void 0 : _a.length) {
        const all = cache.pages.flatMap((p) => p.paragraphs);
        if (all.length > 0) return all;
      }
      const apiResult = extractFromApiAttribute();
      if (apiResult.length > 0) return apiResult.map((p) => p.text);
      return [];
    },
    extractText() {
      const liveParagraphs = extractParagraphsFromLiveDOM();
      if (liveParagraphs.length >= 3) {
        return liveParagraphs.map((p) => p.text).join("\n\n");
      }
      const cachedParagraphs = extractFromGlobalCache();
      if (cachedParagraphs.length > 0) {
        return cachedParagraphs.map((p) => p.text).join("\n\n");
      }
      const containerTexts = extractTextFromDOMContainers();
      if (containerTexts.length > 3) {
        return containerTexts.join("\n\n");
      }
      const apiParagraphs = extractFromApiAttribute();
      if (apiParagraphs.length > 0) {
        return apiParagraphs.map((p) => p.text).join("\n\n");
      }
      console.log("[weread] extractText: 尝试 Readability");
      if (isReaderable()) {
        const result = extractWithReadability();
        if ((result == null ? void 0 : result.textContent) && !isJunkText(result.textContent.substring(0, 200))) {
          return result.textContent;
        }
      }
      return null;
    },
    extractTitle() {
      const domTitle = findTitle();
      if (domTitle) return domTitle;
      const cache = globalThis.__castreader_weread_cache__;
      return (cache == null ? void 0 : cache.title) || null;
    },
    extractLanguage() {
      return "zh";
    },
    /**
     * 异步提取：等待 hook 缓存（含段落位置）就绪
     */
    async extractParagraphsAsync() {
      var _a, _b, _c, _d, _e;
      const canvasContainer = document.querySelector(".wr_canvasContainer");
      if (canvasContainer) {
        const cache = () => globalThis.__castreader_weread_cache__;
        if (!((_b = (_a = cache()) == null ? void 0 : _a.paragraphPositions) == null ? void 0 : _b.length)) {
          console.log("[weread] 等待段落位置数据...");
          for (let i = 0; i < 10; i++) {
            await new Promise((r) => setTimeout(r, 300));
            if ((_d = (_c = cache()) == null ? void 0 : _c.paragraphPositions) == null ? void 0 : _d.length) {
              console.log(`[weread] 段落位置就绪 (${(i + 1) * 300}ms), ${cache().paragraphPositions.length} 个`);
              break;
            }
          }
        }
        const LAYOUT_ATTR = "data-castreader-wr-layout";
        if (!document.documentElement.getAttribute(LAYOUT_ATTR)) {
          console.log("[weread] Canvas 模式：等待 fillText 布局数据...");
          for (let i = 0; i < 15; i++) {
            await new Promise((r) => setTimeout(r, 300));
            if (document.documentElement.getAttribute(LAYOUT_ATTR)) {
              console.log(`[weread] fillText 布局数据就绪 (${(i + 1) * 300}ms)`);
              break;
            }
          }
          if (!document.documentElement.getAttribute(LAYOUT_ATTR)) {
            console.log("[weread] fillText 布局数据等待超时 (4.5s)，回退到其他策略");
          }
        }
      }
      const immediate = this.extractParagraphsWithElements();
      if (immediate.length > 0) {
        return immediate;
      }
      console.log("[weread] cache 内容不足，等待 hook 捕获 preRenderContainer...");
      const maxWait = 8e3;
      const pollInterval = 500;
      const startTime = Date.now();
      while (Date.now() - startTime < maxWait) {
        await new Promise((resolve) => setTimeout(resolve, pollInterval));
        const cache = globalThis.__castreader_weread_cache__;
        const totalParagraphs = ((cache == null ? void 0 : cache.pages) || []).reduce((sum, p) => sum + p.paragraphs.length, 0) + (((_e = cache == null ? void 0 : cache.apiContent) == null ? void 0 : _e.length) || 0);
        if (totalParagraphs >= 3) {
          console.log(`[weread] hook 已捕获 ${totalParagraphs} 段落 (等待 ${Date.now() - startTime}ms)`);
          return this.extractParagraphsWithElements();
        }
      }
      console.log("[weread] 等待超时，返回当前已有内容");
      return this.extractParagraphsWithElements();
    },
    /**
     * 提取段落及其 DOM 元素引用
     * 优先从 DOM 提取以支持高亮，回退到缓存文本（仅 TTS）
     */
    extractParagraphsWithElements() {
      var _a, _b, _c, _d, _e, _f;
      try {
        delete document.documentElement.dataset.castreaderGapDiag;
        delete document.documentElement.dataset.castreaderFlushDiag;
        delete document.documentElement.dataset.castreaderExtResult;
        delete document.documentElement.dataset.castreaderExtParas;
        delete document.documentElement.dataset.castreaderPageDebug;
        delete document.documentElement.dataset.castreaderFillResult;
      } catch {
      }
      const cache = globalThis.__castreader_weread_cache__;
      const domAttr = document.documentElement.getAttribute("data-castreader-wr-chapter");
      console.log(
        "[weread] 开始提取段落 |",
        "hook缓存:",
        cache ? `存在(pages=${((_a = cache.pages) == null ? void 0 : _a.length) || 0}, apiContent=${((_b = cache.apiContent) == null ? void 0 : _b.length) || 0})` : "❌ 不存在",
        "| DOM属性:",
        domAttr ? `有数据(${domAttr.length}字符)` : "无"
      );
      const isCanvasMode = !!document.querySelector(".wr_canvasContainer");
      const liveParagraphs = extractParagraphsFromLiveDOM();
      if (isCanvasMode) {
        const canvasEl = document.querySelector(".wr_canvasContainer");
        const isDualColumn2 = canvasEl ? isCanvasDualColumn(canvasEl) : false;
        if (isDualColumn2) {
          const chapterParas = this.getAllCachedTexts();
          console.log("[weread-dual] chapterParas:", chapterParas.length);
          if (chapterParas.length > 0) {
            const matched = matchFillTextPagesToChapter(chapterParas);
            console.log(
              "[weread-dual] matched:",
              (matched == null ? void 0 : matched.length) || 0,
              matched ? matched.map((m) => `"${m.text.substring(0, 20)}" hl=${m.canHighlight}`).slice(0, 3) : []
            );
            if (matched && matched.length > 0) {
              console.log("[weread] ✅ 双栏 fillText→章节匹配:", matched.length, "段落");
              try {
                const hlN = matched.filter((p) => p.canHighlight).length;
                const teN = matched.filter((p) => p.textElement).length;
                const paraDigest = matched.map((m, i) => `p${i}:[${m.text.length}字]"${m.text.substring(0, 20)}"`).join(" | ");
                document.documentElement.dataset.castreaderExtResult = `PATH=matchFillText total=${matched.length} hl=${hlN} tEl=${teN} chapterParas=${chapterParas.length}`;
                document.documentElement.dataset.castreaderExtParas = paraDigest;
              } catch {
              }
              return matched;
            }
          }
          const fillTextParas = extractFromFillTextPages();
          if (fillTextParas.length > 0) {
            console.log(
              "[weread] ✅ 双栏 fillText 直接提取:",
              fillTextParas.length,
              "段落",
              `可高亮: ${fillTextParas.filter((p) => p.canHighlight).length}`
            );
            try {
              const paraDigest = fillTextParas.map((m, i) => `p${i}:[${m.text.length}字]"${m.text.substring(0, 20)}"`).join(" | ");
              document.documentElement.dataset.castreaderExtResult = `PATH=fillTextDirect total=${fillTextParas.length} hl=${fillTextParas.filter((p) => p.canHighlight).length}`;
              document.documentElement.dataset.castreaderExtParas = paraDigest;
            } catch {
            }
            return fillTextParas;
          }
          if (liveParagraphs.length >= 3) {
            console.log("[weread] ⚠️ 双栏提取全部失败，回退到 DOM 段落:", liveParagraphs.length);
            try {
              document.documentElement.dataset.castreaderExtResult = `PATH=domFallback total=${liveParagraphs.length}`;
            } catch {
            }
            return liveParagraphs;
          }
        }
        const allTexts = this.getAllCachedTexts();
        if (allTexts.length > 0) {
          const overlays = createCanvasHighlightOverlays(allTexts);
          if (overlays.length > 0) {
            console.log("[weread] ✅ Canvas 高亮模式（单栏）:", overlays.length, "个定位覆盖层");
            try {
              const hlN = overlays.filter((p) => p.canHighlight).length;
              const noHl = overlays.map((m, i) => m.canHighlight ? null : i).filter((i) => i !== null);
              const _ftDbg = readFillTextLayout();
              const _cacheDbg = globalThis.__castreader_weread_cache__;
              const _hasTextEl = overlays.filter((p) => p.textElement).length;
              const _firstFS = ((_d = (_c = _cacheDbg == null ? void 0 : _cacheDbg.paragraphPositions) == null ? void 0 : _c[0]) == null ? void 0 : _d.fontStyle) || "";
              const _cssLH = ((_e = _firstFS.match(/line-height:\s*([^;]+)/)) == null ? void 0 : _e[1]) || "N/A";
              const _canvasW2 = ((_f = document.querySelector(".wr_canvasContainer")) == null ? void 0 : _f.offsetWidth) ?? 0;
              document.documentElement.dataset.castreaderExtResult = `PATH=singleCol total=${overlays.length} hl=${hlN} textSpans=${_hasTextEl} ftLineH=${(_ftDbg == null ? void 0 : _ftDbg.lineHeight) ?? "null"} cssLH=${_cssLH}`;
              const _sampleDetails = overlays.slice(0, 8).map((o, idx) => {
                const el = o.element;
                return `p${idx}:top=${el.style.top},h=${el.style.height},"${o.text.substring(0, 6)}"`;
              }).join(" | ");
              document.documentElement.dataset.castreaderOverlayPos = _sampleDetails;
              document.documentElement.dataset.castreaderExtParas = overlays.map(
                (m, i) => `p${i}:${m.canHighlight ? "✓" : "✗"}[${m.text.length}字]"${m.text.substring(0, 20)}"`
              ).join(" | ");
            } catch {
            }
            return overlays;
          }
        }
      }
      if (liveParagraphs.length >= 3) {
        console.log("[weread] ✅ DOM 模式：使用真实段落元素，段落数:", liveParagraphs.length);
        return liveParagraphs;
      }
      const fallbackTexts = isCanvasMode ? this.getAllCachedTexts() : [];
      if (fallbackTexts.length > 0) {
        console.log("[weread] 纯文本模式（仅 TTS），段落数:", fallbackTexts.length);
        return fallbackTexts.map((text) => ({
          text,
          element: document.body,
          canHighlight: false
        }));
      }
      const containerTexts = extractTextFromDOMContainers();
      if (containerTexts.length > 3) {
        console.log("[weread] 容器文本模式（仅 TTS），段落数:", containerTexts.length);
        return containerTexts.map((text) => ({
          text,
          element: document.body,
          canHighlight: false
        }));
      }
      const apiParagraphs = extractFromApiAttribute();
      if (apiParagraphs.length > 0) {
        return apiParagraphs;
      }
      if (isReaderable()) {
        console.log("[weread] 回退到 Readability");
        const result = extractWithReadability();
        if (result == null ? void 0 : result.textContent) {
          const texts = result.textContent.split(/\n+/).map((p) => p.trim()).filter((p) => p.length > 10);
          if (texts.length > 0) {
            return texts.map((text) => ({
              text,
              element: document.body,
              canHighlight: false
            }));
          }
        }
      }
      console.log("[weread] 未能提取任何内容");
      return [];
    }
  };
  function findKindleBlobImage() {
    const imgs = document.querySelectorAll('img[src^="blob:"]');
    if (imgs.length === 0) return null;
    let best = null;
    let bestArea = 0;
    for (const img of Array.from(imgs)) {
      if (!img.complete || img.naturalWidth === 0) continue;
      const rect = img.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) continue;
      const area = img.naturalWidth * img.naturalHeight;
      if (area > bestArea) {
        bestArea = area;
        best = img;
      }
    }
    return best;
  }
  function captureImageToDataURL(img) {
    const canvas = document.createElement("canvas");
    canvas.width = img.naturalWidth || img.width;
    canvas.height = img.naturalHeight || img.height;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    return canvas.toDataURL("image/png");
  }
  function isDualColumn(img) {
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;
    return w / h > 1.15;
  }
  function splitDualColumn(img) {
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;
    const mid = Math.floor(w / 2);
    const leftCanvas = document.createElement("canvas");
    leftCanvas.width = mid;
    leftCanvas.height = h;
    leftCanvas.getContext("2d").drawImage(img, 0, 0, mid, h, 0, 0, mid, h);
    const rightCanvas = document.createElement("canvas");
    rightCanvas.width = w - mid;
    rightCanvas.height = h;
    rightCanvas.getContext("2d").drawImage(img, mid, 0, w - mid, h, 0, 0, w - mid, h);
    return [leftCanvas.toDataURL("image/png"), rightCanvas.toDataURL("image/png")];
  }
  const LIGATURE_PATTERNS = [
    { chars: "ffi", len: 3 },
    { chars: "ffl", len: 3 },
    { chars: "ff", len: 2 },
    { chars: "fi", len: 2 },
    { chars: "fl", len: 2 }
  ];
  class KindleGlyphMapper {
    constructor() {
      __publicField(this, "glyphMap", /* @__PURE__ */ new Map());
      __publicField(this, "glyphVotes", /* @__PURE__ */ new Map());
      __publicField(this, "spaceGlyphId", -1);
      __publicField(this, "totalUniqueGlyphs", 0);
    }
    get confidence() {
      if (this.totalUniqueGlyphs === 0) return 0;
      return this.glyphMap.size / this.totalUniqueGlyphs;
    }
    isCalibrated() {
      return this.confidence > 0.85;
    }
    /** 获取 totalUniqueGlyphs（用于双栏合并后重算分母） */
    get uniqueGlyphCount() {
      return this.totalUniqueGlyphs;
    }
    /** 双栏合并后重置分母（主 mapper 的 totalUniqueGlyphs 来自全部 runs，虚高） */
    resetTotalUniqueGlyphs(count) {
      this.totalUniqueGlyphs = count;
    }
    /**
     * 检测一组 glyphs 是否与当前校准兼容
     * 不同 batch/font subset 的 glyph ID 不同，需要重新校准
     * @returns 0~1，已映射 glyph 的比例
     */
    checkCompatibility(glyphs) {
      if (glyphs.length === 0 || this.glyphMap.size === 0) return 0;
      let mapped = 0;
      for (const g of glyphs) {
        if (this.glyphMap.has(g)) mapped++;
      }
      return mapped / glyphs.length;
    }
    getUnmappedGlyphs() {
      const unmapped = [];
      for (const [id] of this.glyphMap) {
      }
      return unmapped;
    }
    /**
     * Step 1: 识别空格 glyph
     *
     * 英文文本中空格永远是出现频率最高的字符。
     * 直接取整页最频繁 glyph = space。
     *
     * 之前用位置插值法（positionId→glyph index 映射）在连字 run 中
     * 因 ratio=0.98 导致插值偏移，19 个 space 被错误映射到 word position
     * → 选中了 glyph 62 (freq=323) 而非正确的 glyph 63 (freq=342)。
     */
    identifySpaceGlyph(pageDataRuns) {
      const glyphFreq = /* @__PURE__ */ new Map();
      const allGlyphs = /* @__PURE__ */ new Set();
      for (const run of pageDataRuns) {
        for (const g of run.glyphs) {
          allGlyphs.add(g);
          glyphFreq.set(g, (glyphFreq.get(g) || 0) + 1);
        }
      }
      this.totalUniqueGlyphs = allGlyphs.size;
      const sorted = [...glyphFreq.entries()].sort((a, b) => b[1] - a[1]);
      console.log(
        `[kindle] Glyph freq (${allGlyphs.size} unique, ${sorted.reduce((s, [, c]) => s + c, 0)} total): ` + sorted.slice(0, 15).map(([g, c]) => `g${g}=${c}`).join(" ")
      );
      let bestGlyph = -1;
      let bestCount = 0;
      for (const [g, count] of glyphFreq) {
        if (count > bestCount) {
          bestCount = count;
          bestGlyph = g;
        }
      }
      if (bestGlyph >= 0) {
        this.spaceGlyphId = bestGlyph;
        this.glyphMap.set(bestGlyph, " ");
      }
    }
    /**
     * Step 2: OCR 校准 — character-level 直接对齐
     *
     * 核心思路：去掉所有空格后，OCR 字符序列和 glyph 序列应该一一对应。
     * 唯一的不对称是连字（ff, fi, fl, ffi）：1 个 glyph = 2-3 个字符。
     *
     * 比之前的 word-level 两指针更鲁棒：
     * - 不受行末缺 space glyph 影响（word 边界不一致是 drift 主因）
     * - 不受 OCR 多余空格/换行影响
     * - 唯一需要处理的是连字检测
     */
    /**
     * @returns 校准匹配质量 0~1（前 30 字符的匹配比例）
     */
    calibrate(ocrParagraphs, _tokenPages, pageDataRuns, silent = false, skipLigatures = false, columnSide = "full") {
      const sortedRuns = [...pageDataRuns].sort((a, b) => {
        var _a, _b, _c, _d;
        const ay = ((_a = a.transform) == null ? void 0 : _a[5]) ?? 0;
        const by = ((_b = b.transform) == null ? void 0 : _b[5]) ?? 0;
        if (Math.abs(ay - by) > 1) return ay - by;
        const ax = ((_c = a.transform) == null ? void 0 : _c[4]) ?? 0;
        const bx = ((_d = b.transform) == null ? void 0 : _d[4]) ?? 0;
        return ax - bx;
      });
      const wordPositions = /* @__PURE__ */ new Set();
      for (const page of _tokenPages) {
        for (const para of page.children) {
          for (const word of para.words) {
            for (let pos = word.startPositionId; pos <= word.endPositionId; pos++) {
              wordPositions.add(pos);
            }
          }
        }
      }
      const hasWordFilter = wordPositions.size > 0;
      const nonSpaceGlyphs = [];
      for (const run of sortedRuns) {
        const runRange = run.endPositionId - run.startPositionId + 1;
        for (let i = 0; i < run.glyphs.length; i++) {
          const g = run.glyphs[i];
          if (g === this.spaceGlyphId) continue;
          if (hasWordFilter && runRange > 0) {
            const pos = run.startPositionId + Math.round(
              i * (run.endPositionId - run.startPositionId) / Math.max(run.glyphs.length - 1, 1)
            );
            if (!wordPositions.has(pos)) continue;
          }
          nonSpaceGlyphs.push(g);
        }
      }
      const ocrText = ocrParagraphs.join(" ");
      const chars = [...ocrText].filter((c) => !/\s/.test(c));
      if (nonSpaceGlyphs.length !== chars.length && !silent) {
        const gap = nonSpaceGlyphs.length - chars.length;
        let spaceCount = 0;
        for (const run of sortedRuns) {
          for (const g of run.glyphs) {
            if (g === this.spaceGlyphId) spaceCount++;
          }
        }
        const totalGlyphs = nonSpaceGlyphs.length + spaceCount;
        console.log(
          `[kindle] DIAG chars/glyphs gap: totalGlyphs=${totalGlyphs} - spaces=${spaceCount} = ${nonSpaceGlyphs.length} nonSpace, ocrChars=${chars.length}, gap=${gap}`
        );
        const nonSpaceFreq = /* @__PURE__ */ new Map();
        for (const g of nonSpaceGlyphs) {
          nonSpaceFreq.set(g, (nonSpaceFreq.get(g) || 0) + 1);
        }
        if (gap > 20) {
          const byFreq = [...nonSpaceFreq.entries()].sort((a, b) => b[1] - a[1]);
          console.log(
            `[kindle] DIAG top non-space glyphs: ${byFreq.slice(0, 10).map(([g, c]) => `g${g}=${c}`).join(" ")}`
          );
        }
      }
      let ci = 0, gi = 0;
      while (ci < chars.length && gi < nonSpaceGlyphs.length) {
        const remainingChars = chars.length - ci;
        const remainingGlyphs = nonSpaceGlyphs.length - gi;
        let ligMatched = false;
        if (!skipLigatures && remainingGlyphs < remainingChars) {
          for (const lig of LIGATURE_PATTERNS) {
            if (ci + lig.len <= chars.length) {
              const candidate = chars.slice(ci, ci + lig.len).join("");
              if (candidate === lig.chars) {
                const curMapping = this.glyphMap.get(nonSpaceGlyphs[gi]);
                if (curMapping && curMapping.length === 1) continue;
                if (lig.chars.startsWith("ff") && gi + 1 < nonSpaceGlyphs.length && nonSpaceGlyphs[gi] === nonSpaceGlyphs[gi + 1]) continue;
                if (gi + 1 < nonSpaceGlyphs.length && ci + lig.len < chars.length) {
                  const nextMapping = this.glyphMap.get(nonSpaceGlyphs[gi + 1]);
                  if (nextMapping && nextMapping !== chars[ci + lig.len]) continue;
                }
                this.setMapping(nonSpaceGlyphs[gi], lig.chars);
                ci += lig.len;
                gi++;
                ligMatched = true;
                break;
              }
            }
          }
        }
        if (!ligMatched) {
          this.setMapping(nonSpaceGlyphs[gi], chars[ci]);
          ci++;
          gi++;
        }
      }
      const verifyLen = Math.min(30, nonSpaceGlyphs.length, chars.length);
      const decodedSample = nonSpaceGlyphs.slice(0, verifyLen).map((g) => this.glyphMap.get(g) ?? "?").join("");
      const ocrSample = chars.slice(0, verifyLen).join("");
      let matchCount = 0;
      for (let i = 0; i < verifyLen; i++) {
        if (decodedSample[i] === ocrSample[i]) matchCount++;
      }
      if (!silent) {
        console.log(
          `[kindle] Glyph calibration: ${this.glyphMap.size}/${this.totalUniqueGlyphs} mapped (${(this.confidence * 100).toFixed(0)}%) — chars=${chars.length} glyphs=${nonSpaceGlyphs.length} aligned=${Math.min(ci, gi)}`
        );
      }
      const quality = verifyLen > 0 ? matchCount / verifyLen : 0;
      if (!silent) {
        console.log(
          `[kindle] Calibration verify (first ${verifyLen}): match=${matchCount}/${verifyLen} (${(quality * 100).toFixed(0)}%)${skipLigatures ? " [no-lig retry]" : ""}
  OCR:     "${ocrSample}"
  Decoded: "${decodedSample}"`
        );
      }
      if (columnSide !== "full" && nonSpaceGlyphs.length > 0 && chars.length > 0) {
        const trimThreshold = 3;
        const alignedLen = Math.min(ci, gi, nonSpaceGlyphs.length, chars.length);
        if (columnSide === "left" && alignedLen > trimThreshold) {
          let tailMiss = 0;
          for (let i = alignedLen - 1; i >= 0; i--) {
            const decoded = this.glyphMap.get(nonSpaceGlyphs[i]);
            if (decoded !== chars[i]) tailMiss++;
            else break;
          }
          if (tailMiss > trimThreshold) {
            for (let i = alignedLen - tailMiss; i < alignedLen; i++) {
              this.glyphMap.delete(nonSpaceGlyphs[i]);
            }
            if (!silent) console.log(`[kindle] Edge trim (left tail): removed ${tailMiss} mappings`);
          }
        } else if (columnSide === "right" && alignedLen > trimThreshold) {
          let headMiss = 0;
          for (let i = 0; i < alignedLen; i++) {
            const decoded = this.glyphMap.get(nonSpaceGlyphs[i]);
            if (decoded !== chars[i]) headMiss++;
            else break;
          }
          if (headMiss > trimThreshold) {
            for (let i = 0; i < headMiss; i++) {
              this.glyphMap.delete(nonSpaceGlyphs[i]);
            }
            if (!silent) console.log(`[kindle] Edge trim (right head): removed ${headMiss} mappings`);
          }
        }
      }
      if (quality < 0.7 && !skipLigatures) {
        this.glyphMap.clear();
        this.glyphVotes.clear();
        return this.calibrate(ocrParagraphs, _tokenPages, pageDataRuns, silent, true, columnSide);
      }
      return quality;
    }
    /** 获取当前 glyph 映射表（只读） */
    getGlyphMap() {
      return this.glyphMap;
    }
    /** 从另一个 mapper 合并映射，冲突时按投票数决定 */
    mergeFrom(other) {
      if (other.totalUniqueGlyphs > this.totalUniqueGlyphs) {
        this.totalUniqueGlyphs = other.totalUniqueGlyphs;
      }
      if (this.spaceGlyphId < 0 && other.spaceGlyphId >= 0) {
        this.spaceGlyphId = other.spaceGlyphId;
      }
      for (const [glyphId, char] of other.glyphMap) {
        let votes = this.glyphVotes.get(glyphId);
        if (!votes) {
          votes = /* @__PURE__ */ new Map();
          this.glyphVotes.set(glyphId, votes);
        }
        votes.set(char, (votes.get(char) || 0) + 1);
        const existing = this.glyphMap.get(glyphId);
        if (existing && !votes.has(existing)) {
          votes.set(existing, 1);
        } else if (existing && votes.get(existing) === 0) {
          votes.set(existing, 1);
        }
        let bestChar = char, bestCount = 0;
        for (const [c, count] of votes) {
          if (count > bestCount) {
            bestChar = c;
            bestCount = count;
          }
        }
        this.glyphMap.set(glyphId, bestChar);
      }
    }
    /**
     * 找到 token word 对应的 glyph 序列（通过 positionId 范围交集）
     */
    getGlyphsForWord(word, runs) {
      const result = [];
      for (const run of runs) {
        const overlapStart = Math.max(word.startPositionId, run.startPositionId);
        const overlapEnd = Math.min(word.endPositionId, run.endPositionId);
        if (overlapStart > overlapEnd) continue;
        const runRange = run.endPositionId - run.startPositionId + 1;
        if (runRange <= 0) continue;
        const startIdx = Math.floor((overlapStart - run.startPositionId) * run.glyphs.length / runRange);
        const endIdx = Math.ceil((overlapEnd - run.startPositionId + 1) * run.glyphs.length / runRange);
        for (let i = Math.max(0, startIdx); i < Math.min(run.glyphs.length, endIdx); i++) {
          result.push(run.glyphs[i]);
        }
      }
      return result;
    }
    /**
     * 对齐单个 OCR word 到 glyph 序列，建立映射
     */
    alignWordToGlyphs(word, glyphs) {
      const chars = [...word];
      if (chars.length === glyphs.length) {
        for (let i = 0; i < chars.length; i++) {
          this.setMapping(glyphs[i], chars[i]);
        }
        return;
      }
      if (glyphs.length < chars.length) {
        this.alignWithLigatures(chars, glyphs);
        return;
      }
    }
    /**
     * 处理连字对齐
     */
    alignWithLigatures(chars, glyphs) {
      let ci = 0;
      let gi = 0;
      while (ci < chars.length && gi < glyphs.length) {
        if (ci === chars.length - 1 && gi === glyphs.length - 1) {
          this.setMapping(glyphs[gi], chars[ci]);
          ci++;
          gi++;
          continue;
        }
        let matched = false;
        for (const lig of LIGATURE_PATTERNS) {
          const remaining = chars.slice(ci, ci + lig.len).join("");
          if (remaining === lig.chars && ci + lig.len <= chars.length) {
            this.setMapping(glyphs[gi], lig.chars);
            ci += lig.len;
            gi++;
            matched = true;
            break;
          }
        }
        if (!matched) {
          this.setMapping(glyphs[gi], chars[ci]);
          ci++;
          gi++;
        }
      }
    }
    /**
     * 校准期间的映射：first-seen-wins
     * 1:1 对齐中早期映射更可靠（对齐漂移越往后越大），锁定首次结果。
     */
    setMapping(glyphId, char) {
      if (this.glyphMap.has(glyphId)) return;
      this.glyphMap.set(glyphId, char);
    }
    /**
     * 解码单个 token word 的文本（排除空格 glyph）
     */
    decodeWord(word, runs) {
      const glyphs = this.getGlyphsForWord(word, runs);
      const filtered = this.spaceGlyphId >= 0 ? glyphs.filter((g) => g !== this.spaceGlyphId) : glyphs;
      return this.decode(filtered);
    }
    /**
     * Step 3: 用已建立的映射解码 glyph 序列 → 文本
     */
    decode(glyphs) {
      return glyphs.map((g) => this.glyphMap.get(g) ?? "�").join("");
    }
    /**
     * 解码 run 列表中的所有 glyph → 完整文本
     */
    decodeRuns(runs) {
      return runs.map((run) => this.decode(run.glyphs)).join("");
    }
    /**
     * 按段落解码：给定 token paragraphs 和 page_data runs，
     * 提取每个段落的 glyph 序列并解码为文本
     */
    decodeParagraphs(tokenParas, runs) {
      return tokenParas.map((para) => {
        const paraGlyphs = [];
        for (const word of para.words) {
          if (paraGlyphs.length > 0) {
            paraGlyphs.push(this.spaceGlyphId);
          }
          const wordGlyphs = this.getGlyphsForWord(word, runs);
          const filtered = this.spaceGlyphId >= 0 ? wordGlyphs.filter((g) => g !== this.spaceGlyphId) : wordGlyphs;
          paraGlyphs.push(...filtered);
        }
        return this.decode(paraGlyphs).trim();
      });
    }
    /**
     * 序列化映射表（用于持久化/调试）
     */
    toJSON() {
      const obj = {};
      for (const [id, char] of this.glyphMap) {
        obj[String(id)] = char;
      }
      return obj;
    }
    /**
     * 从序列化数据恢复映射表
     */
    fromJSON(data) {
      for (const [id, char] of Object.entries(data)) {
        this.glyphMap.set(Number(id), char);
      }
    }
  }
  class KindleOverlay {
    constructor(img) {
      __publicField(this, "container", null);
      __publicField(this, "imgEl");
      __publicField(this, "isDual", false);
      __publicField(this, "resizeObserver", null);
      __publicField(this, "paragraphElements", []);
      // Word-level highlight
      __publicField(this, "wordHighlightDiv", null);
      __publicField(this, "wordHighlightBbox", null);
      __publicField(this, "wordHighlightPageBounds", null);
      __publicField(this, "wordHighlightIsRight", false);
      this.imgEl = img;
    }
    /**
     * 初始化 overlay 容器
     * @param isDual 是否双栏布局
     */
    init(isDual) {
      this.isDual = isDual;
      this.container = document.createElement("div");
      this.container.className = "kindle-highlight-container";
      this.container.setAttribute("data-castreader-overlay", "kindle");
      const imgOffsetLeft = this.imgEl.offsetLeft;
      const imgOffsetTop = this.imgEl.offsetTop;
      Object.assign(this.container.style, {
        position: "absolute",
        top: `${imgOffsetTop}px`,
        left: `${imgOffsetLeft}px`,
        width: `${this.imgEl.offsetWidth}px`,
        height: `${this.imgEl.offsetHeight}px`,
        pointerEvents: "none",
        zIndex: "10"
      });
      const imgParent = this.imgEl.parentElement;
      if (imgParent) {
        const parentStyle = getComputedStyle(imgParent);
        if (parentStyle.position === "static") {
          imgParent.style.position = "relative";
        }
        imgParent.appendChild(this.container);
      }
      this.resizeObserver = new ResizeObserver(() => this.handleResize());
      this.resizeObserver.observe(this.imgEl);
    }
    handleResize() {
      if (!this.container) return;
      const w = this.imgEl.offsetWidth;
      const h = this.imgEl.offsetHeight;
      if (w < 50 || h < 50) return;
      this.container.style.left = `${this.imgEl.offsetLeft}px`;
      this.container.style.top = `${this.imgEl.offsetTop}px`;
      this.container.style.width = `${w}px`;
      this.container.style.height = `${h}px`;
      for (const p of this.paragraphElements) {
        const colDisplayWidth = this.isDual ? w / 2 : w;
        const offsetX = p.isRightColumn ? w / 2 : 0;
        const scaleX = colDisplayWidth / p.pageBaseWidth;
        const scaleY = h / p.pageBaseHeight;
        const hPad = 4;
        Object.assign(p.div.style, {
          left: `${p.tokenX * scaleX + offsetX - hPad}px`,
          top: `${p.tokenY * scaleY}px`,
          width: `${p.tokenW * scaleX + hPad * 2}px`,
          height: `${p.tokenH * scaleY}px`
        });
        p.span.style.fontSize = `${p.fontSize * scaleY}px`;
      }
      if (this.wordHighlightBbox) {
        this.positionWordHighlight();
      }
    }
    /**
     * 创建段落 overlay div + textSpan
     *
     * @param paraBbox 段落的 bbox（在页面 1x 坐标空间中）
     * @param text 段落文本
     * @param fontInfo 字体信息
     * @param isRightColumn 是否右栏
     * @param pageBounds 页面坐标空间尺寸
     */
    createParagraphOverlay(paraBbox, text, fontInfo, isRightColumn, pageBounds) {
      if (!this.container) {
        throw new Error("KindleOverlay not initialized. Call init() first.");
      }
      const displayW = this.imgEl.offsetWidth;
      const displayH = this.imgEl.offsetHeight;
      const colDisplayWidth = this.isDual ? displayW / 2 : displayW;
      const offsetX = isRightColumn ? displayW / 2 : 0;
      const scaleX = colDisplayWidth / pageBounds.width;
      const scaleY = displayH / pageBounds.height;
      const div = document.createElement("div");
      div.setAttribute("data-castreader-overlay", "kindle");
      const hPad = 4;
      const left = paraBbox.x * scaleX + offsetX - hPad;
      const top = paraBbox.y * scaleY;
      const width = paraBbox.width * scaleX + hPad * 2;
      const height = paraBbox.height * scaleY;
      Object.assign(div.style, {
        position: "absolute",
        left: `${left}px`,
        top: `${top}px`,
        width: `${width}px`,
        height: `${height}px`,
        pointerEvents: "auto",
        cursor: "pointer",
        borderRadius: "3px"
      });
      const span = document.createElement("span");
      span.textContent = text;
      const fontFamily = fontInfo.fontFamily ? `${fontInfo.fontFamily}, Georgia, serif` : "Georgia, serif";
      Object.assign(span.style, {
        fontFamily,
        fontSize: `${fontInfo.fontSize * scaleY}px`,
        fontWeight: String(fontInfo.fontWeight || 400),
        color: "transparent",
        display: "block",
        position: "absolute",
        top: "0",
        left: "0",
        width: "100%",
        height: "100%",
        overflow: "hidden",
        lineHeight: "1.4",
        letterSpacing: "0",
        wordSpacing: "0"
      });
      div.appendChild(span);
      this.container.appendChild(div);
      this.paragraphElements.push({
        div,
        span,
        tokenX: paraBbox.x,
        tokenY: paraBbox.y,
        tokenW: paraBbox.width,
        tokenH: paraBbox.height,
        isRightColumn,
        pageBaseWidth: pageBounds.width,
        pageBaseHeight: pageBounds.height,
        fontSize: fontInfo.fontSize
      });
      return { element: div, textElement: span };
    }
    // ========== Word-level highlight ==========
    /**
     * 显示单词高亮 — 在 blob 图片上定位金色半透明矩形
     *
     * @param bbox 单词的 bbox（token 1x 坐标空间）
     * @param pageBounds 页面坐标空间尺寸
     * @param isRightColumn 是否右栏
     */
    showWordHighlight(bbox, pageBounds, isRightColumn) {
      if (!this.container) return;
      if (!this.wordHighlightDiv) {
        this.wordHighlightDiv = document.createElement("div");
        Object.assign(this.wordHighlightDiv.style, {
          position: "absolute",
          backgroundColor: "rgba(242, 101, 34, 0.3)",
          borderRadius: "2px",
          pointerEvents: "none",
          transition: "left 0.05s, top 0.05s, width 0.05s",
          zIndex: "20"
        });
        this.container.appendChild(this.wordHighlightDiv);
      }
      this.wordHighlightBbox = bbox;
      this.wordHighlightPageBounds = pageBounds;
      this.wordHighlightIsRight = isRightColumn;
      this.positionWordHighlight();
    }
    clearWordHighlight() {
      if (this.wordHighlightDiv) {
        this.wordHighlightDiv.style.display = "none";
      }
      this.wordHighlightBbox = null;
    }
    positionWordHighlight() {
      if (!this.wordHighlightDiv || !this.wordHighlightBbox || !this.wordHighlightPageBounds) return;
      const bbox = this.wordHighlightBbox;
      const pageBounds = this.wordHighlightPageBounds;
      const displayW = this.imgEl.offsetWidth;
      const displayH = this.imgEl.offsetHeight;
      const scaleX = (this.isDual ? displayW / 2 : displayW) / pageBounds.width;
      const scaleY = displayH / pageBounds.height;
      const offsetX = this.wordHighlightIsRight ? displayW / 2 : 0;
      Object.assign(this.wordHighlightDiv.style, {
        left: `${bbox.x * scaleX + offsetX}px`,
        top: `${bbox.y * scaleY}px`,
        width: `${bbox.width * scaleX}px`,
        height: `${bbox.height * scaleY}px`,
        display: "block"
      });
    }
    destroy() {
      if (this.resizeObserver) {
        this.resizeObserver.disconnect();
        this.resizeObserver = null;
      }
      if (this.container) {
        this.container.remove();
        this.container = null;
      }
      this.paragraphElements = [];
      this.wordHighlightDiv = null;
      this.wordHighlightBbox = null;
    }
    clearParagraphs() {
      for (const { div } of this.paragraphElements) {
        div.remove();
      }
      this.paragraphElements = [];
    }
  }
  function extractFontInfo(pageDataRuns) {
    if (pageDataRuns.length === 0) {
      return { fontFamily: "Georgia, serif", fontSize: 16, fontWeight: 400 };
    }
    const fontCounts = /* @__PURE__ */ new Map();
    for (const run of pageDataRuns) {
      const key = `${run.fontFamily || "serif"}|${run.fontSize || 16}|${run.fontWeight || 400}`;
      fontCounts.set(key, (fontCounts.get(key) || 0) + 1);
    }
    let bestKey = "";
    let bestCount = 0;
    for (const [key, count] of fontCounts) {
      if (count > bestCount) {
        bestCount = count;
        bestKey = key;
      }
    }
    const [fontFamily, fontSize, fontWeight] = bestKey.split("|");
    return {
      fontFamily: fontFamily || "Georgia, serif",
      fontSize: parseFloat(fontSize) || 16,
      fontWeight: parseInt(fontWeight) || 400
    };
  }
  const KINDLE_RENDER_ATTR = "data-castreader-kindle-render";
  let glyphMapper = null;
  let currentOverlay = null;
  let lastRenderSeq = 0;
  let hasTokenData = false;
  let lastExtractedPositionEnd = 0;
  let lastExtractedPageNumber = 0;
  let isAutoAdvanceExtraction = false;
  const KINDLE_IFRAME_SELECTORS = [
    "#kindleReader_book_frame",
    "#KindleReaderIFrame",
    'iframe[src*="kindle"]',
    'iframe[src*="read.amazon"]'
  ];
  const KINDLE_CONTENT_SELECTORS = [
    "#kindleReader_content",
    "#kindle-reader-content",
    ".kindleReader_content",
    "#column_0",
    "#column_1",
    ".a-text-content"
  ];
  function getKindleRenderData() {
    const attr = document.documentElement.getAttribute(KINDLE_RENDER_ATTR);
    if (!attr) return null;
    const colonIdx = attr.indexOf(":");
    if (colonIdx < 0) return null;
    const seq = parseInt(attr.substring(0, colonIdx));
    if (isNaN(seq) || seq <= lastRenderSeq) return null;
    try {
      const payload = JSON.parse(attr.substring(colonIdx + 1));
      return payload;
    } catch {
      console.warn("[kindle] Failed to parse render data");
      return null;
    }
  }
  function readKindlePageNumber() {
    var _a, _b;
    const scrubber = document.querySelector('[aria-label^="Page"]');
    if (scrubber) {
      const label = scrubber.getAttribute("aria-label") || "";
      const match = label.match(/Page\s+(\d+)/i);
      if (match) {
        console.log(`[kindle] readPageNumber: aria-label="${label}" → ${match[1]} (tag=${scrubber.tagName})`);
        return parseInt(match[1]);
      }
      console.log(`[kindle] readPageNumber: found [aria-label^="Page"] but no number: "${label}" (tag=${scrubber.tagName})`);
    }
    const posEls = document.querySelectorAll('[class*="position"]');
    for (const el of posEls) {
      const text = ((_a = el.textContent) == null ? void 0 : _a.trim()) || "";
      const match = text.match(/Page\s+(\d+)/i);
      if (match) {
        console.log(`[kindle] readPageNumber: position text="${text}" → ${match[1]} (tag=${el.tagName}, class=${el.className})`);
        return parseInt(match[1]);
      }
    }
    const locEls = document.querySelectorAll('[class*="location"], [class*="Location"], [aria-label*="Location"]');
    for (const el of locEls) {
      const text = ((_b = el.textContent) == null ? void 0 : _b.trim()) || el.getAttribute("aria-label") || "";
      const match = text.match(/Location\s+(\d+)/i);
      if (match) {
        console.log(`[kindle] readPageNumber: location text="${text}" → Location ${match[1]} (NOT page number)`);
      }
    }
    const allAriaPage = document.querySelectorAll('[aria-label*="page" i], [aria-label*="Page"]');
    if (allAriaPage.length > 0) {
      const debugInfo = Array.from(allAriaPage).map(
        (el) => `${el.tagName}[aria-label="${el.getAttribute("aria-label")}"]`
      ).join(", ");
      console.log(`[kindle] readPageNumber: all [aria-label*="page"]: ${debugInfo}`);
    }
    console.log("[kindle] readPageNumber: no page number found in DOM");
    return 0;
  }
  function buildUniquePageList(allPages) {
    const pageInfos = allPages.filter((p) => (p.children || []).length > 0).map((p, originalIdx) => ({
      page: p,
      originalIdx,
      minPos: Math.min(...p.children.map((c) => c.startPositionId)),
      maxPos: Math.max(...p.children.map((c) => c.endPositionId))
    })).sort((a, b) => a.minPos - b.minPos || b.originalIdx - a.originalIdx);
    const unique = [];
    for (const info of pageInfos) {
      if (unique.length > 0 && info.minPos <= unique[unique.length - 1].maxPos) continue;
      unique.push(info);
    }
    return unique;
  }
  function findPageAtOffset(allPages, anchorPosId, offset) {
    const unique = buildUniquePageList(allPages);
    const anchorIdx = unique.findIndex(
      (info) => anchorPosId >= info.minPos && anchorPosId <= info.maxPos
    );
    if (anchorIdx < 0) {
      console.warn(`[kindle] findPageAtOffset: anchorPosId=${anchorPosId} not found in ${unique.length} unique pages`);
      return null;
    }
    const targetIdx = anchorIdx + offset;
    if (targetIdx < 0 || targetIdx >= unique.length) {
      console.warn(`[kindle] findPageAtOffset: targetIdx=${targetIdx} out of range [0, ${unique.length})`);
      return null;
    }
    console.log(
      `[kindle] findPageAtOffset: ${unique.length} unique pages, anchorIdx=${anchorIdx}, offset=${offset}, targetIdx=${targetIdx}`
    );
    return unique[targetIdx].page;
  }
  function getRenderTimePageNumber(renderData, stride) {
    const requestLog = renderData.requestLog;
    if (!requestLog || requestLog.length === 0) return 0;
    const batch1 = [...requestLog].reverse().find(
      (r) => r.skipPageCount === "0" && parseInt(r.numPage) > 0
    );
    if (!batch1) return 0;
    if (batch1.pageNumberAtRender && batch1.pageNumberAtRender > 0) {
      return batch1.pageNumberAtRender;
    }
    const batch1Seq = batch1.seq;
    for (const entry of requestLog) {
      if (entry.startingPosition === batch1.startingPosition && entry.seq >= batch1Seq && entry.seq <= batch1Seq + 2 && entry.pageNumberAtRender && entry.pageNumberAtRender > 0) {
        return entry.pageNumberAtRender;
      }
    }
    for (const entry of requestLog) {
      if (entry.startingPosition === batch1.startingPosition && parseInt(entry.skipPageCount) > 0 && entry.pageNumberAtRender && entry.pageNumberAtRender > 0) {
        const skip = parseInt(entry.skipPageCount);
        const estimated = entry.pageNumberAtRender - Math.floor(skip / stride);
        console.log(
          `[kindle] renderTimePageNum: back-calculated ${estimated} (from seq=${entry.seq}: pageAtRender=${entry.pageNumberAtRender} - skip=${skip}/stride=${stride})`
        );
        return estimated;
      }
    }
    return 0;
  }
  function dumpPageMap(allPages, selectedPage, anchorPage, renderData, currentPageNum, renderTimePageNum) {
    const unique = buildUniquePageList(allPages);
    const selectedMinPos = selectedPage ? Math.min(...(selectedPage.children || []).map((c) => c.startPositionId)) : -1;
    const anchorMinPos = anchorPage ? Math.min(...(anchorPage.children || []).map((c) => c.startPositionId)) : -1;
    const anchorIdx = unique.findIndex(
      (info) => anchorMinPos >= info.minPos && anchorMinPos <= info.maxPos
    );
    console.log(
      `[kindle] ===== PAGE MAP (${allPages.length} raw → ${unique.length} unique) =====
  renderTimePageNum=${renderTimePageNum}, currentPageNum=${currentPageNum}, delta=${currentPageNum - renderTimePageNum}, anchorIdx=${anchorIdx}`
    );
    for (let i = 0; i < unique.length; i++) {
      const info = unique[i];
      let firstText = "";
      if (glyphMapper == null ? void 0 : glyphMapper.isCalibrated()) {
        const runs = getPageRuns(info.page);
        if (runs.length > 0) {
          firstText = glyphMapper.decode(runs[0].glyphs).substring(0, 60);
        }
      }
      const markers = [];
      if (anchorMinPos >= info.minPos && anchorMinPos <= info.maxPos) markers.push("ANCHOR");
      if (info.minPos === selectedMinPos) markers.push("SELECTED");
      if (lastExtractedPositionEnd >= info.minPos && lastExtractedPositionEnd <= info.maxPos) markers.push("LAST_EXTRACTED");
      const offsetFromAnchor = anchorIdx >= 0 ? `offset=${i - anchorIdx}` : "";
      const markerStr = markers.length > 0 ? ` ← ${markers.join(", ")}` : "";
      console.log(
        `  [${i}] p${info.page.pageIndex} ${offsetFromAnchor} pos:${info.minPos}..${info.maxPos} "${firstText}"${markerStr}`
      );
    }
    console.log(
      `[kindle] ★ 请对比屏幕可见内容，告诉我哪个 [index] 的文本与当前页面匹配`
    );
    console.log("[kindle] ===== END PAGE MAP =====");
  }
  function waitForRenderData(timeoutMs = 8e3) {
    const immediate = getKindleRenderData();
    if (immediate) return Promise.resolve(immediate);
    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        observer.disconnect();
        resolve(null);
      }, timeoutMs);
      const observer = new MutationObserver(() => {
        const data = getKindleRenderData();
        if (data) {
          observer.disconnect();
          clearTimeout(timeout);
          resolve(data);
        }
      });
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: [KINDLE_RENDER_ATTR]
      });
    });
  }
  function getPageRuns(currentPage) {
    const pd = currentPage._pageData;
    if (!pd) return [];
    const children = pd.children;
    if (!children) return [];
    return children.filter((c) => c.type === "run" && !!c.glyphs);
  }
  function findCurrentPageCandidates(renderData) {
    const allPages = renderData.allTokenPages || renderData.tokens;
    if (allPages.length === 0) return [];
    const requestLog = renderData.requestLog;
    if (!requestLog || requestLog.length === 0) {
      console.log("[kindle] findCurrentPageCandidates: no requestLog, using first page");
      return allPages.length > 0 ? [allPages[0]] : [];
    }
    const currentBatch = [...requestLog].reverse().find(
      (r) => r.skipPageCount === "0" && parseInt(r.numPage) > 0
    );
    if (!currentBatch) {
      console.log("[kindle] findCurrentPageCandidates: no batch#1 in requestLog, using first page");
      return allPages.length > 0 ? [allPages[0]] : [];
    }
    const startPos = parseInt(currentBatch.startingPosition);
    if (isNaN(startPos)) return allPages.length > 0 ? [allPages[0]] : [];
    const candidates = [];
    for (let i = allPages.length - 1; i >= 0; i--) {
      const page = allPages[i];
      const blocks = page.children || [];
      if (blocks.length === 0) continue;
      const minPos = Math.min(...blocks.map((b) => b.startPositionId));
      const maxPos = Math.max(...blocks.map((b) => b.endPositionId));
      if (startPos >= minPos && startPos <= maxPos) {
        candidates.push(page);
      }
    }
    if (candidates.length > 0) {
      const batchSeqs = candidates.map((p) => p._batchSeq || "?");
      console.log(
        `[kindle] findCurrentPageCandidates: startPos=${startPos} → ${candidates.length} version(s), batchSeqs=[${batchSeqs.join(",")}], p${candidates[0].pageIndex}`
      );
    } else {
      console.warn(`[kindle] findCurrentPageCandidates: startPos=${startPos} not found in any page`);
    }
    return candidates;
  }
  function effectiveDualColumn(blocks, pageWidth) {
    if (blocks.length === 0 || pageWidth <= 0) return false;
    const midX = pageWidth / 2;
    let leftWords = 0;
    let rightWords = 0;
    let crossingWords = 0;
    for (const b of blocks) {
      for (const w of b.words || []) {
        if (w.x < midX && w.x + w.width > midX) {
          crossingWords++;
        } else if (w.x + w.width / 2 < midX) {
          leftWords++;
        } else {
          rightWords++;
        }
      }
    }
    if (crossingWords >= 3) return false;
    return leftWords >= 20 && rightWords >= 20;
  }
  function computeFullSpreadBounds(blocks) {
    if (blocks.length === 0) return { width: 1014, height: 805 };
    const maxRight = Math.max(...blocks.map((b) => b.x + b.width));
    const minX = Math.min(...blocks.map((b) => b.x));
    const maxBottom = Math.max(...blocks.map((b) => b.y + b.height));
    const minY = Math.min(...blocks.map((b) => b.y));
    return {
      width: maxRight + minX,
      // symmetric margin → full spread width
      height: maxBottom + minY
    };
  }
  function blocksToParagraphs(blocks, pageBounds, isDual) {
    if (blocks.length === 0) return [];
    const sorted = [...blocks].sort((a, b) => a.startPositionId - b.startPositionId);
    const midX = pageBounds.width / 2;
    const result = [];
    for (const block of sorted) {
      const words = block.words || [];
      if (isDual && block.width > pageBounds.width * 0.55 && words.length > 0) {
        const leftWords = words.filter((w) => w.x + w.width / 2 < midX);
        const rightWords = words.filter((w) => w.x + w.width / 2 >= midX);
        if (leftWords.length > 0 || rightWords.length > 0) {
          if (leftWords.length > 0) result.push(regionFromWords(leftWords, block));
          if (rightWords.length > 0) result.push(regionFromWords(rightWords, block));
          continue;
        }
      }
      result.push({
        bbox: { x: block.x, y: block.y, width: block.width, height: block.height },
        text: "",
        posRange: words.length > 0 ? {
          start: Math.min(...words.map((w) => w.startPositionId)),
          end: Math.max(...words.map((w) => w.endPositionId))
        } : null,
        tokenWordCount: words.length,
        sourceBlock: block
      });
    }
    return result;
  }
  function regionFromWords(words, originalBlock) {
    const sortedWords = [...words].sort((a, b) => a.startPositionId - b.startPositionId);
    const minX = Math.min(...words.map((w) => w.x));
    const minY = Math.min(...words.map((w) => w.y));
    const maxRight = Math.max(...words.map((w) => w.x + w.width));
    const maxBottom = Math.max(...words.map((w) => w.y + w.height));
    const syntheticBlock = {
      ...originalBlock,
      x: minX,
      y: minY,
      width: maxRight - minX,
      height: maxBottom - minY,
      words: sortedWords
    };
    return {
      bbox: { x: minX, y: minY, width: maxRight - minX, height: maxBottom - minY },
      text: "",
      posRange: {
        start: sortedWords[0].startPositionId,
        end: sortedWords[sortedWords.length - 1].endPositionId
      },
      tokenWordCount: words.length,
      sourceBlock: syntheticBlock
    };
  }
  function assignOcrTextByWordCount(regions, ocrTexts) {
    const fullText = ocrTexts.join(" ");
    const allWords = fullText.split(/\s+/).filter((w) => w.length > 0);
    const totalTokenWords = regions.reduce((s, r) => s + r.tokenWordCount, 0);
    if (totalTokenWords === 0 || allWords.length === 0) {
      for (let i = 0; i < regions.length && i < ocrTexts.length; i++) {
        if (!regions[i].text) regions[i].text = ocrTexts[i];
      }
      return;
    }
    let wordIdx = 0;
    for (const region of regions) {
      if (region.text && region.text.trim().length > 0) continue;
      const share = Math.max(1, Math.round(region.tokenWordCount / totalTokenWords * allWords.length));
      const endIdx = Math.min(wordIdx + share, allWords.length);
      region.text = allWords.slice(wordIdx, endIdx).join(" ");
      wordIdx = endIdx;
    }
    if (wordIdx < allWords.length && regions.length > 0) {
      const last = regions[regions.length - 1];
      last.text = (last.text + " " + allWords.slice(wordIdx).join(" ")).trim();
    }
  }
  async function tesseractWasmOCR(dataUrls) {
    try {
      console.log(`[kindle] tesseract-wasm: sending ${dataUrls.length} images, sizes=[${dataUrls.map((u) => u.length).join(",")}]`);
      const response = await chrome.runtime.sendMessage({
        type: "OCR_RECOGNIZE_WASM",
        dataUrls
      });
      if ((response == null ? void 0 : response.success) && response.text) {
        const rawLen = response.text.length;
        const nonWs = [...response.text].filter((c) => !/\s/.test(c)).length;
        console.log(`[kindle] tesseract-wasm raw: ${rawLen} chars (${nonWs} non-ws)`);
        console.log(`[kindle] tesseract-wasm first 300: "${response.text.substring(0, 300)}"`);
        const paras = response.text.split(/\n\n+/).filter((p) => p.trim().length > 0).map((p) => p.trim().replace(/[\r\n]+/g, " ").replace(/\s{2,}/g, " "));
        console.log(`[kindle] tesseract-wasm: ${paras.length} paragraphs, total=${paras.reduce((s, p) => s + p.length, 0)} chars`);
        return paras;
      }
      console.warn("[kindle] tesseract-wasm OCR failed:", response == null ? void 0 : response.error);
    } catch (error) {
      console.warn("[kindle] tesseract-wasm OCR error:", error);
    }
    return [];
  }
  async function ocrImage(imageDataUrl) {
    return tesseractWasmOCR([imageDataUrl]);
  }
  async function getFullOcrText(img, dual) {
    if (dual) {
      const [leftUrl, rightUrl] = splitDualColumn(img);
      const [leftTexts, rightTexts] = await Promise.all([ocrImage(leftUrl), ocrImage(rightUrl)]);
      return [...leftTexts, ...rightTexts];
    }
    const dataUrl = captureImageToDataURL(img);
    return ocrImage(dataUrl);
  }
  function buildWordBboxMap(block, runs, mapper, paragraphText) {
    const words = [...block.words || []].sort((a, b) => a.startPositionId - b.startPositionId);
    const entries = [];
    let searchPos = 0;
    let skipped = 0;
    for (const word of words) {
      const wordText = mapper.decodeWord(word, runs);
      if (wordText.length === 0) continue;
      let pos = paragraphText.indexOf(wordText, searchPos);
      if (pos < 0) {
        pos = paragraphText.toLowerCase().indexOf(wordText.toLowerCase(), searchPos);
      }
      if (pos < 0) {
        skipped++;
        if (skipped <= 3) {
          console.warn(
            `[kindle-bbox] SKIP word="${wordText}" searchPos=${searchPos} in "${paragraphText.substring(searchPos, searchPos + 15)}..."`
          );
        }
        searchPos += wordText.length + 1;
        continue;
      }
      entries.push({
        charStart: pos,
        charEnd: pos + wordText.length,
        text: wordText,
        bbox: { x: word.x, y: word.y, width: word.width, height: word.height }
      });
      searchPos = pos + wordText.length;
    }
    if (skipped > 0) {
      console.warn(`[kindle-bbox] ${skipped} words skipped in "${paragraphText.substring(0, 30)}..."`);
    }
    return entries;
  }
  function splitRunsByColumn(runs, blocks, pageBoundsWidth) {
    const midX = pageBoundsWidth / 2;
    const crossColumnThreshold = pageBoundsWidth * 0.55;
    function getRunColumn(run) {
      var _a, _b;
      for (const block of blocks) {
        if (run.startPositionId >= block.startPositionId && run.startPositionId <= block.endPositionId) {
          if (block.width >= crossColumnThreshold) {
            const x = ((_a = run.transform) == null ? void 0 : _a[4]) ?? block.x + block.width / 2;
            return x < midX ? "left" : "right";
          }
          return block.x + block.width / 2 < midX ? "left" : "right";
        }
      }
      return (((_b = run.transform) == null ? void 0 : _b[4]) ?? 0) < midX ? "left" : "right";
    }
    return {
      leftRuns: runs.filter((r) => getRunColumn(r) === "left"),
      rightRuns: runs.filter((r) => getRunColumn(r) === "right")
    };
  }
  function findBestPage(candidates, ocrTexts, leftOcr, rightOcr, pageBoundsWidth) {
    if (candidates.length === 0 || ocrTexts.length === 0) return null;
    let best = null;
    let tested = 0;
    for (const candidate of candidates) {
      const blocks = candidate.page.children || [];
      const runs = getPageRuns(candidate.page);
      if (runs.length === 0) continue;
      const mapper = new KindleGlyphMapper();
      mapper.identifySpaceGlyph(runs);
      let quality;
      const dataDual = effectiveDualColumn(blocks, pageBoundsWidth);
      if (dataDual && leftOcr.length > 0 && rightOcr.length > 0) {
        const { leftRuns, rightRuns } = splitRunsByColumn(runs, blocks, pageBoundsWidth);
        let leftQ = 1, rightQ = 1;
        const leftMapper = new KindleGlyphMapper();
        const rightMapper = new KindleGlyphMapper();
        if (leftOcr.length > 0 && leftRuns.length > 0) {
          leftMapper.identifySpaceGlyph(leftRuns);
          leftQ = leftMapper.calibrate(leftOcr, [candidate.page], leftRuns, true, false, "left");
        }
        if (rightOcr.length > 0 && rightRuns.length > 0) {
          rightMapper.identifySpaceGlyph(rightRuns);
          rightQ = rightMapper.calibrate(rightOcr, [candidate.page], rightRuns, true, false, "right");
        }
        if (leftQ >= 0.3) mapper.mergeFrom(leftMapper);
        if (rightQ >= 0.3) mapper.mergeFrom(rightMapper);
        mapper.resetTotalUniqueGlyphs(
          Math.max(leftMapper.uniqueGlyphCount, rightMapper.uniqueGlyphCount)
        );
        const totalRuns = leftRuns.length + rightRuns.length;
        quality = totalRuns > 0 ? (leftQ * leftRuns.length + rightQ * rightRuns.length) / totalRuns : 0;
      } else {
        quality = mapper.calibrate(ocrTexts, [candidate.page], runs, true);
      }
      tested++;
      if (quality > 0.2) {
        console.log(
          `[kindle] findBestPage: ${candidate.source} p${candidate.page.pageIndex} → quality=${(quality * 100).toFixed(0)}% ★`
        );
      }
      if (!best || quality > best.quality) {
        best = { page: candidate.page, mapper, quality };
      }
      if (quality >= 0.95) break;
    }
    if (best) {
      console.log(
        `[kindle] findBestPage: winner p${best.page.pageIndex} quality=${(best.quality * 100).toFixed(0)}% (${tested}/${candidates.length} tested)`
      );
    }
    return best;
  }
  async function extractWithTokenData() {
    var _a, _b, _c;
    const t0 = performance.now();
    if (currentOverlay) {
      currentOverlay.destroy();
      currentOverlay = null;
    }
    const img = findKindleBlobImage();
    if (!img) return [];
    console.log(`[kindle] Image: ${img.naturalWidth}×${img.naturalHeight}, src=${img.src.substring(0, 50)}...`);
    const savedRenderSeq = lastRenderSeq;
    lastRenderSeq = 0;
    let renderData = getKindleRenderData();
    if (!renderData) {
      lastRenderSeq = savedRenderSeq;
      renderData = await waitForRenderData();
      if (!(renderData == null ? void 0 : renderData.tokens)) {
        console.log("[kindle] No TAR render data available");
        return [];
      }
    }
    lastRenderSeq = renderData.seq;
    const allPages = renderData.allTokenPages || renderData.tokens || [];
    if (allPages.length === 0) {
      console.warn("[kindle] No token pages in render data");
      return [];
    }
    const currentPageNum = readKindlePageNumber();
    const dpr = window.devicePixelRatio || 2;
    const pageBounds = {
      width: img.naturalWidth / dpr,
      height: img.naturalHeight / dpr
    };
    const anchorCandidates = findCurrentPageCandidates(renderData);
    const anchorPage = anchorCandidates.length > 0 ? anchorCandidates[0] : null;
    const anchorBlocks = anchorPage ? anchorPage.children || [] : [];
    const anchorDual = anchorPage ? effectiveDualColumn(anchorBlocks, pageBounds.width) : false;
    const stride = anchorDual ? 2 : 1;
    const renderTimePageNum = getRenderTimePageNumber(renderData, stride);
    const imgDual = isDualColumn(img);
    const requestLog = renderData.requestLog || [];
    console.log(`[kindle] ===== REQUEST LOG (${requestLog.length} entries) =====`);
    for (const entry of requestLog) {
      const type = entry.skipPageCount === "0" ? parseInt(entry.numPage) > 0 ? "batch#1(cur+fwd)" : "batch#2(bwd)" : "batch#3(more-fwd)";
      console.log(
        `  seq=${entry.seq} ${type} skip=${entry.skipPageCount} num=${entry.numPage} startPos=${entry.startingPosition} pageAtRender=${entry.pageNumberAtRender || "?"} posRange=${entry.tokenPosRange}`
      );
    }
    const uniquePages = buildUniquePageList(allPages);
    console.log(
      `[kindle] Page selection: allPages=${allPages.length} → ${uniquePages.length} unique, autoAdvance=${isAutoAdvanceExtraction}, lastPosEnd=${lastExtractedPositionEnd}, currentPageNum=${currentPageNum}, renderTimePageNum=${renderTimePageNum}`
    );
    const delta = currentPageNum > 0 && renderTimePageNum > 0 ? currentPageNum - renderTimePageNum : 0;
    let currentPage;
    let ocrTexts = [];
    let leftOcr = [];
    let rightOcr = [];
    let useOcrFallback = false;
    {
      const candidates = [];
      if (renderTimePageNum > 0 && currentPageNum > 0 && currentPageNum !== renderTimePageNum && anchorPage) {
        const tokenOffset = delta * stride;
        const anchorMinPos = Math.min(...(anchorPage.children || []).map((c) => c.startPositionId));
        const s2page = findPageAtOffset(allPages, anchorMinPos, tokenOffset);
        if (s2page && !candidates.some((c) => c.page === s2page)) {
          candidates.push({ page: s2page, source: `strategy2(delta=${delta})` });
          console.log(`[kindle] Candidate: strategy2 delta=${delta} → p${s2page.pageIndex}`);
        }
      }
      if (anchorPage && !candidates.some((c) => c.page === anchorPage)) {
        candidates.push({ page: anchorPage, source: "anchor" });
      }
      {
        const priorityCenter = candidates.length > 0 ? uniquePages.findIndex((info) => {
          const firstCandidate = candidates[0].page;
          const fcMinPos = Math.min(...(firstCandidate.children || []).map((c) => c.startPositionId));
          return fcMinPos >= info.minPos && fcMinPos <= info.maxPos;
        }) : 0;
        const remainingIndices = uniquePages.map((info, idx) => ({ info, idx })).filter(({ info }) => !candidates.some((c) => {
          const cMinPos = Math.min(...(c.page.children || []).map((ch) => ch.startPositionId));
          return cMinPos >= info.minPos && cMinPos <= info.maxPos;
        })).sort(
          (a, b) => Math.abs(a.idx - priorityCenter) - Math.abs(b.idx - priorityCenter)
        );
        for (const { info, idx } of remainingIndices) {
          candidates.push({ page: info.page, source: `page[${idx}]` });
        }
      }
      if (candidates.length === 0) {
        console.warn("[kindle] No candidate pages found");
        return [];
      }
      console.log(
        `[kindle] ${candidates.length} candidates: ` + candidates.map((c) => `${c.source}(p${c.page.pageIndex})`).join(", ")
      );
      {
        const firstBlocks = candidates[0].page.children || [];
        const dataDualForOcr = effectiveDualColumn(firstBlocks, pageBounds.width);
        if (dataDualForOcr) {
          const [leftUrl, rightUrl] = splitDualColumn(img);
          [leftOcr, rightOcr] = await Promise.all([ocrImage(leftUrl), ocrImage(rightUrl)]);
          ocrTexts = [...leftOcr, ...rightOcr];
          console.log(
            `[kindle] Dual-column OCR: left=${leftOcr.length} paragraphs, right=${rightOcr.length} paragraphs`
          );
        } else {
          ocrTexts = await getFullOcrText(img, false);
          console.log(`[kindle] Single-column OCR: ${ocrTexts.length} paragraphs`);
        }
      }
      if (ocrTexts.length === 0) {
        console.warn("[kindle] OCR returned no text");
        return [];
      }
      const bestResult = findBestPage(candidates, ocrTexts, leftOcr, rightOcr, pageBounds.width);
      if (bestResult && bestResult.quality >= 0.3) {
        currentPage = bestResult.page;
        glyphMapper = bestResult.mapper;
        useOcrFallback = bestResult.quality < 0.7 || !glyphMapper.isCalibrated();
        console.log(
          `[kindle] Using best page p${currentPage.pageIndex} (quality=${(bestResult.quality * 100).toFixed(0)}%${useOcrFallback ? ", OCR fallback" : ""})`
        );
      } else {
        currentPage = (bestResult == null ? void 0 : bestResult.page) || candidates[0].page;
        glyphMapper = new KindleGlyphMapper();
        useOcrFallback = true;
        console.log(
          `[kindle] Calibration quality too low (${bestResult ? (bestResult.quality * 100).toFixed(0) + "%" : "no result"}) → OCR-only fallback`
        );
      }
    }
    hasTokenData = true;
    const blocks = currentPage.children || [];
    if (blocks.length === 0) return [];
    const runs = getPageRuns(currentPage);
    const pageBoundsFromBlocks = computeFullSpreadBounds(blocks);
    const dataDual = effectiveDualColumn(blocks, pageBounds.width);
    const globalFont = runs.length > 0 ? extractFontInfo(runs) : { fontFamily: "Georgia, serif", fontSize: 16, fontWeight: 400 };
    console.log(
      `[kindle] page${currentPage.pageIndex}: ${blocks.length} blocks, ${blocks.reduce((s, b) => {
        var _a2;
        return s + (((_a2 = b.words) == null ? void 0 : _a2.length) || 0);
      }, 0)} words, ${runs.length} runs, imgDual=${imgDual}, dataDual=${dataDual}`
    );
    console.log(
      `[kindle] pageBounds: image=${pageBounds.width}x${pageBounds.height}, blocks=${pageBoundsFromBlocks.width.toFixed(1)}x${pageBoundsFromBlocks.height.toFixed(1)}, img.natural=${img.naturalWidth}x${img.naturalHeight}, dpr=${dpr}, img.offset=${img.offsetWidth}x${img.offsetHeight}`
    );
    for (let i = 0; i < Math.min(3, blocks.length); i++) {
      const b = blocks[i];
      const firstWord = (_a = b.words) == null ? void 0 : _a[0];
      console.log(
        `[kindle] block[${i}]: bbox(${b.x.toFixed(1)},${b.y.toFixed(1)},${b.width.toFixed(1)},${b.height.toFixed(1)}) words=${((_b = b.words) == null ? void 0 : _b.length) || 0} pos=${b.startPositionId}..${b.endPositionId}` + (firstWord ? ` firstWord(${firstWord.x.toFixed(1)},${firstWord.y.toFixed(1)},${firstWord.width.toFixed(1)},${firstWord.height.toFixed(1)})` : "")
      );
    }
    dumpPageMap(allPages, currentPage, anchorPage, renderData, currentPageNum, renderTimePageNum);
    {
      const batchGlyphs = /* @__PURE__ */ new Map();
      for (const page of allPages) {
        const bseq = page._batchSeq || 0;
        const pageRuns = getPageRuns(page);
        if (!batchGlyphs.has(bseq)) batchGlyphs.set(bseq, /* @__PURE__ */ new Set());
        const set = batchGlyphs.get(bseq);
        for (const run of pageRuns) {
          for (const g of run.glyphs) set.add(g);
        }
      }
      for (const [bseq, glyphs] of batchGlyphs) {
        const sorted = [...glyphs].sort((a, b) => a - b);
        console.log(
          `[kindle] DIAG batch#${bseq}: ${glyphs.size} unique glyphs, range=[${sorted[0] ?? "?"}..${sorted[sorted.length - 1] ?? "?"}], sample: ${sorted.slice(0, 8).join(",")}`
        );
      }
    }
    const paraRegions = blocksToParagraphs(blocks, pageBounds, dataDual);
    console.log(`[kindle] ${paraRegions.length} paragraphs from token blocks`);
    if ((glyphMapper == null ? void 0 : glyphMapper.isCalibrated()) && runs.length > 0) {
      const regionBlocks = paraRegions.filter((r) => r.sourceBlock).map((r) => r.sourceBlock);
      const decodedTexts = glyphMapper.decodeParagraphs(regionBlocks, runs);
      let ti = 0;
      for (const region of paraRegions) {
        if (region.sourceBlock) {
          region.text = decodedTexts[ti++] || "";
        }
      }
      console.log(`[kindle] Paragraph text: glyph-decoded (${decodedTexts.length} paragraphs)`);
    } else if (ocrTexts.length > 0) {
      assignOcrTextByWordCount(paraRegions, ocrTexts);
      console.log(`[kindle] Paragraph text: OCR fallback (mapper not calibrated)`);
    }
    for (let i = 0; i < paraRegions.length; i++) {
      const r = paraRegions[i];
      console.log(
        `[kindle] para[${i}]: bbox(${r.bbox.x.toFixed(0)},${r.bbox.y.toFixed(0)},${r.bbox.width.toFixed(0)},${r.bbox.height.toFixed(0)}) words=${r.tokenWordCount} "${r.text.substring(0, 40)}..."`
      );
    }
    if (currentOverlay) currentOverlay.destroy();
    currentOverlay = new KindleOverlay(img);
    currentOverlay.init(false);
    const result = [];
    for (const region of paraRegions) {
      const text = region.text.trim();
      if (!text || text.length < 2) continue;
      let wordBboxMap;
      if (region.sourceBlock && (glyphMapper == null ? void 0 : glyphMapper.isCalibrated()) && runs.length > 0) {
        const entries = buildWordBboxMap(region.sourceBlock, runs, glyphMapper, text);
        if (entries.length > 0) {
          wordBboxMap = {
            entries,
            pageBounds,
            isRightColumn: false,
            isDual: dataDual
          };
        }
      }
      if (region.bbox.width > 0 && region.bbox.height > 0) {
        const { element, textElement } = currentOverlay.createParagraphOverlay(
          region.bbox,
          text,
          globalFont,
          false,
          pageBounds
        );
        result.push({ text, element, textElement, canHighlight: true, wordBboxMap });
      } else {
        result.push({ text, element: document.body, canHighlight: false });
      }
    }
    if (blocks.length > 0) {
      lastExtractedPositionEnd = Math.max(...blocks.map((b) => b.endPositionId));
      lastExtractedPageNumber = readKindlePageNumber();
      currentPage._batchSeq;
    }
    console.log(
      `[kindle] Done: ${result.length} paras, page=${lastExtractedPageNumber}, "${(_c = result[0]) == null ? void 0 : _c.text.substring(0, 50)}..."`
    );
    console.log(`[kindle] extractWithTokenData: ${(performance.now() - t0).toFixed(0)}ms`);
    return result;
  }
  function extractFromDOM() {
    for (const sel of KINDLE_IFRAME_SELECTORS) {
      const iframe = document.querySelector(sel);
      if (iframe == null ? void 0 : iframe.contentDocument) {
        const paragraphs = extractFromContainer(iframe.contentDocument.body);
        if (paragraphs.length > 0) {
          console.log("[kindle] 从同源 iframe 提取成功:", paragraphs.length);
          return paragraphs;
        }
      }
    }
    for (const sel of KINDLE_CONTENT_SELECTORS) {
      const container = document.querySelector(sel);
      if (container) {
        const paragraphs = extractFromContainer(container);
        if (paragraphs.length > 0) {
          console.log("[kindle] 从主页面容器提取成功:", sel, paragraphs.length);
          return paragraphs;
        }
      }
    }
    return [];
  }
  function extractFromContainer(container) {
    var _a, _b;
    const root = container instanceof Document ? container.body : container;
    if (!root) return [];
    const result = [];
    const seenTexts = /* @__PURE__ */ new Set();
    const paragraphEls = root.querySelectorAll('p, div[class*="paragraph"], span[class*="text"], .a-text-content');
    for (const el of Array.from(paragraphEls)) {
      const htmlEl = el;
      const text = (_a = htmlEl.textContent) == null ? void 0 : _a.trim();
      if (!text || text.length < 5) continue;
      const key = text.substring(0, 100);
      if (seenTexts.has(key)) continue;
      seenTexts.add(key);
      if (!isJunkText(text)) {
        result.push({ text, element: htmlEl, canHighlight: true });
      }
    }
    if (result.length <= 3) {
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let node;
      while (node = walker.nextNode()) {
        const text = (_b = node.textContent) == null ? void 0 : _b.trim();
        if (!text || text.length < 10) continue;
        const key = text.substring(0, 100);
        if (seenTexts.has(key)) continue;
        seenTexts.add(key);
        const parent = node.parentElement;
        if (parent && !isJunkText(text)) {
          result.push({ text, element: parent, canHighlight: true });
        }
      }
    }
    return result;
  }
  function cleanOCRText(text) {
    return text.replace(/\|/g, "I").replace(/\s{2,}/g, " ").replace(/- *\n */g, "").replace(/\n/g, " ").trim();
  }
  async function extractViaOCR() {
    const img = findKindleBlobImage();
    if (!img) return [];
    console.log(
      "[kindle] OCR fallback (no overlay)...",
      `${img.naturalWidth}×${img.naturalHeight}`
    );
    try {
      const texts = await getFullOcrText(img, isDualColumn(img));
      if (texts.length > 0) {
        console.log(`[kindle] OCR (no overlay): ${texts.length} paragraphs`);
        return texts.map((t) => ({ text: cleanOCRText(t), element: document.body, canHighlight: false })).filter((p) => p.text.length > 0);
      }
    } catch (error) {
      console.error("[kindle] OCR fallback failed:", error);
    }
    return [];
  }
  const kindleExtractor = {
    siteName: "Kindle",
    matches: ["read.amazon.cn", "read.amazon.com"],
    extractText() {
      const paragraphs = extractFromDOM();
      if (paragraphs.length === 0) return null;
      return paragraphs.map((p) => p.text).join("\n\n");
    },
    extractTitle() {
      var _a;
      const titleSelectors = [
        ".title",
        "#kindle-reader-title",
        '[data-testid="book-title"]',
        "h1"
      ];
      for (const sel of titleSelectors) {
        const el = document.querySelector(sel);
        if ((_a = el == null ? void 0 : el.textContent) == null ? void 0 : _a.trim()) return el.textContent.trim();
      }
      return document.title.replace(/\s*[-–—|]\s*Kindle\s*Cloud\s*Reader\s*$/i, "").replace(/\s*[-–—|]\s*Amazon\s*$/i, "").trim() || null;
    },
    extractParagraphsWithElements() {
      return extractFromDOM();
    },
    async extractParagraphsAsync() {
      try {
        const tokenResult = await extractWithTokenData();
        if (tokenResult.length > 0) return tokenResult;
      } catch (error) {
        console.error("[kindle] Token extraction failed:", error);
      }
      const syncResult = extractFromDOM();
      if (syncResult.length > 0) return syncResult;
      try {
        const ocrResult = await extractViaOCR();
        if (ocrResult.length > 0) return ocrResult;
      } catch (error) {
        console.error("[kindle] OCR extraction failed:", error);
      }
      console.log("[kindle] All methods failed, trying iframe fallback...");
      try {
        const response = await chrome.runtime.sendMessage({
          type: "EXTRACT_FROM_IFRAMES"
        });
        if ((response == null ? void 0 : response.paragraphs) && response.paragraphs.length > 0) {
          console.log("[kindle] iframe 提取成功:", response.paragraphs.length);
          return response.paragraphs.map((p) => ({
            text: p.text,
            element: document.body,
            canHighlight: false
          }));
        }
      } catch (error) {
        console.error("[kindle] iframe 提取失败:", error);
      }
      console.log("[kindle] 所有提取方法均失败");
      return [];
    },
    supportsHighlight() {
      if (hasTokenData) return true;
      return findKindleBlobImage() === null;
    }
  };
  const LAKE_PARAGRAPH_TAGS = [
    "NE-P",
    "NE-H1",
    "NE-H2",
    "NE-H3",
    "NE-H4",
    "NE-H5",
    "NE-H6",
    "NE-ULI",
    "NE-OLI",
    "NE-QUOTE",
    // 标准 HTML 标签作为 fallback
    "P",
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "LI",
    "BLOCKQUOTE"
  ];
  const LAKE_SKIP_TAGS = [
    "NE-CODE-BLOCK",
    "NE-TABLE-HOLE",
    "NE-IMAGE",
    "NE-CARD",
    "NE-DIAGRAM",
    "NE-VIDEO",
    "NE-AUDIO",
    "NE-FILE",
    "NE-MINDMAP",
    "NE-EMBED",
    "PRE",
    "CODE"
  ];
  const LAKE_CONTENT_SELECTORS = [
    ".ne-viewer-body",
    ".lake-content",
    ".lake-content-editor-core",
    ".doc-reader-content",
    ".ne-editor-container",
    "[data-lake-container]",
    "[data-lake-id]",
    // 钉钉公开文档的特殊容器
    ".dingdoc-mainsite-public-root",
    ".publish-doc-content",
    ".doc-content",
    '[class*="DocReader"]',
    '[class*="doc-reader"]'
  ];
  function cleanLakeText(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/●/g, "").replace(/○/g, "").replace(/\s+/g, " ").trim();
  }
  function findLakeContentContainer() {
    for (const selector of LAKE_CONTENT_SELECTORS) {
      const el = document.querySelector(selector);
      if (el && el.textContent && el.textContent.trim().length > 50) {
        return el;
      }
    }
    return null;
  }
  function extractLakeParagraphs(logPrefix = "[lake]") {
    console.log(`${logPrefix} 开始提取段落...`);
    const result = [];
    const content = findLakeContentContainer();
    if (!content) {
      console.log(`${logPrefix} 未找到 Lake 内容容器`);
      console.log(`${logPrefix} 页面可用的容器:`, {
        neViewerBody: !!document.querySelector(".ne-viewer-body"),
        lakeContent: !!document.querySelector(".lake-content"),
        lakeContainer: !!document.querySelector("[data-lake-container]"),
        lakeId: !!document.querySelector("[data-lake-id]")
      });
      return result;
    }
    console.log(`${logPrefix} 找到内容容器:`, content.className || content.tagName);
    console.log(`${logPrefix} 子元素数:`, content.children.length);
    const seenTexts = /* @__PURE__ */ new Set();
    const traverse = (container, depth = 0) => {
      for (const child of Array.from(container.children)) {
        const el = child;
        const tagName = el.tagName.toUpperCase();
        if (LAKE_SKIP_TAGS.includes(tagName)) {
          continue;
        }
        if (LAKE_PARAGRAPH_TAGS.includes(tagName)) {
          const text = cleanLakeText(el.textContent || "");
          if (!text || text.length < 5) {
            continue;
          }
          const textKey = text.substring(0, 100);
          if (seenTexts.has(textKey)) {
            continue;
          }
          seenTexts.add(textKey);
          result.push({
            text,
            element: el,
            canHighlight: true
          });
          if (result.length <= 5) {
            console.log(`${logPrefix} 提取段落:`, tagName, text.substring(0, 50));
          }
        } else if (depth < 10) {
          traverse(el, depth + 1);
        }
      }
    };
    traverse(content);
    console.log(`${logPrefix} 提取完成，段落数:`, result.length);
    return result;
  }
  function extractLakeText() {
    const content = findLakeContentContainer();
    if (content) {
      return cleanLakeText(content.textContent || "");
    }
    return null;
  }
  const yuqueExtractor = {
    siteName: "语雀",
    matches: ["yuque.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      return extractLakeText();
    },
    extractTitle() {
      var _a;
      const titleSelectors = [
        ".index-module_title_T-MBH",
        ".doc-title",
        ".article-title",
        "h1:first-of-type"
      ];
      for (const selector of titleSelectors) {
        const el = document.querySelector(selector);
        if (el && ((_a = el.textContent) == null ? void 0 : _a.trim())) {
          return el.textContent.trim();
        }
      }
      return document.title.replace(" · 语雀", "").replace(" - 语雀", "").trim() || null;
    },
    extractLanguage() {
      const htmlLang = document.documentElement.lang;
      if (htmlLang && htmlLang.startsWith("en")) {
        return "en";
      }
      return "zh";
    },
    extractParagraphsWithElements() {
      return extractLakeParagraphs("[yuque]");
    }
  };
  const CONTENT_SELECTORS = [
    ".page-block.root-block",
    '[data-content-editable-root="true"]',
    ".doc-content-wrapper",
    ".lark-docs-reader",
    ".doc-body",
    ".render-docs-content"
  ];
  const SKIP_BLOCK_TYPES = /* @__PURE__ */ new Set([
    "code",
    "table",
    "image",
    "file",
    "bitable",
    "diagram",
    "iframe",
    "sheet"
  ]);
  function clean(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function findContent() {
    var _a;
    for (const sel of CONTENT_SELECTORS) {
      const el = document.querySelector(sel);
      if (el && (((_a = el.textContent) == null ? void 0 : _a.trim().length) || 0) > 50) return el;
    }
    return null;
  }
  function findScroller() {
    for (const sel of [".bear-web-x-container", ".page-main-item", ".page-main"]) {
      const el = document.querySelector(sel);
      if (el && el.scrollHeight > el.clientHeight) return el;
    }
    return null;
  }
  function isToc(text, blockType) {
    if (/[\.·。]{4,}|…{2,}/.test(text)) return true;
    if (blockType.startsWith("heading") && text === "目录") return true;
    return false;
  }
  function collectNewBlocks(content, seen, scrollY) {
    const newBlocks = [];
    content.querySelectorAll("div.block[data-block-type]").forEach((node) => {
      const el = node;
      const blockId = el.getAttribute("data-block-id") || "";
      if (!blockId || seen.has(blockId)) return;
      if (el.classList.contains("isEmpty")) return;
      const blockType = el.getAttribute("data-block-type") || "";
      if (SKIP_BLOCK_TYPES.has(blockType)) return;
      if (el.closest(".catalogue-container")) return;
      const text = clean(el.textContent || "");
      if (!text || text.length < 2) return;
      if (isToc(text, blockType)) return;
      seen.add(blockId);
      newBlocks.push({ text, blockId, scrollY });
    });
    return newBlocks;
  }
  async function scrollAndCollect(scroller, content) {
    const all = [];
    const seen = /* @__PURE__ */ new Set();
    const originalTop = scroller.scrollTop;
    const step = scroller.clientHeight * 0.7;
    let maxH = scroller.scrollHeight;
    let pos = 0;
    while (pos < maxH) {
      scroller.scrollTop = pos;
      await new Promise((r) => setTimeout(r, 200));
      const newBlocks = collectNewBlocks(content, seen, pos);
      all.push(...newBlocks);
      pos += step;
      const h = scroller.scrollHeight;
      if (h > maxH && h < maxH * 3) maxH = h;
    }
    scroller.scrollTop = scroller.scrollHeight;
    await new Promise((r) => setTimeout(r, 200));
    all.push(...collectNewBlocks(content, seen, scroller.scrollTop));
    scroller.scrollTop = originalTop;
    return all;
  }
  function dedup(blocks) {
    const result = [];
    for (const block of blocks) {
      if (!result.some((prev) => prev.text.includes(block.text))) {
        result.push(block);
      }
    }
    return result;
  }
  function findElementByBlockId(blockId) {
    return document.querySelector(`div.block[data-block-id="${blockId}"]`);
  }
  const feishuExtractor = {
    siteName: "飞书文档",
    matches: ["feishu.cn", "larksuite.com", "larkoffice.com"],
    supportsHighlight: () => true,
    extractText() {
      const c = findContent();
      return c ? clean(c.textContent || "") : null;
    },
    extractTitle() {
      var _a;
      for (const sel of [".page-block-header h1", ".doc-title", ".lark-docs-title", "h1:first-of-type"]) {
        const el = document.querySelector(sel);
        if ((_a = el == null ? void 0 : el.textContent) == null ? void 0 : _a.trim()) return clean(el.textContent);
      }
      return document.title.replace(/ - 飞书文档.*$/, "").replace(/ - Lark Docs.*$/, "").trim() || null;
    },
    extractLanguage: () => {
      var _a;
      return ((_a = document.documentElement.lang) == null ? void 0 : _a.startsWith("en")) ? "en" : "zh";
    },
    extractParagraphsWithElements() {
      const content = findContent();
      if (!content) return [];
      const seen = /* @__PURE__ */ new Set();
      const blocks = collectNewBlocks(content, seen, 0);
      const result = dedup(blocks);
      return result.map((b) => {
        const el = findElementByBlockId(b.blockId);
        return { text: b.text, element: el || document.body, canHighlight: !!el };
      });
    },
    async extractParagraphsAsync() {
      console.log("[feishu] 开始提取...");
      const content = findContent();
      if (!content) {
        console.log("[feishu] 未找到内容容器");
        return [];
      }
      const scroller = findScroller();
      let collected;
      if (scroller) {
        console.log(`[feishu] 滚动提取, scrollH=${scroller.scrollHeight}, viewH=${scroller.clientHeight}`);
        collected = await scrollAndCollect(scroller, content);
      } else {
        console.log("[feishu] 无滚动容器，仅提取可见内容");
        const seen = /* @__PURE__ */ new Set();
        collected = collectNewBlocks(content, seen, 0);
      }
      const result = dedup(collected);
      console.log(`[feishu] 收集 ${collected.length} → 去重 ${result.length} 段`);
      return result.map((b) => {
        const el = findElementByBlockId(b.blockId);
        return { text: b.text, element: el || document.body, canHighlight: !!el };
      });
    }
  };
  const PUBLIC_DOC_SELECTORS = [
    ".publish-doc-content",
    ".doc-content",
    ".dingdoc-mainsite-public-root",
    '[class*="DocReader"]',
    '[class*="doc-reader"]',
    ".article-content",
    "article",
    "main"
  ];
  function extractFromPublicDoc() {
    var _a, _b, _c;
    console.log("[dingtalk] 尝试公开文档提取...");
    const result = [];
    let content = null;
    for (const selector of PUBLIC_DOC_SELECTORS) {
      const el = document.querySelector(selector);
      if (el && el.textContent && el.textContent.trim().length > 50) {
        content = el;
        console.log("[dingtalk] 找到公开文档容器:", selector);
        break;
      }
    }
    if (!content) {
      console.log("[dingtalk] 未找到公开文档容器");
      console.log("[dingtalk] 页面结构:", {
        body: document.body.className,
        firstDiv: (_a = document.body.querySelector("div")) == null ? void 0 : _a.className,
        hasIframe: !!document.querySelector("iframe"),
        textLength: ((_b = document.body.textContent) == null ? void 0 : _b.length) || 0
      });
      return result;
    }
    console.log("[dingtalk] 容器类名:", content.className);
    console.log("[dingtalk] 容器文本长度:", ((_c = content.textContent) == null ? void 0 : _c.length) || 0);
    const seenTexts = /* @__PURE__ */ new Set();
    const lakeElements = content.querySelectorAll(LAKE_PARAGRAPH_TAGS.join(", "));
    if (lakeElements.length > 0) {
      console.log("[dingtalk] 找到 Lake 组件:", lakeElements.length);
      for (const el of Array.from(lakeElements)) {
        const htmlEl = el;
        const text = cleanLakeText(htmlEl.textContent || "");
        if (!text || text.length < 5) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
    }
    if (result.length === 0) {
      console.log("[dingtalk] 使用标准 HTML 提取...");
      const htmlElements = content.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, blockquote, div.paragraph, [data-type="paragraph"]');
      for (const el of Array.from(htmlElements)) {
        const htmlEl = el;
        const text = cleanLakeText(htmlEl.textContent || "");
        if (!text || text.length < 10) continue;
        if (htmlEl.tagName === "DIV" && htmlEl.children.length > 3) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
    }
    if (result.length === 0) {
      console.log("[dingtalk] 尝试深度文本提取...");
      const allDivs = content.querySelectorAll("div");
      for (const div of Array.from(allDivs)) {
        const htmlEl = div;
        if (htmlEl.querySelector("div")) continue;
        const text = cleanLakeText(htmlEl.textContent || "");
        if (!text || text.length < 15) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
    }
    console.log("[dingtalk] 公开文档提取结果:", result.length, "段落");
    return result;
  }
  const dingtalkExtractor = {
    siteName: "钉钉文档",
    matches: ["dingtalk.com", "alidocs.dingtalk.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      const lakeText = extractLakeText();
      if (lakeText && lakeText.length > 50) {
        return lakeText;
      }
      for (const selector of PUBLIC_DOC_SELECTORS) {
        const content = document.querySelector(selector);
        if (content && content.textContent) {
          return cleanLakeText(content.textContent);
        }
      }
      return null;
    },
    extractTitle() {
      var _a;
      const titleSelectors = [
        ".doc-title",
        ".ne-title",
        ".document-title",
        '[data-testid="doc-title"]',
        "h1:first-of-type",
        ".publish-doc-title"
      ];
      for (const selector of titleSelectors) {
        const el = document.querySelector(selector);
        if (el && ((_a = el.textContent) == null ? void 0 : _a.trim())) {
          return el.textContent.trim();
        }
      }
      return document.title.replace(" - 钉钉文档", "").replace(" | 钉钉", "").trim() || null;
    },
    extractLanguage() {
      const htmlLang = document.documentElement.lang;
      if (htmlLang && htmlLang.startsWith("en")) {
        return "en";
      }
      return "zh";
    },
    extractParagraphsWithElements() {
      console.log("[dingtalk] 开始提取段落...");
      const lakeContainer = findLakeContentContainer();
      if (lakeContainer) {
        console.log("[dingtalk] 使用 Lake 编辑器提取");
        return extractLakeParagraphs("[dingtalk]");
      }
      return extractFromPublicDoc();
    }
  };
  const HELP_PAGE_SELECTORS = [
    "article",
    "main article",
    ".article-content"
  ];
  const DOC_PAGE_SELECTORS = [
    ".notion-page-content",
    ".notion-scroller",
    '[data-content-editable-root="true"]',
    ".notion-app-inner",
    "main"
  ];
  const HELP_PARAGRAPH_SELECTORS = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const DOC_BLOCK_SELECTORS = [
    ".notion-text-block",
    ".notion-header-block",
    ".notion-sub_header-block",
    ".notion-sub_sub_header-block",
    ".notion-bulleted_list-block",
    ".notion-numbered_list-block",
    ".notion-to_do-block",
    ".notion-toggle-block",
    ".notion-quote-block",
    ".notion-callout-block",
    "[data-block-id]"
  ];
  const SKIP_SELECTORS$7 = [
    ".notion-code-block",
    ".notion-image-block",
    ".notion-video-block",
    ".notion-embed-block",
    ".notion-table-block",
    ".notion-collection_view-block",
    "script",
    "style",
    "nav",
    "header",
    "footer",
    '[aria-hidden="true"]'
  ];
  function cleanNotionText(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/^\s*[•◦▪]\s*/, "").replace(/^\s*\d+\.\s*/, "").replace(/\s+/g, " ").trim();
  }
  function isHelpPage() {
    const url = window.location.href;
    return url.includes("notion.com/help") || url.includes("notion.so/help") || url.includes("notion.com/guides") || url.includes("notion.so/guides") || url.includes("notion.com/blog") || url.includes("notion.so/blog");
  }
  function shouldSkipElement$7(el) {
    for (const selector of SKIP_SELECTORS$7) {
      if (el.matches(selector) || el.closest(selector)) {
        return true;
      }
    }
    return false;
  }
  function extractFromHelpPage() {
    console.log("[notion] 检测到帮助/营销页面，使用标准 HTML 提取");
    const result = [];
    let content = null;
    for (const selector of HELP_PAGE_SELECTORS) {
      content = document.querySelector(selector);
      if (content && content.textContent && content.textContent.trim().length > 100) {
        break;
      }
    }
    if (!content) {
      console.log("[notion] 未找到文章容器");
      return result;
    }
    console.log("[notion] 找到文章容器:", content.tagName, content.className);
    const seenTexts = /* @__PURE__ */ new Set();
    const elements = content.querySelectorAll(HELP_PARAGRAPH_SELECTORS);
    for (const el of Array.from(elements)) {
      const htmlEl = el;
      if (shouldSkipElement$7(htmlEl)) {
        continue;
      }
      const text = cleanNotionText(htmlEl.textContent || "");
      if (!text || text.length < 5) {
        continue;
      }
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) {
        continue;
      }
      seenTexts.add(textKey);
      result.push({
        text,
        element: htmlEl,
        canHighlight: true
      });
    }
    return result;
  }
  function extractFromDocPage() {
    console.log("[notion] 检测到用户文档页面，使用 block-based 提取");
    const result = [];
    let content = null;
    for (const selector of DOC_PAGE_SELECTORS) {
      content = document.querySelector(selector);
      if (content && content.textContent && content.textContent.trim().length > 50) {
        break;
      }
    }
    if (!content) {
      console.log("[notion] 未找到内容容器");
      return result;
    }
    console.log("[notion] 找到内容容器:", content.className || content.tagName);
    const seenTexts = /* @__PURE__ */ new Set();
    const blocks = content.querySelectorAll("[data-block-id]");
    console.log("[notion] 找到块数量:", blocks.length);
    for (const block of Array.from(blocks)) {
      const el = block;
      if (shouldSkipElement$7(el)) {
        continue;
      }
      const textLeaf = el.querySelector('[data-content-editable-leaf="true"]');
      const targetEl = textLeaf || el;
      const text = cleanNotionText(targetEl.textContent || "");
      if (!text || text.length < 3) {
        continue;
      }
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) {
        continue;
      }
      seenTexts.add(textKey);
      result.push({
        text,
        element: targetEl,
        canHighlight: true
      });
    }
    if (result.length === 0) {
      console.log("[notion] 尝试备用提取方法...");
      for (const selector of DOC_BLOCK_SELECTORS) {
        const elements = content.querySelectorAll(selector);
        for (const el of Array.from(elements)) {
          const htmlEl = el;
          if (shouldSkipElement$7(htmlEl)) {
            continue;
          }
          const text = cleanNotionText(htmlEl.textContent || "");
          if (!text || text.length < 3) {
            continue;
          }
          const textKey = text.substring(0, 100);
          if (seenTexts.has(textKey)) {
            continue;
          }
          seenTexts.add(textKey);
          result.push({
            text,
            element: htmlEl,
            canHighlight: true
          });
        }
      }
    }
    return result;
  }
  const notionExtractor = {
    siteName: "Notion",
    matches: ["notion.so", "notion.site", "notion.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      const selectors = isHelpPage() ? HELP_PAGE_SELECTORS : DOC_PAGE_SELECTORS;
      for (const selector of selectors) {
        const content = document.querySelector(selector);
        if (content && content.textContent) {
          return cleanNotionText(content.textContent);
        }
      }
      return null;
    },
    extractTitle() {
      var _a;
      const titleSelectors = [
        ".notion-page-block .notion-title",
        "h1:first-of-type",
        '[placeholder="Untitled"]',
        "article h1",
        "main h1"
      ];
      for (const selector of titleSelectors) {
        const el = document.querySelector(selector);
        if (el && ((_a = el.textContent) == null ? void 0 : _a.trim())) {
          return el.textContent.trim();
        }
      }
      return document.title.replace(/ \| Notion$/, "").replace(/ – Notion$/, "").trim() || null;
    },
    extractLanguage() {
      const htmlLang = document.documentElement.lang;
      if (htmlLang) {
        const lang = htmlLang.split("-")[0].toLowerCase();
        if (lang === "zh") return "zh";
        return lang;
      }
      const content = document.body.textContent || "";
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      if (chineseChars > content.length * 0.1) {
        return "zh";
      }
      return "en";
    },
    extractParagraphsWithElements() {
      console.log("[notion] 开始提取段落...");
      console.log("[notion] 当前 URL:", window.location.href);
      const result = isHelpPage() ? extractFromHelpPage() : extractFromDocPage();
      console.log("[notion] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const PUBLISHED_SELECTORS = [
    "#contents",
    ".doc-content",
    "article"
  ];
  const EDIT_MODE_SELECTORS = [
    ".kix-appview-editor",
    ".docs-texteventtarget-iframe",
    ".kix-paginateddocumentplugin",
    ".kix-page"
  ];
  const PUBLISHED_PARAGRAPH_SELECTOR = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const SKIP_SELECTORS$6 = [
    "script",
    "style",
    "noscript",
    ".kix-lineview-decorations",
    '[aria-hidden="true"]',
    ".docs-anchormarker",
    ".navigation-widget",
    ".docs-revisions-history-widget"
  ];
  function cleanGoogleDocsText(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function isPublishedMode() {
    return window.location.pathname.includes("/pub");
  }
  function isEditMode() {
    return window.location.pathname.includes("/edit");
  }
  function shouldSkipElement$6(el) {
    for (const selector of SKIP_SELECTORS$6) {
      if (el.matches(selector) || el.closest(selector)) {
        return true;
      }
    }
    return false;
  }
  function extractFromPublished() {
    console.log("[google-docs] 发布模式提取");
    const result = [];
    let content = null;
    for (const selector of PUBLISHED_SELECTORS) {
      content = document.querySelector(selector);
      if (content && content.textContent && content.textContent.trim().length > 50) {
        break;
      }
    }
    if (!content) {
      console.log("[google-docs] 未找到发布内容容器");
      return result;
    }
    console.log("[google-docs] 找到容器:", content.className || content.id);
    const seenTexts = /* @__PURE__ */ new Set();
    const elements = content.querySelectorAll(PUBLISHED_PARAGRAPH_SELECTOR);
    for (const el of Array.from(elements)) {
      const htmlEl = el;
      if (shouldSkipElement$6(htmlEl)) {
        continue;
      }
      const text = cleanGoogleDocsText(htmlEl.textContent || "");
      if (!text || text.length < 5) {
        continue;
      }
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) {
        continue;
      }
      seenTexts.add(textKey);
      result.push({
        text,
        element: htmlEl,
        canHighlight: true
      });
    }
    return result;
  }
  function extractFromEditMode() {
    console.log("[google-docs] 编辑模式提取");
    const result = [];
    let editor = null;
    for (const selector of EDIT_MODE_SELECTORS) {
      editor = document.querySelector(selector);
      if (editor) {
        break;
      }
    }
    if (!editor) {
      console.log("[google-docs] 未找到编辑器容器");
      console.log("[google-docs] 页面可用元素:", {
        kixAppview: !!document.querySelector(".kix-appview-editor"),
        kixPage: !!document.querySelector(".kix-page"),
        kixParagraph: !!document.querySelector(".kix-paragraphrenderer")
      });
      return result;
    }
    console.log("[google-docs] 找到编辑器:", editor.className);
    const seenTexts = /* @__PURE__ */ new Set();
    const paragraphs = document.querySelectorAll(".kix-paragraphrenderer");
    console.log("[google-docs] 找到段落数:", paragraphs.length);
    for (const para of Array.from(paragraphs)) {
      const htmlEl = para;
      const text = cleanGoogleDocsText(htmlEl.textContent || "");
      if (!text || text.length < 3) {
        continue;
      }
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) {
        continue;
      }
      seenTexts.add(textKey);
      result.push({
        text,
        element: htmlEl,
        canHighlight: false
        // 编辑模式下高亮可能不稳定
      });
    }
    if (result.length === 0) {
      console.log("[google-docs] 尝试从整个编辑区域提取...");
      const kixPages = document.querySelectorAll(".kix-page");
      for (const page of Array.from(kixPages)) {
        const text = cleanGoogleDocsText(page.textContent || "");
        if (text.length > 10) {
          result.push({
            text,
            element: page,
            canHighlight: false
          });
        }
      }
    }
    return result;
  }
  const googleDocsExtractor = {
    siteName: "Google Docs",
    matches: ["docs.google.com"],
    supportsHighlight() {
      return isPublishedMode();
    },
    extractText() {
      if (isPublishedMode()) {
        for (const selector of PUBLISHED_SELECTORS) {
          const content = document.querySelector(selector);
          if (content && content.textContent) {
            return cleanGoogleDocsText(content.textContent);
          }
        }
      } else {
        const editor = document.querySelector(".kix-appview-editor");
        if (editor) {
          return cleanGoogleDocsText(editor.textContent || "");
        }
      }
      return null;
    },
    extractTitle() {
      var _a;
      const titleSelectors = [
        ".docs-title-input",
        "#doc-title",
        ".docs-title-inner",
        "h1:first-of-type"
      ];
      for (const selector of titleSelectors) {
        const el = document.querySelector(selector);
        if (el && ((_a = el.textContent) == null ? void 0 : _a.trim())) {
          const title2 = el.textContent.trim();
          if (title2 !== "Google Docs" && title2.length > 0) {
            return title2;
          }
        }
      }
      let title = document.title;
      title = title.replace(/ - Google Docs$/, "");
      title = title.replace(/ - Google 文档$/, "");
      return title.trim() || null;
    },
    extractLanguage() {
      const htmlLang = document.documentElement.lang;
      if (htmlLang) {
        const lang = htmlLang.split("-")[0].toLowerCase();
        if (lang === "zh") return "zh";
        return lang;
      }
      const editor = document.querySelector(".kix-appview-editor");
      if (editor) {
        const text = editor.textContent || "";
        const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
        if (chineseChars > text.length * 0.1) {
          return "zh";
        }
      }
      return "en";
    },
    extractParagraphsWithElements() {
      console.log("[google-docs] 开始提取段落...");
      console.log("[google-docs] 当前 URL:", window.location.href);
      console.log("[google-docs] 模式:", isPublishedMode() ? "发布" : isEditMode() ? "编辑" : "预览");
      const result = isPublishedMode() ? extractFromPublished() : extractFromEditMode();
      console.log("[google-docs] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const CONVERSATION_SELECTORS$5 = [
    '[role="presentation"]',
    "main"
  ];
  const TURN_SELECTOR = 'article[data-testid^="conversation-turn-"]';
  const ASSISTANT_ROLE_SELECTOR = '[data-message-author-role="assistant"]';
  const MARKDOWN_SELECTORS$3 = [
    ".markdown",
    ".text-token-text-primary",
    ".prose",
    '[class*="markdown"]'
  ];
  const PARAGRAPH_SELECTOR$5 = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const SKIP_SELECTORS$5 = [
    "pre",
    "code",
    "button",
    '[role="button"]',
    "svg",
    ".sr-only",
    // screen-reader labels ("ChatGPT said:", "You said:")
    ".flex.items-center.justify-end",
    // action bar (copy/like/dislike)
    '[class*="code-block"]',
    "nav",
    "header",
    "footer",
    '[data-testid*="voice"]',
    // voice play buttons
    '[data-testid*="copy"]',
    // copy buttons
    ".sticky",
    // sticky headers/footers
    ".text-token-text-secondary",
    // secondary UI text
    '[class*="agent-turn-action"]'
    // action elements within turns
  ];
  function cleanText$5(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function shouldSkipElement$5(el) {
    for (const selector of SKIP_SELECTORS$5) {
      try {
        if (el.matches(selector) || el.closest(selector)) {
          return true;
        }
      } catch {
      }
    }
    return false;
  }
  function extractParagraphsFromMessage$4(messageEl, seenTexts) {
    const result = [];
    let markdownContainer = null;
    for (const sel of MARKDOWN_SELECTORS$3) {
      markdownContainer = messageEl.querySelector(sel);
      if (markdownContainer) break;
    }
    const container = markdownContainer || messageEl;
    const elements = container.querySelectorAll(PARAGRAPH_SELECTOR$5);
    let textParagraphCount = 0;
    for (const el of Array.from(elements)) {
      const htmlEl = el;
      if (shouldSkipElement$5(htmlEl)) continue;
      if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
      const hasNestedList = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
      const hasCodeBlock = !!htmlEl.querySelector("pre");
      if (hasNestedList || hasCodeBlock) {
        let ownText = "";
        for (const child of Array.from(htmlEl.childNodes)) {
          if (child.nodeType === Node.TEXT_NODE) {
            ownText += child.textContent || "";
          } else if (child.nodeType === Node.ELEMENT_NODE) {
            const childEl = child;
            const tag = childEl.tagName;
            if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
            if (childEl.querySelector("pre")) continue;
            ownText += childEl.textContent || "";
          }
        }
        const text2 = cleanText$5(ownText);
        if (text2 && text2.length >= 2) {
          const textKey2 = text2.substring(0, 100);
          if (!seenTexts.has(textKey2)) {
            seenTexts.add(textKey2);
            result.push({ text: text2, element: htmlEl, canHighlight: true });
            textParagraphCount++;
          }
        }
        continue;
      }
      const text = cleanText$5(htmlEl.textContent || "");
      if (!text || text.length < 2) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: htmlEl, canHighlight: true });
      textParagraphCount++;
    }
    const preBlocks = container.querySelectorAll("pre");
    for (const pre of Array.from(preBlocks)) {
      const codeEl = pre.querySelector("code");
      const textSource = codeEl || pre;
      const text = cleanText$5(textSource.textContent || "");
      if (!text || text.length < 10) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: pre, canHighlight: true });
    }
    if (textParagraphCount === 0) {
      for (const child of Array.from(container.children)) {
        const htmlChild = child;
        if (shouldSkipElement$5(htmlChild)) continue;
        if (htmlChild.offsetHeight === 0 && htmlChild.offsetWidth === 0) continue;
        const text = cleanText$5(htmlChild.textContent || "");
        if (!text || text.length < 10) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlChild, canHighlight: true });
      }
    }
    if (textParagraphCount === 0 && result.length <= preBlocks.length) {
      const rawText = container.innerText || "";
      const lines = rawText.split(/\n\n+/).map((l) => l.trim()).filter((l) => l.length >= 10);
      if (lines.length >= 2) {
        for (const line of lines) {
          const text = cleanText$5(line);
          if (!text || text.length < 10) continue;
          const textKey = text.substring(0, 100);
          if (seenTexts.has(textKey)) continue;
          seenTexts.add(textKey);
          result.push({ text, element: container, canHighlight: true });
        }
      } else if (result.length <= preBlocks.length) {
        const text = cleanText$5(rawText);
        if (text && text.length >= 10) {
          const textKey = text.substring(0, 100);
          if (!seenTexts.has(textKey)) {
            seenTexts.add(textKey);
            result.push({ text, element: container, canHighlight: true });
          }
        }
      }
    }
    return result;
  }
  const chatgptExtractor = {
    siteName: "ChatGPT",
    matches: ["chatgpt.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      var _a;
      const paragraphs = ((_a = this.extractParagraphsWithElements) == null ? void 0 : _a.call(this)) || [];
      if (paragraphs.length === 0) return null;
      return paragraphs.map((p) => p.text).join("\n\n");
    },
    extractTitle() {
      return document.title.replace(/\s*[-–—|]\s*ChatGPT\s*$/, "").trim() || "ChatGPT";
    },
    extractLanguage() {
      const assistantEls = document.querySelectorAll(ASSISTANT_ROLE_SELECTOR);
      let content = "";
      for (const el of Array.from(assistantEls)) {
        content += el.textContent || "";
        if (content.length > 2e3) break;
      }
      if (!content) content = document.body.textContent || "";
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      return chineseChars > content.length * 0.1 ? "zh" : "en";
    },
    extractParagraphsWithElements() {
      console.log("[chatgpt] 开始提取 AI 回复...");
      const result = [];
      const seenTexts = /* @__PURE__ */ new Set();
      const turns = document.querySelectorAll(TURN_SELECTOR);
      if (turns.length > 0) {
        console.log("[chatgpt] 找到对话轮次:", turns.length);
        for (const turn of Array.from(turns)) {
          const assistantMarker = turn.querySelector(ASSISTANT_ROLE_SELECTOR);
          if (!assistantMarker) continue;
          const paragraphs = extractParagraphsFromMessage$4(
            turn,
            seenTexts
          );
          result.push(...paragraphs);
        }
        if (result.length > 0) {
          console.log("[chatgpt] 提取完成，段落数:", result.length);
          return result;
        }
      }
      console.log("[chatgpt] data-testid 方法未找到内容，尝试 fallback...");
      let conversation = null;
      for (const sel of CONVERSATION_SELECTORS$5) {
        conversation = document.querySelector(sel);
        if (conversation && conversation.textContent && conversation.textContent.trim().length > 100) {
          break;
        }
      }
      if (!conversation) {
        console.log("[chatgpt] 未找到对话容器");
        return result;
      }
      for (const sel of MARKDOWN_SELECTORS$3) {
        const blocks = conversation.querySelectorAll(sel);
        for (const block of Array.from(blocks)) {
          const paragraphs = extractParagraphsFromMessage$4(
            block,
            seenTexts
          );
          result.push(...paragraphs);
        }
        if (result.length > 0) break;
      }
      console.log("[chatgpt] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const USER_MESSAGE_SELECTORS$2 = [
    '[data-testid="user-message"]',
    '[data-testid="user-human-turn"]',
    ".font-user-message",
    '[class*="human-turn"]',
    '[class*="user-turn"]'
  ];
  const AI_MESSAGE_SELECTORS$2 = [
    '[data-testid="ai-message"]',
    '[data-testid="assistant-turn"]',
    '[data-testid="bot-message"]',
    // Share page uses different attributes
    '[data-role="assistant"]',
    "[data-is-streaming]"
  ];
  const MARKDOWN_SELECTORS$2 = [
    ".font-claude-message",
    ".grid-cols-1.grid > .contents",
    ".prose",
    ".markdown",
    '[class*="markdown"]'
  ];
  const CONVERSATION_SELECTORS$4 = [
    '[data-testid="conversation-content"]',
    ".conversation-content",
    '[role="presentation"]',
    '[role="main"]',
    "main"
  ];
  const PARAGRAPH_SELECTOR$4 = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const SKIP_SELECTORS$4 = [
    "pre",
    "code",
    '[data-testid="thinking-block"]',
    '[data-testid="thinking-content"]',
    '[class*="thinking"]',
    '[class*="artifact"]',
    '[data-testid="artifact"]',
    ".sr-only",
    "button",
    '[role="button"]',
    "svg",
    "nav",
    "header",
    "footer",
    '[aria-hidden="true"]'
  ];
  function cleanText$4(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function shouldSkipElement$4(el) {
    for (const selector of SKIP_SELECTORS$4) {
      try {
        if (el.matches(selector) || el.closest(selector)) {
          return true;
        }
      } catch {
      }
    }
    return false;
  }
  function isUserMessage$2(el) {
    for (const sel of USER_MESSAGE_SELECTORS$2) {
      try {
        if (el.matches(sel) || el.closest(sel)) return true;
      } catch {
      }
    }
    return false;
  }
  function extractParagraphsFromMessage$3(messageEl, seenTexts) {
    const result = [];
    const elements = messageEl.querySelectorAll(PARAGRAPH_SELECTOR$4);
    let textParagraphCount = 0;
    for (const el of Array.from(elements)) {
      const htmlEl = el;
      if (shouldSkipElement$4(htmlEl)) continue;
      if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
      const hasNestedList = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
      const hasCodeBlock = !!htmlEl.querySelector("pre");
      if (hasNestedList || hasCodeBlock) {
        let ownText = "";
        for (const child of Array.from(htmlEl.childNodes)) {
          if (child.nodeType === Node.TEXT_NODE) {
            ownText += child.textContent || "";
          } else if (child.nodeType === Node.ELEMENT_NODE) {
            const childEl = child;
            const tag = childEl.tagName;
            if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
            if (childEl.querySelector("pre")) continue;
            ownText += childEl.textContent || "";
          }
        }
        const text2 = cleanText$4(ownText);
        if (text2 && text2.length >= 2) {
          const textKey2 = text2.substring(0, 100);
          if (!seenTexts.has(textKey2)) {
            seenTexts.add(textKey2);
            result.push({ text: text2, element: htmlEl, canHighlight: true });
            textParagraphCount++;
          }
        }
        continue;
      }
      const text = cleanText$4(htmlEl.textContent || "");
      if (!text || text.length < 2) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: htmlEl, canHighlight: true });
      textParagraphCount++;
    }
    const preBlocks = messageEl.querySelectorAll("pre");
    for (const pre of Array.from(preBlocks)) {
      const codeEl = pre.querySelector("code");
      const text = cleanText$4((codeEl || pre).textContent || "");
      if (!text || text.length < 10) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: pre, canHighlight: true });
    }
    if (textParagraphCount === 0) {
      for (const child of Array.from(messageEl.children)) {
        const htmlChild = child;
        if (shouldSkipElement$4(htmlChild)) continue;
        if (htmlChild.offsetHeight === 0 && htmlChild.offsetWidth === 0) continue;
        const text = cleanText$4(htmlChild.textContent || "");
        if (!text || text.length < 10) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlChild, canHighlight: true });
      }
    }
    if (textParagraphCount === 0 && result.length <= preBlocks.length) {
      const text = cleanText$4(messageEl.textContent || "");
      if (text && text.length >= 10) {
        const textKey = text.substring(0, 100);
        if (!seenTexts.has(textKey)) {
          seenTexts.add(textKey);
          result.push({ text, element: messageEl, canHighlight: true });
        }
      }
    }
    return result;
  }
  const claudeAiExtractor = {
    siteName: "Claude",
    matches: ["claude.ai"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      var _a;
      const paragraphs = ((_a = this.extractParagraphsWithElements) == null ? void 0 : _a.call(this)) || [];
      if (paragraphs.length === 0) return null;
      return paragraphs.map((p) => p.text).join("\n\n");
    },
    extractTitle() {
      var _a;
      const titleEl = document.querySelector(
        '[data-testid="chat-title-button"] .truncate, [data-testid="chat-title-button"]'
      );
      if ((_a = titleEl == null ? void 0 : titleEl.textContent) == null ? void 0 : _a.trim()) {
        return titleEl.textContent.trim();
      }
      return document.title.replace(/\s*[-–—|]\s*Claude\s*$/, "").trim() || "Claude";
    },
    extractLanguage() {
      let content = "";
      for (const sel of AI_MESSAGE_SELECTORS$2) {
        const els = document.querySelectorAll(sel);
        for (const el of Array.from(els)) {
          content += el.textContent || "";
          if (content.length > 2e3) break;
        }
        if (content.length > 500) break;
      }
      if (!content || content.length < 100) {
        for (const sel of MARKDOWN_SELECTORS$2) {
          const els = document.querySelectorAll(sel);
          for (const el of Array.from(els)) {
            if (isUserMessage$2(el)) continue;
            content += el.textContent || "";
            if (content.length > 2e3) break;
          }
          if (content.length > 500) break;
        }
      }
      if (!content) content = document.body.textContent || "";
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      return chineseChars > content.length * 0.1 ? "zh" : "en";
    },
    extractParagraphsWithElements() {
      console.log("[claude-ai] 开始提取 AI 回复...");
      const result = [];
      const seenTexts = /* @__PURE__ */ new Set();
      for (const sel of AI_MESSAGE_SELECTORS$2) {
        const aiMessages = document.querySelectorAll(sel);
        if (aiMessages.length > 0) {
          console.log("[claude-ai] 找到 AI 消息:", aiMessages.length, "(selector:", sel, ")");
          for (const msg of Array.from(aiMessages)) {
            const paragraphs = extractParagraphsFromMessage$3(
              msg,
              seenTexts
            );
            result.push(...paragraphs);
          }
          if (result.length > 0) {
            console.log("[claude-ai] 提取完成，段落数:", result.length);
            return result;
          }
        }
      }
      console.log("[claude-ai] data-testid 方法未找到内容，尝试 markdown 容器...");
      for (const sel of MARKDOWN_SELECTORS$2) {
        const mdBlocks = document.querySelectorAll(sel);
        if (mdBlocks.length > 0) {
          console.log("[claude-ai] 找到 markdown 块:", mdBlocks.length, "(selector:", sel, ")");
          for (const block of Array.from(mdBlocks)) {
            const htmlBlock = block;
            if (isUserMessage$2(htmlBlock)) continue;
            const paragraphs = extractParagraphsFromMessage$3(htmlBlock, seenTexts);
            result.push(...paragraphs);
          }
          if (result.length > 0) {
            console.log("[claude-ai] 提取完成，段落数:", result.length);
            return result;
          }
        }
      }
      console.log("[claude-ai] markdown 方法未找到内容，尝试 fallback...");
      let conversation = null;
      for (const sel of CONVERSATION_SELECTORS$4) {
        conversation = document.querySelector(sel);
        if (conversation && conversation.textContent && conversation.textContent.trim().length > 100) {
          break;
        }
      }
      if (!conversation) {
        console.log("[claude-ai] 未找到对话容器");
        return result;
      }
      const elements = conversation.querySelectorAll(PARAGRAPH_SELECTOR$4);
      for (const el of Array.from(elements)) {
        const htmlEl = el;
        if (shouldSkipElement$4(htmlEl)) continue;
        if (isUserMessage$2(htmlEl)) continue;
        if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
        const hasNestedList2 = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
        const hasCodeBlock2 = !!htmlEl.querySelector("pre");
        if (hasNestedList2 || hasCodeBlock2) {
          let ownText = "";
          for (const child of Array.from(htmlEl.childNodes)) {
            if (child.nodeType === Node.TEXT_NODE) {
              ownText += child.textContent || "";
            } else if (child.nodeType === Node.ELEMENT_NODE) {
              const childEl = child;
              const tag = childEl.tagName;
              if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
              if (childEl.querySelector("pre")) continue;
              ownText += childEl.textContent || "";
            }
          }
          const text2 = cleanText$4(ownText);
          if (text2 && text2.length >= 2) {
            const textKey2 = text2.substring(0, 100);
            if (!seenTexts.has(textKey2)) {
              seenTexts.add(textKey2);
              result.push({ text: text2, element: htmlEl, canHighlight: true });
            }
          }
          continue;
        }
        const text = cleanText$4(htmlEl.textContent || "");
        if (!text || text.length < 2) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
      const preBlocks = conversation.querySelectorAll("pre");
      for (const pre of Array.from(preBlocks)) {
        const htmlPre = pre;
        if (isUserMessage$2(htmlPre)) continue;
        const text = cleanText$4(htmlPre.textContent || "");
        if (!text || text.length < 10) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlPre, canHighlight: true });
      }
      console.log("[claude-ai] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const MODEL_RESPONSE_SELECTORS = [
    "model-response",
    "message-content.model-response",
    '[data-message-author="model"]',
    ".model-response-text",
    '[data-content-type="response"]'
  ];
  const MARKDOWN_SELECTORS$1 = [
    ".markdown-main-panel",
    ".markdown",
    ".prose",
    '[class*="markdown"]'
  ];
  const USER_MESSAGE_SELECTORS$1 = [
    "user-query",
    "message-content.user-query",
    '[data-message-author="user"]',
    ".user-message"
  ];
  const CONVERSATION_SELECTORS$3 = [
    ".conversation-container",
    '[role="main"]',
    "main"
  ];
  const PARAGRAPH_SELECTOR$3 = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const SKIP_SELECTORS$3 = [
    "pre",
    "code",
    "code-block",
    '[class*="code-block"]',
    "math-renderer",
    '[class*="citation"]',
    "button",
    '[role="button"]',
    "svg",
    "nav",
    "header",
    "footer",
    '[aria-hidden="true"]'
  ];
  function cleanText$3(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function shouldSkipElement$3(el) {
    for (const selector of SKIP_SELECTORS$3) {
      try {
        if (el.matches(selector) || el.closest(selector)) {
          return true;
        }
      } catch {
      }
    }
    return false;
  }
  function extractParagraphsFromMessage$2(messageEl, seenTexts, useShadow) {
    const result = [];
    const elements = useShadow ? deepQuerySelectorAll(messageEl, PARAGRAPH_SELECTOR$3) : Array.from(messageEl.querySelectorAll(PARAGRAPH_SELECTOR$3));
    for (const el of elements) {
      const htmlEl = el;
      if (shouldSkipElement$3(htmlEl)) continue;
      if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
      const hasNestedList = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
      const hasCodeBlock = !!htmlEl.querySelector("pre");
      if (hasNestedList || hasCodeBlock) {
        let ownText = "";
        for (const child of Array.from(htmlEl.childNodes)) {
          if (child.nodeType === Node.TEXT_NODE) {
            ownText += child.textContent || "";
          } else if (child.nodeType === Node.ELEMENT_NODE) {
            const childEl = child;
            const tag = childEl.tagName;
            if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
            if (childEl.querySelector("pre")) continue;
            ownText += childEl.textContent || "";
          }
        }
        const text2 = cleanText$3(ownText);
        if (text2 && text2.length >= 2) {
          const textKey2 = text2.substring(0, 100);
          if (!seenTexts.has(textKey2)) {
            seenTexts.add(textKey2);
            result.push({ text: text2, element: htmlEl, canHighlight: true });
          }
        }
        continue;
      }
      const text = cleanText$3(htmlEl.textContent || "");
      if (!text || text.length < 2) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: htmlEl, canHighlight: true });
    }
    const preBlocks = useShadow ? deepQuerySelectorAll(messageEl, "pre") : Array.from(messageEl.querySelectorAll("pre"));
    for (const pre of preBlocks) {
      const codeEl = pre.querySelector("code");
      const text = cleanText$3((codeEl || pre).textContent || "");
      if (!text || text.length < 10) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: pre, canHighlight: true });
    }
    if (result.length === 0) {
      const text = cleanText$3(messageEl.textContent || "");
      if (text && text.length >= 10) {
        const textKey = text.substring(0, 100);
        if (!seenTexts.has(textKey)) {
          seenTexts.add(textKey);
          result.push({ text, element: messageEl, canHighlight: true });
        }
      }
    }
    return result;
  }
  function isUserMessage$1(el) {
    for (const sel of USER_MESSAGE_SELECTORS$1) {
      try {
        if (el.matches(sel) || el.closest(sel)) return true;
      } catch {
      }
    }
    return false;
  }
  const geminiExtractor = {
    siteName: "Gemini",
    matches: ["gemini.google.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      var _a;
      const paragraphs = ((_a = this.extractParagraphsWithElements) == null ? void 0 : _a.call(this)) || [];
      if (paragraphs.length === 0) return null;
      return paragraphs.map((p) => p.text).join("\n\n");
    },
    extractTitle() {
      return document.title.replace(/\s*[-–—|]\s*Google Gemini\s*$/i, "").replace(/\s*[-–—|]\s*Gemini\s*$/i, "").trim() || "Gemini";
    },
    extractLanguage() {
      const useShadow = hasShadowContent();
      let content = "";
      for (const sel of MODEL_RESPONSE_SELECTORS) {
        const els = useShadow ? deepQuerySelectorAll(document, sel) : Array.from(document.querySelectorAll(sel));
        for (const el of els) {
          content += el.textContent || "";
          if (content.length > 2e3) break;
        }
        if (content.length > 500) break;
      }
      if (!content || content.length < 100) {
        for (const sel of MARKDOWN_SELECTORS$1) {
          const els = useShadow ? deepQuerySelectorAll(document, sel) : Array.from(document.querySelectorAll(sel));
          for (const el of els) {
            if (isUserMessage$1(el)) continue;
            content += el.textContent || "";
            if (content.length > 2e3) break;
          }
          if (content.length > 500) break;
        }
      }
      if (!content) content = document.body.textContent || "";
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      if (chineseChars > content.length * 0.1) return "zh";
      const htmlLang = document.documentElement.lang;
      if (htmlLang) {
        return htmlLang.split("-")[0].toLowerCase();
      }
      return "en";
    },
    extractParagraphsWithElements() {
      console.log("[gemini] 开始提取模型回复...");
      const useShadow = hasShadowContent();
      if (useShadow) {
        console.log("[gemini] 检测到 Shadow DOM，使用深度查询");
      }
      const result = [];
      const seenTexts = /* @__PURE__ */ new Set();
      for (const sel of MODEL_RESPONSE_SELECTORS) {
        const responses = useShadow ? deepQuerySelectorAll(document, sel) : Array.from(document.querySelectorAll(sel));
        if (responses.length > 0) {
          console.log("[gemini] 找到模型回复:", responses.length, "(selector:", sel, ")");
          for (const resp of responses) {
            const paragraphs = extractParagraphsFromMessage$2(
              resp,
              seenTexts,
              useShadow
            );
            result.push(...paragraphs);
          }
          if (result.length > 0) {
            console.log("[gemini] 提取完成，段落数:", result.length);
            return result;
          }
        }
      }
      console.log("[gemini] 模型回复选择器未找到内容，尝试 markdown 容器...");
      for (const sel of MARKDOWN_SELECTORS$1) {
        const mdBlocks = useShadow ? deepQuerySelectorAll(document, sel) : Array.from(document.querySelectorAll(sel));
        if (mdBlocks.length > 0) {
          console.log("[gemini] 找到 markdown 块:", mdBlocks.length, "(selector:", sel, ")");
          for (const block of mdBlocks) {
            const htmlBlock = block;
            if (isUserMessage$1(htmlBlock)) continue;
            const paragraphs = extractParagraphsFromMessage$2(htmlBlock, seenTexts, useShadow);
            result.push(...paragraphs);
          }
          if (result.length > 0) {
            console.log("[gemini] 提取完成，段落数:", result.length);
            return result;
          }
        }
      }
      console.log("[gemini] markdown 方法未找到内容，尝试 fallback...");
      let conversation = null;
      for (const sel of CONVERSATION_SELECTORS$3) {
        const found = useShadow ? deepQuerySelectorAll(document, sel) : Array.from(document.querySelectorAll(sel));
        if (found.length > 0) {
          const el = found[0];
          if (el.textContent && el.textContent.trim().length > 100) {
            conversation = el;
            break;
          }
        }
      }
      if (!conversation) {
        console.log("[gemini] 未找到对话容器");
        return result;
      }
      const elements = useShadow ? deepQuerySelectorAll(conversation, PARAGRAPH_SELECTOR$3) : Array.from(conversation.querySelectorAll(PARAGRAPH_SELECTOR$3));
      for (const el of elements) {
        const htmlEl = el;
        if (shouldSkipElement$3(htmlEl)) continue;
        if (isUserMessage$1(htmlEl)) continue;
        if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
        const hasNestedList2 = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
        const hasCodeBlock2 = !!htmlEl.querySelector("pre");
        if (hasNestedList2 || hasCodeBlock2) {
          let ownText = "";
          for (const child of Array.from(htmlEl.childNodes)) {
            if (child.nodeType === Node.TEXT_NODE) {
              ownText += child.textContent || "";
            } else if (child.nodeType === Node.ELEMENT_NODE) {
              const childEl = child;
              const tag = childEl.tagName;
              if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
              if (childEl.querySelector("pre")) continue;
              ownText += childEl.textContent || "";
            }
          }
          const text2 = cleanText$3(ownText);
          if (text2 && text2.length >= 2) {
            const textKey2 = text2.substring(0, 100);
            if (!seenTexts.has(textKey2)) {
              seenTexts.add(textKey2);
              result.push({ text: text2, element: htmlEl, canHighlight: true });
            }
          }
          continue;
        }
        const text = cleanText$3(htmlEl.textContent || "");
        if (!text || text.length < 2) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
      const preBlocks = useShadow ? deepQuerySelectorAll(conversation, "pre") : Array.from(conversation.querySelectorAll("pre"));
      for (const pre of preBlocks) {
        const htmlPre = pre;
        if (isUserMessage$1(htmlPre)) continue;
        const text = cleanText$3(htmlPre.textContent || "");
        if (!text || text.length < 10) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlPre, canHighlight: true });
      }
      console.log("[gemini] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const AI_MESSAGE_SELECTORS$1 = [
    '[data-testid="receive_message"]',
    '[data-testid="bot_message"]'
  ];
  const MESSAGE_CONTENT_SELECTOR = '[data-testid="message_text_content"]';
  const CONVERSATION_SELECTORS$2 = [
    '[data-testid="chat_container"]',
    '[role="main"]',
    "main"
  ];
  const PARAGRAPH_SELECTOR$2 = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const SKIP_SELECTORS$2 = [
    "pre",
    "code",
    "button",
    '[role="button"]',
    '[data-testid="message_action_copy"]',
    '[data-testid="message_action_dislike"]',
    "svg",
    "nav",
    "header",
    "footer",
    '[aria-hidden="true"]'
  ];
  function cleanText$2(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function shouldSkipElement$2(el) {
    for (const selector of SKIP_SELECTORS$2) {
      try {
        if (el.matches(selector) || el.closest(selector)) return true;
      } catch {
      }
    }
    return false;
  }
  function extractParagraphsFromMessage$1(messageEl, seenTexts) {
    const result = [];
    const contentEl = messageEl.querySelector(MESSAGE_CONTENT_SELECTOR) || messageEl;
    const elements = contentEl.querySelectorAll(PARAGRAPH_SELECTOR$2);
    for (const el of Array.from(elements)) {
      const htmlEl = el;
      if (shouldSkipElement$2(htmlEl)) continue;
      if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
      const text = cleanText$2(htmlEl.textContent || "");
      if (!text || text.length < 10) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: htmlEl, canHighlight: true });
    }
    if (result.length === 0) {
      const text = cleanText$2(contentEl.textContent || "");
      if (text && text.length >= 10) {
        const textKey = text.substring(0, 100);
        if (!seenTexts.has(textKey)) {
          seenTexts.add(textKey);
          result.push({ text, element: contentEl, canHighlight: true });
        }
      }
    }
    return result;
  }
  const doubaoExtractor = {
    siteName: "豆包",
    matches: ["www.doubao.com", "doubao.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      var _a;
      const paragraphs = ((_a = this.extractParagraphsWithElements) == null ? void 0 : _a.call(this)) || [];
      if (paragraphs.length === 0) return null;
      return paragraphs.map((p) => p.text).join("\n\n");
    },
    extractTitle() {
      return document.title.replace(/\s*[-–—|]\s*豆包\s*$/, "").trim() || "豆包";
    },
    extractLanguage() {
      const content = document.body.textContent || "";
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      return chineseChars > content.length * 0.1 ? "zh" : "en";
    },
    extractParagraphsWithElements() {
      console.log("[doubao] 开始提取 AI 回复...");
      const result = [];
      const seenTexts = /* @__PURE__ */ new Set();
      for (const sel of AI_MESSAGE_SELECTORS$1) {
        const aiMessages = document.querySelectorAll(sel);
        if (aiMessages.length > 0) {
          console.log("[doubao] 找到 AI 消息:", aiMessages.length, "(selector:", sel, ")");
          for (const msg of Array.from(aiMessages)) {
            const paragraphs = extractParagraphsFromMessage$1(msg, seenTexts);
            result.push(...paragraphs);
          }
          if (result.length > 0) {
            console.log("[doubao] 提取完成，段落数:", result.length);
            return result;
          }
        }
      }
      console.log("[doubao] data-testid 方法未找到内容，尝试 fallback...");
      const contentBlocks = document.querySelectorAll(MESSAGE_CONTENT_SELECTOR);
      if (contentBlocks.length > 0) {
        console.log("[doubao] 找到内容块:", contentBlocks.length);
        for (const block of Array.from(contentBlocks)) {
          const paragraphs = extractParagraphsFromMessage$1(block, seenTexts);
          result.push(...paragraphs);
        }
        if (result.length > 0) {
          console.log("[doubao] 提取完成，段落数:", result.length);
          return result;
        }
      }
      let conversation = null;
      for (const sel of CONVERSATION_SELECTORS$2) {
        conversation = document.querySelector(sel);
        if (conversation && conversation.textContent && conversation.textContent.trim().length > 100) break;
      }
      if (conversation) {
        const elements = conversation.querySelectorAll(PARAGRAPH_SELECTOR$2);
        for (const el of Array.from(elements)) {
          const htmlEl = el;
          if (shouldSkipElement$2(htmlEl)) continue;
          if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
          const text = cleanText$2(htmlEl.textContent || "");
          if (!text || text.length < 10) continue;
          const textKey = text.substring(0, 100);
          if (seenTexts.has(textKey)) continue;
          seenTexts.add(textKey);
          result.push({ text, element: htmlEl, canHighlight: true });
        }
      }
      console.log("[doubao] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const MARKDOWN_CONTENT_SELECTORS = [
    ".ds-markdown.ds-markdown--block",
    ".ds-markdown",
    ".markdown",
    '[class*="markdown"]'
  ];
  const THINKING_SKIP_SELECTORS = [
    ".e1675d8b",
    // 已知思考链类名（可能变化）
    '[class*="thinking"]',
    '[class*="thought"]',
    '[data-testid="thinking"]'
  ];
  const CONVERSATION_SELECTORS$1 = [
    '[role="main"]',
    "main",
    "#root"
  ];
  const PARAGRAPH_SELECTOR$1 = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const SKIP_SELECTORS$1 = [
    "pre",
    "code",
    ".ds-icon-button",
    "button",
    '[role="button"]',
    "svg",
    "nav",
    "header",
    "footer",
    '[aria-hidden="true"]'
  ];
  const THINKING_INDICATOR_RE = /^Thought for \d+ seconds?$/i;
  const THINKING_INDICATOR_ZH_RE = /^(已深度思考|思考了\s*\d+\s*秒|深度思考中)/;
  function cleanText$1(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function isThinkingIndicator(text) {
    return THINKING_INDICATOR_RE.test(text) || THINKING_INDICATOR_ZH_RE.test(text);
  }
  function shouldSkipElement$1(el) {
    for (const selector of SKIP_SELECTORS$1) {
      try {
        if (el.matches(selector) || el.closest(selector)) return true;
      } catch {
      }
    }
    for (const sel of THINKING_SKIP_SELECTORS) {
      try {
        if (el.closest(sel)) return true;
      } catch {
      }
    }
    return false;
  }
  function isThinkingBlock(el) {
    var _a, _b, _c, _d;
    for (const sel of THINKING_SKIP_SELECTORS) {
      try {
        if (el.matches(sel) || el.closest(sel)) return true;
      } catch {
      }
    }
    let parent = el.parentElement;
    for (let i = 0; i < 3 && parent; i++) {
      const cls = parent.className || "";
      if (typeof cls === "string" && /\bthink(ing|_chain|_process|-block|-container)\b/i.test(cls)) return true;
      if ((_b = (_a = parent.previousElementSibling) == null ? void 0 : _a.textContent) == null ? void 0 : _b.match(THINKING_INDICATOR_RE)) return true;
      if ((_d = (_c = parent.previousElementSibling) == null ? void 0 : _c.textContent) == null ? void 0 : _d.match(THINKING_INDICATOR_ZH_RE)) return true;
      parent = parent.parentElement;
    }
    return false;
  }
  function extractParagraphsFromMarkdown(markdownEl, seenTexts) {
    const result = [];
    const elements = markdownEl.querySelectorAll(PARAGRAPH_SELECTOR$1);
    for (const el of Array.from(elements)) {
      const htmlEl = el;
      if (shouldSkipElement$1(htmlEl)) continue;
      if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
      const hasNestedList = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
      const hasCodeBlock = !!htmlEl.querySelector("pre");
      if (hasNestedList || hasCodeBlock) {
        let ownText = "";
        for (const child of Array.from(htmlEl.childNodes)) {
          if (child.nodeType === Node.TEXT_NODE) {
            ownText += child.textContent || "";
          } else if (child.nodeType === Node.ELEMENT_NODE) {
            const childEl = child;
            const tag = childEl.tagName;
            if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
            if (childEl.querySelector("pre")) continue;
            ownText += childEl.textContent || "";
          }
        }
        const text2 = cleanText$1(ownText);
        if (text2 && text2.length >= 2 && !isThinkingIndicator(text2)) {
          const textKey2 = text2.substring(0, 100);
          if (!seenTexts.has(textKey2)) {
            seenTexts.add(textKey2);
            result.push({ text: text2, element: htmlEl, canHighlight: true });
          }
        }
        continue;
      }
      const text = cleanText$1(htmlEl.textContent || "");
      if (!text || text.length < 2) continue;
      if (isThinkingIndicator(text)) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: htmlEl, canHighlight: true });
    }
    const preBlocks = markdownEl.querySelectorAll("pre");
    for (const pre of Array.from(preBlocks)) {
      const codeEl = pre.querySelector("code");
      const text = cleanText$1((codeEl || pre).textContent || "");
      if (!text || text.length < 10) continue;
      if (isThinkingIndicator(text)) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: pre, canHighlight: true });
    }
    if (result.length === 0) {
      const text = cleanText$1(markdownEl.textContent || "");
      if (text && text.length >= 10 && !isThinkingIndicator(text)) {
        const textKey = text.substring(0, 100);
        if (!seenTexts.has(textKey)) {
          seenTexts.add(textKey);
          result.push({ text, element: markdownEl, canHighlight: true });
        }
      }
    }
    return result;
  }
  const deepseekExtractor = {
    siteName: "DeepSeek",
    matches: ["chat.deepseek.com", "deepseek.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      var _a;
      const paragraphs = ((_a = this.extractParagraphsWithElements) == null ? void 0 : _a.call(this)) || [];
      if (paragraphs.length === 0) return null;
      return paragraphs.map((p) => p.text).join("\n\n");
    },
    extractTitle() {
      return document.title.replace(/\s*[-–—|]\s*DeepSeek\s*$/i, "").trim() || "DeepSeek";
    },
    extractLanguage() {
      let content = "";
      for (const sel of MARKDOWN_CONTENT_SELECTORS) {
        const blocks = document.querySelectorAll(sel);
        for (const el of Array.from(blocks)) {
          if (isThinkingBlock(el)) continue;
          content += el.textContent || "";
          if (content.length > 2e3) break;
        }
        if (content.length > 500) break;
      }
      if (!content) content = document.body.textContent || "";
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      return chineseChars > content.length * 0.1 ? "zh" : "en";
    },
    extractParagraphsWithElements() {
      console.log("[deepseek] 开始提取 AI 回复...");
      const result = [];
      const seenTexts = /* @__PURE__ */ new Set();
      let markdownBlocks = null;
      for (const sel of MARKDOWN_CONTENT_SELECTORS) {
        const blocks = document.querySelectorAll(sel);
        if (blocks.length > 0) {
          markdownBlocks = blocks;
          console.log("[deepseek] 找到 Markdown 块:", blocks.length, "(selector:", sel, ")");
          break;
        }
      }
      if (markdownBlocks && markdownBlocks.length > 0) {
        for (const block of Array.from(markdownBlocks)) {
          const htmlBlock = block;
          if (isThinkingBlock(htmlBlock)) {
            console.log("[deepseek] 跳过思考链块");
            continue;
          }
          const paragraphs = extractParagraphsFromMarkdown(htmlBlock, seenTexts);
          result.push(...paragraphs);
        }
        if (result.length > 0) {
          console.log("[deepseek] 提取完成，段落数:", result.length);
          return result;
        }
      }
      console.log("[deepseek] .ds-markdown 方法未找到内容，尝试 fallback...");
      let conversation = null;
      for (const sel of CONVERSATION_SELECTORS$1) {
        conversation = document.querySelector(sel);
        if (conversation && conversation.textContent && conversation.textContent.trim().length > 100) break;
      }
      if (!conversation) {
        console.log("[deepseek] 未找到对话容器");
        return result;
      }
      const elements = conversation.querySelectorAll(PARAGRAPH_SELECTOR$1);
      for (const el of Array.from(elements)) {
        const htmlEl = el;
        if (shouldSkipElement$1(htmlEl)) continue;
        if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
        const hasNestedList2 = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
        const hasCodeBlock2 = !!htmlEl.querySelector("pre");
        if (hasNestedList2 || hasCodeBlock2) {
          let ownText = "";
          for (const child of Array.from(htmlEl.childNodes)) {
            if (child.nodeType === Node.TEXT_NODE) {
              ownText += child.textContent || "";
            } else if (child.nodeType === Node.ELEMENT_NODE) {
              const childEl = child;
              const tag = childEl.tagName;
              if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
              if (childEl.querySelector("pre")) continue;
              ownText += childEl.textContent || "";
            }
          }
          const text2 = cleanText$1(ownText);
          if (text2 && text2.length >= 2 && !isThinkingIndicator(text2)) {
            const textKey2 = text2.substring(0, 100);
            if (!seenTexts.has(textKey2)) {
              seenTexts.add(textKey2);
              result.push({ text: text2, element: htmlEl, canHighlight: true });
            }
          }
          continue;
        }
        const text = cleanText$1(htmlEl.textContent || "");
        if (!text || text.length < 2) continue;
        if (isThinkingIndicator(text)) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
      console.log("[deepseek] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const AI_MESSAGE_SELECTORS = [
    // data 属性（如果存在）
    '[data-testid="assistant-message"]',
    '[data-testid="bot-message"]',
    '[data-role="assistant"]',
    '[data-message-role="assistant"]',
    // 语义化 class
    ".assistant-message",
    ".bot-message"
  ];
  const USER_MESSAGE_SELECTORS = [
    '[data-testid="user-message"]',
    '[data-role="user"]',
    '[data-message-role="user"]',
    ".user-message",
    ".human-message"
  ];
  const MARKDOWN_SELECTORS = [
    ".markdown",
    ".markdown-body",
    '[class*="markdown"]',
    ".prose"
  ];
  const CONVERSATION_SELECTORS = [
    '[data-testid="chat-container"]',
    '[role="main"]',
    "main",
    "#root",
    "#app"
  ];
  const PARAGRAPH_SELECTOR = "p, h1, h2, h3, h4, h5, h6, li, blockquote";
  const SHARE_PAGE_PARAGRAPH_SELECTOR = "p, h1, h2, h3, h4, h5, h6, li, blockquote, table, dt, dd";
  const SKIP_SELECTORS = [
    "pre",
    "code",
    "button",
    '[role="button"]',
    "svg",
    "nav",
    "header",
    "footer",
    '[aria-hidden="true"]',
    "img",
    "video",
    "audio"
  ];
  function cleanText(text) {
    return text.replace(/[\u200B-\u200D\uFEFF]/g, "").replace(/\s+/g, " ").trim();
  }
  function shouldSkipElement(el) {
    for (const selector of SKIP_SELECTORS) {
      try {
        if (el.matches(selector) || el.closest(selector)) return true;
      } catch {
      }
    }
    return false;
  }
  function isUserMessage(el) {
    for (const sel of USER_MESSAGE_SELECTORS) {
      try {
        if (el.matches(sel) || el.closest(sel)) return true;
      } catch {
      }
    }
    return false;
  }
  function extractParagraphsFromMessage(messageEl, seenTexts) {
    const result = [];
    let container = messageEl;
    for (const sel of MARKDOWN_SELECTORS) {
      const md = messageEl.querySelector(sel);
      if (md) {
        container = md;
        break;
      }
    }
    const elements = container.querySelectorAll(PARAGRAPH_SELECTOR);
    for (const el of Array.from(elements)) {
      const htmlEl = el;
      if (shouldSkipElement(htmlEl)) continue;
      if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
      const hasNestedList = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
      const hasCodeBlock = !!htmlEl.querySelector("pre");
      if (hasNestedList || hasCodeBlock) {
        let ownText = "";
        for (const child of Array.from(htmlEl.childNodes)) {
          if (child.nodeType === Node.TEXT_NODE) {
            ownText += child.textContent || "";
          } else if (child.nodeType === Node.ELEMENT_NODE) {
            const childEl = child;
            const tag = childEl.tagName;
            if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
            if (childEl.querySelector("pre")) continue;
            ownText += childEl.textContent || "";
          }
        }
        const text2 = cleanText(ownText);
        if (text2 && text2.length >= 2) {
          const textKey2 = text2.substring(0, 100);
          if (!seenTexts.has(textKey2)) {
            seenTexts.add(textKey2);
            result.push({ text: text2, element: htmlEl, canHighlight: true });
          }
        }
        continue;
      }
      const text = cleanText(htmlEl.textContent || "");
      if (!text || text.length < 2) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: htmlEl, canHighlight: true });
    }
    const preBlocks = container.querySelectorAll("pre");
    for (const pre of Array.from(preBlocks)) {
      const codeEl = pre.querySelector("code");
      const text = cleanText((codeEl || pre).textContent || "");
      if (!text || text.length < 10) continue;
      const textKey = text.substring(0, 100);
      if (seenTexts.has(textKey)) continue;
      seenTexts.add(textKey);
      result.push({ text, element: pre, canHighlight: true });
    }
    if (result.length === 0) {
      const text = cleanText(container.textContent || "");
      if (text && text.length >= 10) {
        const textKey = text.substring(0, 100);
        if (!seenTexts.has(textKey)) {
          seenTexts.add(textKey);
          result.push({ text, element: container, canHighlight: true });
        }
      }
    }
    return result;
  }
  function isKimiSharePage() {
    return window.location.pathname.includes("/share");
  }
  function extractFromSharePage(seenTexts) {
    const result = [];
    const mdContainers = document.querySelectorAll('.markdown, [class*="markdown"]');
    if (mdContainers.length === 0) {
      console.log("[kimi/share] 未找到 markdown 容器");
      return result;
    }
    console.log("[kimi/share] 找到 markdown 容器:", mdContainers.length);
    for (const container of Array.from(mdContainers)) {
      const htmlContainer = container;
      if (htmlContainer.offsetHeight === 0 && htmlContainer.offsetWidth === 0) continue;
      const paraElements = htmlContainer.querySelectorAll(SHARE_PAGE_PARAGRAPH_SELECTOR);
      for (const el of Array.from(paraElements)) {
        const htmlEl = el;
        if (shouldSkipElement(htmlEl)) continue;
        if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
        if (htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol")) {
          let ownText = "";
          for (const child of Array.from(htmlEl.childNodes)) {
            if (child.nodeType === Node.TEXT_NODE) {
              ownText += child.textContent || "";
            } else if (child.nodeType === Node.ELEMENT_NODE) {
              const tag = child.tagName;
              if (tag !== "UL" && tag !== "OL") {
                ownText += child.textContent || "";
              }
            }
          }
          const text2 = cleanText(ownText);
          if (text2 && text2.length >= 5) {
            const textKey2 = text2.substring(0, 100);
            if (!seenTexts.has(textKey2)) {
              seenTexts.add(textKey2);
              result.push({ text: text2, element: htmlEl, canHighlight: true });
            }
          }
          continue;
        }
        const text = cleanText(htmlEl.textContent || "");
        if (!text || text.length < 5) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
      const preBlocks = htmlContainer.querySelectorAll("pre");
      for (const pre of Array.from(preBlocks)) {
        const text = cleanText(pre.textContent || "");
        if (!text || text.length < 10) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: pre, canHighlight: true });
      }
    }
    if (result.length === 0) {
      console.log("[kimi/share] 标准选择器未提取到内容，尝试直接子元素...");
      for (const container of Array.from(mdContainers)) {
        const htmlContainer = container;
        if (htmlContainer.offsetHeight === 0 && htmlContainer.offsetWidth === 0) continue;
        for (const child of Array.from(htmlContainer.children)) {
          const htmlChild = child;
          if (shouldSkipElement(htmlChild)) continue;
          if (htmlChild.offsetHeight === 0 && htmlChild.offsetWidth === 0) continue;
          const text = cleanText(htmlChild.textContent || "");
          if (!text || text.length < 5) continue;
          const textKey = text.substring(0, 100);
          if (seenTexts.has(textKey)) continue;
          seenTexts.add(textKey);
          result.push({ text, element: htmlChild, canHighlight: true });
        }
      }
    }
    return result;
  }
  const kimiExtractor = {
    siteName: "Kimi",
    matches: ["kimi.moonshot.cn", "kimi.com"],
    supportsHighlight() {
      return true;
    },
    extractText() {
      var _a;
      const paragraphs = ((_a = this.extractParagraphsWithElements) == null ? void 0 : _a.call(this)) || [];
      if (paragraphs.length === 0) return null;
      return paragraphs.map((p) => p.text).join("\n\n");
    },
    extractTitle() {
      return document.title.replace(/\s*[-–—|]\s*Kimi\s*$/i, "").trim() || "Kimi";
    },
    extractLanguage() {
      let content = "";
      const mdEls = document.querySelectorAll('.markdown, [class*="markdown"]');
      for (const el of Array.from(mdEls)) {
        if (isUserMessage(el)) continue;
        content += el.textContent || "";
        if (content.length > 2e3) break;
      }
      if (!content) content = document.body.textContent || "";
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      return chineseChars > content.length * 0.1 ? "zh" : "en";
    },
    extractParagraphsWithElements() {
      console.log("[kimi] 开始提取 AI 回复...");
      const result = [];
      const seenTexts = /* @__PURE__ */ new Set();
      if (isKimiSharePage()) {
        console.log("[kimi] 检测到分享页，使用专用提取逻辑");
        const shareResult = extractFromSharePage(seenTexts);
        if (shareResult.length > 0) {
          console.log("[kimi/share] 提取完成，段落数:", shareResult.length);
          return shareResult;
        }
        console.log("[kimi/share] 专用提取未获取内容，回退到通用方法");
      }
      for (const sel of AI_MESSAGE_SELECTORS) {
        const aiMessages = document.querySelectorAll(sel);
        if (aiMessages.length > 0) {
          console.log("[kimi] 找到 AI 消息:", aiMessages.length, "(selector:", sel, ")");
          for (const msg of Array.from(aiMessages)) {
            const paragraphs = extractParagraphsFromMessage(msg, seenTexts);
            result.push(...paragraphs);
          }
          if (result.length > 0) {
            console.log("[kimi] 提取完成，段落数:", result.length);
            return result;
          }
        }
      }
      console.log("[kimi] AI 消息选择器未命中，尝试 markdown 容器...");
      for (const sel of MARKDOWN_SELECTORS) {
        const mdBlocks = document.querySelectorAll(sel);
        if (mdBlocks.length > 0) {
          console.log("[kimi] 找到 markdown 块:", mdBlocks.length, "(selector:", sel, ")");
          for (const block of Array.from(mdBlocks)) {
            const htmlBlock = block;
            if (isUserMessage(htmlBlock)) continue;
            const paragraphs = extractParagraphsFromMessage(htmlBlock, seenTexts);
            result.push(...paragraphs);
          }
          if (result.length > 0) {
            console.log("[kimi] 提取完成，段落数:", result.length);
            return result;
          }
        }
      }
      console.log("[kimi] markdown 方法未命中，尝试对话容器...");
      let conversation = null;
      for (const sel of CONVERSATION_SELECTORS) {
        conversation = document.querySelector(sel);
        if (conversation && conversation.textContent && conversation.textContent.trim().length > 100) break;
      }
      if (!conversation) {
        console.log("[kimi] 未找到对话容器");
        return result;
      }
      const elements = conversation.querySelectorAll(PARAGRAPH_SELECTOR);
      for (const el of Array.from(elements)) {
        const htmlEl = el;
        if (shouldSkipElement(htmlEl)) continue;
        if (isUserMessage(htmlEl)) continue;
        if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) continue;
        const hasNestedList2 = htmlEl.tagName === "LI" && htmlEl.querySelector("ul, ol");
        const hasCodeBlock2 = !!htmlEl.querySelector("pre");
        if (hasNestedList2 || hasCodeBlock2) {
          let ownText = "";
          for (const child of Array.from(htmlEl.childNodes)) {
            if (child.nodeType === Node.TEXT_NODE) {
              ownText += child.textContent || "";
            } else if (child.nodeType === Node.ELEMENT_NODE) {
              const childEl = child;
              const tag = childEl.tagName;
              if (tag === "UL" || tag === "OL" || tag === "PRE") continue;
              if (childEl.querySelector("pre")) continue;
              ownText += childEl.textContent || "";
            }
          }
          const text2 = cleanText(ownText);
          if (text2 && text2.length >= 2) {
            const textKey2 = text2.substring(0, 100);
            if (!seenTexts.has(textKey2)) {
              seenTexts.add(textKey2);
              result.push({ text: text2, element: htmlEl, canHighlight: true });
            }
          }
          continue;
        }
        const text = cleanText(htmlEl.textContent || "");
        if (!text || text.length < 2) continue;
        const textKey = text.substring(0, 100);
        if (seenTexts.has(textKey)) continue;
        seenTexts.add(textKey);
        result.push({ text, element: htmlEl, canHighlight: true });
      }
      console.log("[kimi] 提取完成，段落数:", result.length);
      return result;
    }
  };
  const PUA_RANGE = [
    [58344, 58715],
    // Mode 0: U+E3E8 ~ U+E55B
    [58345, 58716]
    // Mode 1: U+E3E9 ~ U+E55C
  ];
  const CHARSET = [
    ["D", "在", "主", "特", "家", "军", "然", "表", "场", "4", "要", "只", "v", "和", "?", "6", "别", "还", "g", "现", "儿", "岁", "?", "?", "此", "象", "月", "3", "出", "战", "工", "相", "o", "男", "直", "失", "世", "F", "都", "平", "文", "什", "V", "O", "将", "真", "T", "那", "当", "?", "会", "立", "些", "u", "是", "十", "张", "学", "气", "大", "爱", "两", "命", "全", "后", "东", "性", "通", "被", "1", "它", "乐", "接", "而", "感", "车", "山", "公", "了", "常", "以", "何", "可", "话", "先", "p", "i", "叫", "轻", "M", "士", "w", "着", "变", "尔", "快", "l", "个", "说", "少", "色", "里", "安", "花", "远", "7", "难", "师", "放", "t", "报", "认", "面", "道", "S", "?", "克", "地", "度", "I", "好", "机", "U", "民", "写", "把", "万", "同", "水", "新", "没", "书", "电", "吃", "像", "斯", "5", "为", "y", "白", "几", "日", "教", "看", "但", "第", "加", "候", "作", "上", "拉", "住", "有", "法", "r", "事", "应", "位", "利", "你", "声", "身", "国", "问", "马", "女", "他", "Y", "比", "父", "x", "A", "H", "N", "s", "X", "边", "美", "对", "所", "金", "活", "回", "意", "到", "z", "从", "j", "知", "又", "内", "因", "点", "Q", "三", "定", "8", "R", "b", "正", "或", "夫", "向", "德", "听", "更", "?", "得", "告", "并", "本", "q", "过", "记", "L", "让", "打", "f", "人", "就", "者", "去", "原", "满", "体", "做", "经", "K", "走", "如", "孩", "c", "G", "给", "使", "物", "?", "最", "笑", "部", "?", "员", "等", "受", "k", "行", "一", "条", "果", "动", "光", "门", "头", "见", "往", "自", "解", "成", "处", "天", "能", "于", "名", "其", "发", "总", "母", "的", "死", "手", "入", "路", "进", "心", "来", "h", "时", "力", "多", "开", "已", "许", "d", "至", "由", "很", "界", "n", "小", "与", "Z", "想", "代", "么", "分", "生", "口", "再", "妈", "望", "次", "西", "风", "种", "带", "J", "?", "实", "情", "才", "这", "?", "E", "我", "神", "格", "长", "觉", "间", "年", "眼", "无", "不", "亲", "关", "结", "0", "友", "信", "下", "却", "重", "己", "老", "2", "音", "字", "m", "呢", "明", "之", "前", "高", "P", "B", "目", "太", "e", "9", "起", "稜", "她", "也", "W", "用", "方", "子", "英", "每", "理", "便", "四", "数", "期", "中", "C", "外", "样", "a", "海", "们", "任"],
    ["s", "?", "作", "口", "在", "他", "能", "并", "B", "士", "4", "U", "克", "才", "正", "们", "字", "声", "高", "全", "尔", "活", "者", "动", "其", "主", "报", "多", "望", "放", "h", "w", "次", "年", "?", "中", "3", "特", "于", "十", "入", "要", "男", "同", "G", "面", "分", "方", "K", "什", "再", "教", "本", "己", "结", "1", "等", "世", "N", "?", "说", "g", "u", "期", "Z", "外", "美", "M", "行", "给", "9", "文", "将", "两", "许", "张", "友", "0", "英", "应", "向", "像", "此", "白", "安", "少", "何", "打", "气", "常", "定", "间", "花", "见", "孩", "它", "直", "风", "数", "使", "道", "第", "水", "已", "女", "山", "解", "d", "P", "的", "通", "关", "性", "叫", "儿", "L", "妈", "问", "回", "神", "来", "S", "", "四", "望", "前", "国", "些", "O", "v", "l", "A", "心", "平", "自", "无", "军", "光", "代", "是", "好", "却", "c", "得", "种", "就", "意", "先", "立", "z", "子", "过", "Y", "j", "表", "", "么", "所", "接", "了", "名", "金", "受", "J", "满", "眼", "没", "部", "那", "m", "每", "车", "度", "可", "R", "斯", "经", "现", "门", "明", "V", "如", "走", "命", "y", "6", "E", "战", "很", "上", "f", "月", "西", "7", "长", "夫", "想", "话", "变", "海", "机", "x", "到", "W", "一", "成", "生", "信", "笑", "但", "父", "开", "内", "东", "马", "日", "小", "而", "后", "带", "以", "三", "几", "为", "认", "X", "死", "员", "目", "位", "之", "学", "远", "人", "音", "呢", "我", "q", "乐", "象", "重", "对", "个", "被", "别", "F", "也", "书", "稜", "D", "写", "还", "因", "家", "发", "时", "i", "或", "住", "德", "当", "o", "l", "比", "觉", "然", "吃", "去", "公", "a", "老", "亲", "情", "体", "太", "b", "万", "C", "电", "理", "?", "失", "力", "更", "拉", "物", "着", "原", "她", "工", "实", "色", "感", "记", "看", "出", "相", "路", "大", "你", "候", "2", "和", "?", "与", "p", "样", "新", "只", "便", "最", "不", "进", "T", "r", "做", "格", "母", "总", "爱", "身", "师", "轻", "知", "往", "加", "从", "?", "天", "e", "H", "?", "听", "场", "由", "快", "边", "让", "把", "任", "8", "条", "头", "事", "至", "起", "点", "真", "手", "这", "难", "都", "界", "用", "法", "n", "处", "下", "又", "Q", "告", "地", "5", "k", "t", "岁", "有", "会", "果", "利", "民"]
  ];
  function decodeFanqieText(text) {
    const decoded0 = decodeWithMode(text, 0);
    let puaRemaining = 0;
    for (const ch of decoded0) {
      const cp = ch.codePointAt(0) || 0;
      if (cp >= 57344 && cp <= 63743) puaRemaining++;
    }
    if (puaRemaining > 5) {
      return decodeWithMode(text, 1);
    }
    return decoded0;
  }
  function decodeWithMode(text, mode) {
    const [lo, hi] = PUA_RANGE[mode];
    const charset = CHARSET[mode];
    let result = "";
    for (const ch of text) {
      const cp = ch.codePointAt(0) || 0;
      if (cp >= lo && cp <= hi) {
        const idx = cp - lo;
        if (idx >= 0 && idx < charset.length && charset[idx] !== "?") {
          result += charset[idx];
        } else {
          result += ch;
        }
      } else {
        result += ch;
      }
    }
    return result;
  }
  const fanqieExtractor = {
    siteName: "FanqieNovel",
    matches: ["fanqienovel.com"],
    extractTitle() {
      var _a;
      const titleEl = document.querySelector("h1.muye-reader-title") || document.querySelector(".chapter-title") || document.querySelector("h1");
      if (titleEl) {
        return decodeFanqieText(((_a = titleEl.textContent) == null ? void 0 : _a.trim()) || "");
      }
      return decodeFanqieText(document.title || "");
    },
    extractText() {
      var _a;
      const paras = ((_a = this.extractParagraphsWithElements) == null ? void 0 : _a.call(this)) || [];
      return paras.map((p) => p.text).join("\n") || null;
    },
    extractLanguage() {
      return "zh";
    },
    extractParagraphsWithElements() {
      var _a;
      const container = document.querySelector("div.muye-reader-content") || document.querySelector(".reader-content") || document.querySelector('[class*="reader-content"]');
      if (!container) return [];
      const paragraphs = [];
      const pElements = container.querySelectorAll("p");
      for (const p of pElements) {
        const rawText = ((_a = p.textContent) == null ? void 0 : _a.trim()) || "";
        if (rawText.length < 2) continue;
        const decoded = decodeFanqieText(rawText);
        if (decoded.length < 2) continue;
        paragraphs.push({
          text: decoded,
          element: p
        });
      }
      return paragraphs;
    }
  };
  function matchSiteRule(hostname, pathname) {
    const rules2 = siteRulesData.rules;
    if (rules2.length === 0) return null;
    let best = null;
    for (const rule of rules2) {
      if (!hostname.includes(rule.domain)) continue;
      try {
        if (rule.pathPattern && !new RegExp(rule.pathPattern).test(pathname)) continue;
      } catch {
        continue;
      }
      if (!best || rule.confidence > best.confidence) {
        best = rule;
      }
    }
    return best;
  }
  function hasSignificantNewlines(el) {
    let significantLines = 0;
    for (const node of el.childNodes) {
      if (node.nodeType !== Node.TEXT_NODE) continue;
      const text = node.textContent || "";
      if (!text.includes("\n")) continue;
      for (const line of text.split("\n")) {
        if (line.trim().length >= 10) significantLines++;
        if (significantLines >= 2) return true;
      }
    }
    return false;
  }
  function normalizeNewlinesToBr(el) {
    const doc = el.ownerDocument;
    const textNodes = [];
    for (const node of Array.from(el.childNodes)) {
      if (node.nodeType === Node.TEXT_NODE && (node.textContent || "").includes("\n")) {
        textNodes.push(node);
      }
    }
    for (const textNode of textNodes) {
      const parts = (textNode.textContent || "").split("\n");
      for (let i = 0; i < parts.length; i++) {
        if (i > 0) el.insertBefore(doc.createElement("br"), textNode);
        if (parts[i]) el.insertBefore(doc.createTextNode(parts[i]), textNode);
      }
      el.removeChild(textNode);
    }
  }
  function splitElementByBr(el) {
    const results = [];
    const doc = el.ownerDocument;
    if (el.querySelectorAll("br").length < 2) {
      normalizeNewlinesToBr(el);
    }
    const children = Array.from(el.childNodes);
    let currentNodes = [];
    const flushSegment = () => {
      if (currentNodes.length === 0) return;
      const text = currentNodes.map((n) => n.textContent || "").join("").trim();
      if (text.length < 10) {
        currentNodes = [];
        return;
      }
      const span = doc.createElement("span");
      span.setAttribute("data-cr-para", "true");
      const firstNode = currentNodes[0];
      el.insertBefore(span, firstNode);
      for (const n of currentNodes) {
        span.appendChild(n);
      }
      results.push({ text, element: span });
      currentNodes = [];
    };
    for (const node of children) {
      if (node.nodeType === Node.ELEMENT_NODE && node.tagName === "BR") {
        flushSegment();
      } else {
        currentNodes.push(node);
      }
    }
    flushSegment();
    return results;
  }
  function extractWithSiteRule(rule) {
    let container = document.querySelector(rule.contentSelector);
    if (!container && hasShadowContent()) {
      const deep = deepQuerySelectorAll(document, rule.contentSelector);
      if (deep.length > 0) container = deep[0];
    }
    if (!container) return [];
    const shadowMode = hasShadowContent();
    const excludeSet = /* @__PURE__ */ new Set();
    for (const sel of rule.excludeSelectors) {
      try {
        container.querySelectorAll(sel).forEach((el) => excludeSet.add(el));
      } catch {
      }
      try {
        document.querySelectorAll(sel).forEach((el) => {
          if (container.contains(el)) excludeSet.add(el);
        });
      } catch {
      }
      if (shadowMode) {
        try {
          deepQuerySelectorAll(container, sel).forEach((el) => excludeSet.add(el));
        } catch {
        }
      }
    }
    let elements = container.querySelectorAll(rule.paragraphSelector);
    if (elements.length === 0) {
      const fromDoc = document.querySelectorAll(rule.paragraphSelector);
      elements = Array.from(fromDoc).filter((el) => container.contains(el));
    }
    if (elements.length === 0 && shadowMode) {
      elements = deepQuerySelectorAll(container, rule.paragraphSelector);
    }
    const paragraphs = [];
    const seen = /* @__PURE__ */ new Set();
    const elementList = elements instanceof NodeList ? Array.from(elements) : elements;
    elementList.forEach((el) => {
      var _a;
      if (excludeSet.has(el)) return;
      for (const ex of excludeSet) {
        if (ex.contains(el)) return;
      }
      const htmlEl = el;
      if (htmlEl.offsetHeight === 0 && htmlEl.offsetWidth === 0) return;
      const text = ((_a = el.textContent) == null ? void 0 : _a.trim()) || "";
      if (text.length < 10) return;
      if (rule.splitByBr && (el.querySelectorAll("br").length >= 2 || hasSignificantNewlines(el))) {
        const brParas = splitElementByBr(el);
        for (const p of brParas) {
          const key2 = p.text.substring(0, 100);
          if (seen.has(key2)) continue;
          seen.add(key2);
          paragraphs.push(p);
        }
        return;
      }
      const key = text.substring(0, 100);
      if (seen.has(key)) return;
      seen.add(key);
      paragraphs.push({ text, element: el });
    });
    return paragraphs;
  }
  const SPECIAL_EXTRACTORS = /* @__PURE__ */ new Map([
    ["mp.weixin.qq.com", weixinExtractor],
    ["weread.qq.com", wereadExtractor],
    ["yuque.com", yuqueExtractor],
    ["dingtalk.com", dingtalkExtractor],
    ["alidocs.dingtalk.com", dingtalkExtractor],
    ["feishu.cn", feishuExtractor],
    ["larksuite.com", feishuExtractor],
    ["larkoffice.com", feishuExtractor],
    ["notion.so", notionExtractor],
    ["notion.site", notionExtractor],
    ["docs.google.com", googleDocsExtractor],
    ["read.amazon.com", kindleExtractor],
    ["read.amazon.cn", kindleExtractor],
    ["chatgpt.com", chatgptExtractor],
    ["claude.ai", claudeAiExtractor],
    ["gemini.google.com", geminiExtractor],
    ["doubao.com", doubaoExtractor],
    ["chat.deepseek.com", deepseekExtractor],
    ["kimi.moonshot.cn", kimiExtractor],
    ["kimi.com", kimiExtractor],
    ["fanqienovel.com", fanqieExtractor]
  ]);
  function getSpecialExtractor(hostname) {
    for (const [domain, extractor] of SPECIAL_EXTRACTORS) {
      if (hostname.includes(domain)) {
        return extractor;
      }
    }
    return null;
  }
  function detectLanguageFromParagraphs(paragraphs) {
    var _a;
    let sampleText = "";
    for (const p of paragraphs) {
      sampleText += p.text + " ";
      if (sampleText.length >= 3e3) break;
    }
    sampleText = sampleText.substring(0, 3e3);
    if (sampleText.length > 0) {
      const japaneseKanaCount = (sampleText.match(/[\u3040-\u309f\u30a0-\u30ff]/g) || []).length;
      if (japaneseKanaCount > sampleText.length * 0.05) return "ja";
      const koreanCount = (sampleText.match(/[\uac00-\ud7af\u1100-\u11ff]/g) || []).length;
      if (koreanCount > sampleText.length * 0.1) return "ko";
      const cjkCount = (sampleText.match(/[\u4e00-\u9fa5]/g) || []).length;
      if (cjkCount > sampleText.length * 0.1) return "zh";
    }
    if (sampleText.length > 0) {
      const latinCount = (sampleText.match(/[a-zA-Z]/g) || []).length;
      if (latinCount > sampleText.length * 0.4) {
        const htmlLang2 = (_a = document.documentElement.lang) == null ? void 0 : _a.split("-")[0].toLowerCase();
        const CJK_LANGS = /* @__PURE__ */ new Set(["zh", "cn", "ja", "ko"]);
        if (!htmlLang2 || CJK_LANGS.has(htmlLang2)) return "en";
        return htmlLang2;
      }
    }
    const htmlLang = document.documentElement.lang;
    if (htmlLang) {
      const lang = htmlLang.split("-")[0].toLowerCase();
      if (lang === "zh" || lang === "cn") return "zh";
      return lang;
    }
    if (window.location.hostname.endsWith(".cn")) return "zh";
    return "en";
  }
  class ExtractionPipeline {
    /**
     * Sync extraction (used by EVAL_EXTRACT and general use)
     *
     * 3-layer pipeline:
     * 1. Special extractor (hostname-matched)
     * 2. Site rules (eval:learn learned CSS selectors)
     * 3. Visible-Text-Walk (Google Translate style)
     */
    extract(mode = "smart") {
      var _a, _b, _c, _d, _e;
      const hostname = window.location.hostname;
      const specialExtractor = mode === "smart" ? getSpecialExtractor(hostname) : null;
      let specialResult = null;
      if (specialExtractor) {
        try {
          const paragraphs2 = ((_a = specialExtractor.extractParagraphsWithElements) == null ? void 0 : _a.call(specialExtractor)) || [];
          if (paragraphs2.length >= 3) {
            const title2 = specialExtractor.extractTitle();
            const language2 = ((_b = specialExtractor.extractLanguage) == null ? void 0 : _b.call(specialExtractor)) || detectLanguageFromParagraphs(paragraphs2);
            return {
              paragraphs: paragraphs2,
              title: title2,
              success: true,
              method: "special",
              language: language2,
              siteName: specialExtractor.siteName
            };
          }
          if (paragraphs2.length > 0) {
            console.log(`[Pipeline] Special extractor sparse: ${paragraphs2.length} paras, will compare with VTB`);
            specialResult = {
              paragraphs: paragraphs2,
              title: specialExtractor.extractTitle(),
              lang: ((_c = specialExtractor.extractLanguage) == null ? void 0 : _c.call(specialExtractor)) || detectLanguageFromParagraphs(paragraphs2),
              siteName: specialExtractor.siteName
            };
          }
        } catch (error) {
          console.error("[Pipeline] Special extractor failed:", error);
        }
      }
      if (mode === "smart") {
        const siteRule = matchSiteRule(hostname, window.location.pathname);
        if (siteRule) {
          try {
            const ruleParagraphs = extractWithSiteRule(siteRule);
            if (ruleParagraphs.length > 0) {
              const ruleTitle = siteRule.titleSelector ? ((_e = (_d = document.querySelector(siteRule.titleSelector)) == null ? void 0 : _d.textContent) == null ? void 0 : _e.trim()) || document.title : document.title;
              console.log(`[Pipeline] Site rule matched: ${siteRule.domain} (${ruleParagraphs.length} paras)`);
              return {
                paragraphs: ruleParagraphs,
                title: ruleTitle,
                success: true,
                method: "site-rule",
                language: detectLanguageFromParagraphs(ruleParagraphs),
                siteName: `SiteRule:${siteRule.domain}`
              };
            }
          } catch (error) {
            console.error("[Pipeline] Site rule extraction failed:", error);
          }
        }
      }
      const paragraphs = mode === "read-all" ? readAllExtract() : visibleTextBlockExtract();
      if (specialResult) {
        const specialChars = specialResult.paragraphs.reduce((s, p) => s + p.text.length, 0);
        const vtbChars = paragraphs.reduce((s, p) => s + p.text.length, 0);
        if (specialChars >= vtbChars || paragraphs.length < 3) {
          console.log(`[Pipeline] Using sparse special result (${specialResult.paragraphs.length} paras, ${specialChars} chars) over VTB (${paragraphs.length} paras, ${vtbChars} chars)`);
          return {
            paragraphs: specialResult.paragraphs,
            title: specialResult.title,
            success: true,
            method: "special",
            language: specialResult.lang,
            siteName: specialResult.siteName
          };
        }
        console.log(`[Pipeline] VTB (${paragraphs.length} paras, ${vtbChars} chars) beats sparse special (${specialResult.paragraphs.length} paras, ${specialChars} chars)`);
      }
      const title = document.title || null;
      const language = detectLanguageFromParagraphs(paragraphs);
      return {
        paragraphs,
        title,
        success: paragraphs.length > 0,
        method: mode === "read-all" ? "read-all" : "visible-text-block",
        language,
        siteName: mode === "read-all" ? "Read-All" : "Visible-Text-Walk"
      };
    }
    /**
     * Async extraction with SPA content waiting.
     *
     * If initial extraction yields very little content, the page may be a SPA
     * still rendering. We use MutationObserver to wait for DOM stabilization
     * (no mutations for 500ms), then re-extract.
     *
     * Timeout: 8 seconds max wait.
     */
    async extractWithLearning(mode = "smart") {
      var _a;
      if (mode === "smart") {
        const hostname = window.location.hostname;
        const specialExtractor = getSpecialExtractor(hostname);
        if (specialExtractor == null ? void 0 : specialExtractor.extractParagraphsAsync) {
          try {
            const paragraphs = await specialExtractor.extractParagraphsAsync();
            if (paragraphs.length > 0) {
              return {
                paragraphs,
                title: specialExtractor.extractTitle(),
                success: true,
                method: "special",
                language: ((_a = specialExtractor.extractLanguage) == null ? void 0 : _a.call(specialExtractor)) || detectLanguageFromParagraphs(paragraphs),
                siteName: specialExtractor.siteName
              };
            }
          } catch (error) {
            console.error("[Pipeline] Async special extractor failed:", error);
          }
        }
      }
      const initial = this.extract(mode);
      const totalChars = initial.paragraphs.reduce((s, p) => s + p.text.length, 0);
      if (initial.paragraphs.length >= 3 && totalChars >= 200) {
        return initial;
      }
      console.log(
        `[Pipeline] Sparse content (${initial.paragraphs.length} paras, ${totalChars} chars). Waiting for SPA render...`
      );
      await waitForDomStable(8e3, 500);
      const afterWait = this.extract(mode);
      const afterChars = afterWait.paragraphs.reduce((s, p) => s + p.text.length, 0);
      console.log(
        `[Pipeline] After SPA wait: ${afterWait.paragraphs.length} paras, ${afterChars} chars`
      );
      return afterChars > totalChars ? afterWait : initial;
    }
  }
  function waitForDomStable(maxWaitMs, quietMs) {
    return new Promise((resolve) => {
      let timer;
      const deadline = setTimeout(() => {
        observer.disconnect();
        resolve();
      }, maxWaitMs);
      const observer = new MutationObserver(() => {
        clearTimeout(timer);
        timer = setTimeout(() => {
          observer.disconnect();
          clearTimeout(deadline);
          resolve();
        }, quietMs);
      });
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
      timer = setTimeout(() => {
        observer.disconnect();
        clearTimeout(deadline);
        resolve();
      }, quietMs);
    });
  }
  if (typeof globalThis.chrome === "undefined") {
    globalThis.chrome = {
      storage: { local: { get: async () => ({}), set: async () => {
      } } },
      runtime: { sendMessage: async () => ({}) }
    };
  }
  async function extract() {
    try {
      const pipeline = new ExtractionPipeline();
      const result = await pipeline.extractWithLearning();
      const paragraphElementMeta = result.paragraphs.map((p) => {
        const el = p.element;
        const hasElement = !!el;
        let isVisible = false;
        let canHighlight = false;
        if (hasElement && el) {
          try {
            isVisible = !!(el.offsetParent !== null || el.offsetWidth > 0 || el.offsetHeight > 0);
            canHighlight = isVisible;
          } catch {
          }
        }
        return { hasElement, isVisible, canHighlight };
      });
      return {
        method: result.method,
        title: result.title,
        paragraphs: result.paragraphs.map((p) => {
          var _a, _b;
          return {
            text: p.text,
            tagName: ((_a = p.element) == null ? void 0 : _a.tagName) || "UNKNOWN",
            className: (((_b = p.element) == null ? void 0 : _b.className) || "").toString().substring(0, 100)
          };
        }),
        totalParagraphs: result.paragraphs.length,
        totalCharacters: result.paragraphs.reduce((sum, p) => sum + p.text.length, 0),
        language: result.language,
        success: result.success,
        paragraphElementMeta
      };
    } catch (error) {
      return {
        method: "error",
        title: null,
        paragraphs: [],
        totalParagraphs: 0,
        totalCharacters: 0,
        language: "unknown",
        success: false,
        error: error.message,
        paragraphElementMeta: []
      };
    }
  }
  window.__castreaderExtract = extract;
})();
