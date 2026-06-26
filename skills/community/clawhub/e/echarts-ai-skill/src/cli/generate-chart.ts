import { buildChartSpec } from "../core/recommend.js";
import { buildOption } from "../core/spec-to-option.js";
import type { ChartRequest, ChartSpec } from "../types/chart.js";
import { readJsonInput, writeTextOutput } from "./args.js";

function isChartSpec(input: ChartRequest | ChartSpec): input is ChartSpec {
  return "fields" in input && "chartType" in input && "width" in input && "height" in input;
}

const input = await readJsonInput<ChartRequest | ChartSpec>();
const spec = isChartSpec(input) ? input : buildChartSpec(input);
const option = buildOption(spec);
await writeTextOutput(`${JSON.stringify(option, null, 2)}\n`, "option.json");
