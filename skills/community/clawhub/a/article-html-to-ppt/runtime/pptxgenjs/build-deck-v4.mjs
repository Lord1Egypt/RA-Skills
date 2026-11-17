#!/usr/bin/env node
// Consume a v4 render-plan.json and render deck.pptx via PptxGenJS.
//
// render_plan is builder-agnostic: EMU coordinates + abstract element types
// (textbox / shape / table / connector / image). This builder is the primary
// renderer (matches v3 visual quality); python-pptx remains the fallback.
//
// Usage: node build-deck-v4.mjs <render-plan.json> <output-dir>

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import PptxGenJS from "pptxgenjs";

const EMU_PER_IN = 914400;
const EMU_PER_PT = 12700;

const [planPath, outputDir] = process.argv.slice(2);
if (!planPath || !outputDir) {
  console.error(JSON.stringify({ ok: false, errors: [{ code: "INVALID_RUNTIME_ARGUMENTS", message: "Usage: build-deck-v4.mjs <render-plan.json> <output-dir>" }] }));
  process.exit(2);
}

const result = { ok: false, pptx: null, warnings: [], errors: [] };

const in2 = (emu) => emu / EMU_PER_IN;
const pt2 = (cpt) => cpt / 100;
const hex = (color) => (color || "000000").replace(/^#/, "");

const SHAPE_MAP = {
  rect: "rect",
  round_rect: "roundRect",
  pill: "roundRect",
  oval: "ellipse",
  diamond: "diamond",
  chevron: "chevron",
};
const ALIGN = { left: "left", center: "center", right: "right" };
const VALIGN = { top: "top", middle: "middle", bottom: "bottom" };

// Flatten v4 paragraphs (runs) into a PptxGenJS rich-text array.
function paragraphsToText(paragraphs) {
  const parts = [];
  for (const para of paragraphs || []) {
    const runs = para.runs || [];
    runs.forEach((run, idx) => {
      const last = idx === runs.length - 1;
      parts.push({
        text: run.text ?? "",
        options: {
          fontFace: run.font,
          fontSize: pt2(run.size_cpt || 1300),
          color: hex(run.color),
          bold: (run.weight || 400) >= 600,
          italic: Boolean(run.italic),
          breakLine: last && para !== (paragraphs[paragraphs.length - 1] || para),
          bullet: para.bullet && para.bullet !== "none" ? { code: "2022", indent: 10 } : undefined,
        },
      });
    });
  }
  return parts;
}

function textOptions(element) {
  const f = element.frame || {};
  return {
    x: in2(f.x || 0),
    y: in2(f.y || 0),
    w: in2(f.w || 0),
    h: in2(f.h || 0),
    align: ALIGN[element.paragraphs?.[0]?.align] || "left",
    valign: VALIGN[element.valign] || "top",
    margin: 0,
  };
}

function renderElement(slide, element, pptx, registry) {
  const type = element.type;
  const f = element.frame || {};

  if (type === "textbox") {
    slide.addText(paragraphsToText(element.paragraphs), textOptions(element));
    registry[element.element_id] = { x: in2(f.x || 0), y: in2(f.y || 0), w: in2(f.w || 0), h: in2(f.h || 0) };
    return { route: "native_text" };
  }

  if (type === "shape") {
    const shapeType = SHAPE_MAP[element.shape] || "rect";
    const opts = {
      x: in2(f.x || 0),
      y: in2(f.y || 0),
      w: in2(f.w || 0),
      h: in2(f.h || 0),
      fill: element.fill ? { color: hex(element.fill.color) } : { type: "none" },
    };
    if (element.shape === "round_rect" || element.shape === "pill") {
      const r = (element.corner_radius_emu || 0) / Math.max(f.w || 1, 1);
      opts.rectRadius = Math.min(r, 0.5) * 100; // PptxGenJS rectRadius is 0..100
    }
    if (element.stroke) {
      opts.line = { color: hex(element.stroke.color), width: (element.stroke.width_emu || EMU_PER_PT) / EMU_PER_PT };
    } else {
      opts.line = { type: "none" };
    }
    if (element.shadow) {
      opts.shadow = {
        type: "outer",
        color: "000000",
        blur: (element.shadow.blur_emu || 0) / EMU_PER_PT,
        offset: {
          x: (element.shadow.offset_x_emu || 0) / EMU_PER_PT,
          y: (element.shadow.offset_y_emu || 0) / EMU_PER_PT,
        },
        opacity: (element.shadow.opacity_pct ?? 12) / 100,
      };
    }
    slide.addShape(pptx.ShapeType[shapeType], opts);
    if (element.paragraphs && element.paragraphs.length) {
      slide.addText(paragraphsToText(element.paragraphs), {
        ...textOptions(element),
        valign: "middle",
        align: "center",
        isTextBox: false,
      });
    }
    registry[element.element_id] = { x: in2(f.x || 0), y: in2(f.y || 0), w: in2(f.w || 0), h: in2(f.h || 0) };
    return { route: "native_shape" };
  }

  if (type === "table") {
    const rows = element.rows || [];
    const tableRows = rows.map((row) =>
      (row.cells || []).map((cell) => ({
        text: paragraphsToText(cell.paragraphs),
        options: {
          fill: cell.fill ? { color: hex(cell.fill.color) } : undefined,
          valign: "middle",
          fontFace: cell.paragraphs?.[0]?.runs?.[0]?.font,
        },
      }))
    );
    const colW = (element.col_widths_emu || []).map((w) => in2(w));
    const isMinimal = element.variant === "minimal";
    const border = isMinimal
      ? { type: "solid", color: hex(element.border?.color || "E4E0D7"), pt: 0.25 }
      : { type: "solid", color: hex(element.border?.color || "E4E0D7"), pt: 0.5 };
    slide.addTable(tableRows, {
      x: in2(f.x || 0),
      y: in2(f.y || 0),
      w: in2(f.w || 0),
      colW,
      border,
    });
    registry[element.element_id] = { x: in2(f.x || 0), y: in2(f.y || 0), w: in2(f.w || 0), h: in2(f.h || 0) };
    return { route: "native_table" };
  }

  if (type === "image") {
    slide.addImage({
      path: element.path,
      x: in2(f.x || 0),
      y: in2(f.y || 0),
      w: in2(f.w || 0),
      h: in2(f.h || 0),
    });
    registry[element.element_id] = { x: in2(f.x || 0), y: in2(f.y || 0), w: in2(f.w || 0), h: in2(f.h || 0) };
    return { route: "native_image" };
  }

  if (type === "chart") {
    const CHART_TYPES = {
      column: "bar", bar: "bar", line: "line", area: "area",
      pie: "pie", donut: "doughnut", scatter: "scatter",
    };
    const chartType = CHART_TYPES[element.chart_type] || "bar";
    const series = element.series || [];
    const data = series.map((s) => ({
      name: s.name,
      labels: element.categories || [],
      values: s.values,
    }));
    const isPie = chartType === "pie" || chartType === "doughnut";
    const opts = {
      x: in2(f.x || 0),
      y: in2(f.y || 0),
      w: in2(f.w || 0),
      h: in2(f.h || 0),
      barDir: element.chart_type === "bar" ? "bar" : "col",
      chartColors: series.map((s) => hex(s.color)),
      showLegend: element.legend !== "none",
      legendPos: element.legend === "right" ? "r" : "b",
      showValue: true,
      showPercent: isPie,
      dataLabelColor: isPie ? "FFFFFF" : hex(element.label_color || "000000"),
      dataLabelFontSize: isPie ? 12 : pt2(element.label_size_cpt || 900),
      dataLabelFontBold: isPie,
      firstSliceAng: 270,
    };
    slide.addChart(pptx.ChartType[chartType], data, opts);
    registry[element.element_id] = { x: in2(f.x || 0), y: in2(f.y || 0), w: in2(f.w || 0), h: in2(f.h || 0) };
    return { route: "native_chart" };
  }

  if (type === "connector") {
    // Straight connector between two registered shapes (v4 MVP).
    const from = registry[element.from_element];
    const to = registry[element.to_element];
    if (!from || !to) {
      throw new Error(`connector endpoints missing: ${element.element_id}`);
    }
    const anchorPoint = (box, side) => {
      const ax = side === "left" ? 0 : side === "right" ? box.w : box.w / 2;
      const ay = side === "top" ? 0 : side === "bottom" ? box.h : box.h / 2;
      return { x: box.x + ax, y: box.y + ay };
    };
    const p1 = anchorPoint(from, element.from_side === "auto" ? "right" : (element.from_side || "right"));
    const p2 = anchorPoint(to, element.to_side === "auto" ? "left" : (element.to_side || "left"));
    const x = Math.min(p1.x, p2.x);
    const y = Math.min(p1.y, p2.y);
    const w = Math.abs(p2.x - p1.x);
    const h = Math.abs(p2.y - p1.y);
    const ah = element.arrowhead || "none";
    const line = { color: hex(element.stroke?.color || "000000"), width: (element.stroke?.width_emu || EMU_PER_PT) / EMU_PER_PT };
    if (ah === "end" || ah === "both") line.endArrowType = "triangle";
    if (ah === "both") line.startArrowType = "triangle";
    const lineOpts = {
      x, y, w, h,
      line,
      flipH: p2.x < p1.x,
      flipV: p2.y < p1.y,
    };
    slide.addShape(pptx.ShapeType.line, lineOpts);
    if (element.label) {
      const lf = element.label.frame || {};
      slide.addText(paragraphsToText(element.label.paragraphs), {
        x: in2(lf.x || 0), y: in2(lf.y || 0), w: in2(lf.w || 0), h: in2(lf.h || 0),
        align: "center", valign: "middle", margin: 0,
      });
    }
    return { route: "native_connector" };
  }

  throw new Error(`unsupported element type: ${type}`);
}

try {
  const plan = JSON.parse(await fs.readFile(planPath, "utf8"));
  await fs.mkdir(outputDir, { recursive: true });

  const pptx = new PptxGenJS();
  const widthIn = in2(plan.canvas?.width_emu || 12192000);
  const heightIn = in2(plan.canvas?.height_emu || 6858000);
  pptx.defineLayout({ name: "PPTSMITH_V4", width: widthIn, height: heightIn });
  pptx.layout = "PPTSMITH_V4";
  pptx.author = "MeowClaw PPTSmith";
  pptx.title = plan.plan?.style_pack?.pack_id || "PPTSmith deck";
  pptx.subject = "PptxGenJS v4 render";

  const primaryFont = plan.fonts_used?.[0] || "Aptos";
  pptx.theme = { headFontFace: primaryFont, bodyFontFace: primaryFont, lang: "en-US" };

  for (const slideSpec of plan.slides || []) {
    const slide = pptx.addSlide();
    if (typeof slideSpec.notes === "string" && slideSpec.notes.trim()) {
      slide.addNotes(slideSpec.notes.trim());
    }
    slide.background = slideSpec.background
      ? { color: hex(slideSpec.background.color) }
      : { color: "FFFFFF" };

    const registry = {};
    const connectors = [];
    for (const element of slideSpec.elements || []) {
      if (element.type === "connector") {
        connectors.push(element); // render after endpoints exist
      } else {
        renderElement(slide, element, pptx, registry);
      }
    }
    for (const connector of connectors) {
      renderElement(slide, connector, pptx, registry);
    }
  }

  const outFile = path.join(outputDir, "deck.pptx");
  await pptx.writeFile({ fileName: outFile });
  result.ok = true;
  result.pptx = outFile;
} catch (err) {
  result.errors.push({ code: "RUNTIME_ERROR", message: String(err?.stack || err) });
}

await fs.writeFile(path.join(outputDir, "pptxgenjs-result.json"), JSON.stringify(result, null, 2));
if (!result.ok) {
  console.error(JSON.stringify(result));
  process.exit(1);
}
console.log(JSON.stringify(result));
