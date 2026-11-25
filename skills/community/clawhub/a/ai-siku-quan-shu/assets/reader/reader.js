/* ============================================================
   《AI四库全典》阅读器 reader.js
   功能：目录树 / 正文渲染 / 全书检索 / 注解笔记 / AI 导读
   ============================================================ */
'use strict';

/* ---------- 全局状态 ---------- */
var S = {
  cur: null,            // 当前卷 {part,no,file,title}
  curHid: null,         // 当前定位标题 id
  cache: {},            // file -> raw text
  index: null,          // [{part,pname,no,vtitle,file,hid,head,text}]
  indexing: false,
  indexed: 0,
  nav: [],              // 平铺导航 [{part,no,file,hid,label,isCh}]
  navPos: -1,
  annos: [],            // 注解
  applied: {},          // 每次渲染标记
  quote: '',            // 待问 AI 的引用
  cfg: null,            // 大模型配置
  pendingAnchor: null
};

var $ = function (s) { return document.querySelector(s); };
var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function toast(msg, ms) {
  var t = $('#toast');
  t.textContent = msg;
  t.classList.remove('hidden');
  clearTimeout(t._tm);
  t._tm = setTimeout(function () { t.classList.add('hidden'); }, ms || 1800);
}
function store(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
function load(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }

/* 是否手机端（与 CSS 断点一致） */
function isMobile() { return window.matchMedia('(max-width: 820px)').matches; }

/* ---------- Markdown 渲染 ---------- */
/* 标题 id 规则与 catalog.js 完全一致：
   ## 开头且以"第"起 → 计入；### 开头且不以"本章"起 → 计入；顺序编号 h0,h1… */
function isCatHeading(line) {
  if (line.indexOf('## ') === 0 && /^第/.test(line.slice(3).trim())) return 2;
  if (line.indexOf('### ') === 0 && line.slice(4).trim().indexOf('本章') !== 0) return 3;
  return 0;
}

function inline(s) {
  s = esc(s);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
  s = s.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<i>$2</i>');
  s = s.replace(/\$\$([^$]+)\$\$/g, '<span class="math">$1</span>');
  s = s.replace(/(?<![\\$])\$([^$\n]{1,80}?)\$(?!\$)/g, '<span class="math">$1</span>');
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  return s;
}

function renderMd(raw) {
  var lines = raw.split(/\r?\n/);
  var out = [], i = 0, hid = 0, inCode = false, codeBuf = [], para = [];

  function flushPara() {
    if (para.length) {
      out.push('<p>' + inline(para.join('')) + '</p>');
      para = [];
    }
  }
  function nextHid() { return 'h' + (hid++); }

  while (i < lines.length) {
    var ln = lines[i];

    /* 代码围栏 */
    if (/^\s*```/.test(ln)) {
      flushPara();
      if (!inCode) { inCode = true; codeBuf = []; }
      else {
        inCode = false;
        out.push('<pre><code>' + esc(codeBuf.join('\n')) + '</code></pre>');
      }
      i++; continue;
    }
    if (inCode) { codeBuf.push(ln); i++; continue; }

    /* 标题 */
    var hm = ln.match(/^(#{1,4})\s+(.*)$/);
    if (hm) {
      flushPara();
      var lvl = hm[1].length, txt = hm[2].replace(/#+\s*$/, '').trim();
      var id;
      if (lvl >= 2 && isCatHeading(ln)) id = nextHid();
      else if (lvl === 1) id = 'voltop';
      else id = 'x' + (hid) + '_' + i;
      out.push('<h' + lvl + ' id="' + id + '" class="anchor-target">' + inline(txt) + '</h' + lvl + '>');
      i++; continue;
    }

    /* 水平线 */
    if (/^\s*-{3,}\s*$/.test(ln)) { flushPara(); out.push('<hr>'); i++; continue; }

    /* 表格：本行含 | 且下一行是分隔行 */
    if ((ln.match(/\|/g) || []).length >= 1 && i + 1 < lines.length &&
        /^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$/.test(lines[i + 1]) && lines[i + 1].indexOf('-') >= 0) {
      flushPara();
      var rows = [];
      function cells(row) {
        var r = row.trim().replace(/^\|/, '').replace(/\|$/, '');
        return r.split('|').map(function (c) { return c.trim(); });
      }
      var head = cells(ln);
      i += 2;
      while (i < lines.length && lines[i].indexOf('|') >= 0 && lines[i].trim() !== '') {
        rows.push(cells(lines[i])); i++;
      }
      var tb = ['<table><thead><tr>'];
      head.forEach(function (c) { tb.push('<th>' + inline(c) + '</th>'); });
      tb.push('</tr></thead><tbody>');
      rows.forEach(function (r) {
        tb.push('<tr>');
        head.forEach(function (_, k) { tb.push('<td>' + inline(r[k] || '') + '</td>'); });
        tb.push('</tr>');
      });
      tb.push('</tbody></table>');
      out.push(tb.join(''));
      continue;
    }

    /* 引用 */
    if (/^\s*>\s?/.test(ln)) {
      flushPara();
      var q = [];
      while (i < lines.length && /^\s*>\s?/.test(lines[i])) {
        q.push(lines[i].replace(/^\s*>\s?/, '')); i++;
      }
      out.push('<blockquote>' + inline(q.join('')) + '</blockquote>');
      continue;
    }

    /* 列表（含一级嵌套） */
    var lm = ln.match(/^(\s*)([-*]|\d+[.、])\s+(.*)$/);
    if (lm) {
      flushPara();
      var ordered = /\d/.test(lm[2]);
      var tag = ordered ? 'ol' : 'ul';
      var depth = lm[1].length >= 2 ? 1 : 0;
      var items = [[depth, lm[3]]];
      i++;
      while (i < lines.length) {
        var m2 = lines[i].match(/^(\s*)([-*]|\d+[.、])\s+(.*)$/);
        if (!m2) break;
        items.push([(m2[1].length >= 2 ? 1 : 0), m2[3]]);
        i++;
      }
      var html = '', open0 = false, open1 = false;
      items.forEach(function (it) {
        if (it[0] === 0) {
          if (open1) { html += '</li></' + tag + '>'; open1 = false; }
          if (open0) html += '</li>';
          html += '<li>' + inline(it[1]); open0 = true;
        } else {
          if (!open1) { html += '<' + tag + '>'; open1 = true; }
          html += '<li>' + inline(it[1]) + '</li>';
        }
      });
      if (open1) html += '</li></' + tag + '>';
      if (open0) html += '</li>';
      html += '</' + tag + '>';
      out.push(html);
      continue;
    }

    /* 空行 */
    if (ln.trim() === '') { flushPara(); i++; continue; }

    para.push(ln.trim());
    i++;
  }
  flushPara();
  if (inCode) out.push('<pre><code>' + esc(codeBuf.join('\n')) + '</code></pre>');
  return out.join('\n');
}

/* ---------- 目录侧栏 ---------- */
var PARTCLASS = { '经': 'jing', '史': 'shi', '子': 'zi', '集': 'ji' };

function buildSidebar() {
  var tree = $('#tocTree');
  tree.innerHTML = '';
  S.nav = [];
  window.CATALOG.forEach(function (part) {
    var pb = document.createElement('div');
    pb.className = 'part-block';
    var total = 0;
    part.vols.forEach(function (v) { total += v.w; });
    var head = document.createElement('div');
    head.className = 'part-head ' + PARTCLASS[part.k];
    head.innerHTML = '<span>' + esc(part.n) + '</span><small>' + part.vols.length + '卷 · ' + (total / 10000).toFixed(1) + '万字</small>';
    head.onclick = function () { pb.classList.toggle('open'); };
    pb.appendChild(head);

    var vols = document.createElement('div');
    vols.className = 'part-vols';
    part.vols.forEach(function (v) {
      var vi = document.createElement('div');
      vi.className = 'vol-item';
      vi.dataset.file = v.f;
      var vh = document.createElement('div');
      vh.className = 'vol-head';
      vh.innerHTML = '<span class="arrow">▶</span><span class="vno">' + part.k + v.no + '</span>' +
        '<span class="vt">' + esc(v.t) + '</span><span class="vw">' + (v.w / 10000).toFixed(1) + '万</span>';
      vh.onclick = function (e) {
        var wasOpen = vi.classList.contains('open');
        $$('.vol-item.open').forEach(function (x) { if (x !== vi) x.classList.remove('open'); });
        vi.classList.toggle('open', !wasOpen);
        if (!wasOpen) navigate(part.k, v.no, null);
      };
      var vlabel = null;
      vi.appendChild(vh);

      var chs = document.createElement('div');
      chs.className = 'vol-chs';
      /* 卷首入口 */
      var first = document.createElement('div');
      first.className = 'ch-item';
      first.textContent = '◆ 卷首';
      first.dataset.file = v.f; first.dataset.hid = 'voltop';
      chs.appendChild(first);
      v.chs.forEach(function (c, k) {
        var d = document.createElement('div');
        d.className = 'ch-item' + (/^第/.test(c) ? ' ch' : '');
        d.textContent = c;
        d.dataset.file = v.f; d.dataset.hid = 'h' + k;
        chs.appendChild(d);
        S.nav.push({ part: part.k, no: v.no, file: v.f, hid: 'h' + k, label: c });
      });
      vi.appendChild(chs);
      vols.appendChild(vi);
    });
    pb.appendChild(vols);
    tree.appendChild(pb);
  });
  /* 事件委托：点击章节 */
  tree.addEventListener('click', function (e) {
    var t = e.target.closest('.ch-item');
    if (!t || !t.dataset.hid) return;
    var v = findVol(t.dataset.file);
    if (v) navigate(v.part.k, v.no, t.dataset.hid);
  });
}

function findVol(file) {
  for (var i = 0; i < window.CATALOG.length; i++) {
    var p = window.CATALOG[i];
    for (var j = 0; j < p.vols.length; j++) {
      if (p.vols[j].f === file) return { part: p, vol: p.vols[j] };
    }
  }
  return null;
}

/* ---------- 卷加载与渲染 ---------- */
function volUrl(file) { return '../' + file; }

function loadVol(file, cb) {
  if (S.cache[file]) return cb(null, S.cache[file]);
  /* 优先离线书库（content.js），双击 index.html 也可读 */
  if (window.BOOK && window.BOOK[file]) {
    S.cache[file] = window.BOOK[file];
    return cb(null, S.cache[file]);
  }
  fetch(volUrl(file)).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.text();
  }).then(function (t) {
    S.cache[file] = t;
    addChunks(file, t);
    cb(null, t);
  }).catch(function (e) {
    cb(e);
  });
}

function navigate(part, no, hid) {
  var found = null;
  window.CATALOG.forEach(function (p) {
    if (p.k !== part) return;
    p.vols.forEach(function (v) { if (v.no === no) found = { part: p, vol: v }; });
  });
  if (!found) return toast('未找到该卷');
  var meta = found;
  S.pendingAnchor = hid || null;
  loadVol(meta.vol.f, function (err, raw) {
    if (err) {
      toast('加载失败：' + err.message);
      $('#content').innerHTML = '<div class="empty-hint">无法读取书稿文件。<br>请确认 <code>content.js</code> 离线书库与本页同目录。</div>';
      return;
    }
    showVol(meta, raw);
  });
}

function showVol(meta, raw) {
  S.cur = { part: meta.part.k, pname: meta.part.n, no: meta.vol.no, file: meta.vol.f, title: meta.vol.t };
  S.curHid = S.pendingAnchor || null;
  var html = renderMd(raw);
  $('#content').innerHTML = html;
  /* 宽表格包一层横向滚动，避免撑破手机屏 */
  $$('#content table').forEach(function (t) {
    var w = document.createElement('div');
    w.className = 'tblwrap';
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });
  $('#breadcrumb').innerHTML =
    '<b>' + esc(meta.part.n) + '</b> › 第' + meta.vol.no + '卷 ' + esc(meta.vol.t) +
    ' <span style="opacity:.7">（' + (meta.vol.w / 10000).toFixed(1) + ' 万字）</span>';
  applyAnnos();
  /* 高亮目录当前项 */
  $$('.vol-head').forEach(function (h) {
    var vi = h.closest('.vol-item');
    h.classList.toggle('current', vi && vi.dataset.file === meta.vol.f);
  });
  /* 定位 */
  var ratio = (load('sqk_pos', {}) || {})[meta.vol.f];
  if (S.pendingAnchor && document.getElementById(S.pendingAnchor)) {
    jumpTo(S.pendingAnchor, false);
  } else if (ratio && ratio > 0.02 && ratio < 0.98) {
    var rd = $('#reader');
    rd.scrollTop = ratio * (rd.scrollHeight - rd.clientHeight);
  } else {
    $('#reader').scrollTop = 0;
  }
  S.pendingAnchor = null;
  updateHash();
  loadAIWelcome();
  /* 抽屉模式：选完章节自动收起，正文全宽 */
  closeToc();
  if (isMobile()) {
    aaClose();
    setUI(false);          /* 归来即见工具栏，读者知道自己在哪 */
    $('#pctTxt').textContent = '0%';
  }
  var h0 = $('#content h2[id],#content h3[id]');
  $('#chNow').textContent = h0.length ? (h0[0].textContent || '').trim().replace(/\s+/g, ' ') : '';
}

function jumpTo(hid, flash) {
  var el = document.getElementById(hid);
  if (!el) return;
  el.scrollIntoView({ block: 'start' });
  S.curHid = hid;
  markCurCh(hid);
  if (flash !== false) {
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
  }
  updateHash();
}

function markCurCh(hid) {
  $$('.ch-item.cur').forEach(function (x) { x.classList.remove('cur'); });
  var t = $$('#tocTree .ch-item').filter(function (x) {
    return x.dataset.hid === hid && S.cur && x.dataset.file === S.cur.file;
  })[0];
  if (t) { t.classList.add('cur'); t.scrollIntoView({ block: 'nearest' }); }
}

function updateHash() {
  if (!S.cur) return;
  location.hash = '/' + S.cur.part + '/' + S.cur.no + '/' + (S.curHid || '');
}

function parseHash() {
  var m = location.hash.match(/^#\/([经史子集])\/(\d+)\/?(.*)$/);
  return m ? { part: m[1], no: +m[2], hid: m[3] || null } : null;
}

/* 上一节 / 下一节 */
function navStep(dir) {
  if (!S.cur) return;
  var items = S.nav;
  var pos = -1;
  if (S.curHid && S.curHid !== 'voltop') {
    for (var i = 0; i < items.length; i++) {
      if (items[i].file === S.cur.file && items[i].hid === S.curHid) { pos = i; break; }
    }
  }
  if (pos < 0) {
    /* 当前在卷首：dir>0 进入第一章，dir<0 上一卷卷首 */
    if (dir > 0) {
      var first = items.filter(function (x) { return x.file === S.cur.file; })[0];
      if (first) return navigate(first.part, first.no, first.hid);
    }
    for (var j = 0; j < items.length; j++) { if (items[j].file === S.cur.file) { pos = j; break; } }
    pos = pos - 1;
    if (pos >= 0) return navigate(items[pos].part, items[pos].no, null);
    return;
  }
  var target = items[pos + dir];
  if (!target) return toast(dir > 0 ? '已是最后一节' : '已是卷首');
  navigate(target.part, target.no, target.hid);
}

/* ---------- 全书索引与检索 ---------- */
function stripMd(t) {
  return t.replace(/```[\s\S]*?```/g, ' ').replace(/\|/g, ' ').replace(/[#>*`\-]/g, ' ').replace(/\s+/g, ' ');
}

function addChunks(file, raw) {
  if (!S.index) S.index = [];
  var meta = findVol(file);
  if (!meta) return;
  var lines = raw.split(/\r?\n/);
  var hid = 0, head = '卷首', curHid = 'voltop', buf = [];
  function push() {
    if (!buf.length) return;
    var text = stripMd(buf.join(' ')).trim();
    if (text.length > 10) {
      S.index.push({
        part: meta.part.k, pname: meta.part.n, no: meta.vol.no,
        vtitle: meta.vol.t, file: file, hid: curHid, head: head, text: text
      });
    }
    buf = [];
  }
  for (var i = 0; i < lines.length; i++) {
    var ln = lines[i];
    var lv = isCatHeading(ln);
    if (lv) {
      push();
      head = ln.replace(/^#+\s*/, '').trim();
      curHid = 'h' + (hid++);
      continue;
    }
    if (/^#{1,4}\s/.test(ln)) { push(); head = ln.replace(/^#+\s*/, '').trim(); continue; }
    buf.push(ln);
  }
  push();
  S.indexed++;
  updateIndexStatus();
}

function updateIndexStatus() {
  var el = $('#indexStatus');
  if (S.indexed >= 48) el.textContent = '✓ 全书索引就绪（48 卷 · ' + S.index.length + ' 段）';
  else el.textContent = '后台建索引中… ' + S.indexed + '/48 卷';
}

function prefetch() {
  if (S.indexing) return;
  S.indexing = true;
  var jobs = [];
  window.CATALOG.forEach(function (p) {
    p.vols.forEach(function (v) { jobs.push(v.f); });
  });
  /* 离线书库模式：直接从内存建索引，分批避免卡顿 */
  if (window.BOOK) {
    var k = 0;
    (function step() {
      var t0 = Date.now();
      while (k < jobs.length && Date.now() - t0 < 40) {
        var f = jobs[k++];
        if (!S.cache[f]) { S.cache[f] = window.BOOK[f]; addChunks(f, window.BOOK[f]); }
        else if (S.indexed < 48 || !S.index) addChunks(f, window.BOOK[f]);
      }
      if (k < jobs.length) setTimeout(step, 20);
      else { S.indexing = false; updateIndexStatus(); }
    })();
    return;
  }
  var k2 = 0;
  function step() {
    if (k2 >= jobs.length) { S.indexing = false; updateIndexStatus(); return; }
    var f = jobs[k2++];
    if (!S.cache[f]) {
      loadVol(f, function () { setTimeout(step, 30); });
    } else { addChunks(f, S.cache[f]); setTimeout(step, 10); }
  }
  setTimeout(step, 800);
}

function searchIndex(q) {
  if (!S.index) return [];
  var tokens = q.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!tokens.length) return [];
  var hits = [];
  S.index.forEach(function (c) {
    var low = c.text.toLowerCase();
    var score = 0, ok = true;
    tokens.forEach(function (t) {
      var n = low.split(t).length - 1;
      if (!n) ok = false;
      score += Math.min(n, 20);
    });
    if (ok) hits.push({ c: c, score: score });
  });
  hits.sort(function (a, b) { return b.score - a.score; });
  return hits.slice(0, 60);
}

function snippet(text, tokens) {
  var sents = text.split('。');
  var scored = [];
  sents.forEach(function (s, i) {
    var n = 0;
    tokens.forEach(function (t) { n += Math.min(s.split(t).length - 1, 5); });
    if (n) scored.push({ s: s, n: n, i: i });
  });
  scored.sort(function (a, b) { return b.n - a.n; });
  var picked = scored.slice(0, 3).sort(function (a, b) { return a.i - b.i; });
  var out = picked.map(function (x) { return x.s; }).join('。') || text.slice(0, 160);
  if (out.length > 220) out = out.slice(0, 220) + '…';
  var html = esc(out);
  tokens.forEach(function (t) {
    html = html.replace(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), '<em>$&</em>');
  });
  return html;
}

function runSearch(q) {
  var box = $('#searchResults');
  if (!q.trim()) { box.className = 'empty-hint'; box.textContent = '输入关键词开始检索（支持多个词，空格分隔，须同时命中）'; return; }
  if (!S.index || S.indexed < 48) {
    box.className = 'empty-hint';
    box.textContent = '索引构建中（' + S.indexed + '/48 卷），请稍候一两秒…';
    return;
  }
  var hits = searchIndex(q);
  var tokens = q.trim().toLowerCase().split(/\s+/);
  if (!hits.length) { box.className = 'empty-hint'; box.textContent = '全书未检索到「' + esc(q) + '」'; return; }
  box.className = '';
  box.innerHTML = hits.map(function (h) {
    var c = h.c;
    return '<div class="sr-item" data-file="' + esc(c.file) + '" data-hid="' + esc(c.hid) + '">' +
      '<div class="sr-path">' + esc(c.pname) + ' · 第' + c.no + '卷 ' + esc(c.vtitle) + '</div>' +
      '<div class="sr-head">' + esc(c.head) + '</div>' +
      '<div class="sr-text">' + snippet(c.text, tokens) + '</div></div>';
  }).join('');
}

/* ---------- 注解 ---------- */
function annos() { return S.annos; }

function saveAnnos() { store('sqk_annos', S.annos); renderAnnoList(); }

function applyAnnos() {
  var file = S.cur && S.cur.file;
  var root = $('#content');
  var list = annos().filter(function (a) { return a.vol === file; });
  if (!list.length) return;
  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, null);
  var nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(function (node) {
    var txt = node.nodeValue;
    list.forEach(function (a) {
      if (a._done) return;
      var p = txt.indexOf(a.text);
      if (p >= 0 && a.text.length >= 2) {
        var range = document.createRange();
        range.setStart(node, p);
        range.setEnd(node, p + a.text.length);
        var mk = document.createElement('mark');
        mk.className = 'anno ' + a.color + (a.note ? ' has-note' : '');
        mk.dataset.aid = a.id;
        try { range.surroundContents(mk); a._done = true; } catch (e) {}
      }
    });
  });
  list.forEach(function (a) { delete a._done; });
}

