import { buildChartSpec } from "../core/recommend.js";
import { buildOption } from "../core/spec-to-option.js";
import { readJsonInput, writeTextOutput } from "./args.js";
function isChartSpec(input) {
    return "fields" in input && "chartType" in input && "width" in input && "height" in input;
}
const input = await readJsonInput();
const spec = isChartSpec(input) ? input : buildChartSpec(input);
const option = buildOption(spec);
await writeTextOutput(`${JSON.stringify(option, null, 2)}\n`, "option.json");
