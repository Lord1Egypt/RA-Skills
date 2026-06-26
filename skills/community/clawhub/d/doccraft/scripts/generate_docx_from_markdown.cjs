#!/usr/bin/env node

const fs = require("node:fs");
const { createRequire } = require("node:module");
const path = require("node:path");

function requireDocx() {
  const localRequire = createRequire(path.resolve(process.cwd(), "sgdb-docx-loader.cjs"));
  const candidates = [];
  if (process.env.SGDB_DOCX_MODULE) {
    candidates.push(process.env.SGDB_DOCX_MODULE);
  }
  candidates.push("docx");
  for (const candidate of candidates) {
    try {
      return localRequire(candidate);
    } catch (error) {
      // Try next candidate.
    }
    try {
      return require(candidate);
    } catch (error) {
      // Try next candidate.
    }
  }
  throw new Error(
    "Cannot load the 'docx' module. Install it in the current workspace or set SGDB_DOCX_MODULE to a resolvable module path.",
  );
}

const {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  LineRuleType,
  PageBreak,
  PageNumber,
  Packer,
  Paragraph,
  Table,
  TableCell,
  TableOfContents,
  TableRow,
  TextRun,
  WidthType,
} = requireDocx();

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    args[key.slice(2)] = value;
    i += 1;
  }
  const required = ["markdown", "delivery-brief", "format-profile", "out"];
  for (const key of required) {
    if (!args[key]) {
      throw new Error(`Missing required argument --${key}`);
    }
  }
  args.stage = args.stage || "final";
  return args;
}

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function readOptional(filePath) {
  if (!filePath) return "";
  return fs.readFileSync(filePath, "utf8");
}

function cmToTwip(cm) {
  return Math.round((Number(cm) / 2.54) * 1440);
}

function ptToHalfPoint(pt) {
  return Math.round(Number(pt) * 2);
}

function lineSpecToTwip(spec, fallbackPt) {
  if (!spec) return fallbackPt * 20;
  const match = String(spec).match(/(\d+(?:\.\d+)?)/);
  return match ? Math.round(Number(match[1]) * 20) : fallbackPt * 20;
}

function firstLineIndent(chars) {
  return Number(chars || 0) * 320;
}

function splitFontSpec(spec, fallbackFont, fallbackSizePt) {
  if (!spec) {
    return { font: fallbackFont, sizePt: fallbackSizePt };
  }
  const match = String(spec).match(/^(.+?)\s+(\d+(?:\.\d+)?)\s*pt/i);
  if (!match) {
    return { font: fallbackFont, sizePt: fallbackSizePt };
  }
  return { font: match[1].trim(), sizePt: Number(match[2]) };
}

function missingFields(payload, fields) {
  const missing = [];
  for (const field of fields) {
    const value = payload[field];
    if (value === undefined || value === null) {
      missing.push(field);
      continue;
    }
    if (typeof value === "string" && value.trim() === "") {
      missing.push(field);
    }
  }
  return missing;
}

function deriveComponents(scope, stage) {
  const normalized = String(scope || "").toLowerCase();
  const components = ["body"];
  if (stage === "draft" && normalized.includes("body-only draft")) {
    return components;
  }
  if (normalized.includes("full-deliverable") || stage === "final") {
    for (const item of ["cover", "table-of-contents"]) {
      if (!components.includes(item)) {
        components.push(item);
      }
    }
  }
  const keywordMap = {
    append: "appendices",
    glossary: "glossary",
    "figure list": "figure-list",
    "table list": "table-list",
    attachment: "attachments-manifest",
  };
  for (const [needle, component] of Object.entries(keywordMap)) {
    if (normalized.includes(needle) && !components.includes(component)) {
      components.push(component);
    }
  }
  return components;
}

function resolveReadiness(brief, profile, stage) {
  const draftMissing = missingFields(brief, [
    "document_title",
    "source_authority",
    "target_structure",
    "document_purpose",
    "audience",
    "output_mode",
  ]);
  const blockers = draftMissing.map((field) => `missing draft field: ${field}`);
  if (stage === "final") {
    const finalMissing = missingFields(brief, [
      "delivery_stage",
      "completeness_scope",
      "review_mode",
      "format_authority",
      "file_naming_and_version",
    ]);
    blockers.push(...finalMissing.map((field) => `missing final field: ${field}`));
    if (String(brief.delivery_stage || "").toLowerCase() !== "final") {
      blockers.push("delivery_stage is not set to final");
    }
    if (profile.needs_confirmation === true) {
      blockers.push("format profile still requires confirmation");
    }
  }
  return {
    blockers,
    components: deriveComponents(brief.completeness_scope || "body-only draft", stage),
  };
}

