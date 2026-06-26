#!/usr/bin/env node
/**
 * 轻量扫描 Android / iOS 工程资源，输出与 generation 兼容的 JSON 报告。
 * Node.js 18+，无需额外 npm 包。
 */
import { readFileSync, readdirSync, statSync, existsSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

function normalizeHex(hex) {
  let h = hex.trim().toUpperCase();
  if (h.startsWith("#")) h = h.slice(1);
  if (h.length === 8) return `#${h.slice(2)}`;
  if (h.length === 6) return `#${h}`;
  return hex.startsWith("#") ? hex : `#${hex}`;
}

function parseAndroidColors(xml) {
  const out = {};
  const re = /<color\s+name="([^"]+)"[^>]*>([^<]+)<\/color>/g;
  let m;
  while ((m = re.exec(xml))) {
    out[m[1]] = m[2].trim();
  }
  return out;
}

function parseAndroidStrings(xml) {
  const out = {};
  const re = /<string\s+name="([^"]+)"[^>]*>([^<]*)<\/string>/g;
  let m;
  while ((m = re.exec(xml))) {
    out[m[1]] = m[2].trim();
  }
  return out;
}

function parseAndroidDimens(xml) {
  const out = {};
  const re = /<dimen\s+name="([^"]+)"[^>]*>([^<]+)<\/dimen>/g;
  let m;
  while ((m = re.exec(xml))) {
    out[m[1]] = m[2].trim();
  }
  return out;
}

function listDrawables(resDir) {
  const d = join(resDir, "drawable");
  if (!existsSync(d)) return [];
  return readdirSync(d)
    .filter((f) => /\.(xml|png|webp|jpg)$/i.test(f))
    .map((f) => f.replace(/\.[^.]+$/, ""));
}

function findAndroidModules(root) {
  const out = [];
  const settings = join(root, "settings.gradle");
  const settingsKts = join(root, "settings.gradle.kts");
  let content = "";
  if (existsSync(settingsKts)) content = readFileSync(settingsKts, "utf8");
  else if (existsSync(settings)) content = readFileSync(settings, "utf8");
  const re = /project\s*\(\s*['"](:([^'"]+))['"]\s*\)/g;
  let m;
  while ((m = re.exec(content))) {
    const name = m[2].replace(/:/g, "/");
    const pathGuess = join(root, name.startsWith("/") ? name.slice(1) : name);
    if (existsSync(join(pathGuess, "src", "main", "res"))) out.push(pathGuess);
  }
  const appRes = join(root, "app", "src", "main", "res");
  if (existsSync(appRes)) out.push(join(root, "app"));
  return [...new Set(out)];
}

function scanAndroidRoot(root) {
  const modules = findAndroidModules(root);
  const scanRoots = modules.length ? modules : [root];
  const colors = {};
  const strings = {};
  const dimens = {};
  const drawables = [];
  const notes = [];

  for (const mod of scanRoots) {
    const res = join(mod, "src", "main", "res");
    if (!existsSync(res)) continue;
    for (const name of ["values", "values-night"]) {
      const vd = join(res, name);
      if (!existsSync(vd)) continue;
      for (const f of readdirSync(vd)) {
        if (!f.endsWith(".xml")) continue;
        const p = join(vd, f);
        const xml = readFileSync(p, "utf8");
        Object.assign(colors, parseAndroidColors(xml));
        Object.assign(strings, parseAndroidStrings(xml));
        Object.assign(dimens, parseAndroidDimens(xml));
      }
    }
    drawables.push(...listDrawables(join(mod, "src", "main", "res")));
  }

  const indices = {
    colors: {},
    strings: {},
    text_styles: {},
  };
  for (const [k, v] of Object.entries(colors)) {
    const hex = normalizeHex(v);
    if (!indices.colors[hex]) indices.colors[hex] = [];
    indices.colors[hex].push(k);
  }
  for (const [k, v] of Object.entries(strings)) {
    if (!indices.strings[v]) indices.strings[v] = [];
    indices.strings[v].push(k);
  }

  return {
    platform: "android",
    root,
    modules: scanRoots,
    colors,
    strings,
    dimens,
    drawables: [...new Set(drawables)],
    indices,
    notes,
  };
}

function hasXcodeProject(dir) {
  try {
    return readdirSync(dir).some((f) => f.endsWith(".xcodeproj"));
  } catch {
    return false;
  }
}

function scanIosRoot(root) {
  const notes = ["iOS：当前为轻量扫描，仅检测工程结构；颜色/文案请结合 Asset Catalog 与 Localizable.strings 人工补充。"];
  return {
    platform: "ios",
    root,
    modules: [],
    colors: {},
    strings: {},
    dimens: {},
    drawables: [],
    indices: { colors: {}, strings: {}, text_styles: {} },
    notes,
  };
}

function detectPlatform(root) {
  if (existsSync(join(root, "build.gradle")) || existsSync(join(root, "build.gradle.kts")))
    return "android";
  if (hasXcodeProject(root)) return "ios";
  if (existsSync(join(root, "app", "build.gradle"))) return "android";
  return "unknown";
}

function parseArgs(argv) {
  const args = [...argv];
  let jsonPretty = false;
  let output = null;
  const positional = [];
  while (args.length) {
    const x = args.shift();
    if (x === "--json") jsonPretty = true;
    else if (x === "--output" || x === "-o") output = args.shift() ?? null;
    else if (!x.startsWith("-")) positional.push(x);
    else throw new Error(`Unknown: ${x}`);
  }
  return { jsonPretty, output, positional };
}

function main() {
  const { jsonPretty, output, positional } = parseArgs(process.argv.slice(2));
  if (positional.length < 1) {
    console.error("Usage: node src/project-scan.js <project-root> [--json] [--output scan-report.json]");
    process.exit(1);
  }
  const root = resolve(positional[0]);
  if (!statSync(root).isDirectory()) {
    console.error(`Not a directory: ${root}`);
    process.exit(1);
  }

  const plat = detectPlatform(root);
  let report;
  if (plat === "android") report = scanAndroidRoot(root);
  else if (plat === "ios") report = scanIosRoot(root);
  else {
    report = {
      platform: "unknown",
      root,
      modules: [],
      colors: {},
      strings: {},
      dimens: {},
      drawables: [],
      indices: { colors: {}, strings: {}, text_styles: {} },
      notes: ["未能识别为 Android Gradle 或 Xcode 工程，报告为空。"],
    };
  }

  const text = JSON.stringify(report, null, jsonPretty ? 2 : 0);
  if (output) {
    writeFileSync(resolve(output), text, "utf8");
    console.error(`Wrote ${output}`);
  }
  console.log(text);
}

try {
  main();
} catch (e) {
  console.error(e instanceof Error ? e.message : e);
  process.exit(1);
}
