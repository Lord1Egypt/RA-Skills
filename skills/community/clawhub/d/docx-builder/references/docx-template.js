/**
 * Docx Skill — 基于 docx 库的 Word 文档生成模板
 * 风格：PRD 级专业文档（配色、表格、标题、边界条件、验收标准）
 *
 * 使用方式：
 *   const { C, T, TB, P, PH1, PH2, reqTable, ... } = require('./docx-skill');
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, LevelFormat,
  TabStopType, TabStopPosition
} = require('docx');

// ═══════════════════════════════════════════════════════════════════════════════
//  1. 配色系统
// ═══════════════════════════════════════════════════════════════════════════════
const C = {
  brand:      '1E40AF', // deep blue
  brandLight: 'DBEAFE', // light blue fill
  accent:     '0F766E', // teal for section headings
  warn:       'B45309', // amber
  danger:     'B91C1C', // red
  ok:         '15803D', // green
  gray1:      'F8FAFC', // lightest row fill
  gray2:      'E2E8F0', // header fill
  gray3:      '94A3B8', // muted text
  border:     'CBD5E1', // table border
  text:       '1E293B', // body text
};

// ═══════════════════════════════════════════════════════════════════════════════
//  2. 基础样式与边框
// ═══════════════════════════════════════════════════════════════════════════════
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: C.border };
const allBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const cellPad = { top: 90, bottom: 90, left: 140, right: 140 };

// ═══════════════════════════════════════════════════════════════════════════════
//  3. 文本辅助函数
// ═══════════════════════════════════════════════════════════════════════════════
const T  = (text, opts = {}) => new TextRun({ text, font: 'Arial', color: C.text, ...opts });
const TB = (text, opts = {}) => T(text, { bold: true, ...opts });
const TG = (text, opts = {}) => T(text, { color: C.gray3, size: 18, ...opts });
const tagRun = (text, color) => T(`[${text}]`, { color, bold: true, size: 16 });

// ═══════════════════════════════════════════════════════════════════════════════
//  4. 段落辅助函数
// ═══════════════════════════════════════════════════════════════════════════════
const P  = (children, opts = {}) => new Paragraph({
  children: Array.isArray(children) ? children : [children],
  spacing: { after: 100 },
  ...opts
});
const PB = (text, opts = {}) => P(TB(text), opts);

const PH1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [T(text, { bold: true })]
});
const PH2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [T(text, { bold: true })]
});
const PH3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  children: [T(text, { bold: true })]
});

const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

const Pbullet = (text, ref = 'bullets', level = 0) => new Paragraph({
  numbering: { reference: ref, level },
  spacing: { after: 80 },
  children: [T(text)]
});

const Pnum = (text, level = 0) => new Paragraph({
  numbering: { reference: 'numbers', level },
  spacing: { after: 80 },
  children: [T(text)]
});

// ═══════════════════════════════════════════════════════════════════════════════
//  5. 表格辅助函数
// ═══════════════════════════════════════════════════════════════════════════════
const hdrCell = (text, width, span = 1) => new TableCell({
  borders: allBorders,
  width: { size: width, type: WidthType.DXA },
  columnSpan: span,
  shading: { fill: C.gray2, type: ShadingType.CLEAR },
  margins: cellPad,
  verticalAlign: VerticalAlign.CENTER,
  children: [new Paragraph({ children: [TB(text, { size: 18 })], spacing: { after: 0 } })]
});

const dataCell = (content, width, fill = null, opts = {}) => {
  let children;
  if (typeof content === 'string') {
    children = [new Paragraph({ children: [T(content, { size: 18 })], spacing: { after: 0 } })];
  } else if (Array.isArray(content)) {
    children = content;
  } else {
    children = [content];
  }
  return new TableCell({
    borders: allBorders,
    width: { size: width, type: WidthType.DXA },
    shading: fill ? { fill, type: ShadingType.CLEAR } : undefined,
    margins: cellPad,
    verticalAlign: VerticalAlign.CENTER,
    children,
    ...opts,
  });
};

const dataRow = (cells, fill = null) => new TableRow({
  children: cells.map(([t, w]) => dataCell(t, w, fill))
});

const altFill = (i) => (i % 2 === 0 ? C.gray1 : null);

// 多段落单元格内容
const cellParas = (items) => items.map(([label, text]) =>
  new Paragraph({ spacing: { after: 60 }, children: [TB(label, { size: 18 }), T(text, { size: 18 })] })
);

// ═══════════════════════════════════════════════════════════════════════════════
//  6. 业务表格组件
// ═══════════════════════════════════════════════════════════════════════════════

// 需求表：编号 | 优先级 | 功能项 | 描述与规则
const reqTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [900, 700, 1500, 6260],
  rows: [
    new TableRow({ children: [
      hdrCell('编号', 900), hdrCell('优先级', 700),
      hdrCell('功能项', 1500), hdrCell('详细描述 / 字段规则 / 边界条件', 6260)
    ]}),
    ...rows.map((r, i) => new TableRow({ children: [
      dataCell(r.id, 900, altFill(i)),
      dataCell(r.pri, 700, altFill(i)),
      dataCell(r.name, 1500, altFill(i)),
      dataCell(r.desc, 6260, altFill(i)),
    ]}))
  ]
});

// 前置条件表：类型 | 项目 | 说明
const precondTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1400, 1200, 6760],
  rows: [
    new TableRow({ children: [hdrCell('类型', 1400), hdrCell('项目', 1200), hdrCell('说明', 6760)] }),
    ...rows.map((r, i) => new TableRow({ children: [
      dataCell(r.type, 1400, altFill(i)),
      dataCell(r.item, 1200, altFill(i)),
      dataCell(r.desc, 6760, altFill(i)),
    ]}))
  ]
});

// 边界条件表：编号 | 边界场景 | 触发条件 | 系统行为 | 恢复策略
const boundaryTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1000, 1800, 2400, 2160, 2000],
  rows: [
    new TableRow({ children: [
      hdrCell('编号', 1000), hdrCell('边界场景', 1800), hdrCell('触发条件', 2400),
      hdrCell('系统行为', 2160), hdrCell('恢复策略', 2000)
    ]}),
    ...rows.map((r, i) => new TableRow({ children: [
      dataCell(r.id, 1000, altFill(i)),
      dataCell(r.scene, 1800, altFill(i)),
      dataCell(r.trigger, 2400, altFill(i)),
      dataCell(r.behavior, 2160, altFill(i)),
      dataCell(r.recover, 2000, altFill(i)),
    ]}))
  ]
});

// 验收标准表：编号 | 验收项 | 预期结果 | 测试方法 | 优先级
const acTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [900, 2500, 3000, 1460, 1500],
  rows: [
    new TableRow({ children: [
      hdrCell('编号', 900), hdrCell('验收项', 2500), hdrCell('预期结果', 3000),
      hdrCell('测试方法', 1460), hdrCell('优先级', 1500)
    ]}),
    ...rows.map((r, i) => new TableRow({ children: [
      dataCell(r.id, 900, altFill(i)),
      dataCell(r.item, 2500, altFill(i)),
      dataCell(r.expected, 3000, altFill(i)),
      dataCell(r.method, 1460, altFill(i)),
      dataCell(r.pri, 1500, altFill(i)),
    ]}))
  ]
});

// 变更日志表：版本 | 日期 | 作者 | 变更内容
const changeTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [900, 1400, 1800, 5260],
  rows: [
    new TableRow({ children: [hdrCell('版本', 900), hdrCell('日期', 1400), hdrCell('作者', 1800), hdrCell('变更内容', 5260)] }),
    ...rows.map((r, i) => dataRow([[r.ver, 900], [r.date, 1400], [r.author, 1800], [r.desc, 5260]], altFill(i)))
  ]
});

// 通用 4 列表：# | 问题 | 现状 | 期望
const problemTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [800, 2200, 3180, 3180],
  rows: [
    new TableRow({ children: [hdrCell('#', 800), hdrCell('问题', 2200), hdrCell('现状', 3180), hdrCell('期望', 3180)] }),
    ...rows.map((r, i) => dataRow([[r.id, 800], [r.problem, 2200], [r.current, 3180], [r.expect, 3180]], altFill(i)))
  ]
});

// 通用 5 列表：编号 | 指标 | 基线 | 目标 | 衡量方式
const metricTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [900, 3000, 1620, 1620, 2220],
  rows: [
    new TableRow({ children: [
      hdrCell('编号', 900), hdrCell('指标', 3000), hdrCell('基线', 1620),
      hdrCell('目标', 1620), hdrCell('衡量方式', 2220)
    ]}),
    ...rows.map((r, i) => dataRow([[r.id, 900], [r.metric, 3000], [r.baseline, 1620], [r.target, 1620], [r.method, 2220]], altFill(i)))
  ]
});

// 通用 6 列表：角色 | 描述 | 核心痛点 | 使用场景 | 技术能力 | 系统权限
const roleTable = (rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1200, 1600, 1600, 1800, 1680, 1480],
  rows: [
    new TableRow({ children: [
      hdrCell('角色', 1200), hdrCell('描述', 1600), hdrCell('核心痛点', 1600),
      hdrCell('使用场景', 1800), hdrCell('技术能力', 1680), hdrCell('系统权限', 1480)
    ]}),
    ...rows.map((r, i) => dataRow([
      [r.role, 1200], [r.desc, 1600], [r.pain, 1600],
      [r.scene, 1800], [r.tech, 1680], [r.perm, 1480]
    ], altFill(i)))
  ]
});

// 权限矩阵：操作 | 角色1 | 角色2 | ...
const permMatrix = (roles, rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2400, ...roles.map(() => (9360 - 2400) / roles.length)],
  rows: [
    new TableRow({ children: [hdrCell('操作', 2400), ...roles.map(r => hdrCell(r, (9360 - 2400) / roles.length))] }),
    ...rows.map((r, i) => dataRow([[r.action, 2400], ...r.perms.map(p => [p, (9360 - 2400) / roles.length])], altFill(i)))
  ]
});

// ═══════════════════════════════════════════════════════════════════════════════
//  7. UI 组件
// ═══════════════════════════════════════════════════════════════════════════════

// 高亮引用块
const callout = (label, text, color = C.brandLight) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [9360],
  rows: [new TableRow({ children: [
    new TableCell({
      borders: {
        top: { style: BorderStyle.SINGLE, size: 4, color },
        bottom: { style: BorderStyle.SINGLE, size: 1, color: C.border },
        left: { style: BorderStyle.SINGLE, size: 12, color },
        right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }
      },
      shading: { fill: color, type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 160, right: 160 },
      children: [new Paragraph({
        spacing: { after: 0 },
        children: [TB(label + '  ', { size: 18, color }), T(text, { size: 18 })]
      })]
    })
  ] })]
});

// 分割线
const divider = () => new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: C.brand, space: 1 } },
  spacing: { before: 240, after: 240 },
  children: []
});

// ═══════════════════════════════════════════════════════════════════════════════
//  8. 文档构建器
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 创建标准 PRD 风格的 Word 文档
 * @param {Object} options
 * @param {string} options.title - 文档标题
 * @param {string} options.subtitle - 副标题
 * @param {string} options.meta - 元信息（版本、日期、作者等）
 * @param {Array} options.children - 文档内容段落/表格数组
 * @param {string} options.headerText - 页眉文字
 * @param {string} options.footerText - 页脚文字
 * @returns {Document}
 */