function makeFooterRuns(style) {
  if (String(style || "").includes("第")) {
    return [new TextRun("第 "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" 页")];
  }
  return [new TextRun("- "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" -")];
}

function buildStyles(profile) {
  const body = profile.fonts.body;
  const h1 = profile.fonts.heading_1;
  const h2 = profile.fonts.heading_2;
  const h3 = profile.fonts.heading_3;
  const h4 = profile.fonts.heading_4;
  const tableCaption = splitFontSpec(profile.tables.caption_font, "SimHei", 12);
  const tableHeader = splitFontSpec(profile.tables.header_font, "SimHei", 12);
  const tableBody = splitFontSpec(profile.tables.body_font, "SimSun", 12);
  const figureCaption = splitFontSpec(profile.figures.caption_font, body.font, 12);
  return {
    default: {
      document: {
        run: {
          font: body.font,
          size: ptToHalfPoint(body.size_pt),
          color: "000000",
        },
      },
    },
    paragraphStyles: [
      {
        id: "SGDB_Body",
        name: "SGDB Body",
        run: { font: body.font, size: ptToHalfPoint(body.size_pt), color: "000000" },
        paragraph: {
          spacing: {
            line: lineSpecToTwip(profile.paragraph.line_spacing, 28),
            lineRule: LineRuleType.EXACT,
            before: Number(profile.paragraph.space_before_pt || 0) * 20,
            after: Number(profile.paragraph.space_after_pt || 0) * 20,
          },
          indent: { firstLine: firstLineIndent(profile.paragraph.first_line_indent_chars || 2) },
          alignment: AlignmentType.JUSTIFIED,
        },
      },
      {
        id: "SGDB_H1",
        name: "SGDB Heading 1",
        basedOn: "SGDB_Body",
        run: { font: h1.font, size: ptToHalfPoint(h1.size_pt), bold: !!h1.bold, color: "000000" },
        paragraph: {
          spacing: { line: lineSpecToTwip(profile.paragraph.line_spacing, 28), lineRule: LineRuleType.EXACT, before: 240, after: 120 },
          indent: { firstLine: 0 },
          outlineLevel: 0,
        },
      },
      {
        id: "SGDB_H2",
        name: "SGDB Heading 2",
        basedOn: "SGDB_Body",
        run: { font: h2.font, size: ptToHalfPoint(h2.size_pt), bold: !!h2.bold, color: "000000" },
        paragraph: {
          spacing: { line: lineSpecToTwip(profile.paragraph.line_spacing, 28), lineRule: LineRuleType.EXACT, before: 200, after: 100 },
          indent: { firstLine: 0 },
          outlineLevel: 1,
        },
      },
      {
        id: "SGDB_H3",
        name: "SGDB Heading 3",
        basedOn: "SGDB_Body",
        run: { font: h3.font, size: ptToHalfPoint(h3.size_pt), bold: !!h3.bold, color: "000000" },
        paragraph: {
          spacing: { line: lineSpecToTwip(profile.paragraph.line_spacing, 28), lineRule: LineRuleType.EXACT, before: 160, after: 80 },
          indent: { firstLine: 0 },
          outlineLevel: 2,
        },
      },
      {
        id: "SGDB_H4",
        name: "SGDB Heading 4",
        basedOn: "SGDB_Body",
        run: { font: h4.font, size: ptToHalfPoint(h4.size_pt), bold: !!h4.bold, color: "000000" },
        paragraph: {
          spacing: {
            line: lineSpecToTwip(h4.line_spacing, 30),
            lineRule: LineRuleType.EXACT,
            before: Number(h4.space_before_pt || 6) * 20,
            after: Number(h4.space_after_pt || 3) * 20,
          },
          indent: { firstLine: 0 },
          outlineLevel: 3,
        },
      },
      {
        id: "SGDB_TableCaption",
        name: "SGDB Table Caption",
        basedOn: "SGDB_Body",
        run: { font: tableCaption.font, size: ptToHalfPoint(tableCaption.sizePt), bold: true, color: "000000" },
        paragraph: { spacing: { line: 360, lineRule: LineRuleType.EXACT, before: 120, after: 80 }, alignment: AlignmentType.CENTER },
      },
      {
        id: "SGDB_TableHeader",
        name: "SGDB Table Header",
        basedOn: "SGDB_Body",
        run: { font: tableHeader.font, size: ptToHalfPoint(tableHeader.sizePt), bold: true, color: "000000" },
        paragraph: { spacing: { line: 360, lineRule: LineRuleType.EXACT, before: 0, after: 0 }, alignment: AlignmentType.CENTER },
      },
      {
        id: "SGDB_TableText",
        name: "SGDB Table Text",
        basedOn: "SGDB_Body",
        run: { font: tableBody.font, size: ptToHalfPoint(tableBody.sizePt), color: "000000" },
        paragraph: { spacing: { line: 360, lineRule: LineRuleType.EXACT, before: 0, after: 0 }, alignment: AlignmentType.LEFT },
      },
      {
        id: "SGDB_FigureCaption",
        name: "SGDB Figure Caption",
        basedOn: "SGDB_Body",
        run: { font: figureCaption.font, size: ptToHalfPoint(figureCaption.sizePt), color: "000000" },
        paragraph: { spacing: { line: 360, lineRule: LineRuleType.EXACT, before: 80, after: 80 }, alignment: AlignmentType.CENTER },
      },
      {
        id: "SGDB_CoverTitle",
        name: "SGDB Cover Title",
        basedOn: "SGDB_Body",
        run: { font: h1.font, size: Math.max(ptToHalfPoint(h1.size_pt + 6), 44), bold: true, color: "000000" },
        paragraph: { spacing: { before: 800, after: 240 }, alignment: AlignmentType.CENTER },
      },
      {
        id: "SGDB_CoverMeta",
        name: "SGDB Cover Meta",
        basedOn: "SGDB_Body",
        run: { font: body.font, size: ptToHalfPoint(body.size_pt), color: "000000" },
        paragraph: { spacing: { before: 80, after: 80 }, alignment: AlignmentType.CENTER },
      },
    ],
  };
}