function selBarAction(act, arg) {
  var sel = window.getSelection();
  var text = sel.toString().trim();
  if (act === 'hl' || act === 'note') {
    if (!text || text.length < 2 || !S.cur) return;
    /* 定位选区所在章节：从选区元素向前找最近的带 id 标题 */
    var el = sel.anchorNode && (sel.anchorNode.nodeType === 1 ? sel.anchorNode : sel.anchorNode.parentElement);
    var hid = 'voltop';
    while (el && el.id !== 'content') {
      if (el.id && /^h\d+$|^voltop$/.test(el.id)) { hid = el.id; break; }
      if (el.previousElementSibling) el = el.previousElementSibling;
      else el = el.parentElement;
    }
    var a = {
      id: 'a' + Date.now(), vol: S.cur.file, vtitle: S.cur.title, part: S.cur.part, no: S.cur.no,
      hid: hid, text: text.slice(0, 300), color: arg || 'y', note: '', ts: Date.now()
    };
    if (act === 'note') { S._pendingAnno = a; openNote(a, false); }
    else { S.annos.push(a); saveAnnos(); applyAnnos(); toast('已高亮'); }
    sel.removeAllRanges();
  } else if (act === 'ask') {
    setAIQuote(text);
    sel.removeAllRanges();
  } else if (act === 'copy') {
    copyText(text); sel.removeAllRanges();
  }
  hideSelBar();
}

