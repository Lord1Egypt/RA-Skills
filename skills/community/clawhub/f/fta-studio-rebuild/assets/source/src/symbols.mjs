/**
 * FTA Studio - IEC 61025 Annex A 符号几何
 *
 * 集中定义门与事件的精确路径，供 SVG 导出（Node）与画布渲染（浏览器）共用，
 * 保证「屏幕上看到的」与「导出报告里的」完全一致。
 *
 * 关键几何约定（对照 IEC 61025:2006 Annex A）：
 *   AND 门：平顶 + 半圆底（flat top, semicircular underside）
 *   OR  门：弧顶 + 凹底（curved top, concave underside），呈盾形
 *   XOR 门：OR 门形状 + 背面附加弧线
 *   k/n 门：矩形 + k/n 标签
 *   INHIBIT：OR 门 + 底部悬垂线（接条件事件）
 *   PAND  ：与门 + 内部横线（表示输入优先次序）
 *
 * 所有路径以 (0,0) 为中心，向右/向下为正，使用相对简洁的绝对坐标。
 */

export const GATE_GEO = {
  // 门宽高（半宽 = W，半高 = H）
  W: 16,
  H: 11,
};

/**
 * AND 门：平底 + 半圆拱顶（medini 风格，向下生长的树形）
 * 操作符 "&" 写在门体内。
 */
export function andGatePath(W = GATE_GEO.W, H = GATE_GEO.H) {
  const w = W, h = H;
  return [
    `M ${-w} ${h}`,
    `L ${-w} 0`,
    `A ${w} ${h} 0 0 1 ${w} 0`,
    `L ${w} ${h}`,
    'Z',
  ].join(' ');
}

/**
 * OR 门：平底 + 尖拱顶（与 AND 的半圆顶可一眼区分）
 * 操作符 "≥1" 写在门体内。
 */
export function orGatePath(W = GATE_GEO.W, H = GATE_GEO.H) {
  const w = W, h = H;
  return [
    `M ${-w} ${h}`,
    `L ${-w} 0`,
    `Q 0 ${-h * 1.62} ${w} 0`,
    `L ${w} ${h}`,
    'Z',
  ].join(' ');
}

/**
 * XOR 门：OR 门 + 门体内侧的平行拱线
 */
export function xorGatePath(W = GATE_GEO.W, H = GATE_GEO.H) {
  const w = W, h = H;
  return [
    orGatePath(w, h),
    `M ${-w * 0.62} ${h * 0.2}`,
    `Q 0 ${-h * 1.05} ${w * 0.62} ${h * 0.2}`,
  ].join(' ');
}

/**
 * INHIBIT 门：AND 门 + 底部悬垂线（条件输入挂载点）
 */
export function inhibitGatePath(W = GATE_GEO.W, H = GATE_GEO.H) {
  const w = W, h = H;
  return [
    andGatePath(w, h),
    `M 0 ${h} L 0 ${h * 1.7}`,
  ].join(' ');
}

/**
 * PAND 优先与门：AND 门 + 底部优先次序横线
 */
export function pandGatePath(W = GATE_GEO.W, H = GATE_GEO.H) {
  const w = W, h = H;
  const body = andGatePath(w, h);
  const lines = [`M ${-w * 0.62} ${h * 1.55} L ${w * 0.62} ${h * 1.55}`];
  return { body, lines };
}

/**
 * k/n 表决门：矩形 + 标签
 */
export function voteGatePath(W = GATE_GEO.W, H = GATE_GEO.H) {
  const w = W, h = H;
  return {
    body: `M ${-w} ${-h} L ${w} ${-h} L ${w} ${h} L ${-w} ${h} Z`,
    w, h,
  };
}

/** 门体内操作符文字（medini 风格） */
export const GATE_OPERATOR = { AND: '&', PAND: '&', OR: '≥1', XOR: '=1', INHIBIT: '&' };

// ============ 事件符号 ============

/** 基本事件：圆（节点固定宽高，按文字宽度略作椭圆化与画布保持一致） */
export function basicEventPath(W = 76, H = 44) {
  const rx = (W / 2) * 0.8;
  const ry = H / 2;
  return `M ${-rx} 0 A ${rx} ${ry} 0 1 0 ${rx} 0 A ${rx} ${ry} 0 1 0 ${-rx} 0 Z`;
}