function paragraph(style, text, extra = {}) {
  return new Paragraph({
    style,
    ...extra,
    children: [new TextRun(text)],
  });
}

function pageBreakParagraph() {
  return new Paragraph({ children: [new PageBreak()] });
}

function makeTableCell(text, widthPct, style) {
  return new TableCell({
    width: { size: widthPct, type: WidthType.PERCENTAGE },
    children: [new Paragraph({ style, children: [new TextRun(text)] })],
  });
}

function makeMarkdownTable(rows) {
  const headers = rows[0];
  const bodyRows = rows.slice(1);
  const cellWidth = Math.floor(100 / headers.length);
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "000000" },
      left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    },
    rows: [
      new TableRow({
        children: headers.map((cell) => makeTableCell(cell, cellWidth, "SGDB_TableHeader")),
      }),
      ...bodyRows.map(
        (row) =>
          new TableRow({
            children: row.map((cell) => makeTableCell(cell, cellWidth, "SGDB_TableText")),
          }),
      ),
    ],
  });
}

function normalizeTableLine(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function flushParagraph(elements, buffer) {
  const text = buffer.join(" ").trim();
  if (!text) return;
  if (/^表[\d一二三四五六七八九十\-]/.test(text)) {
    elements.push(paragraph("SGDB_TableCaption", text));
  } else if (/^图[\d一二三四五六七八九十\-]/.test(text)) {
    elements.push(paragraph("SGDB_FigureCaption", text));
  } else {
    elements.push(paragraph("SGDB_Body", text));
  }
  buffer.length = 0;
}

function markdownToElements(markdown) {
  const elements = [];
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const paragraphBuffer = [];
  const tableBuffer = [];

  function flushTable() {
    if (!tableBuffer.length) return;
    const rows = tableBuffer
      .map(normalizeTableLine)
      .filter((row) => row.length > 0 && !row.every((cell) => /^:?-{2,}:?$/.test(cell)));
    if (rows.length >= 2) {
      elements.push(makeMarkdownTable(rows));
    }
    tableBuffer.length = 0;
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    const trimmed = line.trim();
    if (!trimmed) {
      flushParagraph(elements, paragraphBuffer);
      flushTable();
      continue;
    }
    if (/^\|.+\|$/.test(trimmed)) {
      flushParagraph(elements, paragraphBuffer);
      tableBuffer.push(trimmed);
      continue;
    }
    flushTable();
    const heading = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      flushParagraph(elements, paragraphBuffer);
      const level = heading[1].length;
      elements.push(paragraph(`SGDB_H${level}`, heading[2]));
      continue;
    }
    const bullet = trimmed.match(/^[-*]\s+(.+)$/);
    if (bullet) {
      flushParagraph(elements, paragraphBuffer);
      elements.push(
        new Paragraph({
          style: "SGDB_Body",
          bullet: { level: 0 },
          children: [new TextRun(bullet[1])],
        }),
      );
      continue;
    }
    const ordered = trimmed.match(/^\d+[.)]\s+(.+)$/);
    if (ordered) {
      flushParagraph(elements, paragraphBuffer);
      elements.push(paragraph("SGDB_Body", ordered[1]));
      continue;
    }
    const image = trimmed.match(/^!\[(.*?)\]\((.+?)\)$/);
    if (image) {
      flushParagraph(elements, paragraphBuffer);
      elements.push(paragraph("SGDB_FigureCaption", image[1] || image[2]));
      continue;
    }
    paragraphBuffer.push(trimmed);
  }
  flushParagraph(elements, paragraphBuffer);
  flushTable();
  return elements;
}

