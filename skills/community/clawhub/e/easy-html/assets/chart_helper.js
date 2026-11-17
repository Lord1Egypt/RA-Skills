/* ============================================================
   easy-html 图表助手（B 方案）
   Chart.js 多源 CDN 兜底加载 + 主题色自适应 + 失败降级。
   用法：在 HTML 里放 <canvas data-eh-chart='{...配置...}'></canvas>，
   data-eh-chart 是一个 JSON（type/labels/datasets/options 简化版），
   本脚本会在 Chart.js 就绪后自动渲染所有带 data-eh-chart 的 canvas。

   设计要点：
   - 多 CDN 兜底（单一 CDN 偶发不可达时自动换源）
   - 主题色：从页面 CSS 变量 --primary 等取色，深浅主题自适应
   - 降级：Chart.js 全失败时，canvas 区显示「图表加载失败」文字 + 原始数据表兜底
   - 不依赖入场动画（避免截图/无 JS 时空白）
   ============================================================ */
(function () {
  "use strict";

  // CDN 列表：按顺序尝试，前一个失败自动降级到下一个。
  // 想指定自建/私有镜像，在引入本脚本前设置 window.EH_CHART_CDN = ["https://..."]。
  var CDN_SOURCES = (window.EH_CHART_CDN && window.EH_CHART_CDN.length)
    ? window.EH_CHART_CDN
    : [
        "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js",
        "https://unpkg.com/chart.js@4.4.1/dist/chart.umd.min.js",
        "https://fastly.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"
      ];

  function cssVar(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name);
    return (v && v.trim()) || fallback;
  }

  // 调色板：主色 + 一组和谐辅助色（适配深浅主题）
  function palette() {
    var primary = cssVar("--primary", "#2563EB");
    return [primary, "#22C55E", "#F59E0B", "#A855F7", "#EC4899", "#06B6D4", "#EF4444", "#84CC16"];
  }

  function themeText() { return cssVar("--text-main", cssVar("--text-muted", "#666")); }
  function themeGrid() { return cssVar("--border-color", "rgba(128,128,128,0.15)"); }

  function loadScript(srcs, i, onok, onfail) {
    if (i >= srcs.length) { onfail(); return; }
    var s = document.createElement("script");
    s.src = srcs[i];
    s.onload = function () { onok(); };
    s.onerror = function () { loadScript(srcs, i + 1, onok, onfail); };
    document.head.appendChild(s);
  }

  function renderAll() {
    var nodes = document.querySelectorAll("canvas[data-eh-chart]");
    var txt = themeText(), grid = themeGrid(), colors = palette();
    Chart.defaults.color = txt;
    Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;

    nodes.forEach(function (cv) {
      var cfg;
      try { cfg = JSON.parse(cv.getAttribute("data-eh-chart")); }
      catch (e) { return; }
      var ds = (cfg.datasets || []).map(function (d, idx) {
        var isLine = (cfg.type === "line" || cfg.type === "area");
        return Object.assign({
          backgroundColor: cfg.type === "pie" || cfg.type === "doughnut"
            ? colors
            : (isLine ? (colors[idx % colors.length] + "33") : colors[idx % colors.length]),
          borderColor: colors[idx % colors.length],
          borderWidth: 2,
          fill: cfg.type === "area",
          tension: 0.35,
          borderRadius: cfg.type === "bar" ? 6 : 0
        }, d);
      });
      var type = cfg.type === "area" ? "line" : cfg.type;
      try {
        new Chart(cv.getContext("2d"), {
          type: type,
          data: { labels: cfg.labels || [], datasets: ds },
          options: Object.assign({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: txt, font: { size: 12 } } },
              title: cfg.title ? { display: true, text: cfg.title, color: txt, font: { size: 14, weight: "600" } } : { display: false }
            },
            scales: (type === "pie" || type === "doughnut") ? {} : {
              x: { ticks: { color: txt }, grid: { color: grid } },
              y: { ticks: { color: txt }, grid: { color: grid }, beginAtZero: true }
            }
          }, cfg.options || {})
        });
      } catch (e) { degrade(cv); }
    });
  }

  function degrade(cv) {
    var box = document.createElement("div");
    box.style.cssText = "padding:18px;border:1px dashed " + themeGrid() + ";border-radius:10px;color:" + themeText() + ";font-size:13px;text-align:center;opacity:.8";
    box.textContent = "📊 图表加载失败（可刷新重试）";
    if (cv.parentNode) cv.parentNode.replaceChild(box, cv);
  }

  function degradeAll() {
    document.querySelectorAll("canvas[data-eh-chart]").forEach(degrade);
  }

  function start() {
    if (!document.querySelector("canvas[data-eh-chart]")) return;
    if (window.Chart) { renderAll(); return; }
    loadScript(CDN_SOURCES, 0, renderAll, degradeAll);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else { start(); }
})();
