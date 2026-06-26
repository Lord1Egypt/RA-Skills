#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { renderArtifactImage } from "./render-image.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseDir = path.resolve(__dirname, "..");
const templatePath = path.join(baseDir, "assets", "standalone-chart.template.html");

const DEFAULT_CDN = "https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js";
const CHART_TYPES = new Set([
  "bar",
  "line",
  "area",
  "pie",
  "scatter",
  "radar",
  "heatmap",
  "funnel",
  "gauge",
  "treemap",
  "candlestick",
  "boxplot",
  "sankey",
  "sunburst",
  "graph",
  "tree",
  "parallel",
  "calendar",
  "themeRiver",
  "pictorialBar",
  "waterfall",
  "polarBar",
  "rosePie",
]);
const PAGE_MODES = new Set(["report", "embed"]);
const RENDERERS = new Set(["canvas", "svg"]);
const EXPORT_IMAGE_TYPES = new Set(["png", "svg"]);
const SORT_MODES = new Set(["none", "asc", "desc"]);

const THEMES = {
  light: {
    palette: ["#0f6cbd", "#d95f02", "#2f855a", "#7b61ff", "#c2410c", "#0891b2"],
    background: "#ffffff",
  },
  dark: {
    palette: ["#78c4ff", "#f7a35c", "#6ee7b7", "#c4b5fd", "#fb7185", "#22d3ee"],
    background: "#10141d",
  },
  paper: {
    palette: ["#3f6c51", "#b15f3d", "#355c9a", "#8f5aa8", "#8c6a3c", "#2f7c8c"],
    background: "#f5f0e6",
  },
};

class CliError extends Error {}

function printUsage() {
  console.log(`Usage:
  node {baseDir}/scripts/build.mjs sample --chart line --categories Jan,Feb,Mar --series Revenue:10,20,30 --out ./artifacts/sample
  node {baseDir}/scripts/build.mjs table --input ./data.csv --chart bar --x month --y revenue,profit --out ./artifacts/table
  node {baseDir}/scripts/build.mjs page --option ./option.json --renderer svg --out ./artifacts/page

Modes:
  sample  Build quick charts from inline lists
  table   Build charts from CSV, TSV, or JSON tables
  page    Wrap an existing option JSON file in a standalone HTML export page

Common flags:
  --title <text>
  --subtitle <text>
  --note <text>           Repeatable
  --out <dir>             Required
  --renderer <canvas|svg>
  --theme <light|dark|paper>
  --page-mode <report|embed>
  --width <number>
  --height <number>
  --cdn <url>
  --export-image <png|svg> Repeatable
  --image-out <path>
  --image-pixel-ratio <number>
  --image-background <auto|transparent|color>
  --browser-executable <path>`);
}

function parseArgs(argv) {
  if (argv.length === 0 || argv[0] === "--help" || argv[0] === "-h") {
    return { help: true };
  }

  const [mode, ...rest] = argv;
  const flags = new Map();

  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];
    if (!token.startsWith("--")) {
      throw new CliError(`Unexpected argument: ${token}`);
    }

    const key = token.slice(2);
    const next = rest[index + 1];
    if (!next || next.startsWith("--")) {
      addFlag(flags, key, true);
      continue;
    }

    addFlag(flags, key, next);
    index += 1;
  }

  return { help: false, mode, flags };
}

function addFlag(flags, key, value) {
  if (!flags.has(key)) {
    flags.set(key, []);
  }
  flags.get(key).push(value);
}

function getLast(flags, key, fallback = undefined) {
  const values = flags.get(key);
  return values ? values.at(-1) : fallback;
}

function getAll(flags, key) {
  return flags.get(key) ?? [];
}

function requireFlag(flags, key) {
  const value = getLast(flags, key);
  if (value === undefined || value === true) {
    throw new CliError(`Missing required --${key} value`);
  }
  return value;
}

function parseCsvList(raw) {
  return String(raw)
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function toSlug(value) {
  return (
    String(value)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "") || "echarts-artifact"
  );
}

function toFieldKey(value) {
  return (
    String(value)
      .trim()
      .toLowerCase()
      .replace(/[^\p{L}\p{N}]+/gu, "_")
      .replace(/^_+|_+$/g, "") || "value"
  );
}

function humanize(value) {
  return String(value)
    .replace(/[_-]+/g, " ")
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\b\w/g, (match) => match.toUpperCase());
}

function parseNumber(raw, context) {
  const value = Number(raw);
  if (!Number.isFinite(value)) {
    throw new CliError(`Expected a number for ${context}, got: ${raw}`);
  }
  return value;
}

function parseOptionalNumber(raw) {
  if (raw === null || raw === undefined || raw === "") {
    return null;
  }
  const value = Number(raw);
  return Number.isFinite(value) ? value : null;
}

function parseIntegerFlag(flags, key, fallback) {
  const raw = getLast(flags, key);
  if (raw === undefined) {
    return fallback;
  }
  const value = Number.parseInt(String(raw), 10);
  if (!Number.isFinite(value) || value <= 0) {
    throw new CliError(`--${key} must be a positive integer`);
  }
  return value;
}

function parsePositiveNumberFlag(flags, key, fallback) {
  const raw = getLast(flags, key);
  if (raw === undefined) {
    return fallback;
  }
  const value = Number(raw);
  if (!Number.isFinite(value) || value <= 0) {
    throw new CliError(`--${key} must be a positive number`);
  }
  return value;
}

function parseEnum(value, allowed, label) {
  if (!allowed.has(value)) {
    throw new CliError(`Unsupported ${label}: ${value}`);
  }
  return value;
}

function parseExportImageTypes(flags) {
  const values = getAll(flags, "export-image");
  if (values.length === 0) {
    return [];
  }

  const types = [];
  for (const value of values) {
    if (value === true) {
      throw new CliError("Missing required --export-image value");
    }

    const type = parseEnum(String(value), EXPORT_IMAGE_TYPES, "export image type");
    if (!types.includes(type)) {
      types.push(type);
    }
  }

  return types;
}

function parseBooleanFlag(flags, key) {
  const value = getLast(flags, key);
  if (value === undefined) {
    return false;
  }
  if (value === true || value === "true") {
    return true;
  }
  if (value === "false") {
    return false;
  }
  throw new CliError(`--${key} only accepts true, false, or no value`);
}

function parseSeriesDefinition(raw, index) {
  const separatorIndex = String(raw).indexOf(":");
  if (separatorIndex === -1) {
    throw new CliError(`Series ${index + 1} must look like Name:1,2,3`);
  }

  const name = String(raw).slice(0, separatorIndex).trim();
  const valueList = String(raw)
    .slice(separatorIndex + 1)
    .trim();
  if (!name) {
    throw new CliError(`Series ${index + 1} is missing a name`);
  }

  const values = parseCsvList(valueList).map((value, valueIndex) =>
    parseNumber(value, `${name} value ${valueIndex + 1}`),
  );

  return {
    name,
    key: toFieldKey(name),
    values,
  };
}

function sanitizeObject(value) {
  return JSON.parse(JSON.stringify(value));
}

function resolveCommon(flags) {
  const themeName = getLast(flags, "theme", "light");
  const renderer = getLast(flags, "renderer", "canvas");
  const pageMode = getLast(flags, "page-mode", "report");
  const exportImageTypes = parseExportImageTypes(flags);

  parseEnum(themeName, new Set(Object.keys(THEMES)), "theme");
  parseEnum(renderer, RENDERERS, "renderer");
  parseEnum(pageMode, PAGE_MODES, "page mode");

  return {
    title: getLast(flags, "title", ""),
    subtitle: getLast(flags, "subtitle", ""),
    notes: getAll(flags, "note")
      .map((value) => String(value).trim())
      .filter(Boolean),
    outDir: path.resolve(process.cwd(), requireFlag(flags, "out")),
    renderer,
    theme: themeName,
    pageMode,
    width: parseIntegerFlag(flags, "width", 1280),
    height: parseIntegerFlag(flags, "height", 720),
    cdnUrl: getLast(flags, "cdn", DEFAULT_CDN),
    exportImageTypes,
    imageOut: getLast(flags, "image-out"),
    imagePixelRatio: parsePositiveNumberFlag(flags, "image-pixel-ratio", 2),
    imageBackground: getLast(flags, "image-background", "auto"),
    browserExecutable: getLast(flags, "browser-executable"),
  };
}

function withTitle(title, subtitle) {
  if (!title && !subtitle) {
    return undefined;
  }
  return {
    text: title || "",
    subtext: subtitle || "",
    left: "left",
    top: 16,
  };
}

function resolvePalette(theme) {
  return THEMES[theme].palette;
}

function ensureRows(rows) {
  if (!Array.isArray(rows) || rows.length === 0) {
    throw new CliError("Input data must contain at least one row");
  }
}

function ensureFieldExists(rows, field) {
  const exists = rows.some((row) => Object.hasOwn(row, field));
  if (!exists) {
    throw new CliError(`Field not found in rows: ${field}`);
  }
}

function sortRows(rows, field, sortMode) {
  if (sortMode === "none") {
    return [...rows];
  }

  return [...rows].sort((left, right) => {
    const leftValue = left[field];
    const rightValue = right[field];
    const leftNumber = parseOptionalNumber(leftValue);
    const rightNumber = parseOptionalNumber(rightValue);

    let result = 0;
    if (leftNumber !== null && rightNumber !== null) {
      result = leftNumber - rightNumber;
    } else {
      result = String(leftValue ?? "").localeCompare(String(rightValue ?? ""));
    }

    return sortMode === "asc" ? result : -result;
  });
}