function buildCover(brief) {
  return [
    paragraph("SGDB_CoverTitle", brief.document_title),
    paragraph("SGDB_CoverMeta", brief.document_purpose || ""),
    paragraph("SGDB_CoverMeta", `适用对象：${brief.audience}`),
    pageBreakParagraph(),
  ];
}

function buildToc() {
  return [
    new TableOfContents("目录", { headingStyleRange: "1-4", hyperlink: true }),
    pageBreakParagraph(),
  ];
}

function buildOptionalSection(title, markdown, styleId) {
  const elements = [paragraph(styleId, title)];
  elements.push(...markdownToElements(markdown));
  return elements;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const brief = loadJson(args["delivery-brief"]);
  const profile = loadJson(args["format-profile"]);
  const { blockers, components } = resolveReadiness(brief, profile, args.stage);
  if (blockers.length) {
    throw new Error(`Word job is not ready:\n- ${blockers.join("\n- ")}`);
  }

  const markdown = fs.readFileSync(args.markdown, "utf8");
  const appendixMarkdown = readOptional(args["appendices-markdown"]);
  const glossaryMarkdown = readOptional(args["glossary-markdown"]);
  const attachmentsMarkdown = readOptional(args["attachments-markdown"]);

  if (args.stage === "final") {
    if (components.includes("appendices") && !appendixMarkdown) {
      throw new Error("Appendices are required by completeness_scope but --appendices-markdown was not provided.");
    }
    if (components.includes("glossary") && !glossaryMarkdown) {
      throw new Error("Glossary is required by completeness_scope but --glossary-markdown was not provided.");
    }
    if (components.includes("attachments-manifest") && !attachmentsMarkdown) {
      throw new Error("Attachments manifest is required by completeness_scope but --attachments-markdown was not provided.");
    }
    if (components.includes("figure-list") || components.includes("table-list")) {
      throw new Error("figure-list/table-list output is not implemented yet. Remove them from completeness_scope or extend the generator.");
    }
  }

  const children = [];
  if (components.includes("cover")) {
    children.push(...buildCover(brief));
  }
  if (components.includes("table-of-contents")) {
    children.push(...buildToc());
  }
  children.push(...markdownToElements(markdown));

  if (components.includes("glossary")) {
    children.push(pageBreakParagraph(), ...buildOptionalSection("术语表", glossaryMarkdown || "待补充。", "SGDB_H1"));
  }
  if (components.includes("appendices")) {
    children.push(pageBreakParagraph(), ...buildOptionalSection("附录", appendixMarkdown || "待补充。", "SGDB_H1"));
  }
  if (components.includes("attachments-manifest")) {
    children.push(
      pageBreakParagraph(),
      ...buildOptionalSection("附件清单", attachmentsMarkdown || "待补充。", "SGDB_H1"),
    );
  }

  const footerRuns = makeFooterRuns(profile.footer.page_number_style);
  const doc = new Document({
    styles: buildStyles(profile),
    sections: [
      {
        properties: {
          page: {
            margin: {
              top: cmToTwip(profile.margins_cm.top),
              bottom: cmToTwip(profile.margins_cm.bottom),
              left: cmToTwip(profile.margins_cm.left),
              right: cmToTwip(profile.margins_cm.right),
            },
            pageNumbers: { start: 1, formatType: "decimal" },
          },
        },
        footers: {
          default:
            profile.header === "none"
              ? new Footer({
                  children: [
                    new Paragraph({
                      alignment: AlignmentType.CENTER,
                      children: footerRuns,
                    }),
                  ],
                })
              : undefined,
        },
        children,
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(args.out, buffer);
  console.log(args.out);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
