/**
 * Beautiful Mermaid Style Presets
 *
 * 提供预设样式和 CSS 样式生成功能。
 * 这是唯一的预设数据源 —— render.js 和 preview.html 均从此模块导入。
 *
 * ─────────────────────────────────────────────
 * 同步自上游 src/styles.ts（lukilabs/beautiful-mermaid）
 *   - MONO_FONT / MONO_FONT_STACK        等宽字体栈
 *   - FONT_SIZES / FONT_WEIGHTS          字号与字重
 *   - NODE_PADDING                       节点内边距
 *   - STROKE_WIDTHS                      描边宽度
 *   - TEXT_BASELINE_SHIFT                文本基线偏移
 *   - ARROW_HEAD                         箭头尺寸
 *   - GROUP_HEADER_CONTENT_PAD           子图标题间距
 * ─────────────────────────────────────────────
 */

// ─────────────────────────────────────────────────────────────────────────────
// §1  字体度量常量（源自 src/styles.ts）
// ─────────────────────────────────────────────────────────────────────────────

/** 等宽字体主字体（JetBrains Mono）*/
const MONO_FONT = "'JetBrains Mono'";

/** 完整等宽字体降级栈 */
const MONO_FONT_STACK = `${MONO_FONT}, 'SF Mono', 'Fira Code', ui-monospace, monospace`;

/** 等宽字体文本宽度估算（字符数 × 字号 × 0.6） */
function estimateMonoTextWidth(text, fontSize) {
  return text.length * fontSize * 0.6;
}

// ─────────────────────────────────────────────────────────────────────────────
// §2  字号与字重（源自 src/styles.ts）
// ─────────────────────────────────────────────────────────────────────────────

const FONT_SIZES = {
  nodeLabel:   13,   // 节点标签文本
  edgeLabel:   11,   // 边标签文本
  groupHeader: 12,   // 子图标题文本
};

const FONT_WEIGHTS = {
  nodeLabel:   500,  // 节点标签字重
  edgeLabel:   400,  // 边标签字重
  groupHeader: 600,  // 子图标题字重
};

// ─────────────────────────────────────────────────────────────────────────────
// §3  几何参数（源自 src/styles.ts）
// ─────────────────────────────────────────────────────────────────────────────

/** 子图标题带与内容区域之间的垂直间隙 */
const GROUP_HEADER_CONTENT_PAD = 12;

/** 节点形状内边距 */
const NODE_PADDING = {
  horizontal:   20,  // 水平内边距
  vertical:     10,  // 垂直内边距
  diamondExtra: 24,  // 菱形额外内边距
};

/** 描边宽度 */
const STROKE_WIDTHS = {
  outerBox:  1,      // 外框描边
  innerBox:  0.75,   // 内框描边
  connector: 1,      // 连接器描边
};

/** 文本基线偏移量（用于字体无关的垂直居中） */
const TEXT_BASELINE_SHIFT = '0.35em';

/** 箭头尺寸 */
const ARROW_HEAD = {
  width:  8,   // 箭头宽度
  height: 5,   // 箭头高度
};

// ─────────────────────────────────────────────────────────────────────────────
// §4  主题定义（源自 src/theme.ts，共 15 个）
// ─────────────────────────────────────────────────────────────────────────────
// 每个主题包含完整 7 字段：
//   bg       背景色
//   fg       前景/主文字色
//   line     连线/边颜色
//   accent   强调色（箭头、高亮、子图标题）
//   muted    次要文字色（边标签、辅助信息）
//   surface  节点填充次级色（比 bg 深/浅一级，用于节点内部）
//   border   节点边框精确色
//
// 使用方式：THEMES['tokyo-night'] → { bg, fg, line, accent, muted, surface, border }

