#!/usr/bin/env node

import { appendFileSync, chmodSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import * as echarts from "echarts";
import sharp from "sharp";
import pino from "pino";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc.js";
import timezone from "dayjs/plugin/timezone.js";

const DEFAULT_WIDTH = 1200;
const DEFAULT_HEIGHT = 800;
const SKILL_NAME = "aios-make-chart-image";
const SUPPORTED_FORMATS = new Set(["png", "svg", "jpg", "jpeg", "webp"]);
const OPTION_KEYS = new Set([
  "series",
  "xAxis",
  "yAxis",
  "dataset",
  "radar",
  "geo",
  "calendar",
  "grid",
  "polar",
  "angleAxis",
  "radiusAxis"
]);

const PALETTE = [
  "#2563eb",
  "#16a34a",
  "#dc2626",
  "#9333ea",
  "#ea580c",
  "#0891b2",
  "#be123c",
  "#4f46e5",
  "#65a30d",
  "#c2410c"
];

dayjs.extend(utc);
dayjs.extend(timezone);

const warnedLogDirs = new Set();

function beijingTime() {
  return dayjs().tz("Asia/Shanghai").format("YYYY-MM-DDTHH:mm:ss.SSSZ");
}

function resolveLogDir() {
  const configured = process.env.AIOS_LOG_DIR?.trim();
  if (configured) {
    return configured;
  }

  const root = process.env.AIOS_ROOT?.trim();
  if (root) {
    return path.join(root, "logs");
  }

  const dataDir = process.env.AIOS_DATA_DIR?.trim() || process.env.AIOS_KERNEL_DATA_DIR?.trim();
  if (dataDir) {
    return path.join(path.dirname(dataDir), "logs");
  }

  return undefined;
}

function getDailyLogFile() {
  const logDir = resolveLogDir();
  if (!logDir) {
    return undefined;
  }

  try {
    mkdirSync(logDir, { recursive: true });
    const logFile = path.join(logDir, `${SKILL_NAME}-${dayjs().tz("Asia/Shanghai").format("YYYYMMDD")}.log`);
    if (!existsSync(logFile)) {
      writeFileSync(logFile, "", { mode: 0o660 });
      chmodSync(logFile, 0o660);
    }
    return logFile;
  } catch (error) {
    if (!warnedLogDirs.has(logDir)) {
      warnedLogDirs.add(logDir);
      const message = error instanceof Error ? error.message : String(error);
      process.stderr.write(`[logger] ${beijingTime()} failed to initialize daily log file in ${logDir}: ${message}\n`);
    }
    return undefined;
  }
}

function createDestination() {
  return {
    write(line) {
      process.stderr.write(line);
      const logFile = getDailyLogFile();
      if (logFile) {
        appendFileSync(logFile, line, { mode: 0o660 });
      }
    }
  };
}

const logger = pino({
  name: SKILL_NAME,
  level: process.env.AIOS_LOG_LEVEL || "info",
  timestamp: () => `,"ts":"${beijingTime()}"`,
  base: null
}, createDestination());

function fail(message, code = 1) {
  logger.error({ error: { message } }, "aios-make-chart-image failed");
  process.exit(code);
}

function usage() {
  return [
    "Usage:",
    "  node scripts/make_chart_image.mjs --input data.json --output chart.png [options]",
    "  cat table.md | node scripts/make_chart_image.mjs --input - --output chart.svg",
    "",
    "Options:",
    "  --input <file|- >             JSON or Markdown input. Use - for stdin.",
    "  --data <text>                 Inline JSON or Markdown input.",
    "  --output <file>               Output image path.",
    "  --format <png|svg|jpg|webp>   Defaults to output extension.",
    "  --chart-type <auto|bar|line|pie|scatter>",
    "  --title <text>",
    "  --width <number>              Default 1200.",
    "  --height <number>             Default 800.",
    "  --x <field>                   Category or x field.",
    "  --y <field1,field2>           Numeric value fields.",
    "  --name <field>                Pie name field.",
    "  --value <field>               Pie value field.",
    "  --theme <light|dark>          Default light.",
    "  --save-option <file>          Save generated ECharts option JSON.",
    "  --help"
  ].join("\n");
}

function parseArgs(argv) {
  const args = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      fail(`Unexpected argument: ${token}`);
    }

    const eqIndex = token.indexOf("=");
    const key = eqIndex === -1 ? token.slice(2) : token.slice(2, eqIndex);
    if (!key) {
      fail(`Invalid option: ${token}`);
    }

    if (key === "help") {
      args.help = true;
      continue;
    }

    if (eqIndex !== -1) {
      args[key] = token.slice(eqIndex + 1);
      continue;
    }

    const value = argv[index + 1];
    if (value === undefined || value.startsWith("--")) {
      fail(`Missing value for --${key}`);
    }
    args[key] = value;
    index += 1;
  }

  return args;
}

