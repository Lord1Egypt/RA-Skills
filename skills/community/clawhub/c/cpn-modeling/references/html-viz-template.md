# HTML 可视化模板参考（动态 Canvas 版）

Claude 生成 HTML 可视化时，使用以下模板结构。将 `__CPN_DATA__` 替换为实际 JSON 数据对象。

## 核心规则

1. **渲染引擎**：Canvas（不用 SVG），绘制顺序：泳道 → 弧 → 变迁形状 → 库所形状 → 所有文字 → **依赖虚线最后画**（带背景色块），永不被节点遮挡
2. **动画**：粒子用线性进度值 `prog: 0→1`，每帧 `prog += dt / duration`，`prog >= 1` 时强制落地。**禁止**用指数逼近（`x += (target-x) * k`）——永远无法精确到达，必然卡死
3. **解锁条件**：`particles.every(pk => pk.done)` 全部落地才清除 `firingId`，**不能**用 `length <= 1`
4. **资源库所**：有初始 token 的库所（如"缴费待完成"）必须在 `places` 中设 `tokens: N`，否则多输入变迁永远无法触发
5. **主题**：提供4套宋式配色，CSS 变量驱动，切换时同步更新 canvas 背景

## ⚠️ 使用前必读：三个致命陷阱

生成 HTML 时必须遵守以下规则，否则会产生空白页面或运行卡死。

### 陷阱 1：chain 名 ≠ subproject 名 → 颜色全乱
模板中 `chainColorMap` 按 subproject 建索引，绘制时按 `node.chain` 查找。**两者必须一致**。
- JSON 数据中每个节点的 `"chain"` 字段必须等于 `"subproject"` 字段
- THEMES 中 `chains` 的 key 必须用 subproject 名（不是链名）
- 示例：`subproject:"挂号阶段"` 则 `chain:"挂号阶段"`，THEMES chains key 也是 `"挂号阶段"`

### 陷阱 2：guard_condition predecessor 用变迁 ID → 永远不可达
`guardDeps` 检查的是 `tokenMap[pid]`，tokenMap 只有库所 token，没有变迁 token。
- **predecessor 必须是库所 ID**（即 predecessor 变迁的输出库所）
- 用变迁 ID 会导致 `tokenMap["T3"]` 永远为 undefined → 守卫永远不过 → 死锁

### 陷阱 3：ES6+ 语法 → 旧浏览器报错
- 禁止 `**`（用 `x*x`），禁止 `??` / `?.` / `for...of`
- 禁止 `Math.max(...arr)`（用 `Math.max.apply(null, arr)`）
- 推荐 `function(){}` 代替箭头函数
- 代码分拆到多个 `<script>` 块，每块加 `"use strict"`

## 四套宋式主题

| 主题 | 灵感 | 背景 | 特点 |
|------|------|------|------|
| 天青 | 汝窑青瓷 | 暖米白 | 浅色，雅致清透 |
| 墨夜 | 极简黑白 | 纯黑 | 深色，高对比，荧光链色 |
| 石青 | 冷灰调 | 深蓝灰 | 深色，冷峻清晰 |
| 朱砂 | 暖白纸感 | 米白 | 浅色，饱和链色，对比强 |

## 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>CPN 模型可视化</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:#f0ece3; --cvs:#e8e3d8; --border:#cfc8bc;
  --text:#2a2418; --sub:#7a7060; --dim:#b0a898;
  --btn:#e4dfd4; --btn-t:#4a4030; --btn-b:#c8c0b0;
  --btn-h:#dad4c8; --act:#5a9080; --act-t:#f0ece3; --sep:#cfc8bc;
}
body { font-family:'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif;
  background:var(--bg); color:var(--text); padding:28px;
  min-height:100vh; transition:background .35s,color .35s; }
h1 { font-size:16px; font-weight:600; letter-spacing:.06em; }
.sub { font-size:11px; color:var(--sub); margin-top:4px; letter-spacing:.04em; }
canvas { display:block; border-radius:16px; border:1px solid var(--border);
  background:var(--cvs); transition:background .35s,border-color .35s;
  box-shadow:0 4px 40px rgba(0,0,0,.08); }
.canvas-outer { overflow:auto; margin-top:16px; border-radius:16px;
  max-width:100%; max-height:520px;
  box-shadow:0 4px 40px rgba(0,0,0,.08); }
.row { display:flex; gap:7px; margin-top:13px; align-items:center; flex-wrap:wrap; }
button { padding:5px 13px; border-radius:6px; font-size:11px; cursor:pointer;
  border:1px solid var(--btn-b); background:var(--btn); color:var(--btn-t);
  transition:all .15s; font-family:inherit; }