function copyText(t) {
  if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { toast('已复制'); });
  else toast('复制失败');
}

function openNote(a, editing) {
  $('#noteQuote').textContent = a.text;
  $('#noteText').value = a.note || '';
  $('#noteSave').textContent = editing ? '保存修改' : '保存';
  S._editingId = editing ? a.id : null;
  $('#noteOverlay').classList.remove('hidden');
  var del = $('#noteDelete');
  if (!del) {
    del = document.createElement('button');
    del.id = 'noteDelete'; del.className = 'nav-btn'; del.textContent = '删除高亮';
    del.onclick = function () {
      S.annos = S.annos.filter(function (x) { return x.id !== a.id; });
      saveAnnos(); closeOverlays();
      if (S.cur) navigate(S.cur.part, S.cur.no, S.curHid);
    };
    $('#noteActions').prepend(del);
  }
  del.style.display = '';
  del.classList.toggle('hidden', !editing);
  $('#noteText').focus();
}

function renderAnnoList() {
  var box = $('#annoList');
  $('#annoCount').textContent = S.annos.length || '';
  if (!S.annos.length) { box.className = 'empty-hint'; box.innerHTML = '尚无注解。<br>在正文中选中文字即可高亮或写笔记。'; return; }
  box.className = '';
  box.innerHTML = S.annos.slice().sort(function (a, b) { return b.ts - a.ts; }).map(function (a) {
    return '<div class="anno-item" data-file="' + esc(a.vol) + '" data-hid="' + esc(a.hid) + '" data-aid="' + a.id + '">' +
      '<div class="a-quote">' + esc(a.text.slice(0, 80)) + (a.text.length > 80 ? '…' : '') + '</div>' +
      (a.note ? '<div class="a-note">📝 ' + esc(a.note) + '</div>' : '') +
      '<div class="a-path">' + esc(a.part) + '部第' + a.no + '卷 ' + esc(a.vtitle) + ' · ' + new Date(a.ts).toLocaleDateString() + '</div>' +
      '<button class="a-del" data-del="' + a.id + '">删除</button></div>';
  }).join('');
}

