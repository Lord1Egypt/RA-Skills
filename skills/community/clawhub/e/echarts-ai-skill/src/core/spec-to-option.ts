import type {
  ChartIndicator,
  ChartNode,
  ChartOption,
  ChartSeriesInput,
  ChartSeriesOption,
  ChartSpec,
  DataRow
} from "../types/chart.js";

function categoryValue(row: DataRow, field: string | undefined): string | number | null {
  if (!field) {
    return null;
  }
  return (row[field] as string | number | null) ?? null;
}

function numberValue(row: DataRow, field: string | undefined): number | null {
  if (!field) {
    return null;
  }
  const value = row[field];
  return typeof value === "number" ? value : null;
}

function uniqueValues(values: Array<string | number | null>): Array<string | number> {
  return Array.from(new Set(values.filter((value): value is string | number => value !== null)));
}

function titleBlock(spec: ChartSpec): Record<string, unknown> {
  return spec.subtitle
    ? { text: spec.title, subtext: spec.subtitle, left: "center" }
    : { text: spec.title, left: "center" };
}

function buildCartesianSeries(spec: ChartSpec, type: "line" | "bar"): ChartSeriesOption[] {
  return spec.series.map((series: ChartSeriesInput) => ({
    name: series.name,
    type,
    smooth: type === "line",
    areaStyle: spec.chartType === "line" && spec.goal === "composition" ? {} : undefined,
    data: spec.dataset.map((row) => numberValue(row, series.field))
  }));
}

function buildScatterLikeSeries(spec: ChartSpec, type: "scatter" | "effectScatter"): ChartSeriesOption[] {
  return [
    {
      name: spec.title ?? type,
      type,
      data: spec.dataset.map((row) => [numberValue(row, spec.xField), numberValue(row, spec.yField)])
    }
  ];
}

function buildPieLikeData(spec: ChartSpec) {
  const valueField = spec.valueField;
  return spec.dataset.map((row) => ({
    name: String(categoryValue(row, spec.categoryField) ?? ""),
    value: numberValue(row, valueField) ?? 0
  }));
}

function buildRadarIndicators(spec: ChartSpec): ChartIndicator[] {
  if (spec.indicators.length > 0) {
    return spec.indicators.map((indicator) => {
      if (indicator.max !== undefined || indicator.min !== undefined) {
        return indicator;
      }
      const values = spec.dataset.map((row) => numberValue(row, indicator.name) ?? 0);
      const max = values.length > 0 ? Math.max(...values, 1) : 1;
      return { ...indicator, max };
    });
  }
  return [];
}

function buildRadarSeries(spec: ChartSpec): ChartSeriesOption[] {
  const indicators = buildRadarIndicators(spec);
  return [
    {
      type: "radar",
      data: spec.dataset.map((row) => ({
        name: String(categoryValue(row, spec.categoryField) ?? spec.title ?? "Series"),
        value: indicators.map((indicator) => numberValue(row, indicator.name) ?? 0)
      }))
    }
  ];
}

function buildGaugeSeries(spec: ChartSpec): ChartSeriesOption[] {
  const value = spec.dataset[0] ? numberValue(spec.dataset[0], spec.valueField ?? spec.series[0]?.field) ?? 0 : 0;
  return [
    {
      type: "gauge",
      progress: { show: true, width: 18 },
      detail: { valueAnimation: true, formatter: "{value}" },
      data: [{ value, name: spec.title ?? spec.valueField ?? "Value" }]
    }
  ];
}