function computeDataZoom(rowCount, horizontal) {
  if (rowCount <= 12) {
    return undefined;
  }

  const slider = {
    type: "slider",
    start: 0,
    end: Math.max(35, Math.floor((12 / rowCount) * 100)),
  };
  const inside = {
    type: "inside",
    start: slider.start,
    end: slider.end,
  };

  if (horizontal) {
    slider.yAxisIndex = 0;
    slider.width = 14;
    inside.yAxisIndex = 0;
  } else {
    slider.xAxisIndex = 0;
    slider.height = 16;
    inside.xAxisIndex = 0;
  }

  return [inside, slider];
}
function buildCartesianOption({
  rows,
  chart,
  xField,
  yFields,
  title,
  subtitle,
  smooth,
  stack,
  horizontal,
  sortMode,
  theme,
  fieldLabels = {},
}) {
  ensureRows(rows);
  ensureFieldExists(rows, xField);
  for (const yField of yFields) {
    ensureFieldExists(rows, yField);
  }

  const sortField = sortMode === "none" ? xField : yFields[0];
  const workingRows = sortRows(rows, sortField, sortMode);
  const categories = workingRows.map((row) => String(row[xField] ?? ""));
  const isArea = chart === "area";
  const baseChart = isArea ? "line" : chart;
  const palette = resolvePalette(theme);
  const horizontalMode = chart === "bar" && horizontal;

  const series = yFields.map((field) => {
    const seriesData = workingRows.map((row) => {
      const value = row[field];
      const maybeNumber = parseOptionalNumber(value);
      if (maybeNumber === null && value !== null && value !== undefined && value !== "") {
        throw new CliError(`Field ${field} must be numeric for ${chart} charts`);
      }
      return maybeNumber;
    });

    const seriesConfig = {
      name: fieldLabels[field] ?? humanize(field),
      type: baseChart,
      data: seriesData,
      emphasis: { focus: "series" },
    };

    if (baseChart === "bar") {
      seriesConfig.barMaxWidth = 42;
    }

    if (baseChart === "line") {
      seriesConfig.smooth = smooth;
    }

    if (isArea) {
      seriesConfig.areaStyle = { opacity: 0.18 };
    }

    if (stack) {
      seriesConfig.stack = "total";
    }

    return seriesConfig;
  });

  const labelRotation = categories.length > 8 && !horizontalMode ? 28 : 0;
  const dataZoom = computeDataZoom(workingRows.length, horizontalMode);

  return sanitizeObject({
    color: palette,
    backgroundColor: "transparent",
    aria: { enabled: true },
    animationDuration: 350,
    animationDurationUpdate: 220,
    title: withTitle(title, subtitle),
    tooltip: { trigger: "axis" },
    legend:
      series.length > 1
        ? {
            top: title || subtitle ? 60 : 10,
            type: "scroll",
          }
        : undefined,
    grid: {
      left: 56,
      right: 28,
      top: title || subtitle ? 110 : 44,
      bottom: dataZoom ? 90 : 44,
      containLabel: true,
    },
    xAxis: horizontalMode
      ? {
          type: "value",
          splitLine: { show: true },
        }
      : {
          type: "category",
          data: categories,
          axisTick: { alignWithLabel: true },
          axisLabel: {
            interval: 0,
            rotate: labelRotation,
            hideOverlap: false,
          },
        },
    yAxis: horizontalMode
      ? {
          type: "category",
          data: categories,
          axisLabel: {
            interval: 0,
            hideOverlap: false,
          },
        }
      : {
          type: "value",
          splitLine: { show: true },
        },
    dataZoom,
    series,
  });
}

function buildPieOption({ rows, labelField, valueField, donut, title, subtitle, sortMode, theme }) {
  ensureRows(rows);
  ensureFieldExists(rows, labelField);
  ensureFieldExists(rows, valueField);

  const workingRows = sortRows(rows, valueField, sortMode);
  const data = workingRows.map((row) => {
    const value = parseOptionalNumber(row[valueField]);
    if (value === null) {
      throw new CliError(`Field ${valueField} must be numeric for pie charts`);
    }
    return {
      name: String(row[labelField] ?? ""),
      value,
    };
  });

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    legend: {
      type: "scroll",
      bottom: 0,
    },
    series: [
      {
        name: title || humanize(valueField),
        type: "pie",
        radius: donut ? ["42%", "70%"] : "72%",
        center: ["50%", "42%"],
        avoidLabelOverlap: true,
        itemStyle: {
          borderColor: theme === "dark" ? "#10141d" : theme === "paper" ? "#f5f0e6" : "#ffffff",
          borderWidth: 2,
          borderRadius: 8,
        },
        label: {
          formatter: "{b}: {d}%",
        },
        data,
      },
    ],
  });
}

function buildRosePieOption({ rows, labelField, valueField, title, subtitle, sortMode, theme }) {
  const option = buildPieOption({
    rows,
    labelField,
    valueField,
    donut: false,
    title,
    subtitle,
    sortMode,
    theme,
  });

  option.series[0].roseType = "area";
  option.series[0].radius = ["18%", "78%"];
  option.series[0].center = ["50%", "44%"];
  option.series[0].label = {
    formatter: "{b}: {c}",
  };

  return sanitizeObject(option);
}

function buildPolarBarOption({
  rows,
  xField,
  yFields,
  title,
  subtitle,
  sortMode,
  theme,
  fieldLabels = {},
}) {
  ensureRows(rows);
  ensureFieldExists(rows, xField);
  for (const yField of yFields) {
    ensureFieldExists(rows, yField);
  }

  const sortField = sortMode === "none" ? xField : yFields[0];
  const workingRows = sortRows(rows, sortField, sortMode);
  const categories = workingRows.map((row) => String(row[xField] ?? ""));
  const palette = resolvePalette(theme);

  const series = yFields.map((field) => ({
    name: fieldLabels[field] ?? humanize(field),
    type: "bar",
    coordinateSystem: "polar",
    roundCap: true,
    data: workingRows.map((row) => {
      const value = parseOptionalNumber(row[field]);
      if (value === null && row[field] !== null && row[field] !== undefined && row[field] !== "") {
        throw new CliError(`Field ${field} must be numeric for polarBar charts`);
      }
      return value;
    }),
    emphasis: { focus: "series" },
  }));

  return sanitizeObject({
    color: palette,
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    legend:
      series.length > 1
        ? {
            top: title || subtitle ? 60 : 10,
            type: "scroll",
          }
        : undefined,
    polar: {
      radius: "72%",
      center: ["50%", title || subtitle ? "58%" : "52%"],
    },
    angleAxis: {
      type: "category",
      data: categories,
      startAngle: 90,
    },
    radiusAxis: {
      type: "value",
      splitLine: { show: true },
    },
    series,
  });
}

function buildWaterfallOption({ rows, xField, valueField, title, subtitle, theme }) {
  ensureRows(rows);
  ensureFieldExists(rows, xField);
  ensureFieldExists(rows, valueField);

  const categories = [];
  const offsetData = [];
  const deltaData = [];
  const palette = resolvePalette(theme);
  let runningTotal = 0;

  for (const [index, row] of rows.entries()) {
    const category = String(row[xField] ?? "");
    const delta = parseOptionalNumber(row[valueField]);
    if (delta === null) {
      throw new CliError(`Field ${valueField} must be numeric for waterfall charts`);
    }

    const start = runningTotal;
    const end = runningTotal + delta;
    const base = Math.min(start, end);
    const height = Math.abs(delta);

    categories.push(category);
    offsetData.push(base);
    deltaData.push({
      value: height,
      itemStyle: {
        color: delta >= 0 ? palette[0] : (palette[1] ?? "#d95f02"),
        borderRadius: 6,
      },
      label: {
        show: rows.length <= 18,
        position: delta >= 0 ? "top" : "bottom",
        formatter: `${delta > 0 ? "+" : ""}${delta}`,
      },
    });

    runningTotal = end;
  }

  const dataZoom = computeDataZoom(rows.length, false);

  return sanitizeObject({
    color: palette,
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "axis" },
    grid: {
      left: 56,
      right: 28,
      top: title || subtitle ? 110 : 44,
      bottom: dataZoom ? 90 : 44,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: categories,
      axisTick: { alignWithLabel: true },
      axisLabel: {
        interval: 0,
        rotate: categories.length > 8 ? 28 : 0,
        hideOverlap: false,
      },
    },
    yAxis: {
      type: "value",
      splitLine: { show: true },
    },
    dataZoom,
    series: [
      {
        type: "bar",
        stack: "total",
        silent: true,
        tooltip: { show: false },
        itemStyle: {
          color: "transparent",
          borderColor: "transparent",
        },
        emphasis: {
          disabled: true,
        },
        data: offsetData,
      },
      {
        name: "Change",
        type: "bar",
        stack: "total",
        barMaxWidth: 42,
        data: deltaData,
      },
    ],
  });
}

function scaleSymbolSize(value, maxValue) {
  if (maxValue <= 0) {
    return 16;
  }
  const scaled = 8 + (value / maxValue) * 24;
  return Math.max(8, Math.min(32, Math.round(scaled)));
}

function buildScatterOption({
  rows,
  xField,
  yField,
  seriesField,
  sizeField,
  labelField,
  title,
  subtitle,
  theme,
  sortMode,
}) {
  ensureRows(rows);
  for (const field of [xField, yField, seriesField, sizeField, labelField]) {
    if (field) {
      ensureFieldExists(rows, field);
    }
  }

  const workingRows = sortRows(rows, xField, sortMode);
  const groups = new Map();
  const rawSizes = sizeField
    ? workingRows.map((row) => parseOptionalNumber(row[sizeField]) ?? 0)
    : [];
  const maxSize = rawSizes.length > 0 ? Math.max(...rawSizes) : 0;

  for (const row of workingRows) {
    const groupName = seriesField ? String(row[seriesField] ?? "Series 1") : "Series 1";
    if (!groups.has(groupName)) {
      groups.set(groupName, []);
    }

    const xValue = parseOptionalNumber(row[xField]);
    const yValue = parseOptionalNumber(row[yField]);
    if (xValue === null || yValue === null) {
      throw new CliError(`Fields ${xField} and ${yField} must be numeric for scatter charts`);
    }

    const item = {
      value: [xValue, yValue],
      name: labelField ? String(row[labelField] ?? "") : undefined,
      symbolSize: sizeField
        ? scaleSymbolSize(parseOptionalNumber(row[sizeField]) ?? 0, maxSize)
        : 16,
    };
    groups.get(groupName).push(item);
  }

  const series = Array.from(groups.entries()).map(([name, data]) => ({
    name,
    type: "scatter",
    data,
    emphasis: { focus: "series" },
  }));

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    legend:
      series.length > 1
        ? {
            top: title || subtitle ? 60 : 10,
          }
        : undefined,
    grid: {
      left: 56,
      right: 28,
      top: title || subtitle ? 110 : 44,
      bottom: 44,
      containLabel: true,
    },
    xAxis: {
      type: "value",
      name: humanize(xField),
      splitLine: { show: true },
    },
    yAxis: {
      type: "value",
      name: humanize(yField),
      splitLine: { show: true },
    },
    series,
  });
}

function niceMax(value) {
  if (!Number.isFinite(value) || value <= 0) {
    return 1;
  }
  const magnitude = 10 ** Math.floor(Math.log10(value));
  return Math.ceil((value * 1.1) / magnitude) * magnitude;
}

