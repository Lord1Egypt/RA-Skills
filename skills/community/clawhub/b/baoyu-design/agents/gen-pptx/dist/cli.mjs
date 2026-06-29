#!/usr/bin/env node

// src/cli.ts
import { existsSync, readFileSync as readFileSync2 } from "node:fs";
import { resolve as resolve2 } from "node:path";

// src/core/units.ts
var DPI = 96;
var PX_TO_PT = 0.75;
var pxToInches = (px) => px / DPI;
var pxToPoints = (px) => px * PX_TO_PT;
function clamp(value, lo, hi) {
  return Number.isFinite(value) ? Math.max(lo, Math.min(hi, value)) : lo;
}

// src/core/sanitize.ts
function sanitizeStrings(value) {
  return Array.isArray(value) ? value.filter((v) => typeof v === "string") : [];
}
function sanitizeFontSwaps(value) {
  return Array.isArray(value) ? value.filter(
    (v) => !!v && typeof v.from === "string" && typeof v.to === "string"
  ) : [];
}

// src/render/build-editable.ts
import PptxGenJS from "pptxgenjs";

// src/core/color.ts
function parseColor(input) {
  if (!input) return null;
  const r = input.trim().toLowerCase();
  if (r === "transparent" || r === "none") return null;
  if (r[0] === "#") {
    let body = r.slice(1);
    if (body.length === 3 || body.length === 4) {
      body = body.split("").map((c) => c + c).join("");
    }
    let alpha = 1;
    if (body.length === 8) {
      alpha = parseInt(body.slice(6, 8), 16) / 255;
      body = body.slice(0, 6);
    }
    if (alpha === 0 || body.length !== 6 || /[^0-9a-f]/.test(body)) return null;
    return { hex: body.toUpperCase(), alpha };
  }
  const m = r.match(
    /rgba?\(\s*(-?[\d.]+)[\s,]+(-?[\d.]+)[\s,]+(-?[\d.]+)(?:[\s,/]+([\d.]+%?))?\s*\)/
  );
  if (m) {
    const red = clamp(Math.round(parseFloat(m[1])), 0, 255);
    const green = clamp(Math.round(parseFloat(m[2])), 0, 255);
    const blue = clamp(Math.round(parseFloat(m[3])), 0, 255);
    let alpha = 1;
    if (m[4] !== void 0) {
      alpha = m[4].endsWith("%") ? parseFloat(m[4]) / 100 : parseFloat(m[4]);
      alpha = clamp(alpha, 0, 1);
    }
    if (alpha === 0) return null;
    return {
      hex: (red << 16 | green << 8 | blue).toString(16).padStart(6, "0").toUpperCase(),
      alpha
    };
  }
  return null;
}
function parseGradient(input) {
  if (!input || !input.includes("gradient(")) return null;
  const m = input.match(/(rgba?\([^)]+\)|#[0-9a-fA-F]{3,8})/);
  return m ? parseColor(m[0]) : null;
}
function opacityToTransparency(alpha) {
  return clamp(Math.round((1 - alpha) * 100), 0, 100);
}

// src/core/css.ts
function extractPx(value) {
  if (!value) return 0;
  const m = value.match(/(-?[\d.]+)px/);
  return m ? parseFloat(m[1]) : 0;
}
function isBold(weight) {
  if (!weight) return false;
  if (weight === "bold" || weight === "bolder") return true;
  const n = parseInt(weight, 10);
  return !isNaN(n) && n >= 600;
}
function textAlign(value) {
  switch (value) {
    case "center":
      return "center";
    case "right":
    case "end":
      return "right";
    case "justify":
      return "justify";
    default:
      return "left";
  }
}
function borderStyleToDashType(value) {
  switch (value) {
    case "dashed":
      return "dash";
    case "dotted":
      return "dot";
    case "double":
      return "solid";
    default:
      return void 0;
  }
}
function parseBorderRadius(value, minSide) {
  if (!value || minSide <= 0) return 0;
  const pct = value.match(/^([\d.]+)%/);
  const px = pct ? parseFloat(pct[1]) / 100 * minSide : extractPx(value);
  return px <= 0 ? 0 : clamp(px, 0, minSide / 2);
}
function extractRotation(transform) {
  if (!transform || transform === "none") return void 0;
  const rot = transform.match(/rotate\((-?[\d.]+)deg\)/);
  if (rot) {
    const deg = parseFloat(rot[1]);
    return deg === 0 ? void 0 : deg;
  }
  const mat = transform.match(/matrix\(\s*([^,\s]+),\s*([^,\s]+),/);
  if (mat) {
    const a = parseFloat(mat[1]);
    const b = parseFloat(mat[2]);
    const deg = Math.atan2(b, a) * (180 / Math.PI);
    return Math.abs(deg) < 0.01 ? void 0 : deg;
  }
  return void 0;
}
function parseShadow(value) {
  if (!value || value === "none") return null;
  const parts = [];
  let depth = 0;
  let buf = "";
  for (const ch of value) {
    if (ch === "(") depth++;
    else if (ch === ")") depth--;
    if (ch === "," && depth === 0) {
      parts.push(buf);
      buf = "";
    } else {
      buf += ch;
    }
  }
  if (buf) parts.push(buf);
  for (const part of parts) {
    const s = part.trim();
    if (/\binset\b/.test(s)) continue;
    const colorMatch = s.match(/(rgba?\([^)]+\)|#[0-9a-fA-F]{3,8})/);
    const color = colorMatch ? parseColor(colorMatch[0]) : { hex: "000000", alpha: 0.3 };
    if (!color) continue;
    const lengths = s.replace(colorMatch?.[0] ?? "", "").match(/-?[\d.]+px/g);
    if (!lengths || lengths.length < 2) continue;
    const offsetX = parseFloat(lengths[0]);
    const offsetY = parseFloat(lengths[1]);
    const blur = lengths[2] ? parseFloat(lengths[2]) : 0;
    const dist = Math.sqrt(offsetX * offsetX + offsetY * offsetY);
    let angle = Math.atan2(offsetY, offsetX) * (180 / Math.PI);
    if (angle < 0) angle += 360;
    return {
      type: "outer",
      color: color.hex,
      opacity: clamp(color.alpha, 0, 1),
      blur: clamp(pxToPoints(blur), 0, 100),
      offset: clamp(pxToPoints(dist), 0, 200),
      angle: Math.round(angle)
    };
  }
  return null;
}
function lineSpacingMultiple(lineHeight, fontSizePx) {
  if (!lineHeight || lineHeight === "normal") return void 0;
  const px = extractPx(lineHeight);
  if (px > 0) {
    const baseline = fontSizePx * 1.3333333333333333;
    return baseline <= 0 ? void 0 : clamp(px / baseline, 0.5, 5);
  }
  const mult = parseFloat(lineHeight);
  if (!isNaN(mult) && mult > 0 && mult < 10) return clamp(mult, 0.5, 5);
  return void 0;
}
function letterSpacingPoints(value) {
  if (!value || value === "normal") return void 0;
  const px = extractPx(value);
  if (px !== 0) return clamp(pxToPoints(px), -20, 100);
  return void 0;
}
function underlineStyle(value) {
  switch (value) {
    case "double":
      return "dbl";
    case "dotted":
      return "dotted";
    case "dashed":
      return "dash";
    case "wavy":
      return "wavy";
    default:
      return "sng";
  }
}
function isPreserveWhitespace(whiteSpace) {
  return whiteSpace === "pre" || whiteSpace === "pre-wrap" || whiteSpace === "break-spaces";
}
function trimBlockNewlines(text) {
  return text.replace(/^\n+|\n+$/g, "");
}
function normalizeText(text, whiteSpace) {
  if (isPreserveWhitespace(whiteSpace)) {
    return text;
  }
  if (whiteSpace === "pre-line") {
    return text.split("\n").map((line) => line.replace(/[ \t]+/g, " ").trim()).join("\n");
  }
  return text.replace(/\s+/g, " ").trim();
}
function noWrap(style) {
  if (style.whiteSpace === "pre") return true;
  if (style.whiteSpace !== "nowrap") return false;
  const overflow = (style.overflow ?? "").trim().split(/\s+/)[0] ?? "";
  const scrollable = overflow === "auto" || overflow === "scroll" || overflow === "overlay";
  const ellipsis = (overflow === "hidden" || overflow === "clip") && (style.textOverflow ?? "").includes("ellipsis");
  return !scrollable && !ellipsis;
}

// src/render/context.ts
function rectToPptx(rect, ctx) {
  const x = rect.x - ctx.originX;
  const y = rect.y - ctx.originY;
  return {
    x: pxToInches(clamp(x, -ctx.slideW, ctx.slideW * 2)),
    y: pxToInches(clamp(y, -ctx.slideH, ctx.slideH * 2)),
    w: pxToInches(Math.max(clamp(rect.w, 0, ctx.slideW * 2), 1)),
    h: pxToInches(Math.max(clamp(rect.h, 0, ctx.slideH * 2), 1))
  };
}

// src/render/media-cache.ts
function hashSvg(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h.toString(36);
}
function imageKey(node) {
  if (node.imageUrl) return node.imageUrl;
  if (node.svg) return `svg:${hashSvg(node.svg)}:${node.rect.w}x${node.rect.h}`;
  return null;
}
function collectImageRefs(node, urls, svgs) {
  if (node.imageUrl) {
    urls.add(node.imageUrl);
  } else if (node.svg) {
    const key = imageKey(node);
    if (!svgs.has(key)) svgs.set(key, { svg: node.svg, w: node.rect.w, h: node.rect.h });
  }
  for (const child of node.children) collectImageRefs(child, urls, svgs);
}
async function buildMediaCache(slides, warnings, resolveMedia) {
  const urls = /* @__PURE__ */ new Set();
  const svgs = /* @__PURE__ */ new Map();
  for (const slide of slides) collectImageRefs(slide.root, urls, svgs);
  const refs = [];
  for (const url of urls) refs.push({ kind: "url", key: url, url });
  for (const [key, { svg, w, h }] of svgs) refs.push({ kind: "svg", key, svg, w, h });
  const cache = /* @__PURE__ */ new Map();
  if (refs.length === 0) return cache;
  const resolved = await resolveMedia(refs);
  for (const r of resolved) {
    for (const w of r.warnings) warnings.push(w);
    cache.set(r.key, r.value);
  }
  return cache;
}

// src/core/fonts.ts
var GENERIC_FONT_MAP = {
  serif: "Georgia",
  "sans-serif": "Arial",
  monospace: "Courier New",
  "system-ui": "Arial",
  "-apple-system": "Arial",
  blinkmacsystemfont: "Arial",
  "ui-serif": "Georgia",
  "ui-sans-serif": "Arial",
  "ui-monospace": "Courier New",
  "ui-rounded": "Arial",
  cursive: "Comic Sans MS",
  fantasy: "Impact",
  math: "Cambria Math",
  emoji: "Segoe UI Emoji"
};
function resolveFontFamily(family, swapMap) {
  if (!family) return "Arial";
  const first = family.split(",")[0].trim().replace(/^['"]|['"]$/g, "");
  if (!first) return "Arial";
  const lc = first.toLowerCase();
  if (swapMap) {
    for (const key in swapMap) if (key.toLowerCase() === lc) return swapMap[key];
  }
  return GENERIC_FONT_MAP[lc] ?? first;
}

// src/render/text-runs.ts
function textFormat(style, swapMap) {
  const color = parseColor(style.color) || { hex: "000000", alpha: 1 };
  const deco = `${style.textDecorationLine || ""} ${style.textDecoration || ""}`;
  const decoColor = parseColor(style.textDecorationColor);
  const underlineColor = decoColor && decoColor.hex !== color.hex ? decoColor.hex : void 0;
  const fontSizePx = extractPx(style.fontSize);
  return {
    color: color.hex,
    transparency: opacityToTransparency(color.alpha),
    bold: isBold(style.fontWeight),
    italic: style.fontStyle === "italic" || (style.fontStyle || "").startsWith("oblique"),
    underline: deco.includes("underline") ? { style: underlineStyle(style.textDecorationStyle), color: underlineColor } : void 0,
    strike: deco.includes("line-through") ? true : void 0,
    fontFace: resolveFontFamily(style.fontFamily, swapMap),
    fontSize: fontSizePx > 0 ? clamp(pxToPoints(fontSizePx), 1, 400) : void 0
  };
}
function textTransformFn(value) {
  switch (value) {
    case "uppercase":
      return (s) => s.toUpperCase();
    case "lowercase":
      return (s) => s.toLowerCase();
    case "capitalize":
      return (s) => s.replace(
        new RegExp("(^|[^\\p{L}\\p{N}'\\u2019])(\\p{L})", "gu"),
        (_m, pre, ch) => pre + ch.toUpperCase()
      );
    default:
      return (s) => s;
  }
}
var INLINE_MERGE_KEYS = ["textTransform", "letterSpacing"];
function isRunMergeable(node, parentStyle) {
  if (node.tag === "#text") return true;
  const s = node.style;
  const display = s.display || "";
  if (display !== "inline" && display !== "inline-block" && display !== "inline-flex" && display !== "contents" || s.visibility === "hidden" || s.opacity && s.opacity !== "1") {
    return false;
  }
  const valign = s.verticalAlign || "baseline";
  if (valign !== "baseline" && valign !== "sub" && valign !== "super" && valign !== "0px" && valign !== "0" || imageKey(node) || parseColor(s.backgroundColor) && extractPx(s.paddingTop) + extractPx(s.paddingRight) + extractPx(s.paddingBottom) + extractPx(s.paddingLeft) > 0 || extractPx(s.borderTopWidth || s.borderWidth) > 0 || extractPx(s.borderBottomWidth) > 0 || extractPx(s.borderLeftWidth) > 0 || extractPx(s.borderRightWidth) > 0 || parseShadow(s.boxShadow) || parseShadow(s.textShadow)) {
    return false;
  }
  for (const k of INLINE_MERGE_KEYS) if ((s[k] || "") !== (parentStyle[k] || "")) return false;
  return true;
}
function valignFromBox(style) {
  if (style.display === "flex" || style.display === "inline-flex") {
    const v = (style.flexDirection || "").startsWith("column") ? style.justifyContent : style.alignItems;
    if (v === "center") return "middle";
    if (v === "flex-end" || v === "end") return "bottom";
  }
  if (style.display === "table-cell") {
    if (style.verticalAlign === "middle") return "middle";
    if (style.verticalAlign === "bottom") return "bottom";
  }
  return "top";
}
function alignFromFlex(style) {
  if (style.display !== "flex" && style.display !== "inline-flex") return void 0;
  const a = (style.flexDirection || "").startsWith("column") ? style.alignItems : style.justifyContent;
  if (a === "center") return "center";
  if (a === "flex-end" || a === "end") return "right";
  return void 0;
}
function httpHref(href) {
  return href && /^https?:\/\//i.test(href) ? href : void 0;
}
function formatsEqual(a, b) {
  return a.color === b.color && a.transparency === b.transparency && a.bold === b.bold && a.italic === b.italic && a.fontFace === b.fontFace && a.fontSize === b.fontSize && !!a.underline === !!b.underline && a.underline?.style === b.underline?.style && a.underline?.color === b.underline?.color && !!a.strike === !!b.strike && !!a.subscript === !!b.subscript && !!a.superscript === !!b.superscript && a.highlight === b.highlight;
}
function runsAdjacent(a, b) {
  if (!a.rect || !b.rect) return false;
  const gap = b.rect.x - (a.rect.x + a.rect.w);
  return gap >= -1 && gap < 2;
}
function extractTextRuns(node, swapMap) {
  const consumed = /* @__PURE__ */ new Set();
  const collected = [];
  const ownText = node.text ? normalizeText(node.text, node.style.whiteSpace) : "";
  if (ownText) collected.push({ text: ownText, fmt: textFormat(node.style, swapMap), rect: node.rect });
  const allMergeable = (n) => isRunMergeable(n, node.style) ? n.children.every(allMergeable) : false;
  const absorb = (n, inherited) => {
    consumed.add(n);
    if (n.tag !== "#text" && (n.style.visibility === "hidden" || n.style.opacity === "0")) return;
    if (n.tag === "br") {
      collected.push({ text: "\n", fmt: textFormat(n.style, swapMap), rect: n.rect });
      return;
    }
    const href = httpHref(n.href) || inherited?.href;
    const fmt = textFormat(n.style, swapMap);
    const valign = n.style.verticalAlign;
    const baseline = valign === "sub" ? "sub" : valign === "super" ? "super" : inherited?.baseline;
    if (baseline === "sub") fmt.subscript = true;
    else if (baseline === "super") fmt.superscript = true;
    if (!fmt.underline && inherited?.underline) fmt.underline = inherited.underline;
    if (!fmt.strike && inherited?.strike) fmt.strike = true;
    const bg = parseColor(n.style.backgroundColor);
    const highlight = bg ? bg.hex : inherited?.highlight;
    if (highlight) fmt.highlight = highlight;
    const text = n.text ? normalizeText(n.text, n.style.whiteSpace) : "";
    if (text) collected.push({ text, fmt, rect: n.rect, href });
    for (const child of n.children) {
      absorb(child, { href, baseline, underline: fmt.underline, strike: fmt.strike, highlight });
    }
  };
  if (node.children.length > 0) {
    const hasDirectText = node.children.some((c) => c.tag === "#text");
    const hasMedia = (n) => !!imageKey(n) || n.children.some(hasMedia);
    const allInlineNoMedia = node.children.every((c) => {
      if (c.tag === "#text") return true;
      if (hasMedia(c)) return false;
      const display = c.style.display || "";
      return display === "inline" || display === "inline-block" || display === "inline-flex" || display === "contents";
    });
    if (node.children.every(allMergeable) || hasDirectText && allInlineNoMedia) {
      for (const child of node.children) absorb(child);
    }
  }
  const preserveWs = isPreserveWhitespace(node.style.whiteSpace);
  const merged = [];
  for (const run of collected) {
    const last = merged.at(-1);
    if (last && last.href === run.href && formatsEqual(last.fmt, run.fmt)) {
      const sep = preserveWs || runsAdjacent(last, run) || last.text.endsWith("\n") || run.text.startsWith("\n") ? "" : " ";
      last.text += sep + run.text;
      last.rect = run.rect;
    } else {
      merged.push({ ...run });
    }
  }
  if (merged.length > 0) {
    merged[0].text = merged[0].text.replace(/^\n+/, "");
    merged[merged.length - 1].text = merged[merged.length - 1].text.replace(/\n+$/, "");
  }
  return { runs: merged.filter((r) => r.text !== ""), consumed };
}

// src/render/list.ts
function listStyleConfig(value) {
  switch (value) {
    case "decimal":
    case "decimal-leading-zero":
      return { isNum: true };
    case "lower-alpha":
    case "lower-latin":
      return { isNum: true, numberType: "alphaLcPeriod" };
    case "upper-alpha":
    case "upper-latin":
      return { isNum: true, numberType: "alphaUcPeriod" };
    case "lower-roman":
      return { isNum: true, numberType: "romanLcPeriod" };
    case "upper-roman":
      return { isNum: true, numberType: "romanUcPeriod" };
    case "circle":
      return { isNum: false, characterCode: "25CB" };
    case "square":
      return { isNum: false, characterCode: "25A0" };
    default:
      return { isNum: false };
  }
}
var LIST_UNIFORM_KEYS = [
  "color",
  "fontWeight",
  "fontStyle",
  "fontFamily",
  "fontSize",
  "textDecorationLine",
  "textDecoration",
  "textDecorationStyle",
  "textDecorationColor",
  "textTransform",
  "letterSpacing",
  "textShadow"
];
function detectList(node) {
  if (node.tag !== "ul" && node.tag !== "ol") return null;
  const items = [];
  const first = node.children[0];
  for (const li of node.children) {
    if (li.tag !== "li" || li.style.visibility === "hidden" || li.style.opacity === "0" || li.children.length > 0 || imageKey(li) || parseColor(li.style.backgroundColor)) {
      return null;
    }
    for (const k of LIST_UNIFORM_KEYS) {
      if ((li.style[k] || "") !== (first.style[k] || "")) return null;
    }
    const text = li.text ? normalizeText(li.text, li.style.whiteSpace) : "";
    if (!text) return null;
    items.push(text);
  }
  return items.length > 0 ? items : null;
}

// src/render/render-node.ts
var PT_PER_INCH = 72;
function renderNodeToPptx(node, ctx) {
  if (node.tag === "#text") {
    const style2 = node.style;
    const text = node.text ? trimBlockNewlines(normalizeText(node.text, style2.whiteSpace)) : "";
    if (!text || node.rect.w < 0.5 || node.rect.h < 0.5 || style2.visibility === "hidden") return;
    const coords2 = rectToPptx(node.rect, ctx);
    const fmt = textFormat(style2, ctx.fontMap);
    const fontSize = fmt.fontSize ?? clamp(pxToPoints(extractPx(style2.fontSize) || 16), 1, 400);
    const opacity2 = clamp(parseFloat(style2.opacity ?? "1") || 1, 0, 1);
    const widthPad = pxToInches(Math.max(8, node.rect.w * 0.03));
    try {
      ctx.slide.addText(textTransformFn(style2.textTransform)(text), {
        x: coords2.x,
        y: coords2.y,
        w: coords2.w + widthPad,
        h: coords2.h + pxToInches(4),
        margin: 0,
        fontFace: fmt.fontFace,
        fontSize,
        bold: fmt.bold,
        italic: fmt.italic,
        underline: fmt.underline,
        strike: fmt.strike,
        color: fmt.color,
        transparency: opacityToTransparency((1 - fmt.transparency / 100) * opacity2),
        align: textAlign(style2.textAlign),
        valign: "top",
        fit: "shrink",
        wrap: !noWrap(style2),
        lineSpacingMultiple: lineSpacingMultiple(style2.lineHeight, fontSize),
        charSpacing: letterSpacingPoints(style2.letterSpacing)
      });
    } catch (err) {
      ctx.warnings.push(`addText(#text) failed: ${errMsg(err)}`);
    }
    return;
  }
  const style = node.style;
  if (node.rect.w < 0.5 || node.rect.h < 0.5) {
    for (const child of node.children) renderNodeToPptx(child, ctx);
    return;
  }
  if (style.display === "none" || style.opacity === "0") return;
  if (style.visibility === "hidden") {
    for (const child of node.children) renderNodeToPptx(child, ctx);
    return;
  }
  const rotation = extractRotation(style.transform);
  const box = rotation !== void 0 && node.untransformedRect ? node.untransformedRect : node.rect;
  const coords = rectToPptx(box, ctx);
  const minSide = Math.min(box.w, box.h);
  const radiusPx = parseBorderRadius(style.borderTopLeftRadius || style.borderRadius, minSide);
  const radiusRatio = minSide > 0 ? radiusPx / minSide : 0;
  const opacity = clamp(parseFloat(style.opacity ?? "1") || 1, 0, 1);
  const bgColor = parseColor(style.backgroundColor) || (node.imageUrl ? null : parseGradient(style.backgroundImage));
  const bgFill = bgColor ? { hex: bgColor.hex, alpha: bgColor.alpha * opacity } : null;
  const topW = extractPx(style.borderTopWidth || style.borderWidth);
  const bottomW = extractPx(style.borderBottomWidth);
  const leftW = extractPx(style.borderLeftWidth);
  const rightW = extractPx(style.borderRightWidth);
  const anyBorder = topW || bottomW || leftW || rightW;
  const topColor = style.borderTopColor || style.borderColor;
  const bottomColor = style.borderBottomColor || style.borderColor;
  const leftColor = style.borderLeftColor || style.borderColor;
  const rightColor = style.borderRightColor || style.borderColor;
  const topStyle = style.borderTopStyle || style.borderStyle;
  const bottomStyle = style.borderBottomStyle || style.borderStyle;
  const leftStyle = style.borderLeftStyle || style.borderStyle;
  const rightStyle = style.borderRightStyle || style.borderStyle;
  const uniformBorder = topW > 0 && topW === bottomW && topW === leftW && topW === rightW && topColor === bottomColor && topColor === leftColor && topColor === rightColor && topStyle === bottomStyle && topStyle === leftStyle && topStyle === rightStyle;
  const uniformBorderColor = uniformBorder ? parseColor(topColor) : null;
  const shadow = parseShadow(style.boxShadow);
  const dashType = borderStyleToDashType(style.borderTopStyle || style.borderStyle);
  if (bgFill || uniformBorderColor || shadow) {
    const opts = {
      x: coords.x,
      y: coords.y,
      w: coords.w,
      h: coords.h,
      fill: bgFill ? { color: bgFill.hex, transparency: opacityToTransparency(bgFill.alpha) } : { type: "none" },
      line: uniformBorderColor ? {
        color: uniformBorderColor.hex,
        width: clamp(pxToPoints(topW), 0.25, 20),
        transparency: opacityToTransparency(uniformBorderColor.alpha * opacity),
        dashType
      } : { type: "none" }
    };
    if (shadow) opts.shadow = { ...shadow, opacity: shadow.opacity * opacity };
    if (rotation !== void 0) opts.rotate = rotation;
    let shapeName = "rect";
    if (radiusRatio >= 0.49) {
      const aspect = box.w / box.h;
      if (aspect > 0.75 && aspect < 1.33) {
        shapeName = "ellipse";
      } else {
        shapeName = "roundRect";
        opts.rectRadius = pxToInches(radiusPx);
      }
    } else if (radiusPx > 0.5) {
      shapeName = "roundRect";
      opts.rectRadius = pxToInches(radiusPx);
    }
    try {
      ctx.slide.addShape(shapeName, opts);
    } catch (err) {
      ctx.warnings.push(`addShape failed for <${node.tag}>: ${errMsg(err)}`);
    }
  }
  if (!uniformBorder && anyBorder > 0) {
    const cx = box.x + box.w / 2;
    const cy = box.y + box.h / 2;
    const rad = rotation !== void 0 ? rotation * Math.PI / 180 : 0;
    const cos = Math.cos(rad);
    const sin = Math.sin(rad);
    const side = (width, colorStr, px, py, pw, ph) => {
      if (width <= 0) return;
      const color = parseColor(colorStr);
      if (!color) return;
      let ox = px;
      let oy = py;
      if (rotation !== void 0) {
        const dx = px + pw / 2 - cx;
        const dy = py + ph / 2 - cy;
        ox = cx + dx * cos - dy * sin - pw / 2;
        oy = cy + dx * sin + dy * cos - ph / 2;
      }
      try {
        const opts = {
          x: pxToInches(ox - ctx.originX),
          y: pxToInches(oy - ctx.originY),
          w: pxToInches(Math.max(pw, 1)),
          h: pxToInches(Math.max(ph, 1)),
          fill: { color: color.hex, transparency: opacityToTransparency(color.alpha * opacity) },
          line: { type: "none" }
        };
        if (rotation !== void 0) opts.rotate = rotation;
        ctx.slide.addShape("rect", opts);
      } catch {
      }
    };
    if (bottomW > 0) side(bottomW, bottomColor, box.x, box.y + box.h - bottomW, box.w, bottomW);
    if (topW > 0) side(topW, topColor, box.x, box.y, box.w, topW);
    if (leftW > 0) side(leftW, leftColor, box.x, box.y, leftW, box.h);
    if (rightW > 0) side(rightW, rightColor, box.x + box.w - rightW, box.y, rightW, box.h);
  }
  const key = imageKey(node);
  if (key) {
    const entry = ctx.mediaCache.get(key);
    if (entry) {
      const opts = { x: coords.x, y: coords.y, w: coords.w, h: coords.h, data: entry.dataUrl };
      const isMediaTag = node.tag === "img" || node.tag === "canvas" || node.tag === "svg" || node.tag === "object";
      const hasBgImage = !!style.backgroundImage && style.backgroundImage !== "none";
      const fit = (style.objectFit && (isMediaTag || style.objectFit !== "fill" && !hasBgImage) ? style.objectFit : void 0) || (style.backgroundSize === "cover" ? "cover" : style.backgroundSize === "contain" ? "contain" : void 0);
      if (fit === "cover" || fit === "contain") {
        opts.sizing = { type: fit, w: coords.w, h: coords.h };
        const centered = (pos) => !pos || /^50%\s+50%$/.test(pos.trim());
        const objFitCentered = !!style.objectFit && (isMediaTag || style.objectFit !== "fill") && (style.objectFit === "cover" || style.objectFit === "contain") && (isMediaTag ? centered(style.objectPosition) : !hasBgImage);
        const bgCentered = !isMediaTag && hasBgImage && /^50%\s+50%$/.test((style.backgroundPosition ?? "").trim());
        if (node.imageUrl && entry.w && entry.h && (objFitCentered || bgCentered)) {
          opts.w = pxToInches(entry.w);
          opts.h = pxToInches(entry.h);
        }
      }
      if (radiusRatio >= 0.4) opts.rounding = true;
      if (opacity < 1) opts.transparency = clamp(Math.round((1 - opacity) * 100), 0, 100);
      if (rotation !== void 0) opts.rotate = rotation;
      try {
        ctx.slide.addImage(opts);
      } catch (err) {
        ctx.warnings.push(`addImage failed for <${node.tag}>: ${errMsg(err)}`);
      }
    }
    if (node.tag === "svg" || node.tag === "img" || node.tag === "canvas") return;
  }
  const listItems = detectList(node);
  const consumed = /* @__PURE__ */ new Set();
  if (listItems) {
    const firstLi = node.children[0];
    const liStyle = firstLi.style;
    const listType = liStyle.listStyleType || "";
    const fontSize = clamp(pxToPoints(extractPx(liStyle.fontSize) || 16), 1, 400);
    const fmt = textFormat(liStyle, ctx.fontMap);
    const transform = textTransformFn(liStyle.textTransform);
    const cfg = listStyleConfig(listType);
    const indentPt = cfg.isNum ? Math.max(fontSize * 1.5, 14) : Math.max(fontSize * 0.7, 8);
    const lastLi = node.children[node.children.length - 1];
    const top = firstLi.rect.y - ctx.originY;
    const bottom = lastLi.rect.y + lastLi.rect.h - ctx.originY;
    const left = firstLi.rect.x - ctx.originX;
    const opts = {
      x: pxToInches(left) - indentPt / PT_PER_INCH,
      y: pxToInches(top),
      w: pxToInches(Math.max(firstLi.rect.w, 4)) + indentPt / PT_PER_INCH + pxToInches(8),
      h: pxToInches(Math.max(bottom - top, 4)) + pxToInches(4),
      margin: 2,
      fontFace: fmt.fontFace,
      fontSize,
      bold: fmt.bold,
      italic: fmt.italic,
      underline: fmt.underline,
      strike: fmt.strike,
      color: fmt.color,
      transparency: clamp(Math.round(100 - (100 - fmt.transparency) * opacity), 0, 100),
      align: textAlign(liStyle.textAlign),
      valign: "top",
      fit: "shrink",
      wrap: !noWrap(liStyle),
      lineSpacingMultiple: lineSpacingMultiple(liStyle.lineHeight, fontSize),
      charSpacing: letterSpacingPoints(liStyle.letterSpacing)
    };
    const listShadow = parseShadow(liStyle.textShadow);
    if (listShadow) opts.shadow = { ...listShadow, opacity: listShadow.opacity * opacity };
    const tabPos = indentPt / PT_PER_INCH;
    const bulletFor = (i) => listType === "none" ? false : cfg.isNum ? { type: "number", indent: indentPt, numberStartAt: i + 1, numberType: cfg.numberType } : { indent: indentPt, characterCode: cfg.characterCode };
    const textObjs = listItems.map((item, i) => ({
      text: transform(item),
      options: {
        bullet: bulletFor(i),
        tabStops: listType === "none" ? void 0 : [{ position: tabPos }],
        breakLine: i < listItems.length - 1
      }
    }));
    try {
      ctx.slide.addText(textObjs, opts);
    } catch (err) {
      ctx.warnings.push(`addText(list) failed: ${errMsg(err)}`);
    }
    for (const child of node.children) consumed.add(child);
  }
  const { runs, consumed: runConsumed } = extractTextRuns(node, ctx.fontMap);
  for (const c of runConsumed) consumed.add(c);
  if (runs.length > 0) {
    const fontSize = clamp(pxToPoints(extractPx(style.fontSize) || 16), 1, 400);
    const valign = valignFromBox(style);
    const align = alignFromFlex(style) || textAlign(style.textAlign);
    const padTop = extractPx(style.paddingTop);
    const padBottom = extractPx(style.paddingBottom);
    const padLeft = extractPx(style.paddingLeft);
    const padRight = extractPx(style.paddingRight);
    const insetLeft = leftW + padLeft;
    const insetRight = rightW + padRight;
    const insetTop = topW + padTop;
    const insetBottom = bottomW + padBottom;
    const boxX = coords.x + pxToInches(insetLeft);
    const boxY = coords.y + pxToInches(insetTop);
    const boxW = Math.max(coords.w - pxToInches(insetLeft + insetRight), pxToInches(4));
    const boxH = Math.max(coords.h - pxToInches(insetTop + insetBottom), pxToInches(4));
    const extraW = pxToInches(Math.max(8, box.w * 0.03));
    const shiftX = align === "right" ? extraW : align === "center" ? extraW / 2 : 0;
    const opts = {
      x: boxX - shiftX,
      y: boxY,
      w: boxW + extraW,
      h: boxH + pxToInches(4),
      margin: 2,
      fontSize,
      align,
      valign,
      fit: "shrink",
      wrap: !noWrap(style),
      lineSpacingMultiple: lineSpacingMultiple(style.lineHeight, fontSize),
      charSpacing: letterSpacingPoints(style.letterSpacing)
    };
    if (rotation !== void 0) opts.rotate = rotation;
    const textShadow = parseShadow(style.textShadow);
    if (textShadow) opts.shadow = { ...textShadow, opacity: textShadow.opacity * opacity };
    if (node.tag === "li") {
      const listType = style.listStyleType || "";
      if (listType !== "none") {
        const cfg = listStyleConfig(listType);
        const indentPt = cfg.isNum ? Math.max(fontSize * 1.5, 14) : Math.max(fontSize * 0.7, 8);
        const indentIn = indentPt / PT_PER_INCH;
        opts.x = opts.x - indentIn;
        opts.w = opts.w + indentIn;
        opts.tabStops = [{ position: indentIn }];
        opts.bullet = cfg.isNum ? {
          type: "number",
          indent: indentPt,
          numberType: cfg.numberType,
          ...node.liIndex ? { numberStartAt: node.liIndex } : {}
        } : { indent: indentPt, characterCode: cfg.characterCode };
      }
    }
    const nodeHref = httpHref(node.href);
    if (nodeHref) opts.hyperlink = { url: nodeHref };
    const transform = textTransformFn(style.textTransform);
    if (runs.length === 1) {
      const run = runs[0];
      const alpha = (1 - run.fmt.transparency / 100) * opacity;
      if (!nodeHref && run.href) opts.hyperlink = { url: run.href };
      Object.assign(opts, {
        fontFace: run.fmt.fontFace,
        fontSize: run.fmt.fontSize ?? opts.fontSize,
        bold: run.fmt.bold,
        italic: run.fmt.italic,
        underline: run.fmt.underline,
        strike: run.fmt.strike,
        subscript: run.fmt.subscript,
        superscript: run.fmt.superscript,
        highlight: run.fmt.highlight,
        color: run.fmt.color,
        transparency: opacityToTransparency(alpha)
      });
      try {
        ctx.slide.addText(transform(run.text), opts);
      } catch (err) {
        ctx.warnings.push(`addText failed for <${node.tag}>: ${errMsg(err)}`);
      }
    } else {
      const preserveWs = isPreserveWhitespace(style.whiteSpace);
      const runOpts = (run) => {
        const alpha = (1 - run.fmt.transparency / 100) * opacity;
        return {
          fontFace: run.fmt.fontFace,
          fontSize: run.fmt.fontSize,
          bold: run.fmt.bold,
          italic: run.fmt.italic,
          underline: run.fmt.underline,
          strike: run.fmt.strike,
          subscript: run.fmt.subscript,
          superscript: run.fmt.superscript,
          highlight: run.fmt.highlight,
          color: run.fmt.color,
          transparency: opacityToTransparency(alpha),
          hyperlink: !nodeHref && run.href ? { url: run.href } : void 0
        };
      };
      const lines = [[]];
      runs.forEach((run, i) => {
        const segs = transform(run.text).split("\n");
        segs.forEach((seg, j) => {
          if (j > 0) lines.push([]);
          if (seg !== "") lines[lines.length - 1].push({ text: seg, options: runOpts(run) });
        });
        const next = runs[i + 1];
        const sep = !preserveWs && next && !runsAdjacent(run, next) && !/\n$/.test(run.text) && !/^\n/.test(next.text) ? " " : "";
        if (sep) {
          const cur = lines[lines.length - 1];
          if (cur.length) cur[cur.length - 1].text += sep;
        }
      });
      const lastLine = lines.length - 1;
      const textObjs = [];
      lines.forEach((line, li) => {
        const breakAfter = li < lastLine;
        if (line.length === 0) {
          textObjs.push({ text: "", options: { breakLine: breakAfter } });
          return;
        }
        line.forEach((piece, pi) => {
          textObjs.push({
            text: piece.text,
            options: { ...piece.options, breakLine: pi === line.length - 1 ? breakAfter : false }
          });
        });
      });
      try {
        ctx.slide.addText(textObjs, opts);
      } catch (err) {
        ctx.warnings.push(`addText(runs) failed for <${node.tag}>: ${errMsg(err)}`);
      }
    }
  }
  for (const child of node.children) if (!consumed.has(child)) renderNodeToPptx(child, ctx);
}
function errMsg(err) {
  return err instanceof Error ? err.message : String(err);
}

// src/render/build-editable.ts
async function buildEditablePptx(input, resolveMedia) {
  if (!Array.isArray(input.slides) || input.slides.length === 0) {
    throw new Error("buildEditablePptx: deck has no slides");
  }
  const warnings = [];
  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: "CUSTOM", width: pxToInches(input.width), height: pxToInches(input.height) });
  pptx.layout = "CUSTOM";
  const mediaCache = await buildMediaCache(input.slides, warnings, resolveMedia);
  for (const captured of input.slides) {
    const slide = pptx.addSlide();
    const rootBg = parseColor(captured.root.style.backgroundColor);
    if (rootBg && rootBg.alpha === 1) {
      slide.background = { color: rootBg.hex };
      captured.root.style.backgroundColor = "transparent";
    }
    try {
      renderNodeToPptx(captured.root, {
        slide,
        slideW: input.width,
        slideH: input.height,
        originX: captured.rect.x,
        originY: captured.rect.y,
        mediaCache,
        warnings,
        fontMap: input.fontMap
      });
    } catch (err) {
      warnings.push(`Slide render aborted: ${err instanceof Error ? err.message : String(err)}`);
    }
    if (captured.notes?.trim()) {
      try {
        slide.addNotes(captured.notes);
      } catch (err) {
        warnings.push(`addNotes failed: ${err instanceof Error ? err.message : String(err)}`);
      }
    }
  }
  const buffer = await pptx.write({ outputType: "nodebuffer" });
  return { buffer, bytes: buffer.length, slides: input.slides.length, warnings };
}

// src/render/build-screenshot.ts
import PptxGenJS2 from "pptxgenjs";
async function buildScreenshotPptx(slideTiles, notes, input) {
  const warnings = [];
  const pptx = new PptxGenJS2();
  pptx.defineLayout({ name: "CUSTOM", width: pxToInches(input.width), height: pxToInches(input.height) });
  pptx.layout = "CUSTOM";
  for (let i = 0; i < slideTiles.length; i++) {
    const slide = pptx.addSlide();
    for (const tile of slideTiles[i]) {
      slide.addImage({ data: tile.data, x: tile.x, y: tile.y, w: tile.w, h: tile.h });
    }
    const note = notes[i];
    if (note?.trim()) {
      try {
        slide.addNotes(note);
      } catch (err) {
        warnings.push(`addNotes slide ${i + 1}: ${err instanceof Error ? err.message : String(err)}`);
      }
    }
  }
  const buffer = await pptx.write({ outputType: "nodebuffer" });
  return { buffer, bytes: buffer.length, slides: slideTiles.length, warnings };
}

// src/validate/validate.ts
function validate(setup, perSlide, slideTrees, input, mode) {
  const flags = [];
  if (!setup.fontsReady) {
    flags.push({
      kind: "fonts_timeout",
      message: "document.fonts.ready did not resolve within 8s \u2014 text metrics may use fallback fonts. Check that font URLs are reachable."
    });
  }
  const misses = Array.isArray(setup.fontSwapMisses) ? setup.fontSwapMisses : [];
  if (misses.length > 0) {
    const list = misses.join(", ");
    flags.push({
      kind: "font_swap_failed",
      message: mode === "screenshots" ? `Font swap target(s) ${list} never loaded \u2014 the Google Fonts CSS fetch failed or returned nothing for the family, or the face isn't installed locally. The screenshots were rendered with a fallback font. Retry with a corrected family name or a Google-served family (check fonts.google.com) \u2014 web-safe faces may not exist in this rendering environment either, so they are not a fix here. Tell the user plainly which fonts couldn't be applied.` : `Font swap target(s) ${list} never loaded \u2014 the Google Fonts CSS fetch failed or returned nothing for the family, or the face isn't installed locally. The exported file names these fonts, but layout used a fallback, so text sizing and wrapping may drift. Retry with a corrected family name (check fonts.google.com) or web-safe fonts, and tell the user plainly which fonts couldn't be applied.`
    });
  }
  if (mode === "editable" && input.resetTransformSelector && !setup.resetRect) {
    flags.push({
      kind: "reset_selector_miss",
      message: `resetTransformSelector ${JSON.stringify(input.resetTransformSelector)} matched nothing \u2014 capture may be scaled.`
    });
  } else if (setup.resetRect) {
    const dw = Math.abs(setup.resetRect.w - input.width);
    const dh = Math.abs(setup.resetRect.h - input.height);
    if (dw > 2 || dh > 2) {
      flags.push({
        kind: "slide_size_mismatch",
        message: `resetTransformSelector measures ${Math.round(setup.resetRect.w)}\xD7${Math.round(setup.resetRect.h)} after reset, expected ${input.width}\xD7${input.height}. Check the element isn't constrained by a parent's max-width/overflow.`
      });
    }
  }
  for (let i = 0; i < slideTrees.length; i++) {
    const rect = slideTrees[i].rect;
    if (Math.abs(rect.w - input.width) > 2 || Math.abs(rect.h - input.height) > 2) {
      flags.push({
        kind: "slide_size_mismatch",
        message: `Slide ${i + 1} root measures ${Math.round(rect.w)}\xD7${Math.round(rect.h)}, expected ${input.width}\xD7${input.height}. The selector may be matching a wrapper rather than the slide content, or the deck doesn't fix slide dimensions.`
      });
      break;
    }
  }
  const dupAdjacent = [];
  for (let i = 1; i < perSlide.length; i++) {
    if (perSlide[i].hash === perSlide[i - 1].hash) dupAdjacent.push(i);
  }
  if (dupAdjacent.length > 0) {
    flags.push({
      kind: "duplicate_adjacent",
      message: `Slides ${dupAdjacent.map((i) => `${i}/${i + 1}`).join(", ")} captured identically \u2014 showJs likely failed to navigate. Check the JS actually changes the visible slide; some decks need a longer delay for transitions.`
    });
  }
  const counts = /* @__PURE__ */ new Map();
  for (const r of perSlide) counts.set(r.hash, (counts.get(r.hash) ?? 0) + 1);
  const maxCount = Math.max(0, ...counts.values());
  if (perSlide.length >= 3 && maxCount > perSlide.length / 2) {
    flags.push({
      kind: "duplicate_majority",
      message: `${maxCount}/${perSlide.length} slides captured identically. The deck likely doesn't expose a JS navigation hook, or the showJs is wrong.`
    });
  }
  const notes = setup.notes;
  if (notes.length === 0) {
    flags.push({
      kind: "no_speaker_notes",
      message: "No speaker notes found in the deck (neither data-speaker-notes attributes nor a #speaker-notes JSON block). Expected if the deck has no notes."
    });
  } else {
    if (notes.length !== input.slides.length) {
      flags.push({
        kind: "notes_count_mismatch",
        message: `Speaker notes have ${notes.length} entries but ${input.slides.length} slides were requested \u2014 notes attach by index, so the tail will be missing or misalign.`
      });
    }
    const nonEmpty = notes.filter((n) => n.trim());
    if (nonEmpty.length >= 2 && new Set(nonEmpty).size === 1) {
      flags.push({
        kind: "notes_uniform_nonempty",
        message: `All ${nonEmpty.length} non-empty speaker notes are identical \u2014 likely a placeholder, not real notes.`
      });
    }
  }
  const failed = perSlide.reduce((sum, r) => sum + r.imagesFailed, 0);
  if (failed > 0) {
    const waited = perSlide.reduce((sum, r) => sum + r.imagesWaited, 0);
    flags.push({
      kind: "images_failed",
      message: `${failed}/${waited} images failed to decode before capture \u2014 they'll be missing from the export. Usually a 404 src or a CORS-blocked external URL.`
    });
  }
  return flags;
}

// src/orchestrator/driver.ts
var PlaywrightDriver = class _PlaywrightDriver {
  browser;
  context;
  page;
  constructor(browser, context, page) {
    this.browser = browser;
    this.context = context;
    this.page = page;
  }
  static async launch(url, opts) {
    const { chromium } = await import("playwright");
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: opts.width, height: opts.height },
      deviceScaleFactor: opts.deviceScaleFactor ?? 1
    });
    const page = await context.newPage();
    page.setDefaultTimeout(opts.timeout ?? 3e4);
    await page.goto(url, { waitUntil: "load", timeout: opts.timeout ?? 3e4 });
    return new _PlaywrightDriver(browser, context, page);
  }
  /** Full-viewport PNG as a base64 data URL. (←capturePage().toDataURL()) */
  async screenshot() {
    const buf = await this.page.screenshot({ type: "png" });
    return `data:image/png;base64,${buf.toString("base64")}`;
  }
  async setViewportSize(width, height) {
    await this.page.setViewportSize({ width, height });
  }
  async close() {
    try {
      await this.context.close();
    } catch {
    }
    try {
      await this.browser.close();
    } catch {
    }
  }
};

