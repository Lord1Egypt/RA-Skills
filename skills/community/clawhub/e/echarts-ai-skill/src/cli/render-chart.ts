import type { ChartOption } from "../types/chart.js";

import { renderHtml, renderSvg } from "../core/render.js";
import { getArg, getNumberArg, readJsonInput, writeTextOutput } from "./args.js";

const option = await readJsonInput<ChartOption>();
const format = getArg("--format") ?? "html";
const width = getNumberArg("--width", 960);
const height = getNumberArg("--height", 540);

if (format === "svg") {
  await writeTextOutput(await renderSvg(option, width, height), "preview.svg");
} else if (format === "html") {
  await writeTextOutput(renderHtml(option, width, height), "preview.html");
} else {
  throw new Error(`Unsupported format: ${format}`);
}