/* ---------- AI 导读 ---------- */
function loadAIWelcome() {
  var chat = $('#aiChat');
  if (chat.children.length) return;
  aiMsg('ai', '我是《AI四库全典》的 AI 导读。\n\n你可以直接问我书里的任何问题——我会从全书 48 卷中检索最相关的段落，给出处、给摘录。\n\n试试问：\n· 什么叫"世界模型的压缩与预测"?\n· RAG 为什么需要向量数据库？\n· 1996 年深蓝是怎么赢卡斯帕罗夫的？');
}

function aiMsg(role, html) {
  var d = document.createElement('div');
  d.className = 'msg ' + role;
  d.innerHTML = html;
  $('#aiChat').appendChild(d);
  $('#aiChat').scrollTop = $('#aiChat').scrollHeight;
  return d;
}

function retrieve(q, k) {
  if (!S.index) return [];
  var tokens = q.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!tokens.length) return [];
  var scored = [];
  S.index.forEach(function (c) {
    var low = c.text.toLowerCase(), n = 0, ok = true;
    tokens.forEach(function (t) {
      var x = low.split(t).length - 1;
      if (!x) ok = false;
      n += Math.min(x, 15);
    });
    if (ok) scored.push({ c: c, n: n + (c.head.toLowerCase().indexOf(tokens[0]) >= 0 ? 8 : 0) });
  });
  scored.sort(function (a, b) { return b.n - a.n; });
  return scored.slice(0, k || 5).map(function (x) { return x.c; });
}

function srcHtml(c, i) {
  return '<span class="src" data-file="' + esc(c.file) + '" data-hid="' + esc(c.hid) + '">' +
    '<i>出处 ' + (i + 1) + ' · ' + esc(c.pname) + ' 第' + c.no + '卷 · ' + esc(c.head) + '</i>' +
    esc(c.text.slice(0, 130)) + '…</span>';
}

function aiAsk(q) {
  if (!q.trim()) return;
  var quoted = S.quote;
  aiMsg('user', esc((quoted ? '【引用】' + quoted.slice(0, 120) + '\n\n' : '') + q));
  S.quote = ''; $('#aiQuote').classList.add('hidden');
  var input = $('#aiInput'); input.value = '';

  if (S.cfg && S.cfg.key) { llmAsk(q, quoted); return; }

  /* 书内检索模式 */
  var thinking = aiMsg('ai think', '正在翻书…');
  setTimeout(function () {
    var srcs = retrieve(q, 5);
    thinking.remove();
    if (!srcs.length) {
      aiMsg('ai', '全书 48 卷中没有检索到与「' + esc(q) + '」直接相关的内容。\n\n试试换几个关键词，或者更具体一点（比如提到人名、年份、术语）。');
      return;
    }
    var html = '在全书里找到 <b>' + srcs.length + '</b> 处最相关的内容：\n' +
      srcs.map(function (c, i) { return srcHtml(c, i); }).join('');
    aiMsg('ai', html);
  }, 350);
}

/* ---------- 大模型传输层 ----------
   安卓 WebView 里的页面来自 file://，targetSdk>=30 时系统禁止其发起跨域请求，
   直接 fetch 任何 https 接口都会以 "Failed to fetch" 收场（且 WebSettings 的
   allowUniversalAccessFromFileURLs 已对该目标版本失效）。APK 内改走原生
   HttpURLConnection 通道，同源策略、CORS 预检全部绕开；桌面浏览器仍用 fetch。 */
var LLM = (function () {
  var seq = 0, jobs = {};

  window.__llmDelta = function (id, chunk) {
    var j = jobs[id];
    if (j && j.onDelta) j.onDelta(chunk || '');
  };
  window.__llmDone = function (id, full) {
    var j = jobs[id];
    if (!j) return;
    delete jobs[id];
    if (j.onDone) j.onDone(full || '');
  };
  window.__llmErr = function (id, msg) {
    var j = jobs[id];
    if (!j) return;
    delete jobs[id];
    if (j.onErr) j.onErr(String(msg || ''));
  };

  function native() {
    try {
      return !!(window.AndroidLLM && window.AndroidLLM.ready && window.AndroidLLM.ready());
    } catch (e) { return false; }
  }

  function pull(json) {
    try {
      var o = JSON.parse(json);
      var c = o.choices && o.choices[0];
      if (!c) return null;
      if (c.delta && typeof c.delta.content === 'string') return c.delta.content;
      if (c.message && typeof c.message.content === 'string') return c.message.content;
      if (typeof c.text === 'string') return c.text;
    } catch (e) {}
    return null;
  }

  /* 桌面路径：流式 fetch（需要接口允许 CORS） */
  function viaFetch(url, key, payload, cbs) {
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) {
        return r.text().then(function (t) {
          var m = '';
          try { m = (JSON.parse(t).error || {}).message || ''; } catch (e) {}
          cbs.onErr('HTTP ' + r.status + '|' + (m || t.slice(0, 200)));
        });
      }
      if (!r.body || !r.body.getReader) {
        return r.text().then(function (t) {
          var one = pull(t.trim());
          if (one == null) { cbs.onErr('EMPTY|' + t.slice(0, 200)); return; }
          cbs.onDelta(one); cbs.onDone(one);
        });
      }
      var reader = r.body.getReader(), dec = new TextDecoder(), buf = '', acc = '';
      function pump() {
        return reader.read().then(function (x) {
          if (x.done) {
            if (!acc) cbs.onErr('EMPTY|无返回内容');
            else cbs.onDone(acc);
            return;
          }
          buf += dec.decode(x.value, { stream: true });
          var lines = buf.split('\n');
          buf = lines.pop();
          lines.forEach(function (l) {
            l = l.trim();
            if (l.indexOf('data:') !== 0) return;
            var p = l.slice(5).trim();
            if (!p || p === '[DONE]') return;
            var d = pull(p);
            if (d) { acc += d; cbs.onDelta(d); }
          });
          return pump();
        });
      }
      return pump();
    }).catch(function (e) {
      var msg = e && e.message ? e.message : String(e);
      if (location.protocol === 'file:') msg = 'CORSBLOCK|' + msg;
      else if (navigator.onLine === false) msg = 'OFFLINE|' + msg;
      cbs.onErr(msg);
    });
  }

  function post(url, key, payload, cbs) {
    if (native()) {
      var id = 'L' + (++seq) + '_' + Date.now();
      jobs[id] = cbs;
      try {
        window.AndroidLLM.chat(id, url, key, JSON.stringify(payload));
      } catch (e) {
        delete jobs[id];
        cbs.onErr('BRIDGE|' + (e && e.message ? e.message : e));
      }
      return;
    }
    viaFetch(url, key, payload, cbs);
  }

  return { post: post, native: native };
})();

