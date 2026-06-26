(() => {
  function cloneAndClean(root, isX) {
    var clone = root.cloneNode(true);

    var dropSelectors = [
      'script', 'style', 'noscript', 'svg', 'canvas', 'iframe',
      'header', 'footer', 'nav', 'aside',
      '[role="banner"]', '[role="navigation"]', '[role="complementary"]',
      '[class*="cookie"]', '[id*="cookie"]', '[class*="consent"]', '[id*="consent"]',
      '[class*="gdpr"]', '[id*="gdpr"]', '[class*="ad-"]', '[id*="ad-"]',
      '[class*="advert"]', '[id*="advert"]', '[class*="promo"]', '[id*="promo"]'
    ];

    if (isX) {
      dropSelectors = dropSelectors.concat([
        '[data-testid="sidebarColumn"]',
        '[data-testid="Trend"]',
        '[data-testid="trends"]',
        '[data-testid="trending"]',
        '[data-testid="BottomBar"]',
        '[data-testid="BottomBarContainer"]',
        '[data-testid="SignupModal"]',
        '[data-testid="drawer"]',
        '[data-testid="placementTracking"]',
        '[data-testid="inlinePlayer"]',
        '[aria-label*="Trending"]',
        '[aria-label*="Who to follow"]',
        '[aria-label*="Footer"]',
        '[aria-label*="Footer"]',
        '[role="status"][aria-busy]'
      ]);
    }

    clone.querySelectorAll(dropSelectors.join(',')).forEach(function (node) {
      if (node && node.parentNode) node.parentNode.removeChild(node);
    });

    return clone;
  }

  function normalizeSpace(text) {
    return (text || '').replace(/\s+/g, ' ').replace(/\u00a0/g, ' ').trim();
  }

  function isActionWidget(el) {
    if (!el || !el.getAttribute) return false;
    var id = el.getAttribute('data-testid') || '';
    var role = (el.getAttribute('role') || '').toLowerCase();
    var label = (el.getAttribute('aria-label') || '').toLowerCase();
    var actionIds = {
      reply: 1, retweet: 1, like: 1, bookmark: 1, share: 1,
      analytics: 1, tweetText: 0,
      'tweet-text-show-more-link': 1,
      'logged_out_read_replies_pivot': 1,
      socialContext: 1,
      socialProof: 1,
      replyButton: 1,
      likeButton: 1,
      retweetButton: 1,
      bookmarkButton: 1,
      shareButton: 1
    };
    if (actionIds[id]) return true;
    if (role === 'button' && /(reply|retweet|like|share|bookmark|analytics|repost)/i.test(label)) return true;
    if (role === 'button' && /\b(view|views)\b/i.test(label)) return true;
    return false;
  }

  function removeNode(node) {
    if (!node || !node.parentNode) return;
    node.parentNode.removeChild(node);
  }

  function pickSeed(root, statusId) {
    var candidates = [];

    if (statusId) {
      var allTweets = Array.from(root.querySelectorAll('article[data-testid="tweet"]'));
      for (var i = 0; i < allTweets.length; i++) {
        var tweet = allTweets[i];
        var links = Array.from(tweet.querySelectorAll('a[href]'));
        for (var j = 0; j < links.length; j++) {
          var href = links[j].getAttribute('href') || '';
          if (href.indexOf('/status/' + statusId) !== -1) {
            return tweet;
          }
        }
      }
    }

    // Prefer X tweet/article nodes if present.
    var xSelector = root.querySelectorAll('article[data-testid="tweet"]');
    if (xSelector && xSelector.length) {
      candidates = Array.from(xSelector);
    }

    if (!candidates.length) {
      candidates = Array.from(root.querySelectorAll('article, [role="main"], main, [itemtype="https://schema.org/NewsArticle"], [itemtype="http://schema.org/NewsArticle"], [class*="article"], [data-testid="tweetText"]'));
    }

    if (!candidates.length) return root;

    var best = candidates[0];
    var bestScore = -1;

    for (var c = 0; c < candidates.length; c++) {
      var el = candidates[c];
      var txt = normalizeSpace((el.innerText || ''));
      var len = txt.length;
      if (!len) continue;

      var score = len;
      var role = (el.getAttribute('role') || '').toLowerCase();
      if (role === 'article') score += 5000;
      if (el.tagName && el.tagName.toLowerCase() === 'article') score += 4000;
      if (el.getAttribute && el.getAttribute('data-testid') === 'tweet') score += 3000;
      if (statusId && el.innerText && el.innerText.indexOf(statusId) !== -1) score += 2000;

      var rect = el.getBoundingClientRect ? el.getBoundingClientRect() : null;
      if (rect && rect.width * rect.height > 0) score += 1000;

      if (score > bestScore) {
        bestScore = score;
        best = el;
      }
    }

    return best;
  }

  function inlineText(node) {
    if (!node) return '';
    if (node.nodeType === Node.TEXT_NODE) {
      return (node.textContent || '').replace(/\s+/g, ' ');
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return '';

    var tag = node.tagName.toLowerCase();
    var childText = '';
    for (var c = 0; c < node.childNodes.length; c++) {
      childText += inlineText(node.childNodes[c]);
    }

    if (tag === 'a') {
      return childText;
    }
    if (tag === 'img') {
      var alt = (node.getAttribute('alt') || 'image').trim();
      return '![' + alt + '](' + (node.getAttribute('src') || '') + ')';
    }
    if (tag === 'b' || tag === 'strong') return childText ? ('**' + childText + '**') : '';
    if (tag === 'i' || tag === 'em') return childText ? ('*' + childText + '*') : '';
    if (tag === 'code' || tag === 'pre') return childText ? ('\n\n' + childText.trim() + '\n\n') : '';
    if (tag === 'br') return '\n';
    return childText;
  }

  function blockText(node, depth) {
    depth = depth || 0;
    if (!node) return '';

    if (node.nodeType === Node.TEXT_NODE) {
      var text = (node.textContent || '').trim();
      return text ? text + '\n\n' : '';
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return '';

    var tag = node.tagName.toLowerCase();
    var out = '';

    if (/^h[1-6]$/.test(tag)) {
      var level = parseInt(tag.substring(1), 10);
      var prefix = new Array(level + 1).join('#');
      out += prefix + ' ' + normalizeSpace(node.textContent || '') + '\n\n';
      return out;
    }

    if (tag === 'ul' || tag === 'ol') {
      var ordered = tag === 'ol';
      var items = node.children;
      for (var i = 0; i < items.length; i++) {
        var child = items[i];
        if (!child.tagName || child.tagName.toLowerCase() !== 'li') continue;
        var bullet = ordered ? (i + 1) + '. ' : '- ';
        out += new Array(depth + 1).join('  ') + bullet + normalizeSpace(inlineText(child)) + '\n';
      }
      return out + '\n';
    }

    if (tag === 'p' || tag === 'blockquote' || tag === 'li') {
      return normalizeSpace(inlineText(node)) + '\n\n';
    }

    if (tag === 'hr') return '\n---\n\n';

    for (var c2 = 0; c2 < node.childNodes.length; c2++) {
      out += blockText(node.childNodes[c2], depth + 1);
    }
    return out;
  }

  function markdownify(node) {
    return (blockText(node, 0) || '').replace(/\n{3,}/g, '\n\n').trim();
  }

  function shouldDropLine(line, index, lines) {
    var t = line.trim();
    if (!t) return true;

    // Metrics-only lines, usually from reaction/footer blocks.
    if (/^(?:\d+(?:\.\d+)?[KkMmBb]?)$/.test(t)) return true;

    // X CTA/promotional/footer phrases.
    var noise = [
      /want to publish your own article\?/i,
      /upgrade to premium/i,
      /promoted/i,
      /^log in$/i,
      /^sign up$/i,
      /^view\s+more$/i,
      /connect with/i,
      /^views?$/i
    ];
    for (var n = 0; n < noise.length; n++) {
      if (noise[n].test(t)) return true;
    }

    // Side-module labels.
    if (t.length <= 28 && /^(?:trending|who to follow|relevant)$/i.test(t)) return true;

    // Repeated tweet metadata line at the bottom of article pages.
    if (t.length < 200 && /^[^\n]*·\s*\d+(?:\.\d+)?[KkMmBb]?(?:\.\d+)?\s*views?[^\n]*$/i.test(t)) return true;

    // Remove near-empty metric-like fragments
    if (/^\d+[KkMmBb]?$/.test(t) && (lines[index - 1] || '').length < 40 && (lines[index + 1] || '').length < 40) {
      return true;
    }

    return false;
  }

  function cleanText(text) {
    var lines = (text || '').split(/\r?\n/);
    var cleaned = [];
    var hadText = false;

    for (var i = 0; i < lines.length; i++) {
      var t = normalizeSpace(lines[i]);
      if (!t) {
        if (hadText) {
          cleaned.push('');
          hadText = false;
        }
        continue;
      }
      if (shouldDropLine(t, i, lines)) continue;
      cleaned.push(t);
      hadText = true;
    }

    return cleaned.join('\n').replace(/\n{3,}/g, '\n\n').trim();
  }

  function filterXSpecificNodes(clone) {
    // Action buttons/metrics controls.
    var toDrop = [];
    var all = Array.from(clone.querySelectorAll('[data-testid], [role="button"], a, button, section, div, span'));

    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (!el || !el.getAttribute) continue;
      var href = el.getAttribute('href') || '';
      var text = normalizeSpace(el.textContent || '');
      var label = normalizeSpace(el.getAttribute('aria-label') || '');
      var id = el.getAttribute('data-testid') || '';

      if (id === 'tweet-text-show-more-link' || id === 'logged_out_read_replies_pivot') {
        toDrop.push(el);
        continue;
      }
      if (href.indexOf('/i/premium_sign_up') !== -1 || href.indexOf('/i/flow/signup') !== -1 || href.indexOf('/i/flow/login') !== -1) {
        toDrop.push(el);
        continue;
      }
      if (label && /read more/i.test(label) && el.tagName && el.tagName.toLowerCase() === 'a') {
        // Keep textual "Read more" inside article text? only drop if tiny.
        if (text.length < 24) {
          toDrop.push(el);
          continue;
        }
      }
      if (isActionWidget(el)) {
        toDrop.push(el);
      }
    }

    for (var j = 0; j < toDrop.length; j++) {
      removeNode(toDrop[j]);
    }
  }

  try {
    var isX = false;
    var host = (document.location && document.location.hostname || '').toLowerCase();
    if (host === 'x.com' || host === 'www.x.com' || host === 'twitter.com' || host === 'www.twitter.com') {
      isX = true;
    }

    var pathMatch = (document.location && document.location.pathname || '').match(/\/status\/(\d+)/);
    var statusId = pathMatch ? pathMatch[1] : null;

    var body = document.body || document.documentElement;
    var clean = cloneAndClean(body, isX);

    var seed = pickSeed(clean, statusId);
    if (!seed) seed = clean;

    if (isX && seed) {
      filterXSpecificNodes(seed);
    }

    var content = cleanText(markdownify(seed));

    if (!content || content.length < 80) {
      content = cleanText((document.body && document.body.innerText) ? document.body.innerText : '');
    }

    function getMetaContent(selectors) {
      for (var i = 0; i < selectors.length; i++) {
        var el = document.querySelector(selectors[i]);
        if (el && el.getAttribute) {
          return el.getAttribute('content') || '';
        }
      }
      return '';
    }

    var title = (document.title || '').trim();
    var siteName =
      getMetaContent([
        'meta[property="og:site_name"]',
        'meta[name="application-name"]'
      ]) || document.location.hostname;

    var byline =
      getMetaContent([
        'meta[name="author"]',
        'meta[property="article:author"]'
      ]);

    var excerpt = normalizeSpace(content).slice(0, 220);

    return {
      title: title,
      content: content,
      excerpt: excerpt,
      byline: byline,
      siteName: siteName,
      length: content.length,
      url: document.location.href,
      status: isX ? 'x-tuned' : 'generic-fallback'
    };
  } catch (e) {
    var fallback = (document.body ? (document.body.innerText || '') : '');
    return {
      title: document.title || '',
      content: fallback.trim(),
      excerpt: normalizeSpace(fallback).slice(0, 220),
      byline: '',
      siteName: document.location.hostname,
      length: fallback.length,
      url: document.location.href,
      status: 'error-fallback',
      error: String(e && e.message || e)
    };
  }
})();