function readNumberArg(args, name, fallback) {
  if (args[name] === undefined) {
    return fallback;
  }

  const value = Number(args[name]);
  if (!Number.isFinite(value) || value <= 0) {
    fail(`--${name} must be a positive number`);
  }

  return Math.round(value);
}

function deriveFormat(args) {
  const explicit = args.format?.trim().toLowerCase();
  if (explicit) {
    if (!SUPPORTED_FORMATS.has(explicit)) {
      fail(`Unsupported --format: ${args.format}`);
    }
    return explicit;
  }

  const ext = path.extname(args.output ?? "").replace(".", "").toLowerCase();
  if (!ext || !SUPPORTED_FORMATS.has(ext)) {
    fail("Unable to infer image format from --output. Pass --format png|svg|jpg|jpeg|webp.");
  }

  return ext;
}

function normalizeFormat(format) {
  return format === "jpg" ? "jpeg" : format;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8");
}

async function loadInput(args) {
  if (args.data !== undefined) {
    return {
      text: String(args.data),
      sourcePath: undefined
    };
  }

  if (!args.input) {
    fail("Missing --input or --data");
  }

  if (args.input === "-") {
    return {
      text: await readStdin(),
      sourcePath: undefined
    };
  }

  const sourcePath = path.resolve(args.input);
  return {
    text: await readFile(sourcePath, "utf8"),
    sourcePath
  };
}

function parseScalar(value) {
  const trimmed = value.trim();
  if (!trimmed) {
    return null;
  }
  if (/^(null|undefined)$/i.test(trimmed)) {
    return null;
  }
  if (/^(true|false)$/i.test(trimmed)) {
    return trimmed.toLowerCase() === "true";
  }

  const normalized = trimmed
    .replace(/^[¥￥$€£]\s*/, "")
    .replace(/\s*%$/, "")
    .replace(/,/g, "");
  if (/^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i.test(normalized)) {
    return Number(normalized);
  }

  return trimmed.replace(/<br\s*\/?>/gi, "\n");
}

function splitMarkdownRow(line) {
  let content = line.trim();
  if (content.startsWith("|")) {
    content = content.slice(1);
  }
  if (content.endsWith("|")) {
    content = content.slice(0, -1);
  }

  const cells = [];
  let current = "";
  let escaped = false;

  for (const char of content) {
    if (escaped) {
      current += char;
      escaped = false;
      continue;
    }
    if (char === "\\") {
      escaped = true;
      continue;
    }
    if (char === "|") {
      cells.push(current.trim());
      current = "";
      continue;
    }
    current += char;
  }

  cells.push(current.trim());
  return cells;
}

function isMarkdownSeparator(line) {
  const cells = splitMarkdownRow(line);
  return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell.trim()));
}

