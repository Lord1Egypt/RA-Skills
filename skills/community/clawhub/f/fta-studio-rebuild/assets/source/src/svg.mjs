/**
 * FTA Studio - SVG 渲染器
 * 遵循 IEC 61025 Annex A 标准符号体系（几何定义见 symbols.mjs）
 */

import { layout } from './layout.mjs';
import { buildIndex, findTopEvent, fmtNum, EVENT_TYPE_LABEL } from './model.mjs';
import { eventPath, gatePath } from './symbols.mjs';
import { autoPaginate, buildPageView, buildFlatView, paginateBanded, buildBandedView } from './paginate.mjs';

/**
 * 渲染故障树为 SVG 字符串
 * @param {object} tree
 * @param {object} opts
 *   heatmap: {id: 0..1}  热力着色
 *   showProb: boolean    显示概率
 *   mode: 'light'|'dark'
 *   page: {nodes:Set, label}  仅渲染指定页（跨页功能）
 */
export function renderSVG(tree, opts = {}) {
  const view = opts.page ? filterToPage(tree, opts.page) : tree;
  const L = layout(view);
  const heat = opts.heatmap || {};
  const dark = opts.mode === 'dark';
  const showProb = opts.showProb !== false;

  const bg = dark ? '#14161a' : '#ffffff';
  const stroke = dark ? '#e6e8eb' : '#1f2937';
  const text = dark ? '#e6e8eb' : '#111827';
  const muted = dark ? '#9aa3af' : '#6b7280';
  const link = dark ? '#6b7280' : '#374151';
  const gateFill = dark ? '#1f2937' : '#ffffff';

  // 承接事件：来自上一页、为了说明"挂在谁下面"而补画的一级父事件
  const ctxIds = opts.contextIds instanceof Set
    ? opts.contextIds
    : new Set(opts.contextIds || []);

  // 存根：为保证"同一事件的子事件齐全"而补画、但内容在别的页的兄弟事件
  const stubMap = (opts.stubs && typeof opts.stubs === 'object') ? opts.stubs : {};

  // 手动分页点：本页页底的虚线框，表示该支已分到下一页
  const markerIds = opts.markers instanceof Set
    ? opts.markers
    : new Set(opts.markers || []);

  // 分页标注文字（打印件用）：{id: '⤓ 分页 → 第 2 页'}，画在虚线框正上方
  const pageNotes = (opts.pageNotes && typeof opts.pageNotes === 'object') ? opts.pageNotes : {};
  const noteColor = dark ? '#5ee0a8' : '#0a7d55';
  // 顶部留白：标注文字画在事件框上边缘之上，首行没有留白会被 viewBox 裁掉
  const topPad = Math.max(0, Number(opts.topPad) || 0);

  const width = opts.width ?? Math.max(L.width, 640);
  const height = (opts.height ?? Math.max(L.height, 420)) + topPad;

  const parts = [];
  parts.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" font-family="Inter, 'Segoe UI', 'Microsoft YaHei', sans-serif">`);
  parts.push(`<rect width="100%" height="100%" fill="${bg}"/>`);
  parts.push(`<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="${link}"/>
  </marker>
</defs>`);

  if (opts.page?.title) {
    parts.push(`<text x="24" y="30" font-size="15" font-weight="600" fill="${text}">${esc(opts.page.title)}</text>`);
  }

  // 几何整体下移，给事件框上方的分页标注让出空间
  if (topPad) parts.push(`<g transform="translate(0,${topPad})">`);

  // ---- 连接线 ----
  parts.push(`<g class="links" fill="none" stroke="${link}" stroke-width="1.6" marker-end="url(#arrow)">`);
  for (const l of L.links) {
    const fromNode = L.nodeById?.get(l.from);
    const dashed = l.dashed ? ' stroke-dasharray="5 4"' : '';
    parts.push(`<path d="${l.curve}"${dashed} opacity="0.85"/>`);
  }
  parts.push(`</g>`);

  // ---- 节点 ----
  for (const [id, nd] of L.nodes) {
    const n = nd.node;
    const x = nd.x, y = nd.y, w = nd.w, h = nd.h;
    const cx = x + w / 2, cy = y + h / 2;
    const h01 = heat[id] ?? 0;
    const fill = heatColor(h01, dark);
    const shape = eventPath(n.type, w, h);
    const s = [`<g class="node node-${n.type}" data-id="${id}" id="n_${id}">`];

    // 形状（几何以 0,0 为中心，用 transform 平移到节点中心）
    //
    // 注意：绝不能把路径里的数字两两相加来"平移"。
    // 椭圆用 `A rx ry rot large sweep x y`，7 个参数不是坐标对，
    // 逐对相加会破坏弧命令 → 基本事件（圆）在导出图里直接消失。
    const tf = `translate(${cx},${cy})`;
    const isCtx = ctxIds.has(id);
    const stubPage = stubMap[id];
    const isStub = stubPage != null;
    const isMarker = markerIds.has(id);
    const dashAttr = isStub
      ? ' stroke-dasharray="1.5 3"'
      : ((shape.dashed || isCtx || isMarker) ? ' stroke-dasharray="4 3"' : '');

    if (shape.kind === 'complex') {
      s.push(`<path d="${shape.body}" transform="${tf}" fill="${fill}" stroke="${stroke}" stroke-width="1.7"${dashAttr}/>`);
      for (const c of shape.cross) s.push(`<path d="${c}" transform="${tf}" fill="none" stroke="${stroke}" stroke-width="1.4"/>`);
    } else {
      s.push(`<path d="${shape.d}" transform="${tf}" fill="${fill}" stroke="${stroke}" stroke-width="1.7"${dashAttr}/>`);
    }

    // 承接事件标注：让读者知道这一框是上一页的底事件，不是本页新出现的
    if (isCtx) {
      s.push(`<text x="${cx}" y="${y - 6}" text-anchor="middle" font-size="9" fill="${muted}">↑ 承接上页</text>`);
    }
    // 存根标注：本页只画出这个兄弟事件本身，它的展开在另一页
    if (isStub) {
      s.push(`<text x="${cx}" y="${y - 6}" text-anchor="middle" font-size="9" fill="${muted}">→ 续见第 ${stubPage} 页</text>`);
    }
    // 分页标注（打印件最重要的导航信息）：本页页底虚线框 → 翻到第几页；
    // 本页顶事件 → 从第几页续过来。放在框正上方并加粗，打印后一眼能找到。
    if (pageNotes[id]) {
      s.push(`<text x="${cx}" y="${y - 6}" text-anchor="middle" font-size="9.5" font-weight="700" fill="${noteColor}">${esc(pageNotes[id])}</text>`);
    }

    // 文本（按可用宽度自适应截断：中文按 1 个字号宽、西文约 0.56 个字号宽）
    // 圆/椭圆类事件的实际宽度只有 0.8w，文字宽度要按图形宽度算，否则会溢出圆外
    const ellipseLike = n.type === 'basic' || n.type === 'condition';
    let labelMax = ellipseLike ? w * 0.8 - 12 : w - 14;
    let labelX = cx;
    let labelAnchor = 'middle';
    if (n.type === 'basic') {
      // medini 风格：底事件左缘红色圆点，文字左对齐紧随其后
      const rx = w * 0.4;
      const dotX = cx - rx + 9;
      s.push(`<circle cx="${dotX}" cy="${cy}" r="4" fill="#e01b24" stroke="#9c1a1a" stroke-width="0.8"/>`);
      labelX = dotX + 10;
      labelAnchor = 'start';
      labelMax = (cx + rx - 8) - labelX;
    }
    const label = fitLabel(n.name || EVENT_TYPE_LABEL[n.type] || n.type, labelMax, 12.5);
    // 文字基线：椭圆/圆在上部迅速收窄，文字必须靠近中线才不会溢出圆外
    const textY = cy + 4;
    s.push(`<text x="${labelX}" y="${textY}" text-anchor="${labelAnchor}" font-size="12.5" fill="${text}" font-weight="500">${esc(label)}</text>`);

    if (showProb && (n.type === 'basic' || n.type === 'undeveloped') && n.prob != null) {
      const qY = ellipseLike ? cy + 17 : cy + 13;
      s.push(`<text x="${cx}" y="${qY}" text-anchor="middle" font-size="10.5" fill="${muted}" font-family="'JetBrains Mono',Consolas,monospace">q=${fmtNum(n.prob)}</text>`);
    }
    if (n.ref) {
      s.push(`<text x="${cx}" y="${y + h + 12}" text-anchor="middle" font-size="9.5" fill="${muted}">${esc(n.ref)}</text>`);
    }
    // 跨页引用标注
    if (n.type === 'transfer_in' && n.transferRef) {
      s.push(`<text x="${cx}" y="${y + h + 12}" text-anchor="middle" font-size="9.5" fill="${link}">→ ${esc(n.transferRef)}</text>`);
    }
    s.push(`</g>`);
    parts.push(s.join(''));

    // ---- 门符号 ----
    if (n.gate && nd.gateY != null && L.links.some((l) => l.from === id)) {
      parts.push(renderGate(n.gate, nd.gateX, nd.gateY, n.voteK, n.voteN, gateFill, stroke, text));
    }
  }

  parts.push(topPad ? '</g></svg>' : '</svg>');
  return parts.join('\n');
}