button:hover { background:var(--btn-h); }
button.active { background:var(--act); color:var(--act-t); border-color:var(--act); }
.sep { width:1px; height:18px; background:var(--sep); margin:0 3px; }
.legend { display:flex; gap:16px; margin-top:11px; font-size:11px; color:var(--dim); flex-wrap:wrap; align-items:center; }
.li { display:flex; align-items:center; gap:5px; }
</style>
</head>
<body>
<div style="display:flex;justify-content:space-between;align-items:flex-start;">
  <div>
    <h1>CPN 模型：<span id="pid"></span></h1>
    <div class="sub">着色 Petri 网</div>
  </div>
  <select id="theme-sel" style="padding:4px 8px;border-radius:6px;font-size:11px;cursor:pointer;border:1px solid var(--btn-b);background:var(--btn);color:var(--btn-t);font-family:inherit;letter-spacing:.04em;outline:none;transition:background .2s,color .2s,border-color .2s;" onchange="applyTheme(THEMES[this.selectedIndex])"></select>
</div>
<div class="canvas-outer">
<canvas id="c"></canvas>
</div>
<div class="row">
  <button id="btn-auto" onclick="toggleAuto()">▶ 自动运行</button>
  <button onclick="stepOnce()">单步</button>
  <button onclick="resetSim()">重置</button>
  <div class="sep"></div>
  <span style="font-size:11px;color:var(--dim)">速度</span>
  <button onclick="setSpeed(1400)" id="sp-slow">慢</button>
  <button onclick="setSpeed(800)"  id="sp-mid" class="active">中</button>
  <button onclick="setSpeed(360)"  id="sp-fast">快</button>
</div>
<div class="legend">
  <div class="li"><svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>库所</div>
  <div class="li"><svg width="16" height="10"><rect width="16" height="10" rx="2" fill="currentColor" opacity=".5"/></svg>变迁</div>
  <div class="li"><svg width="10" height="10"><circle cx="5" cy="5" r="4" fill="currentColor"/></svg>Token</div>
  <div class="li"><svg width="26" height="3"><line x1="0" y1="1.5" x2="26" y2="1.5" stroke="currentColor" stroke-width="1.5"/></svg>顺序弧</div>
  <div class="li"><svg width="26" height="3"><line x1="0" y1="1.5" x2="26" y2="1.5" stroke="#c07020" stroke-width="1.5" stroke-dasharray="6,4"/></svg><span style="color:#c07020">资源依赖</span></div>
  <div class="li"><svg width="26" height="3"><line x1="0" y1="1.5" x2="26" y2="1.5" stroke="#c02020" stroke-width="1.5" stroke-dasharray="3,3,8,3"/></svg><span style="color:#c02020">跨链守卫</span></div>
</div>
<script>
const data = __CPN_DATA__;
document.getElementById('pid').textContent = data.project_id;
```

```js
// ── 四套宋式主题 ──
const THEMES = [
  { id:'tiānqīng',name:'天青',sub:'汝窑',swatch:'#7aaa98',
    css:{'--bg':'#f0ece3','--cvs':'#e8e3d8','--border':'#cfc8bc','--text':'#2a2418','--sub':'#7a7060','--dim':'#b0a898','--btn':'#e4dfd4','--btn-t':'#4a4030','--btn-b':'#c8c0b0','--btn-h':'#dad4c8','--act':'#5a9080','--act-t':'#f0ece3','--sep':'#cfc8bc'},
    cvsBg:'#e8e3d8', dark:false, laneA:.09,
    chains:[{s:"#5a9a88",g:"#78b8a0",f:"#daeee8"},{s:"#6888a0",g:"#88a8c0",f:"#d8e4f0"},{s:"#9a7850",g:"#b89870",f:"#ecddd0"},{s:"#8a7898",g:"#a898b8",f:"#e4dce8"}],
    dep:'#c04828' },
  { id:'mòyè',name:'墨夜',sub:'极简',swatch:'#e8e8e8',
    css:{'--bg':'#0a0a0a','--cvs':'#111111','--border':'#2a2a2a','--text':'#f0f0f0','--sub':'#888888','--dim':'#555555','--btn':'#1a1a1a','--btn-t':'#d0d0d0','--btn-b':'#333333','--btn-h':'#222222','--act':'#e8e8e8','--act-t':'#0a0a0a','--sep':'#333333'},
    cvsBg:'#111111', dark:true, laneA:.07,
    chains:[{s:"#60c8a0",g:"#80e8c0",f:"#0a2018"},{s:"#60a8e0",g:"#80c8ff",f:"#0a1828"},{s:"#e0a040",g:"#ffc060",f:"#281a08"},{s:"#c060c0",g:"#e080e0",f:"#200820"}],
    dep:'#ff5040' },
  { id:'shíqīng',name:'石青',sub:'冷灰',swatch:'#7090b0',
    css:{'--bg':'#1a1e24','--cvs':'#20262e','--border':'#303840','--text':'#d8e4f0','--sub':'#6878a0','--dim':'#485870','--btn':'#252c38','--btn-t':'#a8c0d8','--btn-b':'#384858','--btn-h':'#2e3848','--act':'#4878b8','--act-t':'#e8f4ff','--sep':'#384858'},
    cvsBg:'#20262e', dark:true, laneA:.08,
    chains:[{s:"#48c8a0",g:"#68e8c0",f:"#0c2820"},{s:"#4898e0",g:"#68b8ff",f:"#0c1c38"},{s:"#e09848",g:"#ffb868",f:"#281c08"},{s:"#a868e0",g:"#c888ff",f:"#1c0c30"}],
    dep:'#ff6050' },
  { id:'zhūshā',name:'朱砂',sub:'暖白',swatch:'#c83828',
    css:{'--bg':'#fafaf8','--cvs':'#f4f4f0','--border':'#d8d4cc','--text':'#1a1410','--sub':'#6a5a50','--dim':'#a89888','--btn':'#eeeae4','--btn-t':'#3a2a20','--btn-b':'#c8c0b4','--btn-h':'#e4e0d8','--act':'#c83828','--act-t':'#fff8f4','--sep':'#d8d4cc'},
    cvsBg:'#f4f4f0', dark:false, laneA:.07,
    chains:[{s:"#1a9870",g:"#28c890",f:"#d8f4ec"},{s:"#1870c0",g:"#2890e8",f:"#d8ecf8"},{s:"#c87820",g:"#f09830",f:"#f8ead8"},{s:"#9828b8",g:"#c038e0",f:"#f0d8f8"}],
    dep:'#c83828' },
];

