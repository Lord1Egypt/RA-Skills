#!/usr/bin/env node

/**
 * 图表类型 → 中文标签（与 preview.html 一一对应）
 * 必须在所有函数之前定义（analyzeContent 等会调用 getTypeLabel）
 */
const TYPE_LABEL = {
  'Flowchart': '流程图',
  'Sequence':  '时序图',
  'State':     '状态图',
  'Class':     '类图',
  'ER':        'ER图',
  'XY Chart':  '图表',
  'Gantt':     '甘特图',
  'Pie':       '饼图',
  'Timeline':  '时间轴',
  'Mindmap':   '思维导图',
};
function getTypeLabel(type) {
  return TYPE_LABEL[type] || type;
}

/**
 * Beautiful Mermaid — Rich HTML Generator
 *
 * 将多个 Mermaid 图表渲染为内容丰富的展示 HTML
 * 包含：顶部 Badge、标签页导航、信息卡片网格、SVG 图表展示、页脚说明
 *
 * 用法:
 *   node scripts/rich-html.js <title> --diagrams <file1.mmd> [file2.mmd ...] [options]
 *   node scripts/rich-html.js <title> --batch <dir> [options]
 *
 * 选项:
 *   --diagrams      指定要渲染的 .mmd 文件列表（至少 1 个）
 *   --batch         批量读取目录下所有 .mmd 文件
 *   --theme, -t     主题名称（默认: tokyo-night）
 *   --preset, -p    样式预设（默认: glass）
 *   --output, -o    输出 HTML 路径（默认: result.html）
 *   --subtitle      副标题文字
 *   --help, -h      显示帮助
 *
 * 图表元数据（可选，在 .mmd 注释中声明，格式见下方说明）:
 *   # @title  图表标题
 *   # @desc   图表描述
 *   # @icon   图标 emoji
 *   # @meta   key:value|key:value  (显示在信息卡片中，最多4个)
 *
 * 示例:
 *   node scripts/rich-html.js "秒杀系统" \
 *     --diagrams assets/examples/flowchart-basic.mmd assets/examples/system-architecture.mmd \
 *     --theme tokyo-night --preset glass \
 *     --output result.html
 */

const fs = require('fs');
const path = require('path');

const {
  STYLE_PRESETS,
  THEMES: LOCAL_THEMES,
  injectStylesToSVG,
  isValidPreset,
  resolveTheme,
  getRecommendedPreset,
} = require('./styles');

// ─── CLI 参数解析 ───────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    title: null,
    subtitle: null,
    diagrams: [],
    batch: null,
    theme: 'tokyo-night',
    preset: null,
    output: 'result.html',
  };

  let i = 0;
  // 第一个非 flag 参数作为 title
  if (args.length > 0 && !args[0].startsWith('-')) {
    options.title = args[0];
    i = 1;
  }

  for (; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--diagrams':
        // 收集后续所有非 flag 参数直到遇到下一个 flag
        while (i + 1 < args.length && !args[i + 1].startsWith('-')) {
          options.diagrams.push(args[++i]);
        }
        break;
      case '--batch':
        options.batch = args[++i];
        break;
      case '--theme':
      case '-t':
        options.theme = args[++i];
        break;
      case '--preset':
      case '-p':
        options.preset = args[++i];
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--subtitle':
        options.subtitle = args[++i];
        break;
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
        break;
      default:
        if (!arg.startsWith('-') && !options.title) {
          options.title = arg;
        }
        break;
    }
  }

  return options;
}

function showHelp() {
  console.log(`
Beautiful Mermaid — Rich HTML Generator
========================================

用法:
  node scripts/rich-html.js <title> --diagrams <file1.mmd> [file2.mmd ...] [options]
  node scripts/rich-html.js <title> --batch <dir> [options]

选项:
  --diagrams        指定要渲染的 .mmd 文件路径列表
  --batch <dir>     批量读取目录下所有 .mmd 文件
  --theme, -t       主题名称 (默认: tokyo-night)
                    可选: tokyo-night | dracula | github-dark | nord | catppuccin-mocha 等
  --preset, -p      样式预设 (默认: 主题推荐值)
                    可选: default | modern | gradient | outline | glass
  --output, -o      输出 HTML 路径 (默认: result.html)
  --subtitle        页面副标题

图表元数据 (在 .mmd 文件注释中声明):
  # @title  图表标题
  # @desc   图表描述
  # @icon   图标 emoji (默认: 📊)
  # @meta   标签:值|标签:值|... (最多4组，显示在信息卡片中)
  # @type   图表类型说明 (显示在第一张信息卡片)

示例:
  node scripts/rich-html.js "系统架构" \\
    --diagrams assets/examples/system-architecture.mmd assets/examples/flowchart-basic.mmd \\
    --theme tokyo-night --preset glass \\
    --output my-report.html

  node scripts/rich-html.js "所有示例" \\
    --batch assets/examples \\
    --theme dracula --preset gradient \\
    --output examples-report.html
`);
}

// ─── 元数据解析 + 内容智能分析 ──────────────────────────────────────────────

/**
 * 推断图表类型（从代码首行）
 */
function inferDiagramType(codeLines) {
  const first = codeLines.find(l => l.trim() && !l.trim().startsWith('#'));
  if (!first) return { type: 'Diagram', typeDetail: '通用图表' };
  const t = first.trim().toLowerCase();
  if (t.startsWith('graph td') || t.startsWith('graph tb'))    return { type: 'Flowchart', typeDetail: '自上而下流程图' };
  if (t.startsWith('graph lr') || t.startsWith('graph rl'))    return { type: 'Flowchart', typeDetail: '左右布局流程图' };
  if (t.startsWith('graph'))                                    return { type: 'Flowchart', typeDetail: '有向流程图' };
  if (t.startsWith('flowchart td') || t.startsWith('flowchart tb')) return { type: 'Flowchart', typeDetail: '自上而下流程图' };
  if (t.startsWith('flowchart lr'))                             return { type: 'Flowchart', typeDetail: '左右布局流程图' };
  if (t.startsWith('flowchart'))                                return { type: 'Flowchart', typeDetail: '有向流程图' };
  if (t.startsWith('sequencediagram'))                          return { type: 'Sequence',  typeDetail: '时序/交互图' };
  if (t.startsWith('statediagram-v2'))                          return { type: 'State',     typeDetail: '状态机 v2' };
  if (t.startsWith('statediagram'))                             return { type: 'State',     typeDetail: '有限状态机' };
  if (t.startsWith('classdiagram'))                             return { type: 'Class',     typeDetail: 'UML 类图' };
  if (t.startsWith('erdiagram'))                                return { type: 'ER',        typeDetail: '实体关系图' };
  if (t.startsWith('xychart-beta') || t.startsWith('xychart')) return { type: 'XY Chart',  typeDetail: '柱/折线数据图' };
  if (t.startsWith('gantt'))                                    return { type: 'Gantt',     typeDetail: '项目甘特图' };
  if (t.startsWith('pie'))                                      return { type: 'Pie',       typeDetail: '饼图' };
  if (t.startsWith('timeline'))                                 return { type: 'Timeline',  typeDetail: '时间线图' };
  if (t.startsWith('mindmap'))                                  return { type: 'Mindmap',   typeDetail: '思维导图' };
  if (t.startsWith('block'))                                    return { type: 'Block',     typeDetail: '块状图' };
  return { type: 'Diagram', typeDetail: '通用图表' };
}

/**
 * 对 Mermaid 代码进行内容分析，自动生成多维度信息卡片
 * 返回 4 个信息卡片对象 [{label, value, detail}]，全部基于实际内容
 */
function analyzeContent(content, diagramType, manualCards) {
  // 如果用户手动声明了 @meta，优先使用（但仍在第一位加类型卡片）
  if (manualCards && manualCards.length > 0) {
    const cards = [
      { label: '图表类型', value: getTypeLabel(diagramType.type), detail: diagramType.typeDetail },
      ...manualCards.map(c => ({ label: c.label, value: c.value, detail: '' }))
    ].slice(0, 4);
    return cards;
  }

  // 去掉注释行，只保留代码行
  const codeLines = content
    .split('\n')
    .filter(l => l.trim() && !l.trim().startsWith('#'));

  switch (diagramType.type) {
    case 'Flowchart':   return analyzeFlowchart(codeLines, diagramType);
    case 'Sequence':    return analyzeSequence(codeLines, diagramType);
    case 'State':       return analyzeState(codeLines, diagramType);
    case 'Class':       return analyzeClass(codeLines, diagramType);
    case 'ER':          return analyzeER(codeLines, diagramType);
    case 'XY Chart':    return analyzeXYChart(codeLines, diagramType);
    case 'Gantt':       return analyzeGantt(codeLines, diagramType);
    case 'Pie':         return analyzePie(codeLines, diagramType);
    case 'Timeline':    return analyzeTimeline(codeLines, diagramType);
    default:            return analyzeGeneric(codeLines, diagramType);
  }
}

