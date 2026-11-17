#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import PptxGenJS from "pptxgenjs";
import JSZip from "jszip";

const GENERATED_SUPPORT_DERIVATION = "same_slide_evidence_augmenter";

const [inputPath, outputDir] = process.argv.slice(2);
if (!inputPath || !outputDir) {
  console.error(JSON.stringify({ status: "failed", errors: [{ code: "INVALID_RUNTIME_ARGUMENTS", message: "Usage: build-deck.mjs <input.json> <output-dir>" }] }));
  process.exit(2);
}

const resultPath = path.join(outputDir, "runtime-result.json");
const result = { run_id: null, status: "failed", pptx: null, object_results: [], fallbacks: [], warnings: [], errors: [] };

try {
  const plan = JSON.parse(await fs.readFile(inputPath, "utf8"));
  result.run_id = plan.run_id || null;
  await fs.mkdir(outputDir, { recursive: true });
  validateNativeRequired(plan);

  const pptx = new PptxGenJS();
  const style = resolveStyle(plan.style_contract, result.warnings);
  if (style.aspectRatio === "9:16") {
    pptx.defineLayout({ name: "PPTSMITH_PORTRAIT", width: 7.5, height: 13.333 });
    pptx.layout = "PPTSMITH_PORTRAIT";
  } else if (style.aspectRatio === "4:3") {
    pptx.defineLayout({ name: "PPTSMITH_4X3", width: 10, height: 7.5 });
    pptx.layout = "PPTSMITH_4X3";
  } else {
    pptx.layout = "LAYOUT_WIDE";
  }
  pptx.author = "MeowClaw PPTSmith";
  pptx.subject = "PptxGenJS production runtime";
  pptx.title = "PPTSmith deck";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: style.titleFont,
    bodyFontFace: style.bodyFont,
    lang: "en-US",
  };

  for (const [slideIndex, slidePlan] of (plan.slides || []).entries()) {
    const slide = pptx.addSlide();
    slide.background = { color: style.colors.background };
    const objects = slidePlan.objects || [];
    const contentWidth = style.pageWidth - style.grid.left - style.grid.right;
    const isCoverSlide = slidePlan.slide_role === "cover";
    const titleText = visibleSlideTitle(slidePlan);
    const body = [slidePlan.judgment, slidePlan.message]
      .filter((value) => typeof value === "string" && value.trim())
      .join("\n");

    if (isCoverSlide) {
      renderCoverSlide(pptx, slide, slidePlan, style);
    } else {
      if (titleText) {
        addText(slide, titleText, style.grid.left, style.grid.top, contentWidth, style.grid.titleHeight, {
          objectName: `Title:${slidePlan.id || slidePlan.slide_id || `slide-${slideIndex + 1}`}`,
          fontFace: style.titleFont,
          fontSize: style.titleSize,
          bold: true,
          color: style.colors.textPrimary,
        });
      }
      if (body) {
        addText(slide, body, style.grid.left, style.grid.top + (titleText ? style.grid.titleHeight : 0.18) + style.spacing.titleToBody, contentWidth, 0.55, {
          objectName: `Body:${slidePlan.id || slidePlan.slide_id || `slide-${slideIndex + 1}`}`,
          fontSize: style.bodySize,
          color: style.colors.textSecondary,
          breakLine: false,
        });
      }
    }

    const contentRegion = resolveContentRegion({
      isCoverSlide,
      hasBody: Boolean(body && !isCoverSlide),
      hasTitle: Boolean(titleText && !isCoverSlide),
      style,
    });
    const frames = computeObjectFrames(slidePlan, objects, style, contentRegion);
    for (const [objectIndex, obj] of objects.entries()) {
      const plannedRoute = obj.delivery_plan?.selected_route || obj.delivery_preferences?.preferred_route || "native_ppt";
      const rendered = renderObject(pptx, slide, obj, frames[objectIndex], style);
      const actualRoute = rendered.route;
      result.object_results.push({
        slide_id: slidePlan.id || slidePlan.slide_id || `S${String(slideIndex + 1).padStart(2, "0")}`,
        object_id: obj.id || obj.object_id || `object-${objectIndex + 1}`,
        component_type: obj.component_type || obj.type || "unknown",
        planned_route: plannedRoute,
        actual_route: actualRoute,
        status: "created",
      });
      if (actualRoute !== plannedRoute) {
        result.fallbacks.push({
          slide_id: slidePlan.id || slidePlan.slide_id,
          object_id: obj.id || obj.object_id,
          component_type: obj.component_type || obj.type,
          planned_route: plannedRoute,
          actual_route: actualRoute,
          reason_codes: ["PPTXGENJS_EDITABLE_NATIVE_FALLBACK"],
          editable_core_preserved: true,
        });
      }
      if (rendered.semanticFallback) {
        result.fallbacks.push({
          slide_id: slidePlan.id || slidePlan.slide_id,
          object_id: obj.id || obj.object_id,
          component_type: obj.component_type || obj.type,
          planned_route: plannedRoute,
          actual_route: actualRoute,
          reason_codes: ["PPTXGENJS_SEMANTIC_CARD_FALLBACK"],
          editable_core_preserved: true,
        });
        result.warnings.push(`Object ${obj.id || obj.object_id || "unknown"} (${obj.component_type || obj.type || "unknown"}) used reason-coded semantic card fallback.`);
      }
    }
  }

  const deckPath = path.join(outputDir, "deck.pptx");
  await pptx.writeFile({ fileName: deckPath });
  await normalizeInternalRelationshipTargets(deckPath);
  result.status = "created";
  result.pptx = deckPath;
  await fs.writeFile(resultPath, `${JSON.stringify(result, null, 2)}\n`, "utf8");
  console.log(JSON.stringify(result));
} catch (error) {
  const structured = error?.structured || { code: "PPTXGENJS_RUNTIME_FAILED", message: String(error?.message || error) };
  result.errors.push(structured);
  try {
    await fs.mkdir(outputDir, { recursive: true });
    await fs.writeFile(resultPath, `${JSON.stringify(result, null, 2)}\n`, "utf8");
  } catch {}
  console.error(JSON.stringify(result));
  process.exit(1);
}

