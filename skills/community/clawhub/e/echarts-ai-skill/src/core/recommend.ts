import type {
  ChartField,
  ChartGoal,
  ChartIndicator,
  ChartParallelAxis,
  ChartRequest,
  ChartSpec,
  ChartType,
  DataRow
} from "../types/chart.js";

const DEFAULT_WIDTH = 960;
const DEFAULT_HEIGHT = 540;
const EXPLICIT_TYPES: ChartType[] = [
  "line",
  "bar",
  "pie",
  "scatter",
  "effectScatter",
  "radar",
  "funnel",
  "gauge",
  "heatmap",
  "treemap",
  "sunburst",
  "sankey",
  "graph",
  "candlestick",
  "boxplot",
  "parallel",
  "map",
  "lines"
];

function isIsoLikeDate(value: string): boolean {
  return /^\d{4}[-/]\d{1,2}[-/]\d{1,2}/.test(value) || !Number.isNaN(Date.parse(value));
}

function inferFieldType(values: Array<DataRow[keyof DataRow]>): ChartField["type"] {
  const filtered = values.filter((value) => value !== null);
  if (filtered.length === 0) {
    return "unknown";
  }
  if (filtered.every((value) => typeof value === "number")) {
    return "number";
  }
  if (filtered.every((value) => typeof value === "boolean")) {
    return "boolean";
  }
  if (filtered.every((value) => typeof value === "string" && isIsoLikeDate(value))) {
    return "date";
  }
  if (filtered.every((value) => typeof value === "string")) {
    return "string";
  }
  return "unknown";
}

export function inferFields(dataset: DataRow[]): ChartField[] {
  if (dataset.length === 0) {
    return [];
  }
  const fieldNames = new Set<string>();
  for (const row of dataset) {
    Object.keys(row).forEach((key) => fieldNames.add(key));
  }
  return Array.from(fieldNames).map((name) => ({
    name,
    type: inferFieldType(dataset.map((row) => row[name] ?? null))
  }));
}

function firstField(fields: ChartField[], type: ChartField["type"]): string | undefined {
  return fields.find((field) => field.type === type)?.name;
}

function numericFields(fields: ChartField[]): string[] {
  return fields.filter((field) => field.type === "number").map((field) => field.name);
}

function recommendGoal(request: ChartRequest, fields: ChartField[]): ChartGoal {
  if (request.goal && request.goal !== "unknown") {
    return request.goal;
  }
  switch (request.chartType) {
    case "pie":
    case "treemap":
    case "sunburst":
    case "funnel":
      return "composition";
    case "scatter":
    case "effectScatter":
    case "heatmap":
    case "boxplot":
    case "candlestick":
      return "distribution";
    case "sankey":
    case "graph":
    case "lines":
      return "flow";
    default:
      break;
  }
  const hasDate = fields.some((field) => field.type === "date");
  if (hasDate) {
    return "trend";
  }
  if (numericFields(fields).length >= 2) {
    return "distribution";
  }
  return "comparison";
}

function recommendChartType(request: ChartRequest, fields: ChartField[]): ChartType {
  if (request.chartType && EXPLICIT_TYPES.includes(request.chartType)) {
    return request.chartType;
  }
  if (request.nodes?.length && request.links?.length) {
    return "sankey";
  }
  if (request.tree?.length) {
    return "treemap";
  }
  if (request.lineCoordinates?.length) {
    return "lines";
  }
  if (request.indicators?.length) {
    return "radar";
  }
  if (request.xField && request.yField) {
    const xType = fields.find((field) => field.name === request.xField)?.type;
    const yType = fields.find((field) => field.name === request.yField)?.type;
    if (xType === "number" && yType === "number") {
      return "scatter";
    }
    if (xType === "date" || xType === "string") {
      return "line";
    }
  }
  const categoryField = request.categoryField ?? firstField(fields, "date") ?? firstField(fields, "string");
  const numbers = numericFields(fields);
  if (categoryField && numbers.length === 1 && request.dataset.length <= 12) {
    return "pie";
  }
  if (categoryField && numbers.length >= 1) {
    const categoryType = fields.find((field) => field.name === categoryField)?.type;
    return categoryType === "date" ? "line" : "bar";
  }
  if (numbers.length >= 2) {
    return "scatter";
  }
  return "bar";
}

function buildIndicators(request: ChartRequest, fields: ChartField[]): ChartIndicator[] {
  if (request.indicators?.length) {
    return request.indicators;
  }
  const excluded = new Set([request.categoryField, request.xField, request.groupField].filter(Boolean));
  return numericFields(fields)
    .filter((name) => !excluded.has(name))
    .map((name) => ({ name }));
}

function buildParallelAxis(request: ChartRequest, fields: ChartField[]): ChartParallelAxis[] {
  if (request.parallelAxis?.length) {
    return request.parallelAxis;
  }
  const dims = (request.dimensions?.length ? request.dimensions : numericFields(fields)).filter(Boolean);
  return dims.map((name, index) => ({ dim: index, name }));
}

function buildSeries(request: ChartRequest, chartType: ChartType, fields: ChartField[]) {
  if (request.series && request.series.length > 0) {
    return request.series;
  }
  if (["pie", "funnel", "gauge", "map"].includes(chartType)) {
    const valueField = request.valueField ?? firstField(fields, "number");
    return valueField ? [{ name: valueField, field: valueField }] : [];
  }
  if (["candlestick"].includes(chartType)) {
    return [];
  }
  if (["radar", "parallel", "treemap", "sunburst", "sankey", "graph", "lines", "heatmap", "boxplot"].includes(chartType)) {
    return [];
  }
  if (request.yField) {
    return [{ name: request.yField, field: request.yField }];
  }
  return numericFields(fields).map((field) => ({ name: field, field }));
}

export function buildChartSpec(request: ChartRequest): ChartSpec {
  const fields = inferFields(request.dataset);
  const chartType = recommendChartType(request, fields);
  const goal = recommendGoal(request, fields);
  const categoryField =
    request.categoryField ??
    (["pie", "funnel", "map"].includes(chartType) ? firstField(fields, "string") : firstField(fields, "date") ?? firstField(fields, "string"));
  const xField = request.xField ?? (["scatter", "effectScatter", "heatmap"].includes(chartType) ? firstField(fields, "number") : categoryField);
  const yField =
    request.yField ??
    (["scatter", "effectScatter"].includes(chartType)
      ? fields.filter((field) => field.type === "number" && field.name !== xField)[0]?.name
      : firstField(fields, "number"));
  const valueField = request.valueField ?? yField;

  return {
    title: request.title,
    subtitle: request.subtitle,
    chartType,
    goal,
    dataset: request.dataset,
    categoryField,
    xField,
    yField,
    valueField,
    groupField: request.groupField,
    series: buildSeries(request, chartType, fields),
    indicators: buildIndicators(request, fields),
    nodes: request.nodes ?? [],
    links: request.links ?? [],
    tree: request.tree ?? [],
    lineCoordinates: request.lineCoordinates ?? [],
    mapName: request.mapName,
    dimensions: request.dimensions ?? numericFields(fields),
    parallelAxis: buildParallelAxis(request, fields),
    openField: request.openField,
    closeField: request.closeField,
    lowField: request.lowField,
    highField: request.highField,
    minField: request.minField,
    q1Field: request.q1Field,
    medianField: request.medianField,
    q3Field: request.q3Field,
    maxField: request.maxField,
    width: request.width ?? DEFAULT_WIDTH,
    height: request.height ?? DEFAULT_HEIGHT,
    fields,
    rawOption: request.rawOption
  };
}
