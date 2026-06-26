import { buildChartSpec } from "../core/recommend.js";
import { readJsonInput, writeTextOutput } from "./args.js";
const request = await readJsonInput();
await writeTextOutput(`${JSON.stringify(buildChartSpec(request), null, 2)}\n`, "spec.json");