let T = THEMES[0];
const canvas = document.getElementById('c');

function applyTheme(theme) {
  T = theme;
  Object.entries(theme.css).forEach(([k,v]) => document.documentElement.style.setProperty(k,v));
  canvas.style.background = theme.cvsBg;
  const sel = document.getElementById('theme-sel');
  if (sel) sel.selectedIndex = THEMES.indexOf(theme);
}

const sel = document.getElementById('theme-sel');
THEMES.forEach((t,i) => {
  const opt = document.createElement('option');
  opt.value = i;
  opt.textContent = `${t.name} · ${t.sub}`;
  sel.appendChild(opt);
});
applyTheme(THEMES[0]);
```

```js
// ── 自动布局（最长路径算法，保证所有正向弧从左往右）──
const allNodes = [...data.places, ...data.transitions];
const spList = [...new Set(allNodes.map(n => n.subproject).filter(Boolean))];

// 资源库所：有初始 token，且同一变迁既消耗又归还（循环弧）
const resourcePlaceIds = new Set(
  data.places.filter(p => {
    if (!p.initial_marking || !p.initial_marking.length) return false;
    const consumers = data.arcs.filter(a => a.from === p.id && a.to.startsWith('T')).map(a => a.to);
    const producers = data.arcs.filter(a => a.to === p.id && a.from.startsWith('T')).map(a => a.from);
    return consumers.some(t => producers.includes(t));
  }).map(p => p.id)
);

// 去掉资源归还弧（T→资源库所），得到无环 DAG
const returnArcSet = new Set(
  data.arcs.filter(a => a.from.startsWith('T') && resourcePlaceIds.has(a.to)).map(a => a.id)
);
const dagAdj = {};
data.arcs.filter(a => !returnArcSet.has(a.id)).forEach(a => {
  if (!dagAdj[a.from]) dagAdj[a.from] = [];
  dagAdj[a.from].push(a.to);
});

// 最长路径（关键路径）：保证所有正向弧从左往右
const inDeg = {};
allNodes.forEach(n => inDeg[n.id] = 0);
Object.values(dagAdj).forEach(tos => tos.forEach(to => inDeg[to] = (inDeg[to]||0) + 1));
const dist = {};
const topoQ = allNodes.map(n => n.id).filter(id => !inDeg[id]);
topoQ.forEach(id => dist[id] = 0);
let tqi = 0;
while (tqi < topoQ.length) {
  const id = topoQ[tqi++];
  (dagAdj[id]||[]).forEach(nx => {
    dist[nx] = Math.max(dist[nx]||0, (dist[id]||0) + 1);
    if (--inDeg[nx] === 0) topoQ.push(nx);
  });
}
allNodes.forEach(n => { if (dist[n.id] === undefined) dist[n.id] = 0; });

// 资源库所放在其消费变迁的前一列（紧靠左侧）
resourcePlaceIds.forEach(pid => {
  const consumers = data.arcs.filter(a => a.from === pid && a.to.startsWith('T')).map(a => a.to);
  const minD = Math.min(...consumers.map(tid => dist[tid]||0));
  dist[pid] = Math.max(0, minD - 1);
});

const COL=160, SLOT_H=100, LANE_GAP=60, PX=80, PY=80;

// 第一遍：统计每条泳道在同一深度最多几个节点（决定泳道高度）
const spMaxSlot={}, spDepCnt2={};
allNodes.forEach(n => {
  const sp=n.subproject||'_', d=dist[n.id]||0, key=`${sp}:${d}`;
  spDepCnt2[key]=(spDepCnt2[key]||0)+1;
});
spList.forEach(sp => {
  let maxSlots=0;
  Object.keys(spDepCnt2).forEach(k => {
    if (k.startsWith(sp+':')) maxSlots=Math.max(maxSlots, spDepCnt2[k]);
  });
  spMaxSlot[sp]=maxSlots||1;
});