function findMarkdownTitle(text) {
  const match = text.match(/^\s{0,3}#{1,2}\s+(.+?)\s*#*\s*$/m);
  return match?.[1]?.trim();
}

function parseMarkdownTable(text) {
  const lines = text.split(/\r?\n/);

  for (let index = 0; index < lines.length - 1; index += 1) {
    if (!lines[index].includes("|") || !isMarkdownSeparator(lines[index + 1])) {
      continue;
    }

    const columns = splitMarkdownRow(lines[index]).map((cell, columnIndex) => cell || `Column ${columnIndex + 1}`);
    const rows = [];

    for (let rowIndex = index + 2; rowIndex < lines.length; rowIndex += 1) {
      const line = lines[rowIndex];
      if (!line.includes("|") || !line.trim()) {
        break;
      }

      const cells = splitMarkdownRow(line);
      if (cells.length === 0) {
        continue;
      }

      const row = {};
      columns.forEach((column, columnIndex) => {
        row[column] = parseScalar(cells[columnIndex] ?? "");
      });
      rows.push(row);
    }

    if (rows.length === 0) {
      fail("Markdown table has headers but no data rows");
    }

    return {
      kind: "table",
      rows,
      columns,
      title: findMarkdownTitle(text)
    };
  }

  fail("No Markdown table found in input");
}

function looksLikeEchartsOption(value) {
  return Boolean(
    value
    && typeof value === "object"
    && !Array.isArray(value)
    && Object.keys(value).some((key) => OPTION_KEYS.has(key))
  );
}

function parseJsonInput(text) {
  let value;
  try {
    value = JSON.parse(text);
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    fail(`Input is not valid JSON: ${reason}`);
  }

  if (looksLikeEchartsOption(value)) {
    return {
      kind: "option",
      option: value
    };
  }

  if (looksLikeEchartsOption(value?.option)) {
    return {
      kind: "option",
      option: value.option,
      title: value.title
    };
  }

  return normalizeDataInput(value);
}

function parseInput(text, sourcePath) {
  let trimmed = text.trim();
  if (!trimmed) {
    fail("Input is empty");
  }

  const ext = sourcePath ? path.extname(sourcePath).toLowerCase() : "";
  if (!sourcePath && ext !== ".json" && !trimmed.includes("\n") && trimmed.includes("\\n")) {
    trimmed = trimmed.replace(/\\r\\n/g, "\n").replace(/\\n/g, "\n");
  }

  if (ext === ".md" || ext === ".markdown") {
    return parseMarkdownTable(trimmed);
  }
  if (ext === ".json") {
    return parseJsonInput(trimmed);
  }
  if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
    return parseJsonInput(trimmed);
  }
  return parseMarkdownTable(trimmed);
}

function normalizeDataInput(value) {
  if (Array.isArray(value)) {
    return normalizeRows(value);
  }

  if (!value || typeof value !== "object") {
    fail("JSON input must be an object, an array, or an ECharts option");
  }

  if (Array.isArray(value.data)) {
    const normalized = normalizeRows(value.data);
    return {
      ...normalized,
      title: value.title,
      chartType: value.chartType ?? value.type,
      xField: value.xField ?? value.x,
      yFields: value.yFields ?? value.y,
      nameField: value.nameField ?? value.name,
      valueField: value.valueField ?? value.value
    };
  }

  if (Array.isArray(value.rows)) {
    const normalized = normalizeRows(value.rows, value.columns);
    return {
      ...normalized,
      title: value.title,
      chartType: value.chartType ?? value.type,
      xField: value.xField ?? value.x,
      yFields: value.yFields ?? value.y,
      nameField: value.nameField ?? value.name,
      valueField: value.valueField ?? value.value
    };
  }

  if (Array.isArray(value.labels) && Array.isArray(value.values)) {
    const rows = value.labels.map((label, index) => ({
      label,
      value: parseScalar(String(value.values[index] ?? ""))
    }));
    return {
      kind: "table",
      rows,
      columns: ["label", "value"],
      title: value.title,
      chartType: value.chartType ?? value.type,
      xField: "label",
      yFields: ["value"],
      nameField: "label",
      valueField: "value"
    };
  }

  const entries = Object.entries(value);
  if (entries.length > 0 && entries.every(([, entryValue]) => typeof entryValue === "number")) {
    return {
      kind: "table",
      rows: entries.map(([name, entryValue]) => ({ name, value: entryValue })),
      columns: ["name", "value"],
      xField: "name",
      yFields: ["value"],
      nameField: "name",
      valueField: "value"
    };
  }

  fail("Unsupported JSON data shape. Provide an ECharts option, an array of rows, rows/columns, or labels/values.");
}