async function normalizeInternalRelationshipTargets(deckPath) {
  const zip = await JSZip.loadAsync(await fs.readFile(deckPath));
  for (const relPath of Object.keys(zip.files).filter((name) => name.endsWith(".rels"))) {
    const entry = zip.file(relPath);
    if (!entry) continue;
    let xml = await entry.async("string");
    const sourceDir = path.posix.dirname(relPath.replace("/_rels/", "/").replace(/\.rels$/, ""));
    xml = xml.replace(/Target="\/(ppt\/[^\"]+)"/g, (_match, target) => `Target="${path.posix.relative(sourceDir, target)}"`);
    zip.file(relPath, xml);
  }
  await fs.writeFile(deckPath, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

function validateNativeRequired(plan) {
  const supported = new Set([
    "text", "shape", "card", "metric_card", "comparison_card", "evidence_block",
    "summary_action_card", "table", "native_table", "chart", "bar_chart",
    "column_chart", "line_chart", "pie_chart", "diagram", "process",
    "process_flow", "relationship",
  ]);
  for (const slide of plan.slides || []) {
    for (const obj of slide.objects || []) {
      const kind = String(obj.component_type || obj.type || "").toLowerCase();
      if (obj.editability === "native_required" && !supported.has(kind)) {
        const error = new Error(`Unsupported native-required object: ${kind || "unknown"}`);
        error.structured = {
          code: "UNSUPPORTED_NATIVE_REQUIRED_OBJECT",
          message: error.message,
          slide_id: slide.id || slide.slide_id,
          object_id: obj.id || obj.object_id,
          component_type: kind || "unknown",
        };
        throw error;
      }
    }
  }
}

function renderObject(pptx, slide, obj, frame, style) {
  const kind = String(obj.component_type || obj.type || "").toLowerCase();
  const route = obj.delivery_plan?.selected_route || obj.delivery_preferences?.preferred_route || "native_ppt";
  const x = frame?.x ?? style.grid.left;
  const y = frame?.y ?? style.grid.top + style.grid.titleHeight + style.spacing.titleToBody + 0.65;
  const w = frame?.w ?? (style.pageWidth - style.grid.left - style.grid.right);
  const h = frame?.h ?? 2.4;

  if (kind === "table" || kind === "native_table" || route === "native_table") {
    const rows = tableRows(obj);
    slide.addTable(rows, {
      x,
      y,
      w,
      h: Math.max(1.9, h),
      border: { type: "solid", color: style.colors.border, pt: 1 },
      fill: style.colors.background,
      color: style.colors.textPrimary,
      fontFace: style.bodyFont,
      fontSize: style.smallBodySize,
      margin: 0.08,
      rowH: 0.4,
      autoFit: false,
    });
    return { route: "native_table" };
  }
  if (kind.includes("chart") || route === "native_chart") {
    const data = chartData(obj);
    const chartType = kind.includes("line") ? pptx.ChartType.line : kind.includes("pie") ? pptx.ChartType.pie : pptx.ChartType.bar;
    slide.addChart(chartType, data, {
      x,
      y,
      w,
      h: Math.max(2.8, h),
      showLegend: data.length > 1,
      showTitle: false,
      showValue: true,
      catAxisLabelFontSize: 10,
      valAxisLabelFontSize: 9,
      chartColors: style.colors.dataSeries,
    });
    return { route: "native_chart" };
  }
  if (["diagram", "process", "process_flow", "relationship"].includes(kind) || route === "native_diagram") {
    renderProcess(pptx, slide, obj, x, y, w, h, style);
    return { route: "native_diagram" };
  }
  renderCard(pptx, slide, obj, x, y, w, h, style);
  const knownCard = [
    "text", "shape", "card", "metric_card", "comparison_card", "evidence_block",
    "summary_action_card",
  ].includes(kind);
  return { route: "native_ppt", semanticFallback: !knownCard };
}

function renderCard(pptx, slide, obj, x, y, w, h, style) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    objectName: `Material:card:${obj.id || "object"}`,
    rectRadius: 0.08,
    fill: { color: style.colors.surface1 },
    line: { color: style.colors.border, pt: 1 },
  });
  addText(slide, objectText(obj), x + style.spacing.padding, y + style.spacing.padding, w - 2 * style.spacing.padding, Math.max(0.9, h - 2 * style.spacing.padding), {
    objectName: `Label:${obj.id || "object"}`,
    fontFace: style.bodyFont,
    fontSize: style.bodySize,
    bold: true,
    color: style.colors.textPrimary,
    valign: "mid",
  });
}