function buildRadarOption({ rows, nameField, yFields, title, subtitle, theme, fieldLabels = {} }) {
  ensureRows(rows);
  ensureFieldExists(rows, nameField);
  for (const field of yFields) {
    ensureFieldExists(rows, field);
  }

  const indicator = yFields.map((field) => {
    const values = rows.map((row) => parseOptionalNumber(row[field]) ?? 0);
    return {
      name: fieldLabels[field] ?? humanize(field),
      max: niceMax(Math.max(...values)),
    };
  });

  const data = rows.map((row) => ({
    name: String(row[nameField] ?? ""),
    value: yFields.map((field) => {
      const value = parseOptionalNumber(row[field]);
      if (value === null) {
        throw new CliError(`Field ${field} must be numeric for radar charts`);
      }
      return value;
    }),
  }));

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    legend:
      data.length > 1
        ? {
            top: title || subtitle ? 60 : 10,
          }
        : undefined,
    radar: {
      radius: "64%",
      indicator,
      axisName: {
        color: theme === "dark" ? "#dbe7ff" : "#25313f",
      },
      splitArea: {
        areaStyle: {
          color:
            theme === "dark"
              ? ["rgba(120, 196, 255, 0.02)", "rgba(120, 196, 255, 0.05)"]
              : ["rgba(15, 108, 189, 0.02)", "rgba(15, 108, 189, 0.05)"],
        },
      },
    },
    series: [
      {
        type: "radar",
        areaStyle: {
          opacity: data.length === 1 ? 0.18 : 0.08,
        },
        data,
      },
    ],
  });
}
function parseMatrix(raw, xCount, yCount) {
  const rows = String(raw)
    .split(";")
    .map((row) => parseCsvList(row))
    .filter((row) => row.length > 0);

  if (rows.length !== yCount) {
    throw new CliError(`Matrix row count ${rows.length} does not match y-category count ${yCount}`);
  }

  return rows.map((row, rowIndex) => {
    if (row.length !== xCount) {
      throw new CliError(
        `Matrix column count ${row.length} on row ${rowIndex + 1} does not match x-category count ${xCount}`,
      );
    }

    return row.map((value, columnIndex) =>
      parseNumber(value, `matrix cell row ${rowIndex + 1} column ${columnIndex + 1}`),
    );
  });
}

function buildHeatmapOption({ rows, xField, yField, valueField, title, subtitle, theme }) {
  ensureRows(rows);
  ensureFieldExists(rows, xField);
  ensureFieldExists(rows, yField);
  ensureFieldExists(rows, valueField);

  const xCategories = [];
  const yCategories = [];
  const xIndex = new Map();
  const yIndex = new Map();

  for (const row of rows) {
    const xValue = String(row[xField] ?? "");
    const yValue = String(row[yField] ?? "");

    if (!xIndex.has(xValue)) {
      xIndex.set(xValue, xCategories.length);
      xCategories.push(xValue);
    }

    if (!yIndex.has(yValue)) {
      yIndex.set(yValue, yCategories.length);
      yCategories.push(yValue);
    }
  }

  const data = rows.map((row) => {
    const value = parseOptionalNumber(row[valueField]);
    if (value === null) {
      throw new CliError(`Field ${valueField} must be numeric for heatmap charts`);
    }

    return [xIndex.get(String(row[xField] ?? "")), yIndex.get(String(row[yField] ?? "")), value];
  });

  const values = data.map((entry) => entry[2]);
  const min = Math.min(...values);
  const max = Math.max(...values);

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { position: "top" },
    grid: {
      left: 80,
      right: 28,
      top: title || subtitle ? 110 : 44,
      bottom: 88,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: xCategories,
      splitArea: { show: true },
      axisLabel: {
        interval: 0,
        rotate: xCategories.length > 10 ? 24 : 0,
        hideOverlap: false,
      },
    },
    yAxis: {
      type: "category",
      data: yCategories,
      splitArea: { show: true },
      axisLabel: {
        interval: 0,
        hideOverlap: false,
      },
    },
    visualMap: {
      min,
      max,
      calculable: true,
      orient: "horizontal",
      left: "center",
      bottom: 18,
      inRange: {
        color:
          theme === "dark"
            ? ["#0f172a", "#164e63", "#0f766e", "#22c55e", "#eab308"]
            : ["#f3f7ff", "#cfe3ff", "#8ec5ff", "#3fa7ff", "#0f6cbd"],
      },
    },
    series: [
      {
        type: "heatmap",
        data,
        label: {
          show: data.length <= 24,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 14,
            shadowColor: "rgba(15, 23, 42, 0.28)",
          },
        },
      },
    ],
  });
}

function buildFunnelOption({ rows, labelField, valueField, title, subtitle, sortMode, theme }) {
  ensureRows(rows);
  ensureFieldExists(rows, labelField);
  ensureFieldExists(rows, valueField);

  const funnelSort = sortMode === "none" ? "desc" : sortMode;
  const workingRows = sortRows(rows, valueField, funnelSort);
  const values = [];
  const data = workingRows.map((row) => {
    const value = parseOptionalNumber(row[valueField]);
    if (value === null) {
      throw new CliError(`Field ${valueField} must be numeric for funnel charts`);
    }
    values.push(value);
    return {
      name: String(row[labelField] ?? ""),
      value,
    };
  });

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    legend: {
      type: "scroll",
      bottom: 0,
    },
    series: [
      {
        type: "funnel",
        sort: funnelSort,
        left: "10%",
        top: title || subtitle ? 92 : 28,
        bottom: 44,
        width: "80%",
        min: Math.min(...values),
        max: Math.max(...values),
        minSize: "20%",
        maxSize: "100%",
        gap: 4,
        label: {
          show: true,
          position: "inside",
        },
        itemStyle: {
          borderColor: theme === "dark" ? "#10141d" : theme === "paper" ? "#f5f0e6" : "#ffffff",
          borderWidth: 2,
          borderRadius: 8,
        },
        data,
      },
    ],
  });
}

function buildGaugeCenter(index, count) {
  if (count <= 1) {
    return ["50%", "58%"];
  }

  const columns = count <= 2 ? count : 2;
  const rows = Math.ceil(count / columns);
  const column = index % columns;
  const row = Math.floor(index / columns);
  const x = `${Math.round(((column + 0.5) / columns) * 100)}%`;
  const y = `${Math.round(24 + ((row + 0.5) / rows) * 60)}%`;
  return [x, y];
}

function buildGaugeOption({
  rows,
  labelField,
  valueField,
  maxField,
  maxValue,
  title,
  subtitle,
  theme,
}) {
  ensureRows(rows);
  ensureFieldExists(rows, valueField);
  if (labelField) {
    ensureFieldExists(rows, labelField);
  }
  if (maxField) {
    ensureFieldExists(rows, maxField);
  }

  const baseValues = rows.map((row) => {
    const value = parseOptionalNumber(row[valueField]);
    if (value === null) {
      throw new CliError(`Field ${valueField} must be numeric for gauge charts`);
    }
    return value;
  });
  const fallbackMax = maxValue ?? niceMax(Math.max(...baseValues));
  const total = rows.length;

  const series = rows.map((row, index) => {
    const value = parseOptionalNumber(row[valueField]);
    const rawMax = maxField ? parseOptionalNumber(row[maxField]) : fallbackMax;
    const max = rawMax === null ? fallbackMax : rawMax;
    if (max <= 0) {
      throw new CliError("Gauge max must be greater than zero");
    }

    return {
      type: "gauge",
      center: buildGaugeCenter(index, total),
      radius: total === 1 ? "78%" : total <= 2 ? "62%" : "50%",
      min: 0,
      max,
      progress: {
        show: true,
        width: 14,
        roundCap: true,
      },
      axisLine: {
        lineStyle: {
          width: 14,
        },
      },
      splitLine: {
        distance: -18,
        length: 12,
        lineStyle: {
          width: 2,
        },
      },
      axisTick: {
        distance: -18,
        length: 6,
      },
      axisLabel: {
        distance: 22,
        color: theme === "dark" ? "#99a7c0" : "#536176",
      },
      pointer: {
        length: "70%",
        width: 4,
      },
      anchor: {
        show: true,
        size: 10,
      },
      title: {
        fontSize: 14,
        offsetCenter: [0, total === 1 ? "72%" : "82%"],
      },
      detail: {
        valueAnimation: true,
        fontSize: total === 1 ? 30 : 22,
        offsetCenter: [0, total === 1 ? "40%" : "54%"],
        formatter: "{value}",
      },
      data: [
        {
          value,
          name: labelField ? String(row[labelField] ?? "") : title || humanize(valueField),
        },
      ],
    };
  });

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    series,
  });
}

function normalizeTreemapNode(node) {
  const next = { name: node.name };
  if (node.children.length > 0) {
    next.children = node.children.map((child) => normalizeTreemapNode(child));
    next.value = node.value ?? next.children.reduce((sum, child) => sum + (child.value ?? 0), 0);
  } else {
    next.value = node.value ?? 0;
  }
  return next;
}

function buildTreemapData(rows, labelField, valueField, parentField) {
  const nodes = new Map();
  const childNames = new Set();

  function getNode(name) {
    if (!nodes.has(name)) {
      nodes.set(name, { name, value: null, children: [] });
    }
    return nodes.get(name);
  }

  for (const row of rows) {
    const label = String(row[labelField] ?? "").trim();
    if (!label) {
      throw new CliError(`Field ${labelField} must contain non-empty labels for treemap charts`);
    }

    const value = parseOptionalNumber(row[valueField]);
    if (value === null) {
      throw new CliError(`Field ${valueField} must be numeric for treemap charts`);
    }

    const node = getNode(label);
    node.value = value;

    if (!parentField) {
      continue;
    }

    const parent = String(row[parentField] ?? "").trim();
    if (!parent) {
      continue;
    }

    const parentNode = getNode(parent);
    if (!parentNode.children.includes(node)) {
      parentNode.children.push(node);
    }
    childNames.add(label);
  }

  if (!parentField) {
    return rows.map((row) => ({
      name: String(row[labelField] ?? ""),
      value: parseOptionalNumber(row[valueField]) ?? 0,
    }));
  }

  return Array.from(nodes.values())
    .filter((node) => !childNames.has(node.name))
    .map((node) => normalizeTreemapNode(node));
}

function buildTreemapOption({ rows, labelField, valueField, parentField, title, subtitle, theme }) {
  ensureRows(rows);
  ensureFieldExists(rows, labelField);
  ensureFieldExists(rows, valueField);
  if (parentField) {
    ensureFieldExists(rows, parentField);
  }

  const data = buildTreemapData(rows, labelField, valueField, parentField);

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    series: [
      {
        type: "treemap",
        roam: false,
        top: title || subtitle ? 92 : 24,
        bottom: 18,
        breadcrumb: {
          show: true,
        },
        label: {
          show: true,
        },
        upperLabel: {
          show: true,
          height: 22,
        },
        itemStyle: {
          borderColor: theme === "dark" ? "#10141d" : theme === "paper" ? "#f5f0e6" : "#ffffff",
          borderWidth: 2,
          gapWidth: 2,
          borderRadius: 8,
        },
        data,
      },
    ],
  });
}
function parseTupleList(raw, tupleSize, label) {
  const rows = String(raw)
    .split(";")
    .map((row) => parseCsvList(row))
    .filter((row) => row.length > 0);

  return rows.map((row, rowIndex) => {
    if (row.length !== tupleSize) {
      throw new CliError(
        `${label} row ${rowIndex + 1} must contain ${tupleSize} values, got ${row.length}`,
      );
    }

    return row.map((value, valueIndex) =>
      parseNumber(value, `${label} row ${rowIndex + 1} value ${valueIndex + 1}`),
    );
  });
}