// 每条泳道高度 = maxSlots * SLOT_H，泳道间固定间隔 LANE_GAP
// 泳道框绘制时上下各加 50px padding，所以：
//   box_top    = spYStart - 50
//   box_bottom = spYStart + (maxSlots-1)*SLOT_H + 100
// 下一条泳道的 box_top 必须 >= 上一条 box_bottom + LANE_GAP
// 即 next_spYStart = spYStart + (maxSlots-1)*SLOT_H + 100 + LANE_GAP + 50
const spYStart={};
let curY=PY;
spList.forEach(sp => {
  spYStart[sp]=curY;
  curY = curY + (spMaxSlot[sp]-1)*SLOT_H + 150 + LANE_GAP;
});

// 第二遍：分配节点位置
const spDepCnt={}, positions={};
allNodes.forEach(n => {
  const sp=n.subproject||'_', d=dist[n.id]||0, key=`${sp}:${d}`;
  if (!spDepCnt[key]) spDepCnt[key]=0;
  const slot=spDepCnt[key]++;
  positions[n.id]={ x:PX+d*COL, y:spYStart[sp]+slot*SLOT_H };
});

// 画布按内容自然大小，外层容器负责滚动
const dpr=window.devicePixelRatio||1;
const maxX=Math.max(...Object.values(positions).map(p=>p.x))+120;
const maxY=Math.max(...Object.values(positions).map(p=>p.y))+120;
canvas.width=maxX*dpr; canvas.height=maxY*dpr;
canvas.style.width=maxX+'px'; canvas.style.height=maxY+'px';
const ctx=canvas.getContext('2d');
ctx.scale(dpr, dpr);

// ── 变迁输入输出表（从 arcs 推导）──
const tIn={}, tOut={};
data.transitions.forEach(t => { tIn[t.id]=[]; tOut[t.id]=[]; });
data.arcs.forEach(a => {
  if (a.from.startsWith('T') && tOut[a.from]) tOut[a.from].push(a.to);
  if (a.to.startsWith('T')   && tIn[a.to])    tIn[a.to].push(a.from);
});

// ── 模拟状态 ──
let tokenMap={}, tokenVal={}, particles=[], firingId=null, autoMode=false, autoTimer=null, stepMs=800;

