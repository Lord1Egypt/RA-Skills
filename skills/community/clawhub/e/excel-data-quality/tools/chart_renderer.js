#!/usr/bin/env node
"use strict";
const path = require("path");
const fs = require("fs");
const { parseFile } = require("./lib/parser");
const U = require("./lib/utils");
const { inferFieldType } = require("./lib/profiler");

// --------------- data helpers ---------------

function getColumnData(rows, col, limit) {
  return rows.slice(0, limit).map(r => r[col] != null ? r[col] : null);
}

function aggregate(rows, groupCol, valueCol, fn) {
  const groups = {};
  for (const row of rows) {
    const k = row[groupCol] != null ? String(row[groupCol]) : "(empty)";
    if (!groups[k]) groups[k] = [];
    const v = U.tryParseNumber(row[valueCol]);
    if (v !== null) groups[k].push(v);
  }
  const result = {};
  for (const [k, arr] of Object.entries(groups)) {
    if (fn === "count") result[k] = arr.length;
    else if (fn === "avg" || fn === "mean") result[k] = arr.length ? U.round(arr.reduce((a, b) => a + b, 0) / arr.length, 2) : 0;
    else if (fn === "max") result[k] = Math.max(...arr);
    else if (fn === "min") result[k] = Math.min(...arr);
    else result[k] = U.round(arr.reduce((a, b) => a + b, 0), 2);
  }
  return result;
}

// --------------- chart option builders ---------------