function buildCandlestickOption({
  rows,
  xField,
  openField,
  closeField,
  lowField,
  highField,
  title,
  subtitle,
  theme,
  sortMode,
}) {
  ensureRows(rows);
  for (const field of [xField, openField, closeField, lowField, highField]) {
    ensureFieldExists(rows, field);
  }

  const workingRows = sortRows(rows, xField, sortMode);
  const categories = workingRows.map((row) => String(row[xField] ?? ""));
  const palette = resolvePalette(theme);
  const dataZoom = computeDataZoom(workingRows.length, false);
  const data = workingRows.map((row, index) => {
    const open = parseOptionalNumber(row[openField]);
    const close = parseOptionalNumber(row[closeField]);
    const low = parseOptionalNumber(row[lowField]);
    const high = parseOptionalNumber(row[highField]);
    if (open === null || close === null || low === null || high === null) {
      throw new CliError(`Candlestick row ${index + 1} must provide numeric OHLC values`);
    }
    if (low > high) {
      throw new CliError(`Candlestick row ${index + 1} has low greater than high`);
    }
    if (low > Math.min(open, close) || high < Math.max(open, close)) {
      throw new CliError(`Candlestick row ${index + 1} must satisfy low <= open/close <= high`);
    }
    return [open, close, low, high];
  });

  return sanitizeObject({
    color: palette,
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "cross" },
    },
    grid: {
      left: 56,
      right: 28,
      top: title || subtitle ? 110 : 44,
      bottom: dataZoom ? 90 : 44,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: categories,
      axisLabel: {
        interval: 0,
        rotate: categories.length > 10 ? 24 : 0,
        hideOverlap: false,
      },
    },
    yAxis: {
      type: "value",
      scale: true,
      splitLine: { show: true },
    },
    dataZoom,
    series: [
      {
        name: title || "OHLC",
        type: "candlestick",
        data,
        itemStyle: {
          color: palette[0],
          color0: palette[1] ?? "#d95f02",
          borderColor: palette[0],
          borderColor0: palette[1] ?? "#d95f02",
        },
      },
    ],
  });
}

function buildBoxplotOption({
  rows,
  xField,
  lowField,
  q1Field,
  medianField,
  q3Field,
  highField,
  title,
  subtitle,
  theme,
  sortMode,
}) {
  ensureRows(rows);
  for (const field of [xField, lowField, q1Field, medianField, q3Field, highField]) {
    ensureFieldExists(rows, field);
  }

  const sortField = sortMode === "none" ? xField : medianField;
  const workingRows = sortRows(rows, sortField, sortMode);
  const categories = workingRows.map((row) => String(row[xField] ?? ""));
  const dataZoom = computeDataZoom(workingRows.length, false);
  const data = workingRows.map((row, index) => {
    const low = parseOptionalNumber(row[lowField]);
    const q1 = parseOptionalNumber(row[q1Field]);
    const median = parseOptionalNumber(row[medianField]);
    const q3 = parseOptionalNumber(row[q3Field]);
    const high = parseOptionalNumber(row[highField]);
    if (low === null || q1 === null || median === null || q3 === null || high === null) {
      throw new CliError(`Boxplot row ${index + 1} must provide numeric quartile values`);
    }
    if (!(low <= q1 && q1 <= median && median <= q3 && q3 <= high)) {
      throw new CliError(`Boxplot row ${index + 1} must satisfy low <= q1 <= median <= q3 <= high`);
    }
    return [low, q1, median, q3, high];
  });

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    grid: {
      left: 56,
      right: 28,
      top: title || subtitle ? 110 : 44,
      bottom: dataZoom ? 90 : 44,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: categories,
      axisLabel: {
        interval: 0,
        rotate: categories.length > 10 ? 24 : 0,
        hideOverlap: false,
      },
    },
    yAxis: {
      type: "value",
      splitLine: { show: true },
    },
    dataZoom,
    series: [
      {
        name: title || "Distribution",
        type: "boxplot",
        boxWidth: [16, 48],
        data,
      },
    ],
  });
}

function parseLinkDefinition(raw, index) {
  const text = String(raw).trim();
  const valueSeparator = text.lastIndexOf(":");
  if (valueSeparator === -1) {
    throw new CliError(`Link ${index + 1} must look like Source>Target:Value`);
  }

  const endpoints = text.slice(0, valueSeparator).trim();
  const arrowIndex = endpoints.indexOf(">");
  if (arrowIndex === -1) {
    throw new CliError(`Link ${index + 1} must look like Source>Target:Value`);
  }

  const source = endpoints.slice(0, arrowIndex).trim();
  const target = endpoints.slice(arrowIndex + 1).trim();
  if (!source || !target) {
    throw new CliError(`Link ${index + 1} must include both source and target names`);
  }

  return {
    source,
    target,
    value: parseNumber(text.slice(valueSeparator + 1).trim(), `link ${index + 1} value`),
  };
}

function buildSankeyOption({ rows, sourceField, targetField, valueField, title, subtitle, theme }) {
  ensureRows(rows);
  for (const field of [sourceField, targetField, valueField]) {
    ensureFieldExists(rows, field);
  }

  const nodeNames = new Set();
  const links = rows.map((row, index) => {
    const source = String(row[sourceField] ?? "").trim();
    const target = String(row[targetField] ?? "").trim();
    const value = parseOptionalNumber(row[valueField]);
    if (!source || !target) {
      throw new CliError(`Sankey row ${index + 1} must include non-empty source and target values`);
    }
    if (value === null) {
      throw new CliError(`Field ${valueField} must be numeric for sankey charts`);
    }
    nodeNames.add(source);
    nodeNames.add(target);
    return { source, target, value };
  });

  const data = Array.from(nodeNames)
    .sort((left, right) => left.localeCompare(right))
    .map((name) => ({ name }));

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    series: [
      {
        type: "sankey",
        top: title || subtitle ? 92 : 24,
        bottom: 18,
        left: 18,
        right: 18,
        layoutIterations: 32,
        nodeGap: 18,
        draggable: false,
        emphasis: { focus: "adjacency" },
        lineStyle: {
          color: "gradient",
          curveness: 0.5,
          opacity: 0.35,
        },
        label: {
          color: theme === "dark" ? "#dbe7ff" : "#25313f",
        },
        data,
        links,
      },
    ],
  });
}

function buildSunburstOption({
  rows,
  labelField,
  valueField,
  parentField,
  title,
  subtitle,
  theme,
}) {
  ensureRows(rows);
  ensureFieldExists(rows, labelField);
  ensureFieldExists(rows, valueField);
  if (parentField) {
    ensureFieldExists(rows, parentField);
  }

  const data = buildTreemapData(rows, labelField, valueField, parentField);

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    series: [
      {
        type: "sunburst",
        center: ["50%", title || subtitle ? "56%" : "50%"],
        radius: [0, title || subtitle ? "78%" : "86%"],
        sort: null,
        nodeClick: "rootToNode",
        emphasis: { focus: "ancestor" },
        label: {
          rotate: "radial",
        },
        itemStyle: {
          borderColor: theme === "dark" ? "#10141d" : theme === "paper" ? "#f5f0e6" : "#ffffff",
          borderWidth: 2,
        },
        data,
      },
    ],
  });
}

function buildTreeOption({ rows, labelField, valueField, parentField, title, subtitle, theme }) {
  ensureRows(rows);
  ensureFieldExists(rows, labelField);
  ensureFieldExists(rows, valueField);
  if (parentField) {
    ensureFieldExists(rows, parentField);
  }

  const data = buildTreemapData(rows, labelField, valueField, parentField);

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    series: [
      {
        type: "tree",
        data,
        top: title || subtitle ? 92 : 24,
        bottom: 18,
        left: "8%",
        right: "24%",
        symbol: "circle",
        symbolSize: 10,
        edgeShape: "polyline",
        expandAndCollapse: true,
        initialTreeDepth: -1,
        emphasis: {
          focus: "descendant",
        },
        lineStyle: {
          width: 1.5,
          curveness: 0.5,
        },
        label: {
          position: "left",
          verticalAlign: "middle",
          align: "right",
        },
        leaves: {
          label: {
            position: "right",
            verticalAlign: "middle",
            align: "left",
          },
        },
      },
    ],
  });
}

function parseNodeDefinition(raw, index) {
  const parts = String(raw)
    .split(":")
    .map((part) => part.trim());
  const name = parts[0] ?? "";
  if (!name) {
    throw new CliError(`Node ${index + 1} must include a name`);
  }

  let size = null;
  let group = null;

  if (parts.length >= 2 && parts[1]) {
    const maybeSize = parseOptionalNumber(parts[1]);
    if (maybeSize === null) {
      group = parts[1];
    } else {
      size = maybeSize;
    }
  }

  if (parts.length >= 3) {
    group = parts.slice(2).join(":").trim() || group;
  }

  return {
    name,
    size,
    group,
  };
}

function clampNodeSize(value) {
  return Math.max(12, Math.min(42, Math.round(value)));
}

function buildGraphOption({
  rows,
  sourceField,
  targetField,
  valueField,
  sourceGroupField,
  targetGroupField,
  sourceSizeField,
  targetSizeField,
  title,
  subtitle,
  theme,
  nodes = [],
}) {
  ensureRows(rows);
  for (const field of [
    sourceField,
    targetField,
    valueField,
    sourceGroupField,
    targetGroupField,
    sourceSizeField,
    targetSizeField,
  ]) {
    if (field) {
      ensureFieldExists(rows, field);
    }
  }

  const nodeMap = new Map();

  function rememberNode(name, details = {}) {
    if (!nodeMap.has(name)) {
      nodeMap.set(name, { name, group: null, size: null, degree: 0 });
    }
    const node = nodeMap.get(name);
    if (details.group && !node.group) {
      node.group = details.group;
    }
    if (details.size !== null && details.size !== undefined && Number.isFinite(details.size)) {
      node.size = node.size === null ? details.size : Math.max(node.size, details.size);
    }
    return node;
  }

  for (const node of nodes) {
    rememberNode(node.name, {
      group: node.group ?? null,
      size: node.size ?? null,
    });
  }

  const baseLinks = rows.map((row, index) => {
    const source = String(row[sourceField] ?? "").trim();
    const target = String(row[targetField] ?? "").trim();
    if (!source || !target) {
      throw new CliError(`Graph row ${index + 1} must include non-empty source and target values`);
    }

    const edgeValue = valueField ? parseOptionalNumber(row[valueField]) : 1;
    if (valueField && edgeValue === null) {
      throw new CliError(`Field ${valueField} must be numeric for graph charts`);
    }

    const sourceNode = rememberNode(source, {
      group: sourceGroupField ? String(row[sourceGroupField] ?? "").trim() || null : null,
      size: sourceSizeField ? parseOptionalNumber(row[sourceSizeField]) : null,
    });
    const targetNode = rememberNode(target, {
      group: targetGroupField ? String(row[targetGroupField] ?? "").trim() || null : null,
      size: targetSizeField ? parseOptionalNumber(row[targetSizeField]) : null,
    });
    sourceNode.degree += 1;
    targetNode.degree += 1;

    return {
      source,
      target,
      value: edgeValue ?? 1,
    };
  });

  const groupNames = Array.from(
    new Set(
      Array.from(nodeMap.values())
        .map((node) => node.group)
        .filter(Boolean),
    ),
  ).sort((left, right) => left.localeCompare(right));
  const categories = groupNames.map((name) => ({ name }));
  const categoryIndex = new Map(groupNames.map((name, index) => [name, index]));
  const maxLinkValue =
    baseLinks.length > 0 ? Math.max(...baseLinks.map((link) => link.value ?? 1)) : 1;

  const data = Array.from(nodeMap.values())
    .sort((left, right) => left.name.localeCompare(right.name))
    .map((node) => ({
      name: node.name,
      value: node.size ?? node.degree,
      symbolSize:
        node.size !== null && node.size !== undefined
          ? clampNodeSize(node.size)
          : clampNodeSize(16 + node.degree * 2),
      category: node.group ? categoryIndex.get(node.group) : undefined,
    }));

  const links = baseLinks.map((link) => ({
    ...link,
    lineStyle: {
      width: maxLinkValue > 0 ? 1 + (link.value / maxLinkValue) * 4 : 2,
    },
  }));

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    legend:
      categories.length > 1
        ? {
            top: title || subtitle ? 60 : 10,
            type: "scroll",
          }
        : undefined,
    series: [
      {
        type: "graph",
        top: title || subtitle ? 92 : 24,
        bottom: 18,
        left: 18,
        right: 18,
        layout: "force",
        roam: true,
        draggable: false,
        emphasis: {
          focus: "adjacency",
        },
        force: {
          repulsion: 180,
          edgeLength: [60, 140],
          gravity: 0.08,
        },
        label: {
          show: true,
          position: "right",
        },
        lineStyle: {
          opacity: 0.35,
          curveness: 0.2,
        },
        categories,
        data,
        links,
      },
    ],
  });
}