function renderGate(gate, cx, cy, k, n, fill, stroke, text) {
  const g = gatePath(gate, k, n);
  const parts = [`<g class="gate gate-${gate}">`];
  parts.push(`<path d="${g.body}" transform="translate(${cx},${cy})" fill="${fill}" stroke="${stroke}" stroke-width="1.3"/>`);
  for (const line of g.lines || []) {
    parts.push(`<path d="${line}" transform="translate(${cx},${cy})" fill="none" stroke="${stroke}" stroke-width="1"/>`);
  }
  if (g.label) {
    parts.push(`<text x="${cx}" y="${cy + 4}" text-anchor="middle" font-size="9.5" font-weight="700" fill="${text}" font-family="'JetBrains Mono',Consolas,monospace">${esc(g.label)}</text>`);
  } else if (g.op) {
    // medini 风格：操作符画在门体内（& / ≥1 / =1）
    parts.push(`<text x="${cx}" y="${cy + 6.8}" text-anchor="middle" font-size="9.5" font-weight="700" fill="${text}">${esc(g.op)}</text>`);
  }
  parts.push('</g>');
  return parts.join('');
}

/** 热力图配色：绿 → 黄 → 红（定量热力图） */
export function heatColor(h, dark = false) {
  const t = Math.max(0, Math.min(1, h || 0));
  const stops = [
    { p: 0.0, c: dark ? [30, 58, 46] : [220, 252, 231] },
    { p: 0.4, c: dark ? [120, 88, 20] : [254, 249, 195] },
    { p: 0.72, c: dark ? [140, 66, 20] : [254, 226, 150] },
    { p: 1.0, c: dark ? [150, 34, 34] : [254, 202, 202] },
  ];
  for (let i = 0; i < stops.length - 1; i++) {
    const a = stops[i], b = stops[i + 1];
    if (t >= a.p && t <= b.p) {
      const f = (t - a.p) / (b.p - a.p);
      const r = Math.round(a.c[0] + (b.c[0] - a.c[0]) * f);
      const g = Math.round(a.c[1] + (b.c[1] - a.c[1]) * f);
      const bl = Math.round(a.c[2] + (b.c[2] - a.c[2]) * f);
      return `rgb(${r},${g},${bl})`;
    }
  }
  return stops[stops.length - 1].c.join(',');
}

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function truncate(s, n) {
  const str = String(s ?? '');
  return str.length > n ? str.slice(0, n - 1) + '…' : str;
}