function buildOption(config, headers, rows) {
  const limit = config.limit || 500;
  const type = config.type || "bar";

  if (["pie", "funnel", "treemap"].includes(type)) {
    const agg = aggregate(rows, config.x, config.y, config.aggregate || "sum");
    const data = Object.entries(agg).map(([name, value]) => ({ name, value }));
    const base = {
      title: { text: config.title || "", left: "center" },
      tooltip: { trigger: "item" },
    };
    if (type === "pie") {
      base.series = [{ type: "pie", radius: config.radius || "60%", data, label: { show: true } }];
      if (config.roseType) base.series[0].roseType = config.roseType;
    } else if (type === "funnel") {
      base.series = [{ type: "funnel", data, sort: "descending" }];
    } else {
      base.series = [{ type: "treemap", data: data.map(d => ({ name: d.name, value: d.value })) }];
    }
    return deepMerge(base, config.echarts || {});
  }

  if (type === "scatter") {
    const pairs = rows.slice(0, limit)
      .map(r => [U.tryParseNumber(r[config.x]), U.tryParseNumber(r[config.y])])
      .filter(d => d[0] !== null && d[1] !== null);
    const base = {
      title: { text: config.title || "", left: "center" },
      tooltip: { trigger: "item" },
      xAxis: { name: config.xName || config.x, type: "value" },
      yAxis: { name: config.yName || config.y, type: "value" },
      series: [{ type: "scatter", data: pairs, symbolSize: config.symbolSize || 8 }],
    };
    return deepMerge(base, config.echarts || {});
  }

  if (type === "boxplot") {
    const yCols = Array.isArray(config.y) ? config.y : [config.y];
    const boxData = yCols.map(col => {
      const nums = rows.map(r => U.tryParseNumber(r[col])).filter(n => n !== null).sort((a, b) => a - b);
      if (!nums.length) return [0, 0, 0, 0, 0];
      return [nums[0], U.quantile(nums, 0.25), U.quantile(nums, 0.5), U.quantile(nums, 0.75), nums[nums.length - 1]];
    });
    const base = {
      title: { text: config.title || "", left: "center" },
      tooltip: { trigger: "item" },
      xAxis: { type: "category", data: yCols },
      yAxis: { type: "value" },
      series: [{ type: "boxplot", data: boxData }],
    };
    return deepMerge(base, config.echarts || {});
  }

  if (type === "radar") {
    const yCols = Array.isArray(config.y) ? config.y : [config.y];
    const indicator = yCols.map(col => {
      const nums = rows.map(r => U.tryParseNumber(r[col])).filter(n => n !== null);
      return { name: col, max: nums.length ? Math.max(...nums) * 1.2 : 100 };
    });
    const values = yCols.map(col => {
      const nums = rows.map(r => U.tryParseNumber(r[col])).filter(n => n !== null);
      return nums.length ? U.round(nums.reduce((a, b) => a + b, 0) / nums.length, 2) : 0;
    });
    const base = {
      title: { text: config.title || "", left: "center" },
      tooltip: {},
      radar: { indicator },
      series: [{ type: "radar", data: [{ value: values, name: config.title || "Average" }] }],
    };
    return deepMerge(base, config.echarts || {});
  }

  if (type === "heatmap") {
    const xData = [...new Set(rows.map(r => String(r[config.x] ?? "")))];
    const yData = [...new Set(rows.map(r => String(r[config.y] ?? "")))];
    const valCol = config.value || config.z;
    const data = [];
    for (const row of rows.slice(0, limit)) {
      const xi = xData.indexOf(String(row[config.x] ?? ""));
      const yi = yData.indexOf(String(row[config.y] ?? ""));
      const v = U.tryParseNumber(row[valCol]);
      if (xi >= 0 && yi >= 0 && v !== null) data.push([xi, yi, v]);
    }
    const base = {
      title: { text: config.title || "", left: "center" },
      tooltip: {},
      xAxis: { type: "category", data: xData },
      yAxis: { type: "category", data: yData },
      visualMap: { min: 0, max: Math.max(...data.map(d => d[2]), 1), calculable: true },
      series: [{ type: "heatmap", data, label: { show: data.length < 200 } }],
    };
    return deepMerge(base, config.echarts || {});
  }

  // Default: bar / line / area / combo
  const xData = getColumnData(rows, config.x, limit).map(v => v != null ? String(v) : "");
  const yCols = Array.isArray(config.y) ? config.y : [config.y];

  const series = yCols.map((col, idx) => {
    const seriesConf = (config.series && config.series[idx]) || {};
    const sType = seriesConf.type || (type === "area" ? "line" : type);
    const s = {
      name: seriesConf.name || col,
      type: sType,
      data: getColumnData(rows, col, limit).map(v => U.tryParseNumber(v)),
    };
    if (sType === "line" && (type === "area" || seriesConf.area)) s.areaStyle = seriesConf.areaStyle || {};
    if (seriesConf.smooth) s.smooth = true;
    if (seriesConf.stack) s.stack = seriesConf.stack;
    if (seriesConf.itemStyle) s.itemStyle = seriesConf.itemStyle;
    if (seriesConf.label) s.label = seriesConf.label;
    if (seriesConf.markLine) s.markLine = seriesConf.markLine;
    if (seriesConf.markPoint) s.markPoint = seriesConf.markPoint;
    return s;
  });

  const base = {
    title: { text: config.title || "", left: "center" },
    tooltip: { trigger: "axis" },
    legend: yCols.length > 1 ? { data: series.map(s => s.name), top: 30 } : undefined,
    grid: { left: "10%", right: "5%", bottom: "15%", top: yCols.length > 1 ? 60 : 40 },
    xAxis: {
      type: "category",
      data: xData,
      name: config.xName || undefined,
      axisLabel: { rotate: xData.length > 20 ? 45 : 0 },
    },
    yAxis: { type: "value", name: config.yName || undefined },
    series,
  };
  return deepMerge(base, config.echarts || {});
}