/* 把原始错误翻译成人话，附上该去改什么 */
function llmErrText(raw) {
  var s = String(raw || ''), i = s.indexOf('|');
  var head = i < 0 ? s : s.slice(0, i);
  var tail = i < 0 ? '' : s.slice(i + 1);
  var m = /^HTTP\s+(\d{3})/.exec(head);
  if (m) {
    var c = m[1];
    if (c === '400') return '请求被服务端拒绝（400）—— 多为「模型名称」写错，或该模型不支持对话接口。' + (tail ? '\n服务端说：' + tail : '');
    if (c === '401') return 'API Key 无效（401）—— 请重新复制密钥，注意不要带空格或引号。' + (tail ? '\n服务端说：' + tail : '');
    if (c === '403') return '密钥无此接口权限（403）—— 确认已在控制台开通该模型。' + (tail ? '\n服务端说：' + tail : '');
    if (c === '402') return '账户余额不足（402）—— 去控制台充值后再问。';
    if (c === '404') return '接口地址不存在（404）—— 地址通常要以 /chat/completions 结尾。' + (tail ? '\n服务端说：' + tail : '');
    if (c === '429') return '请求过密或额度用尽（429）—— 等一会儿再试。';
    return '服务端返回 HTTP ' + c + (tail ? '：\n' + tail : '');
  }
  if (head === 'CORSBLOCK')
    return '浏览器跨域被拦（这是网页版的限制）。手机上请使用 1.1.1 以上版本的 APK，它走系统原生通道，不会被跨域拦。';
  if (head === 'OFFLINE') return '设备当前没有联网 —— 打开 Wi-Fi 或移动数据后再试。';
  if (head === 'UnknownHostException') return '域名解析失败 —— 接口地址可能敲错了，或当前网络不可达该域名。';
  if (head === 'ConnectException' || head === 'NoRouteToHostException') return '连不上服务器 —— 检查网络，或该域名在当前网络被阻断。';
  if (head === 'SocketTimeoutException') return '连接超时 —— 网络太慢，或接口地址不可达。';
  if (head === 'SSLException' || head === 'SSLHandshakeException' || head === 'CertificateException')
    return 'HTTPS 证书校验失败 —— 请使用 https 开头的正规域名。';
  if (head === 'EMPTY') return '模型没有返回内容：' + tail;
  if (head === 'BRIDGE') return '原生通道调用失败：' + tail;
  return head + (tail ? '（' + tail + '）' : '');
}

function llmAsk(q, quoted) {
  var srcs = retrieve(q, 5);
  var ctx = srcs.map(function (c, i) {
    return '[' + (i + 1) + '] 《' + c.pname + '·第' + c.no + '卷》' + c.head + '\n' + c.text.slice(0, 700);
  }).join('\n\n');
  var sys = '你是《AI四库全典》的 AI 导读。这是一部四部 48 卷的人工智能百科（经：理论根基；史：发展史；子：技术体系；集：应用落地）。' +
    '请用简体中文、口语化但准确地回答用户问题，优先依据下面提供的书中段落，可适当补充常识，但不要编造书里没有的引文。回答控制在 400 字内，并标注你主要参考了哪几处（如 [1][3]）。\n\n书中相关段落：\n' + ctx;
  var history = [];
  $$('#aiChat .msg').forEach(function (m) {
    if (m.classList.contains('user')) history.push({ role: 'user', content: m.textContent });
    else if (m.classList.contains('ai')) history.push({ role: 'assistant', content: m.textContent });
  });
  history = history.slice(-6);
  if (quoted) q = '（用户引用了书中一段话："' + quoted.slice(0, 300) + '"）\n\n' + q;
  history.push({ role: 'user', content: q });

  var bubble = aiMsg('ai', '<span class="think">思考中…</span>');
  var acc = '', painted = false;

  function paint() {
    bubble.innerHTML = esc(acc).replace(/\n/g, '<br>');
    $('#aiChat').scrollTop = $('#aiChat').scrollHeight;
  }
  function appendSrcs() {
    if (srcs.length) bubble.innerHTML += '<br>' + srcs.map(function (c, i) { return srcHtml(c, i); }).join('');
  }

  LLM.post(S.cfg.base, S.cfg.key, {
    model: S.cfg.model,
    messages: [{ role: 'system', content: sys }].concat(history),
    stream: true, temperature: 0.5
  }, {
    onDelta: function (chunk) {
      acc += chunk;
      if (!painted) { bubble.innerHTML = ''; painted = true; }
      paint();
    },
    onDone: function (full) {
      if (!acc && full) acc = full;
      if (!acc) { bubble.innerHTML = '<i>模型返回为空。请检查模型名称是否正确。</i>'; return; }
      paint();
      appendSrcs();
    },
    onErr: function (raw) {
      var fb = retrieve(q, 3);
      bubble.innerHTML = '<b>未能连上大模型。</b><br>' + esc(llmErrText(raw)).replace(/\n/g, '<br>') +
        '<br><br><span class="muted">已退回书内检索，以下是书中相关段落：</span>' +
        (fb.length ? fb.map(function (c, i) { return srcHtml(c, i); }).join('') : '（未检索到）');
    }
  });
}

function setAIQuote(text) {
  S.quote = text;
  var box = $('#aiQuote');
  box.innerHTML = esc(text.slice(0, 150)) + (text.length > 150 ? '…' : '') + '<button id="qDel">×</button>';
  box.classList.remove('hidden');
  $('#qDel').onclick = function () { S.quote = ''; box.classList.add('hidden'); };
  $('#aiPanel').classList.remove('collapsed');
  $('#btnAI').classList.add('on');
  $('#aiInput').focus();
}

/* ---------- 弹窗 / 工具条 ---------- */
function closeOverlays() {
  $$('.overlay').forEach(function (o) { o.classList.add('hidden'); });
  hideSelBar();
}
function hideSelBar() { $('#selBar').classList.add('hidden'); }

/* ---------- 抽屉目录 ---------- */
function tocPinned() { return document.body.classList.contains('toc-pinned'); }
function refreshScrim() {
  var aiOn = $('#aiPanel') && !$('#aiPanel').classList.contains('collapsed');
  var any = document.body.classList.contains('toc-open') ||
    document.body.classList.contains('aa-open') ||
    document.body.classList.contains('sel-open') ||
    aiOn;
  document.body.classList.toggle('scrim', isMobile() && !!any);
}
function openToc() {
  document.body.classList.add('toc-open');
  setUI(false);
  refreshScrim();
}
function closeToc() {
  /* 桌面端固定态不自动收 */
  if (tocPinned() && !isMobile()) { refreshScrim(); return; }
  document.body.classList.remove('toc-open');
  setTimeout(function () {
    if (!isMobile()) document.body.classList.remove('toc-hover');
  }, 120);
  refreshScrim();
}
function toggleToc() {
  if (document.body.classList.contains('toc-open')) closeToc(); else openToc();
}
function toggleTocPin() {
  document.body.classList.toggle('toc-pinned');
  document.body.classList.toggle('toc-open', tocPinned());
  refreshScrim();
}

/* ---------- 沉浸模式（手机：隐显顶栏与工具栏） ---------- */
function setUI(hidden) { document.body.classList.toggle('ui-hidden', !!hidden); }
function toggleUI() { setUI(!document.body.classList.contains('ui-hidden')); }