function createDoc({ title, subtitle, meta, children = [], headerText, footerText } = {}) {
  const docChildren = [];

  // 封面
  if (title) {
    docChildren.push(new Paragraph({ spacing: { before: 1440, after: 0 }, children: [T('')] }));
    docChildren.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 120 },
      children: [T(title, { size: 52, bold: true, color: C.brand })]
    }));
  }
  if (subtitle) {
    docChildren.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [T(subtitle, { size: 36, bold: true, color: C.accent })]
    }));
  }
  if (meta) {
    const metaLines = Array.isArray(meta) ? meta : [meta];
    metaLines.forEach(line => {
      docChildren.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [T(line, { size: 22, color: C.gray3 })]
      }));
    });
  }

  // 分隔 + 用户内容
  docChildren.push(pageBreak());
  docChildren.push(...children);

  // 结束标记
  docChildren.push(new Paragraph({
    spacing: { before: 800, after: 0 },
    alignment: AlignmentType.CENTER,
    children: [TG('— 文档结束 —')]
  }));

  return new Document({
    numbering: {
      config: [
        {
          reference: 'bullets',
          levels: [
            { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } },
            { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1120, hanging: 280 } } } },
          ]
        },
        {
          reference: 'numbers',
          levels: [
            { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 560, hanging: 280 } } } },
          ]
        },
      ]
    },
    styles: {
      default: { document: { run: { font: 'Arial', size: 22, color: C.text } } },
      paragraphStyles: [
        {
          id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 36, bold: true, font: 'Arial', color: C.brand },
          paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0,
            border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: C.brand, space: 1 } } }
        },
        {
          id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 28, bold: true, font: 'Arial', color: C.accent },
          paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 1 }
        },
        {
          id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 24, bold: true, font: 'Arial', color: C.text },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
        },
      ]
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: C.brand, space: 4 } },
            children: headerText
              ? [TB(headerText, { size: 18, color: C.brand })]
              : []
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            spacing: { after: 0 },
            border: { top: { style: BorderStyle.SINGLE, size: 2, color: C.brand, space: 4 } },
            tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            children: footerText
              ? [T(footerText, { size: 18, color: C.gray3 })]
              : []
          })]
        })
      },
      children: docChildren
    }]
  });
}

/**
 * 保存文档到文件
 * @param {Document} doc
 * @param {string} filename
 */
async function saveDoc(doc, filename = './output.docx') {
  const fs = require('fs');
  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(filename, buf);
  console.log(`✅ 文档已保存: ${filename}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
//  9. 导出
// ═══════════════════════════════════════════════════════════════════════════════
module.exports = {
  // 基础依赖（如需直接引用）
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, LevelFormat,
  TabStopType, TabStopPosition,

  // 配色
  C,

  // 边框与填充
  thinBorder, allBorders, cellPad,

  // 文本
  T, TB, TG, tagRun,

  // 段落
  P, PB, PH1, PH2, PH3, pageBreak, Pbullet, Pnum,

  // 表格单元格
  hdrCell, dataCell, dataRow, altFill, cellParas,

  // 业务表格
  reqTable, precondTable, boundaryTable, acTable, changeTable,
  problemTable, metricTable, roleTable, permMatrix,

  // UI 组件
  callout, divider,

  // 文档构建器
  createDoc, saveDoc,
};