function buildHeatmapOption(spec: ChartSpec): ChartOption {
  const xValues = uniqueValues(spec.dataset.map((row) => categoryValue(row, spec.xField)));
  const yValues = uniqueValues(spec.dataset.map((row) => categoryValue(row, spec.yField)));
  return {
    title: titleBlock(spec),
    tooltip: { position: "top" },
    grid: { left: 60, right: 20, top: 72, bottom: 40 },
    xAxis: { type: "category", data: xValues },
    yAxis: { type: "category", data: yValues },
    visualMap: {
      min: 0,
      max: Math.max(...spec.dataset.map((row) => numberValue(row, spec.valueField) ?? 0), 1),
      calculable: true,
      orient: "horizontal",
      left: "center",
      bottom: 0
    },
    series: [{
      type: "heatmap",
      data: spec.dataset.map((row) => [
        xValues.indexOf(categoryValue(row, spec.xField) as string | number),
        yValues.indexOf(categoryValue(row, spec.yField) as string | number),
        numberValue(row, spec.valueField) ?? 0
      ])
    }]
  };
}

function buildCandlestickOption(spec: ChartSpec): ChartOption {
  const axisData = spec.dataset.map((row) => categoryValue(row, spec.categoryField));
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: axisData },
    yAxis: { type: "value", scale: true },
    series: [{
      type: "candlestick",
      data: spec.dataset.map((row) => [
        numberValue(row, spec.openField),
        numberValue(row, spec.closeField),
        numberValue(row, spec.lowField),
        numberValue(row, spec.highField)
      ])
    }]
  };
}

function buildBoxplotOption(spec: ChartSpec): ChartOption {
  const axisData = spec.dataset.map((row) => categoryValue(row, spec.categoryField));
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    xAxis: { type: "category", data: axisData },
    yAxis: { type: "value" },
    series: [{
      type: "boxplot",
      data: spec.dataset.map((row) => [
        numberValue(row, spec.minField),
        numberValue(row, spec.q1Field),
        numberValue(row, spec.medianField),
        numberValue(row, spec.q3Field),
        numberValue(row, spec.maxField)
      ])
    }]
  };
}

function buildTreeSeries(spec: ChartSpec, type: "treemap" | "sunburst"): ChartSeriesOption[] {
  const data = spec.tree.length > 0
    ? spec.tree
    : spec.dataset.map((row) => ({
        name: String(categoryValue(row, spec.categoryField) ?? ""),
        value: numberValue(row, spec.valueField) ?? 0
      }));

  return [{
    type,
    radius: type === "sunburst" ? ["15%", "82%"] : undefined,
    roam: false,
    nodeClick: false,
    data
  }];
}

function buildSankeyOption(spec: ChartSpec): ChartOption {
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    series: [{
      type: "sankey",
      emphasis: { focus: "adjacency" },
      data: spec.nodes,
      links: spec.links,
      lineStyle: { color: "gradient", curveness: 0.5 }
    }]
  };
}

function buildGraphOption(spec: ChartSpec): ChartOption {
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    legend: spec.nodes.some((node) => node.category !== undefined)
      ? { data: uniqueValues(spec.nodes.map((node) => (node.category ?? null) as string | number | null)) }
      : undefined,
    series: [{
      type: "graph",
      layout: spec.nodes.some((node) => node.x !== undefined && node.y !== undefined) ? "none" : "force",
      roam: true,
      label: { show: true },
      force: { repulsion: 180, edgeLength: 120 },
      data: spec.nodes,
      links: spec.links
    }]
  };
}

function buildParallelOption(spec: ChartSpec): ChartOption {
  return {
    title: titleBlock(spec),
    parallelAxis: spec.parallelAxis,
    parallel: { left: 60, right: 40, bottom: 50, top: 80 },
    tooltip: { trigger: "item" },
    series: [{
      type: "parallel",
      lineStyle: { width: 1.5, opacity: 0.45 },
      data: spec.dataset.map((row) => spec.parallelAxis.map((axis) => numberValue(row, axis.name) ?? 0))
    }]
  };
}