function computeAxisBounds(values) {
  const finiteValues = values.filter((value) => Number.isFinite(value));
  if (finiteValues.length === 0) {
    return { min: 0, max: 1 };
  }

  const min = Math.min(...finiteValues);
  const max = Math.max(...finiteValues);
  if (min === max) {
    const padding = Math.abs(min) * 0.1 || 1;
    return {
      min: Number((min - padding).toFixed(2)),
      max: Number((max + padding).toFixed(2)),
    };
  }

  const padding = (max - min) * 0.08;
  return {
    min: Number((min - padding).toFixed(2)),
    max: Number((max + padding).toFixed(2)),
  };
}

function buildParallelOption({
  rows,
  nameField,
  yFields,
  title,
  subtitle,
  theme,
  fieldLabels = {},
}) {
  ensureRows(rows);
  ensureFieldExists(rows, nameField);
  for (const field of yFields) {
    ensureFieldExists(rows, field);
  }

  const data = rows.map((row, index) => ({
    name: String(row[nameField] ?? `Series ${index + 1}`),
    value: yFields.map((field) => {
      const value = parseOptionalNumber(row[field]);
      if (value === null) {
        throw new CliError(`Field ${field} must be numeric for parallel charts`);
      }
      return value;
    }),
  }));

  const parallelAxis = yFields.map((field, dim) => {
    const bounds = computeAxisBounds(data.map((item) => item.value[dim]));
    return {
      dim,
      name: fieldLabels[field] ?? humanize(field),
      min: bounds.min,
      max: bounds.max,
    };
  });

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { trigger: "item" },
    legend:
      data.length > 1
        ? {
            top: title || subtitle ? 60 : 10,
            type: "scroll",
          }
        : undefined,
    parallel: {
      left: 80,
      right: 56,
      top: title || subtitle ? 118 : 48,
      bottom: 56,
      parallelAxisExpandable: true,
      parallelAxisExpandCenter: 50,
    },
    parallelAxisDefault: {
      type: "value",
      nameLocation: "end",
      nameGap: 18,
      axisLabel: {
        color: theme === "dark" ? "#dbe7ff" : "#25313f",
      },
    },
    parallelAxis,
    series: [
      {
        type: "parallel",
        lineStyle: {
          width: 2,
          opacity: 0.45,
        },
        emphasis: {
          lineStyle: {
            width: 3,
            opacity: 0.85,
          },
        },
        data,
      },
    ],
  });
}

function normalizeDateValue(raw, context) {
  const value = String(raw ?? "").trim();
  if (!value) {
    throw new CliError(`Expected a date for ${context}`);
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    throw new CliError(`Expected an ISO-like date for ${context}, got: ${raw}`);
  }

  return date.toISOString().slice(0, 10);
}

function buildCalendarOption({ rows, dateField, valueField, title, subtitle, theme }) {
  ensureRows(rows);
  ensureFieldExists(rows, dateField);
  ensureFieldExists(rows, valueField);

  const data = rows
    .map((row, index) => {
      const date = normalizeDateValue(row[dateField], `${dateField} row ${index + 1}`);
      const value = parseOptionalNumber(row[valueField]);
      if (value === null) {
        throw new CliError(`Field ${valueField} must be numeric for calendar charts`);
      }
      return [date, value];
    })
    .sort((left, right) => left[0].localeCompare(right[0]));

  const values = data.map((entry) => entry[1]);
  const startDate = data[0][0];
  const endDate = data.at(-1)[0];
  const range = startDate === endDate ? startDate : [startDate, endDate];

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: { position: "top" },
    visualMap: {
      min: Math.min(...values),
      max: Math.max(...values),
      calculable: true,
      orient: "horizontal",
      left: "center",
      bottom: 18,
      inRange: {
        color:
          theme === "dark"
            ? ["#0f172a", "#164e63", "#0f766e", "#22c55e", "#eab308"]
            : ["#f3f7ff", "#cfe3ff", "#8ec5ff", "#3fa7ff", "#0f6cbd"],
      },
    },
    calendar: {
      top: title || subtitle ? 98 : 36,
      left: 36,
      right: 36,
      range,
      cellSize: ["auto", 16],
      splitLine: {
        show: false,
      },
      itemStyle: {
        borderWidth: 3,
        borderColor: theme === "dark" ? "#10141d" : theme === "paper" ? "#f5f0e6" : "#ffffff",
      },
      dayLabel: {
        firstDay: 1,
        nameMap: "en",
      },
      monthLabel: {
        nameMap: "en",
      },
    },
    series: [
      {
        type: "heatmap",
        coordinateSystem: "calendar",
        data,
      },
    ],
  });
}

function buildThemeRiverOption({
  rows,
  dateField,
  valueField,
  seriesField,
  title,
  subtitle,
  theme,
}) {
  ensureRows(rows);
  ensureFieldExists(rows, dateField);
  ensureFieldExists(rows, valueField);
  ensureFieldExists(rows, seriesField);

  const data = rows
    .map((row, index) => {
      const date = normalizeDateValue(row[dateField], `${dateField} row ${index + 1}`);
      const value = parseOptionalNumber(row[valueField]);
      const name = String(row[seriesField] ?? "").trim();
      if (value === null) {
        throw new CliError(`Field ${valueField} must be numeric for themeRiver charts`);
      }
      if (!name) {
        throw new CliError(
          `Field ${seriesField} must contain non-empty names for themeRiver charts`,
        );
      }
      return [date, value, name];
    })
    .sort((left, right) => left[0].localeCompare(right[0]) || left[2].localeCompare(right[2]));

  const names = Array.from(new Set(data.map((entry) => entry[2])));

  return sanitizeObject({
    color: resolvePalette(theme),
    backgroundColor: "transparent",
    aria: { enabled: true },
    title: withTitle(title, subtitle),
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "line",
      },
    },
    legend:
      names.length > 1
        ? {
            top: title || subtitle ? 60 : 10,
            type: "scroll",
          }
        : undefined,
    singleAxis: {
      top: title || subtitle ? 110 : 44,
      bottom: 44,
      type: "time",
      axisLabel: {
        color: theme === "dark" ? "#dbe7ff" : "#25313f",
      },
    },
    series: [
      {
        type: "themeRiver",
        emphasis: {
          focus: "series",
        },
        data,
      },
    ],
  });
}

function buildPictorialBarOption({
  rows,
  xField,
  yFields,
  title,
  subtitle,
  horizontal,
  sortMode,
  theme,
  fieldLabels = {},
}) {
  const option = buildCartesianOption({
    rows,
    chart: "bar",
    xField,
    yFields,
    title,
    subtitle,
    smooth: false,
    stack: false,
    horizontal,
    sortMode,
    theme,
    fieldLabels,
  });

  const maxValue = Math.max(
    1,
    ...option.series.flatMap((series) =>
      series.data.filter((value) => Number.isFinite(value)).map((value) => Number(value)),
    ),
  );

  option.series = option.series.map((series) => ({
    ...series,
    type: "pictorialBar",
    symbol: "roundRect",
    symbolRepeat: "fixed",
    symbolClip: true,
    symbolMargin: 2,
    symbolBoundingData: maxValue,
    symbolSize: horizontal ? [10, 18] : [18, 10],
    symbolPosition: "end",
  }));

  return sanitizeObject(option);
}

function escapeJsonForHtml(value) {
  return JSON.stringify(value, null, 2)
    .replace(/</g, "\\u003c")
    .replace(/>/g, "\\u003e")
    .replace(/&/g, "\\u0026");
}

async function loadTemplate() {
  return fs.readFile(templatePath, "utf8");
}

function renderHtml(template, bootstrap) {
  return template.replace("__BOOTSTRAP_JSON__", escapeJsonForHtml(bootstrap));
}