// 从弧 annotation 推导每个库所对应的颜色值
const placeVal={};
data.arcs.forEach(a => {
  if (a.annotation) {
    const v=a.annotation.replace(/^\d+`/,'');
    if (a.from.startsWith('P')) placeVal[a.from]=v;
    if (a.to.startsWith('P'))   placeVal[a.to]=v;
  }
});
data.places.forEach(p => {
  if (p.initial_marking&&p.initial_marking[0]) placeVal[p.id]=p.initial_marking[0].replace(/^\d+`/,'');
});

function resetSim() {
  tokenMap={}; tokenVal={};
  data.places.forEach(p => {
    tokenMap[p.id]=(p.initial_marking&&p.initial_marking.length)?p.initial_marking.length:0;
    tokenVal[p.id]=placeVal[p.id]||'';
  });
  particles=[]; firingId=null;
}
resetSim();

// guard_condition 依赖：predecessor 必须是库所 ID（变迁的输出库所）
// ⚠️ predecessor 不能是变迁 ID，tokenMap 只存库所，不存变迁
const guardDeps = {};
// 先统计每变迁的输出库所
const transOutPlaces = {};
data.arcs.forEach(a => {
  if (a.from.startsWith('T') && a.to.startsWith('P')) {
    if (!transOutPlaces[a.from]) transOutPlaces[a.from] = [];
    transOutPlaces[a.from].push(a.to);
  }
});
(data.dependency_rules||[]).forEach(dep => {
  if (dep.mechanism === 'guard_condition') {
    if (!guardDeps[dep.successor]) guardDeps[dep.successor] = [];
    // 若 predecessor 是变迁 ID，自动替换为其输出库所
    if (dep.predecessor.startsWith('T') && transOutPlaces[dep.predecessor]) {
      guardDeps[dep.successor] = guardDeps[dep.successor].concat(transOutPlaces[dep.predecessor]);
    } else {
      guardDeps[dep.successor].push(dep.predecessor);
    }
  }
});

function getEnabled() {
  return data.transitions.filter(t => {
    if (!(tIn[t.id]||[]).length) return false;
    if (!(tIn[t.id]||[]).every(pid=>(tokenMap[pid]||0)>0)) return false;
    // guard_condition：守卫库所必须有 token，但不消耗
    const guards = guardDeps[t.id]||[];
    return guards.every(pid=>(tokenMap[pid]||0)>0);
  });
}

function fire(t) {
  if (firingId) return;
  (tIn[t.id]||[]).forEach(pid => tokenMap[pid]--);
  firingId=t.id;
  // 每条输出弧产生一个粒子（修复多输入变迁重复加 token 的 bug）
  const tp=positions[t.id];
  const srcVal=tokenVal[tIn[t.id][0]]||'';
  (tOut[t.id]||[]).forEach(toId => {
    const oarc=data.arcs.find(a=>a.from===t.id&&a.to===toId);
    const oval=oarc?oarc.annotation.replace(/^\d+`/,''):srcVal;
    particles.push({ path:[tp,positions[toId]], prog:0, chain:t.chain, toId, val:oval, done:false });
  });
}

function stepOnce() { if (!firingId) { const en=getEnabled(); if(en.length) fire(en[0]); } }

function toggleAuto() {
  autoMode=!autoMode;
  const btn=document.getElementById('btn-auto');
  if (autoMode) { btn.textContent='⏸ 暂停'; btn.classList.add('active'); scheduleNext(); }
  else { btn.textContent='▶ 自动运行'; btn.classList.remove('active'); clearTimeout(autoTimer); }
}

function scheduleNext() {
  if (!autoMode) return;
  autoTimer=setTimeout(() => {
    if (!firingId) {
      const en=getEnabled();
      if (!en.length) { setTimeout(()=>{ resetSim(); if(autoMode) scheduleNext(); },1400); return; }
      fire(en[Math.floor(Math.random()*en.length)]);
    }
    scheduleNext();
  }, 60);
}

function setSpeed(ms) {
  stepMs=ms;
  ['sp-slow','sp-mid','sp-fast'].forEach(id=>document.getElementById(id).classList.remove('active'));
  document.getElementById(ms===1400?'sp-slow':ms===800?'sp-mid':'sp-fast').classList.add('active');
}
```

```js
// ── 绘制工具 ──
const PR=28, TW=60, TH=32;

function roundRect(x,y,w,h,r) {
  ctx.beginPath();
  ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r); ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
  ctx.lineTo(x+r,y+h); ctx.arcTo(x,y+h,x,y+h-r,r);
  ctx.lineTo(x,y+r); ctx.arcTo(x,y,x+r,y,r); ctx.closePath();
}

function edgePt(id, toward, isStart) {
  const f=positions[id], t=positions[toward];
  const dx=t.x-f.x, dy=t.y-f.y, len=Math.sqrt(dx*dx+dy*dy)||1;
  const ux=dx/len, uy=dy/len, sign=isStart?1:-1;
  if (id.startsWith('P')) return {x:f.x+ux*sign*PR, y:f.y+uy*sign*PR};
  const sx=Math.abs(ux)<1e-6?1e9:(TW/2)/Math.abs(ux);
  const sy=Math.abs(uy)<1e-6?1e9:(TH/2)/Math.abs(uy);
  const s=Math.min(sx,sy);
  return {x:f.x+ux*sign*s, y:f.y+uy*sign*s};
}

function arrow(x1,y1,x2,y2,color,dashed,lw) {
  ctx.save(); ctx.strokeStyle=color; ctx.lineWidth=lw||1.3;
  if (dashed) ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); ctx.setLineDash([]);
  const dx=x2-x1,dy=y2-y1,len=Math.sqrt(dx*dx+dy*dy)||1,ux=dx/len,uy=dy/len;
  const ax=x2-ux*8,ay=y2-uy*8;
  ctx.fillStyle=color; ctx.beginPath();
  ctx.moveTo(x2,y2); ctx.lineTo(ax-uy*4,ay+ux*4); ctx.lineTo(ax+uy*4,ay-ux*4);
  ctx.closePath(); ctx.fill(); ctx.restore();
}

// 曲线弧（用于资源归还弧，向上弯曲避免与正向弧重叠）
function arrowCurve(x1,y1,x2,y2,color,lw) {
  const mx=(x1+x2)/2, my=(y1+y2)/2;
  const dx=x2-x1, dy=y2-y1, len=Math.sqrt(dx*dx+dy*dy)||1;
  const cx=mx-dy/len*50, cy=my+dx/len*50;
  ctx.save(); ctx.strokeStyle=color; ctx.lineWidth=lw||1.3;
  ctx.beginPath(); ctx.moveTo(x1,y1); ctx.quadraticCurveTo(cx,cy,x2,y2); ctx.stroke();
  const ex=x2-(x2-cx)*0.15, ey=y2-(y2-cy)*0.15;
  const ux2=(x2-ex)/Math.sqrt((x2-ex)**2+(y2-ey)**2)||1, uy2=(y2-ey)/Math.sqrt((x2-ex)**2+(y2-ey)**2)||0;
  const ax=x2-ux2*8, ay=y2-uy2*8;
  ctx.fillStyle=color; ctx.beginPath();
  ctx.moveTo(x2,y2); ctx.lineTo(ax-uy2*4,ay+ux2*4); ctx.lineTo(ax+uy2*4,ay-ux2*4);
  ctx.closePath(); ctx.fill(); ctx.restore();
}

function pathLerp(path, prog) {
  let segs=[], total=0;
  for (let i=1;i<path.length;i++) {
    const d=Math.sqrt((path[i].x-path[i-1].x)**2+(path[i].y-path[i-1].y)**2);
    segs.push(d); total+=d;
  }
  if (!total) return path[0];
  let dist=prog*total;
  for (let i=0;i<segs.length;i++) {
    if (dist<=segs[i]) { const f=segs[i]>0?dist/segs[i]:0; return {x:path[i].x+(path[i+1].x-path[i].x)*f,y:path[i].y+(path[i+1].y-path[i].y)*f}; }
    dist-=segs[i];
  }
  return path[path.length-1];
}

const DEP_STYLE = {
  arc_sequence:   { color: null, dash:[],        lw:1.0, label:'顺序' },
  fusion_place:   { color: null, dash:[6,4],     lw:1.4, label:'资源' },
  guard_condition:{ color: null, dash:[3,3,8,3], lw:1.4, label:'守卫' },
};

// ── 主绘制循环 ──
let lastT=0, frame=0;

function draw(now) {
  const dt=Math.min((now-lastT)/1000,.05); lastT=now; frame++;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const ch=T.chains;
  // 按泳道顺序分配链色（不依赖名称匹配，避免新模型链名不同时颜色错乱）
  const chainColors=Object.values(ch);
  const chainColorMap={};
  spList.forEach((sp,i)=>{ chainColorMap[sp]=chainColors[i%chainColors.length]; });
  // 补充链名索引：chain≠subproject 时也能正确查找颜色
  allNodes.forEach(n => {
    if (n.chain && n.subproject && !chainColorMap[n.chain]) {
      chainColorMap[n.chain] = chainColorMap[n.subproject] || chainColors[0];
    }
  });

  // 1. 泳道背景
  spList.forEach((sp,i) => {
    const spNodes=allNodes.filter(n=>n.subproject===sp); if(!spNodes.length) return;
    const xs=spNodes.map(n=>positions[n.id].x), ys=spNodes.map(n=>positions[n.id].y);
    const lx=Math.min(...xs)-50, ly=Math.min(...ys)-50, lw=Math.max(...xs)-lx+100, lh=Math.max(...ys)-ly+100;
    const c=Object.values(ch)[i%chainColors.length];
    ctx.save(); ctx.globalAlpha=T.laneA; ctx.fillStyle=c.s; roundRect(lx,ly,lw,lh,12); ctx.fill();
    ctx.globalAlpha=1; ctx.strokeStyle=c.s+(T.dark?'55':'44'); ctx.lineWidth=1; ctx.setLineDash([4,4]);
    roundRect(lx,ly,lw,lh,12); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle=c.s+(T.dark?'99':'bb'); ctx.font='bold 11px PingFang SC,sans-serif';
    ctx.fillText(sp,lx+10,ly+18); ctx.restore();
  });

  // 2. 普通弧（含弧表达式标注）
  data.arcs.forEach(a => {
    const node=data.places.find(p=>p.id===a.from)||data.transitions.find(t=>t.id===a.from);
    const c=chainColorMap[node?.chain]||chainColors[0];
    const s=edgePt(a.from,a.to,true), e=edgePt(a.to,a.from,false);
    const isReturn = returnArcSet.has(a.id);
    if (isReturn) {
      arrowCurve(s.x,s.y,e.x,e.y,c.s+(T.dark?'55':'66'),1.1);
    } else {
      arrow(s.x,s.y,e.x,e.y,c.s+(T.dark?'77':'88'),false,1.2);
    }
    if (a.annotation) {
      const mx=(s.x+e.x)/2, my=(s.y+e.y)/2;
      const dx=e.x-s.x, dy=e.y-s.y, len=Math.sqrt(dx*dx+dy*dy)||1;
      const nx=-dy/len, ny=dx/len, off=14;
      const label=a.annotation.replace(/^\d+`/,'');
      ctx.save(); ctx.font='9px PingFang SC,sans-serif';
      const tw=ctx.measureText(label).width;
      ctx.fillStyle=T.dark?'rgba(10,10,10,.8)':'rgba(255,255,255,.88)';
      ctx.fillRect(mx+nx*off-tw/2-3, my+ny*off-7, tw+6, 14);
      ctx.fillStyle=c.s+(T.dark?'':'cc'); ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(label, mx+nx*off, my+ny*off); ctx.restore();
    }
  });

  // 2b. dependency_rules 可视化（按 ID 直查，不做字符串匹配）
  // arc_sequence: 已由 arcs 覆盖，跳过
  // fusion_place: 橙色虚线（资源依赖）
  // guard_condition: 红色点划线（跨链守卫）
  DEP_STYLE.fusion_place.color    = T.dark?'#e09040':'#c07020';
  DEP_STYLE.guard_condition.color = T.dark?'#e05050':'#c02020';
  (data.dependency_rules||[]).forEach(dep => {
    if (dep.mechanism === 'arc_sequence') return;
    const fromPos = positions[dep.predecessor], toPos = positions[dep.successor];
    if (!fromPos || !toPos) return;
    const st = DEP_STYLE[dep.mechanism] || DEP_STYLE.fusion_place;
    const s2 = edgePt(dep.predecessor, dep.successor, true);
    const e2 = edgePt(dep.successor, dep.predecessor, false);
    const dx=e2.x-s2.x, dy=e2.y-s2.y, len=Math.sqrt(dx*dx+dy*dy)||1;
    const ox=-dy/len*6, oy=dx/len*6;
    ctx.save();
    ctx.strokeStyle=st.color; ctx.lineWidth=st.lw;
    ctx.setLineDash(st.dash); ctx.globalAlpha=0.75;
    ctx.beginPath(); ctx.moveTo(s2.x+ox,s2.y+oy); ctx.lineTo(e2.x+ox,e2.y+oy); ctx.stroke();
    ctx.setLineDash([]); ctx.globalAlpha=1;
    const ax=e2.x+ox, ay=e2.y+oy, ux=dx/len, uy=dy/len;
    const hx=ax-ux*8, hy=ay-uy*8;
    ctx.fillStyle=st.color;
    ctx.beginPath(); ctx.moveTo(ax,ay); ctx.lineTo(hx-uy*4,hy+ux*4); ctx.lineTo(hx+uy*4,hy-ux*4);
    ctx.closePath(); ctx.fill();
    const mx2=(s2.x+e2.x)/2+ox, my2=(s2.y+e2.y)/2+oy;
    ctx.font='9px PingFang SC,sans-serif';
    const tw2=ctx.measureText(st.label).width;
    ctx.fillStyle=T.dark?'rgba(10,10,10,.75)':'rgba(255,255,255,.82)';
    ctx.fillRect(mx2-tw2/2-3, my2-7, tw2+6, 14);
    ctx.fillStyle=st.color; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(st.label, mx2, my2);
    ctx.restore();
  });

  // 3. 变迁形状（填充确保文字可见）
  data.transitions.forEach(t => {
    const p=positions[t.id]; if(!p) return;
    const c=chainColorMap[t.chain]||chainColors[0];
    const isFiring=firingId===t.id, isEnabled=!firingId&&getEnabled().some(e=>e.id===t.id);
    ctx.save();
    if (isFiring) { ctx.shadowColor=c.g; ctx.shadowBlur=22+Math.sin(frame*.15)*6; }
    else if (isEnabled) { ctx.shadowColor=c.g; ctx.shadowBlur=10; }
    ctx.fillStyle=isFiring?c.g+'ee':(isEnabled?c.s+'cc':(T.dark?c.s+'33':c.f));
    roundRect(p.x-TW/2,p.y-TH/2,TW,TH,4); ctx.fill();
    ctx.strokeStyle=isFiring?c.g:(isEnabled?c.g+'cc':c.s+(T.dark?'88':'99'));
    ctx.lineWidth=isEnabled||isFiring?2:1.2;
    roundRect(p.x-TW/2,p.y-TH/2,TW,TH,4); ctx.stroke(); ctx.restore();
  });

  // 4. 库所形状
  data.places.forEach(pl => {
    const p=positions[pl.id]; if(!p) return;
    const c=chainColorMap[pl.chain]||chainColors[0];
    const has=(tokenMap[pl.id]||0)>0;
    ctx.save(); ctx.beginPath(); ctx.arc(p.x,p.y,PR,0,Math.PI*2);
    ctx.fillStyle=has?c.f+(T.dark?'dd':'cc'):(T.dark?'#0d0c0a':'#f8f5f0'); ctx.fill();
    ctx.strokeStyle=has?c.s:c.s+(T.dark?'44':'55'); ctx.lineWidth=has?2:1.2;
    if (has) { ctx.shadowColor=c.g; ctx.shadowBlur=12; }
    ctx.stroke(); ctx.restore();
    if (has) {
      const cnt=tokenMap[pl.id];
      for (let i=0;i<Math.min(cnt,5);i++) {
        const angle=cnt===1?-Math.PI/2:(i/cnt)*Math.PI*2-Math.PI/2, r=cnt===1?0:9;
        ctx.save(); ctx.beginPath(); ctx.arc(p.x+Math.cos(angle)*r,p.y+Math.sin(angle)*r,4.5,0,Math.PI*2);
        ctx.fillStyle=c.g; ctx.shadowColor=c.g; ctx.shadowBlur=14; ctx.fill(); ctx.restore();
      }
    }
  });

  // 5. 所有文字最后画（永不被遮挡）
  // 变迁：名称在矩形内（CPN 标准），guard 在矩形下方
  data.transitions.forEach(t => {
    const p=positions[t.id]; if(!p) return;
    const c=chainColorMap[t.chain]||chainColors[0];
    const isFiring=firingId===t.id, isEnabled=!firingId&&getEnabled().some(e=>e.id===t.id);
    ctx.save(); ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.font='bold 11px PingFang SC,sans-serif';
    ctx.fillStyle=isFiring?(T.dark?'#fff8e8':'#1a1000'):(isEnabled?(T.dark?'#e8f8f0':'#1a3a2a'):(T.dark?'#d0d8e0':'#2a3848'));
    ctx.fillText(t.name.length>5?t.name.slice(0,5)+'…':t.name,p.x,p.y);
    if (t.guard && t.guard!=='true') {
      ctx.font='9px monospace'; ctx.fillStyle=T.dark?'#888':'#888';
      ctx.fillText('['+t.guard+']', p.x, p.y+TH/2+10);
    }
    ctx.restore();
  });

  // 库所：CPN 标准布局
  // - 初始标记值：圆外上方（替代颜色集合英文名，更直观）
  // - 初始标记文字：圆内（始终显示，有 token 时被 token 点覆盖）
  // - 库所名称：圆外下方（两行）
  data.places.forEach(pl => {
    const p=positions[pl.id]; if(!p) return;
    const c=chainColorMap[pl.chain]||chainColors[0];
    const has=(tokenMap[pl.id]||0)>0;

    // 圆外上方：初始标记值（CPN 标准：颜色集合注释位置，改为显示初始值更直观）
    ctx.save(); ctx.textAlign='center'; ctx.textBaseline='bottom';
    ctx.font='9px PingFang SC,sans-serif';
    ctx.fillStyle=T.dark?c.s+'88':c.s+'99';
    const aboveText = pl.initial_marking&&pl.initial_marking.length
      ? pl.initial_marking[0].replace(/^\d+`/,'')
      : '';
    if (aboveText) ctx.fillText(aboveText, p.x, p.y-PR-4);
    ctx.restore();

    // 圆内：初始标记（始终显示，有 token 时被 token 点覆盖）
    if (pl.initial_marking && pl.initial_marking.length) {
      const initVal=pl.initial_marking[0].replace(/^\d+`/,'');
      ctx.save(); ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.font='bold 11px PingFang SC,sans-serif';
      ctx.fillStyle=T.dark?'#e8f8f0':'#1a3028';
      ctx.fillText(initVal, p.x, p.y); ctx.restore();
    }
    // 圆内：有 token 时显示当前颜色值（在 token 点旁）
    if (has) {
      const val=(typeof tokenVal!=='undefined'&&tokenVal[pl.id])||'';
      if (val) {
        ctx.save(); ctx.textAlign='center'; ctx.textBaseline='middle';
        ctx.font='bold 11px PingFang SC,sans-serif';
        ctx.fillStyle=T.dark?c.g:c.s;
        ctx.fillText(val, p.x, p.y+14); ctx.restore();
      }
    }

    // 圆外下方：库所名称（两行）
    ctx.save(); ctx.textAlign='center'; ctx.textBaseline='top';
    ctx.font='11px PingFang SC,sans-serif';
    ctx.fillStyle=has?(T.dark?'#d4c870':c.s):(T.dark?c.s+'aa':'#3a3028');
    const lines=pl.name.split('_'), lh=14;
    lines.forEach((ln,i)=>ctx.fillText(ln,p.x,p.y+PR+6+i*lh)); ctx.restore();
  });

  // 6. 依赖关系（最后画，永远在最上层）— 已在步骤 2b 绘制，此处无需重复

  // 7. 粒子（线性进度，不会卡死）
  const dur=stepMs*0.001*0.65;
  particles.forEach(pk => {
    if (pk.done) return;
    pk.prog+=dt/dur;
    if (pk.prog>=1) { pk.prog=1; pk.done=true; tokenMap[pk.toId]=(tokenMap[pk.toId]||0)+1; tokenVal[pk.toId]=pk.val||''; }
    const pt=pathLerp(pk.path,pk.prog), pt0=pathLerp(pk.path,Math.max(0,pk.prog-.1));
    const c=chainColorMap[pk.chain]||chainColors[0];
    ctx.save();
    ctx.strokeStyle=c.g+'55'; ctx.lineWidth=3;
    ctx.beginPath(); ctx.moveTo(pt0.x,pt0.y); ctx.lineTo(pt.x,pt.y); ctx.stroke();
    ctx.beginPath(); ctx.arc(pt.x,pt.y,6,0,Math.PI*2);
    ctx.fillStyle=c.g; ctx.shadowColor=c.g; ctx.shadowBlur=20; ctx.fill(); ctx.restore();
  });

  // 全部落地才解锁（必须 every，不能用 length <= 1）
  if (particles.length>0 && particles.every(pk=>pk.done)) { firingId=null; particles=[]; }

  requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
</script>
</body>
</html>
```

## 使用说明

1. 将 `__CPN_DATA__` 替换为 json-schema.md 格式的完整 JSON 对象
2. `places` 中有初始 token 的库所必须在 `initial_marking` 中列出（如 `["1\`收费链"]`），否则多输入变迁永远无法触发
3. 浏览器打开即可看到动态 Petri 网，支持自动运行、单步、重置、速度调节
4. 右上角4套宋式主题可切换：天青（汝窑）/ 墨夜（极简）/ 石青（冷灰）/ 朱砂（暖白）
5. 圆形=库所，矩形=变迁，实线=弧，红色虚线=依赖关系；可触发变迁发光提示
