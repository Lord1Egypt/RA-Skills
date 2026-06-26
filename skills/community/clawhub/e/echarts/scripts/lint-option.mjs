#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function usage() {
  console.log("Usage: node {baseDir}/scripts/lint-option.mjs <path/to/chart.option.json>");
}

function firstAxis(axis) {
  if (!axis) {
    return null;
  }
  return Array.isArray(axis) ? axis[0] : axis;
}

function getSeries(option) {
  if (!option.series) {
    return [];
  }
  return Array.isArray(option.series) ? option.series : [option.series];
}

function getSeriesByType(series, type) {
  return series.find((item) => item?.type === type) ?? null;
}

function categoryCount(option) {
  const xAxis = firstAxis(option.xAxis);
  const yAxis = firstAxis(option.yAxis);
  const xCategories =
    xAxis?.type === "category" && Array.isArray(xAxis.data) ? xAxis.data.length : 0;
  const yCategories =
    yAxis?.type === "category" && Array.isArray(yAxis.data) ? yAxis.data.length : 0;
  return Math.max(xCategories, yCategories);
}

async function main() {
  const input = process.argv[2];
  if (!input) {
    usage();
    process.exitCode = 1;
    return;
  }

  const filePath = path.resolve(process.cwd(), input);
  const raw = await fs.readFile(filePath, "utf8");
  const option = JSON.parse(raw);
  const series = getSeries(option);
  const errors = [];
  const warnings = [];
  const notes = [];

  if (!option || typeof option !== "object" || Array.isArray(option)) {
    errors.push("Option root must be a JSON object.");
  }

  if (series.length === 0) {
    errors.push("Option must define at least one series.");
  }

  const types = new Set(series.map((item) => item?.type ?? "line"));
  const hasDataset = Boolean(option.dataset);
  const hasPie = types.has("pie");
  const hasRadar = types.has("radar");
  const hasHeatmap = types.has("heatmap");
  const hasGauge = types.has("gauge");
  const hasTreemap = types.has("treemap");
  const hasCandlestick = types.has("candlestick");
  const hasBoxplot = types.has("boxplot");
  const hasSankey = types.has("sankey");
  const hasSunburst = types.has("sunburst");
  const hasGraph = types.has("graph");
  const hasTree = types.has("tree");
  const hasParallel = types.has("parallel");
  const hasThemeRiver = types.has("themeRiver");
  const hasPictorialBar = types.has("pictorialBar");
  const hasPolarBar =
    Boolean(option.polar) &&
    series.some((item) => item?.type === "bar" && item?.coordinateSystem === "polar");
  const hasCalendar =
    Boolean(option.calendar) || series.some((item) => item?.coordinateSystem === "calendar");
  const xAxis = firstAxis(option.xAxis);
  const yAxis = firstAxis(option.yAxis);

  if ((types.has("bar") || types.has("line") || hasPictorialBar) && !hasPolarBar && !option.xAxis) {
    errors.push("Bar, line, and pictorial bar charts should define xAxis.");
  }

  if ((types.has("bar") || types.has("line") || hasPictorialBar) && !hasPolarBar && !option.yAxis) {
    errors.push("Bar, line, and pictorial bar charts should define yAxis.");
  }

  if (hasPolarBar) {
    if (!option.polar || !option.angleAxis || !option.radiusAxis) {
      errors.push("Polar bar charts should define polar, angleAxis, and radiusAxis.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Polar bar charts do not usually need xAxis or yAxis.");
    }
  }

  if (types.has("scatter")) {
    if (!option.xAxis || !option.yAxis) {
      errors.push("Scatter charts should define both xAxis and yAxis.");
    }
    if (xAxis?.type && xAxis.type !== "value") {
      warnings.push("Scatter charts usually use xAxis.type = value.");
    }
    if (yAxis?.type && yAxis.type !== "value") {
      warnings.push("Scatter charts usually use yAxis.type = value.");
    }
  }

  if (hasCandlestick) {
    if (!option.xAxis || !option.yAxis) {
      errors.push("Candlestick charts should define both xAxis and yAxis.");
    }
    if (xAxis?.type && xAxis.type !== "category") {
      warnings.push("Candlestick charts usually use xAxis.type = category.");
    }
    if (yAxis?.type && yAxis.type !== "value") {
      warnings.push("Candlestick charts usually use yAxis.type = value.");
    }
  }

  if (hasBoxplot) {
    if (!option.xAxis || !option.yAxis) {
      errors.push("Boxplot charts should define both xAxis and yAxis.");
    }
    if (xAxis?.type && xAxis.type !== "category") {
      warnings.push("Boxplot charts usually use xAxis.type = category.");
    }
    if (yAxis?.type && yAxis.type !== "value") {
      warnings.push("Boxplot charts usually use yAxis.type = value.");
    }
  }

  if (hasPie && (option.xAxis || option.yAxis)) {
    warnings.push("Pie charts do not usually need xAxis or yAxis.");
  }

  if (hasRadar && !option.radar) {
    errors.push("Radar charts must define radar.indicator.");
  }

  if (hasParallel) {
    if (!Array.isArray(option.parallelAxis) || option.parallelAxis.length === 0) {
      errors.push("Parallel charts should define a non-empty parallelAxis array.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Parallel charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasThemeRiver) {
    if (!option.singleAxis) {
      errors.push("ThemeRiver charts should define singleAxis.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("ThemeRiver charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasHeatmap) {
    if (!hasCalendar && (!option.xAxis || !option.yAxis)) {
      errors.push("Heatmap charts should define both xAxis and yAxis unless they use calendar.");
    }
    if (!option.visualMap) {
      warnings.push(
        "Heatmap and calendar charts usually define visualMap for readable color scaling.",
      );
    }
  }

  if (hasCalendar) {
    if (!option.calendar) {
      errors.push("Calendar charts should define calendar.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Calendar charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasTreemap) {
    const treemapSeries = getSeriesByType(series, "treemap");
    if (!Array.isArray(treemapSeries?.data) || treemapSeries.data.length === 0) {
      errors.push("Treemap charts should include non-empty series.data.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Treemap charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasSunburst) {
    const sunburstSeries = getSeriesByType(series, "sunburst");
    if (!Array.isArray(sunburstSeries?.data) || sunburstSeries.data.length === 0) {
      errors.push("Sunburst charts should include non-empty series.data.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Sunburst charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasTree) {
    const treeSeries = getSeriesByType(series, "tree");
    if (!Array.isArray(treeSeries?.data) || treeSeries.data.length === 0) {
      errors.push("Tree charts should include non-empty series.data.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Tree charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasSankey) {
    const sankeySeries = getSeriesByType(series, "sankey");
    const links = Array.isArray(sankeySeries?.links)
      ? sankeySeries.links
      : Array.isArray(sankeySeries?.edges)
        ? sankeySeries.edges
        : null;
    if (!Array.isArray(sankeySeries?.data) || sankeySeries.data.length === 0) {
      errors.push("Sankey charts should include non-empty series.data.");
    }
    if (!Array.isArray(links) || links.length === 0) {
      errors.push("Sankey charts should include non-empty series.links or series.edges.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Sankey charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasGraph) {
    const graphSeries = getSeriesByType(series, "graph");
    const links = Array.isArray(graphSeries?.links)
      ? graphSeries.links
      : Array.isArray(graphSeries?.edges)
        ? graphSeries.edges
        : null;
    if (!Array.isArray(graphSeries?.data) || graphSeries.data.length === 0) {
      errors.push("Graph charts should include non-empty series.data.");
    }
    if (!Array.isArray(links) || links.length === 0) {
      errors.push("Graph charts should include non-empty series.links or series.edges.");
    }
    if (option.xAxis || option.yAxis) {
      warnings.push("Graph charts do not usually need xAxis or yAxis.");
    }
  }

  if (hasGauge && (option.xAxis || option.yAxis)) {
    notes.push("Gauge charts usually do not need xAxis or yAxis.");
  }

  if (!option.tooltip && !hasGauge) {
    warnings.push("Tooltip is missing. Interactive previews will feel incomplete.");
  }

  if (!option.aria) {
    warnings.push(
      "aria.enabled is missing. Generated charts are harder to audit for accessibility.",
    );
  }

  if (!option.title) {
    notes.push(
      "No title found. This is fine for embeds, but reports usually benefit from a visible title.",
    );
  }

  if (!hasDataset) {
    for (const [index, item] of series.entries()) {
      if (!Array.isArray(item?.data) || item.data.length === 0) {
        if (item?.type === "gauge") {
          continue;
        }
        errors.push(`Series ${index + 1} is missing data.`);
      }
    }
  }

  const categories = categoryCount(option);
  if (
    categories > 12 &&
    !option.dataZoom &&
    !hasPie &&
    !hasRadar &&
    !hasHeatmap &&
    !hasCalendar &&
    !hasThemeRiver &&
    !hasSankey &&
    !hasSunburst &&
    !hasTreemap &&
    !hasGraph &&
    !hasTree &&
    !hasParallel
  ) {
    warnings.push("Category count is high and dataZoom is missing.");
  }

  if (
    series.length === 1 &&
    option.legend &&
    !hasPie &&
    !hasRadar &&
    !hasTreemap &&
    !hasSunburst &&
    !hasSankey &&
    !hasGraph &&
    !hasTree &&
    !hasParallel &&
    !hasThemeRiver
  ) {
    notes.push(
      "Legend is present for a single-series chart. Consider removing it if space is tight.",
    );
  }

  const categoryAxis =
    xAxis?.type === "category" ? xAxis : yAxis?.type === "category" ? yAxis : null;
  if (categoryAxis && Array.isArray(categoryAxis.data) && !hasDataset && !hasHeatmap) {
    const expectedLength = categoryAxis.data.length;
    for (const [index, item] of series.entries()) {
      if (Array.isArray(item?.data) && item.data.length !== expectedLength) {
        warnings.push(
          `Series ${index + 1} data length (${item.data.length}) does not match category count (${expectedLength}).`,
        );
      }
    }
  }

  if (errors.length === 0) {
    console.log(`[ok] ${path.relative(process.cwd(), filePath) || path.basename(filePath)}`);
  }

  if (errors.length > 0) {
    console.log("Errors:");
    for (const issue of errors) {
      console.log(`- ${issue}`);
    }
  }

  if (warnings.length > 0) {
    console.log("Warnings:");
    for (const issue of warnings) {
      console.log(`- ${issue}`);
    }
  }

  if (notes.length > 0) {
    console.log("Notes:");
    for (const issue of notes) {
      console.log(`- ${issue}`);
    }
  }

  process.exitCode = errors.length > 0 ? 1 : 0;
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