/** 中间事件/顶事件：矩形 */
export function rectEventPath(W = 76, H = 44) {
  const w = W / 2, h = H / 2;
  return `M ${-w} ${-h} L ${w} ${-h} L ${w} ${h} L ${-w} ${h} Z`;
}

/** 未开发事件：菱形 */
export function undevelopedEventPath(W = 76, H = 44) {
  const w = W / 2, h = H / 2;
  return `M 0 ${-h} L ${w} 0 L 0 ${h} L ${-w} 0 Z`;
}

/** 房屋事件：五边形（IEC 61025 房屋形） */
export function houseEventPath(W = 76, H = 44) {
  const w = W / 2, h = H / 2;
  const ridge = h * 0.44;
  const eave = h * 0.72;
  return [
    `M ${-w} ${h}`,
    `L ${-w} ${-eave}`,
    `L 0 ${-h}`,
    `L ${w} ${-eave}`,
    `L ${w} ${h}`,
    'Z',
  ].join(' ');
}

/** 条件事件：扁椭圆（与基本事件区分，与画布一致） */
export function conditionEventPath(W = 76, H = 44) {
  const rx = W / 2;
  const ry = (H / 2) * 0.76;
  return [
    `M ${-rx} 0`,
    `A ${rx} ${ry} 0 1 0 ${rx} 0`,
    `A ${rx} ${ry} 0 1 0 ${-rx} 0`,
    'Z',
  ].join(' ');
}

/** 外部事件：圆 + 内部叉（IEC 61025） */
export function externalEventPath(W = 76, H = 44) {
  const r = Math.min(W, H) / 2;
  return {
    body: `M ${-r} 0 A ${r} ${r} 0 1 0 ${r} 0 A ${r} ${r} 0 1 0 ${-r} 0 Z`,
    cross: [`M ${-r * 0.62} ${-r * 0.62} L ${r * 0.62} ${r * 0.62}`,
            `M ${r * 0.62} ${-r * 0.62} L ${-r * 0.62} ${r * 0.62}`],
    r,
  };
}

/** 传输符号：三角形（跨页引用） */
export function transferEventPath(W = 76, H = 44) {
  const w = W / 2, h = H / 2;
  return `M 0 ${-h} L ${w} ${h} L ${-w} ${h} Z`;
}

/** 注释事件：虚线矩形 */
export function commentEventPath(W = 76, H = 44) {
  return rectEventPath(W, H);
}

/** 按事件类型取路径 */
export function eventPath(type, W = 76, H = 44) {
  switch (type) {
    case 'basic': return { kind: 'path', d: basicEventPath(W, H) };
    case 'undeveloped': return { kind: 'path', d: undevelopedEventPath(W, H) };
    case 'house': return { kind: 'path', d: houseEventPath(W, H) };
    case 'condition': return { kind: 'path', d: conditionEventPath(W, H) };
    case 'external': return { kind: 'complex', ...externalEventPath(W, H) };
    case 'transfer_in': case 'transfer_out':
      return { kind: 'path', d: transferEventPath(W, H) };
    case 'comment': return { kind: 'path', d: commentEventPath(W, H), dashed: true };
    default: return { kind: 'path', d: rectEventPath(W, H) };
  }
}

/** 按门类型取路径与附加元素 */
export function gatePath(gate, k, n) {
  const w = GATE_GEO.W, h = GATE_GEO.H;
  const op = GATE_OPERATOR[gate];
  switch (gate) {
    case 'AND': return { body: andGatePath(), lines: [], op, w, h };
    case 'PAND': {
      const { body, lines } = pandGatePath();
      return { body, lines, op, w, h };
    }
    case 'OR': return { body: orGatePath(), lines: [], op, w, h };
    case 'XOR': return { body: xorGatePath(), lines: [], op, w, h };
    case 'INHIBIT': return { body: inhibitGatePath(), lines: [], op, w, h };
    case 'NOT': return { body: `M ${-w} ${-h} L ${w} ${-h} L 0 ${h} Z`, lines: [], w, h };
    case 'VOTE': {
      const r = voteGatePath();
      return { body: r.body, lines: [], label: `${k}/${n}`, w: r.w, h: r.h };
    }
    default: return { body: andGatePath(), lines: [], op, w, h };
  }
}

/**
 * 判断是否为「非相干门」（影响求解方法选择）
 */
export function isNonCoherent(gate) {
  return gate === 'XOR' || gate === 'NOT' || gate === 'INHIBIT';
}