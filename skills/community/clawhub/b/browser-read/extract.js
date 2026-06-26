(() => {
  function cloneAndClean(root) {
    const clone = root.cloneNode(true);
    const dropSelectors = [
      'script', 'style', 'noscript', 'svg', 'canvas', 'iframe',
      'nav', 'footer', 'header', 'aside',
      '[role="banner"]', '[role="navigation"]', '[role="complementary"]',
      '[class*="cookie"]', '[id*="cookie"]', '[class*="consent"]', '[id*="consent"]',
      '[class*="gdpr"]', '[id*="gdpr"]', '[class*="ad-"]', '[id*="ad-"]',
      '[class*="advert"]', '[id*="advert"]', '[class*="promo"]', '[id*="promo"]'
    ];
    clone.querySelectorAll(dropSelectors.join(',')).forEach(function (n) { n.remove(); });
    return clone;
  }

  function pickSeed(node) {
    const selectors = [
      'article', 'main', '[role="main"]', '[itemtype="https://schema.org/NewsArticle"]',
      '[itemtype="http://schema.org/NewsArticle"]', '[class*="post"]', '[class*="article"]',
      '[data-testid="tweet"]', '[data-testid="tweetText"]'
    ];

    var found = [];
    selectors.forEach(function (sel) {
      var list = node.querySelectorAll(sel);
      for (var i = 0; i < list.length; i++) found.push(list[i]);
    });
    found.push(node);

    var best = node;
    var bestLen = -1;
    for (var i = 0; i < found.length; i++) {
      var el = found[i];
      var txt = (el.innerText || '').trim();
      if (txt.length > bestLen) {
        bestLen = txt.length;
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
      var href = node.getAttribute('href') || '';
      var label = childText.trim();
      return label ? '[' + label + '](' + href + ')' : '';
    }
    if (tag === 'img') {
      var alt = (node.getAttribute('alt') || 'image').trim();
      var src = node.getAttribute('src') || '';
      return '![' + alt + '](' + src + ')';
    }
    if (tag === 'b' || tag === 'strong') return '**' + childText.trim() + '**';
    if (tag === 'i' || tag === 'em') return '*' + childText.trim() + '*';
    if (tag === 'code') return '`' + childText.trim() + '`';
    if (tag === 'br') return '\n';
    if (tag === 'pre') return '\n\n' + childText.trim() + '\n\n';
    return childText;
  }

  function blockText(node, depth) {
    depth = depth || 0;
    if (!node) return '';
    if (node.nodeType === Node.TEXT_NODE) {
      var t = (node.textContent || '').trim();
      return t ? t + '\n\n' : '';
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return '';

    var tag = node.tagName.toLowerCase();
    var out = '';

    if (/^h[1-6]$/.test(tag)) {
      var level = parseInt(tag.substring(1), 10);
      var prefix = new Array(level + 1).join('#');
      out += prefix + ' ' + (node.textContent || '').trim() + '\n\n';
      return out;
    }

    if (tag === 'ul' || tag === 'ol') {
      var ordered = tag === 'ol';
      var items = node.children;
      for (var i = 0; i < items.length; i++) {
        if (!items[i].tagName || items[i].tagName.toLowerCase() !== 'li') continue;
        var bullet = ordered ? String(i + 1) + '. ' : '- ';
        out += new Array(depth + 1).join('  ') + bullet + inlineText(items[i]).trim() + '\n';
      }
      return out + '\n';
    }

    if (tag === 'p' || tag === 'article' || tag === 'section' || tag === 'main' ||
        tag === 'blockquote' || tag === 'div' || tag === 'header') {
      return inlineText(node).trim() + '\n\n';
    }

    if (tag === 'li') return inlineText(node).trim() + '\n';
    if (tag === 'hr') return '\n---\n\n';

    for (var i2 = 0; i2 < node.childNodes.length; i2++) {
      out += blockText(node.childNodes[i2], depth + 1);
    }
    return out;
  }

  function markdownify(node) {
    return blockText(node, 0).replace(/\n{3,}/g, '\n\n').trim();
  }

  try {
    var body = document.body || document.documentElement;
    var clean = cloneAndClean(body);
    var seed = pickSeed(clean);
    var content = markdownify(seed);

    if (!content || content.length < 80) {
      content = (document.body && document.body.innerText ? document.body.innerText : '').trim();
    }

    var title = (document.title || '').trim();
    var siteName =
      (document.querySelector('meta[property="og:site_name"]') || {}).getAttribute &&
      (document.querySelector('meta[property="og:site_name"]').getAttribute('content')) ||
      (document.querySelector('meta[name="application-name"]') || {}).getAttribute &&
      (document.querySelector('meta[name="application-name"]').getAttribute('content')) ||
      document.location.hostname;

    var bylineEl = document.querySelector('meta[name="author"]') || document.querySelector('meta[property="article:author"]');
    var byline = bylineEl ? bylineEl.getAttribute('content') || '' : '';

    var excerpt = (content || '').replace(/\s+/g, ' ').slice(0, 220);

    return {
      title: title,
      content: content,
      excerpt: excerpt,
      byline: byline,
      siteName: siteName,
      length: (content || '').length,
      url: document.location.href,
    };
  } catch (e) {
    var bodyText = document.body ? (document.body.innerText || '') : '';
    return {
      title: document.title || '',
      content: bodyText.trim(),
      excerpt: '',
      byline: '',
      siteName: document.location.hostname,
      length: bodyText.length,
      url: document.location.href,
    };
  }
})()