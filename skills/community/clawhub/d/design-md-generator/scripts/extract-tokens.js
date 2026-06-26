#!/usr/bin/env node
/**
 * extract-tokens.js — Extract design tokens from a URL via Puppeteer/CDP
 * 
 * Usage: node extract-tokens.js <URL> [--output tokens.json]
 * 
 * Extracts: colors, fonts, spacing, borders, shadows, radii from computed styles.
 * Outputs structured JSON for DESIGN.md generation.
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const url = process.argv[2];
const outputFlag = process.argv.indexOf('--output');
const outputPath = outputFlag > -1 ? process.argv[outputFlag + 1] : '/tmp/design-tokens.json';

if (!url) {
  console.error('Usage: node extract-tokens.js <URL> [--output tokens.json]');
  process.exit(1);
}

async function extractTokens() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

  // Wait a bit for fonts and animations
  await new Promise(r => setTimeout(r, 2000));

  const tokens = await page.evaluate(() => {
    const colors = new Map();
    const fonts = new Map();
    const fontSizes = new Map();
    const fontWeights = new Map();
    const lineHeights = new Map();
    const letterSpacings = new Map();
    const borderRadii = new Map();
    const shadows = new Map();
    const borders = new Map();
    const spacings = new Set();

    function addColor(color, context) {
      if (!color || color === 'rgba(0, 0, 0, 0)' || color === 'transparent') return;
      const key = color;
      if (!colors.has(key)) colors.set(key, { value: color, contexts: [], count: 0 });
      const entry = colors.get(key);
      entry.count++;
      if (!entry.contexts.includes(context) && entry.contexts.length < 5) {
        entry.contexts.push(context);
      }
    }

    function rgbToHex(rgb) {
      const match = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      if (!match) return rgb;
      const [, r, g, b] = match;
      return '#' + [r, g, b].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
    }

    const allElements = document.querySelectorAll('*');
    const sampleSize = Math.min(allElements.length, 500);
    const step = Math.max(1, Math.floor(allElements.length / sampleSize));

    for (let i = 0; i < allElements.length; i += step) {
      const el = allElements[i];
      const tag = el.tagName.toLowerCase();
      const styles = getComputedStyle(el);

      // Colors
      addColor(styles.color, `text:${tag}`);
      addColor(styles.backgroundColor, `bg:${tag}`);
      addColor(styles.borderColor, `border:${tag}`);
      if (styles.borderTopColor !== styles.borderColor) addColor(styles.borderTopColor, `border-top:${tag}`);

      // Fonts
      const fontFamily = styles.fontFamily.split(',')[0].trim().replace(/['"]/g, '');
      if (fontFamily) {
        if (!fonts.has(fontFamily)) fonts.set(fontFamily, 0);
        fonts.set(fontFamily, fonts.get(fontFamily) + 1);
      }

      // Font sizes
      const fontSize = styles.fontSize;
      if (fontSize) {
        if (!fontSizes.has(fontSize)) fontSizes.set(fontSize, { count: 0, elements: [] });
        const entry = fontSizes.get(fontSize);
        entry.count++;
        if (entry.elements.length < 3) entry.elements.push(tag);
      }

      // Font weights
      const weight = styles.fontWeight;
      if (weight) {
        if (!fontWeights.has(weight)) fontWeights.set(weight, 0);
        fontWeights.set(weight, fontWeights.get(weight) + 1);
      }

      // Line heights
      const lh = styles.lineHeight;
      if (lh && lh !== 'normal') {
        if (!lineHeights.has(lh)) lineHeights.set(lh, 0);
        lineHeights.set(lh, lineHeights.get(lh) + 1);
      }

      // Letter spacing
      const ls = styles.letterSpacing;
      if (ls && ls !== 'normal' && ls !== '0px') {
        if (!letterSpacings.has(ls)) letterSpacings.set(ls, 0);
        letterSpacings.set(ls, letterSpacings.get(ls) + 1);
      }

      // Border radius
      const radius = styles.borderRadius;
      if (radius && radius !== '0px') {
        if (!borderRadii.has(radius)) borderRadii.set(radius, 0);
        borderRadii.set(radius, borderRadii.get(radius) + 1);
      }

      // Shadows
      const shadow = styles.boxShadow;
      if (shadow && shadow !== 'none') {
        if (!shadows.has(shadow)) shadows.set(shadow, 0);
        shadows.set(shadow, shadows.get(shadow) + 1);
      }

      // Borders
      const border = styles.border;
      if (border && border !== 'none' && !border.startsWith('0px')) {
        if (!borders.has(border)) borders.set(border, 0);
        borders.set(border, borders.get(border) + 1);
      }

      // Spacing (margins and paddings)
      ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight'].forEach(prop => {
        const val = parseFloat(styles[prop]);
        if (val > 0 && val < 200) spacings.add(Math.round(val));
      });
    }

    // Convert colors to hex and dedupe
    const colorList = [];
    for (const [raw, data] of colors) {
      const hex = rgbToHex(raw);
      colorList.push({ raw, hex, contexts: data.contexts, count: data.count });
    }
    colorList.sort((a, b) => b.count - a.count);

    // Get CSS custom properties
    const cssVars = {};
    const rootStyles = getComputedStyle(document.documentElement);
    for (const sheet of document.styleSheets) {
      try {
        for (const rule of sheet.cssRules) {
          if (rule.selectorText === ':root' || rule.selectorText === ':root, :host') {
            for (const prop of rule.style) {
              if (prop.startsWith('--')) {
                cssVars[prop] = rootStyles.getPropertyValue(prop).trim();
              }
            }
          }
        }
      } catch (e) { /* cross-origin stylesheet */ }
    }

    return {
      url: window.location.href,
      title: document.title,
      colors: colorList.slice(0, 50),
      fonts: Object.fromEntries([...fonts].sort((a, b) => b[1] - a[1])),
      fontSizes: Object.fromEntries([...fontSizes].sort((a, b) => parseInt(b[0]) - parseInt(a[0]))),
      fontWeights: Object.fromEntries([...fontWeights].sort((a, b) => b[1] - a[1])),
      lineHeights: Object.fromEntries([...lineHeights].sort((a, b) => b[1] - a[1]).slice(0, 10)),
      letterSpacings: Object.fromEntries([...letterSpacings].sort((a, b) => b[1] - a[1])),
      borderRadii: Object.fromEntries([...borderRadii].sort((a, b) => b[1] - a[1])),
      shadows: Object.fromEntries([...shadows].sort((a, b) => b[1] - a[1]).slice(0, 10)),
      borders: Object.fromEntries([...borders].sort((a, b) => b[1] - a[1]).slice(0, 10)),
      spacingScale: [...spacings].sort((a, b) => a - b),
      cssVariables: cssVars,
      meta: {
        elementCount: allElements.length,
        sampledCount: sampleSize,
        extractedAt: new Date().toISOString()
      }
    };
  });

  await browser.close();

  fs.writeFileSync(outputPath, JSON.stringify(tokens, null, 2));
  console.log(`Tokens extracted: ${outputPath}`);
  console.log(`  Colors: ${tokens.colors.length}`);
  console.log(`  Fonts: ${Object.keys(tokens.fonts).length}`);
  console.log(`  Font sizes: ${Object.keys(tokens.fontSizes).length}`);
  console.log(`  CSS variables: ${Object.keys(tokens.cssVariables).length}`);
  console.log(`  Shadows: ${Object.keys(tokens.shadows).length}`);
}

extractTokens().catch(err => {
  console.error('Extraction failed:', err.message);
  process.exit(1);
});