function normalizeRows(rows, columnsHint) {
  if (rows.length === 0) {
    fail("Data rows are empty");
  }

  if (rows.every((row) => typeof row === "number")) {
    const normalizedRows = rows.map((value, index) => ({ index: index + 1, value }));
    return {
      kind: "table",
      rows: normalizedRows,
      columns: ["index", "value"],
      xField: "index",
      yFields: ["value"]
    };
  }

  if (rows.every((row) => Array.isArray(row))) {
    const first = rows[0];
    const hasHeader = first.every((cell) => typeof cell === "string");
    const columns = columnsHint ?? (hasHeader ? first : first.map((_, index) => `Column ${index + 1}`));
    const dataRows = hasHeader && !columnsHint ? rows.slice(1) : rows;
    const normalizedRows = dataRows.map((row) => {
      const record = {};
      columns.forEach((column, index) => {
        record[String(column)] = typeof row[index] === "string" ? parseScalar(row[index]) : row[index] ?? null;
      });
      return record;
    });

    return {
      kind: "table",
      rows: normalizedRows,
      columns: columns.map(String)
    };
  }

  if (rows.every((row) => row && typeof row === "object" && !Array.isArray(row))) {
    const discoveredColumns = [];
    for (const row of rows) {
      for (const key of Object.keys(row)) {
        if (!discoveredColumns.includes(key)) {
          discoveredColumns.push(key);
        }
      }
    }
    const columns = columnsHint?.map(String) ?? discoveredColumns;
    const normalizedRows = rows.map((row) => {
      const record = {};
      columns.forEach((column) => {
        const value = row[column];
        record[column] = typeof value === "string" ? parseScalar(value) : value ?? null;
      });
      return record;
    });
    return {
      kind: "table",
      rows: normalizedRows,
      columns
    };
  }

  fail("Rows must be numbers, arrays, or objects");
}

function unique(values) {
  return [...new Set(values)];
}

function hasNumericValue(rows, field) {
  return rows.some((row) => typeof row[field] === "number" && Number.isFinite(row[field]));
}

function numericFields(rows, columns) {
  return columns.filter((column) => hasNumericValue(rows, column));
}

function firstNonNumericField(rows, columns) {
  return columns.find((column) => !hasNumericValue(rows, column)) ?? columns[0];
}

function splitList(value) {
  if (Array.isArray(value)) {
    return value.map(String).filter(Boolean);
  }
  if (typeof value === "string") {
    return value.split(",").map((item) => item.trim()).filter(Boolean);
  }
  if (value === undefined || value === null) {
    return undefined;
  }
  return [String(value)];
}

function inferChartType({ requested, rows, columns, xField, yFields }) {
  if (requested && requested !== "auto") {
    return requested;
  }

  if (yFields.length === 1 && rows.length <= 12) {
    return "bar";
  }

  const sampleX = rows.find((row) => row[xField] !== null && row[xField] !== undefined)?.[xField];
  if (typeof sampleX === "string" && /^\d{4}[-/]\d{1,2}([-/]\d{1,2})?/.test(sampleX)) {
    return "line";
  }

  if (columns.length >= 2 && yFields.length > 1) {
    return "line";
  }

  return "bar";
}

function ensureField(columns, field, optionName) {
  if (!field) {
    return;
  }
  if (!columns.includes(field)) {
    fail(`${optionName} field "${field}" was not found. Available fields: ${columns.join(", ")}`);
  }
}