function renderProcess(pptx, slide, obj, x, y, w, h, style) {
  const nodes = processNodes(obj);
  const nodeW = Math.min(1.65, (w - 0.3 * (nodes.length - 1)) / nodes.length);
  const route = String(obj.connector_route || obj.connectorRoute || "straight");
  const nodeH = Math.max(1.15, Math.min(1.6, h));
  const nodeY = y + Math.max(0, (h - nodeH) / 2);
  if (route !== "straight") {
    throw new Error(`PPTXGENJS_CONNECTOR_ROUTE_UNSUPPORTED:${route}`);
  }
  nodes.forEach((label, i) => {
    const nodeX = x + i * (nodeW + 0.3);
    if (i > 0) slide.addShape(pptx.ShapeType.line, { x: nodeX - 0.28, y: nodeY + nodeH / 2, w: 0.23, h: 0, objectName: `Connector:${route}:process:${i}`, line: { color: style.colors.primary, pt: 1.5, beginArrowType: "none", endArrowType: "triangle" } });
    slide.addShape(pptx.ShapeType.roundRect, { x: nodeX, y: nodeY, w: nodeW, h: nodeH, objectName: `Material:process-node:${i}`, fill: { color: style.colors.surface2 }, line: { color: style.colors.primary, pt: 1.2 } });
    addText(slide, label, nodeX + 0.08, nodeY + 0.12, nodeW - 0.16, Math.max(0.7, nodeH - 0.24), { fontFace: style.bodyFont, fontSize: style.smallBodySize, bold: true, color: style.colors.textPrimary, align: "center", valign: "mid" });
  });
}