async function writeJson(filePath, value) {
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function logWrite(filePath) {
  const relative = path.relative(process.cwd(), filePath) || path.basename(filePath);
  console.log(`[ok] wrote ${relative}`);
}

function toManifestFileRef(baseDir, filePath) {
  const relative = path.relative(baseDir, filePath);
  if (!relative.startsWith("..") && !path.isAbsolute(relative)) {
    return relative.replaceAll("\\", "/");
  }
  return filePath;
}

async function validateImageOutPath(imageOut, exportImageTypes) {
  if (!imageOut || exportImageTypes.length <= 1) {
    return;
  }

  const resolved = path.resolve(process.cwd(), imageOut);
  const stat = await fs.stat(resolved).catch(() => null);
  if (stat?.isDirectory()) {
    return;
  }

  if (path.extname(resolved)) {
    throw new CliError(
      "When using multiple --export-image values, --image-out must point to a directory or a path without an extension",
    );
  }
}

function detectInputKind(filePath) {
  const extension = path.extname(filePath).toLowerCase();
  if (extension === ".csv") {
    return "csv";
  }
  if (extension === ".tsv" || extension === ".tab") {
    return "tsv";
  }
  if (extension === ".json") {
    return "json";
  }
  throw new CliError(`Unsupported input file type: ${extension}`);
}

function parseDelimited(text, delimiter) {
  const rows = [];
  let current = "";
  let row = [];
  let inQuotes = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (char === '"') {
      if (inQuotes && next === '"') {
        current += '"';
        index += 1;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }

    if (!inQuotes && char === delimiter) {
      row.push(current);
      current = "";
      continue;
    }

    if (!inQuotes && (char === "\n" || char === "\r")) {
      if (char === "\r" && next === "\n") {
        index += 1;
      }
      row.push(current);
      current = "";
      if (row.some((cell) => cell !== "")) {
        rows.push(row);
      }
      row = [];
      continue;
    }

    current += char;
  }

  row.push(current);
  if (row.some((cell) => cell !== "")) {
    rows.push(row);
  }

  return rows;
}

function coerceCell(value) {
  const trimmed = String(value).trim();
  if (trimmed === "") {
    return null;
  }
  const maybeNumber = Number(trimmed);
  return Number.isFinite(maybeNumber) && /^[-+]?\d*\.?\d+(e[-+]?\d+)?$/i.test(trimmed)
    ? maybeNumber
    : trimmed;
}

function normalizeHeader(header, index) {
  const cleaned = String(header ?? "").trim();
  return cleaned || `column_${index + 1}`;
}

async function readDelimitedRows(filePath, delimiter) {
  const text = await fs.readFile(filePath, "utf8");
  const records = parseDelimited(text, delimiter);
  if (records.length < 2) {
    throw new CliError(`Expected a header row and at least one data row in ${filePath}`);
  }

  const headers = records[0].map(normalizeHeader);
  return records.slice(1).map((cells) => {
    const row = {};
    for (let index = 0; index < headers.length; index += 1) {
      row[headers[index]] = coerceCell(cells[index] ?? "");
    }
    return row;
  });
}

function extractRowsFromJson(value) {
  if (Array.isArray(value)) {
    return value;
  }
  if (value && typeof value === "object") {
    for (const key of ["rows", "data", "items"]) {
      if (Array.isArray(value[key])) {
        return value[key];
      }
    }
  }
  throw new CliError(
    "JSON input must be an array of objects or an object containing rows, data, or items",
  );
}

async function readRows(inputPath) {
  const inputKind = detectInputKind(inputPath);
  if (inputKind === "csv") {
    return readDelimitedRows(inputPath, ",");
  }
  if (inputKind === "tsv") {
    return readDelimitedRows(inputPath, "\t");
  }

  const raw = await fs.readFile(inputPath, "utf8");
  const parsed = JSON.parse(raw);
  const rows = extractRowsFromJson(parsed);
  if (!rows.every((row) => row && typeof row === "object" && !Array.isArray(row))) {
    throw new CliError("JSON rows must be objects");
  }
  return rows;
}

function extractOptionTitle(option) {
  const title = Array.isArray(option.title) ? option.title[0] : option.title;
  return title && typeof title === "object" ? (title.text ?? "") : "";
}

function extractOptionSubtitle(option) {
  const title = Array.isArray(option.title) ? option.title[0] : option.title;
  return title && typeof title === "object" ? (title.subtext ?? "") : "";
}

async function readOption(optionPath) {
  const raw = await fs.readFile(optionPath, "utf8");
  return JSON.parse(raw);
}

function applyOptionDefaults(option, common, fallbackChart) {
  const nextOption = sanitizeObject(option);
  nextOption.color ??= resolvePalette(common.theme);
  nextOption.backgroundColor ??= "transparent";
  nextOption.aria ??= { enabled: true };

  const desiredTitle = common.title || extractOptionTitle(nextOption);
  const desiredSubtitle = common.subtitle || extractOptionSubtitle(nextOption);
  if (desiredTitle || desiredSubtitle) {
    nextOption.title = withTitle(desiredTitle, desiredSubtitle);
  }

  return {
    chart: fallbackChart,
    option: nextOption,
    title: desiredTitle,
    subtitle: desiredSubtitle,
  };
}
function buildFromSample(flags, common) {
  const chart = parseEnum(requireFlag(flags, "chart"), CHART_TYPES, "chart");
  const sortMode = parseEnum(getLast(flags, "sort", "none"), SORT_MODES, "sort mode");

  if (["pie", "rosePie", "funnel", "treemap", "sunburst", "tree"].includes(chart)) {
    const labels = parseCsvList(requireFlag(flags, "labels"));
    const values = parseCsvList(requireFlag(flags, "values")).map((value, index) =>
      parseNumber(value, `${chart} value ${index + 1}`),
    );
    if (labels.length !== values.length) {
      throw new CliError("--labels and --values must have the same length");
    }

    const parents = getLast(flags, "parents") ? parseCsvList(requireFlag(flags, "parents")) : [];
    if (parents.length > 0 && parents.length !== labels.length) {
      throw new CliError("--parents must match the length of --labels when provided");
    }

    const rows = labels.map((label, index) => ({
      label,
      value: values[index],
      parent: parents[index] ?? null,
    }));
    const parentField = parents.length > 0 ? "parent" : null;

    if (chart === "pie") {
      const donut = parseBooleanFlag(flags, "donut");
      return {
        chart,
        rows,
        spec: {
          chart,
          mode: "sample",
          labelField: "label",
          valueField: "value",
          donut,
          sortMode,
        },
        option: buildPieOption({
          rows,
          labelField: "label",
          valueField: "value",
          donut,
          title: common.title,
          subtitle: common.subtitle,
          sortMode,
          theme: common.theme,
        }),
      };
    }

    if (chart === "rosePie") {
      return {
        chart,
        rows,
        spec: {
          chart,
          mode: "sample",
          labelField: "label",
          valueField: "value",
          sortMode,
        },
        option: buildRosePieOption({
          rows,
          labelField: "label",
          valueField: "value",
          title: common.title,
          subtitle: common.subtitle,
          sortMode,
          theme: common.theme,
        }),
      };
    }

    if (chart === "funnel") {
      return {
        chart,
        rows,
        spec: {
          chart,
          mode: "sample",
          labelField: "label",
          valueField: "value",
          sortMode,
        },
        option: buildFunnelOption({
          rows,
          labelField: "label",
          valueField: "value",
          title: common.title,
          subtitle: common.subtitle,
          sortMode,
          theme: common.theme,
        }),
      };
    }

    if (chart === "sunburst") {
      return {
        chart,
        rows,
        spec: {
          chart,
          mode: "sample",
          labelField: "label",
          valueField: "value",
          parentField,
        },
        option: buildSunburstOption({
          rows,
          labelField: "label",
          valueField: "value",
          parentField,
          title: common.title,
          subtitle: common.subtitle,
          theme: common.theme,
        }),
      };
    }

    if (chart === "tree") {
      return {
        chart,
        rows,
        spec: {
          chart,
          mode: "sample",
          labelField: "label",
          valueField: "value",
          parentField,
        },
        option: buildTreeOption({
          rows,
          labelField: "label",
          valueField: "value",
          parentField,
          title: common.title,
          subtitle: common.subtitle,
          theme: common.theme,
        }),
      };
    }

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        labelField: "label",
        valueField: "value",
        parentField,
      },
      option: buildTreemapOption({
        rows,
        labelField: "label",
        valueField: "value",
        parentField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "gauge") {
    const values = parseCsvList(requireFlag(flags, "values")).map((value, index) =>
      parseNumber(value, `gauge value ${index + 1}`),
    );
    const labels = getLast(flags, "labels")
      ? parseCsvList(requireFlag(flags, "labels"))
      : values.map((_value, index) =>
          values.length === 1 ? common.title || "Value" : `Gauge ${index + 1}`,
        );
    if (labels.length !== values.length) {
      throw new CliError("--labels and --values must have the same length");
    }

    const maxes = getLast(flags, "maxes")
      ? parseCsvList(requireFlag(flags, "maxes")).map((value, index) =>
          parseNumber(value, `gauge max ${index + 1}`),
        )
      : [];
    if (maxes.length > 0 && maxes.length !== values.length) {
      throw new CliError("--maxes must match the length of --values when provided");
    }

    const maxValue = getLast(flags, "max-value")
      ? parseNumber(requireFlag(flags, "max-value"), "max-value")
      : null;
    const rows = labels.map((label, index) => ({
      label,
      value: values[index],
      max: maxes[index] ?? null,
    }));
    const maxField = maxes.length > 0 ? "max" : null;

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        labelField: "label",
        valueField: "value",
        maxField,
        maxValue,
      },
      option: buildGaugeOption({
        rows,
        labelField: "label",
        valueField: "value",
        maxField,
        maxValue,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "heatmap") {
    const xCategories = parseCsvList(requireFlag(flags, "x-categories"));
    const yCategories = parseCsvList(requireFlag(flags, "y-categories"));
    const matrix = parseMatrix(
      requireFlag(flags, "matrix"),
      xCategories.length,
      yCategories.length,
    );
    const rows = [];

    for (let yIndex = 0; yIndex < yCategories.length; yIndex += 1) {
      for (let xIndex = 0; xIndex < xCategories.length; xIndex += 1) {
        rows.push({
          x: xCategories[xIndex],
          y: yCategories[yIndex],
          value: matrix[yIndex][xIndex],
        });
      }
    }

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        xField: "x",
        yField: "y",
        valueField: "value",
      },
      option: buildHeatmapOption({
        rows,
        xField: "x",
        yField: "y",
        valueField: "value",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "waterfall") {
    const categories = parseCsvList(requireFlag(flags, "categories"));
    const values = parseCsvList(requireFlag(flags, "values")).map((value, index) =>
      parseNumber(value, `waterfall value ${index + 1}`),
    );
    if (categories.length !== values.length) {
      throw new CliError("--categories and --values must have the same length");
    }

    const rows = categories.map((category, index) => ({
      category,
      value: values[index],
    }));

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        xField: "category",
        valueField: "value",
      },
      option: buildWaterfallOption({
        rows,
        xField: "category",
        valueField: "value",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "calendar") {
    const dates = parseCsvList(requireFlag(flags, "dates")).map((value, index) =>
      normalizeDateValue(value, `date ${index + 1}`),
    );
    const values = parseCsvList(requireFlag(flags, "values")).map((value, index) =>
      parseNumber(value, `calendar value ${index + 1}`),
    );
    if (dates.length !== values.length) {
      throw new CliError("--dates and --values must have the same length");
    }

    const rows = dates.map((date, index) => ({
      date,
      value: values[index],
    }));

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        dateField: "date",
        valueField: "value",
      },
      option: buildCalendarOption({
        rows,
        dateField: "date",
        valueField: "value",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "themeRiver") {
    const dates = parseCsvList(requireFlag(flags, "dates")).map((value, index) =>
      normalizeDateValue(value, `date ${index + 1}`),
    );
    const seriesArgs = getAll(flags, "series");
    if (seriesArgs.length === 0) {
      throw new CliError("ThemeRiver sample mode requires at least one --series Name:1,2,3");
    }

    const rows = [];
    for (const [seriesIndex, entry] of seriesArgs.entries()) {
      const series = parseSeriesDefinition(entry, seriesIndex);
      if (series.values.length !== dates.length) {
        throw new CliError(`ThemeRiver series ${series.name} must have ${dates.length} values`);
      }
      for (let valueIndex = 0; valueIndex < dates.length; valueIndex += 1) {
        rows.push({
          date: dates[valueIndex],
          value: series.values[valueIndex],
          name: series.name,
        });
      }
    }

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        dateField: "date",
        valueField: "value",
        seriesField: "name",
      },
      option: buildThemeRiverOption({
        rows,
        dateField: "date",
        valueField: "value",
        seriesField: "name",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }
  if (chart === "candlestick") {
    const categories = parseCsvList(requireFlag(flags, "categories"));
    const tuples = parseTupleList(requireFlag(flags, "ohlc"), 4, "ohlc");
    if (categories.length !== tuples.length) {
      throw new CliError("--categories and --ohlc must describe the same number of points");
    }

    const rows = categories.map((category, index) => ({
      category,
      open: tuples[index][0],
      close: tuples[index][1],
      low: tuples[index][2],
      high: tuples[index][3],
    }));

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        xField: "category",
        openField: "open",
        closeField: "close",
        lowField: "low",
        highField: "high",
        sortMode,
      },
      option: buildCandlestickOption({
        rows,
        xField: "category",
        openField: "open",
        closeField: "close",
        lowField: "low",
        highField: "high",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        sortMode,
      }),
    };
  }

  if (chart === "boxplot") {
    const categories = parseCsvList(requireFlag(flags, "categories"));
    const boxes = parseTupleList(requireFlag(flags, "boxes"), 5, "box");
    if (categories.length !== boxes.length) {
      throw new CliError("--categories and --boxes must describe the same number of points");
    }

    const rows = categories.map((category, index) => ({
      category,
      low: boxes[index][0],
      q1: boxes[index][1],
      median: boxes[index][2],
      q3: boxes[index][3],
      high: boxes[index][4],
    }));

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        xField: "category",
        lowField: "low",
        q1Field: "q1",
        medianField: "median",
        q3Field: "q3",
        highField: "high",
        sortMode,
      },
      option: buildBoxplotOption({
        rows,
        xField: "category",
        lowField: "low",
        q1Field: "q1",
        medianField: "median",
        q3Field: "q3",
        highField: "high",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        sortMode,
      }),
    };
  }

  if (chart === "sankey") {
    const linkArgs = getAll(flags, "link");
    const linkDefinitions =
      linkArgs.length > 0 ? linkArgs : parseCsvList(requireFlag(flags, "links"));
    if (linkDefinitions.length === 0) {
      throw new CliError("Sankey sample mode requires --links or repeated --link values");
    }

    const rows = linkDefinitions.map((entry, index) => parseLinkDefinition(entry, index));

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        sourceField: "source",
        targetField: "target",
        valueField: "value",
      },
      option: buildSankeyOption({
        rows,
        sourceField: "source",
        targetField: "target",
        valueField: "value",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "graph") {
    const linkArgs = getAll(flags, "link");
    const linkDefinitions =
      linkArgs.length > 0 ? linkArgs : parseCsvList(requireFlag(flags, "links"));
    if (linkDefinitions.length === 0) {
      throw new CliError("Graph sample mode requires --links or repeated --link values");
    }

    const nodeArgs = getAll(flags, "node");
    const nodeDefinitions =
      nodeArgs.length > 0
        ? nodeArgs
        : getLast(flags, "nodes")
          ? parseCsvList(requireFlag(flags, "nodes"))
          : [];
    const rows = linkDefinitions.map((entry, index) => parseLinkDefinition(entry, index));
    const nodes = nodeDefinitions.map((entry, index) => parseNodeDefinition(entry, index));

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        sourceField: "source",
        targetField: "target",
        valueField: "value",
        nodeCount: nodes.length,
      },
      option: buildGraphOption({
        rows,
        sourceField: "source",
        targetField: "target",
        valueField: "value",
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        nodes,
      }),
    };
  }

  if (chart === "parallel") {
    const dimensions = parseCsvList(requireFlag(flags, "dimensions"));
    const seriesArgs = getAll(flags, "series");
    if (seriesArgs.length === 0) {
      throw new CliError("Parallel sample mode requires at least one --series Name:1,2,3");
    }

    const dimensionFields = dimensions.map((dimension) => toFieldKey(dimension));
    const fieldLabels = Object.fromEntries(
      dimensions.map((dimension, index) => [dimensionFields[index], dimension]),
    );

    const rows = seriesArgs.map((entry, index) => {
      const series = parseSeriesDefinition(entry, index);
      if (series.values.length !== dimensions.length) {
        throw new CliError(`Parallel series ${series.name} must have ${dimensions.length} values`);
      }
      const row = { name: series.name };
      for (let dimensionIndex = 0; dimensionIndex < dimensionFields.length; dimensionIndex += 1) {
        row[dimensionFields[dimensionIndex]] = series.values[dimensionIndex];
      }
      return row;
    });

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        nameField: "name",
        yFields: dimensionFields,
      },
      option: buildParallelOption({
        rows,
        nameField: "name",
        yFields: dimensionFields,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        fieldLabels,
      }),
    };
  }

  if (chart === "radar") {
    const indicators = parseCsvList(requireFlag(flags, "indicators"));
    const seriesArgs = getAll(flags, "series");
    if (seriesArgs.length === 0) {
      throw new CliError("Radar sample mode requires at least one --series Name:1,2,3");
    }

    const indicatorFields = indicators.map((indicator) => toFieldKey(indicator));
    const fieldLabels = Object.fromEntries(
      indicators.map((indicator, index) => [indicatorFields[index], indicator]),
    );

    const rows = seriesArgs.map((entry, index) => {
      const series = parseSeriesDefinition(entry, index);
      if (series.values.length !== indicators.length) {
        throw new CliError(`Radar series ${series.name} must have ${indicators.length} values`);
      }
      const row = { name: series.name };
      for (let indicatorIndex = 0; indicatorIndex < indicatorFields.length; indicatorIndex += 1) {
        row[indicatorFields[indicatorIndex]] = series.values[indicatorIndex];
      }
      return row;
    });

    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "sample",
        nameField: "name",
        yFields: indicatorFields,
      },
      option: buildRadarOption({
        rows,
        nameField: "name",
        yFields: indicatorFields,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        fieldLabels,
      }),
    };
  }

  if (!["bar", "line", "area", "pictorialBar", "polarBar"].includes(chart)) {
    throw new CliError(`Sample mode does not support ${chart}; use table or page mode instead`);
  }

  const categories = parseCsvList(requireFlag(flags, "categories"));
  const seriesArgs = getAll(flags, "series");
  const seriesDefinitions =
    seriesArgs.length > 0
      ? seriesArgs.map((entry, index) => parseSeriesDefinition(entry, index))
      : [
          {
            name: "Value",
            key: "value",
            values: parseCsvList(requireFlag(flags, "values")).map((value, index) =>
              parseNumber(value, `value ${index + 1}`),
            ),
          },
        ];

  for (const series of seriesDefinitions) {
    if (series.values.length !== categories.length) {
      throw new CliError(`Series ${series.name} must contain ${categories.length} values`);
    }
  }

  const rows = categories.map((category, index) => {
    const row = { category };
    for (const series of seriesDefinitions) {
      row[series.key] = series.values[index];
    }
    return row;
  });

  const fieldLabels = Object.fromEntries(
    seriesDefinitions.map((series) => [series.key, series.name]),
  );

  return {
    chart,
    rows,
    spec: {
      chart,
      mode: "sample",
      xField: "category",
      yFields: seriesDefinitions.map((series) => series.key),
      smooth: parseBooleanFlag(flags, "smooth"),
      stack: parseBooleanFlag(flags, "stack"),
      horizontal: parseBooleanFlag(flags, "horizontal"),
      sortMode,
    },
    option:
      chart === "pictorialBar"
        ? buildPictorialBarOption({
            rows,
            xField: "category",
            yFields: seriesDefinitions.map((series) => series.key),
            title: common.title,
            subtitle: common.subtitle,
            horizontal: parseBooleanFlag(flags, "horizontal"),
            sortMode,
            theme: common.theme,
            fieldLabels,
          })
        : chart === "polarBar"
          ? buildPolarBarOption({
              rows,
              xField: "category",
              yFields: seriesDefinitions.map((series) => series.key),
              title: common.title,
              subtitle: common.subtitle,
              sortMode,
              theme: common.theme,
              fieldLabels,
            })
          : buildCartesianOption({
              rows,
              chart,
              xField: "category",
              yFields: seriesDefinitions.map((series) => series.key),
              title: common.title,
              subtitle: common.subtitle,
              smooth: parseBooleanFlag(flags, "smooth"),
              stack: parseBooleanFlag(flags, "stack"),
              horizontal: parseBooleanFlag(flags, "horizontal"),
              sortMode,
              theme: common.theme,
              fieldLabels,
            }),
  };
}