const THEMES = {
  // ── Zinc（极简黑白系） ──────────────────────────────────────────────────────
  'zinc-light': {
    bg:      '#FFFFFF',
    fg:      '#27272A',
    line:    '#A1A1AA',   // zinc-400
    accent:  '#3F3F46',   // zinc-700
    muted:   '#71717A',   // zinc-500
    surface: '#F4F4F5',   // zinc-100
    border:  '#D4D4D8',   // zinc-300
  },
  'zinc-dark': {
    bg:      '#18181B',
    fg:      '#FAFAFA',
    line:    '#52525B',   // zinc-600
    accent:  '#A1A1AA',   // zinc-400
    muted:   '#71717A',   // zinc-500
    surface: '#27272A',   // zinc-800
    border:  '#3F3F46',   // zinc-700
  },

  // ── Tokyo Night（夜间代码主题） ────────────────────────────────────────────
  'tokyo-night': {
    bg:      '#1a1b26',
    fg:      '#a9b1d6',
    line:    '#3d59a1',
    accent:  '#7aa2f7',
    muted:   '#565f89',
    surface: '#24283b',   // storm 背景色作为节点 surface
    border:  '#414868',   // 暗紫灰
  },
  'tokyo-night-storm': {
    bg:      '#24283b',
    fg:      '#a9b1d6',
    line:    '#3d59a1',
    accent:  '#7aa2f7',
    muted:   '#565f89',
    surface: '#2f3549',   // 比 bg 稍亮
    border:  '#414868',
  },
  'tokyo-night-light': {
    bg:      '#d5d6db',
    fg:      '#343b58',
    line:    '#34548a',
    accent:  '#34548a',
    muted:   '#9699a3',
    surface: '#e9e9ec',   // 比 bg 稍亮
    border:  '#b9bac4',
  },

  // ── Catppuccin（柔和莫卡系） ───────────────────────────────────────────────
  'catppuccin-mocha': {
    bg:      '#1e1e2e',
    fg:      '#cdd6f4',
    line:    '#585b70',
    accent:  '#cba6f7',   // mauve
    muted:   '#6c7086',
    surface: '#313244',   // surface0
    border:  '#45475a',   // surface1
  },
  'catppuccin-latte': {
    bg:      '#eff1f5',
    fg:      '#4c4f69',
    line:    '#9ca0b0',
    accent:  '#8839ef',   // mauve
    muted:   '#9ca0b0',
    surface: '#e6e9ef',   // mantle
    border:  '#ccd0da',   // surface0
  },

  // ── Nord（北欧极光） ────────────────────────────────────────────────────────
  'nord': {
    bg:      '#2e3440',
    fg:      '#d8dee9',
    line:    '#4c566a',
    accent:  '#88c0d0',   // nord8（冰蓝）
    muted:   '#616e88',
    surface: '#3b4252',   // nord1
    border:  '#434c5e',   // nord2
  },
  'nord-light': {
    bg:      '#eceff4',
    fg:      '#2e3440',
    line:    '#aab1c0',
    accent:  '#5e81ac',   // nord10（深蓝）
    muted:   '#7b88a1',
    surface: '#e5e9f0',   // nord5
    border:  '#d8dee9',   // nord4
  },

  // ── Dracula（经典德古拉） ──────────────────────────────────────────────────
  'dracula': {
    bg:      '#282a36',
    fg:      '#f8f8f2',
    line:    '#6272a4',
    accent:  '#bd93f9',   // purple
    muted:   '#6272a4',
    surface: '#44475a',   // current line / selection
    border:  '#6272a4',   // comment 色
  },

  // ── GitHub（官方 IDE 主题） ────────────────────────────────────────────────
  'github-light': {
    bg:      '#ffffff',
    fg:      '#1f2328',
    line:    '#d1d9e0',
    accent:  '#0969da',   // blue-500
    muted:   '#59636e',
    surface: '#f6f8fa',   // neutral-1
    border:  '#d1d9e0',   // border-default
  },
  'github-dark': {
    bg:      '#0d1117',
    fg:      '#e6edf3',
    line:    '#3d444d',
    accent:  '#4493f8',   // blue-400
    muted:   '#9198a1',
    surface: '#161b22',   // canvas-subtle
    border:  '#30363d',   // border-default
  },

  // ── Solarized（精准色温校准） ──────────────────────────────────────────────
  'solarized-light': {
    bg:      '#fdf6e3',
    fg:      '#657b83',
    line:    '#93a1a1',
    accent:  '#268bd2',   // blue
    muted:   '#93a1a1',
    surface: '#eee8d5',   // base2
    border:  '#d3ccb4',   // 介于 base2/base1 之间
  },
  'solarized-dark': {
    bg:      '#002b36',
    fg:      '#839496',
    line:    '#586e75',
    accent:  '#268bd2',   // blue
    muted:   '#586e75',
    surface: '#073642',   // base02
    border:  '#0a4555',   // 稍亮于 surface
  },

  // ── One Dark（Atom 编辑器经典） ────────────────────────────────────────────
  'one-dark': {
    bg:      '#282c34',
    fg:      '#abb2bf',
    line:    '#4b5263',
    accent:  '#c678dd',   // purple
    muted:   '#5c6370',
    surface: '#2c313a',   // 比 bg 略亮
    border:  '#3e4451',   // 背景高亮行
  },
  // 橙色系
  'orange-dark': {
    bg:      '#1c1410',   // 深棕黑
    fg:      '#f5e6d3',   // 暖白
    line:    '#6b4a2e',   // 深橙棕
    accent:  '#f97316',   // 橙色主色 orange-500
    muted:   '#9a6a4a',   // 中性橙棕
    surface: '#2a1e15',   // 比 bg 略亮
    border:  '#3d2b1c',   // 橙棕边框
  },
  'orange-light': {
    bg:      '#fffbf5',   // 暖白底
    fg:      '#431407',   // 深橙棕文字
    line:    '#c2a070',   // 浅橙棕连线
    accent:  '#ea580c',   // 橙色主色 orange-600
    muted:   '#9a6a4a',   // 中性橙棕
    surface: '#fff7ed',   // 浅橙面板背景
    border:  '#fed7aa',   // 浅橙边框 orange-200
  },
};