function renderCoverSlide(pptx, slide, slidePlan, style) {
  const title = visibleSlideTitle(slidePlan) || String(slidePlan.message || slidePlan.judgment || "Presentation");
  const subtitle = normalizeSubtitle(slidePlan, title);
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: style.pageWidth,
    h: style.pageHeight,
    objectName: `Decoration:cover:bg:${slidePlan.id || slidePlan.slide_id || "cover"}`,
    fill: { color: style.colors.background },
    line: { color: style.colors.background, transparency: 100 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: style.grid.left + 0.1,
    y: 1.35,
    w: 0.12,
    h: 3.95,
    objectName: `Decoration:cover:accent:${slidePlan.id || slidePlan.slide_id || "cover"}`,
    fill: { color: style.colors.primary },
    line: { color: style.colors.primary, transparency: 100 },
  });
  addText(slide, title, style.grid.left + 0.55, 1.9, style.pageWidth - style.grid.left - style.grid.right - 0.7, 1.55, {
    objectName: `Title:${slidePlan.id || slidePlan.slide_id || "cover"}`,
    fontFace: style.titleFont,
    fontSize: style.coverTitleSize,
    bold: true,
    color: style.colors.textPrimary,
    valign: "mid",
  });
  if (subtitle) {
    addText(slide, subtitle, style.grid.left + 0.55, 3.9, 9.3, 0.72, {
      objectName: `Subtitle:${slidePlan.id || slidePlan.slide_id || "cover"}`,
      fontFace: style.bodyFont,
      fontSize: Math.max(style.bodySize, 14),
      color: style.colors.textSecondary,
    });
  }
  slide.addShape(pptx.ShapeType.line, {
    x: style.grid.left + 0.55,
    y: 5.25,
    w: 3.9,
    h: 0,
    objectName: `Decoration:cover:rule:${slidePlan.id || slidePlan.slide_id || "cover"}`,
    line: { color: style.colors.border, pt: 1.2 },
  });
}

function addText(slide, text, x, y, w, h, options = {}) {
  slide.addText(String(text), { x, y, w, h, margin: 0, fontFace: "Aptos", fit: "shrink", valign: "top", ...options });
}

