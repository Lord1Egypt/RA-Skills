/**
 * 投标文件编制助手 — 可配置化标书生成引擎
 *
 * 接收配置对象，生成格式正确的投标文件 docx。
 * 支持：四种编号体系、动态章节列表、自定义项目编号、封面【正本】、X/100 页脚。
 *
 * 使用方式:
 *   node generate_bid_template.js [--config config.json] [--out output.docx]
 *
 * 也可在 JS 中作为模块调用：
 *   const { generateBidDocument } = require('./generate_bid_template.js');
 *   generateBidDocument(config).then(buffer => ...);
 */

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageBreak, PageNumber, TableOfContents,
  TabStopType, TabStopPosition, convertInchesToTwip
} = require('docx');

// ============================================================
// 格式常量
// ============================================================
const PAGE_W = 11906;        // A4
const PAGE_H = 16838;
const MARGIN = 1440;         // ~2.5cm
const LINE_BODY = 360;       // 1.5倍行距
const LINE_TABLE = 300;      // 1.25倍行距
const INDENT_FIRST = 480;    // 首行缩进2字符
const TB = { style: BorderStyle.SINGLE, size: 1, color: '000000' };
const TBL_BORDERS = { top: TB, bottom: TB, left: TB, right: TB };
const TBL_CELL_MARGINS = { top: 60, bottom: 60, left: 100, right: 100 };

// ============================================================
// 编号体系定义
// ============================================================
const NUMBERING_SCHEMES = {
  // 体系一：纯阿拉伯数字级联（推荐默认）
  // H4=1.1.1.1, H5=1.1.1.1.1
  scheme1: {
    name: '体系一：纯阿拉伯数字级联',
    generate: (level, counters) => {
      if (level === 1) return `${counters[0]}`;
      if (level === 2) return `${counters[0]}.${counters[1]}`;
      if (level === 3) return `${counters[0]}.${counters[1]}.${counters[2]}`;
      if (level === 4) return `${counters[0]}.${counters[1]}.${counters[2]}.${counters[3]}`;
      if (level === 5) return `${counters[0]}.${counters[1]}.${counters[2]}.${counters[3]}.${counters[4]}`;
      return '';
    }
  },
  // 体系二：阿拉伯数字+符号转换
  // H4=(1), H5=①
  scheme2: {
    name: '体系二：阿拉伯数字+符号转换',
    generate: (level, counters) => {
      if (level === 1) return `${counters[0]}`;
      if (level === 2) return `${counters[0]}.${counters[1]}`;
      if (level === 3) return `${counters[0]}.${counters[1]}.${counters[2]}`;
      if (level === 4) return `(${counters[3]})`;
      if (level === 5) return numberToCircle(counters[4]);
      return '';
    }
  },
  // 体系三：政府/事业单位格式
  // H1=一、 H2=（一） H3=1 H4=（1） H5=①
  scheme3: {
    name: '体系三：政府/事业单位格式',
    generate: (level, counters) => {
      if (level === 1) return `${numberToChinese(counters[0])}、`;
      if (level === 2) return `（${numberToChinese(counters[1])}）`;
      if (level === 3) return `${counters[2]}`;
      if (level === 4) return `（${counters[3]}）`;
      if (level === 5) return numberToCircle(counters[4]);
      return '';
    }
  },
  // 体系四：工程类格式
  // H1=第一章 H2=第一节 H3=一、 H4=（一） H5=1.
  scheme4: {
    name: '体系四：工程类格式',
    generate: (level, counters) => {
      if (level === 1) return `第${numberToChinese(counters[0])}章`;
      if (level === 2) return `第${numberToChinese(counters[1])}节`;
      if (level === 3) return `${numberToChinese(counters[2])}、`;
      if (level === 4) return `（${numberToChinese(counters[3])}）`;
      if (level === 5) return `${counters[4]}.`;
      return '';
    }
  }
};

// ============================================================
// 辅助函数
// ============================================================

/**
 * 阿拉伯数字 → 中文数字（完整转换，支持至亿级）。
 * P2 修复：原实现仅支持 1–20，第 21+ 章号在 scheme3/scheme4 下会落回阿拉伯数字
 * （如「第29章」而非「第二十九章」）。现支持任意正整数，超亿级回退阿拉伯数字。
 */