/* ---------- 排版抽屉 ---------- */
function aaOpen() {
  $('#aaSheet').classList.add('open');
  document.body.classList.add('aa-open');
  setUI(false);
  syncAA(); refreshScrim();
}
function aaClose() {
  $('#aaSheet').classList.remove('open');
  document.body.classList.remove('aa-open');
  refreshScrim();
}
function aaToggle() {
  if ($('#aaSheet').classList.contains('open')) aaClose(); else aaOpen();
}
function syncAA() {
  $('#aaFont').value = S.fsizes[S.fsi];
  $('#aaFontVal').textContent = S.fsizes[S.fsi];
  $('#aaLine').value = Math.round(S.line * 100);
  $('#aaLineVal').textContent = S.line.toFixed(1);
  $('#aaWidth').value = S.cw;
  $('#aaWidthVal').textContent = S.cw;
  var dark = document.documentElement.classList.contains('dark');
  $('#aaDark').textContent = dark ? '开' : '关';
  $('#aaDark').classList.toggle('on', dark);
  $('#aaSwipe').textContent = S.swipe ? '开' : '关';
  $('#aaSwipe').classList.toggle('on', !!S.swipe);
}
function setFsPx(px) {
  var sizes = S.fsizes;
  S.fsi = Math.max(0, Math.min(sizes.length - 1, sizes.indexOf(px) >= 0 ? sizes.indexOf(px) : Math.round((px - sizes[0]) / 2)));
  document.documentElement.style.setProperty('--fs', sizes[S.fsi] + 'px');
  store('sqk_fs', sizes[S.fsi]);
  if ($('#aaSheet').classList.contains('open')) syncAA();
}

/* ---------- 面板统一收起（选完即收） ---------- */
function closePanels() {
  closeToc();
  aaClose();
  hideSelBar();
  if (isMobile()) closeAI();
}
function closeAI() {
  $('#aiPanel').classList.add('collapsed');
  $('#btnAI').classList.remove('on');
  var mb = $$('#mBar button').filter(function (b) { return b.dataset.m === 'ai'; })[0];
  if (mb) mb.classList.remove('on');
  refreshScrim();
}

/* ---------- 初始化 ---------- */
function init() {
  buildSidebar();
  S.annos = load('sqk_annos', []);
  renderAnnoList();
  S.cfg = load('sqk_cfg', null);
  if (S.cfg && S.cfg.key) {
    $('#aiMode').innerHTML = '当前：<b>大模型对话模式</b>（' + esc(S.cfg.model || '') + '）—— AI 会自动检索书中相关段落作为参考。' +
      '<a id="lnkSettings">修改设置</a>';
  }

  /* 主题 / 字号 / 行距 / 版心 */
  if (load('sqk_dark', false)) document.documentElement.classList.add('dark');
  var sizes = [15, 17, 19, 21, 23, 25, 27];
  var defFs = window.innerWidth < 820 ? sizes[1] : sizes[2];
  var fs = load('sqk_fs', defFs);
  if (sizes.indexOf(fs) < 0) fs = defFs;
  S.fsizes = sizes; S.fsi = sizes.indexOf(fs);
  S.line = load('sqk_lh', isMobile() ? 1.95 : 2.0);
  S.cw = load('sqk_cw', 860);
  S.swipe = load('sqk_swipe', true);
  document.documentElement.style.setProperty('--fs', fs + 'px');
  document.documentElement.style.setProperty('--lh', S.line);
  document.documentElement.style.setProperty('--cw', S.cw + 'px');

  /* 手机初始态：AI 面板默认收起，给正文让满屏 */
  if (window.innerWidth < 1100) {
    $('#aiPanel').classList.add('collapsed');
    $('#btnAI').classList.remove('on');
  }

  /* hash 路由 */
  var h = parseHash();
  if (h) navigate(h.part, h.no, h.hid);
  else {
    /* 默认打开经部卷1 */
    navigate('经', 1, null);
  }
  prefetch();
  if (!load('sqk_welcomed', false)) $('#welcome').classList.remove('hidden');
  else $('#welcome').classList.add('hidden');

  bindEvents();
  updateIndexStatus();
}