function valueOrNull(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function commonOption({ title, subtitle, theme }) {
  const dark = theme === "dark";
  return {
    backgroundColor: dark ? "#0f172a" : "#ffffff",
    color: PALETTE,
    textStyle: {
      fontFamily: "Arial, Helvetica, sans-serif",
      color: dark ? "#e5e7eb" : "#111827"
    },
    title: title ? {
      text: title,
      subtext: subtitle,
      left: "center",
      top: 24,
      textStyle: {
        fontSize: 24,
        fontWeight: 700,
        color: dark ? "#f8fafc" : "#111827"
      },
      subtextStyle: {
        color: dark ? "#cbd5e1" : "#64748b"
      }
    } : undefined,
    tooltip: {},
    legend: {
      type: "scroll",
      top: title ? 76 : 24,
      textStyle: {
        color: dark ? "#e5e7eb" : "#374151"
      }
    }
  };
}

function buildOptionFromTable(input, args) {
  const rows = input.rows;
  const columns = input.columns;
  const requestedType = (args["chart-type"] ?? input.chartType ?? "auto").toLowerCase();
  if (!["auto", "bar", "line", "pie", "scatter"].includes(requestedType)) {
    fail(`Unsupported --chart-type: ${requestedType}`);
  }

  const theme = (args.theme ?? "light").toLowerCase();
  if (!["light", "dark"].includes(theme)) {
    fail("--theme must be light or dark");
  }

  const title = args.title ?? input.title;
  const base = commonOption({ title, theme });
  const numeric = numericFields(rows, columns);
  const xField = args.x ?? input.xField ?? firstNonNumericField(rows, columns);
  const yFields = splitList(args.y ?? input.yFields) ?? numeric.filter((field) => field !== xField);
  const nameField = args.name ?? input.nameField ?? firstNonNumericField(rows, columns);
  const valueField = args.value ?? input.valueField ?? yFields[0] ?? numeric[0];

  ensureField(columns, xField, "--x");
  yFields.forEach((field) => ensureField(columns, field, "--y"));
  ensureField(columns, nameField, "--name");
  ensureField(columns, valueField, "--value");

  const chartType = inferChartType({
    requested: requestedType,
    rows,
    columns,
    xField,
    yFields
  });

  if (chartType === "pie") {
    if (!nameField || !valueField) {
      fail("Pie charts require a name field and a value field");
    }
    return {
      option: {
        ...base,
        tooltip: { trigger: "item" },
        legend: {
          ...base.legend,
          orient: "vertical",
          right: 28,
          top: "middle"
        },
        series: [{
          name: valueField,
          type: "pie",
          radius: ["35%", "68%"],
          center: ["43%", "55%"],
          avoidLabelOverlap: true,
          label: {
            formatter: "{b}: {d}%"
          },
          data: rows.map((row) => ({
            name: String(row[nameField] ?? ""),
            value: valueOrNull(row[valueField])
          }))
        }]
      },
      chartType
    };
  }

  if (chartType === "scatter") {
    const scatterFields = yFields.length >= 2 ? yFields : numeric.slice(0, 2);
    if (scatterFields.length < 2) {
      fail("Scatter charts require at least two numeric fields");
    }
    return {
      option: {
        ...base,
        tooltip: {
          trigger: "item"
        },
        grid: {
          left: 72,
          right: 44,
          top: title ? 132 : 88,
          bottom: 72
        },
        xAxis: {
          type: "value",
          name: scatterFields[0],
          nameLocation: "middle",
          nameGap: 42
        },
        yAxis: {
          type: "value",
          name: scatterFields[1],
          nameLocation: "middle",
          nameGap: 52
        },
        series: [{
          name: `${scatterFields[0]} / ${scatterFields[1]}`,
          type: "scatter",
          symbolSize: 10,
          data: rows.map((row) => [valueOrNull(row[scatterFields[0]]), valueOrNull(row[scatterFields[1]])])
        }]
      },
      chartType
    };
  }

  if (!xField) {
    fail("Bar and line charts require a category field. Pass --x <field>.");
  }
  if (yFields.length === 0) {
    fail("No numeric value fields found. Pass --y <field1,field2>.");
  }

  const categories = rows.map((row) => String(row[xField] ?? ""));
  const option = {
    ...base,
    tooltip: { trigger: "axis" },
    grid: {
      left: 72,
      right: 44,
      top: title ? 132 : 88,
      bottom: categories.length > 12 ? 112 : 72,
      containLabel: true
    },
    xAxis: {
      type: "category",
      data: categories,
      axisLabel: {
        interval: categories.length > 18 ? "auto" : 0,
        rotate: categories.length > 12 ? 30 : 0
      }
    },
    yAxis: {
      type: "value"
    },
    series: yFields.map((field) => ({
      name: field,
      type: chartType,
      smooth: chartType === "line",
      showSymbol: chartType === "line" && rows.length <= 60,
      data: rows.map((row) => valueOrNull(row[field])),
      emphasis: {
        focus: "series"
      }
    }))
  };

  if (categories.length > 30) {
    option.dataZoom = [{
      type: "inside"
    }, {
      type: "slider",
      bottom: 24
    }];
  }

  return {
    option,
    chartType
  };
}

function finalizeProvidedOption(option, args) {
  const theme = (args.theme ?? "light").toLowerCase();
  if (!["light", "dark"].includes(theme)) {
    fail("--theme must be light or dark");
  }
  const dark = theme === "dark";
  const finalOption = structuredClone(option);
  if (args.title) {
    finalOption.title = {
      ...(typeof finalOption.title === "object" && !Array.isArray(finalOption.title) ? finalOption.title : {}),
      text: args.title
    };
  }
  if (!finalOption.backgroundColor) {
    finalOption.backgroundColor = dark ? "#0f172a" : "#ffffff";
  }
  return {
    option: finalOption,
    chartType: inferTypeFromOption(finalOption)
  };
}

function inferTypeFromOption(option) {
  const series = Array.isArray(option.series) ? option.series : option.series ? [option.series] : [];
  return unique(series.map((item) => item?.type).filter(Boolean)).join(",") || "custom";
}

function renderSvg(option, { width, height, theme }) {
  const chart = echarts.init(null, theme === "dark" ? "dark" : null, {
    renderer: "svg",
    ssr: true,
    width,
    height
  });

  chart.setOption(option, true);
  const svg = chart.renderToSVGString();
  chart.dispose();
  return svg;
}

async function writeImage(svg, outputPath, format) {
  await mkdir(path.dirname(outputPath), { recursive: true });

  if (format === "svg") {
    await writeFile(outputPath, svg, "utf8");
    return;
  }

  const normalized = normalizeFormat(format);
  let image = sharp(Buffer.from(svg));
  if (normalized === "png") {
    image = image.png();
  } else if (normalized === "jpeg") {
    image = image.flatten({ background: "#ffffff" }).jpeg({ quality: 92 });
  } else if (normalized === "webp") {
    image = image.webp({ quality: 92 });
  }

  await image.toFile(outputPath);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(usage());
    return;
  }

  if (!args.output) {
    fail("Missing --output");
  }

  const width = readNumberArg(args, "width", DEFAULT_WIDTH);
  const height = readNumberArg(args, "height", DEFAULT_HEIGHT);
  const format = deriveFormat(args);
  const theme = (args.theme ?? "light").toLowerCase();
  const outputPath = path.resolve(args.output);
  const { text, sourcePath } = await loadInput(args);
  const input = parseInput(text, sourcePath);
  const built = input.kind === "option"
    ? finalizeProvidedOption(input.option, args)
    : buildOptionFromTable(input, args);

  if (args["save-option"]) {
    const optionPath = path.resolve(args["save-option"]);
    await mkdir(path.dirname(optionPath), { recursive: true });
    await writeFile(optionPath, `${JSON.stringify(built.option, null, 2)}\n`, "utf8");
  }

  const svg = renderSvg(built.option, { width, height, theme });
  await writeImage(svg, outputPath, format);

  console.log(JSON.stringify({
    output: outputPath,
    format,
    width,
    height,
    chartType: built.chartType,
    option: args["save-option"] ? path.resolve(args["save-option"]) : undefined
  }, null, 2));
}

main().catch((error) => {
  const reason = error instanceof Error ? error.message : String(error);
  logger.error({
    error: error instanceof Error
      ? { message: reason, stack: error.stack }
      : { message: reason }
  }, "aios-make-chart-image failed");
  process.exit(1);
});