function numberToChinese(num) {
  if (!Number.isInteger(num) || num < 0) return String(num);
  if (num === 0) return '零';
  const digits = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'];
  const units = ['', '十', '百', '千'];

  if (num <= 20) {
    const small = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
      '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十'];
    return small[num];
  }

  // 递归处理 万/亿 级
  if (num >= 100000000) {
    const yi = Math.floor(num / 100000000);
    const rem = num % 100000000;
    const yiStr = numberToChinese(yi) + '亿';
    const remStr = rem === 0 ? '' : (rem < 10000000 ? '零' + numberToChinese(rem) : numberToChinese(rem));
    return yiStr + remStr;
  }
  if (num >= 10000) {
    const wan = Math.floor(num / 10000);
    const rem = num % 10000;
    const wanStr = numberToChinese(wan) + '万';
    const remStr = rem === 0 ? '' : (rem < 1000 ? '零' + numberToChinese(rem) : numberToChinese(rem));
    return wanStr + remStr;
  }

  // 1–9999：按位转换，处理零与「一十→十」
  const str = String(num);
  const len = str.length;
  let s = '';
  for (let i = 0; i < len; i++) {
    const d = Number(str[i]);
    const pos = len - 1 - i;
    if (d === 0) {
      if (s.length > 0 && !s.endsWith('零')) s += '零';
    } else if (pos === 1 && d === 1 && s === '') {
      // 十位为 1 且位于首位：十五而非一十五
      s += '十';
    } else {
      s += digits[d] + units[pos];
    }
  }
  return s.replace(/零+$/, '');
}

/** 数字 → 圈号字符（1→①, 2→②, ... 20→⑳） */
function numberToCircle(n) {
  if (n >= 1 && n <= 20) {
    return String.fromCharCode(0x2460 + n - 1);
  }
  return `(${n})`;
}

/** 生成带编号的标题文本 */
function generateHeadingText(schemeKey, chapters) {
  // 按层级和顺序维护计数器
  const counters = [0, 0, 0, 0, 0];
  const schemeFn = NUMBERING_SCHEMES[schemeKey];
  if (!schemeFn) {
    // 回退到体系一
    return chapters.map(ch => ({ ...ch, title: ch.title }));
  }

  return chapters.map(ch => {
    const level = ch.level;
    // 重置当前层级以下的所有计数器
    counters[level - 1]++;
    for (let i = level; i < 5; i++) counters[i] = 0;
    // P1 修复：若祖先层级计数器仍为 0（输入层级不连续），置 1，避免 0.0.0.1
    for (let i = 0; i < level - 1; i++) {
      if (counters[i] === 0) counters[i] = 1;
    }
    const num = schemeFn.generate(level, counters);
    const fullTitle = num ? `${num} ${ch.title}` : ch.title;
    return { ...ch, title: fullTitle, number: num };
  });
}

// ============================================================
// 段落/表格生成函数
// ============================================================

function bodyPara(text, opts = {}) {
  return new Paragraph({
    spacing: { line: LINE_BODY, before: 0, after: 0 },
    indent: opts.noIndent ? undefined : { firstLine: INDENT_FIRST },
    alignment: opts.align || AlignmentType.JUSTIFIED,
    children: [new TextRun({
      text, font: opts.font || 'SimSun',
      size: opts.size || 24,
      bold: opts.bold || false
    })]
  });
}

function makeHeading(chapter, config) {
  const fs = config.fonts;
  let levelClass;
  switch (chapter.level) {
    case 1: levelClass = HeadingLevel.HEADING_1; break;
    case 2: levelClass = HeadingLevel.HEADING_2; break;
    case 3: levelClass = HeadingLevel.HEADING_3; break;
    case 4: levelClass = HeadingLevel.HEADING_4; break;
    case 5: levelClass = HeadingLevel.HEADING_5; break;
    default: levelClass = undefined;
  }
  const fontKey = `h${Math.min(chapter.level, 5)}`;
  const f = fs[fontKey] || fs.body;
  const size = f.size;
  const fontName = f.name;
  const bold = 'bold' in f ? f.bold : true;

  const opts = {
    spacing: { before: 0, after: 0, line: LINE_BODY },
    children: [new TextRun({
      text: chapter.title,
      font: fontName,
      size: size,
      bold: bold
    })]
  };
  // P1 修复：H1–H5 均授予对应 Heading 样式（此前仅 1–3 级，H4/H5 进不了目录/大纲）
  if (levelClass) {
    opts.heading = levelClass;
  }
  return new Paragraph(opts);
}