/** 未指定主题时的默认颜色 */
const THEME_DEFAULTS = {
  bg:      '#FFFFFF',
  fg:      '#27272A',
  line:    '#A1A1AA',
  accent:  '#3F3F46',
  muted:   '#71717A',
  surface: '#F4F4F5',
  border:  '#D4D4D8',
};

// ─────────────────────────────────────────────────────────────────────────────
// §4a  主题元数据（分组、亮暗、推荐预设）
// ─────────────────────────────────────────────────────────────────────────────

/**
 * 主题元数据：提供 dark/light 分类、显示名称、推荐搭配预设
 *
 * recommendedPreset: 该主题搭配哪种样式预设效果最佳
 *   - dark 主题 → glass（深色毛玻璃效果佳）或 modern
 *   - light 主题 → modern 或 outline
 */
const THEME_META = {
  'zinc-light':          { dark: false, label: 'Zinc Light',         family: 'zinc',        recommendedPreset: 'outline'  },
  'zinc-dark':           { dark: true,  label: 'Zinc Dark',          family: 'zinc',        recommendedPreset: 'glass'    },
  'tokyo-night':         { dark: true,  label: 'Tokyo Night',        family: 'tokyo-night', recommendedPreset: 'glass'    },
  'tokyo-night-storm':   { dark: true,  label: 'Tokyo Storm',        family: 'tokyo-night', recommendedPreset: 'modern'   },
  'tokyo-night-light':   { dark: false, label: 'Tokyo Light',        family: 'tokyo-night', recommendedPreset: 'modern'   },
  'catppuccin-mocha':    { dark: true,  label: 'Catppuccin Mocha',   family: 'catppuccin',  recommendedPreset: 'glass'    },
  'catppuccin-latte':    { dark: false, label: 'Catppuccin Latte',   family: 'catppuccin',  recommendedPreset: 'modern'   },
  'nord':                { dark: true,  label: 'Nord',               family: 'nord',        recommendedPreset: 'modern'   },
  'nord-light':          { dark: false, label: 'Nord Light',         family: 'nord',        recommendedPreset: 'outline'  },
  'dracula':             { dark: true,  label: 'Dracula',            family: 'dracula',     recommendedPreset: 'gradient' },
  'github-light':        { dark: false, label: 'GitHub Light',       family: 'github',      recommendedPreset: 'default'  },
  'github-dark':         { dark: true,  label: 'GitHub Dark',        family: 'github',      recommendedPreset: 'modern'   },
  'solarized-light':     { dark: false, label: 'Solarized Light',    family: 'solarized',   recommendedPreset: 'outline'  },
  'solarized-dark':      { dark: true,  label: 'Solarized Dark',     family: 'solarized',   recommendedPreset: 'modern'   },
  'one-dark':            { dark: true,  label: 'One Dark',           family: 'one-dark',    recommendedPreset: 'gradient' },
  'orange-dark':         { dark: true,  label: 'Orange Dark',        family: 'orange',      recommendedPreset: 'glass'    },
  'orange-light':        { dark: false, label: 'Orange Light',       family: 'orange',      recommendedPreset: 'modern'   },
};

// ─────────────────────────────────────────────────────────────────────────────
// §5  视觉样式预设（Preset）—— 5 种
// ─────────────────────────────────────────────────────────────────────────────
// 预设控制形状几何（圆角、描边、阴影）和字体，与主题颜色正交组合。

