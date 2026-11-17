// render_probe.js — 渲染级证据探针(五镜自审的机械部分)
// 用法:把下面整个 IIFE 传给浏览器工具的 evaluate(如 tab.playwright.evaluate),
// 返回 JSON 证据 → 存成 evidence.json → `lint_page.py page.html --render evidence.json`。
// 采集:每个元素的计算色+面积、最小字号、背景/前景对比对、主题倾向。

(() => {
  const sRGB = (r, g, b) => {
    const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  };
  const parse = c => {
    const m = c.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
    return m ? { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] } : null;
  };
  const hex = ({ r, g, b }) => [r, g, b].map(x => x.toString(16).padStart(2, "0")).join("").toUpperCase();

  const els = [...document.querySelectorAll("body *")].filter(e => {
    const r = e.getBoundingClientRect();
    return r.width > 4 && r.height > 4 && r.bottom > 0 && r.top < innerHeight * 8;
  });
  const view = Math.max(1, els.reduce((s, e) => {
    const r = e.getBoundingClientRect();
    return Math.max(s, r.width * innerHeight * 8);
  }, 1));

  const colorArea = {};
  let minFont = 999, fontSample = "";
  const pairs = [];
  for (const e of els) {
    const cs = getComputedStyle(e);
    if (cs.display === "none" || cs.visibility === "hidden") continue;
    const r = e.getBoundingClientRect();
    const area = r.width * Math.min(r.height, innerHeight);
    const bg = parse(cs.backgroundColor);
    if (bg && bg.a > 0.5) {
      const h = hex(bg);
      colorArea[h] = (colorArea[h] || 0) + area;
    }
    const fg = parse(cs.color);
    if (fg && e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) {
      const h = hex(fg);
      colorArea[h] = (colorArea[h] || 0) + 8;
      if (bg && bg.a > 0.5) {
        const l1 = sRGB(Math.max(fg.r, bg.r), Math.max(fg.g, bg.g), Math.max(fg.b, bg.b));
        const l2 = sRGB(Math.min(fg.r, bg.r), Math.min(fg.g, bg.g), Math.min(fg.b, bg.b));
        pairs.push({ fg: hex(fg), bg: hex(bg), ratio: +(((l1 + 0.05) / (l2 + 0.05)).toFixed(2)) });
      }
      const fs = parseFloat(cs.fontSize);
      if (fs < minFont) { minFont = fs; fontSample = e.textContent.trim().slice(0, 18); }
    }
  }
  const total = Object.values(colorArea).reduce((a, b) => a + b, 0) || 1;
  const colors = Object.entries(colorArea)
    .map(([hex, area]) => ({ hex, areaRatio: +(area / total).toFixed(4) }))
    .sort((a, b) => b.areaRatio - a.areaRatio);
  const bodyBg = hex(parse(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255 });
  const bgLum = sRGB(...(bodyBg.match(/../g) || ["FF"]).map(h => parseInt(h, 16)));
  return JSON.stringify({
    url: location.href, bodyBg, theme: bgLum < 0.35 ? "dark" : "light",
    colors: colors.slice(0, 12),
    minFont: +minFont.toFixed(1), fontSample,
    worstPairs: pairs.sort((a, b) => a.ratio - b.ratio).slice(0, 6),
    sections: document.querySelectorAll("section, article, main > div").length
  });
})()