function emptyPara() {
  return new Paragraph({
    spacing: { line: LINE_BODY },
    children: [new TextRun({ text: '', font: 'SimSun', size: 24 })]
  });
}

function centeredText(text, sizeVal = 24, fontName = 'SimSun') {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { line: LINE_BODY },
    children: [new TextRun({ text, font: fontName, size: sizeVal })]
  });
}

function centeredBold(text, sizeVal = 24, fontName = 'SimSun') {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { line: LINE_BODY },
    children: [new TextRun({ text, font: fontName, size: sizeVal, bold: true })]
  });
}

function rightAligned(text, sizeVal = 24, fontName = 'SimSun') {
  return new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { line: LINE_BODY },
    children: [new TextRun({ text, font: fontName, size: sizeVal })]
  });
}

function tableCell(text, opts = {}) {
  return new TableCell({
    borders: TBL_BORDERS,
    width: { size: opts.width || 2000, type: WidthType.DXA },
    margins: TBL_CELL_MARGINS,
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    verticalAlign: 'center',
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.LEFT,
      spacing: { line: LINE_TABLE },
      children: [new TextRun({
        text: text || '', font: 'SimSun',
        size: opts.size || 20, bold: opts.bold || false
      })]
    })]
  });
}

function makeTable(headers, rows, colWidths, headerShading = 'D9E2F3') {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  const headerRow = new TableRow({
    children: headers.map((h, i) => tableCell(h, {
      width: colWidths[i], bold: true, shading: headerShading,
      align: AlignmentType.CENTER
    }))
  });
  const dataRows = rows.map(row =>
    new TableRow({
      children: row.map((cell, i) => tableCell(cell, {
        width: colWidths[i],
        align: i === 0 ? AlignmentType.CENTER : AlignmentType.LEFT
      }))
    })
  );
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows]
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ============================================================
// 封面构建
// ============================================================

function buildCoverPage(config) {
  const p = config.project;
  const sizeH1 = config.fonts.h1.size;
  const sizeBody = config.fonts.body.size;
  const fontName = config.fonts.body.name;

  const children = [];

  // 右上角：【正本】
  children.push(
    new Paragraph({
      alignment: AlignmentType.RIGHT,
      spacing: { after: 0 },
      children: [new TextRun({
        text: p.copyMark || '【正本】',
        font: fontName,
        size: 28,
        bold: true
      })]
    })
  );

  // 空行
  for (let i = 0; i < 5; i++) children.push(emptyPara());

  // 投标文件标题
  children.push(centeredText('投 标 文 件', sizeH1, fontName));
  children.push(emptyPara());
  children.push(emptyPara());
  children.push(centeredBold(p.copyMark === '【副本】' ? '副  本' : '正  本', 32, fontName));

  for (let i = 0; i < 3; i++) children.push(emptyPara());

  // 自定义项目编号
  if (p.customNo) {
    const cnParts = p.customNo.split('\n');
    cnParts.forEach(line => {
      children.push(centeredText(line.trim(), sizeBody, fontName));
    });
  }

  // 项目名称
  children.push(centeredText(`项目名称：${p.name}`));
  children.push(emptyPara());

  // 代理编号
  if (p.agentNo) {
    children.push(centeredText(`代理编号：${p.agentNo}`));
    children.push(emptyPara());
  }

  for (let i = 0; i < 5; i++) children.push(emptyPara());

  // 投标人信息
  children.push(centeredText(`投标人名称：${p.bidder}`));
  children.push(emptyPara());
  children.push(centeredText(`投标人地址：${p.address}`));

  for (let i = 0; i < 2; i++) children.push(emptyPara());

  // 日期
  children.push(centeredText(p.date || '20XX年X月'));

  return children;
}