const STYLE_PRESETS = {
  // 默认样式
  default: {
    name: '默认样式',
    node: {
      borderRadius: 8,
      borderWidth: STROKE_WIDTHS.outerBox * 2,
      shadowBlur: 4,
      shadowColor: 'rgba(0,0,0,0.3)',
    },
    line: {
      width: STROKE_WIDTHS.connector * 2,
      radius: 0,
      arrowSize: ARROW_HEAD.width + ARROW_HEAD.height,   // 13
    },
    font: {
      family: 'system-ui, -apple-system, sans-serif',
      size: FONT_SIZES.nodeLabel,
    },
  },

  // 现代简约
  modern: {
    name: '现代简约',
    node: {
      borderRadius: 16,
      borderWidth: STROKE_WIDTHS.outerBox,
      shadowBlur: 8,
      shadowColor: 'rgba(0,0,0,0.2)',
    },
    line: {
      width: 1.5,
      radius: 5,
      arrowSize: ARROW_HEAD.width + 2,   // 10
    },
    font: {
      family: "'Inter', 'PingFang SC', sans-serif",
      size: FONT_SIZES.nodeLabel,
    },
  },

  // 渐变风格
  gradient: {
    name: '渐变风格',
    node: {
      borderRadius: 12,
      borderWidth: 0,
      shadowBlur: 12,
      shadowColor: 'rgba(122,162,247,0.4)',
    },
    line: {
      width: STROKE_WIDTHS.connector * 2,
      radius: 8,
      arrowSize: ARROW_HEAD.width + ARROW_HEAD.height,
    },
    font: {
      family: "'SF Pro Display', sans-serif",
      size: FONT_SIZES.nodeLabel,
    },
  },

  // 线条轮廓
  outline: {
    name: '线条轮廓',
    node: {
      borderRadius: 4,
      borderWidth: STROKE_WIDTHS.outerBox * 2,
      shadowBlur: 0,
      shadowColor: 'transparent',
    },
    line: {
      width: STROKE_WIDTHS.connector * 2,
      radius: 0,
      arrowSize: ARROW_HEAD.width + ARROW_HEAD.height,
    },
    font: {
      family: MONO_FONT_STACK,
      size: FONT_SIZES.edgeLabel + 2,   // 13
    },
  },

  // 毛玻璃效果
  glass: {
    name: '毛玻璃',
    node: {
      borderRadius: 12,
      borderWidth: STROKE_WIDTHS.outerBox,
      shadowBlur: 16,
      shadowColor: 'rgba(255,255,255,0.1)',
    },
    line: {
      width: 1.5,
      radius: 4,
      arrowSize: ARROW_HEAD.width + 2,
    },
    font: {
      family: "'SF Pro Text', sans-serif",
      size: FONT_SIZES.nodeLabel,
    },
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// §6  CSS 生成函数
// ─────────────────────────────────────────────────────────────────────────────

/**
 * 生成 CSS 样式字符串（Node.js 环境 —— 字符串拼接，无 DOM 依赖）
 * 用于 render.js 的 SVG 样式注入。
 *
 * @param {object} theme  - 主题对象，包含 bg / fg / line 等颜色字段
 * @param {string} preset - 预设名称（default / modern / gradient / outline / glass）
 * @param {string} [svgId] - SVG 根元素的唯一 id（如 'diagram-flow'）。
 *                           传入后所有选择器会被作用域化为 #svgId xxx，
 *                           防止 SVG 内联到 HTML 时跨图表 CSS 污染。
 *                           不传则使用 'svg' 作为根选择器（单独文件场景）。
 */
function generateCSSStyles(theme, preset = 'default', svgId = null) {
  const p = STYLE_PRESETS[preset] || STYLE_PRESETS.default;
  const lineColor = theme.line || theme.fg + '80';
  const borderColor = theme.muted || theme.fg + '40';

  // 根选择器：有 id 时用 #id，否则用 svg（保持向后兼容）
  const root = svgId ? `#${svgId}` : 'svg';

  return `
${root} {
  /* 覆盖 CSS 变量 */
  --_text:       ${theme.fg}       !important;
  --_text-sec:   ${theme.muted  || theme.fg + '80'} !important;
  --_line:       ${lineColor}      !important;
  --_arrow:      ${lineColor}      !important;
  --_node-fill:  ${theme.bg}       !important;
  --_node-stroke:${borderColor}    !important;
  --_group-fill: ${theme.accent ? theme.accent + '18' : theme.fg + '0a'} !important;
  --_group-hdr:  ${theme.accent || theme.fg} !important;
}
${root} text {
  font-family: ${p.font.family} !important;
  font-size:   ${p.font.size}px !important;
  dominant-baseline: central;
  dy: ${TEXT_BASELINE_SHIFT};
}
/* 直接覆盖元素属性 */
${root} rect[fill="var(--_node-fill)"],
${root} circle[fill="var(--_node-fill)"],
${root} ellipse[fill="var(--_node-fill)"],
${root} polygon[fill="var(--_node-fill)"] {
  fill:         ${theme.bg}        !important;
  stroke:       ${borderColor}     !important;
  stroke-width: ${p.node.borderWidth}px !important;
  rx:           ${p.node.borderRadius}px !important;
  ry:           ${p.node.borderRadius}px !important;
  filter: drop-shadow(0 ${p.node.shadowBlur / 2}px ${p.node.shadowBlur}px ${p.node.shadowColor}) !important;
}
/* 节点文字 */
${root} g.node text {
  fill: ${theme.fg} !important;
}
/* 子图/cluster 标题 */
${root} .cluster-label text {
  fill:        ${theme.accent || theme.fg} !important;
  font-size:   ${FONT_SIZES.groupHeader}px !important;
  font-weight: ${FONT_WEIGHTS.groupHeader} !important;
}
/* 边/连线 */
${root} .edge, ${root} .edgePath .path {
  stroke:       ${lineColor}  !important;
  stroke-width: ${p.line.width}px !important;
}
${root} path {
  stroke:       ${lineColor}  !important;
  stroke-width: ${p.line.width}px !important;
}
/* 箭头 */
${root} .arrowhead polygon,
${root} marker polygon {
  stroke: ${lineColor} !important;
  fill:   ${lineColor} !important;
}
/* 边标签 */
${root} .edgeLabel text {
  fill:      ${theme.muted || theme.fg} !important;
  font-size: ${FONT_SIZES.edgeLabel}px  !important;
}`;
}

// 自增计数器，用于生成唯一 SVG id（每次进程内递增）
let _svgIdCounter = 0;

/**
 * 将 CSS 样式注入 SVG（Node.js 版本，无需 DOMParser）
 * 用于 render.js 的 CLI 渲染流程。
 *
 * 除注入样式外，还会：
 * 1. 给 SVG 根元素注入唯一 id（svgId），防止内联到 HTML 时跨图表 CSS 污染
 * 2. 用 svgId 作用域化所有内部 <style> 选择器（svg {} → #id {}，text {} → #id text {} 等）
 * 3. 在 SVG 的 style 属性中补全 --_line / --_arrow 等映射变量，确保独立用软件打开 SVG 时线条有颜色
 * 4. 修复 SVG 的 width/height 属性：
 *    - 若 width 或 height 是百分比（如 "100%"），从 viewBox 推算实际像素值写回
 *    - 若没有 viewBox 但有具体 width/height，补全 viewBox
 *
 * @param {string}  svgString  - 原始 SVG 字符串
 * @param {object}  theme      - 完整主题对象（含 bg/fg/line/accent/muted/surface/border）
 * @param {string}  [preset]   - 样式预设名称，默认 'default'
 * @param {string}  [svgId]    - 可选：指定 SVG 根元素 id；不传则自动生成 bm-diagram-N
 */
function injectStylesToSVG(svgString, theme, preset = 'default', svgId = null) {
  // 自动生成唯一 id（若未指定）
  const effectiveSvgId = svgId || `bm-diagram-${++_svgIdCounter}`;

  const css = generateCSSStyles(theme, preset, effectiveSvgId);
  const styleTag = `<style>${css}</style>`;

  // ── Step 1：修复 SVG 的 width/height，注入唯一 id，补全下划线 CSS 变量 ──
  let fixed = svgString;

  // 提取 <svg ...> 开标签（包含所有属性）
  const svgTagMatch = fixed.match(/<svg([^>]*)>/);
  if (svgTagMatch) {
    let attrs = svgTagMatch[1];

    // 提取当前 width / height / viewBox / id / style
    const wMatch     = attrs.match(/\bwidth\s*=\s*["']([^"']*)["']/);
    const hMatch     = attrs.match(/\bheight\s*=\s*["']([^"']*)["']/);
    const vbMatch    = attrs.match(/\bviewBox\s*=\s*["']([^"']*)["']/);
    const idMatch    = attrs.match(/\bid\s*=\s*["']([^"']*)["']/);
    const styleMatch = attrs.match(/\bstyle\s*=\s*["']([^"']*)["']/);

    const w  = wMatch  ? wMatch[1].trim()  : null;
    const h  = hMatch  ? hMatch[1].trim()  : null;
    const vb = vbMatch ? vbMatch[1].trim() : null;

    // 判断是否为有效像素数值（纯数字，不含 %、px、em 等单位）
    const isPixel = (v) => v != null && /^\d+(\.\d+)?$/.test(v);

    let newW = w, newH = h;
    let newVb = vb;

    // 如果 width 或 height 不是有效像素值，尝试从 viewBox 推算
    if (vb && (!isPixel(w) || !isPixel(h))) {
      const parts = vb.split(/[\s,]+/).map(Number);
      if (parts.length >= 4 && parts[2] > 0 && parts[3] > 0) {
        if (!isPixel(w)) newW = String(parts[2]);
        if (!isPixel(h)) newH = String(parts[3]);
      }
    }

    // 如果没有 viewBox，但有具体 width/height，补全 viewBox
    if (!vb && isPixel(newW) && isPixel(newH)) {
      newVb = `0 0 ${newW} ${newH}`;
    }

    // 重新构建 <svg> 开标签
    let newAttrs = attrs;

    // 1a. 修复 width/height/viewBox
    const changed = (newW !== w) || (newH !== h) || (newVb !== vb);
    if (changed) {
      if (newW !== w) {
        if (wMatch) newAttrs = newAttrs.replace(wMatch[0], `width="${newW}"`);
        else        newAttrs = newAttrs + ` width="${newW}"`;
      }
      if (newH !== h) {
        if (hMatch) newAttrs = newAttrs.replace(hMatch[0], `height="${newH}"`);
        else        newAttrs = newAttrs + ` height="${newH}"`;
      }
      if (!vb && newVb) {
        newAttrs = newAttrs + ` viewBox="${newVb}"`;
      }
    }

    // 1b. 注入唯一 id（若已有 id 则覆盖，保持幂等）
    if (idMatch) {
      newAttrs = newAttrs.replace(idMatch[0], `id="${effectiveSvgId}"`);
    } else {
      newAttrs = newAttrs + ` id="${effectiveSvgId}"`;
    }

    // 1c. 在 style 属性中补全 --_xxx 映射变量，解决独立打开 SVG 时线条/箭头无颜色的问题
    //     原因：SVG 内部元素用 stroke="var(--_line)"，这些变量通常由第二个 <style> 块
    //     通过 CSS 继承从 --line 映射而来，但独立打开 SVG 时该 CSS 可能不生效。
    //     直接在 style 属性里内联精确颜色值是最稳健的方案。
    const lineColor   = theme.line   || (theme.fg + '80');
    const borderColor = theme.muted  || (theme.fg + '40');
    const accentColor = theme.accent || theme.fg;
    const extraVars = [
      `--_line:${lineColor}`,
      `--_arrow:${lineColor}`,
      `--_text:${theme.fg}`,
      `--_text-sec:${theme.muted || theme.fg + '80'}`,
      `--_text-muted:${theme.muted || theme.fg + '80'}`,
      `--_node-fill:${theme.bg}`,
      `--_node-stroke:${borderColor}`,
      `--_group-fill:${accentColor + '18'}`,
      `--_group-hdr:${accentColor}`,
      `--_inner-stroke:${borderColor}`,
    ].join(';');

    if (styleMatch) {
      // 已有 style 属性：追加变量（避免重复，先去掉相同 key）
      let existingStyle = styleMatch[1];
      // 去掉已存在的 --_xxx: 声明（防止重复）
      existingStyle = existingStyle.replace(/--_[a-z-]+:[^;]+;?/g, '');
      // 补全 background: 颜色（如果还没设置）
      if (!existingStyle.includes('background')) {
        existingStyle += `;background:${theme.bg}`;
      }
      const newStyle = `${existingStyle};${extraVars}`.replace(/^;+/, '');
      newAttrs = newAttrs.replace(styleMatch[0], `style="${newStyle}"`);
    } else {
      newAttrs = newAttrs + ` style="background:${theme.bg};${extraVars}"`;
    }

    fixed = fixed.replace(svgTagMatch[0], `<svg${newAttrs}>`);
  }

  // ── Step 2：在 <svg> 开标签之后注入样式 ──
  const svgOpenEnd = fixed.indexOf('>');
  if (svgOpenEnd === -1) return fixed;

  return fixed.slice(0, svgOpenEnd + 1) + '\n' + styleTag + fixed.slice(svgOpenEnd + 1);
}

/**
 * 应用样式到 SVG 字符串（浏览器版本，依赖 DOMParser / XMLSerializer）
 * 用于 preview.html 等浏览器环境。
 */
function applyStylesToSVG(svgString, theme, preset = 'default', options = {}) {
  const {
    transparentBg = false,
    includeFonts   = true,
    width          = null,
    height         = null,
    fontFamily     = null,
    fontSize       = null,
  } = options;

  const parser = new DOMParser();
  const doc    = parser.parseFromString(svgString, 'image/svg+xml');
  const svgEl  = doc.querySelector('svg');

  if (!svgEl) return svgString;

  const styleEl = document.createElementNS('http://www.w3.org/2000/svg', 'style');
  const p       = STYLE_PRESETS[preset] || STYLE_PRESETS.default;

  const customFontFamily = fontFamily || p.font.family;
  const customFontSize   = fontSize   || p.font.size;
  const lineColor        = theme.line || theme.fg + '80';
  const borderColor      = theme.muted || theme.fg + '40';

  styleEl.textContent = `
    .node rect,
    .node circle,
    .node ellipse,
    .node polygon {
      fill:         ${theme.bg}         !important;
      stroke:       ${borderColor}      !important;
      stroke-width: ${p.node.borderWidth}px !important;
      rx:           ${p.node.borderRadius}px !important;
      ry:           ${p.node.borderRadius}px !important;
      filter: drop-shadow(0 ${p.node.shadowBlur / 2}px ${p.node.shadowBlur}px ${p.node.shadowColor}) !important;
    }
    .node text {
      fill:        ${theme.fg}          !important;
      font-family: ${customFontFamily}  !important;
      font-size:   ${customFontSize}px  !important;
      dominant-baseline: central;
      dy: ${TEXT_BASELINE_SHIFT};
    }
    .cluster-label text {
      fill:        ${theme.accent || theme.fg} !important;
      font-size:   ${FONT_SIZES.groupHeader}px !important;
      font-weight: ${FONT_WEIGHTS.groupHeader} !important;
    }
    .edgePath .path {
      stroke:       ${lineColor}  !important;
      stroke-width: ${p.line.width}px !important;
    }
    .edgeLabel text {
      fill:      ${theme.muted || theme.fg} !important;
      font-size: ${FONT_SIZES.edgeLabel}px  !important;
    }
    .arrowhead,
    marker polygon {
      stroke: ${lineColor} !important;
      fill:   ${lineColor} !important;
    }
  `;
  svgEl.insertBefore(styleEl, svgEl.firstChild);

  if (includeFonts) {
    svgEl.setAttribute('font-family', customFontFamily);
  }
  if (width)  svgEl.setAttribute('width',  width);
  if (height) svgEl.setAttribute('height', height);

  if (!transparentBg) {
    const bgRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    bgRect.setAttribute('width',  '100%');
    bgRect.setAttribute('height', '100%');
    bgRect.setAttribute('fill',   theme.bg);
    svgEl.insertBefore(bgRect, svgEl.firstChild);
  }

  const serializer = new XMLSerializer();
  return serializer.serializeToString(svgEl);
}

// ─────────────────────────────────────────────────────────────────────────────
// §7  工具函数
// ─────────────────────────────────────────────────────────────────────────────

/** 获取可用预设名称列表 */
function getPresetNames() {
  return Object.keys(STYLE_PRESETS);
}

/** 获取预设配置 */
function getPreset(presetName) {
  return STYLE_PRESETS[presetName] || null;
}

/** 验证预设名称 */
function isValidPreset(presetName) {
  return presetName in STYLE_PRESETS;
}

/** 获取主题配置（按名称） */
function getTheme(themeName) {
  return THEMES[themeName] || null;
}

/** 获取所有主题名称 */
function getThemeNames() {
  return Object.keys(THEMES);
}

/** 验证主题名称 */
function isValidTheme(themeName) {
  return themeName in THEMES;
}

// ─────────────────────────────────────────────────────────────────────────────
// §7a  主题元数据工具函数
// ─────────────────────────────────────────────────────────────────────────────

/**
 * 获取主题元数据（dark标志、label、family、推荐预设）
 * @param {string} themeName
 * @returns {{ dark: boolean, label: string, family: string, recommendedPreset: string } | null}
 */
function getThemeMeta(themeName) {
  return THEME_META[themeName] || null;
}

/**
 * 获取所有暗色主题名称列表
 * @returns {string[]}
 */
function getDarkThemes() {
  return Object.keys(THEME_META).filter(k => THEME_META[k].dark);
}

/**
 * 获取所有亮色主题名称列表
 * @returns {string[]}
 */
function getLightThemes() {
  return Object.keys(THEME_META).filter(k => !THEME_META[k].dark);
}

/**
 * 按 family 分组返回主题名称数组
 * @returns {{ [family: string]: string[] }}
 */
function getThemesByFamily() {
  const groups = {};
  for (const [name, meta] of Object.entries(THEME_META)) {
    if (!groups[meta.family]) groups[meta.family] = [];
    groups[meta.family].push(name);
  }
  return groups;
}

/**
 * 获取某主题的推荐搭配预设
 * @param {string} themeName
 * @returns {string}  预设名称，未知主题时返回 'default'
 */
function getRecommendedPreset(themeName) {
  const meta = THEME_META[themeName];
  return meta ? meta.recommendedPreset : 'default';
}

/**
 * 解析并补全主题对象 —— 确保返回包含全部 7 个字段的完整主题对象。
 * 输入可以是：主题名称字符串、部分主题对象、或 null（返回默认值）。
 *
 * @param {string | object | null} themeInput  主题名称或主题对象
 * @returns {{ bg, fg, line, accent, muted, surface, border }}
 */
function resolveTheme(themeInput) {
  let base;

  if (typeof themeInput === 'string') {
    base = THEMES[themeInput] || THEME_DEFAULTS;
  } else if (themeInput && typeof themeInput === 'object') {
    base = themeInput;
  } else {
    base = THEME_DEFAULTS;
  }

  // 用 THEME_DEFAULTS 补全缺省字段
  return {
    bg:      base.bg      || THEME_DEFAULTS.bg,
    fg:      base.fg      || THEME_DEFAULTS.fg,
    line:    base.line    || base.fg + '80' || THEME_DEFAULTS.line,
    accent:  base.accent  || base.fg       || THEME_DEFAULTS.accent,
    muted:   base.muted   || base.fg + '80' || THEME_DEFAULTS.muted,
    surface: base.surface || base.bg       || THEME_DEFAULTS.surface,
    border:  base.border  || base.line     || base.fg + '40' || THEME_DEFAULTS.border,
  };
}

/**
 * 判断颜色对比度是否足够（WCAG AA 近似检测）
 * 用途：帮助 AI 在推荐主题时判断 fg/bg 对是否可读
 *
 * @param {string} hex1  十六进制颜色（如 '#1a1b26'）
 * @param {string} hex2  十六进制颜色
 * @returns {number}     相对亮度对比比值（>= 4.5 为 WCAG AA）
 */
function colorContrast(hex1, hex2) {
  function luminance(hex) {
    const r = parseInt(hex.slice(1, 3), 16) / 255;
    const g = parseInt(hex.slice(3, 5), 16) / 255;
    const b = parseInt(hex.slice(5, 7), 16) / 255;
    const channel = c => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
  }
  const L1 = luminance(hex1);
  const L2 = luminance(hex2);
  const lighter = Math.max(L1, L2);
  const darker  = Math.min(L1, L2);
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * 检测一个主题的可读性评分（bg vs fg 的对比度）
 * @param {string} themeName
 * @returns {{ contrast: number, passAA: boolean, passAAA: boolean }}
 */
function checkThemeReadability(themeName) {
  const theme = THEMES[themeName];
  if (!theme) return null;
  const contrast = colorContrast(theme.bg, theme.fg);
  return {
    contrast: Math.round(contrast * 10) / 10,
    passAA:   contrast >= 4.5,
    passAAA:  contrast >= 7.0,
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// §8  导出
// ─────────────────────────────────────────────────────────────────────────────

module.exports = {
  // 字体度量
  MONO_FONT,
  MONO_FONT_STACK,
  estimateMonoTextWidth,

  // 几何常量（源自 src/styles.ts）
  FONT_SIZES,
  FONT_WEIGHTS,
  NODE_PADDING,
  STROKE_WIDTHS,
  TEXT_BASELINE_SHIFT,
  ARROW_HEAD,
  GROUP_HEADER_CONTENT_PAD,

  // 主题（15 个，源自 src/theme.ts，已补全 surface/border）
  THEMES,
  THEME_DEFAULTS,
  THEME_META,
  // 主题查询
  getTheme,
  getThemeNames,
  isValidTheme,
  // 主题元数据工具
  getThemeMeta,
  getDarkThemes,
  getLightThemes,
  getThemesByFamily,
  getRecommendedPreset,
  resolveTheme,
  // 对比度检测
  colorContrast,
  checkThemeReadability,

  // 视觉预设（5 个）
  STYLE_PRESETS,
  getPresetNames,
  getPreset,
  isValidPreset,

  // CSS / SVG 生成
  generateCSSStyles,
  injectStylesToSVG,
  applyStylesToSVG,
};
