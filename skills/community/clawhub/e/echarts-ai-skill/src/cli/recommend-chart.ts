import { buildChartSpec } from "../core/recommend.js";
import type { ChartRequest } from "../types/chart.js";
import { readJsonInput, writeTextOutput } from "./args.js";

const request = await readJsonInput<ChartRequest>();
await writeTextOutput(`${JSON.stringify(buildChartSpec(request), null, 2)}\n`, "spec.json");
