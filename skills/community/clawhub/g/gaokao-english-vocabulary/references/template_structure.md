# HTML Template Structure

This is the complete HTML template for the Gaokao English Vocabulary Frequency Grading System. Copy this template and customize the data file path, thresholds, and content as needed.

## Template

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>高考英语词汇频率分级系统（完整3500词+真题扩展）</title>
<script src="vocab_data.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#c9d1d9;font-family:'Segoe UI','Microsoft YaHei',Arial,sans-serif;min-height:100vh}

/* === Sticky Top Bar === */
.top-bar{
  position:sticky;top:0;z-index:100;
  background:linear-gradient(135deg,#1a1f2e 0%,#0d1117 100%);
  border-bottom:1px solid #21262d;
  backdrop-filter:blur(12px);
}
.top-inner{max-width:1440px;margin:0 auto;padding:18px 32px 14px}
.header h1{font-size:1.5rem;color:#58a6ff;margin-bottom:2px;display:flex;align-items:center;gap:8px;justify-content:center}
.header p{color:#8b949e;font-size:0.85rem;text-align:center;margin-bottom:12px}
.stats-bar{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:12px}
.stat{background:#161b22;padding:5px 14px;border-radius:20px;font-size:0.78rem;border:1px solid #30363d}
.stat span{color:#58a6ff;font-weight:bold}

/* === Search === */
.search-row{display:flex;justify-content:center;margin-bottom:10px}
.search-box{position:relative;width:100%;max-width:420px}
.search-box input{width:100%;background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:8px 12px 8px 36px;color:#c9d1d9;font-size:0.9rem;outline:none;transition:border-color 0.2s}
.search-box input:focus{border-color:#58a6ff}
.search-icon{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:#6e7681;font-size:1rem}

/* === Filter Buttons with Frequency Annotations === */
.filter-row{display:flex;gap:6px;justify-content:center;flex-wrap:wrap}
.filter-btn{padding:5px 11px;background:#21262d;border:1px solid #30363d;border-radius:16px;color:#8b949e;cursor:pointer;font-size:0.75rem;transition:all 0.2s;white-space:nowrap;line-height:1.4}
.filter-btn:hover{border-color:#58a6ff;color:#58a6ff}
.filter-btn.active{background:#1f6feb;border-color:#58a6ff;color:#fff}
.filter-btn small{font-size:0.62rem;color:#6e7681;display:block;line-height:1}
.filter-btn:hover small,.filter-btn.active small{color:inherit;opacity:0.7}
.filter-sep{width:1px;background:#30363d;margin:0 4px}

/* === Main Content === */
.main{padding:20px 32px;max-width:1440px;margin:0 auto}
.level-section{margin-bottom:24px}

/* === Sticky Level Headers === */
.level-header{display:flex;align-items:center;gap:12px;padding:10px 16px;border-radius:8px;cursor:pointer;margin-bottom:12px;transition:0.2s;user-select:none;position:sticky;top:0;z-index:50;box-shadow:0 2px 8px rgba(0,0,0,0.3)}
.level-header:hover{filter:brightness(1.15)}
.level-title{font-size:0.95rem;font-weight:600}
.level-count{background:rgba(255,255,255,0.1);padding:2px 10px;border-radius:10px;font-size:0.78rem;color:rgba(255,255,255,0.7)}
.collapse-icon{margin-left:auto;font-size:0.8rem;transition:0.3s;color:rgba(255,255,255,0.5)}
.level-body{overflow:hidden;transition:max-height 0.4s ease}

/* === Word Card Grid === */
.word-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.word-card{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px 16px;transition:all 0.2s;position:relative;overflow:hidden}
.word-card:hover{border-color:#58a6ff;transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,0.3)}
.word-card.wrong-word{border-left:3px solid #9e6de6}
.word-bar{position:absolute;top:0;left:0;height:3px;border-radius:2px 0 0 0;transition:width 0.3s}
.word-top{display:flex;align-items:baseline;gap:8px;margin-bottom:6px;flex-wrap:wrap}
.word-text{font-size:1.1rem;font-weight:700;color:#e6edf3}
.word-pos{font-size:0.72rem;color:#8b949e;background:#21262d;padding:1px 6px;border-radius:4px}
.word-phonetic{font-size:0.78rem;color:#6e7681;font-style:italic}
.word-meaning{font-size:0.86rem;color:#c9d1d9;margin-bottom:6px;line-height:1.5}
.meaning-item{display:inline;margin-right:12px}
.meaning-count{font-size:0.72rem;color:#6e7681;margin-left:2px}
.word-footer{display:flex;align-items:center;gap:8px;flex-wrap:wrap}

/* === Mastery Badges === */
.mastery-badge{font-size:0.7rem;padding:2px 8px;border-radius:10px;font-weight:600}
.m145{background:#1a3a2a;color:#3fb950;border:1px solid #238636}
.mmust{background:#1c2128;color:#d29922;border:1px solid #9e6a03}
.mnormal{background:#21262d;color:#8b949e;border:1px solid #30363d}
.mknow{background:#161b22;color:#6e7681;border:1px solid #21262d}
.count-badge{font-size:0.7rem;color:#6e7681;margin-left:auto}
.wrong-tip{font-size:0.75rem;color:#c084fc;background:#1a1030;border-radius:4px;padding:4px 8px;margin-top:6px;border-left:2px solid #9e6de6;line-height:1.4}

/* === Word 6-Level Colors === */
.level-1 .level-header{background:linear-gradient(90deg,#1a2a1a,#161b22);border:1px solid #238636}
.level-1 .level-title{color:#3fb950}
.level-1 .word-bar{background:#3fb950}
.level-2 .level-header{background:linear-gradient(90deg,#1a2a3a,#161b22);border:1px solid #1f6feb}
.level-2 .level-title{color:#58a6ff}
.level-2 .word-bar{background:#58a6ff}
.level-3 .level-header{background:linear-gradient(90deg,#2a2a1a,#161b22);border:1px solid #9e6a03}
.level-3 .level-title{color:#e3b341}
.level-3 .word-bar{background:#e3b341}
.level-4 .level-header{background:linear-gradient(90deg,#2a1a1a,#161b22);border:1px solid #b91c1c}
.level-4 .level-title{color:#f85149}
.level-4 .word-bar{background:#f85149}
.level-5 .level-header{background:linear-gradient(90deg,#2a1a2a,#161b22);border:1px solid #6e40c9}
.level-5 .level-title{color:#a371f7}
.level-5 .word-bar{background:#a371f7}
.level-6 .level-header{background:linear-gradient(90deg,#1a1a1a,#161b22);border:1px solid #484f58}
.level-6 .level-title{color:#8b949e}
.level-6 .word-bar{background:#484f58}

/* === Phrase 6-Level Colors === */
.level-p1 .level-header{background:linear-gradient(90deg,#0d2a2a,#161b22);border:1px solid #0891b2}
.level-p1 .level-title{color:#38bdf8}
.level-p1 .word-bar{background:#38bdf8}
.level-p2 .level-header{background:linear-gradient(90deg,#0d2025,#161b22);border:1px solid #0e7490}
.level-p2 .level-title{color:#22d3ee}
.level-p2 .word-bar{background:#22d3ee}
.level-p3 .level-header{background:linear-gradient(90deg,#0d1a25,#161b22);border:1px solid #0369a1}
.level-p3 .level-title{color:#38bdf8}
.level-p3 .word-bar{background:#38bdf8}
.level-p4 .level-header{background:linear-gradient(90deg,#0d1520,#161b22);border:1px solid #075985}
.level-p4 .level-title{color:#7dd3fc}
.level-p4 .word-bar{background:#7dd3fc}
.level-p5 .level-header{background:linear-gradient(90deg,#0d1218,#161b22);border:1px solid #0c4a6e}
.level-p5 .level-title{color:#93c5fd}
.level-p5 .word-bar{background:#93c5fd}
.level-p6 .level-header{background:linear-gradient(90deg,#0d1015,#161b22);border:1px solid #1e3a5f}
.level-p6 .level-title{color:#94a3b8}
.level-p6 .word-bar{background:#94a3b8}

.no-result{text-align:center;padding:60px;color:#6e7681;font-size:1rem}
.no-result span{font-size:3rem;display:block;margin-bottom:12px}
.loading{text-align:center;padding:60px;color:#58a6ff;font-size:1.1rem}

@media(max-width:600px){
.main{padding:12px 16px}
.top-inner{padding:14px 16px 10px}
.header h1{font-size:1.2rem}
.word-grid{grid-template-columns:1fr}
.filter-btn{font-size:0.68rem;padding:4px 8px}
}
</style>
</head>
<body>

<div class="top-bar">
  <div class="top-inner">
    <div class="header">
      <h1>📚 高考英语词汇频率分级系统</h1>
      <p>{{SUBTITLE}}</p>
      <!-- Optional signature line -->
      <!-- <p style="color:#484f58;font-size:0.72rem;text-align:center;margin-bottom:4px">{{AUTHOR}}</p> -->
    </div>
    <div class="stats-bar" id="statsBar">
      <div class="stat">总词汇 <span id="totalCount">—</span></div>
      <div class="stat">单词 <span id="cntWord">—</span></div>
      <div class="stat">词组 <span id="cntPhrase">—</span></div>
      <div class="stat">🔥 <span id="cnt145">—</span> 个145分必掌握</div>
      <div class="stat">⚠️ <span id="cntWrong">—</span> 个易错</div>
    </div>
    <div class="search-row">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" placeholder="搜索单词、词义、音标…" oninput="doSearch()">
      </div>
    </div>
    <div class="filter-row">
      <button class="filter-btn active" onclick="setFilter('all',this)">全部</button>
      <button class="filter-btn" onclick="setFilter('lv1',this)">🟢 Lv.1超高频<br><small>≥40次</small></button>
      <button class="filter-btn" onclick="setFilter('lv2',this)">🔵 Lv.2高频<br><small>20-39次</small></button>
      <button class="filter-btn" onclick="setFilter('lv3',this)">🟡 Lv.3次高频<br><small>10-19次</small></button>
      <button class="filter-btn" onclick="setFilter('lv4',this)">🔴 Lv.4中频<br><small>5-9次</small></button>
      <button class="filter-btn" onclick="setFilter('lv5',this)">🟣 Lv.5低频<br><small>2-4次</small></button>
      <button class="filter-btn" onclick="setFilter('lv6',this)">⚫ Lv.6超低频<br><small>0-1次</small></button>
      <div class="filter-sep"></div>
      <button class="filter-btn" onclick="setFilter('phr',this)">📌 全部词组</button>
      <button class="filter-btn" onclick="setFilter('phr1',this)">📌 词组Lv.1<br><small>≥20次</small></button>
      <button class="filter-btn" onclick="setFilter('phr2',this)">📌 词组Lv.2<br><small>12-19次</small></button>
      <button class="filter-btn" onclick="setFilter('phr3',this)">📌 词组Lv.3<br><small>8-11次</small></button>
      <button class="filter-btn" onclick="setFilter('phr4',this)">📌 词组Lv.4<br><small>5-7次</small></button>
      <button class="filter-btn" onclick="setFilter('phr5',this)">📌 词组Lv.5<br><small>3-4次</small></button>
      <button class="filter-btn" onclick="setFilter('phr6',this)">📌 词组Lv.6<br><small>1-2次</small></button>
      <div class="filter-sep"></div>
      <button class="filter-btn" onclick="setFilter('145',this)">🔥 145必掌握</button>
      <button class="filter-btn" onclick="setFilter('wrong',this)">⚠️ 易错</button>
    </div>
  </div>
</div>

<div class="main" id="mainContent"><div class="loading">⏳ 正在加载词汇数据...</div></div>

<script>
var currentFilter = 'all';
var currentSearch = '';

var LEVEL_NAMES = {
  1: {name:"🟢 Lv.1 超高频（≥40次考查）", cls:"level-1"},
  2: {name:"🔵 Lv.2 高频（20-39次考查）", cls:"level-2"},
  3: {name:"🟡 Lv.3 次高频（10-19次考查）", cls:"level-3"},
  4: {name:"🔴 Lv.4 中频（5-9次考查）", cls:"level-4"},
  5: {name:"🟣 Lv.5 低频（2-4次考查）", cls:"level-5"},
  6: {name:"⚫ Lv.6 超低频（0-1次考查）", cls:"level-6"},
  'p1': {name:"📌 词组 Lv.1 超高频（≥20次考查）", cls:"level-p1"},
  'p2': {name:"📌 词组 Lv.2 高频（12-19次考查）", cls:"level-p2"},
  'p3': {name:"📌 词组 Lv.3 次高频（8-11次考查）", cls:"level-p3"},
  'p4': {name:"📌 词组 Lv.4 中频（5-7次考查）", cls:"level-p4"},
  'p5': {name:"📌 词组 Lv.5 低频（3-4次考查）", cls:"level-p5"},
  'p6': {name:"📌 词组 Lv.6 超低频（1-2次考查）", cls:"level-p6"}
};

var DISPLAY_ORDER = [1,2,3,4,5,6,'p1','p2','p3','p4','p5','p6'];

function getLevel(w) {
  if (w.s === 'phr.') {
    var c = getMaxCount(w);
    if (c >= 20) return 'p1';
    if (c >= 12) return 'p2';
    if (c >= 8) return 'p3';
    if (c >= 5) return 'p4';
    if (c >= 3) return 'p5';
    return 'p6';
  }
  return w.l;
}

function getMaxCount(w) {
  if (w.s === 'phr.') return w.c || 0;
  var mx = 0;
  if (w.d) {
    for (var i = 0; i < w.d.length; i++) {
      if (w.d[i].c > mx) mx = w.d[i].c;
    }
  }
  return mx;
}

function getMasteryClass(m) {
  if (m === '145') return 'mastery-badge m145';
  if (m === 'must') return 'mastery-badge mmust';
  if (m === 'normal') return 'mastery-badge mnormal';
  return 'mastery-badge mknow';
}
function getMasteryLabel(m) {
  if (m === '145') return '🔥 145分必掌握';
  if (m === 'must') return '✅ 必须掌握';
  if (m === 'normal') return '📖 一般掌握';
  return '👀 了解意思';
}

function isPhrase(w) { return w.s === 'phr.'; }

function filterWord(w) {
  var lv = getLevel(w);
  var phr = isPhrase(w);
  switch(currentFilter) {
    case 'lv1': if (lv !== 1 || phr) return false; break;
    case 'lv2': if (lv !== 2 || phr) return false; break;
    case 'lv3': if (lv !== 3 || phr) return false; break;
    case 'lv4': if (lv !== 4 || phr) return false; break;
    case 'lv5': if (lv !== 5 || phr) return false; break;
    case 'lv6': if (lv !== 6 || phr) return false; break;
    case 'phr': if (!phr) return false; break;
    case 'phr1': if (lv !== 'p1') return false; break;
    case 'phr2': if (lv !== 'p2') return false; break;
    case 'phr3': if (lv !== 'p3') return false; break;
    case 'phr4': if (lv !== 'p4') return false; break;
    case 'phr5': if (lv !== 'p5') return false; break;
    case 'phr6': if (lv !== 'p6') return false; break;
    case '145': if (w.v !== '145') return false; break;
    case 'wrong': if (!w.e) return false; break;
  }
  if (currentSearch) {
    var q = currentSearch.toLowerCase();
    var meaningStr = '';
    if (w.d) {
      for (var di = 0; di < w.d.length; di++) {
        meaningStr += w.d[di].m + ' ';
      }
    } else if (w.m) {
      meaningStr = w.m;
    }
    var ok = w.w.toLowerCase().indexOf(q) >= 0 || meaningStr.indexOf(q) >= 0 || (w.p && w.p.toLowerCase().indexOf(q) >= 0);
    if (!ok) return false;
  }
  return true;
}

function escHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function getBarColor(lv) {
  switch(lv) {
    case 1: return '#3fb950'; case 2: return '#58a6ff'; case 3: return '#e3b341';
    case 4: return '#f85149'; case 5: return '#a371f7'; case 6: return '#484f58';
    case 'p1': return '#38bdf8'; case 'p2': return '#22d3ee'; case 'p3': return '#38bdf8';
    case 'p4': return '#7dd3fc'; case 'p5': return '#93c5fd'; case 'p6': return '#94a3b8';
    default: return '#58a6ff';
  }
}

function renderCard(w) {
  var lv = getLevel(w);
  var barColor = getBarColor(lv);
  var maxC = getMaxCount(w);
  var wrongClass = w.e ? ' wrong-word' : '';
  var wrongHtml = w.e && w.t ? '<div class="wrong-tip">⚠️ ' + escHtml(w.t) + '</div>' : '';
  var phoneticHtml = w.p ? ' <span class="word-phonetic">[' + escHtml(w.p) + ']</span>' : '';
  var meaningHtml = '';
  var masteryField = w.v || w.i || 'normal';
  if (w.d && w.d.length > 0) {
    for (var i = 0; i < w.d.length; i++) {
      var item = w.d[i];
      meaningHtml += '<span class="meaning-item">' + escHtml(item.m);
      if (w.d.length > 1) {
        meaningHtml += '<span class="meaning-count">(' + item.c + '次)</span>';
      }
      meaningHtml += '</span>';
    }
  } else if (w.m) {
    meaningHtml = '<span class="meaning-item">' + escHtml(w.m) + '</span>';
  }
  return '<div class="word-card' + wrongClass + '">' +
    '<div class="word-bar" style="width:' + Math.min(100, maxC) + '%;background:' + barColor + '"></div>' +
    '<div class="word-top"><span class="word-text">' + escHtml(w.w) + '</span><span class="word-pos">' + escHtml(w.s) + '</span>' + phoneticHtml + '</div>' +
    '<div class="word-meaning">' + meaningHtml + '</div>' +
    '<div class="word-footer">' +
      '<span class="' + getMasteryClass(masteryField) + '">' + getMasteryLabel(masteryField) + '</span>' +
      '<span class="count-badge">考查' + maxC + '次</span>' +
    '</div>' +
    wrongHtml +
    '</div>';
}

function render() {
  var groups = {};
  for (var i=0;i<DISPLAY_ORDER.length;i++) groups[DISPLAY_ORDER[i]] = [];
  var shown = 0;
  for (var j=0;j<VOCAB.length;j++) {
    var w = VOCAB[j];
    if (filterWord(w)) {
      var lv = getLevel(w);
      if (!groups[lv]) groups[lv] = [];
      groups[lv].push(w);
      shown++;
    }
  }
  var html = '';
  if (shown === 0) {
    html = '<div class="no-result"><span>🔍</span>没有找到匹配的词汇</div>';
  } else {
    for (var oi=0;oi<DISPLAY_ORDER.length;oi++) {
      var lv2 = DISPLAY_ORDER[oi];
      var words = groups[lv2];
      if (!words || words.length === 0) continue;
      var info = LEVEL_NAMES[lv2];
      var cardsHtml = '';
      for (var wi=0;wi<words.length;wi++) {
        cardsHtml += renderCard(words[wi]);
      }
      html += '<div class="level-section ' + info.cls + '">';
      html += '<div class="level-header" onclick="toggleSection(this)">';
      html += '<span class="level-title">' + info.name + '</span>';
      html += '<span class="level-count">' + words.length + ' 词</span>';
      html += '<span class="collapse-icon">▼</span>';
      html += '</div>';
      html += '<div class="level-body" style="max-height:0;overflow:hidden">';
      html += '<div class="word-grid">' + cardsHtml + '</div></div></div>';
    }
  }
  document.getElementById('mainContent').innerHTML = html;
  var firstHeader = document.querySelector('.level-header');
  if (firstHeader) toggleSection(firstHeader);
}

function toggleSection(header) {
  var body = header.nextElementSibling;
  var icon = header.querySelector('.collapse-icon');
  if (body.style.maxHeight && body.style.maxHeight !== '0px') {
    body.style.maxHeight = '0px';
    body.style.overflow = 'hidden';
    icon.textContent = '▼';
  } else {
    body.style.maxHeight = body.scrollHeight + 'px';
    body.style.overflow = 'visible';
    icon.textContent = '▲';
  }
}

function setFilter(f, btn) {
  currentFilter = f;
  var btns = document.querySelectorAll('.filter-btn');
  for (var i=0;i<btns.length;i++) btns[i].classList.remove('active');
  btn.classList.add('active');
  render();
}

function doSearch() {
  currentSearch = document.getElementById('searchInput').value.trim();
  render();
}

function initStats() {
  var total = VOCAB.length, cnt145 = 0, cntWrong = 0, cntPhr = 0;
  for (var i=0;i<VOCAB.length;i++) {
    var vi = VOCAB[i].v || VOCAB[i].i || '';
    if (vi === '145') cnt145++;
    if (VOCAB[i].e) cntWrong++;
    if (VOCAB[i].s === 'phr.') cntPhr++;
  }
  document.getElementById('totalCount').textContent = total;
  document.getElementById('cntWord').textContent = total - cntPhr;
  document.getElementById('cntPhrase').textContent = cntPhr;
  document.getElementById('cnt145').textContent = cnt145;
  document.getElementById('cntWrong').textContent = cntWrong;
}

window.onload = function() {
  if (typeof VOCAB === 'undefined') {
    document.getElementById('mainContent').innerHTML = '<div class="no-result"><span>⚠️</span>词汇数据加载失败，请确保vocab_data.js与本文件在同一目录</div>';
    return;
  }
  initStats();
  render();
};
</script>
</body>
</html>
```

## Customization Placeholders

- `{{SUBTITLE}}` — Replace with description text, e.g., "1977—2025年真题统计 · 完整4000词+真题扩展+806词组 · 智能分级掌握"
- `{{AUTHOR}}` — Optional signature, e.g., "杨继军 2026.03.29"
- Level thresholds in `getLevel()` — Adjust the `>=` boundaries
- Level names in `LEVEL_NAMES` — Update display text and emoji
- CSS level colors — Modify `.level-X` and `.level-pX` classes