async function buildFromTable(flags, common) {
  const inputPath = path.resolve(process.cwd(), requireFlag(flags, "input"));
  const inputName = path.basename(inputPath);
  const chart = parseEnum(requireFlag(flags, "chart"), CHART_TYPES, "chart");
  const sortMode = parseEnum(getLast(flags, "sort", "none"), SORT_MODES, "sort mode");
  const rows = await readRows(inputPath);

  if (["bar", "line", "area", "pictorialBar", "polarBar"].includes(chart)) {
    const xField = requireFlag(flags, "x");
    const yFields = parseCsvList(requireFlag(flags, "y"));
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        xField,
        yFields,
        smooth: parseBooleanFlag(flags, "smooth"),
        stack: parseBooleanFlag(flags, "stack"),
        horizontal: parseBooleanFlag(flags, "horizontal"),
        sortMode,
      },
      option:
        chart === "pictorialBar"
          ? buildPictorialBarOption({
              rows,
              xField,
              yFields,
              title: common.title,
              subtitle: common.subtitle,
              horizontal: parseBooleanFlag(flags, "horizontal"),
              sortMode,
              theme: common.theme,
            })
          : chart === "polarBar"
            ? buildPolarBarOption({
                rows,
                xField,
                yFields,
                title: common.title,
                subtitle: common.subtitle,
                sortMode,
                theme: common.theme,
              })
            : buildCartesianOption({
                rows,
                chart,
                xField,
                yFields,
                title: common.title,
                subtitle: common.subtitle,
                smooth: parseBooleanFlag(flags, "smooth"),
                stack: parseBooleanFlag(flags, "stack"),
                horizontal: parseBooleanFlag(flags, "horizontal"),
                sortMode,
                theme: common.theme,
              }),
    };
  }

  if (["pie", "rosePie"].includes(chart)) {
    const labelField = requireFlag(flags, "label");
    const valueField = requireFlag(flags, "value");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        labelField,
        valueField,
        donut: parseBooleanFlag(flags, "donut"),
        sortMode,
      },
      option:
        chart === "rosePie"
          ? buildRosePieOption({
              rows,
              labelField,
              valueField,
              title: common.title,
              subtitle: common.subtitle,
              sortMode,
              theme: common.theme,
            })
          : buildPieOption({
              rows,
              labelField,
              valueField,
              donut: parseBooleanFlag(flags, "donut"),
              title: common.title,
              subtitle: common.subtitle,
              sortMode,
              theme: common.theme,
            }),
    };
  }

  if (chart === "scatter") {
    const xField = requireFlag(flags, "x");
    const yField = requireFlag(flags, "y");
    const seriesField = getLast(flags, "series-field");
    const sizeField = getLast(flags, "size-field");
    const labelField = getLast(flags, "label-field");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        xField,
        yField,
        seriesField,
        sizeField,
        labelField,
        sortMode,
      },
      option: buildScatterOption({
        rows,
        xField,
        yField,
        seriesField,
        sizeField,
        labelField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        sortMode,
      }),
    };
  }

  if (chart === "heatmap") {
    const xField = requireFlag(flags, "x");
    const yField = requireFlag(flags, "y");
    const valueField = requireFlag(flags, "value");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        xField,
        yField,
        valueField,
      },
      option: buildHeatmapOption({
        rows,
        xField,
        yField,
        valueField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "waterfall") {
    const xField = requireFlag(flags, "x");
    const valueField = requireFlag(flags, "value");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: inputName,
        xField,
        valueField,
      },
      option: buildWaterfallOption({
        rows,
        xField,
        valueField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "calendar") {
    const dateField = requireFlag(flags, "date");
    const valueField = requireFlag(flags, "value");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: inputName,
        dateField,
        valueField,
      },
      option: buildCalendarOption({
        rows,
        dateField,
        valueField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "themeRiver") {
    const dateField = requireFlag(flags, "date");
    const valueField = requireFlag(flags, "value");
    const seriesField = requireFlag(flags, "series-field");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: inputName,
        dateField,
        valueField,
        seriesField,
      },
      option: buildThemeRiverOption({
        rows,
        dateField,
        valueField,
        seriesField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "funnel") {
    const labelField = requireFlag(flags, "label");
    const valueField = requireFlag(flags, "value");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: inputName,
        labelField,
        valueField,
        sortMode,
      },
      option: buildFunnelOption({
        rows,
        labelField,
        valueField,
        title: common.title,
        subtitle: common.subtitle,
        sortMode,
        theme: common.theme,
      }),
    };
  }

  if (chart === "gauge") {
    const labelField = getLast(flags, "label");
    const valueField = requireFlag(flags, "value");
    const maxField = getLast(flags, "max-field");
    const maxValue = getLast(flags, "max-value")
      ? parseNumber(requireFlag(flags, "max-value"), "max-value")
      : null;
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: inputName,
        labelField,
        valueField,
        maxField,
        maxValue,
      },
      option: buildGaugeOption({
        rows,
        labelField,
        valueField,
        maxField,
        maxValue,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (["treemap", "sunburst", "tree"].includes(chart)) {
    const labelField = requireFlag(flags, "label");
    const valueField = requireFlag(flags, "value");
    const parentField = getLast(flags, "parent-field");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: inputName,
        labelField,
        valueField,
        parentField,
      },
      option:
        chart === "sunburst"
          ? buildSunburstOption({
              rows,
              labelField,
              valueField,
              parentField,
              title: common.title,
              subtitle: common.subtitle,
              theme: common.theme,
            })
          : chart === "tree"
            ? buildTreeOption({
                rows,
                labelField,
                valueField,
                parentField,
                title: common.title,
                subtitle: common.subtitle,
                theme: common.theme,
              })
            : buildTreemapOption({
                rows,
                labelField,
                valueField,
                parentField,
                title: common.title,
                subtitle: common.subtitle,
                theme: common.theme,
              }),
    };
  }

  if (chart === "candlestick") {
    const xField = requireFlag(flags, "x");
    const openField = requireFlag(flags, "open");
    const closeField = requireFlag(flags, "close");
    const lowField = requireFlag(flags, "low");
    const highField = requireFlag(flags, "high");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        xField,
        openField,
        closeField,
        lowField,
        highField,
        sortMode,
      },
      option: buildCandlestickOption({
        rows,
        xField,
        openField,
        closeField,
        lowField,
        highField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        sortMode,
      }),
    };
  }

  if (chart === "boxplot") {
    const xField = requireFlag(flags, "x");
    const lowField = requireFlag(flags, "low");
    const q1Field = requireFlag(flags, "q1");
    const medianField = requireFlag(flags, "median");
    const q3Field = requireFlag(flags, "q3");
    const highField = requireFlag(flags, "high");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        xField,
        lowField,
        q1Field,
        medianField,
        q3Field,
        highField,
        sortMode,
      },
      option: buildBoxplotOption({
        rows,
        xField,
        lowField,
        q1Field,
        medianField,
        q3Field,
        highField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
        sortMode,
      }),
    };
  }

  if (chart === "sankey") {
    const sourceField = requireFlag(flags, "source");
    const targetField = requireFlag(flags, "target");
    const valueField = requireFlag(flags, "value");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        sourceField,
        targetField,
        valueField,
      },
      option: buildSankeyOption({
        rows,
        sourceField,
        targetField,
        valueField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "graph") {
    const sourceField = requireFlag(flags, "source");
    const targetField = requireFlag(flags, "target");
    const valueField = getLast(flags, "value");
    const sourceGroupField = getLast(flags, "source-group");
    const targetGroupField = getLast(flags, "target-group");
    const sourceSizeField = getLast(flags, "source-size");
    const targetSizeField = getLast(flags, "target-size");
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        sourceField,
        targetField,
        valueField,
        sourceGroupField,
        targetGroupField,
        sourceSizeField,
        targetSizeField,
      },
      option: buildGraphOption({
        rows,
        sourceField,
        targetField,
        valueField,
        sourceGroupField,
        targetGroupField,
        sourceSizeField,
        targetSizeField,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  if (chart === "parallel") {
    const nameField = requireFlag(flags, "name-field");
    const yFields = parseCsvList(requireFlag(flags, "y"));
    return {
      chart,
      rows,
      spec: {
        chart,
        mode: "table",
        input: path.basename(inputPath),
        nameField,
        yFields,
      },
      option: buildParallelOption({
        rows,
        nameField,
        yFields,
        title: common.title,
        subtitle: common.subtitle,
        theme: common.theme,
      }),
    };
  }

  const nameField = requireFlag(flags, "name-field");
  const yFields = parseCsvList(requireFlag(flags, "y"));
  return {
    chart,
    rows,
    spec: {
      chart,
      mode: "table",
      input: path.basename(inputPath),
      nameField,
      yFields,
    },
    option: buildRadarOption({
      rows,
      nameField,
      yFields,
      title: common.title,
      subtitle: common.subtitle,
      theme: common.theme,
    }),
  };
}
async function buildFromPage(flags, common) {
  const optionPath = path.resolve(process.cwd(), requireFlag(flags, "option"));
  const option = await readOption(optionPath);
  const firstSeries = Array.isArray(option.series) ? option.series[0] : option.series;
  const chart = firstSeries?.type ?? "custom";
  const normalized = applyOptionDefaults(option, common, chart);

  return {
    chart: normalized.chart,
    rows: null,
    spec: {
      chart: normalized.chart,
      mode: "page",
      input: path.basename(optionPath),
    },
    option: normalized.option,
    title: normalized.title,
    subtitle: normalized.subtitle,
  };
}

async function writeArtifacts(result, common) {
  await fs.mkdir(common.outDir, { recursive: true });

  const template = await loadTemplate();
  const finalTitle = result.title ?? common.title;
  const finalSubtitle = result.subtitle ?? common.subtitle;
  const fileBase = toSlug(finalTitle || result.chart || "echarts-chart");
  const generatedAt = new Date().toISOString();

  const manifest = {
    createdAt: generatedAt,
    mode: result.spec.mode,
    chart: result.chart,
    theme: common.theme,
    renderer: common.renderer,
    pageMode: common.pageMode,
    files: {
      spec: "chart.spec.json",
      option: "chart.option.json",
      data: result.rows ? "chart.data.json" : null,
      html: "chart.html",
    },
  };

  const bootstrap = {
    title: finalTitle || humanize(result.chart),
    subtitle: finalSubtitle || "",
    notes: common.notes,
    width: common.width,
    height: common.height,
    renderer: common.renderer,
    theme: common.theme,
    pageMode: common.pageMode,
    cdnUrl: common.cdnUrl,
    fileBase,
    generatedAt,
    chart: result.chart,
    option: result.option,
    manifest,
  };

  const specPath = path.join(common.outDir, "chart.spec.json");
  const optionPath = path.join(common.outDir, "chart.option.json");
  const dataPath = path.join(common.outDir, "chart.data.json");
  const htmlPath = path.join(common.outDir, "chart.html");
  const manifestPath = path.join(common.outDir, "manifest.json");

  await writeJson(specPath, {
    ...result.spec,
    title: bootstrap.title,
    subtitle: bootstrap.subtitle,
    theme: common.theme,
    renderer: common.renderer,
    pageMode: common.pageMode,
    width: common.width,
    height: common.height,
    noteCount: common.notes.length,
  });
  await writeJson(optionPath, result.option);
  if (result.rows) {
    await writeJson(dataPath, result.rows);
  }
  await fs.writeFile(htmlPath, renderHtml(template, bootstrap), "utf8");
  await writeJson(manifestPath, manifest);

  logWrite(specPath);
  logWrite(optionPath);
  if (result.rows) {
    logWrite(dataPath);
  }
  logWrite(htmlPath);
  logWrite(manifestPath);

  return {
    bootstrap,
    manifest,
    manifestPath,
    htmlPath,
  };
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (parsed.help) {
    printUsage();
    return;
  }

  const common = resolveCommon(parsed.flags);
  let result;

  switch (parsed.mode) {
    case "sample":
      result = buildFromSample(parsed.flags, common);
      break;
    case "table":
      result = await buildFromTable(parsed.flags, common);
      break;
    case "page":
      result = await buildFromPage(parsed.flags, common);
      break;
    default:
      throw new CliError(`Unknown mode: ${parsed.mode}`);
  }

  if (common.exportImageTypes.includes("svg") && common.renderer !== "svg") {
    throw new CliError("--export-image svg requires --renderer svg");
  }

  await validateImageOutPath(common.imageOut, common.exportImageTypes);

  const artifacts = await writeArtifacts(result, common);
  if (common.exportImageTypes.length > 0) {
    const imageRefs = [];

    for (const exportImageType of common.exportImageTypes) {
      const rendered = await renderArtifactImage({
        inputPath: common.outDir,
        type: exportImageType,
        outPath: common.imageOut,
        browserExecutable: common.browserExecutable,
        pixelRatio: common.imagePixelRatio,
        background: common.imageBackground,
      });
      imageRefs.push(toManifestFileRef(common.outDir, rendered.outputPath));
    }

    if (imageRefs.length === 1) {
      artifacts.manifest.files.image = imageRefs[0];
    }
    if (imageRefs.length > 1) {
      artifacts.manifest.files.images = imageRefs;
    }

    await writeJson(artifacts.manifestPath, artifacts.manifest);
    logWrite(artifacts.manifestPath);
  }
}

main().catch((error) => {
  if (error instanceof CliError) {
    console.error(`[error] ${error.message}`);
    console.error("");
    printUsage();
    process.exitCode = 1;
    return;
  }

  console.error(error);
  process.exitCode = 1;
});