function resolveStyle(contract, warnings) {
  const value = contract && typeof contract === "object" ? contract : {};
  const scale = value.spacing?.scale || {};
  const rules = value.spacing?.rules || {};
  const consumedScaleTokens = new Set(["md"]);
  for (const rule of ["card_gap", "title_to_body"]) {
    if (typeof rules[rule] === "string") consumedScaleTokens.add(rules[rule]);
  }
  warnUnsupportedStylePaths(value, {
    schema_version: true,
    style_id: true,
    display_name: true,
    aspect_ratios: true,
    colors: {
      primary: true, accent: true, background: true, surface_1: true, surface_2: true,
      text_primary: true, text_secondary: true, border: true, data_series: true,
    },
    typography: {
      font_primary: true,
      font_editorial: true,
      title_sizes_pt: { cover: true, slide: true },
      body_sizes_pt: { normal: true, small: true },
    },
    grid: {
      margin_left_in: true, margin_right_in: true, margin_top_in: true,
      title_zone_height_in: true, gutter_horizontal_in: true,
    },
    spacing: {
      unit: true,
      scale: Object.fromEntries([...consumedScaleTokens].map((token) => [token, true])),
      rules: { card_gap: true, title_to_body: true },
    },
  }, "", warnings);
  const color = (key, fallback) => String(value.colors?.[key] || fallback).replace(/^#/, "").toUpperCase();
  const spacingRule = (name, fallback) => Number(scale[rules[name]]) || fallback;
  const aspectRatio = ["16:9", "4:3", "9:16"].includes(value.aspect_ratios?.[0]) ? value.aspect_ratios[0] : "16:9";
  const pageWidth = aspectRatio === "4:3" ? 10 : aspectRatio === "9:16" ? 7.5 : 13.333;
  const pageHeight = aspectRatio === "9:16" ? 13.333 : 7.5;
  return {
    aspectRatio,
    pageWidth,
    pageHeight,
    titleFont: value.typography?.font_editorial?.[0] || value.typography?.font_primary?.[0] || "Aptos Display",
    bodyFont: value.typography?.font_primary?.[0] || "Aptos",
    coverTitleSize: Number(value.typography?.title_sizes_pt?.cover) || Math.max(34, (Number(value.typography?.title_sizes_pt?.slide) || 24) * 1.45),
    titleSize: Number(value.typography?.title_sizes_pt?.slide) || 24,
    bodySize: Number(value.typography?.body_sizes_pt?.normal) || 13,
    smallBodySize: Number(value.typography?.body_sizes_pt?.small) || 11,
    colors: {
      primary: color("primary", "4F7CAC"), accent: color("accent", "D6A85F"), background: color("background", "FCFBF8"),
      surface1: color("surface_1", "F4F1EA"), surface2: color("surface_2", "E8F0F7"), textPrimary: color("text_primary", "2D3340"),
      textSecondary: color("text_secondary", "6E6A60"), border: color("border", "E4E0D7"),
      dataSeries: (value.colors?.data_series || ["#4F7CAC", "#D6A85F", "#7A9E7E"]).map((entry) => String(entry).replace(/^#/, "").toUpperCase()),
    },
    grid: {
      left: Number(value.grid?.margin_left_in) || 0.55, right: Number(value.grid?.margin_right_in) || 0.55,
      top: Number(value.grid?.margin_top_in) || 0.3, bottom: 0.45, titleHeight: Number(value.grid?.title_zone_height_in) || 0.5,
    },
    spacing: { cardGap: spacingRule("card_gap", Number(value.grid?.gutter_horizontal_in) || 0.2), titleToBody: spacingRule("title_to_body", 0.15), padding: Number(scale.md) || 0.16 },
  };
}

function resolveContentRegion({ isCoverSlide, hasBody, hasTitle, style }) {
  if (isCoverSlide) {
    return { x: style.grid.left, y: 5.65, w: style.pageWidth - style.grid.left - style.grid.right, h: Math.max(1.2, style.pageHeight - 6.05) };
  }
  const headerOffset = hasTitle ? style.grid.titleHeight : 0;
  const bodyHeight = hasBody ? 0.72 : 0;
  const y = style.grid.top + headerOffset + style.spacing.titleToBody + bodyHeight + 0.28;
  const h = Math.max(1.8, style.pageHeight - y - style.grid.bottom);
  return { x: style.grid.left, y, w: style.pageWidth - style.grid.left - style.grid.right, h };
}

function computeObjectFrames(slidePlan, objects, style, region) {
  if (!objects.length) return [];
  const sidebarFrames = computeSidebarFrames(objects, style, region);
  if (sidebarFrames) return sidebarFrames;
  if (objects.length === 1) {
    return [{ x: region.x, y: region.y, w: region.w, h: region.h }];
  }
  if (objects.length === 2) {
    const width = (region.w - style.spacing.cardGap) / 2;
    return [0, 1].map((index) => ({
      x: region.x + index * (width + style.spacing.cardGap),
      y: region.y,
      w: width,
      h: region.h,
    }));
  }
  const width = (region.w - style.spacing.cardGap * (objects.length - 1)) / objects.length;
  const height = Math.max(2.2, Math.min(region.h, region.h * 0.72));
  return objects.map((_, index) => ({
    x: region.x + index * (width + style.spacing.cardGap),
    y: region.y,
    w: width,
    h: height,
  }));
}

function computeSidebarFrames(objects, style, region) {
  const supportIndexes = objects
    .map((obj, index) => [obj, index])
    .filter(([obj]) => isSecondarySupportObject(obj))
    .map(([, index]) => index);
  const primaryIndexes = objects
    .map((obj, index) => [obj, index])
    .filter(([obj]) => !isSecondarySupportObject(obj))
    .map(([, index]) => index);
  if (supportIndexes.length !== 1 || !primaryIndexes.length || primaryIndexes.length > 2) {
    return null;
  }

  const frames = new Array(objects.length);
  const sidebarGap = Math.max(0.24, style.spacing.cardGap);
  const mainWidth = Math.max(6.6, Math.min(region.w * 0.7, region.w - 3.0 - sidebarGap));
  const sidebarWidth = region.w - mainWidth - sidebarGap;
  if (sidebarWidth < 2.8) {
    return null;
  }

  frames[supportIndexes[0]] = {
    x: region.x + mainWidth + sidebarGap,
    y: region.y,
    w: sidebarWidth,
    h: region.h,
  };

  if (primaryIndexes.length === 1) {
    frames[primaryIndexes[0]] = { x: region.x, y: region.y, w: mainWidth, h: region.h };
    return frames;
  }

  const [firstPrimary, secondPrimary] = primaryIndexes;
  const stackGap = 0.24;
  const topBias = isChartLike(objects[firstPrimary]) ? 0.58 : 0.52;
  const topHeight = Math.max(1.9, region.h * topBias - stackGap / 2);
  const bottomHeight = Math.max(1.35, region.h - topHeight - stackGap);
  frames[firstPrimary] = { x: region.x, y: region.y, w: mainWidth, h: topHeight };
  frames[secondPrimary] = { x: region.x, y: region.y + topHeight + stackGap, w: mainWidth, h: bottomHeight };
  return frames;
}

function isSecondarySupportObject(obj) {
  if (obj?.priority === "primary") return false;
  return obj?.provenance?.derivation === GENERATED_SUPPORT_DERIVATION || String(obj?.semantic_role || "").toLowerCase() === "interpretation";
}

function isChartLike(obj) {
  const component = String(obj?.component_type || obj?.type || "").toLowerCase();
  const route = String(obj?.delivery_plan?.selected_route || obj?.delivery_preferences?.preferred_route || "").toLowerCase();
  return component.includes("chart") || route === "native_chart";
}

function visibleSlideTitle(slidePlan) {
  const title = typeof slidePlan?.title === "string" ? slidePlan.title.trim() : "";
  if (!title) return "";
  return isInternalSlideLabel(title, slidePlan) ? "" : title;
}

function isInternalSlideLabel(title, slidePlan) {
  const normalized = String(title || "").trim();
  if (!normalized) return false;
  const lowered = normalized.toLowerCase();
  const slideId = String(slidePlan?.id || slidePlan?.slide_id || "").trim().toLowerCase();
  return lowered === slideId || /^slide[-_ ]?\d{1,3}$/i.test(normalized) || /^s\d{1,3}$/i.test(normalized);
}

function normalizeSubtitle(slidePlan, title) {
  const subtitle = String(slidePlan?.message || slidePlan?.judgment || "").trim();
  return subtitle && subtitle !== title ? subtitle : "";
}

function warnUnsupportedStylePaths(object, supportTree, prefix, warnings) {
  if (!object || typeof object !== "object" || Array.isArray(object)) return;
  for (const key of Object.keys(object)) {
    const pathName = prefix ? `${prefix}.${key}` : key;
    const support = supportTree?.[key];
    if (!support) {
      warnings.push(`Unsupported style field ignored by PptxGenJS runtime: ${pathName}`);
    } else if (support !== true) {
      warnUnsupportedStylePaths(object[key], support, pathName, warnings);
    }
  }
}

function objectText(obj) {
  const content = obj.content;
  if (typeof content === "string" && content.trim()) return content.trim();
  if (content && typeof content === "object") {
    const title = content.title || content.label || content.claim || content.text;
    const value = content.value;
    if (title && value !== undefined) return `${title}\n${value}`;
    if (title) return String(title);
  }
  return String(obj.component_type || obj.semantic_role || obj.type || "PPT object").replaceAll("_", " ");
}

function tableRows(obj) {
  const content = obj.content || {};
  if (Array.isArray(content.rows) && content.rows.length) return content.rows.map((row) => row.map(String));
  if (Array.isArray(content.headers) && Array.isArray(content.body)) return [content.headers.map(String), ...content.body.map((row) => row.map(String))];
  return [["Item", "Status"], [objectText(obj), "Editable"]];
}

function chartData(obj) {
  const content = obj.content || {};
  const categories = Array.isArray(content.categories) ? content.categories.map(String) : ["A", "B", "C"];
  if (Array.isArray(content.series) && content.series.length) return content.series.map((series, i) => ({ name: String(series.name || `Series ${i + 1}`), labels: categories, values: (series.values || []).map(Number) }));
  return [{ name: "Value", labels: categories, values: categories.map((_, i) => i + 1) }];
}

function processNodes(obj) {
  const nodes = obj.content?.nodes;
  if (Array.isArray(nodes) && nodes.length) return nodes.slice(0, 5).map((node, i) => String(typeof node === "string" ? node : node.label || node.title || node.id || `Step ${i + 1}`));
  return ["Start", "Build", "Finish"];
}