/** Flowchart / 流程图分析 */
function analyzeFlowchart(lines, dt) {
  // 统计节点（字母/中文 ID 的声明行，排除方向声明）
  const nodeLines = lines.filter(l =>
    /^[\s]*[A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_-]*[\s]*[\[({>|\[]/.test(l) ||
    /^[\s]*[A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_-]*[\s]*["']/.test(l)
  );
  // 统计连线（--> / --- / ==> / -.->）
  const edgeLines = lines.filter(l => /-->|--[-o*x]?|==+>|[-.]->/.test(l));
  // 统计子图
  const subgraphCount = lines.filter(l => /^\s*subgraph\b/.test(l.toLowerCase())).length;
  // 统计判断节点（菱形 {}）
  const branchCount = lines.filter(l => /\{[^}]+\}/.test(l)).length;

  const nodeCount = Math.max(nodeLines.length, countUniqueNodes(lines));
  const edgeCount = edgeLines.length;

  const cards = [
    { label: '图表类型', value: getTypeLabel(dt.type), detail: dt.typeDetail },
    { label: '节点总数', value: `${nodeCount} 个`, detail: subgraphCount > 0 ? `含 ${subgraphCount} 个子图` : (branchCount > 0 ? `${branchCount} 个判断分支` : '纯线性流程') },
    { label: '连接数量', value: `${edgeCount} 条`, detail: edgeCount > nodeCount ? '分支较多' : '主干流程' },
    subgraphCount > 0
      ? { label: '分层结构', value: `${subgraphCount} 层`, detail: '含子图分组' }
      : { label: '判断分支', value: `${branchCount} 处`, detail: branchCount > 3 ? '复杂分支' : (branchCount > 0 ? '有条件分支' : '顺序流程') },
  ];
  return cards;
}

/** 统计唯一节点 ID 数量（从箭头行拆出节点 ID） */
function countUniqueNodes(lines) {
  const nodeIds = new Set();
  const edgeLines = lines.filter(l => /-->|--[-o*x]?|==+>|[-.]->/.test(l));
  for (const line of edgeLines) {
    // 拆出连线两端节点 ID（简单正则）
    const parts = line.split(/-->|--[-o*x]?|==+>|[-.]->/).map(p => p.trim());
    for (const part of parts) {
      // 提取 ID（字母数字中文开头，后跟 [、(、{、> 等）
      const m = part.match(/^([A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_-]*)/);
      if (m) nodeIds.add(m[1]);
    }
  }
  return nodeIds.size;
}

/** Sequence / 时序图分析 */
function analyzeSequence(lines, dt) {
  // 统计参与者（participant / actor 声明 + 箭头行里出现的 ID）
  const participants = new Set();
  lines.forEach(l => {
    const pm = l.match(/^\s*(?:participant|actor)\s+(.+?)(?:\s+as\s+|$)/i);
    if (pm) participants.add(pm[1].trim());
    // 从箭头行 A->>B 提取
    const am = l.match(/^\s*([^\s:]+)\s*-[->>xo]+\s*([^\s:]+)/);
    if (am) { participants.add(am[1].trim()); participants.add(am[2].trim()); }
  });

  // 统计消息/交互数量（包含 --> / ->> / -->> 等箭头行）
  const msgLines = lines.filter(l => /^\s*[^\s]+\s*-[->>xo]+\s*[^\s:]+\s*:/.test(l));
  // 统计 loop / alt / opt 块
  const loopCount = lines.filter(l => /^\s*loop\b/.test(l.toLowerCase())).length;
  const altCount  = lines.filter(l => /^\s*(?:alt|opt|par|critical)\b/.test(l.toLowerCase())).length;
  // 统计激活块
  const activateCount = lines.filter(l => /^\s*activate\b/.test(l.toLowerCase())).length;

  // 去掉 ":" 之前后可能的杂项
  const cleanParts = Array.from(participants).filter(p =>
    !p.includes(':') && !p.startsWith('Note') && p.length < 40
  );

  return [
    { label: '图表类型',   value: getTypeLabel(dt.type),     detail: dt.typeDetail },
    { label: '参与角色',   value: `${cleanParts.length} 个`, detail: cleanParts.slice(0, 3).join(' / ') + (cleanParts.length > 3 ? ' …' : '') },
    { label: '消息交互',   value: `${msgLines.length} 次`,   detail: loopCount > 0 ? `含 ${loopCount} 个循环块` : (altCount > 0 ? `含 ${altCount} 个分支块` : '顺序交互') },
    activateCount > 0
      ? { label: '激活区段', value: `${activateCount} 处`, detail: '标注服务处理阶段' }
      : { label: '分支/条件', value: `${altCount} 处`, detail: altCount > 0 ? '含条件/可选路径' : '无条件分支' },
  ];
}

/** State / 状态图分析 */
function analyzeState(lines, dt) {
  // 统计状态（state 声明 + 转换行 A --> B 中的 ID）
  const states = new Set();
  lines.forEach(l => {
    const sm = l.match(/^\s*state\s+"?([^"{\n]+)"?\s*/i);
    if (sm) states.add(sm[1].trim());
    const tm = l.match(/^\s*([^\s]+)\s*-->\s*([^\s:]+)/);
    if (tm) { states.add(tm[1].trim()); states.add(tm[2].trim()); }
  });
  // 过滤掉 [*]（初始/终止伪态）
  states.delete('[*]');

  // 统计转换数
  const transitions = lines.filter(l => /^\s*[^\s]+\s*-->\s*[^\s]/.test(l)).length;
  // 统计嵌套状态（state xxx {）
  const nestedCount = lines.filter(l => /^\s*state\s+.+\s*\{/.test(l)).length;
  // 统计 note 标注
  const noteCount = lines.filter(l => /^\s*note\b/.test(l.toLowerCase())).length;

  return [
    { label: '图表类型', value: getTypeLabel(dt.type),                  detail: dt.typeDetail },
    { label: '状态节点', value: `${states.size} 个`,       detail: nestedCount > 0 ? `含 ${nestedCount} 组嵌套状态` : '扁平状态机' },
    { label: '状态转换', value: `${transitions} 条`,       detail: transitions > states.size * 1.5 ? '多路转换' : '线性流程' },
    noteCount > 0
      ? { label: '注释标注', value: `${noteCount} 处`, detail: '关键状态有说明' }
      : { label: '嵌套结构', value: nestedCount > 0 ? `${nestedCount} 层` : '无', detail: nestedCount > 0 ? '含子状态机' : '单层扁平' },
  ];
}

/** Class / 类图分析 */
function analyzeClass(lines, dt) {
  // 统计类（class xxx 或 xxx : ）
  const classes = new Set();
  lines.forEach(l => {
    const cm = l.match(/^\s*class\s+([A-Za-z_]\w*)/);
    if (cm) classes.add(cm[1]);
    const im = l.match(/^\s*([A-Za-z_]\w*)\s*:/);
    if (im && im[1] !== 'note') classes.add(im[1]);
  });
  // 统计关系（-- / --> / ..> / --|> / --o / --* 等）
  const relations = lines.filter(l => /--|<|>|\.\./.test(l) && !l.trim().startsWith('%%')).length;
  // 统计方法
  const methods = lines.filter(l => /\+|\-|\#.*\(/.test(l)).length;
  // 统计接口/抽象（<<interface>> <<abstract>> <<service>>）
  const interfaceCount = lines.filter(l => /<<[a-zA-Z]+>>/.test(l)).length;

  return [
    { label: '图表类型', value: getTypeLabel(dt.type),                    detail: dt.typeDetail },
    { label: '类/接口',  value: `${classes.size} 个`,        detail: interfaceCount > 0 ? `含 ${interfaceCount} 个注解标记` : '纯类结构' },
    { label: '类关系',   value: `${relations} 条`,           detail: '继承/组合/依赖' },
    { label: '方法成员', value: `${methods} 个`,             detail: methods > 10 ? '功能丰富' : (methods > 0 ? '适中规模' : '待补全') },
  ];
}

/** ER / 实体关系图分析 */
function analyzeER(lines, dt) {
  const entities = new Set();
  lines.forEach(l => {
    // 关系行: EntityA }|--|| EntityB : "..."
    const rm = l.match(/^\s*([A-Za-z_]\w*)\s+[|}o{|*]+[|-]+[|}o{|*]+\s+([A-Za-z_]\w*)/);
    if (rm) { entities.add(rm[1]); entities.add(rm[2]); }
    // 实体声明 entity {
    const em = l.match(/^\s*([A-Za-z_]\w*)\s*\{/);
    if (em) entities.add(em[1]);
  });
  // 统计关系（含关系说明行）
  const relations = lines.filter(l => /[|}o]{1,2}--?[|}o]{1,2}/.test(l)).length;
  // 统计属性行（type name）
  const attrLines = lines.filter(l => /^\s+[a-z][a-zA-Z]*\s+\w+/.test(l)).length;

  return [
    { label: '图表类型', value: getTypeLabel(dt.type),               detail: dt.typeDetail },
    { label: '实体数量', value: `${entities.size} 个`,  detail: '数据建模核心' },
    { label: '关联关系', value: `${relations} 条`,      detail: '含基数约束' },
    { label: '属性字段', value: `${attrLines} 个`,      detail: attrLines > 10 ? '字段较多' : '精简设计' },
  ];
}

/** XY Chart / 数据图分析 */
function analyzeXYChart(lines, dt) {
  // 提取 x-axis 标签数量
  const xAxis = lines.find(l => /^\s*x-axis/.test(l.toLowerCase()));
  let xCount = 0;
  if (xAxis) {
    const m = xAxis.match(/\[([^\]]+)\]/);
    if (m) xCount = m[1].split(',').length;
  }
  // 统计数据集（bar / line 行）
  const barLines  = lines.filter(l => /^\s*bar\s+\[/.test(l.toLowerCase())).length;
  const lineCharts = lines.filter(l => /^\s*line\s+\[/.test(l.toLowerCase())).length;
  // 提取 y-axis 范围
  const yAxis = lines.find(l => /^\s*y-axis/.test(l.toLowerCase()));
  let yRange = '自动';
  if (yAxis) {
    const m = yAxis.match(/(\d+)\s*-->\s*(\d+)/);
    if (m) yRange = `${m[1]} ~ ${m[2]}`;
  }

  return [
    { label: '图表类型', value: getTypeLabel(dt.type),            detail: dt.typeDetail },
    { label: 'X 轴分类', value: `${xCount} 组`,     detail: '数据分类维度' },
    { label: '数据系列', value: `${barLines + lineCharts} 条`, detail: `柱 ${barLines} / 折线 ${lineCharts}` },
    { label: 'Y 轴范围', value: yRange,             detail: '数值展示区间' },
  ];
}

/** Gantt / 甘特图分析 */
function analyzeGantt(lines, dt) {
  // 统计任务
  const taskLines = lines.filter(l => /^\s+\w.*:/.test(l) && !l.trim().startsWith('section')).length;
  // 统计 section
  const sectionCount = lines.filter(l => /^\s*section\s/.test(l.toLowerCase())).length;
  // 检测 excludes
  const excludes = lines.find(l => /excludes/.test(l.toLowerCase()));
  // 检测 dateFormat
  const dateFmt = lines.find(l => /dateformat/i.test(l));
  let dateStr = '默认';
  if (dateFmt) {
    const m = dateFmt.match(/dateformat\s+(.+)/i);
    if (m) dateStr = m[1].trim();
  }

  return [
    { label: '图表类型', value: getTypeLabel(dt.type),                   detail: dt.typeDetail },
    { label: '任务数量', value: `${taskLines} 个`,          detail: `分 ${sectionCount} 个阶段` },
    { label: '时间格式', value: dateStr,                   detail: '日期格式' },
    { label: '工作规则', value: excludes ? '有排除日' : '无例外', detail: excludes ? '排除特定日期' : '连续时间轴' },
  ];
}

/** Pie / 饼图分析 */
function analyzePie(lines, dt) {
  // 统计数据项
  const items = lines.filter(l => /^\s*"[^"]+"\s*:\s*[\d.]+/.test(l));
  const total = items.reduce((sum, l) => {
    const m = l.match(/:\s*([\d.]+)/);
    return sum + (m ? parseFloat(m[1]) : 0);
  }, 0);
  // 找最大值
  let maxItem = { label: '', value: 0 };
  items.forEach(l => {
    const lm = l.match(/"([^"]+)"\s*:\s*([\d.]+)/);
    if (lm && parseFloat(lm[2]) > maxItem.value) {
      maxItem = { label: lm[1], value: parseFloat(lm[2]) };
    }
  });
  const maxPct = total > 0 ? Math.round(maxItem.value / total * 100) : 0;
  const showData = lines.some(l => /showdata/i.test(l));

  return [
    { label: '图表类型', value: getTypeLabel(dt.type),                            detail: dt.typeDetail },
    { label: '数据分类', value: `${items.length} 项`,               detail: `总量 ${Math.round(total)}` },
    { label: '最大占比', value: maxItem.label || '—',               detail: maxItem.label ? `${maxPct}%` : '' },
    { label: '数值展示', value: showData ? '显示' : '隐藏',          detail: 'showData 选项' },
  ];
}

/** Timeline / 时间线分析 */
function analyzeTimeline(lines, dt) {
  // 统计时间节点（格式通常是单行非缩进标题）
  const sections = lines.filter(l => /^\s{0,2}\S/.test(l) && !l.trim().startsWith('timeline') && !l.trim().startsWith('title')).length;
  // 统计事件（缩进行）
  const events = lines.filter(l => /^\s{4,}/.test(l) && l.trim()).length;
  // 标题
  const titleLine = lines.find(l => /^\s*title\s+/i.test(l));
  let titleText = '无标题';
  if (titleLine) {
    const m = titleLine.match(/title\s+(.+)/i);
    if (m) titleText = m[1].trim().slice(0, 16);
  }

  return [
    { label: '图表类型', value: getTypeLabel(dt.type),           detail: dt.typeDetail },
    { label: '时间阶段', value: `${sections} 个`,  detail: '主要时间节点' },
    { label: '事件总数', value: `${events} 个`,    detail: '各节点事件数' },
    { label: '主题',     value: titleText,         detail: '时间线标题' },
  ];
}

/** Generic / 通用分析 */
function analyzeGeneric(lines, dt) {
  const total = lines.length;
  const nonEmpty = lines.filter(l => l.trim()).length;
  const indented = lines.filter(l => /^\s{2,}/.test(l)).length;
  return [
    { label: '图表类型',  value: getTypeLabel(dt.type), detail: dt.typeDetail },
    { label: '代码行数',  value: `${total} 行`,    detail: `有效行 ${nonEmpty}` },
    { label: '缩进层级',  value: indented > 0 ? '多层' : '单层', detail: `${indented} 行缩进` },
    { label: '结构复杂度', value: total > 30 ? '较复杂' : (total > 15 ? '适中' : '简洁'), detail: '按代码行估计' },
  ];
}

/**
 * 从 .mmd 文件内容解析元数据注释 + 自动分析内容
 * 支持格式:
 *   # @title  标题
 *   # @desc   描述
 *   # @icon   emoji
 *   # @meta   key1:val1|key2:val2|key3:val3|key4:val4
 *   # @type   图表类型
 */
function parseMmdMeta(content, filename) {
  const meta = {
    title: null,
    desc: null,
    icon: null,
    metaCards: [],  // 手动声明的 @meta 卡片（优先级高于自动分析）
    type: null,
    typeDetail: null,
  };

  const lines = content.split('\n');
  for (const line of lines) {
    const m = line.match(/^#\s*@(\w+)\s+(.*)/);
    if (!m) continue;
    const [, key, val] = m;
    const v = val.trim();
    switch (key) {
      case 'title': meta.title = v; break;
      case 'desc':  meta.desc  = v; break;
      case 'icon':  meta.icon  = v; break;
      case 'type':  meta.type  = v; break;
      case 'meta':
        meta.metaCards = v.split('|').slice(0, 3).map(pair => {
          const idx = pair.indexOf(':');
          if (idx < 0) return { label: pair.trim(), value: '' };
          return { label: pair.slice(0, idx).trim(), value: pair.slice(idx + 1).trim() };
        });
        break;
    }
  }

  // 自动推断图表类型（从内容首行）
  const diagramType = meta.type
    ? { type: meta.type, typeDetail: meta.typeDetail || '' }
    : inferDiagramType(lines);

  meta.type = diagramType.type;
  meta.typeDetail = diagramType.typeDetail;

  // 自动推断图标（若未手动声明）— 使用单色 SVG icon 代替 emoji
  if (!meta.icon) {
    const typeIconMap = {
      // 流程图：箭头循环
      'Flowchart': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="9" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a3 3 0 0 0 3 3h3"/><path d="M18 9v3a3 3 0 0 1-3 3h-0.1"/></svg>`,
      // 时序图：双向箭头
      'Sequence': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="17" y1="12" x2="3" y2="12"/><polyline points="8 7 3 12 8 17"/><line x1="7" y1="12" x2="21" y2="12"/><polyline points="16 7 21 12 16 17"/></svg>`,
      // 状态图：分支箭头
      'State': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M12 7v3l-5 7"/><path d="M12 10l5 7"/></svg>`,
      // 类图：代码方块
      'Class': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>`,
      // ER图：数据库
      'ER': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>`,
      // 折线图
      'XY Chart': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
      // 甘特图：日历
      'Gantt': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="14" x2="14" y2="14"/><line x1="8" y1="18" x2="11" y2="18"/></svg>`,
      // 饼图
      'Pie': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>`,
      // 时间线
      'Timeline': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><circle cx="7" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="17" cy="12" r="2"/><line x1="7" y1="10" x2="7" y2="4"/><line x1="12" y1="10" x2="12" y2="7"/><line x1="17" y1="10" x2="17" y2="2"/></svg>`,
      // 思维导图
      'Mindmap': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 9V3"/><path d="M12 21v-6"/><path d="M9 12H3"/><path d="M21 12h-6"/><path d="M18.36 5.64l-4.24 4.24"/><path d="M5.64 18.36l4.24-4.24"/><path d="M18.36 18.36l-4.24-4.24"/><path d="M5.64 5.64l4.24 4.24"/></svg>`,
      // 块图
      'Block': `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
    };
    // 默认图标：图表
    meta.icon = typeIconMap[meta.type] || `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="3" y1="9" x2="21" y2="9"/></svg>`;
  }

  // 默认标题：用文件名生成
  if (!meta.title) {
    meta.title = path.basename(filename, '.mmd').replace(/[-_]/g, ' ');
  }

  // 自动分析生成信息卡片
  meta.infoCards = analyzeContent(content, diagramType, meta.metaCards);

  return meta;
}

// ─── 主题颜色提取 ────────────────────────────────────────────────────────────

/**
 * 提取主题的 CSS 变量（用于 HTML 模板）
 * 直接从 resolvedTheme 读取，不做任何 tokyo-night 硬编码 fallback
 * resolveTheme() 已经保证了所有字段都有值（用 THEME_DEFAULTS 补全）
 */
function extractThemeColors(themeName, resolvedTheme) {
  return {
    bg:      resolvedTheme.bg,
    surface: resolvedTheme.surface,
    border:  resolvedTheme.border,
    fg:      resolvedTheme.fg,
    muted:   resolvedTheme.muted,
    accent:  resolvedTheme.accent,
    line:    resolvedTheme.line,
  };
}

/**
 * 判断主题是否为亮色
 */
function isLightTheme(bg) {
  // 简单亮度判断
  const hex = bg.replace('#', '');
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5;
}

// ─── HTML 模板生成 ───────────────────────────────────────────────────────────

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/**
 * 图表类型对应的 SVG icon（内联，避免 emoji 渲染不一致）
 */
function getTypeIcon(type) {
  const icons = {
    'Flowchart': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="5" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="8" y="16" width="8" height="5" rx="1"/><path d="M6.5 8v3h11V8"/><path d="M12 11v5"/></svg>`,
    'Sequence': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="4" x2="5" y2="20"/><line x1="19" y1="4" x2="19" y2="20"/><path d="M5 9h14"/><path d="M19 14H5"/><circle cx="5" cy="4" r="2" fill="currentColor" stroke="none"/><circle cx="19" cy="4" r="2" fill="currentColor" stroke="none"/></svg>`,
    'State': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v5M12 16v5M3 12h5M16 12h5"/></svg>`,
    'Class': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="18" rx="2"/><path d="M2 9h20"/><path d="M2 15h20"/></svg>`,
    'ER': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="8" height="16" rx="1"/><rect x="14" y="4" width="8" height="16" rx="1"/><path d="M10 12h4"/></svg>`,
    'XY Chart': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21V3"/><path d="M3 21h18"/><rect x="6" y="13" width="3" height="8" rx="1" fill="currentColor" stroke="none"/><rect x="11" y="9" width="3" height="12" rx="1" fill="currentColor" stroke="none"/><rect x="16" y="5" width="3" height="16" rx="1" fill="currentColor" stroke="none"/></svg>`,
    'Gantt': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 5h18M3 10h18M3 15h18M3 20h18"/><rect x="3" y="3" width="8" height="4" rx="1" fill="currentColor" stroke="none" opacity=".6"/><rect x="9" y="8" width="10" height="4" rx="1" fill="currentColor" stroke="none" opacity=".6"/><rect x="5" y="13" width="12" height="4" rx="1" fill="currentColor" stroke="none" opacity=".6"/></svg>`,
    'Pie': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 3v9l6.5 6.5" stroke-width="2"/></svg>`,
    'Timeline': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18"/><circle cx="7" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="17" cy="12" r="2" fill="currentColor" stroke="none"/><path d="M7 12V7M12 12V5M17 12V9"/></svg>`,
    'Mindmap': `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 9V5M12 19v-4M9 12H5M19 12h-4M9.5 9.5L6.5 6.5M17.5 9.5l3-3M9.5 14.5l-3 3M17.5 14.5l3 3"/></svg>`,
  };
  return icons[type] || `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>`;
}

/**
 * 构建左侧 TOC 导航
 */
function buildTocNav(diagrams, isLight) {
  const items = diagrams.map((d, i) => {
    const { meta } = d;
    const label   = getTypeLabel(meta.type);
    const tooltip = meta.desc ? `${label} — ${meta.desc}` : label;
    return `
      <a href="#diagram-${i}" class="toc-item" data-idx="${i}"
         onclick="scrollToCard(${i}, event)"
         title="${escHtml(tooltip)}">
        <span class="toc-icon" aria-hidden="true">${getTypeIcon(meta.type)}</span>
        <span class="toc-label">${escHtml(meta.title)}</span>
        <span class="toc-type" aria-label="${escHtml(label)}">${escHtml(label)}</span>
      </a>`;
  }).join('');
  return items;
}

// ─── 流程总结 + 自检 ─────────────────────────────────────────────────────────

/**
 * 深度分析 Mermaid 流程图内容，提取：
 * - 起点 / 终点
 * - 角色列表（通过节点 ID 前缀 / 子图名称推断）
 * - 主流程步骤
 * - 判断分支（成功/失败/取消/异常）
 * - 页面跳转 & 状态流转
 * - 输入输出字段 / 提示文案 / 边界规则
 */
function deepAnalyzeDiagram(content, diagramType) {
  const lines = content.split('\n').filter(l => l.trim() && !l.trim().startsWith('#'));

  if (diagramType.type === 'Flowchart') {
    return analyzeFlowchartDeep(lines);
  } else if (diagramType.type === 'Sequence') {
    return analyzeSequenceDeep(lines);
  } else if (diagramType.type === 'State') {
    return analyzeStateDeep(lines);
  }
  return analyzeGenericDeep(lines, diagramType);
}

/** 流程图深度分析 */
function analyzeFlowchartDeep(lines) {
  const nodes = {};   // id -> label
  const edges = [];   // { from, to, label }
  const subgraphs = []; // 子图名称
  const branches = []; // 判断节点

  // 解析子图
  lines.forEach(l => {
    const sg = l.match(/^\s*subgraph\s+([^\n]+)/i);
    if (sg) subgraphs.push(sg[1].trim().replace(/^["']|["']$/g, ''));
  });

  // 解析节点（形如 A[text] / A(text) / A{text} / A((text)) / A([text])）
  lines.forEach(l => {
    // 多节点连线里也可能含节点定义
    const parts = l.split(/-->|--[-o*x]?|==+>|[-.]->|--\|[^|]*\|/);
    parts.forEach(part => {
      const m = part.match(/([A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_\-]*)[\s]*(?:\[([^\]]*)\]|\(([^)]*)\)|\{([^}]*)\}|\(\(([^)]*)\)\)|\(\[([^\]]*)\]\))/);
      if (m) {
        const id = m[1].trim();
        const label = (m[2] || m[3] || m[4] || m[5] || m[6] || '').trim();
        if (id && label) nodes[id] = label;
      }
    });

    // 解析带标签的边
    const edgeMatch = l.match(/([A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_\-]*)\s*-->\s*(?:\|([^|]*)\|)?\s*([A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_\-]*)/g);
    if (edgeMatch) {
      edgeMatch.forEach(e => {
        const em = e.match(/([^\s]+)\s*-->\s*(?:\|([^|]*)\|)?\s*([^\s]+)/);
        if (em) edges.push({ from: em[1], label: em[2] || '', to: em[3] });
      });
    }

    // 判断节点（菱形 {}）
    const branchM = l.match(/([A-Za-z\u4e00-\u9fff_][A-Za-z0-9\u4e00-\u9fff_\-]*)\s*\{([^}]+)\}/);
    if (branchM) branches.push({ id: branchM[1], text: branchM[2].trim() });
  });

  // 找起点（没有入边的节点）和终点（没有出边的节点）
  const fromIds = new Set(edges.map(e => e.from));
  const toIds   = new Set(edges.map(e => e.to));
  const nodeIds = new Set(Object.keys(nodes));

  // 起点 = 有出边但无入边
  const startNodes = [...nodeIds].filter(id => fromIds.has(id) && !toIds.has(id))
    .map(id => nodes[id] || id).slice(0, 3);

  // 终点 = 有入边但无出边，或是 ([xxx]) 终止符形状
  const endNodes = [...nodeIds].filter(id => toIds.has(id) && !fromIds.has(id))
    .map(id => nodes[id] || id).slice(0, 3);

  // 主流程步骤（按边顺序，去掉分支路径）
  const mainSteps = [];
  // 从起点开始做 BFS，取最长主干路径
  if (startNodes.length > 0) {
    const startId = [...nodeIds].find(id => fromIds.has(id) && !toIds.has(id));
    if (startId) {
      let cur = startId;
      const visited = new Set();
      for (let i = 0; i < 20; i++) {
        if (!cur || visited.has(cur)) break;
        visited.add(cur);
        if (nodes[cur]) mainSteps.push(nodes[cur]);
        const nextEdge = edges.find(e => e.from === cur && !e.label);
        if (!nextEdge) {
          // 无标签的下一步没有了，试试有标签的
          const anyNext = edges.find(e => e.from === cur);
          if (anyNext) { cur = anyNext.to; } else break;
        } else {
          cur = nextEdge.to;
        }
      }
    }
  }

  // 提取判断分支条件
  const branchConditions = [];
  branches.forEach(b => {
    const outEdges = edges.filter(e => e.from === b.id && e.label);
    const conditions = outEdges.map(e => `"${e.label}" → ${nodes[e.to] || e.to}`);
    if (conditions.length > 0) {
      branchConditions.push({ question: b.text, conditions });
    }
  });

  // 角色 / 泳道（来自 subgraph 名称）
  const roles = subgraphs.length > 0 ? subgraphs : inferRolesFromNodeLabels(nodes);

  // 边界规则：提取边标签里含"失败/错误/异常/取消/超时"的条件
  const errorBranches = edges
    .filter(e => /失败|错误|异常|取消|超时|拒绝|invalid|error|fail|cancel|timeout/i.test(e.label))
    .map(e => `${e.label}: → ${nodes[e.to] || e.to}`)
    .slice(0, 5);

  return {
    type: 'flowchart',
    startNodes: startNodes.length > 0 ? startNodes : ['（未检测到，请检查节点连接）'],
    endNodes: endNodes.length > 0 ? endNodes : ['（未检测到，请检查节点连接）'],
    roles: roles.length > 0 ? roles : ['（未声明子图/泳道，请手动补充）'],
    mainSteps: mainSteps.length > 0 ? mainSteps : Object.values(nodes).slice(0, 8),
    branchConditions,
    errorBranches,
    nodeCount: Object.keys(nodes).length,
    edgeCount: edges.length,
  };
}

/** 从节点标签推断角色（简单启发式） */
function inferRolesFromNodeLabels(nodes) {
  const roleKeywords = ['用户', '系统', '管理员', '服务', '数据库', 'DB', 'API', '前端', '后端', '客户', '商家', '平台'];
  const found = new Set();
  Object.values(nodes).forEach(label => {
    roleKeywords.forEach(kw => {
      if (label.includes(kw)) found.add(kw);
    });
  });
  return [...found];
}

/** 时序图深度分析 */
function analyzeSequenceDeep(lines) {
  const participants = [];
  const messages = [];
  const notes = [];
  const altBlocks = [];

  lines.forEach(l => {
    const pm = l.match(/^\s*(?:participant|actor)\s+(.+?)(?:\s+as\s+(.+))?$/i);
    if (pm) {
      participants.push(pm[2] ? pm[2].trim() : pm[1].trim());
    }
    const mm = l.match(/^\s*([^\s:]+)\s*(-[->>xo]+)\s*([^\s:]+)\s*:\s*(.+)/);
    if (mm) {
      messages.push({ from: mm[1], arrow: mm[2], to: mm[3], text: mm[4].trim() });
    }
    const nm = l.match(/^\s*[Nn]ote\s+(?:over|left of|right of)\s+.+:\s*(.+)/);
    if (nm) notes.push(nm[1].trim());
    const am = l.match(/^\s*(?:alt|opt|else)\s+(.+)/i);
    if (am) altBlocks.push(am[1].trim());
  });

  // 推断参与者（从消息行）
  if (participants.length === 0) {
    const pSet = new Set();
    messages.forEach(m => { pSet.add(m.from); pSet.add(m.to); });
    participants.push(...pSet);
  }

  const errorMessages = messages.filter(m =>
    /失败|错误|异常|取消|超时|error|fail|cancel|timeout/i.test(m.text)
  ).map(m => `${m.from} → ${m.to}: ${m.text}`).slice(0, 5);

  return {
    type: 'sequence',
    startNodes: [messages[0] ? `${messages[0].from} 发起「${messages[0].text}」` : '（见第一条消息）'],
    endNodes: [messages.length > 0 ? `${messages[messages.length-1].to} 完成「${messages[messages.length-1].text}」` : '（见最后一条消息）'],
    roles: participants.slice(0, 8),
    mainSteps: messages.slice(0, 10).map(m => `${m.from} → ${m.to}: ${m.text}`),
    branchConditions: altBlocks.map(a => ({ question: a, conditions: [] })),
    errorBranches: errorMessages,
    nodeCount: participants.length,
    edgeCount: messages.length,
  };
}

/** 状态图深度分析 */
function analyzeStateDeep(lines) {
  const states = new Set();
  const transitions = [];

  lines.forEach(l => {
    const tm = l.match(/^\s*([^\s]+)\s*-->\s*([^\s:]+)\s*(?::\s*(.+))?/);
    if (tm) {
      states.add(tm[1]); states.add(tm[2]);
      transitions.push({ from: tm[1], to: tm[2], label: tm[3] || '' });
    }
  });
  states.delete('[*]');

  const stateList = [...states].slice(0, 10);
  const startTrans = transitions.filter(t => t.from === '[*]').map(t => t.to);
  const endTrans   = transitions.filter(t => t.to === '[*]').map(t => t.from);

  const errorTrans = transitions.filter(t =>
    /失败|异常|错误|取消|error|fail/i.test(t.label)
  ).map(t => `${t.from} →${t.label ? '「'+t.label+'」' : ''} ${t.to}`).slice(0, 5);

  return {
    type: 'state',
    startNodes: startTrans.length > 0 ? startTrans : ['（初始状态）'],
    endNodes: endTrans.length > 0 ? endTrans : ['（终止状态）'],
    roles: ['系统状态机'],
    mainSteps: stateList,
    branchConditions: transitions.filter(t => t.label)
      .slice(0, 6)
      .map(t => ({ question: `${t.from}`, conditions: [`「${t.label}」→ ${t.to}`] })),
    errorBranches: errorTrans,
    nodeCount: states.size,
    edgeCount: transitions.length,
  };
}

/** 通用图表深度分析（fallback） */
function analyzeGenericDeep(lines, diagramType) {
  return {
    type: 'generic',
    startNodes: ['（见图表起始节点）'],
    endNodes: ['（见图表终止节点）'],
    roles: ['（请根据图表内容补充）'],
    mainSteps: ['（请查阅图表了解主流程）'],
    branchConditions: [],
    errorBranches: [],
    nodeCount: lines.length,
    edgeCount: 0,
  };
}

/**
 * 自检函数：基于深度分析结果生成五维自检报告
 * 返回 { closedLoop, exceptionBranch, roleClarity, stateLogic, implementable }
 * 每项为 { pass: boolean, score: 'pass'|'warn'|'fail', message: string }
 */
function selfCheck(analysis) {
  const checks = {};

  // 1. 闭环检测
  const hasStart = analysis.startNodes.some(s => !s.includes('（'));
  const hasEnd   = analysis.endNodes.some(s => !s.includes('（'));
  checks.closedLoop = {
    score: (hasStart && hasEnd) ? 'pass' : 'warn',
    label: '闭环完整性',
    message: (hasStart && hasEnd)
      ? `起点「${analysis.startNodes[0]}」→ 终点「${analysis.endNodes[0]}」，流程闭合`
      : '未检测到明确的起点或终点，建议补充起止节点',
  };

  // 2. 异常分支
  const hasError = analysis.errorBranches && analysis.errorBranches.length > 0;
  const hasBranch = analysis.branchConditions && analysis.branchConditions.some(b => b.conditions.length > 0);
  checks.exceptionBranch = {
    score: (hasError || hasBranch) ? 'pass' : 'warn',
    label: '异常分支覆盖',
    message: hasError
      ? `已包含 ${analysis.errorBranches.length} 条异常路径`
      : (hasBranch
        ? `有判断分支，建议为每个分支补充异常/失败处理`
        : '未检测到异常/失败分支，建议补充超时、取消、错误处理'),
  };

  // 3. 角色清晰度
  const hasRoles = analysis.roles && analysis.roles.some(r => !r.includes('（'));
  checks.roleClarity = {
    score: hasRoles ? 'pass' : 'fail',
    label: '角色清晰度',
    message: hasRoles
      ? `已识别角色：${analysis.roles.slice(0, 4).join('、')}`
      : '未检测到明确角色/泳道，建议用 subgraph 划分角色',
  };

  // 4. 状态流转合理性
  const totalNodes = analysis.nodeCount || 0;
  const totalEdges = analysis.edgeCount || 0;
  const isolated = totalNodes > 0 && totalEdges === 0;
  checks.stateLogic = {
    score: isolated ? 'fail' : (totalEdges >= totalNodes ? 'pass' : 'warn'),
    label: '状态流转合理',
    message: isolated
      ? '节点之间无连接，状态无法流转'
      : (totalEdges >= totalNodes
        ? `连接数(${totalEdges}) ≥ 节点数(${totalNodes})，流转路径充足`
        : `连接数(${totalEdges}) 较少，部分节点可能是孤立状态`),
  };

  // 5. 可落地性（有主流程步骤且有名称）
  const hasSteps = analysis.mainSteps && analysis.mainSteps.some(s => s && !s.includes('（'));
  checks.implementable = {
    score: hasSteps ? 'pass' : 'warn',
    label: '可落地性',
    message: hasSteps
      ? `识别到 ${Math.min(analysis.mainSteps.length, 8)} 个主流程步骤，可对应前端页面和接口`
      : '主流程步骤标签不清晰，建议为每个节点补充明确的操作描述',
  };

  return checks;
}

/**
 * 构建流程总结 HTML 区块
 */
function buildFlowSummary(analysis, colors, isLight) {
  if (!analysis) return '';

  const labelColor = isLight ? colors.fg : '#ffffff';
  const mutedColor = colors.muted;
  const accentColor = colors.accent;

  // 判断分支 HTML
  const branchHtml = analysis.branchConditions && analysis.branchConditions.length > 0
    ? analysis.branchConditions.map(b => `
      <div class="summary-branch-item">
        <span class="summary-branch-q">${escHtml(b.question)}</span>
        <div class="summary-branch-conds">
          ${b.conditions.map(c => `<span class="summary-cond-tag">${escHtml(c)}</span>`).join('')}
        </div>
      </div>`).join('')
    : `<span class="summary-empty">（此图表类型暂无判断分支，或分支无标签）</span>`;

  // 异常/边界规则 HTML
  const errorHtml = analysis.errorBranches && analysis.errorBranches.length > 0
    ? analysis.errorBranches.map(e => `<span class="summary-error-tag">${escHtml(e)}</span>`).join('')
    : `<span class="summary-empty">（未检测到失败/异常分支，建议补充）</span>`;

  // 主流程步骤 HTML
  const stepsHtml = (analysis.mainSteps || []).slice(0, 12).map((s, i) => `
    <div class="summary-step-item">
      <span class="summary-step-num">${i + 1}</span>
      <span class="summary-step-text">${escHtml(String(s))}</span>
    </div>`).join('');

  // 角色列表 HTML
  const rolesHtml = (analysis.roles || []).map(r => `
    <span class="summary-role-tag">${escHtml(r)}</span>`).join('');

  return `
  <!-- Flow Summary -->
  <div class="flow-summary">
    <div class="summary-header">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
      流程规格总结
    </div>
    <div class="summary-grid">

      <!-- 起止 -->
      <div class="summary-block">
        <div class="summary-block-label">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
          流程起止
        </div>
        <div class="summary-block-content">
          <div class="summary-start-end">
            <div class="summary-se-item">
              <span class="summary-se-dot start"></span>
              <span class="summary-se-label">起点</span>
              <span class="summary-se-val">${escHtml(analysis.startNodes.join(' / '))}</span>
            </div>
            <div class="summary-se-item">
              <span class="summary-se-dot end"></span>
              <span class="summary-se-label">终点</span>
              <span class="summary-se-val">${escHtml(analysis.endNodes.join(' / '))}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 角色 -->
      <div class="summary-block">
        <div class="summary-block-label">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          角色列表
        </div>
        <div class="summary-block-content summary-roles">
          ${rolesHtml}
        </div>
      </div>

      <!-- 主流程 -->
      <div class="summary-block summary-block-wide">
        <div class="summary-block-label">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
          主流程步骤
        </div>
        <div class="summary-block-content">
          <div class="summary-steps">${stepsHtml}</div>
        </div>
      </div>

      <!-- 判断分支 -->
      <div class="summary-block summary-block-wide">
        <div class="summary-block-label">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l5.1 5.1M4 4l5 5"/></svg>
          判断分支
        </div>
        <div class="summary-block-content">${branchHtml}</div>
      </div>

      <!-- 异常/边界 -->
      <div class="summary-block summary-block-wide">
        <div class="summary-block-label">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          异常分支 / 边界规则
        </div>
        <div class="summary-block-content summary-errors">
          ${errorHtml}
        </div>
      </div>

    </div>
  </div>`;
}

/**
 * 构建自检清单 HTML 区块
 */
function buildSelfCheckPanel(checks, isLight) {
  if (!checks) return '';

  const scoreConfig = {
    pass: { icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`, color: '#22c55e', bg: '#22c55e18', label: '通过' },
    warn: { icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`, color: '#f59e0b', bg: '#f59e0b18', label: '建议完善' },
    fail: { icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`, color: '#ef4444', bg: '#ef444418', label: '需要修复' },
  };

  const checkItems = Object.values(checks).map(c => {
    const cfg = scoreConfig[c.score] || scoreConfig.warn;
    return `
    <div class="check-item" style="--check-color:${cfg.color};--check-bg:${cfg.bg};">
      <div class="check-item-header">
        <span class="check-icon" style="color:${cfg.color};">${cfg.icon}</span>
        <span class="check-label">${escHtml(c.label)}</span>
        <span class="check-badge" style="background:${cfg.bg};color:${cfg.color};border-color:${cfg.color}44;">${cfg.label}</span>
      </div>
      <div class="check-message">${escHtml(c.message)}</div>
    </div>`;
  }).join('');

  // 汇总评分
  const passCount = Object.values(checks).filter(c => c.score === 'pass').length;
  const total = Object.keys(checks).length;
  const overallScore = passCount === total ? 'pass' : (passCount >= total / 2 ? 'warn' : 'fail');
  const overallCfg = scoreConfig[overallScore];
  const passLabel = passCount === total ? '设计完整，可直接落地' : (passCount >= total / 2 ? '基本完整，建议完善高亮项' : '存在缺陷，建议优先修复红色项');

  return `
  <!-- Self Check Panel -->
  <div class="self-check-panel">
    <div class="check-header">
      <div class="check-header-left">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        落地自检清单
      </div>
      <div class="check-overall" style="color:${overallCfg.color};background:${overallCfg.bg};border-color:${overallCfg.color}44;">
        ${overallCfg.icon}
        ${passCount}/${total} 通过 · ${passLabel}
      </div>
    </div>
    <div class="check-items">
      ${checkItems}
    </div>
  </div>`;
}

/**
 * 构建 stats 统计区（每个卡片含 icon + accent bar + 三行文字）
 */
function buildStatsGrid(infoCards, accentColor, isLight) {
  // 不同卡片用不同的 micro-icon
  const cardIcons = [
    // 图表类型 icon
    `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`,
    // 数量/节点 icon
    `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><circle cx="4" cy="6" r="2"/><circle cx="20" cy="6" r="2"/><circle cx="4" cy="18" r="2"/><circle cx="20" cy="18" r="2"/><path d="M6 6.5l4 4M14 13.5l4 4M6 17.5l4-4M14 10.5l4-4"/></svg>`,
    // 连接/关系 icon
    `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`,
    // 结构/层级 icon
    `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="6" height="5" rx="1"/><rect x="9" y="11" width="6" height="5" rx="1"/><rect x="15" y="16" width="6" height="5" rx="1"/><path d="M6 8v3h6v3h6"/></svg>`,
  ];

  return infoCards.map((c, idx) => {
    const icon = cardIcons[idx] || cardIcons[0];
    return `
        <div class="stat-card">
          <div class="stat-accent-bar"></div>
          <div class="stat-body">
            <div class="stat-header">
              <span class="stat-icon">${icon}</span>
              <span class="stat-label">${escHtml(c.label)}</span>
            </div>
            <div class="stat-value">${escHtml(c.value || '—')}</div>
            <div class="stat-detail">${escHtml(c.detail || '—')}</div>
          </div>
        </div>`;
  }).join('');
}

/**
 * 构建每个图表卡片（大卡片）
 */
function buildDiagramCards(diagrams, colors, isLight) {
  return diagrams.map((d, i) => {
    const { meta, svgContent, mmdSource } = d;
    const statsGrid = buildStatsGrid(meta.infoCards, colors.accent, isLight);
    const titleFg = isLight ? colors.fg : '#ffffff';

    // SVG 内容：若为空则显示 fallback UI
    const hasSvg = svgContent && svgContent.trim().length > 30;
    const svgOrFallback = hasSvg ? svgContent : `
      <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:40px;color:var(--muted);text-align:center;">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <p style="font-size:13px;font-weight:500;">图表渲染失败，请检查 Mermaid 语法</p>
        <p style="font-size:11.5px;opacity:0.7;">The diagram could not be rendered</p>
      </div>
    `;

    // 深度分析 + 自检（仅对 Flowchart/Sequence/State 做详细分析）
    const deepAnalysis = deepAnalyzeDiagram(mmdSource || '', { type: meta.type });
    const flowSummaryHtml = buildFlowSummary(deepAnalysis, colors, isLight);
    const checks = selfCheck(deepAnalysis);
    const selfCheckHtml = buildSelfCheckPanel(checks, isLight);

    // 图表类型 badge 颜色（基于类型稳定哈希）
    const typeBadgeColors = {
      'Flowchart': '#3b82f6', 'Sequence': '#8b5cf6', 'State': '#10b981',
      'Class': '#f59e0b', 'ER': '#ef4444', 'XY Chart': '#06b6d4',
      'Gantt': '#84cc16', 'Pie': '#ec4899', 'Timeline': '#f97316',
      'Mindmap': '#6366f1',
    };
    const badgeColor = typeBadgeColors[meta.type] || colors.accent;

    return `
  <!-- ═══ Diagram ${i + 1}: ${escHtml(meta.title)} ═══ -->
  <section class="diagram-section" id="diagram-${i}" aria-labelledby="dtitle-${i}">
    <!-- Card Header -->
    <div class="diagram-card">
      <div class="diagram-card-header">
        <div class="diagram-card-header-left">
          <div class="diagram-icon-wrap">${meta.icon && meta.icon.trim().startsWith('<') ? meta.icon : `<span style="font-size:14px;line-height:1;">${meta.icon}</span>`}</div>
          <div class="diagram-title-wrap">
            <h2 class="diagram-title" id="dtitle-${i}">${escHtml(meta.title)}</h2>
            ${meta.desc ? `<p class="diagram-desc">${escHtml(meta.desc)}</p>` : ''}
          </div>
        </div>
        <div class="diagram-card-header-right">
          <span class="type-badge" style="background:${badgeColor}22;color:${badgeColor};border-color:${badgeColor}44;"
                aria-label="${escHtml(getTypeLabel(meta.type))}">
            ${getTypeIcon(meta.type)}
            ${escHtml(getTypeLabel(meta.type))}
          </span>
        </div>
      </div>

      <!-- Stats Row -->
      <div class="stats-row">
        ${statsGrid}
      </div>

      <!-- SVG Render Area -->
      <div class="svg-render-area" data-idx="${i}"
           role="button" tabindex="0"
           aria-label="点击全屏查看 ${escHtml(meta.title)}">
        <div class="svg-render-inner" id="svg-container-${i}">${svgOrFallback}</div>
        <span class="svg-zoom-hint" aria-hidden="true">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
          点击全屏查看
        </span>
      </div>

      ${flowSummaryHtml}
      ${selfCheckHtml}

      <!-- Code Toggle Footer -->
      <div class="card-footer">
        <button class="code-toggle-btn" onclick="toggleCode('code-${i}', this)" aria-expanded="false">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
          查看源码
          <svg class="toggle-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
      </div>
      <div class="code-block" id="code-${i}">
        <div class="code-block-header">
          <span class="code-lang-tag">mermaid</span>
          <button class="copy-btn" onclick="copyCode('code-src-${i}')">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            复制
          </button>
        </div>
        <pre class="code-pre"><code id="code-src-${i}">${escHtml(mmdSource || '')}</code></pre>
      </div>
    </div>
  </section>`;
  }).join('\n');
}

function buildHtml(options, diagrams, colors, themeName, presetName) {
  const title = options.title || '图表集合';
  const subtitle = options.subtitle || `${diagrams.length} 张图 · Beautiful Mermaid 渲染`;
  const isLight = isLightTheme(colors.bg);

  // 读取 logo PNG 并转为 base64 data URI
  const logoPngPath = path.resolve(__dirname, '../beautiful-mermaid.png');
  let logoDatasUri = '';
  try {
    const logoData = fs.readFileSync(logoPngPath);
    logoDatasUri = `data:image/png;base64,${logoData.toString('base64')}`;
  } catch (_) {
    // PNG 不存在时静默降级（不显示 logo 图片）
  }

  // 精细颜色计算
  const headerBg = isLight
    ? adjustBrightness(colors.bg, -4)
    : adjustBrightness(colors.bg, 4);
  const sidebarBg = isLight
    ? adjustBrightness(colors.bg, -6)
    : adjustBrightness(colors.bg, -6);
  const cardBg = isLight
    ? colors.bg
    : adjustBrightness(colors.bg, 6);
  const svgAreaBg = isLight
    ? adjustBrightness(colors.bg, -8)
    : adjustBrightness(colors.bg, -8);
  const codeBlockBg = isLight
    ? adjustBrightness(colors.bg, -12)
    : adjustBrightness(colors.bg, -12);

  const headingFg = isLight ? adjustBrightness(colors.fg, -20) : '#ffffff';
  const badgeFg = isLight ? colors.bg : '#ffffff';

  // 构建各区块
  const tocNav = buildTocNav(diagrams, isLight);
  const diagramCards = buildDiagramCards(diagrams, colors, isLight);

  // accent 渐变（用于 stat-accent-bar 和一些 hover 效果）
  const accentRgb = hexToRgb(colors.accent);
  const accentAlpha = accentRgb ? `rgba(${accentRgb.r},${accentRgb.g},${accentRgb.b},0.15)` : colors.accent + '26';
  const accentAlphaHover = accentRgb ? `rgba(${accentRgb.r},${accentRgb.g},${accentRgb.b},0.25)` : colors.accent + '40';

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${escHtml(title)} — Beautiful Mermaid</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    /* ─── Skip Link (WCAG 2.4.1) ────────────────── */
    .skip-link {
      position: absolute;
      top: -999px;
      left: 16px;
      z-index: 9999;
      padding: 8px 18px;
      background: var(--accent, #7aa2f7);
      color: #fff;
      border-radius: 0 0 8px 8px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: top 0.15s;
    }
    .skip-link:focus { top: 0; outline: none; }
  </style>
  <style>
    /* ─── CSS 变量 ──────────────────────────────── */
    :root {
      --bg:         ${colors.bg};
      --surface:    ${colors.surface};
      --border:     ${colors.border};
      --fg:         ${colors.fg};
      --muted:      ${colors.muted};
      --accent:     ${colors.accent};
      --accent-a:   ${accentAlpha};
      --accent-ah:  ${accentAlphaHover};
      --heading:    ${headingFg};
      --header-bg:  ${headerBg};
      --sidebar-bg: ${sidebarBg};
      --card-bg:    ${cardBg};
      --svg-area:   ${svgAreaBg};
      --code-bg:    ${codeBlockBg};
      --sidebar-w:  268px;
      --header-h:   60px;
      --radius-card: 16px;
      --radius-sm:   8px;
      --transition:  0.18s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ─── Reset ────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--fg);
      font-family: 'Fira Sans', 'Inter', -apple-system, 'PingFang SC',
                   'Noto Sans SC', 'Microsoft YaHei', 'Segoe UI', sans-serif;
      font-size: 14px;
      line-height: 1.6;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* ─── Subtle background texture ────────────── */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      background-image: radial-gradient(
        circle at 20% 50%,
        ${accentAlpha} 0%,
        transparent 60%
      ), radial-gradient(
        circle at 80% 20%,
        ${accentAlpha} 0%,
        transparent 50%
      );
      opacity: ${isLight ? '0.6' : '0.4'};
    }

    /* ─── Top Header ────────────────────────────── */
    .top-header {
      position: fixed;
      top: 0; left: 0; right: 0;
      height: var(--header-h);
      background: ${isLight
        ? `rgba(${hexToRgb(headerBg) ? `${hexToRgb(headerBg).r},${hexToRgb(headerBg).g},${hexToRgb(headerBg).b}` : '255,255,255'},0.88)`
        : `rgba(${hexToRgb(headerBg) ? `${hexToRgb(headerBg).r},${hexToRgb(headerBg).g},${hexToRgb(headerBg).b}` : '15,15,20'},0.88)`
      };
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 200;
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
    }
    .top-header-left {
      display: flex;
      align-items: center;
      gap: 16px;
      min-width: 0;
    }
    .header-logo {
      display: flex;
      align-items: center;
      gap: 9px;
      font-weight: 700;
      font-size: 14.5px;
      color: var(--heading);
      letter-spacing: -0.02em;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .header-logo img {
      border-radius: 6px;
      transition: filter var(--transition);
    }
    [data-theme="dark"] .header-logo img {
      filter: brightness(0) invert(1);
      opacity: 0.92;
    }
    [data-theme="light"] .header-logo img {
      filter: brightness(0.1);
      opacity: 0.85;
    }
    .header-divider {
      width: 1px;
      height: 22px;
      background: var(--border);
      flex-shrink: 0;
    }
    .header-meta { min-width: 0; }
    .header-title {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--fg);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .header-subtitle {
      font-size: 11.5px;
      color: var(--muted);
      white-space: nowrap;
    }
    .top-header-right {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    .theme-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 12px;
      border-radius: 20px;
      background: var(--accent-a);
      border: 1px solid ${colors.accent}66;
      color: var(--accent);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.02em;
      transition: background var(--transition);
    }
    .theme-pill:hover { background: var(--accent-ah); }
    .diagram-count-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 12px;
      border-radius: 20px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--muted);
      font-size: 11px;
      font-weight: 500;
    }
    .header-kbd-hint {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 10.5px;
      color: var(--muted);
      opacity: 0.6;
      white-space: nowrap;
    }
    .header-kbd-hint kbd {
      display: inline-block;
      padding: 1px 5px;
      border-radius: 4px;
      background: var(--surface);
      border: 1px solid var(--border);
      font-family: inherit;
      font-size: 10px;
      line-height: 16px;
    }
    /* Mobile menu button */
    .menu-btn {
      display: none;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
      cursor: pointer;
      transition: all var(--transition);
    }
    .menu-btn:hover { background: var(--accent-a); color: var(--accent); border-color: var(--accent); }

    /* ─── Layout ────────────────────────────────── */
    .app-layout {
      display: flex;
      padding-top: var(--header-h);
      min-height: 100vh;
      position: relative;
      z-index: 1;
    }

    /* ─── Sidebar ───────────────────────────────── */
    .sidebar {
      position: fixed;
      top: var(--header-h);
      left: 0;
      width: var(--sidebar-w);
      height: calc(100vh - var(--header-h));
      background: ${isLight
        ? `rgba(${hexToRgb(sidebarBg) ? `${hexToRgb(sidebarBg).r},${hexToRgb(sidebarBg).g},${hexToRgb(sidebarBg).b}` : '248,248,250'},0.95)`
        : `rgba(${hexToRgb(sidebarBg) ? `${hexToRgb(sidebarBg).r},${hexToRgb(sidebarBg).g},${hexToRgb(sidebarBg).b}` : '12,12,18'},0.95)`
      };
      border-right: 1px solid var(--border);
      overflow-y: auto;
      padding: 16px 0 24px;
      z-index: 100;
      transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .sidebar.collapsed { transform: translateX(-100%); }
    .sidebar::-webkit-scrollbar { width: 3px; }
    .sidebar::-webkit-scrollbar-track { background: transparent; }
    .sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
    .sidebar-section-title {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--muted);
      padding: 0 16px 10px;
      opacity: 0.7;
    }
    .toc-item {
      display: flex;
      align-items: center;
      gap: 9px;
      padding: 7px 16px 7px 14px;
      cursor: pointer;
      border-left: 3px solid transparent;
      color: var(--muted);
      text-decoration: none;
      transition: background var(--transition), color var(--transition), border-color var(--transition);
      position: relative;
    }
    .toc-item:hover {
      background: var(--accent-a);
      color: var(--fg);
      text-decoration: none;
    }
    .toc-item.active {
      background: var(--accent-a);
      border-left-color: var(--accent);
      color: var(--accent);
    }
    .toc-item.active::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 3px;
      background: var(--accent);
      box-shadow: 0 0 8px ${colors.accent}66;
    }
    .toc-icon {
      flex-shrink: 0;
      opacity: 0.65;
      display: flex;
      align-items: center;
      transition: opacity var(--transition);
    }
    .toc-item.active .toc-icon,
    .toc-item:hover .toc-icon { opacity: 1; }
    .toc-label {
      flex: 1;
      font-size: 13px;
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      letter-spacing: -0.01em;
    }
    .toc-type {
      flex-shrink: 0;
      font-size: 10px;
      color: var(--muted);
      opacity: 0.6;
      font-weight: 500;
    }
    .toc-item.active .toc-type { color: var(--accent); opacity: 0.75; }

    /* ─── Main Content ──────────────────────────── */
    .main-content {
      margin-left: var(--sidebar-w);
      flex: 1;
      padding: 28px 36px 72px;
      max-width: calc(100% - var(--sidebar-w));
      transition: margin-left 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                  max-width 0.28s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .main-content.expanded {
      margin-left: 0;
      max-width: 100%;
    }

    /* ─── Diagram Section ───────────────────────── */
    .diagram-section {
      margin-bottom: 36px;
      scroll-margin-top: calc(var(--header-h) + 20px);
      opacity: 0;
      transform: translateY(16px);
      animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    @keyframes fadeInUp {
      to { opacity: 1; transform: translateY(0); }
    }

    /* ─── Diagram Card ──────────────────────────── */
    .diagram-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-card);
      overflow: hidden;
      box-shadow:
        0 1px 2px rgba(0,0,0,${isLight ? '.04' : '.15'}),
        0 4px 12px rgba(0,0,0,${isLight ? '.04' : '.12'}),
        0 0 0 0 ${colors.accent}00;
      transition:
        box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
        transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      /* 顶部彩色渐变线 —— 品牌记忆点 */
      border-top: 2px solid transparent;
      background-clip: padding-box;
      position: relative;
    }
    .diagram-card::before {
      content: '';
      position: absolute;
      top: -2px; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, var(--accent), ${accentAlphaHover.replace('rgba', 'rgba').replace(/,[\d.]+\)/, ',0.6)')}, var(--accent));
      background-size: 200% 100%;
      animation: shimmer 3s ease infinite;
      border-radius: var(--radius-card) var(--radius-card) 0 0;
      opacity: 0.8;
    }
    @keyframes shimmer {
      0%   { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }
    .diagram-card:hover {
      box-shadow:
        0 2px 8px rgba(0,0,0,${isLight ? '.06' : '.22'}),
        0 12px 32px rgba(0,0,0,${isLight ? '.06' : '.18'}),
        0 0 0 1px ${colors.accent}22;
      transform: translateY(-2px);
    }

    /* Card Header */
    .diagram-card-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      padding: 22px 26px 18px;
      border-bottom: 1px solid var(--border);
      gap: 16px;
    }
    .diagram-card-header-left {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      min-width: 0;
    }
    .diagram-icon-wrap {
      width: 40px;
      height: 40px;
      border-radius: 11px;
      background: linear-gradient(135deg, var(--accent-a), var(--accent-ah));
      border: 1px solid ${colors.accent}44;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      color: var(--accent);
      box-shadow: 0 2px 8px ${colors.accent}22;
      transition: box-shadow var(--transition);
    }
    .diagram-card:hover .diagram-icon-wrap {
      box-shadow: 0 4px 14px ${colors.accent}40;
    }
    .diagram-icon-wrap svg { display: block; flex-shrink: 0; }
    .diagram-title-wrap { min-width: 0; padding-top: 2px; }
    .diagram-title {
      font-size: 17px;
      font-weight: 700;
      color: var(--heading);
      letter-spacing: -0.025em;
      line-height: 1.3;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .diagram-desc {
      font-size: 12.5px;
      color: var(--muted);
      margin-top: 3px;
      line-height: 1.5;
    }
    .diagram-card-header-right {
      flex-shrink: 0;
      padding-top: 3px;
    }
    .type-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 5px 12px;
      border-radius: 20px;
      border: 1px solid;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.02em;
      white-space: nowrap;
    }

    /* Stats Row */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      border-bottom: 1px solid var(--border);
    }
    .stat-card {
      display: flex;
      position: relative;
      overflow: hidden;
      border-right: 1px solid var(--border);
      transition: background var(--transition);
      cursor: default;
    }
    .stat-card:last-child { border-right: none; }
    .stat-card:hover { background: var(--accent-a); }
    .stat-card:hover .stat-accent-bar { opacity: 1; width: 4px; }
    .stat-accent-bar {
      width: 3px;
      flex-shrink: 0;
      background: linear-gradient(180deg, var(--accent), ${accentAlpha});
      opacity: 0.45;
      transition: opacity var(--transition), width var(--transition);
    }
    .stat-body {
      padding: 16px 16px 14px;
      flex: 1;
      min-width: 0;
    }
    .stat-header {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 7px;
    }
    .stat-icon {
      color: var(--accent);
      opacity: 0.75;
      display: flex;
      align-items: center;
      flex-shrink: 0;
      transition: opacity var(--transition);
    }
    .stat-card:hover .stat-icon { opacity: 1; }
    .stat-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .stat-value {
      font-size: 20px;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: -0.03em;
      line-height: 1.15;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .stat-detail {
      font-size: 11px;
      color: var(--muted);
      margin-top: 3px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    /* SVG Render Area */
    .svg-render-area {
      background: var(--svg-area);
      position: relative;
      width: 100%;
      min-height: min(52vw, 480px);
      overflow: visible;
      display: flex;
      align-items: center;
      justify-content: center;
      /* 点阵背景 — 让 SVG 悬浮在网格上 */
      background-image:
        radial-gradient(circle, ${isLight ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.08)'} 1px, transparent 1px);
      background-size: 20px 20px;
      background-color: var(--svg-area);
    }
    .svg-render-inner {
      padding: 32px 40px;
      width: 100%;
      min-width: 0;
    }
    .svg-render-inner svg {
      max-width: 100%;
      height: auto;
      display: block;
      margin: 0 auto;
      filter: drop-shadow(0 4px 12px rgba(0,0,0,${isLight ? '0.06' : '0.3'}));
    }

    /* Card Footer / Code Toggle */
    .card-footer {
      padding: 10px 22px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 8px;
      background: ${isLight ? adjustBrightness(colors.bg, -3) : adjustBrightness(colors.bg, 2)};
    }
    .code-toggle-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 13px;
      border-radius: 7px;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      font-family: inherit;
      transition: all var(--transition);
    }
    .code-toggle-btn:hover, .code-toggle-btn.open {
      background: var(--accent-a);
      border-color: ${colors.accent}66;
      color: var(--accent);
    }
    .toggle-chevron { transition: transform 0.22s cubic-bezier(0.4, 0, 0.2, 1); }
    .code-toggle-btn.open .toggle-chevron { transform: rotate(180deg); }

    /* Code Block */
    .code-block {
      display: none;
      border-top: 1px solid var(--border);
    }
    .code-block.open { display: block; }
    .code-block-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 22px;
      background: var(--code-bg);
      border-bottom: 1px solid var(--border);
    }
    .code-lang-tag {
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--muted);
      text-transform: uppercase;
      opacity: 0.7;
    }
    .copy-btn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 10px;
      border-radius: 6px;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
      font-size: 11px;
      font-weight: 500;
      cursor: pointer;
      font-family: inherit;
      transition: all var(--transition);
    }
    .copy-btn:hover { border-color: ${colors.accent}66; color: var(--accent); }
    .copy-btn.copied { color: #22c55e; border-color: #22c55e55; background: #22c55e0e; }
    .code-pre {
      margin: 0;
      padding: 20px 22px;
      background: var(--code-bg);
      overflow-x: auto;
      font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code',
                   'SF Mono', 'Monaco', 'Menlo', 'Consolas', monospace;
      font-size: 12.5px;
      line-height: 1.75;
      color: var(--fg);
      tab-size: 2;
    }
    .code-pre code { display: block; }

    /* ─── Flow Summary ──────────────────────────── */
    .flow-summary {
      border-top: 1px solid var(--border);
      padding: 22px 26px 18px;
      background: ${isLight ? adjustBrightness(colors.bg, -2) : adjustBrightness(colors.bg, 3)};
    }
    .summary-header {
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 14px;
    }
    .summary-header svg { opacity: 0.85; }
    .summary-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .summary-block {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      transition: border-color var(--transition);
    }
    .summary-block:hover { border-color: ${colors.accent}55; }
    .summary-block-wide { grid-column: 1 / -1; }
    .summary-block-label {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      border-bottom: 1px solid var(--border);
      background: ${isLight ? adjustBrightness(colors.bg, -5) : adjustBrightness(colors.bg, 2)};
      opacity: 0.9;
    }
    .summary-block-label svg { opacity: 0.65; flex-shrink: 0; }
    .summary-block-content { padding: 10px 14px; }

    /* 起止节点 */
    .summary-start-end { display: flex; flex-direction: column; gap: 7px; }
    .summary-se-item {
      display: flex;
      align-items: center;
      gap: 9px;
      font-size: 12.5px;
    }
    .summary-se-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .summary-se-dot.start { background: #22c55e; box-shadow: 0 0 6px #22c55e66; }
    .summary-se-dot.end   { background: #ef4444; box-shadow: 0 0 6px #ef444466; }
    .summary-se-label {
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.06em;
      color: var(--muted);
      min-width: 28px;
      text-transform: uppercase;
    }
    .summary-se-val {
      color: var(--fg);
      font-size: 12.5px;
      font-weight: 500;
    }

    /* 角色标签 */
    .summary-roles { display: flex; flex-wrap: wrap; gap: 5px; }
    .summary-role-tag {
      display: inline-flex;
      align-items: center;
      padding: 3px 10px;
      border-radius: 14px;
      font-size: 11.5px;
      font-weight: 500;
      background: var(--accent-a);
      color: var(--accent);
      border: 1px solid ${colors.accent}44;
      transition: background var(--transition);
    }
    .summary-role-tag:hover { background: var(--accent-ah); }

    /* 主流程步骤 */
    .summary-steps { display: flex; flex-wrap: wrap; gap: 5px; align-items: flex-start; }
    .summary-step-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 10px 3px 5px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 7px;
      font-size: 12px;
      transition: border-color var(--transition);
    }
    .summary-step-item:hover { border-color: ${colors.accent}55; }
    .summary-step-num {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--accent);
      color: ${isLight ? '#fff' : '#fff'};
      font-size: 9px;
      font-weight: 700;
      flex-shrink: 0;
    }
    .summary-step-text { color: var(--fg); font-weight: 500; }

    /* 判断分支 */
    .summary-branch-item {
      display: flex;
      flex-direction: column;
      gap: 5px;
      margin-bottom: 9px;
    }
    .summary-branch-item:last-child { margin-bottom: 0; }
    .summary-branch-q {
      font-size: 12px;
      font-weight: 600;
      color: var(--fg);
    }
    .summary-branch-conds { display: flex; flex-wrap: wrap; gap: 4px; }
    .summary-cond-tag {
      display: inline-flex;
      align-items: center;
      padding: 2px 9px;
      background: #3b82f614;
      color: #3b82f6;
      border: 1px solid #3b82f640;
      border-radius: 6px;
      font-size: 11.5px;
      transition: background var(--transition);
    }
    .summary-cond-tag:hover { background: #3b82f622; }
    .summary-empty { font-size: 11.5px; color: var(--muted); font-style: italic; opacity: 0.7; }

    /* 异常分支 */
    .summary-errors { display: flex; flex-wrap: wrap; gap: 5px; }
    .summary-error-tag {
      display: inline-flex;
      align-items: center;
      padding: 3px 10px;
      background: #ef444414;
      color: #ef4444;
      border: 1px solid #ef444440;
      border-radius: 6px;
      font-size: 11.5px;
      transition: background var(--transition);
    }
    .summary-error-tag:hover { background: #ef444422; }

    /* ─── Self Check Panel ───────────────────────── */
    .self-check-panel {
      border-top: 1px solid var(--border);
      padding: 20px 26px 18px;
      background: ${isLight ? adjustBrightness(colors.bg, -4) : adjustBrightness(colors.bg, 2)};
    }
    .check-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      gap: 12px;
    }
    .check-header-left {
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--fg);
    }
    .check-header-left svg { color: var(--accent); opacity: 0.85; }
    .check-overall {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 12px;
      border-radius: 20px;
      border: 1px solid;
      font-size: 11.5px;
      font-weight: 600;
    }
    .check-items {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
    }
    .check-item {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 11px 13px;
      transition: background var(--transition), border-color var(--transition), transform var(--transition);
    }
    .check-item:hover {
      background: var(--check-bg, var(--accent-a));
      border-color: var(--check-color, var(--accent));
      transform: translateY(-1px);
    }
    .check-item-header {
      display: flex;
      align-items: center;
      gap: 5px;
      margin-bottom: 6px;
    }
    .check-icon { display: flex; align-items: center; flex-shrink: 0; }
    .check-label {
      flex: 1;
      font-size: 11.5px;
      font-weight: 600;
      color: var(--fg);
    }
    .check-badge {
      display: inline-flex;
      align-items: center;
      padding: 1px 6px;
      border-radius: 10px;
      border: 1px solid;
      font-size: 10px;
      font-weight: 600;
      flex-shrink: 0;
    }
    .check-message {
      font-size: 11px;
      color: var(--muted);
      line-height: 1.55;
    }

    /* ─── Sidebar Overlay (mobile) ──────────────── */
    .sidebar-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.4);
      z-index: 90;
      backdrop-filter: blur(2px);
    }
    .sidebar-overlay.show { display: block; }

    /* ─── Scrollbar Global ──────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--muted); }

    /* ─── Stagger animation for sections ────────── */
    .diagram-section:nth-child(1)  { animation-delay: 0.05s; }
    .diagram-section:nth-child(2)  { animation-delay: 0.12s; }
    .diagram-section:nth-child(3)  { animation-delay: 0.18s; }
    .diagram-section:nth-child(4)  { animation-delay: 0.24s; }
    .diagram-section:nth-child(5)  { animation-delay: 0.30s; }
    .diagram-section:nth-child(n+6){ animation-delay: 0.36s; }

    /* ─── prefers-reduced-motion ────────────────── */
    @media (prefers-reduced-motion: reduce) {
      .diagram-section {
        animation: none;
        opacity: 1;
        transform: none;
      }
      .diagram-card::before { animation: none; }
      .diagram-card:hover { transform: none; }
      .check-item:hover { transform: none; }
      * { transition-duration: 0.01ms !important; }
    }

    /* ─── Focus styles ──────────────────────────── */
    :focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 2px;
      border-radius: 4px;
    }

    /* ─── Mermaid 关键词语法着色 ─────────────────── */
    /* 基础关键词 - graph/flowchart 方向 */
    .code-pre .kw-dir { color: ${isLight ? '#7c3aed' : '#bb9af7'}; font-weight: 500; }
    /* 节点声明符号 */
    .code-pre .kw-node { color: ${isLight ? '#0369a1' : '#7dcfff'}; }
    /* 箭头/边 */
    .code-pre .kw-arrow { color: ${isLight ? '#15803d' : '#9ece6a'}; }
    /* 字符串/文本 */
    .code-pre .kw-string { color: ${isLight ? '#b45309' : '#e0af68'}; }
    /* 注释 */
    .code-pre .kw-comment { color: var(--muted); font-style: italic; }
    /* 关键词 (graph, flowchart, sequence 等) */
    .code-pre .kw-type { color: ${isLight ? '#9333ea' : '#7aa2f7'}; font-weight: 600; }

    /* ─── Fullscreen Overlay ─────────────────────── */
    .fullscreen-overlay {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 500;
      background: ${isLight ? 'rgba(255,255,255,0.95)' : 'rgba(10,10,15,0.96)'};
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      align-items: center;
      justify-content: center;
      padding: 40px;
      cursor: zoom-out;
    }
    .fullscreen-overlay.show {
      display: flex;
      animation: fsIn 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    }
    @keyframes fsIn {
      from { opacity: 0; transform: scale(0.96); }
      to   { opacity: 1; transform: scale(1); }
    }
    .fullscreen-overlay svg {
      max-width: 90vw;
      max-height: 90vh;
      width: auto;
      height: auto;
    }
    .fullscreen-close {
      position: absolute;
      top: 20px;
      right: 24px;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--muted);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all var(--transition);
    }
    .fullscreen-close:hover {
      background: var(--accent-a);
      color: var(--accent);
      border-color: var(--accent);
    }
    .fullscreen-kbd-hints {
      position: absolute;
      bottom: 18px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      color: rgba(255,255,255,0.35);
      pointer-events: none;
      white-space: nowrap;
    }
    .fullscreen-kbd-hints kbd {
      display: inline-block;
      padding: 1px 5px;
      border-radius: 4px;
      background: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.18);
      font-family: inherit;
      font-size: 10px;
      line-height: 16px;
    }
    /* SVG 区域点击全屏：pointer-events:none 让 SVG 内部元素不吸收点击，点击自然冒泡到 .svg-render-area */
    .svg-render-area {
      cursor: zoom-in;
    }
    .svg-render-area:focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: -2px;
    }
    /* 让 SVG 内部所有子元素不拦截鼠标事件 */
    .svg-render-inner svg,
    .svg-render-inner svg * {
      pointer-events: none !important;
    }
    .svg-zoom-hint {
      position: absolute;
      bottom: 10px;
      right: 14px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 20px;
      background: ${isLight ? 'rgba(0,0,0,0.07)' : 'rgba(255,255,255,0.08)'};
      font-size: 10.5px;
      color: var(--muted);
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.2s;
      font-family: inherit;
    }
    .svg-render-area:hover .svg-zoom-hint { opacity: 1; }

    /* ─── Responsive ────────────────────────────── */
    @media (max-width: 960px) {
      .sidebar {
        transform: translateX(-100%);
        z-index: 150;
        background: var(--sidebar-bg);
        box-shadow: 4px 0 20px rgba(0,0,0,0.2);
      }
      .sidebar.open {
        transform: translateX(0);
      }
      .main-content { margin-left: 0; max-width: 100%; padding: 24px 20px 56px; }
      .menu-btn { display: inline-flex; }
      .stats-row { grid-template-columns: repeat(2, 1fr); }
      .stat-card:nth-child(2) { border-right: none; }
      .summary-grid { grid-template-columns: 1fr; }
      .check-items { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 640px) {
      :root { --header-h: 54px; }
      .stats-row { grid-template-columns: 1fr 1fr; }
      .top-header-right .theme-pill,
      .top-header-right .diagram-count-badge,
      .top-header-right .header-kbd-hint { display: none; }
      .main-content { padding: 16px 14px 48px; }
      .svg-render-inner { padding: 20px 16px; }
      .check-items { grid-template-columns: 1fr 1fr; }
      .flow-summary, .self-check-panel { padding: 16px 16px 14px; }
      .diagram-card-header { padding: 16px 18px 14px; }
      .diagram-title { font-size: 15px; }
    }
  </style>
</head>
<body data-theme="${isLight ? 'light' : 'dark'}">

<!-- ─── Skip to main content (WCAG 2.4.1) ─── -->
<a class="skip-link" href="#main-content">Skip to main content</a>

<!-- ─── Fullscreen SVG Overlay ─── -->
<div class="fullscreen-overlay" id="fullscreen-overlay" role="dialog" aria-modal="true" aria-label="Full screen diagram" onclick="closeFullscreen(event)">
  <button class="fullscreen-close" onclick="closeFullscreen()" aria-label="Close fullscreen (ESC)">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  </button>
  <div class="fullscreen-kbd-hints" aria-hidden="true">
    <kbd>ESC</kbd> 退出 &nbsp;·&nbsp; <kbd>F</kbd> 浏览器全屏
  </div>
  <div id="fullscreen-content"></div>
</div>

<!-- ─── Mobile Sidebar Overlay ─── -->
<div class="sidebar-overlay" id="sidebar-overlay" onclick="closeSidebar()"></div>

<!-- ═══ Fixed Top Header ═══ -->
<header class="top-header" role="banner">
  <div class="top-header-left">
    <button class="menu-btn" id="menu-btn" onclick="toggleSidebar()" aria-label="Toggle navigation">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    </button>
    <div class="header-logo">
      ${logoDatasUri
        ? `<img src="${logoDatasUri}" alt="Beautiful Mermaid" width="22" height="22" style="display:block;object-fit:contain;border-radius:5px;">`
        : ''}
      Beautiful Mermaid
    </div>
    <div class="header-divider"></div>
    <div class="header-meta">
      <div class="header-title">${escHtml(title)}</div>
      ${subtitle ? `<div class="header-subtitle">${escHtml(subtitle)}</div>` : ''}
    </div>
  </div>
  <div class="top-header-right">
    <span class="theme-pill">
      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <circle cx="12" cy="12" r="4"/>
        <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
      </svg>
      ${escHtml(themeName)}
    </span>
    <span class="diagram-count-badge">
      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>
      </svg>
      ${diagrams.length} diagrams
    </span>
    <span class="header-kbd-hint" aria-hidden="true" title="按 F 切换浏览器全屏">
      <kbd>F</kbd> 全屏
    </span>
  </div>
</header>

<!-- ═══ App Layout ═══ -->
<div class="app-layout">

  <!-- ─── Sidebar / TOC ─── -->
  <aside class="sidebar" id="sidebar" role="navigation" aria-label="Diagram contents">
    <div class="sidebar-section-title">Contents</div>
    ${tocNav}
  </aside>

  <!-- ─── Main Content ─── -->
  <main class="main-content" id="main-content" role="main" tabindex="-1">
    ${diagramCards}
  </main>

</div>

<script>
// ─── TOC 高亮（基于 IntersectionObserver）+ URL hash 深链接
(function() {
  const tocLinks = document.querySelectorAll('.toc-item');
  const sections = document.querySelectorAll('.diagram-section');
  if (!sections.length) return;

  // 初始化：若 URL 有 hash，滚动到对应 section
  const initHash = window.location.hash;
  if (initHash) {
    const target = document.querySelector(initHash);
    if (target) {
      requestAnimationFrame(() => {
        const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 60;
        const top = target.getBoundingClientRect().top + window.scrollY - offset - 20;
        window.scrollTo({ top, behavior: 'smooth' });
      });
    }
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        tocLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === '#' + id);
        });
        // 更新 URL hash（不触发跳转）
        if (history.replaceState) {
          history.replaceState(null, '', '#' + id);
        }
        // 同步 TOC 滚动到可见区
        const activeLink = document.querySelector('.toc-item.active');
        if (activeLink) {
          activeLink.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
      }
    });
  }, { rootMargin: '-60px 0px -55% 0px', threshold: 0 });

  sections.forEach(s => observer.observe(s));
})();

// ─── 平滑滚动
function scrollToCard(idx, event) {
  event && event.preventDefault();
  const el = document.getElementById('diagram-' + idx);
  if (el) {
    const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 60;
    const top = el.getBoundingClientRect().top + window.scrollY - offset - 20;
    window.scrollTo({ top, behavior: 'smooth' });
  }
  // 移动端点击 TOC 后关闭侧边栏
  if (window.innerWidth <= 960) closeSidebar();
}

// ─── 移动端侧边栏
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const isOpen  = sidebar.classList.toggle('open');
  overlay.classList.toggle('show', isOpen);
  document.getElementById('menu-btn').setAttribute('aria-expanded', isOpen ? 'true' : 'false');
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebar-overlay').classList.remove('show');
  const menuBtn = document.getElementById('menu-btn');
  if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
}

// ─── 代码块展开/收起
function toggleCode(id, btn) {
  const block = document.getElementById(id);
  if (!block) return;
  const isOpen = block.classList.toggle('open');
  btn.classList.toggle('open', isOpen);
  btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  // 更新按钮文本（第三个文本节点）
  for (const node of btn.childNodes) {
    if (node.nodeType === 3 && node.textContent.trim()) {
      node.textContent = isOpen ? ' 收起源码' : ' 查看源码';
      break;
    }
  }
}

// ─── 复制代码
async function copyCode(id) {
  const el = document.getElementById(id);
  if (!el) return;
  try {
    await navigator.clipboard.writeText(el.textContent);
    const btn = el.closest('.code-block').querySelector('.copy-btn');
    if (btn) {
      const orig = btn.innerHTML;
      btn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> 已复制';
      btn.classList.add('copied');
      setTimeout(() => { btn.innerHTML = orig; btn.classList.remove('copied'); }, 2000);
    }
  } catch(e) {
    try {
      const range = document.createRange();
      range.selectNode(el);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
      document.execCommand('copy');
      window.getSelection().removeAllRanges();
    } catch(_) {}
}

// ─── SVG 区域点击全屏（事件委托，在 document 级捕获）
document.addEventListener('click', function(e) {
  const area = e.target.closest('.svg-render-area');
  if (!area) return;
  const idx = parseInt(area.dataset.idx, 10);
  if (!isNaN(idx)) openFullscreen(idx);
});
document.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' || e.key === ' ') {
    const area = e.target.closest('.svg-render-area');
    if (!area) return;
    e.preventDefault();
    const idx = parseInt(area.dataset.idx, 10);
    if (!isNaN(idx)) openFullscreen(idx);
  }
});

// ─── 全屏查看 SVG
function openFullscreen(idx) {
  const container = document.getElementById('svg-container-' + idx);
  if (!container) return;
  const svgEl = container.querySelector('svg');
  if (!svgEl) return;
  const fsContent = document.getElementById('fullscreen-content');
  fsContent.innerHTML = '';
  const clone = svgEl.cloneNode(true);
  clone.removeAttribute('width');
  clone.removeAttribute('height');
  clone.style.maxWidth  = '90vw';
  clone.style.maxHeight = '90vh';
  clone.style.width     = 'auto';
  clone.style.height    = 'auto';
  // 全屏内的 SVG 允许交互（拖动等）
  clone.style.pointerEvents = 'all';
  clone.querySelectorAll('*').forEach(el => el.style.pointerEvents = '');
  fsContent.appendChild(clone);
  const overlay = document.getElementById('fullscreen-overlay');
  overlay.classList.add('show');
  document.body.style.overflow = 'hidden';
  const closeBtn = overlay.querySelector('.fullscreen-close');
  if (closeBtn) setTimeout(() => closeBtn.focus(), 50);
}
function closeFullscreen(e) {
  if (e && e.type === 'click') {
    // 只允许点击纯背景遮罩（overlay 本身）或关闭按钮时关闭；点击 SVG 内容区不关闭
    const overlay = document.getElementById('fullscreen-overlay');
    const isBackdrop = e.target === overlay;
    const isCloseBtn = e.target.closest && e.target.closest('.fullscreen-close');
    if (!isBackdrop && !isCloseBtn) return;
  }
  const overlay = document.getElementById('fullscreen-overlay');
  if (!overlay) return;
  overlay.classList.remove('show');
  document.body.style.overflow = '';
}

// ─── 全屏弹窗：移动端触摸手势（下滑关闭）
(function() {
  let _touchStartY = 0, _touchStartX = 0;
  document.addEventListener('touchstart', function(e) {
    const overlay = document.getElementById('fullscreen-overlay');
    if (!overlay || !overlay.classList.contains('show')) return;
    _touchStartY = e.touches[0].clientY;
    _touchStartX = e.touches[0].clientX;
  }, { passive: true });
  document.addEventListener('touchend', function(e) {
    const overlay = document.getElementById('fullscreen-overlay');
    if (!overlay || !overlay.classList.contains('show')) return;
    const dy = e.changedTouches[0].clientY - _touchStartY;
    const dx = e.changedTouches[0].clientX - _touchStartX;
    // 下滑距离 > 80px 且垂直方向为主时关闭
    if (dy > 80 && Math.abs(dy) > Math.abs(dx) * 1.5) {
      overlay.classList.remove('show');
      document.body.style.overflow = '';
    }
  }, { passive: true });
})();

// ─── 键盘全局快捷键
document.addEventListener('keydown', e => {
  // ESC：关闭全屏或侧边栏
  if (e.key === 'Escape') {
    const fs = document.getElementById('fullscreen-overlay');
    if (fs && fs.classList.contains('show')) {
      fs.classList.remove('show');
      document.body.style.overflow = '';
    } else {
      closeSidebar();
    }
    return;
  }
  // F / f：切换浏览器全屏
  if ((e.key === 'f' || e.key === 'F') && !e.ctrlKey && !e.metaKey && !e.altKey) {
    const tag = document.activeElement && document.activeElement.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return; // 输入框内不触发
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
    } else {
      document.exitFullscreen && document.exitFullscreen();
    }
  }
});

// ─── Mermaid 语法着色（简易 tokenizer）
(function highlightMermaid() {
  const KEYWORDS = /^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|stateDiagram-v2|erDiagram|gantt|pie|xychart-beta|mindmap|timeline|gitGraph|TD|TB|LR|RL|BT)$/i;
  const ARROWS = /^(-+>|-->|-\.->|===>|--[|o*]|<--)/;
  const pres = document.querySelectorAll('.code-pre code');
  pres.forEach(pre => {
    const lines = pre.textContent.split('\\n');
    pre.innerHTML = lines.map(line => {
      // 注释行
      if (/^\\s*%%/.test(line)) {
        return '<span class="kw-comment">' + escHtml2(line) + '</span>';
      }
      // 逐词着色
      return line.replace(/("[^"]*")|(%%.*)|(-->|-->|==>|-.->|--[|o*x]?[->]|<--)|(\\b(?:graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(?:-v2)?|erDiagram|gantt|pie|xychart-beta|mindmap|timeline|gitGraph|TD|TB|LR|RL|BT|participant|actor|activate|deactivate|loop|alt|else|end|opt|par|critical|break|rect|Note|note)\\b)/g,
        (m, str, cmt, arr, kw) => {
          if (str) return '<span class="kw-string">' + escHtml2(m) + '</span>';
          if (cmt) return '<span class="kw-comment">' + escHtml2(m) + '</span>';
          if (arr) return '<span class="kw-arrow">' + escHtml2(m) + '</span>';
          if (kw)  return '<span class="kw-type">' + escHtml2(m) + '</span>';
          return escHtml2(m);
        }
      );
    }).join('\\n');
  });
  function escHtml2(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
})();
</script>
</body>
</html>`;
}

// ─── 颜色工具 ────────────────────────────────────────────────────────────────

/**
 * 调整十六进制颜色亮度（正值增亮，负值降暗）
 */
function adjustBrightness(hex, amount) {
  const h = hex.replace('#', '');
  if (h.length !== 6) return hex;
  const r = Math.max(0, Math.min(255, parseInt(h.slice(0,2), 16) + amount));
  const g = Math.max(0, Math.min(255, parseInt(h.slice(2,4), 16) + amount));
  const b = Math.max(0, Math.min(255, parseInt(h.slice(4,6), 16) + amount));
  return '#' + [r,g,b].map(v => v.toString(16).padStart(2,'0')).join('');
}

/**
 * 十六进制颜色转 RGB 对象
 */
function hexToRgb(hex) {
  const h = hex.replace('#', '');
  if (h.length !== 6) return null;
  return {
    r: parseInt(h.slice(0,2), 16),
    g: parseInt(h.slice(2,4), 16),
    b: parseInt(h.slice(4,6), 16),
  };
}

// ─── 主流程 ──────────────────────────────────────────────────────────────────

async function main() {
  const options = parseArgs();

  if (!options.title) {
    console.error('错误: 请提供图表集标题（第一个位置参数）');
    showHelp();
    process.exit(1);
  }

  // 收集 .mmd 文件路径
  let mmdFiles = [];
  if (options.batch) {
    if (!fs.existsSync(options.batch)) {
      console.error(`错误: 目录不存在 ${options.batch}`);
      process.exit(1);
    }
    mmdFiles = fs.readdirSync(options.batch)
      .filter(f => f.endsWith('.mmd'))
      .sort()
      .map(f => path.join(options.batch, f));
  } else if (options.diagrams.length > 0) {
    mmdFiles = options.diagrams;
  } else {
    console.error('错误: 请通过 --diagrams 指定文件，或通过 --batch 指定目录');
    showHelp();
    process.exit(1);
  }

  if (mmdFiles.length === 0) {
    console.error('错误: 未找到 .mmd 文件');
    process.exit(1);
  }

  // 动态导入 beautiful-mermaid (ESM)
  const { renderMermaidSVG, THEMES } = await import('beautiful-mermaid');

  // 解析主题
  const rawTheme = options.theme;
  const resolvedTheme = resolveTheme(rawTheme);
  const colors = extractThemeColors(rawTheme, resolvedTheme);
  const effectivePreset = options.preset || getRecommendedPreset(rawTheme) || 'glass';

  console.log(`\n主题: ${rawTheme} · 预设: ${effectivePreset}`);
  console.log(`渲染 ${mmdFiles.length} 个图表...\n`);

  // 渲染每个图表
  const diagrams = [];
  for (const filePath of mmdFiles) {
    if (!fs.existsSync(filePath)) {
      console.warn(`  ⚠ 文件不存在，跳过: ${filePath}`);
      continue;
    }
    const content = fs.readFileSync(filePath, 'utf-8');
    const meta = parseMmdMeta(content, filePath);

    try {
      // 过滤掉注释行（# 开头），避免 mermaid 解析报错
      const renderCode = content
        .split('\n')
        .filter(l => !l.trim().startsWith('#'))
        .join('\n')
        .trim();

      const renderOptions = { ...resolvedTheme, interactive: false };
      let svg = renderMermaidSVG(renderCode, renderOptions);
      svg = injectStylesToSVG(svg, resolvedTheme, effectivePreset);

      // 移除 svg 的固定 width/height，让它能够响应式缩放
      svg = svg
        .replace(/\bwidth="[^"]*"/, 'width="100%"')
        .replace(/\bheight="[^"]*px"/, '');

      // 将原始 mmd 源码保存（去掉 @meta 注释行，只保留可读代码）
      const mmdSource = content
        .split('\n')
        .filter(l => !l.trim().match(/^#\s*@(title|desc|icon|meta|type)\b/))
        .join('\n')
        .trim();

      diagrams.push({ meta, svgContent: svg, filePath, mmdSource });
      console.log(`  ✓ ${path.basename(filePath)} → ${meta.title} [${meta.type}]`);
    } catch (err) {
      console.error(`  ✗ ${path.basename(filePath)}: ${err.message}`);
    }
  }

  if (diagrams.length === 0) {
    console.error('错误: 所有图表渲染失败，无法生成 HTML');
    process.exit(1);
  }

  // 生成 HTML
  const html = buildHtml(options, diagrams, colors, rawTheme, effectivePreset);

  // 确保输出目录存在
  const outputDir = path.dirname(path.resolve(options.output));
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(options.output, html, 'utf-8');

  const absPath = path.resolve(options.output);
  console.log(`\n✓ Rich HTML 已生成: ${absPath}`);
  console.log(`  包含 ${diagrams.length} 张图表 · 主题: ${rawTheme} · 预设: ${effectivePreset}\n`);
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