// src/orchestrator/inject.ts
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
var cached = null;
function bundleSource() {
  if (cached == null) {
    const path = fileURLToPath(new URL("./capture.iife.js", import.meta.url));
    cached = readFileSync(path, "utf8");
  }
  return cached;
}
async function injectCaptureBundle(page) {
  await page.addScriptTag({ content: bundleSource() });
  const ok = await page.evaluate(
    () => typeof window.__genpptx === "object"
  );
  if (!ok) throw new Error("capture bundle failed to initialise window.__genpptx");
}
function evaluateWithTimeout(p, ms, label) {
  let timer;
  const guard = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`${label} timed out after ${ms}ms`)), ms);
  });
  return Promise.race([p, guard]).finally(() => clearTimeout(timer));
}
function captureBudget(spec) {
  const d = Number(spec.delay);
  return 15e3 + (Number.isFinite(d) ? d : 600);
}
function callSetup(page, input) {
  return evaluateWithTimeout(
    page.evaluate((arg) => window.__genpptx.setup(arg), input),
    15e3,
    "setup"
  );
}
function callCaptureEditable(page, spec, fontSwaps) {
  return evaluateWithTimeout(
    page.evaluate(
      ([s, f]) => window.__genpptx.captureEditable(s, f),
      [spec, fontSwaps]
    ),
    captureBudget(spec),
    "editable capture"
  );
}
function callCaptureScreenshot(page, spec) {
  return evaluateWithTimeout(
    page.evaluate((s) => window.__genpptx.captureScreenshot(s), spec),
    captureBudget(spec),
    "screenshot capture"
  );
}
function callResolveMedia(page, refs) {
  return page.evaluate((r) => window.__genpptx.resolveMedia(r), refs);
}