function bindEvents() {
  /* 侧栏 tab */
  $$('#sidebarTabs .tab').forEach(function (t) {
    t.onclick = function () {
      $$('#sidebarTabs .tab').forEach(function (x) { x.classList.remove('active'); });
      t.classList.add('active');
      $$('.tab-body').forEach(function (b) { b.classList.add('hidden'); });
      $('#tab-' + t.dataset.tab).classList.remove('hidden');
    };
  });

  /* 顶栏：☰ 开合目录（桌面可另用 📌 固定） */
  $('#btnSidebar').onclick = toggleToc;
  $('#btnTocPin').onclick = toggleTocPin;
  /* 桌面：左缘热区滑出目录（手机无悬停，走工具栏） */
  var edge = $('#edgeZone');
  if (edge) edge.addEventListener('mouseenter', function () { if (!isMobile()) openToc(); });
  $('#sidebar').addEventListener('mouseleave', function () {
    if (!isMobile() && !tocPinned()) document.body.classList.remove('toc-open');
  });
  $('#sidebar').addEventListener('mouseenter', function () {
    if (!isMobile() && !tocPinned()) document.body.classList.add('toc-hover');
  });
  /* 遮罩：点空白收起所有面板 */
  $('#scrim').addEventListener('click', function () {
    closeToc(); aaClose(); closeAI();
  });
  $('#btnTheme').onclick = function () {
    var dark = document.documentElement.classList.toggle('dark');
    store('sqk_dark', dark);
  };
  var sizes = S.fsizes;
  function setFs(d) {
    S.fsi = Math.max(0, Math.min(sizes.length - 1, S.fsi + d));
    document.documentElement.style.setProperty('--fs', sizes[S.fsi] + 'px');
    store('sqk_fs', sizes[S.fsi]);
    syncAA();
  }
  $('#btnFontUp').onclick = function () { setFs(1); toast('字号 ' + sizes[S.fsi], 700); };
  $('#btnFontDown').onclick = function () { setFs(-1); toast('字号 ' + sizes[S.fsi], 700); };

  /* 手机底部工具栏 */
  $$('#mBar button').forEach(function (b) {
    b.onclick = function () {
      var m = b.dataset.m;
      if (m === 'toc') {
        if (document.body.classList.contains('toc-open')) closeToc(); else openToc();
        return;
      }
      if (m === 'anno') {
        $$('#sidebarTabs .tab').forEach(function (x) { x.classList.remove('active'); });
        var at = $$('#sidebarTabs .tab').filter(function (x) { return x.dataset.tab === 'anno'; })[0];
        if (at) at.classList.add('active');
        $$('.tab-body').forEach(function (x) { x.classList.add('hidden'); });
        $('#tab-anno').classList.remove('hidden');
        openToc();
        return;
      }
      if (m === 'search') { openSearch(); return; }
      if (m === 'aa') { aaToggle(); return; }
      if (m === 'ai') {
        var p = $('#aiPanel');
        p.classList.toggle('collapsed');
        var on = !p.classList.contains('collapsed');
        $('#btnAI').classList.toggle('on', on);
        b.classList.toggle('on', on);
        if (on) setUI(false);
        refreshScrim();
        return;
      }
    };
  });

  /* 排版抽屉控件 */
  $('#aaClose').onclick = aaClose;
  $('#aaFont').addEventListener('input', function () {
    var v = +this.value;
    document.documentElement.style.setProperty('--fs', v + 'px');
    $('#aaFontVal').textContent = v;
    S.fsi = Math.max(0, Math.min(S.fsizes.length - 1, Math.round((v - S.fsizes[0]) / 2)));
    store('sqk_fs', S.fsizes[S.fsi]);
  });
  $('#aaLine').addEventListener('input', function () {
    S.line = +this.value / 100;
    document.documentElement.style.setProperty('--lh', S.line);
    $('#aaLineVal').textContent = S.line.toFixed(1);
    store('sqk_lh', S.line);
  });
  $('#aaWidth').addEventListener('input', function () {
    S.cw = +this.value;
    document.documentElement.style.setProperty('--cw', S.cw + 'px');
    $('#aaWidthVal').textContent = S.cw;
    store('sqk_cw', S.cw);
  });
  $('#aaDark').onclick = function () {
    var dark = document.documentElement.classList.toggle('dark');
    store('sqk_dark', dark);
    syncAA();
  };
  $('#aaSwipe').onclick = function () {
    S.swipe = !S.swipe;
    store('sqk_swipe', S.swipe);
    syncAA();
    toast(S.swipe ? '左右滑翻节：开' : '左右滑翻节：关', 900);
  };

  /* AI 面板开关 */
  function aiTabBtn() { return $$('#mBar button').filter(function (b) { return b.dataset.m === 'ai'; })[0]; }
  $('#btnAI').onclick = function () {
    var p = $('#aiPanel');
    p.classList.toggle('collapsed');
    var on = !p.classList.contains('collapsed');
    $('#btnAI').classList.toggle('on', on);
    if (aiTabBtn()) aiTabBtn().classList.toggle('on', on);
    if (on) setUI(false);
    refreshScrim();
  };
  $('#btnAIClose').onclick = closeAI;
  $('#btnAISend').onclick = function () { aiAsk($('#aiInput').value); };
  $('#aiInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); aiAsk(this.value); }
  });

  /* AI 设置 */
  var PRESETS = {
    deepseek: { base: 'https://api.deepseek.com/chat/completions', model: 'deepseek-chat' },
    qwen: { base: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', model: 'qwen-plus' },
    zhipu: { base: 'https://open.bigmodel.cn/api/paas/v4/chat/completions', model: 'glm-4-flash' },
    moonshot: { base: 'https://api.moonshot.cn/v1/chat/completions', model: 'moonshot-v1-8k' },
    openai: { base: 'https://api.openai.com/v1/chat/completions', model: 'gpt-4o-mini' }
  };
  function openCfg() {
    var c = S.cfg || {};
    $('#cfgBase').value = c.base || 'https://api.deepseek.com/chat/completions';
    $('#cfgKey').value = c.key || '';
    $('#cfgModel').value = c.model || '';
    $('#cfgTestOut').textContent = '';
    $('#cfgTestOut').className = '';
    $('#cfgOverlay').classList.remove('hidden');
  }
  $$('#cfgPanel .cfg-presets button').forEach(function (b) {
    b.onclick = function () {
      var p = PRESETS[b.dataset.p];
      if (!p) return;
      $('#cfgBase').value = p.base;
      $('#cfgModel').value = p.model;
      $('#cfgTestOut').textContent = '已填入 ' + b.textContent + ' 的地址与模型，填上你的 Key 即可';
      $('#cfgTestOut').className = '';
      $('#cfgKey').focus();
    };
  });
  $('#cfgTest').onclick = function () {
    var base = $('#cfgBase').value.trim(), key = $('#cfgKey').value.trim(), model = $('#cfgModel').value.trim();
    var out = $('#cfgTestOut');
    if (!base || !key || !model) { out.className = 'bad'; out.textContent = '三项都要填'; return; }
    out.className = '';
    out.textContent = '连接中…';
    var t0 = Date.now();
    LLM.post(base, key, {
      model: model,
      messages: [{ role: 'user', content: '回复两个字：可以' }],
      stream: false, max_tokens: 16
    }, {
      onDelta: function () {},
      onDone: function (full) {
        var s = ((Date.now() - t0) / 1000).toFixed(1);
        out.className = 'ok';
        out.textContent = '连接正常（' + s + 's）' + (full ? '：' + String(full).replace(/\s+/g, ' ').slice(0, 20) : '');
      },
      onErr: function (raw) {
        out.className = 'bad';
        out.textContent = llmErrText(raw).split('\n')[0];
      }
    });
  };
  $('#btnAISettings').onclick = openCfg;
  document.addEventListener('click', function (e) {
    if (e.target.id === 'lnkSettings') openCfg();
  });
  $('#cfgCancel').onclick = closeOverlays;
  $('#cfgSave').onclick = function () {
    var base = $('#cfgBase').value.trim(), key = $('#cfgKey').value.trim(), model = $('#cfgModel').value.trim();
    if (!base || !key || !model) return toast('三项都要填');
    S.cfg = { base: base, key: key, model: model };
    store('sqk_cfg', S.cfg);
    $('#aiMode').innerHTML = '当前：<b>大模型对话模式</b>（' + esc(model) + '）—— AI 会自动检索书中相关段落作为参考。<a id="lnkSettings">修改设置</a>';
    closeOverlays(); toast('已接入大模型，可以自由对话了');
  };

  /* AI 消息内出处点击（事件委托） */
  $('#aiChat').addEventListener('click', function (e) {
    var s = e.target.closest('.src');
    if (!s) return;
    var v = findVol(s.dataset.file);
    if (v) {
      navigate(v.part.k, v.no, s.dataset.hid);
      if (isMobile()) closeAI();   /* 手机上跳到原文即收起 AI，直接看内容 */
    }
  });

  /* 搜索 */
  var sTimer = null;
  function openSearch() {
    $('#searchOverlay').classList.remove('hidden');
    $('#searchPanelInput').focus();
    $('#searchPanelInput').select();
  }
  $('#searchInput').onclick = openSearch;
  $('#searchPanelInput').addEventListener('input', function () {
    var v = this.value;
    clearTimeout(sTimer);
    sTimer = setTimeout(function () { runSearch(v); }, 250);
  });
  $('#searchPanelInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') runSearch(this.value);
  });
  $('#searchResults').addEventListener('click', function (e) {
    var it = e.target.closest('.sr-item');
    if (!it) return;
    var v = findVol(it.dataset.file);
    if (v) { navigate(v.part.k, v.no, it.dataset.hid); closeOverlays(); }
  });

  /* 注解列表 */
  $('#annoList').addEventListener('click', function (e) {
    var del = e.target.closest('.a-del');
    if (del) {
      S.annos = S.annos.filter(function (x) { return x.id !== del.dataset.del; });
      saveAnnos();
      if (S.cur) navigate(S.cur.part, S.cur.no, S.curHid);
      return;
    }
    var it = e.target.closest('.anno-item');
    if (!it) return;
    var v = findVol(it.dataset.file);
    if (v) navigate(v.part.k, v.no, it.dataset.hid);
  });

  /* 笔记弹窗 */
  $('#noteCancel').onclick = closeOverlays;
  $('#noteSave').onclick = function () {
    if (S._pendingAnno) {
      S._pendingAnno.note = $('#noteText').value.trim();
      S.annos.push(S._pendingAnno);
      S._pendingAnno = null;
      saveAnnos(); applyAnnos(); closeOverlays(); toast('笔记已保存');
    } else if (S._editingId) {
      var a = S.annos.filter(function (x) { return x.id === S._editingId; })[0];
      if (a) {
        a.note = $('#noteText').value.trim();
        saveAnnos(); closeOverlays();
        if (S.cur) navigate(S.cur.part, S.cur.no, S.curHid);
        toast('笔记已更新');
      }
      S._editingId = null;
    }
  };

  /* 选中工具条 */
  function placeSelBar() {
    var sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) { hideSelBar(); return; }
    var content = $('#content');
    if (!content.contains(sel.anchorNode)) { hideSelBar(); return; }
    var bar = $('#selBar');
    bar.classList.remove('hidden');
    if (isMobile()) return;   /* 手机：贴底整条，位置由 CSS 定；键盘弹起时也不会被挡 */
    var rect = sel.getRangeAt(0).getBoundingClientRect();
    bar.style.top = Math.max(60, rect.top - 48) + 'px';
    bar.style.left = Math.max(10, rect.left + rect.width / 2 - 120) + 'px';
  }
  document.addEventListener('mouseup', function (e) {
    if (e.target.closest('#selBar')) return;
    setTimeout(placeSelBar, 10);
  });
  /* 手机：选择变化即出工具条（长按选词不会触发 mouseup） */
  var selTimer = null;
  document.addEventListener('selectionchange', function () {
    if (!isMobile()) return;
    clearTimeout(selTimer);
    selTimer = setTimeout(function () {
      var sel = window.getSelection();
      if (sel && !sel.isCollapsed && sel.toString().trim().length > 1) placeSelBar();
    }, 260);
  });
  $('#selBar').addEventListener('mousedown', function (e) { e.preventDefault(); });
  $('#selBar').addEventListener('touchstart', function (e) { e.stopPropagation(); }, { passive: true });
  $('#selBar').addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.color) selBarAction('hl', b.dataset.color);
    else selBarAction(b.dataset.act);
  });

  /* 点击正文中的高亮 → 编辑 */
  $('#content').addEventListener('click', function (e) {
    var mk = e.target.closest('mark.anno');
    if (!mk) return;
    var a = S.annos.filter(function (x) { return x.id === mk.dataset.aid; })[0];
    if (a) { S._pendingAnno = null; openNote(a, true); }
  });

  /* 导航 */
  $('#btnPrev').onclick = function () { navStep(-1); };
  $('#btnNext').onclick = function () { navStep(1); };
  $('#btnTop').onclick = function () { $('#reader').scrollTop = 0; };

  /* 阅读进度 + 顶栏随滚动隐退 + 当前章名 */
  var lastSave = 0, lastY = 0, spyTimer = null;
  $('#reader').addEventListener('scroll', function () {
    var rd = $('#reader');
    var max = rd.scrollHeight - rd.clientHeight;
    var r = max > 0 ? rd.scrollTop / max : 0;
    $('#progressBar').style.width = (r * 100).toFixed(1) + '%';
    $('#pctTxt').textContent = Math.round(r * 100) + '%';

    /* 手机：下滑藏顶栏，上滑显 */
    if (isMobile()) {
      var y = rd.scrollTop;
      if (y > lastY + 14 && y > 90) setUI(true);
      else if (y < lastY - 10) setUI(false);
      lastY = y;
    }
    /* 滚动定位当前章（节流 200ms） */
    clearTimeout(spyTimer);
    spyTimer = setTimeout(updateSpy, 200);

    var now = Date.now();
    if (S.cur && now - lastSave > 800) {
      lastSave = now;
      var pos = load('sqk_pos', {}); pos[S.cur.file] = r; store('sqk_pos', pos);
    }
  });

  /* 滚动反查当前所在章，写入顶栏小字 */
  function updateSpy() {
    var heads = $$('#content h2[id],#content h3[id]');
    if (!heads.length) return;
    var top = $('#reader').getBoundingClientRect().top + (isMobile() ? 56 : 0);
    var curEl = heads[0];
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top <= top + 40) curEl = heads[i]; else break;
    }
    var t = (curEl.textContent || '').trim().replace(/\s+/g, ' ');
    $('#chNow').textContent = t;
    if (t && S.curHid !== curEl.id) { S.curHid = curEl.id; markCurCh(curEl.id); }
  }

  /* ===== 手机手势层：左右滑翻节 / 捏合调字号 / 点按沉浸 ===== */
  (function bindGestures() {
    var rd = $('#reader');
    var tg = { x: 0, y: 0, t: 0, on: false, skip: false, moved: false };
    var pn = { on: false, d0: 0, fs0: 0 };

    function dist(t) {
      var dx = t[0].clientX - t[1].clientX, dy = t[0].clientY - t[1].clientY;
      return Math.sqrt(dx * dx + dy * dy);
    }

    rd.addEventListener('touchstart', function (e) {
      if (e.touches.length === 2) {
        pn.on = true; pn.d0 = dist(e.touches); pn.fs0 = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--fs')) || 17;
        tg.on = false;
        return;
      }
      if (e.touches.length !== 1) { tg.on = false; return; }
      var t = e.touches[0];
      tg.x = t.clientX; tg.y = t.clientY; tg.t = Date.now();
      tg.moved = false; tg.on = true;
      /* 表格横向滚动、代码块、可编辑区不参与翻章 */
      tg.skip = !!(e.target.closest && e.target.closest('.tblwrap,pre,input,textarea,mark.anno,#selBar'));
    }, { passive: true });

    rd.addEventListener('touchmove', function (e) {
      if (pn.on && e.touches.length === 2) {
        var r = dist(e.touches) / (pn.d0 || 1);
        var px = Math.max(13, Math.min(30, pn.fs0 * r));
        document.documentElement.style.setProperty('--fs', px.toFixed(1) + 'px');
        e.preventDefault();
        return;
      }
      if (!tg.on || e.touches.length !== 1) return;
      var t = e.touches[0];
      if (Math.abs(t.clientX - tg.x) > 8 || Math.abs(t.clientY - tg.y) > 8) tg.moved = true;
    }, { passive: false });

    rd.addEventListener('touchend', function (e) {
      /* 捏合结束：吸附到最近档位 */
      if (pn.on && e.touches.length === 0) {
        pn.on = false;
        var px = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--fs')) || 17;
        var best = S.fsizes[0];
        S.fsizes.forEach(function (v) { if (Math.abs(v - px) < Math.abs(best - px)) best = v; });
        document.documentElement.style.setProperty('--fs', best + 'px');
        S.fsi = S.fsizes.indexOf(best);
        store('sqk_fs', best);
        syncAA();
        toast('字号 ' + best, 800);
        return;
      }
      if (!tg.on) return;
      tg.on = false;
      var t = e.changedTouches[0];
      var dx = t.clientX - tg.x, dy = t.clientY - tg.y, dt = Date.now() - tg.t;
      if (window.getSelection && String(window.getSelection()).trim()) return;   /* 正在选字 */

      /* 左右滑翻节 */
      if (S.swipe !== false && !tg.skip && dt < 800 && Math.abs(dx) >= 64 && Math.abs(dx) > Math.abs(dy) * 1.8) {
        if (dx < 0) { navStep(1); toast('下一节 →', 700); }
        else if (tg.x > 34) { navStep(-1); toast('← 上一节', 700); }   /* 左缘右滑让给系统返回手势 */
        return;
      }

      /* 点按正文中央：隐显工具栏 */
      if (!tg.skip && !tg.moved && dt < 320) {
        toggleUI();
        if (!document.body.classList.contains('ui-hidden')) { /* 显出来 */ }
      }
    }, { passive: true });

    /* 双指捏合阻止页面缩放（部分 WebView 仍会缩放） */
    document.addEventListener('gesturestart', function (e) { e.preventDefault(); }, { passive: false });
  })();

  /* 安卓返回键：先关面板，再退历史 */
  window.__sqkBack = function () {
    try {
      if (!$('#welcome').classList.contains('hidden')) {
        $('#welcome').classList.add('hidden'); store('sqk_welcomed', true); return true;
      }
      var open = false;
      if ($('#aaSheet').classList.contains('open')) { aaClose(); open = true; }
      if (document.body.classList.contains('toc-open')) { closeToc(); open = true; }
      var ov = $$('.overlay').filter(function (o) {
        return !o.classList.contains('hidden') && o.id !== 'welcome';
      })[0];
      if (ov) { closeOverlays(); open = true; }
      if (isMobile() && !$('#aiPanel').classList.contains('collapsed')) { closeAI(); open = true; }
      return open;
    } catch (e) { return false; }
  };

  /* 断点切换：复位抽屉/遮罩状态 */
  var mq = window.matchMedia('(max-width: 820px)');
  var onMq = function () {
    document.body.classList.remove('scrim');
    if (!mq.matches) { setUI(false); document.body.classList.remove('toc-pinned'); }
    syncAA();
  };
  if (mq.addEventListener) mq.addEventListener('change', onMq);

  /* 欢迎页 */
  $('#welcomeGo').onclick = function () {
    $('#welcome').classList.add('hidden');
    store('sqk_welcomed', true);
  };
  $('#welcome').addEventListener('click', function (e) {
    if (e.target === this) { this.classList.add('hidden'); store('sqk_welcomed', true); }
  });

  /* 遮罩点击空白关闭 */
  $$('.overlay').forEach(function (o) {
    o.addEventListener('mousedown', function (e) {
      if (e.target === o && o.id !== 'welcome') closeOverlays();
    });
  });

  /* 键盘 */
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'm') { e.preventDefault(); toggleTocPin(); }
    if (e.key === 'Escape') closeOverlays();
  });
}

document.addEventListener('DOMContentLoaded', init);