// ============================================================
// 文档样式定义
// ============================================================

function buildStyles(config) {
  const fs = config.fonts;
  const marginEmu = config.page && config.page.margin
    ? config.page.margin : MARGIN;

  const styles = {
    default: {
      document: {
        run: { font: fs.body.name, size: fs.body.size }
      }
    },
    paragraphStyles: []
  };

  // P1 修复：H1–H5 统一生成样式定义（此前仅 1–3，H4/H5 用默认样式与 curated 字体不一致）
  for (let i = 1; i <= 5; i++) {
    const key = `h${i}`;
    const f = fs[key] || fs.body;
    styles.paragraphStyles.push({
      id: `Heading${i}`,
      name: `Heading ${i}`,
      basedOn: 'Normal',
      next: 'Normal',
      quickFormat: true,
      run: { size: f.size, font: f.name, bold: f.bold !== false },
      paragraph: { spacing: { before: 0, after: 0, line: LINE_BODY }, outlineLevel: i - 1 }
    });
  }

  return styles;
}

// ============================================================
// 默认配置
// ============================================================

const DEFAULT_FONTS = {
  body: { name: 'SimSun', size: 24, bold: false },
  h1:   { name: 'SimSun', size: 36, bold: true },
  h2:   { name: 'SimSun', size: 32, bold: true },
  h3:   { name: 'SimSun', size: 30, bold: true },
  h4:   { name: 'SimSun', size: 28, bold: true },
  h5:   { name: 'SimSun', size: 24, bold: true },
};

const DEFAULT_CHAPTERS = [
  { level: 1, title: '投标函' },
  { level: 1, title: '法定代表人（单位负责人）身份证明' },
  { level: 1, title: '授权委托书' },
  { level: 1, title: '联合体协议书' },
  { level: 1, title: '投标保证金' },
  { level: 1, title: '投标一览表' },
  { level: 1, title: '商务和技术偏差表' },
  { level: 1, title: '分项报价表' },
  { level: 1, title: '资格审查资料' },
  { level: 2, title: '基本情况表' },
  { level: 2, title: '投标人资格证明资料' },
  { level: 3, title: '基本资格条件' },
  { level: 3, title: '特定资格条件' },
  { level: 2, title: '投标人资格声明' },
  { level: 1, title: '投标技术方案' },
  { level: 2, title: '响应一览表' },
  { level: 2, title: '项目组人员汇总表' },
  { level: 2, title: '主要人员简历表' },
  { level: 2, title: '综合实力（资质证书复印件）' },
  { level: 2, title: '实施案例' },
  { level: 2, title: '业务方案' },
  { level: 2, title: '技术方案' },
  { level: 2, title: '实施方案' },
  { level: 2, title: '人员投入' },
  { level: 2, title: '售后服务' },
  { level: 1, title: '业绩证明材料' },
  { level: 1, title: '投标单位廉洁承诺书' },
  { level: 1, title: '其他资料' },
  { level: 1, title: '评分索引表' },
];

function mergeConfig(userConfig) {
  const c = { ...userConfig };
  c.project = {
    name: '【项目名称】',
    bidder: '【投标人名称】',
    address: '【投标人地址】',
    tenderer: '【招标人名称】',
    agentNo: '',
    customNo: '',
    date: '20XX年X月',
    copyMark: '【正本】',
    ...(c.project || {})
  };
  c.fonts = {};
  for (const key of Object.keys(DEFAULT_FONTS)) {
    c.fonts[key] = { ...DEFAULT_FONTS[key], ...((c.fonts || {})[key] || {}) };
  }
  // P0-1 修复：优先读 numbering，回退到解析器输出的 numbering_scheme
  c.numbering = c.numbering || c.numbering_scheme || 'scheme1';
  c.chapters = c.chapters || DEFAULT_CHAPTERS;
  // P0-3 修复：解析器 extract_format_info 输出的 format.page 单位为 EMU，
  // 此处转换为 docx.js 所需的 twip（1 inch = 914400 EMU = 1440 twip，比值 635）后套用，
  // 使「按招标文件页面设置生成」真正生效（此前被写死常量丢弃）。
  const srcFmt = c.format || {};
  const srcPage = srcFmt.page || {};
  const emuToTwip = (emu) =>
    (typeof emu === 'number' && emu > 0) ? Math.round(emu / 635) : null;
  c.page = {
    width: emuToTwip(srcPage.width) || PAGE_W,
    height: emuToTwip(srcPage.height) || PAGE_H,
    margin: emuToTwip(srcPage.margin_top) || MARGIN,
    ...(c.page || {})
  };
  return c;
}

