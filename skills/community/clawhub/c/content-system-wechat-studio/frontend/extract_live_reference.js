#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

function toHex(color) {
  if (!color || color === "transparent") return "";
  const normalized = color.trim().toLowerCase();
  if (normalized.startsWith("#")) {
    if (normalized.length === 4) {
      return `#${normalized[1]}${normalized[1]}${normalized[2]}${normalized[2]}${normalized[3]}${normalized[3]}`;
    }
    return normalized;
  }
  const match = normalized.match(/rgba?\(([^)]+)\)/);
  if (!match) return "";
  const parts = match[1].split(",").map((part) => Number.parseFloat(part.trim()));
  if (parts.length < 3) return "";
  if (parts.length >= 4 && parts[3] === 0) return "";
  const [red, green, blue] = parts;
  const toByte = (value) => Math.max(0, Math.min(255, Math.round(value)));
  return `#${toByte(red).toString(16).padStart(2, "0")}${toByte(green)
    .toString(16)
    .padStart(2, "0")}${toByte(blue).toString(16).padStart(2, "0")}`;
}

function slugify(value) {
  return String(value || "reference")
    .toLowerCase()
    .replace(/https?:\/\//g, "")
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/gi, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

async function main() {
  const [, , url, outputDirArg] = process.argv;
  if (!url) {
    throw new Error("Usage: extract_live_reference.js <url> [output-dir]");
  }

  const outputDir = path.resolve(outputDirArg || path.join(process.cwd(), "..", "AI", "reference-shots"));
  fs.mkdirSync(outputDir, { recursive: true });
  const screenshotPath = path.join(outputDir, `${slugify(url)}.png`);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1440, height: 2200 },
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    locale: "zh-CN",
    deviceScaleFactor: 1.5,
  });

  try {
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: screenshotPath, fullPage: false });

    const payload = await page.evaluate(() => {
      function toHexLocal(color) {
        if (!color || color === "transparent") return "";
        const normalized = String(color).trim().toLowerCase();
        if (normalized.startsWith("#")) {
          if (normalized.length === 4) {
            return `#${normalized[1]}${normalized[1]}${normalized[2]}${normalized[2]}${normalized[3]}${normalized[3]}`;
          }
          return normalized;
        }
        const match = normalized.match(/rgba?\(([^)]+)\)/);
        if (!match) return "";
        const parts = match[1].split(",").map((part) => Number.parseFloat(part.trim()));
        if (parts.length < 3) return "";
        if (parts.length >= 4 && parts[3] === 0) return "";
        const [red, green, blue] = parts;
        const toByte = (value) => Math.max(0, Math.min(255, Math.round(value)));
        return `#${toByte(red).toString(16).padStart(2, "0")}${toByte(green)
          .toString(16)
          .padStart(2, "0")}${toByte(blue).toString(16).padStart(2, "0")}`;
      }

      function textLength(node) {
        return (node?.innerText || node?.textContent || "").trim().length;
      }

      function backgroundOf(node) {
        let current = node;
        while (current) {
          const bg = toHexLocal(getComputedStyle(current).backgroundColor);
          if (bg) return bg;
          current = current.parentElement;
        }
        return "";
      }

      function firstMatch(selectors, root = document) {
        for (const selector of selectors) {
          const found = root.querySelector(selector);
          if (found) return found;
        }
        return null;
      }

      function count(map, value, weight = 1) {
        if (!value) return;
        map.set(value, (map.get(value) || 0) + weight);
      }

      function mostCommon(map, fallback = "") {
        let winner = fallback;
        let best = -1;
        for (const [key, score] of map.entries()) {
          if (score > best) {
            winner = key;
            best = score;
          }
        }
        return winner;
      }

      const preferredSelectors = [
        ".rich_media_content",
        "#js_content",
        ".rich_media_wrp",
        "#img-content",
        ".rich_media_area_primary_inner",
        ".rich_media_area_primary",
        "article",
        "main",
        ".content",
        ".post",
        ".entry",
      ];

      let container = null;
      for (const selector of preferredSelectors) {
        const candidate = document.querySelector(selector);
        if (candidate && textLength(candidate) > 600) {
          container = candidate;
          break;
        }
      }

      if (!container) {
        const candidates = Array.from(document.querySelectorAll("article,main,section,div,body"));
        let bestScore = -1;
        for (const candidate of candidates) {
          const score = textLength(candidate) + candidate.querySelectorAll("p,h1,h2,h3,img,blockquote").length * 40;
          if (score > bestScore) {
            container = candidate;
            bestScore = score;
          }
        }
      }

      const pageContainer =
        firstMatch([".rich_media_area_primary", ".rich_media_area_primary_inner", ".rich_media_wrp", "#img-content"]) ||
        container ||
        document.body;
      const titleEl = firstMatch([".rich_media_title", "h1", ".title"], pageContainer) || firstMatch(["h1", ".rich_media_title"]);
      const quoteEl = firstMatch(["blockquote"], container);
      const codeEl = firstMatch(["pre", "code"], container);
      const tableEl = firstMatch(["table", "thead", "th"], container);

      const bodyStyle = getComputedStyle(document.body);
      const pageStyle = getComputedStyle(pageContainer);
      const containerStyle = getComputedStyle(container);
      const titleStyle = titleEl ? getComputedStyle(titleEl) : bodyStyle;

      const sampleNodes = Array.from(container.querySelectorAll("*"))
        .filter((el) => textLength(el) >= 18)
        .slice(0, 1200);
      const imageDrivenElements = Array.from(container.querySelectorAll("*")).filter((el) => {
        const style = getComputedStyle(el);
        return style.backgroundImage && style.backgroundImage !== "none";
      }).length;
      const imageCount = container.querySelectorAll("img").length;
      const fontSizeCounts = new Map();
      const lineHeightCounts = new Map();
      const fontFamilyCounts = new Map();
      const textColorCounts = new Map();
      const accentCounts = new Map();
      const headingSizeCounts = new Map();

      for (const el of sampleNodes) {
        const style = getComputedStyle(el);
        const textLen = textLength(el);
        const fontSize = Number.parseFloat(style.fontSize) || 0;
        const lineHeight = Number.parseFloat(style.lineHeight) || 0;
        const ratio = fontSize > 0 && lineHeight > 0 ? Math.round((lineHeight / fontSize) * 100) / 100 : 0;
        const color = toHexLocal(style.color);
        const weight = Math.max(1, Math.min(6, Math.floor(textLen / 60)));

        if (fontSize >= 11 && fontSize <= 26) {
          count(fontSizeCounts, String(Math.round(fontSize)), weight);
        }
        if (ratio >= 1.2 && ratio <= 2.4) {
          count(lineHeightCounts, String(ratio), weight);
        }
        count(fontFamilyCounts, style.fontFamily, weight);
        if (color && color !== "#ffffff") {
          count(textColorCounts, color, weight);
        }
        if (fontSize >= 18 && textLen <= 120) {
          count(headingSizeCounts, String(Math.round(fontSize)), weight);
        }
        if (color && !["#000000", "#ffffff", "#3e3e3e", "#5f5f5f"].includes(color)) {
          count(accentCounts, color, weight);
        }
        const borderLeft = toHexLocal(style.borderLeftColor);
        if (borderLeft && !["#000000", "#ffffff"].includes(borderLeft)) {
          count(accentCounts, borderLeft, 1);
        }
        const bg = toHexLocal(style.backgroundColor);
        if (bg && !["#000000", "#ffffff", color].includes(bg)) {
          count(accentCounts, bg, 1);
        }
      }

      const paragraphSize = Number.parseFloat(mostCommon(fontSizeCounts, "16")) || 16;
      const paragraphLineHeight = Number.parseFloat(mostCommon(lineHeightCounts, "1.8")) || 1.8;
      const textColor = mostCommon(textColorCounts, toHexLocal(bodyStyle.color)) || "#3e3e3e";
      const accent = mostCommon(accentCounts, toHexLocal(titleStyle.color) || "#576b95");
      const h1Size = Number.parseFloat(titleStyle.fontSize) || Math.max(22, paragraphSize + 8);
      const h2Size = Number.parseFloat(mostCommon(headingSizeCounts, String(Math.max(22, paragraphSize + 6)))) || Math.max(22, paragraphSize + 6);
      const h3Size = Math.max(18, h2Size - 2);
      const rect = container.getBoundingClientRect();
      return {
        title: document.title || "",
        theme: {
          page_bg: backgroundOf(document.body) || toHexLocal(bodyStyle.backgroundColor),
          card_bg: backgroundOf(pageContainer) || backgroundOf(container),
          card_border: toHexLocal(pageStyle.borderColor) || toHexLocal(containerStyle.borderColor),
          text: textColor,
          primary: accent || toHexLocal(titleStyle.color),
          quote_bg: quoteEl ? backgroundOf(quoteEl) : "",
          quote_border: quoteEl ? toHexLocal(getComputedStyle(quoteEl).borderLeftColor) : "",
          code_bg: codeEl ? backgroundOf(codeEl) : "",
          code_border: codeEl ? toHexLocal(getComputedStyle(codeEl).borderColor) : "",
          table_header_bg: tableEl ? backgroundOf(tableEl) : "",
          table_border: tableEl ? toHexLocal(getComputedStyle(tableEl).borderColor) : "",
          body_font: mostCommon(fontFamilyCounts, bodyStyle.fontFamily),
          paragraph_size: paragraphSize,
          paragraph_line_height: paragraphLineHeight,
          h1_size: h1Size,
          h2_size: h2Size,
          h3_size: h3Size,
          container_padding: containerStyle.padding || "32px 24px",
          page_padding: pageStyle.padding || bodyStyle.padding || "24px 12px",
          container_max_width: Math.round(rect.width || 760),
          card_radius: Number.parseFloat(pageStyle.borderRadius) || Number.parseFloat(containerStyle.borderRadius) || 24,
        },
        meta: {
          bodyTextLength: textLength(container),
          containerWidth: Math.round(rect.width || 0),
          containerTag: container.tagName.toLowerCase(),
          pageContainerTag: pageContainer.tagName.toLowerCase(),
          imageCount,
          imageDrivenElements,
          imageDriven: imageCount >= 3 || imageDrivenElements >= 3,
        },
      };
    });

    const result = {
      theme: payload.theme,
      meta: {
        source: url,
        screenshotPath,
        extractor: "playwright-live",
        pageTitle: payload.title,
        ...payload.meta,
      },
    };
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error.message}\n`);
  process.exit(1);
});