function deepMerge(target, source) {
  if (!source || typeof source !== "object") return target;
  const result = { ...target };
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === "object" && !Array.isArray(source[key]) &&
        result[key] && typeof result[key] === "object" && !Array.isArray(result[key])) {
      result[key] = deepMerge(result[key], source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

// --------------- PNG rendering (ECharts SSR + sharp) ---------------

async function renderToPng(option, width, height, outputPath) {
  const echarts = require("echarts");
  const sharp = require("sharp");

  const chart = echarts.init(null, null, {
    renderer: "svg",
    ssr: true,
    width: width || 900,
    height: height || 600,
  });
  chart.setOption(option);
  const svgStr = chart.renderToSVGString();
  chart.dispose();

  await sharp(Buffer.from(svgStr))
    .png({ compressionLevel: 6 })
    .toFile(outputPath);
}

// --------------- info mode ---------------

function getInfo(headers, rows) {
  const columns = headers.map(h => {
    const type = inferFieldType(h, rows);
    const vals = rows.map(r => r[h]).filter(v => !U.isNullish(v));
    const info = { name: h, type, nonNullCount: vals.length };
    if (["integer", "float"].includes(type)) {
      const nums = vals.map(U.tryParseNumber).filter(n => n !== null);
      if (nums.length) {
        info.min = Math.min(...nums);
        info.max = Math.max(...nums);
        info.mean = U.round(nums.reduce((a, b) => a + b, 0) / nums.length, 2);
      }
    }
    if (["categorical", "string"].includes(type)) {
      const uniq = [...new Set(vals.map(String))];
      info.uniqueCount = uniq.length;
      info.sampleValues = uniq.slice(0, 8);
    }
    if (["date", "datetime"].includes(type)) {
      const dates = vals.map(v => U.tryParseDate(v)).filter(d => d !== null).sort((a, b) => a - b);
      if (dates.length) {
        info.minDate = dates[0].toISOString().slice(0, 10);
        info.maxDate = dates[dates.length - 1].toISOString().slice(0, 10);
      }
    }
    return info;
  });
  return { rowCount: rows.length, columnCount: headers.length, columns };
}

// --------------- main ---------------

async function main() {
  const args = process.argv.slice(2);
  if (!args.length) {
    process.stderr.write([
      "Usage:",
      "  chart_renderer.js <file> --info",
      "    Returns column types and stats for chart planning.",
      "",
      "  chart_renderer.js <file> --config '<json>'",
      "    Render a chart to PNG. Config JSON fields:",
      '    { "type":"bar", "x":"col", "y":"col"|["c1","c2"],',
      '      "title":"...", "aggregate":"sum|avg|count",',
      '      "series":[{"name":"...","type":"line","smooth":true}],',
      '      "echarts":{...}, "width":900, "height":600 }',
      "",
      "  Supported types: bar, line, area, pie, scatter, radar,",
      "    boxplot, heatmap, funnel, treemap, combo (+ any via echarts override)",
      "",
      "  chart_renderer.js <file> --config '<json>' --output <path>",
      "    Save PNG to custom path instead of auto-generated filename.",
    ].join("\n") + "\n");
    process.exit(1);
  }

  const filePath = path.resolve(args[0]);
  let mode = null, configStr = null, outputPath = null;

  for (let i = 1; i < args.length; i++) {
    if (args[i] === "--info") mode = "info";
    else if (args[i] === "--config" && args[i + 1]) { mode = "render"; configStr = args[++i]; }
    else if (args[i] === "--output" && args[i + 1]) outputPath = args[++i];
  }

  try {
    const { headers, rows } = parseFile(filePath);

    if (mode === "info") {
      process.stdout.write(JSON.stringify(getInfo(headers, rows), null, 2) + "\n");
      return;
    }

    if (mode !== "render" || !configStr) {
      process.stderr.write("Specify --info or --config '<json>'\n");
      process.exit(1);
    }

    const config = JSON.parse(configStr);
    const option = buildOption(config, headers, rows);

    if (!outputPath) {
      const dir = path.dirname(filePath);
      const base = path.basename(filePath, path.extname(filePath));
      const suffix = config.title ? config.title.replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, "_").slice(0, 30) : config.type || "chart";
      outputPath = path.join(dir, `${base}_${suffix}.png`);
    }

    const absOut = path.resolve(outputPath);
    await renderToPng(option, config.width, config.height, absOut);

    process.stdout.write(JSON.stringify({
      imageFile: absOut,
      chartType: config.type,
      title: config.title || "",
    }, null, 2) + "\n");
  } catch (err) {
    process.stdout.write(JSON.stringify({ error: err.message }) + "\n");
    process.exit(1);
  }
}

main();