// ============================================================
// 主生成函数
// ============================================================

async function generateBidDocument(config) {
  config = mergeConfig(config);

  // 根据编号体系生成标题文本
  const numberedChapters = generateHeadingText(config.numbering, config.chapters);

  // 构建样式
  const styles = buildStyles(config);

  // 构建封面
  const coverChildren = buildCoverPage(config);

  // 构建正文 Children
  const bodyChildren = [];

  // 目录
  bodyChildren.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 0, after: 0, line: LINE_BODY },
    children: [new TextRun({ text: '目  录', font: config.fonts.h1.name, size: config.fonts.h1.size, bold: true })]
  }));
  bodyChildren.push(new TableOfContents('目录', { hyperlink: true, headingStyleRange: '1-4' }));
  bodyChildren.push(pageBreak());

  // 各章节
  for (const ch of numberedChapters) {
    bodyChildren.push(makeHeading(ch, config));
    if (ch.level >= 4) {
      bodyChildren.push(bodyPara('（内容详见招标文件要求，此处需根据具体项目填写。）'));
    } else {
      bodyChildren.push(bodyPara('（此处填写具体内容）'));
    }
  }

  // ====== 页号从2开始，首页无页脚 ======
  // 封面节：无页眉页脚
  const coverSection = {
    properties: {
      page: {
        size: { width: config.page.width, height: config.page.height },
        margin: {
          top: config.page.margin, bottom: config.page.margin,
          left: config.page.margin, right: config.page.margin
        }
      }
    },
    children: coverChildren
  };

  // 正文节：页脚从2开始，首页不显示
  const contentSection = {
    properties: {
      page: {
        size: { width: config.page.width, height: config.page.height },
        margin: {
          top: config.page.margin, bottom: config.page.margin,
          left: config.page.margin, right: config.page.margin
        },
        pageNumbers: { start: 2 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: config.project.name, font: config.fonts.body.name, size: 20 })],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }]
        })]
      })
    },
    footers: {
      // 首页（即正文节第一页/目录页）：空页脚
      first: new Footer({ children: [] }),
      // 后续页：显示 X/总页数
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ children: [PageNumber.CURRENT], font: config.fonts.body.name, size: 20 }),
            new TextRun({ text: ' / ', font: config.fonts.body.name, size: 20 }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: config.fonts.body.name, size: 20 })
          ]
        })]
      })
    },
    children: bodyChildren
  };

  const doc = new Document({
    styles,
    sections: [coverSection, contentSection]
  });

  return await Packer.toBuffer(doc);
}

// ============================================================
// CLI 入口
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  let config = {};
  let outPath = '投标文件.docx';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--config' && i + 1 < args.length) {
      const cfgPath = path.resolve(args[++i]);
      config = JSON.parse(fs.readFileSync(cfgPath, 'utf-8'));
    }
    if (args[i] === '--out' && i + 1 < args.length) {
      outPath = args[++i];
    }
  }

  const buffer = await generateBidDocument(config);
  fs.writeFileSync(outPath, buffer);
  console.log(`[OK] 投标文件已生成: ${outPath} (${(buffer.length / 1024).toFixed(1)} KB)`);
}

// 作为模块导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { generateBidDocument, NUMBERING_SCHEMES, DEFAULT_FONTS, DEFAULT_CHAPTERS };
}

// 直接运行时
if (require.main === module) {
  main().catch(err => { console.error(err); process.exit(1); });
}
