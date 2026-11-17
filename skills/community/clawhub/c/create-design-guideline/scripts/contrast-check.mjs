#!/usr/bin/env node

const usage = `Usage: node contrast-check.mjs [--min RATIO] [--json] "#foreground:#background" [more pairs]

Report mode classifies opaque sRGB #RGB/#RRGGBB pairs.
--min sets a gate from 1 through 21; choose it for the actual use.
Exit: 0 report/passing gate, 1 missed threshold, 2 invalid input.`;

function normalizeHex(value) {
  const match = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(value.trim());
  if (!match) throw new Error(`Unsupported opaque sRGB hex: ${value}`);
  const digits = match[1].length === 3
    ? [...match[1]].map((character) => character.repeat(2)).join("")
    : match[1];
  return `#${digits.toUpperCase()}`;
}

function relativeLuminance(hex) {
  const channels = [1, 3, 5].map((start) =>
    Number.parseInt(hex.slice(start, start + 2), 16) / 255,
  );
  const linear = channels.map((channel) =>
    channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4,
  );
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

function checkPair(pair, minimum) {
  const parts = pair.split(":");
  if (parts.length !== 2) throw new Error(`Invalid pair: ${pair}`);
  const foreground = normalizeHex(parts[0]);
  const background = normalizeHex(parts[1]);
  const luminances = [relativeLuminance(foreground), relativeLuminance(background)];
  const ratio = (Math.max(...luminances) + 0.05) / (Math.min(...luminances) + 0.05);
  return {
    foreground,
    background,
    ratio,
    aaText: ratio >= 4.5,
    aaaText: ratio >= 7,
    largeTextAndUI: ratio >= 3,
    meetsMinimum: minimum === null ? null : ratio >= minimum,
  };
}

const args = process.argv.slice(2);
let minimum = null;
let json = false;
const pairs = [];
const errors = [];

if (args.includes("--help") || args.includes("-h")) {
  console.log(usage);
  process.exit(0);
}

for (let index = 0; index < args.length; index += 1) {
  const arg = args[index];
  if (arg === "--json") {
    json = true;
  } else if (arg === "--min" || arg.startsWith("--min=")) {
    if (arg === "--min" && (args[index + 1] === undefined || args[index + 1].startsWith("--"))) {
      errors.push("--min requires a ratio from 1 through 21.");
      continue;
    }
    const value = arg === "--min" ? args[++index] : arg.slice(6);
    const parsed = Number(value);
    if (minimum !== null || !Number.isFinite(parsed) || parsed < 1 || parsed > 21) {
      errors.push("--min must be specified once with a finite ratio from 1 through 21.");
    } else {
      minimum = parsed;
    }
  } else if (arg.startsWith("-")) {
    errors.push(`Unknown option: ${arg}`);
  } else {
    pairs.push(arg);
  }
}

if (pairs.length === 0) errors.push("Provide at least one foreground/background pair.");
const results = [];
for (const pair of pairs) {
  try {
    results.push(checkPair(pair, minimum));
  } catch (error) {
    errors.push(error instanceof Error ? error.message : String(error));
  }
}

if (json) {
  console.log(JSON.stringify({ minimum, results, errors }, null, 2));
} else {
  for (const result of results) {
    const labels = [
      `AA text: ${result.aaText ? "pass" : "fail"}`,
      `large text / essential UI: ${result.largeTextAndUI ? "pass" : "fail"}`,
    ];
    if (result.aaaText) labels.push("AAA text: pass");
    if (minimum !== null) labels.push(`minimum ${minimum}: ${result.meetsMinimum ? "pass" : "fail"}`);
    console.log(`${result.foreground} / ${result.background} = ${result.ratio.toFixed(4)}:1 (${labels.join(", ")})`);
  }
  for (const error of errors) console.error(error);
  if (pairs.length === 0) console.error(usage);
}

if (errors.length > 0) {
  process.exitCode = 2;
} else if (results.some((result) => result.meetsMinimum === false)) {
  process.exitCode = 1;
}