function buildMapOption(spec: ChartSpec): ChartOption {
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    visualMap: {
      min: 0,
      max: Math.max(...spec.dataset.map((row) => numberValue(row, spec.valueField) ?? 0), 1),
      left: "right",
      top: "bottom",
      text: ["High", "Low"],
      calculable: true
    },
    series: [{
      type: "map",
      map: spec.mapName ?? "world",
      roam: true,
      data: spec.dataset.map((row) => ({
        name: String(categoryValue(row, spec.categoryField) ?? ""),
        value: numberValue(row, spec.valueField) ?? 0
      }))
    }]
  };
}

function buildLinesOption(spec: ChartSpec): ChartOption {
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    xAxis: { type: "value" },
    yAxis: { type: "value" },
    series: [{
      type: "lines",
      coordinateSystem: "cartesian2d",
      polyline: true,
      data: spec.lineCoordinates
    }]
  };
}

function buildFunnelSeries(spec: ChartSpec): ChartSeriesOption[] {
  return [{
    type: "funnel",
    sort: "descending",
    label: { show: true, position: "inside" },
    data: buildPieLikeData(spec)
  }];
}

function buildRadarOption(spec: ChartSpec): ChartOption {
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    legend: { top: 28 },
    radar: { indicator: buildRadarIndicators(spec) },
    series: buildRadarSeries(spec)
  };
}

function buildPieOption(spec: ChartSpec): ChartOption {
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    legend: { bottom: 0 },
    series: [{
      name: spec.title ?? "Pie",
      type: "pie",
      radius: "60%",
      data: buildPieLikeData(spec)
    }]
  };
}

function buildCartesianOption(spec: ChartSpec, type: "line" | "bar"): ChartOption {
  const axisData = spec.dataset.map((row) => categoryValue(row, spec.categoryField));
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "axis" },
    legend: { top: 28 },
    grid: { left: 48, right: 24, top: 72, bottom: 48 },
    xAxis: {
      type: "category",
      name: spec.categoryField,
      boundaryGap: type === "bar",
      data: axisData
    },
    yAxis: { type: "value" },
    series: buildCartesianSeries(spec, type)
  };
}

function buildScatterOption(spec: ChartSpec, type: "scatter" | "effectScatter"): ChartOption {
  return {
    title: titleBlock(spec),
    tooltip: { trigger: "item" },
    xAxis: { type: "value", name: spec.xField },
    yAxis: { type: "value", name: spec.yField },
    series: buildScatterLikeSeries(spec, type)
  };
}

export function buildOption(spec: ChartSpec): ChartOption {
  if (spec.rawOption) {
    return spec.rawOption;
  }

  switch (spec.chartType) {
    case "pie":
      return buildPieOption(spec);
    case "scatter":
      return buildScatterOption(spec, "scatter");
    case "effectScatter":
      return buildScatterOption(spec, "effectScatter");
    case "line":
      return buildCartesianOption(spec, "line");
    case "bar":
      return buildCartesianOption(spec, "bar");
    case "radar":
      return buildRadarOption(spec);
    case "funnel":
      return { title: titleBlock(spec), tooltip: { trigger: "item" }, legend: { top: 28 }, series: buildFunnelSeries(spec) };
    case "gauge":
      return { title: titleBlock(spec), tooltip: { trigger: "item" }, series: buildGaugeSeries(spec) };
    case "heatmap":
      return buildHeatmapOption(spec);
    case "treemap":
      return { title: titleBlock(spec), tooltip: { trigger: "item" }, series: buildTreeSeries(spec, "treemap") };
    case "sunburst":
      return { title: titleBlock(spec), tooltip: { trigger: "item" }, series: buildTreeSeries(spec, "sunburst") };
    case "sankey":
      return buildSankeyOption(spec);
    case "graph":
      return buildGraphOption(spec);
    case "candlestick":
      return buildCandlestickOption(spec);
    case "boxplot":
      return buildBoxplotOption(spec);
    case "parallel":
      return buildParallelOption(spec);
    case "map":
      return buildMapOption(spec);
    case "lines":
      return buildLinesOption(spec);
    default:
      return buildCartesianOption(spec, "bar");
  }
}
