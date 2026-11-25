() => {
  const MAX_STYLE_ELEMENTS = 8000;
  const MAX_CARD_ELEMENTS = 2000;
  const TOP_COLORS = 8;
  const TOP_RADII = 8;
  const TOP_SHADOWS = 6;

  const data = {
    url: location.href,
    title: document.title,
    viewport: { width: window.innerWidth, height: window.innerHeight },
    errors: [],
  };

  const isRendered = (el) => {
    try {
      const s = getComputedStyle(el);
      if (s.display === "none" || s.visibility === "hidden" || s.opacity === "0") return false;
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    } catch { return false; }
  };

  const isInViewport = (el) => {
    if (!isRendered(el)) return false;
    const r = el.getBoundingClientRect();
    return r.bottom > 0 && r.top < window.innerHeight;
  };

  const bump = (map, key) => {
    if (!key) return;
    map.set(key, (map.get(key) || 0) + 1);
  };

  const safeSelector = (el) => {
    const tag = el.tagName.toLowerCase();
    const cls =
      el.className && typeof el.className === "string" && el.className.trim()
        ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".")
        : "";
    return tag + cls;
  };

  const topN = (map, n) =>
    [...map.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, n)
      .map(([value, count]) => ({ value, count }));

  const skipBg = (c) => !c || c === "rgba(0, 0, 0, 0)" || c === "transparent";

  const styleEls = [];
  const viewportEls = [];
  const all = document.body ? document.body.querySelectorAll("*") : [];
  for (let i = 0; i < all.length; i++) {
    const el = all[i];
    if (styleEls.length < MAX_STYLE_ELEMENTS && isRendered(el)) styleEls.push(el);
    if (viewportEls.length < MAX_CARD_ELEMENTS && isInViewport(el)) viewportEls.push(el);
    if (styleEls.length >= MAX_STYLE_ELEMENTS && viewportEls.length >= MAX_CARD_ELEMENTS) break;
  }
  if (styleEls.length >= MAX_STYLE_ELEMENTS) data.truncated = true;

  const visible = styleEls;

  try {
    const bgCounts = new Map();
    const fgCounts = new Map();
    const bgArea = new Map();
    const families = new Map();
    const headings = {};
    const sizeCounts = new Map();
    const weightCounts = new Map();
    const lineHeightSamples = [];
    const letterSpacingSamples = [];
    const radiiCount = new Map();
    const shadowCount = new Map();
    const transitionSet = new Set();
    const borderCounts = new Map();
    const spacingCounts = new Map();
    const animationSet = new Set();
    const transitionDurations = new Map();
    const transitionEasings = new Map();

    const bodyBg = document.body
      ? getComputedStyle(document.body).backgroundColor
      : "rgb(255, 255, 255)";
    let totalArea = 0;

    for (const el of visible) {
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();

      if (!skipBg(s.backgroundColor)) {
        bump(bgCounts, s.backgroundColor);
        const a = r.width * r.height;
        bgArea.set(s.backgroundColor, (bgArea.get(s.backgroundColor) || 0) + a);
        totalArea += a;
      }
      if (s.color) bump(fgCounts, s.color);

      const family = s.fontFamily.split(",")[0].trim().replace(/['"]/g, "");
      if (family) bump(families, family);

      const tag = el.tagName.toLowerCase();
      if (/^h[1-6]$/.test(tag) && !headings[tag]) {
        headings[tag] = {
          fontSize: s.fontSize,
          fontWeight: s.fontWeight,
          lineHeight: s.lineHeight,
          letterSpacing: s.letterSpacing,
          fontFamily: family,
        };
      }
      bump(sizeCounts, s.fontSize);
      bump(weightCounts, s.fontWeight);

      if (lineHeightSamples.length < 20 && s.lineHeight && s.lineHeight !== "normal") {
        const ctx = `${tag} ${s.fontSize}`;
        if (!lineHeightSamples.find(x => x.context === ctx)) {
          lineHeightSamples.push({ value: s.lineHeight, context: ctx });
        }
      }
      if (letterSpacingSamples.length < 20 && s.letterSpacing && s.letterSpacing !== "normal" && s.letterSpacing !== "0px") {
        const ctx = `${tag} ${s.fontSize}`;
        if (!letterSpacingSamples.find(x => x.context === ctx)) {
          letterSpacingSamples.push({ value: s.letterSpacing, context: ctx });
        }
      }

      const radius = s.borderRadius;
      if (radius && radius !== "0px") bump(radiiCount, radius);

      const shadow = s.boxShadow;
      if (shadow && shadow !== "none") bump(shadowCount, shadow);

      if (s.borderWidth && s.borderWidth !== "0px" && s.borderStyle && s.borderStyle !== "none") {
        const borderVal = `${s.borderWidth} ${s.borderStyle} ${s.borderColor}`;
        bump(borderCounts, borderVal);
      }

      if (s.transition && s.transition !== "none" && s.transition !== "all 0s ease 0s") {
        transitionSet.add(s.transition);
        const parts = s.transition.split(",");
        for (const part of parts) {
          const trimmed = part.trim();
          const durMatch = trimmed.match(/(\d+\.?\d*)(ms|s)/);
          if (durMatch) {
            const dur = durMatch[2] === "s"
              ? `${parseFloat(durMatch[1]) * 1000}ms`
              : `${durMatch[1]}ms`;
            bump(transitionDurations, dur);
          }
          const easeMatch = trimmed.match(/(ease-in-out|ease-in|ease-out|ease|linear|cubic-bezier\([^)]+\))/);
          if (easeMatch) bump(transitionEasings, easeMatch[1]);
        }
      }

      if (s.animationName && s.animationName !== "none") {
        animationSet.add(`${s.animationName} ${s.animationDuration} ${s.animationTimingFunction}`);
      }

      const mt = parseInt(s.marginTop) || 0;
      const mb = parseInt(s.marginBottom) || 0;
      const pt = parseInt(s.paddingTop) || 0;
      const pb = parseInt(s.paddingBottom) || 0;
      for (const v of [mt, mb, pt, pb]) {
        if (v > 0) bump(spacingCounts, `${v}px`);
      }
    }

    const pageBackground = skipBg(bodyBg) ? "#ffffff" : bodyBg;

    data.colors = {
      pageBackground,
      backgroundColors: topN(bgCounts, TOP_COLORS).map((c) => ({
        ...c,
        areaPct: totalArea > 0 ? Math.round(((bgArea.get(c.value) || 0) / totalArea) * 100) : 0,
      })),
      textColors: topN(fgCounts, TOP_COLORS),
      accentCandidates: topN(fgCounts, 20)
        .filter((c) => {
          const v = c.value;
          return !(
            v.includes("255, 255, 255") ||
            v.includes("0, 0, 0") ||
            /rgb\((\d+), \1, \1\)/.test(v)
          );
        })
        .slice(0, 5),
    };

    const bodyStyle = document.body ? getComputedStyle(document.body) : null;
    data.typography = {
      uniqueFamilies: topN(families, 10),
      headings,
      body: bodyStyle
        ? {
            fontSize: bodyStyle.fontSize,
            fontWeight: bodyStyle.fontWeight,
            lineHeight: bodyStyle.lineHeight,
            fontFamily: bodyStyle.fontFamily.split(",")[0].trim().replace(/['"]/g, ""),
          }
        : null,
      sizeDistribution: topN(sizeCounts, 15),
      weightDistribution: topN(weightCounts, 8),
      lineHeights: lineHeightSamples,
      letterSpacings: letterSpacingSamples,
    };

    data.effects = {
      radii: topN(radiiCount, TOP_RADII),
      shadows: topN(shadowCount, TOP_SHADOWS),
      transitions: [...transitionSet].slice(0, 10),
      borders: topN(borderCounts, 8),
    };

    data.motion = {
      transitions: [...transitionSet].slice(0, 15),
      animations: [...animationSet].slice(0, 10),
      dominantDuration: topN(transitionDurations, 1)[0]?.value || null,
      dominantEasing: topN(transitionEasings, 1)[0]?.value || null,
    };

    data.spacingDistribution = topN(spacingCounts, 20);

  } catch (e) {
    data.errors.push(`Style sampling error: ${e.message}`);
  }

  try {
    const spacingSamples = [];
    const sampleTags = ["section", "div", "main", "article", "header", "footer", "nav"];
    for (const el of visible.slice(0, 500)) {
      const tag = el.tagName.toLowerCase();
      if (!sampleTags.includes(tag)) continue;
      if (spacingSamples.length >= 30) break;
      const s = getComputedStyle(el);
      spacingSamples.push({
        tag: safeSelector(el),
        margin: `${s.marginTop} ${s.marginRight} ${s.marginBottom} ${s.marginLeft}`,
        padding: `${s.paddingTop} ${s.paddingRight} ${s.paddingBottom} ${s.paddingLeft}`,
      });
    }
    data.spacingSamples = spacingSamples;
  } catch (e) {
    data.errors.push(`Spacing samples error: ${e.message}`);
  }

  try {
    const sections = document.querySelectorAll("section, [class*='section'], main > div, main > section");
    const gaps = [];
    const sArr = [...sections].filter(isRendered).slice(0, 15);
    for (let i = 0; i < sArr.length - 1; i++) {
      const a = sArr[i].getBoundingClientRect();
      const b = sArr[i + 1].getBoundingClientRect();
      const gap = Math.round(b.top - a.bottom);
      if (gap >= 0) {
        gaps.push({
          between: `${safeSelector(sArr[i])} → ${safeSelector(sArr[i + 1])}`,
          gap: `${gap}px`,
        });
      }
    }
    data.sectionGaps = gaps;
  } catch (e) {
    data.errors.push(`Section gaps error: ${e.message}`);
  }

  try {
    const cards = [];
    const cardSelectors = viewportEls.filter((el) => {
      const s = getComputedStyle(el);
      const hasDepth = (s.boxShadow && s.boxShadow !== "none") ||
                       (s.borderRadius && s.borderRadius !== "0px" && s.borderWidth && s.borderWidth !== "0px");
      const r = el.getBoundingClientRect();
      const isCard = r.width > 100 && r.height > 60 && r.width < 800 && r.height < 600;
      return hasDepth && isCard;
    });

    for (const el of cardSelectors.slice(0, 8)) {
      const s = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      cards.push({
        selector: safeSelector(el),
        width: Math.round(r.width),
        height: Math.round(r.height),
        ratio: `${Math.round(r.width)}:${Math.round(r.height)}`,
        radius: s.borderRadius,
        shadow: s.boxShadow !== "none" ? s.boxShadow : null,
      });
    }
    data.cards = cards;
  } catch (e) {
    data.errors.push(`Card detection error: ${e.message}`);
  }

  try {
    const images = [];
    const imgEls = document.querySelectorAll("img, picture img, video, [style*='background-image']");
    for (const el of [...imgEls].filter(isRendered).slice(0, 15)) {
      const r = el.getBoundingClientRect();
      const isHero = r.width > window.innerWidth * 0.6 && r.top < window.innerHeight;
      const isThumbnail = r.width < 200 && r.height < 200;
      images.push({
        src: el.src || el.currentSrc || "background-image",
        naturalWidth: el.naturalWidth || Math.round(r.width),
        naturalHeight: el.naturalHeight || Math.round(r.height),
        ratio: `${Math.round(r.width)}:${Math.round(r.height)}`,
        role: isHero ? "hero" : isThumbnail ? "thumbnail" : "feature",
      });
    }
    data.images = images;
  } catch (e) {
    data.errors.push(`Image detection error: ${e.message}`);
  }

  try {
    let gridInfo = null;
    let gridCount = 0;
    for (const el of viewportEls) {
      const s = getComputedStyle(el);
      if (s.display === "grid" || s.display === "inline-grid") {
        gridCount++;
        if (!gridInfo) {
          gridInfo = {
            columns: s.gridTemplateColumns.split(" ").length,
            gap: s.gap || s.gridGap || "0px",
            template: s.gridTemplateColumns,
          };
        }
      }
    }
    data.grid = gridInfo;
    data.gridCount = gridCount;
  } catch (e) {
    data.errors.push(`Grid detection error: ${e.message}`);
  }

  try {
    const bodyS = document.body ? getComputedStyle(document.body) : null;
    const containers = document.querySelectorAll("[class*='container'], [class*='wrapper'], [class*='max-w'], main");
    let maxW = null;
    let containerPad = null;
    for (const c of [...containers].filter(isRendered).slice(0, 5)) {
      const cs = getComputedStyle(c);
      if (cs.maxWidth && cs.maxWidth !== "none") {
        maxW = cs.maxWidth;
        containerPad = `${cs.paddingLeft} ${cs.paddingRight}`;
        break;
      }
    }
    data.layout = {
      bodyPadding: bodyS ? `${bodyS.paddingTop} ${bodyS.paddingRight} ${bodyS.paddingBottom} ${bodyS.paddingLeft}` : null,
      containerMaxWidth: maxW,
      containerPadding: containerPad,
    };
  } catch (e) {
    data.errors.push(`Layout detection error: ${e.message}`);
  }

  try {
    const buttons = [];
    const btnEls = document.querySelectorAll('button, a[class*="btn"], a[class*="button"], [role="button"], input[type="submit"]');
    for (const el of [...btnEls].filter(isRendered).slice(0, 10)) {
      const s = getComputedStyle(el);
      buttons.push({
        text: (el.textContent || "").trim().slice(0, 40),
        fontSize: s.fontSize,
        fontWeight: s.fontWeight,
        letterSpacing: s.letterSpacing,
        textTransform: s.textTransform,
        borderRadius: s.borderRadius,
        padding: `${s.paddingTop} ${s.paddingRight} ${s.paddingBottom} ${s.paddingLeft}`,
        background: s.backgroundColor,
        border: s.border,
        transition: s.transition !== "all 0s ease 0s" ? s.transition : null,
      });
    }
    data.buttons = buttons;
  } catch (e) {
    data.errors.push(`Button detection error: ${e.message}`);
  }

  try {
    const navLinks = [];
    const navEls = document.querySelectorAll("nav a, header a, [class*='nav'] a");
    const origin = location.origin;
    const seen = new Set();
    for (const el of navEls) {
      try {
        const href = new URL(el.href, location.href);
        if (href.origin !== origin) continue;
        const path = href.pathname;
        if (seen.has(path)) continue;
        if (/\/(login|signin|signup|register|auth|checkout|cart|account|api|admin)/i.test(path)) continue;
        if (path === "/" || path === location.pathname) continue;
        seen.add(path);
        navLinks.push({
          href: href.href,
          text: (el.textContent || "").trim().slice(0, 60),
        });
      } catch {}
    }
    data.navLinks = navLinks.slice(0, 10);
  } catch (e) {
    data.errors.push(`Nav links error: ${e.message}`);
  }

  try {
    data.focusVisible = !!document.querySelector("[tabindex], a:focus, button:focus");
    data.reducedMotion = false;
    for (const sheet of document.styleSheets) {
      try {
        for (const rule of sheet.cssRules || []) {
          if (rule.conditionText && rule.conditionText.includes("prefers-reduced-motion")) {
            data.reducedMotion = true;
            break;
          }
        }
      } catch {}
      if (data.reducedMotion) break;
    }
  } catch (e) {
    data.errors.push(`Accessibility check error: ${e.message}`);
  }

  return data;
}
