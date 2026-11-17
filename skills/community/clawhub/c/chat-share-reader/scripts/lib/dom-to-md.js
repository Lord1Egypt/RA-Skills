// 注入页面的 DOM → markdown 转换器。定义 window.__csrMd(el, opts) 返回字符串。
// 用于没有结构化接口、只能靠渲染结果的站点（Gemini、Grok 等）。
//
// 设计取舍：
// - 表格、代码块必须自己处理，innerText 会拍平它们
// - 遇到未知的自定义元素（Angular/Web Component）一律递归子节点，不做语义假设
// - 跳过 UI 部件（按钮、图标、反馈条），它们会污染正文
// - 宁可多留空行也不做激进压缩，markdown 渲染器容错
(function () {
  var SKIP_TAGS = {
    BUTTON: 1, SVG: 1, STYLE: 1, SCRIPT: 1, NOSCRIPT: 1, INPUT: 1,
    TEXTAREA: 1, SELECT: 1, MAT: 1, TEMPLATE: 1, CANVAS: 1,
  };
  var SKIP_SELECTOR =
    '[role="button"],[aria-hidden="true"],.sr-only,.screen-reader-text,.visually-hidden,' +
    '.response-footer,.response-actions,' +
    '.response-container-footer,.copy-button,.share-button,.thumb-up,.thumb-down,' +
    'mat-icon,.icon-button,.buttons-container,.sources-list,.response-content-sources';

  function txt(el) {
    return (el.textContent || '').replace(/\u00a0/g, ' ').replace(/[ \t]+/g, ' ').trim();
  }

  function isSkipped(el) {
    if (SKIP_TAGS[el.tagName]) return true;
    if (el.tagName === 'MAT') return true;
    if (el.tagName.indexOf('MAT-') === 0) return true;
    if (el.tagName.indexOf('BUTTON') === 0) return true;
    try {
      if (el.matches && el.matches(SKIP_SELECTOR)) return true;
    } catch (e) {}
    return false;
  }

  function inline(el) {
    var out = '';
    var nodes = el.childNodes;
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.nodeType === 3) {
        out += n.textContent.replace(/\u00a0/g, ' ').replace(/\s+/g, ' ');
        continue;
      }
      if (n.nodeType !== 1) continue;
      if (isSkipped(n)) continue;
      var tag = n.tagName;
      if (tag === 'BR') { out += '  \n'; continue; }
      if (tag === 'STRONG' || tag === 'B') { out += '**' + inline(n).trim() + '**'; continue; }
      if (tag === 'EM' || tag === 'I') { out += '*' + inline(n).trim() + '*'; continue; }
      if (tag === 'DEL' || tag === 'S') { out += '~~' + inline(n).trim() + '~~'; continue; }
      if (tag === 'CODE') { out += '`' + txt(n) + '`'; continue; }
      if (tag === 'A') {
        var href = n.getAttribute('href') || '';
        var t = inline(n).trim() || href;
        out += href && href.indexOf('javascript') !== 0 ? '[' + t + '](' + href + ')' : t;
        continue;
      }
      if (tag === 'IMG') {
        var src = n.getAttribute('src') || '';
        var alt = n.getAttribute('alt') || '';
        if (src && src.indexOf('data:') !== 0 && src.indexOf('chrome-extension') !== 0) {
          out += '![' + alt + '](' + src + ')';
        }
        continue;
      }
      out += inline(n);
    }
    return out;
  }

  function cell(td) {
    return inline(td).replace(/\s+/g, ' ').replace(/\|/g, '\\|').trim();
  }

  function tableToMd(tb) {
    var trs = tb.querySelectorAll('tr');
    var rows = [];
    for (var i = 0; i < trs.length; i++) {
      var cells = [];
      var kids = trs[i].children;
      for (var j = 0; j < kids.length; j++) {
        var k = kids[j];
        if (k.tagName === 'TD' || k.tagName === 'TH') {
          cells.push({ th: k.tagName === 'TH', v: cell(k) });
        }
      }
      if (cells.length) rows.push(cells);
    }
    if (!rows.length) return '';
    var width = 0;
    rows.forEach(function (r) { if (r.length > width) width = r.length; });
    function pad(r) {
      var v = r.map(function (c) { return c.v; });
      while (v.length < width) v.push('');
      return v;
    }
    var headIdx = -1;
    for (var a = 0; a < rows.length; a++) {
      if (rows[a].some(function (c) { return c.th; })) { headIdx = a; break; }
    }
    var head, body;
    if (headIdx >= 0) {
      head = pad(rows[headIdx]);
      body = rows.filter(function (_, idx) { return idx !== headIdx; });
    } else {
      head = pad(rows[0]);
      body = rows.slice(1);
    }
    var lines = ['| ' + head.join(' | ') + ' |'];
    lines.push('|' + head.map(function () { return ' --- '; }).join('|') + '|');
    body.forEach(function (r) { lines.push('| ' + pad(r).join(' | ') + ' |'); });
    return '\n' + lines.join('\n') + '\n';
  }

  function preToMd(el) {
    var codeEl = el.querySelector('code') || el;
    var text = (codeEl.innerText || codeEl.textContent || '').replace(/\n+$/, '');
    var cls = ((codeEl.className || '') + ' ' + (el.className || '')).toString();
    var m = cls.match(/language-([a-z0-9+#-]+)/i);
    var lang = m ? m[1] : '';
    return '\n```' + lang + '\n' + text + '\n```\n';
  }

  function listToMd(el, depth) {
    var ordered = el.tagName === 'OL';
    var out = '';
    var idx = 1;
    for (var i = 0; i < el.children.length; i++) {
      var li = el.children[i];
      if (li.tagName !== 'LI') continue;
      var body = '';
      var nested = [];
      for (var j = 0; j < li.childNodes.length; j++) {
        var n = li.childNodes[j];
        if (n.nodeType === 1 && (n.tagName === 'UL' || n.tagName === 'OL')) nested.push(n);
        else if (n.nodeType === 1) body += inline(n);
        else if (n.nodeType === 3) body += n.textContent.replace(/\s+/g, ' ');
      }
      body = body.replace(/\s+/g, ' ').trim();
      out += '  '.repeat(depth) + (ordered ? idx++ + '. ' : '- ') + body + '\n';
      nested.forEach(function (s) { out += listToMd(s, depth + 1); });
    }
    return '\n' + out;
  }

  // 判断是否还有块级后代。必须查后代而不是只看直接子元素：
  // 这些站点的正文外面套着若干层未知的自定义元素（如 <message-content>），
  // 只看直接子元素会误判成行内内容，把整段回答拼成一行。
  function hasBlockChild(el) {
    try {
      return !!el.querySelector('table,pre,ul,ol,p,h1,h2,h3,h4,h5,h6,blockquote,hr');
    } catch (e) {
      return false;
    }
  }

  function render(el, opts) {
    if (!el) return '';
    if (isSkipped(el)) return '';
    var tag = el.tagName;
    if (tag === 'TABLE') return tableToMd(el);
    if (tag === 'PRE') return preToMd(el);
    if (tag === 'HR') return '\n---\n';
    if (tag === 'BLOCKQUOTE') {
      return '\n' + inline(el).split('\n').map(function (l) { return '> ' + l.trim(); }).join('\n') + '\n';
    }
    if (/^H[1-6]$/.test(tag)) {
      var lvl = Math.min(parseInt(tag[1], 10) + (opts.headOffset || 0), 6);
      return '\n' + '#'.repeat(lvl) + ' ' + inline(el).trim() + '\n';
    }
    if (tag === 'UL' || tag === 'OL') return listToMd(el, 0);
    if (tag === 'P') {
      var t = inline(el).replace(/\s+\n/g, '\n').trim();
      return t ? '\n' + t + '\n' : '';
    }
    if (tag === 'CODE') return '`' + txt(el) + '`';
    if (hasBlockChild(el)) {
      var s = '';
      for (var i = 0; i < el.children.length; i++) s += render(el.children[i], opts);
      return s;
    }
    var inlineTxt = inline(el).replace(/\s+\n/g, '\n').trim();
    return inlineTxt ? '\n' + inlineTxt + '\n' : '';
  }

  window.__csrMd = function (el, opts) {
    var md = render(el, opts || {});
    return md
      .replace(/[ \t]+\n/g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .replace(/^\n+/, '')
      .trim();
  };
})();