// src/orchestrator/errors.ts
function stringifyError(err) {
  if (err instanceof Error) return err.message;
  try {
    return String(err);
  } catch {
    return "unknown error";
  }
}
function timeoutHint(message, phase, slideNum) {
  if (!/timed?\s*out|timeout/i.test(message)) return "";
  if (phase === "setup") {
    return ". The page didn't finish loading the deck in time \u2014 confirm the URL serves the deck, then retry.";
  }
  const where = `slide ${slideNum}`;
  return phase === "editable" ? `. Capture stalled on ${where} (slide too heavy for editable capture). Retrying identically will stall again \u2014 tell the user, then retry with mode:'screenshots' for a pixel-perfect non-editable fallback.` : `. Capture stalled on ${where}. Retrying identically may stall again \u2014 tell the user and consider a longer delay.`;
}

// src/orchestrator/run.ts
async function runGenPptx(rawInput, driver) {
  const mode = rawInput.mode ?? "editable";
  const input = {
    ...rawInput,
    hideSelectors: sanitizeStrings(rawInput.hideSelectors),
    googleFontImports: sanitizeStrings(rawInput.googleFontImports),
    fontSwaps: sanitizeFontSwaps(rawInput.fontSwaps)
  };
  if (!Array.isArray(input.slides) || input.slides.length === 0) {
    throw new Error("genPptx: slides[] is empty");
  }
  const { page } = driver;
  await injectCaptureBundle(page);
  if (mode === "screenshots") {
    await driver.setViewportSize(input.width, input.height);
    await page.evaluate(
      () => new Promise(
        (r) => requestAnimationFrame(() => requestAnimationFrame(() => r()))
      )
    );
  }
  let setupRes;
  try {
    setupRes = await callSetup(page, {
      mode,
      width: input.width,
      height: input.height,
      hideSelectors: input.hideSelectors,
      googleFontImports: input.googleFontImports,
      fontSwaps: input.fontSwaps,
      resetTransformSelector: mode === "screenshots" ? void 0 : input.resetTransformSelector
    });
  } catch (err) {
    const msg = stringifyError(err);
    throw new Error(`genPptx: setup failed: ${msg}${timeoutHint(msg, "setup")}`);
  }
  if (mode === "editable") {
    const captures = [];
    const capturedSlides = [];
    for (let i = 0; i < input.slides.length; i++) {
      let cap;
      try {
        cap = await callCaptureEditable(page, input.slides[i], input.fontSwaps ?? []);
      } catch (err) {
        const msg = stringifyError(err);
        throw new Error(
          `genPptx: slide ${i + 1}/${input.slides.length} capture failed: ${msg}${timeoutHint(msg, "editable", i + 1)}`
        );
      }
      const captured = { rect: cap.slide.rect, root: cap.slide.root };
      const note = setupRes.notes[i];
      if (note?.trim()) captured.notes = note;
      capturedSlides.push(captured);
      captures.push({ hash: cap.hash, imagesWaited: cap.imagesWaited, imagesFailed: cap.imagesFailed });
    }
    const build2 = await buildEditablePptx(
      { width: input.width, height: input.height, slides: capturedSlides },
      (refs) => callResolveMedia(page, refs)
    );
    const validation2 = validate(setupRes, captures, capturedSlides, input, "editable");
    return {
      buffer: build2.buffer,
      result: {
        bytes: build2.bytes,
        slides: build2.slides,
        warnings: build2.warnings,
        validation: validation2,
        speakerNotes: setupRes.notes.slice(0, input.slides.length)
      }
    };
  }
  const wIn = pxToInches(input.width);
  const hIn = pxToInches(input.height);
  const tiles = [];
  const hashes = [];
  for (let i = 0; i < input.slides.length; i++) {
    let dataUrl;
    try {
      await callCaptureScreenshot(page, input.slides[i]);
      dataUrl = await driver.screenshot();
    } catch (err) {
      const msg = stringifyError(err);
      throw new Error(
        `genPptx: slide ${i + 1}/${input.slides.length} capture failed: ${msg}${timeoutHint(msg, "screenshots", i + 1)}`
      );
    }
    let v = 5381;
    const mid = dataUrl.length >> 1;
    const slice = dataUrl.slice(mid, mid + 4096);
    for (let k = 0; k < slice.length; k++) v = (v << 5) + v + slice.charCodeAt(k) | 0;
    hashes.push({ hash: v >>> 0, imagesWaited: 0, imagesFailed: 0 });
    tiles.push([{ data: dataUrl, x: 0, y: 0, w: wIn, h: hIn }]);
  }
  const build = await buildScreenshotPptx(tiles, setupRes.notes, input);
  const validation = validate(setupRes, hashes, [], input, "screenshots");
  return {
    buffer: build.buffer,
    result: {
      bytes: build.bytes,
      slides: build.slides,
      warnings: build.warnings,
      validation,
      speakerNotes: setupRes.notes.slice(0, input.slides.length)
    }
  };
}