/**
 * 按可用像素宽度截断（中文按 1 个字号宽，西文约 0.56 个字号宽）。
 * 事件框固定 150px，长名称若不截断会溢出到相邻节点，看起来像文字互相重叠。
 */
function fitLabel(s, maxPx, fontSize) {
  const str = String(s ?? '');
  let used = 0;
  let out = '';
  for (const ch of str) {
    const cjk = /[\u2E80-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/.test(ch);
    const cw = cjk ? fontSize : fontSize * 0.56;
    if (used + cw > maxPx) return out + '…';
    used += cw;
    out += ch;
  }
  return out;
}

/** 将 SVG 嵌入 Markdown（base64 data URI） */
export function svgToDataURI(svg) {
  const cleaned = svg.replace(/\n\s*/g, ' ').trim();
  return `data:image/svg+xml;base64,${Buffer.from(cleaned, 'utf8').toString('base64')}`;
}

/** 页眉的「承接」说明：本页顶事件来自上一页的哪些事件 */
function contTextOf(view, page) {
  const pages = view?.meta?.continuedFromPages || [];
  const names = view?.meta?.continuedFromNames || [];
  if (!pages.length) return page?.index === 1 ? '本页为顶事件' : '承接上一页';
  const pg = pages.join('、');
  if (names.length === 1) {
    const nm = names[0].length > 24 ? names[0].slice(0, 24) + '…' : names[0];
    return `承接第 ${pg} 页：${nm}`;
  }
  return `承接第 ${pg} 页（${names.length} 个上层事件）`;
}

/**
 * 渲染「A4 分页」HTML：每个故障树页 = 一张真实 A4 纸。
 *
 * 用途：导出后可直接用浏览器打印 / 另存为 PDF，按 A4 自动分页，
 * 不再出现「整棵树挤在一页」的情况。
 *
 * @param {object} tree
 * @param {object} opts
 *   maxNodes  每页节点数上限（默认 16）
 *   heatmap   热力着色
 *   showProb  是否显示概率
 *   mode      light | dark
 */
export function renderA4HTML(tree, opts = {}) {
  // 前沿推进分页：自上而下连续，下一页的顶事件 = 上一页的页底事件
  const pag = paginateBanded(tree, { budget: opts.budget ?? 14 });
  const heat = opts.heatmap || {};
  const title = tree.meta?.title || '故障树分析';

  // A4 @96dpi
  const A4W = 794, A4H = 1123, PAD = 28, HEAD = 34, FOOT = 18;
  const cw = A4W - PAD * 2;
  const ch = A4H - PAD * 2 - HEAD - FOOT;

  // 每个事件归属的页号（后写的页胜出：分页点同时出现在本页虚线保留
  // 和下一页页首，取它真正展开的那一页）
  const pageOfId = {};
  for (const pg of pag.pages) for (const id of pg.nodes) pageOfId[id] = pg.index;

  const sheets = pag.pages.map((p) => {
    const view = buildBandedView(tree, pag, p.index) || tree;
    const breakIds = view.meta?.breakMarkerIds || [];
    const contIds = view.meta?.contMarkerIds || [];
    // 打印件上的页码导航：虚线框旁直接写「翻到第几页 / 从第几页续过来」。
    // 同一页有多个分页点时各自开页，目标页必须逐个查，不能统一写 p.index+1。
    const notes = {};
    for (const id of breakIds) {
      notes[id] = pageOfId[id] ? `⤓ 分页 → 第 ${pageOfId[id]} 页` : '⤓ 分页 → 下一页';
    }
    for (const id of contIds) {
      notes[id] = p.continuedFrom ? `↑ 续自第 ${p.continuedFrom} 页` : '↑ 续自上一页';
    }
    let raw = renderSVG(view, {
      heatmap: heat,
      showProb: opts.showProb !== false,
      mode: opts.mode || 'light',
      markers: [...breakIds, ...contIds],
      pageNotes: notes,
      topPad: Object.keys(notes).length ? 16 : 0,
    });
    const m = /width="([\d.]+)"\s+height="([\d.]+)"/.exec(raw);
    const w = m ? parseFloat(m[1]) : cw;
    const h = m ? parseFloat(m[2]) : ch;
    // 等比缩放并充满纸面：既保证不裁切，也避免窄页面（如主干链）看起来大片留白。
    // 上限 1.6 倍，防止节点少时被放得过大。
    const scale = Math.min(1.6, cw / w, ch / h);
    raw = raw.replace(
      /width="[\d.]+"\s+height="[\d.]+"/,
      `width="${Math.max(1, Math.round(w * scale))}" height="${Math.max(1, Math.round(h * scale))}"`
    );
    return { p, svg: raw, scale, contText: contTextOf(view, p) };
  });

  const total = sheets.length;
  const body = sheets.map(({ p, svg, contText }, i) => `
  <section class="sheet">
    <div class="hd">
      <span class="t">${esc(title)}</span>
      <span class="p">第 ${i + 1} / ${total} 页 · ${esc(contText)}</span>
    </div>
    <div class="bd">${svg}</div>
    <div class="ft"><span>FTA Studio · IEC 61025</span><span>${i + 1} / ${total}</span></div>
  </section>`).join('\n');

  return `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>${esc(title)} · FTA 分页图</title>
<style>
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: #eef1f4; }
  body { font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", sans-serif; }
  .hint {
    max-width: 210mm; margin: 12px auto; padding: 10px 14px; border-radius: 6px;
    background: #fff8e1; border: 1px solid #f0d48a; color: #7a5b00; font-size: 13px;
  }
  .sheet {
    width: 210mm; height: 297mm; padding: 10mm; margin: 0 auto 8mm;
    background: #fff; position: relative; overflow: hidden;
    box-shadow: 0 1px 6px rgba(0,0,0,.14);
    page-break-after: always; break-after: page;
    display: flex; flex-direction: column;
  }
  .sheet:last-of-type { page-break-after: auto; break-after: auto; margin-bottom: 0; }
  .hd {
    flex: 0 0 auto; height: 9mm; display: flex; align-items: center;
    justify-content: space-between; gap: 12px; font-size: 11px; color: #555;
    border-bottom: 1px solid #d8dde3; padding-bottom: 3px;
  }
  .hd .t {
    flex: 1 1 auto; min-width: 0; font-weight: 700; color: #1a1a1a; font-size: 12.5px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .hd .p { flex: 0 0 auto; white-space: nowrap; }
  .bd {
    flex: 1 1 auto; display: flex; align-items: flex-start; justify-content: center;
    overflow: hidden; padding-top: 4mm;
  }
  .bd svg { max-width: 100%; max-height: 100%; }
  .ft {
    flex: 0 0 auto; height: 6mm; display: flex; align-items: center;
    justify-content: space-between; font-size: 9.5px; color: #999;
  }
  @media print {
    html, body { background: #fff; }
    .hint { display: none; }
    .sheet { margin: 0; box-shadow: none; }
  }
</style>
</head>
<body>
<div class="hint">共 ${total} 页（A4）。按 <b>Ctrl+P</b> → 目标选择「另存为 PDF」即可得到按 A4 分页的文件。</div>
${body}
</body>
</html>`;
}

/** 取指定页的子图（跨页渲染用） */
function filterToPage(tree, page) {
  const ids = page.nodes instanceof Set ? page.nodes : new Set(page.nodes || []);
  return {
    ...tree,
    nodes: tree.nodes.filter((n) => ids.has(n.id)),
    connections: tree.connections.filter((c) => ids.has(c.from) && ids.has(c.to)),
  };
}