// src/orchestrator/output.ts
import { mkdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

// src/core/filename.ts
function safeBasename(filename, fallback) {
  const cleaned = (filename ?? "").normalize("NFC").replace(/[^\p{L}\p{N}\-_. ]/gu, "_").replace(/\s+/g, " ").replace(/^[.\s]+|[.\s]+$/g, "");
  return cleaned || fallback;
}

// src/orchestrator/output.ts
async function writeOutput(buffer, outDir, filename) {
  const base = safeBasename(filename, "deck").replace(/\.pptx$/i, "") || "deck";
  const name = `${base}.pptx`;
  const dir = resolve(outDir);
  await mkdir(dir, { recursive: true });
  const path = join(dir, name);
  await writeFile(path, buffer);
  return path;
}

// src/cli.ts
var SETUP_HINT = "cd <skill>/agents/gen-pptx && npm install && npx playwright install chromium";
function usage(msg) {
  process.stderr.write(
    `${msg}

Usage: gen-pptx --url <servedDeckUrl> --config <jsonPath|-> [--out <dir>]
`
  );
  process.exit(64);
}
function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--url") out.url = argv[++i];
    else if (a === "--config") out.config = argv[++i];
    else if (a === "--out") out.out = argv[++i];
    else if (a === "-h" || a === "--help") usage("gen-pptx");
    else usage(`Unknown argument: ${a}`);
  }
  if (!out.url) usage("Missing --url");
  if (!out.config) usage("Missing --config");
  if (!/^https?:\/\//i.test(out.url)) {
    usage("--url must be an http(s) URL (deck-stage / multi-file decks need a served origin, not file://)");
  }
  return out;
}
async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}
async function preflight() {
  const major = parseInt(process.versions.node.split(".")[0] ?? "0", 10);
  if (major < 18) {
    process.stderr.write(`gen-pptx: node >= 18 required (found ${process.versions.node}).
`);
    process.exit(1);
  }
  let pw;
  try {
    pw = await import("playwright");
  } catch {
    process.stderr.write(`gen-pptx: playwright is not installed.
One-time setup:
  ${SETUP_HINT}
`);
    process.exit(1);
  }
  let exe = "";
  try {
    exe = pw.chromium.executablePath();
  } catch {
  }
  if (!exe || !existsSync(exe)) {
    process.stderr.write(`gen-pptx: Chromium browser is not installed.
One-time setup:
  ${SETUP_HINT}
`);
    process.exit(1);
  }
}
async function main() {
  const args = parseArgs(process.argv.slice(2));
  await preflight();
  const raw = args.config === "-" ? await readStdin() : readFileSync2(resolve2(args.config), "utf8");
  let input;
  try {
    input = JSON.parse(raw);
  } catch (err) {
    usage(`--config is not valid JSON: ${err instanceof Error ? err.message : String(err)}`);
  }
  if (!input || typeof input.width !== "number" || typeof input.height !== "number") {
    usage("config must include numeric width and height");
  }
  const mode = input.mode ?? "editable";
  const driver = await PlaywrightDriver.launch(args.url, {
    width: input.width,
    height: input.height,
    deviceScaleFactor: mode === "screenshots" ? 2 : 1
  });
  try {
    const { result, buffer } = await runGenPptx(input, driver);
    const savedPath = await writeOutput(buffer, args.out ?? process.cwd(), input.filename);
    process.stdout.write(
      JSON.stringify({
        ok: true,
        file: savedPath,
        slides: result.slides,
        bytes: result.bytes,
        flags: result.validation.map((v) => ({ code: v.kind, message: v.message })),
        warnings: result.warnings,
        speakerNotes: result.speakerNotes
      }) + "\n"
    );
    process.exit(0);
  } catch (err) {
    process.stdout.write(
      JSON.stringify({ ok: false, error: err instanceof Error ? err.message : String(err) }) + "\n"
    );
    process.exit(1);
  } finally {
    await driver.close();
  }
}
main().catch((err) => {
  process.stdout.write(
    JSON.stringify({ ok: false, error: err instanceof Error ? err.message : String(err) }) + "\n"
  );
  process.exit(1);
});
