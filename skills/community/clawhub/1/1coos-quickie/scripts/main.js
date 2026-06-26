// @bun
// skills/1coos-quickie/scripts/main.ts
import { parseArgs } from "util";
import { resolve, dirname, join } from "path";
import { mkdirSync } from "fs";

// skills/1coos-quickie/scripts/url-extractor.ts
function extractFirstUrl(text) {
  const urlRegex = /https?:\/\/[^\s<>\[\]\uFF08\uFF09\u3010\u3011\u300C\u300D\u300A\u300B\u3000-\u303F\uFF00-\uFFEF\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF\u2E80-\u2EFF\u3000-\u303F\uFE30-\uFE4F]+/i;
  const match = text.match(urlRegex);
  if (!match)
    return null;
  let url = match[0];
  url = url.replace(/[.,;:!?'"\uFF09\u300B\u300D\u3011\u3002\uFF0C\uFF1B\uFF1A\uFF01\uFF1F]+$/, "");
  while (url.endsWith(")")) {
    const openParens = (url.match(/\(/g) || []).length;
    const closeParens = (url.match(/\)/g) || []).length;
    if (closeParens > openParens) {
      url = url.slice(0, -1);
    } else {
      break;
    }
  }
  return url;
}

// skills/1coos-quickie/scripts/reader.ts
var DEFAULT_READER_CONFIG = {
  timeout: 120000
};
async function checkUvxAvailable() {
  try {
    const proc = Bun.spawn(["which", "uvx"], {
      stdout: "pipe",
      stderr: "pipe"
    });
    const exitCode = await proc.exited;
    return exitCode === 0;
  } catch {
    return false;
  }
}
async function fetchWithXReader(url, config = {}) {
  const fullConfig = { ...DEFAULT_READER_CONFIG, ...config };
  if (!await checkUvxAvailable()) {
    return {
      success: false,
      markdown: "",
      title: "",
      error: "uvx is not installed. Please install uv first: https://docs.astral.sh/uv/getting-started/installation/"
    };
  }
  const args = [
    "uvx",
    "--from",
    "x-reader[all] @ git+https://github.com/runesleo/x-reader.git",
    "x-reader",
    url
  ];
  try {
    const proc = Bun.spawn(args, {
      stdout: "pipe",
      stderr: "pipe"
    });
    const result = await Promise.race([
      (async () => {
        const exitCode = await proc.exited;
        const stdout = await new Response(proc.stdout).text();
        const stderr = await new Response(proc.stderr).text();
        return { exitCode, stdout, stderr, timedOut: false };
      })(),
      new Promise((resolve) => setTimeout(() => {
        proc.kill();
        resolve({
          exitCode: -1,
          stdout: "",
          stderr: "",
          timedOut: true
        });
      }, fullConfig.timeout))
    ]);
    if (result.timedOut) {
      return {
        success: false,
        markdown: "",
        title: "",
        error: `Fetch timed out (${fullConfig.timeout / 1000}s)`
      };
    }
    if (result.exitCode !== 0) {
      return {
        success: false,
        markdown: "",
        title: "",
        error: `x-reader failed (exit ${result.exitCode}): ${result.stderr.trim()}`
      };
    }
    const markdown = result.stdout;
    if (!markdown.trim()) {
      return {
        success: false,
        markdown: "",
        title: "",
        error: "x-reader produced empty output \u2014 URL may not be accessible"
      };
    }
    const title = extractTitle(markdown, url);
    return { success: true, markdown, title };
  } catch (err) {
    return {
      success: false,
      markdown: "",
      title: "",
      error: `Fetch error: ${String(err)}`
    };
  }
}
function extractTitle(markdown, fallbackUrl) {
  const headingMatch = markdown.match(/^#\s+(.+)$/m);
  if (headingMatch) {
    return headingMatch[1].trim();
  }
  try {
    return new URL(fallbackUrl).hostname;
  } catch {
    return "untitled";
  }
}

// skills/1coos-quickie/scripts/formatter.ts
var DEFAULT_FORMATTING_CONFIG = {
  maxWidth: 80,
  listMarker: "-"
};
function splitByCodeBlocks(content) {
  const segments = [];
  const lines = content.split(`
`);
  let inCodeBlock = false;
  let currentLines = [];
  let codeFence = "";
  for (const line of lines) {
    const fenceMatch = line.match(/^(`{3,}|~{3,})/);
    if (!inCodeBlock && fenceMatch) {
      if (currentLines.length > 0) {
        segments.push({ type: "text", content: currentLines.join(`
`) });
        currentLines = [];
      }
      inCodeBlock = true;
      codeFence = fenceMatch[1][0];
      currentLines.push(line);
    } else if (inCodeBlock && line.match(new RegExp(`^${codeFence}{3,}\\s*$`))) {
      currentLines.push(line);
      segments.push({ type: "code", content: currentLines.join(`
`) });
      currentLines = [];
      inCodeBlock = false;
      codeFence = "";
    } else {
      currentLines.push(line);
    }
  }
  if (currentLines.length > 0) {
    segments.push({
      type: inCodeBlock ? "code" : "text",
      content: currentLines.join(`
`)
    });
  }
  return segments;
}
function applyToTextSegments(content, transform) {
  const segments = splitByCodeBlocks(content);
  return segments.map((seg) => seg.type === "text" ? transform(seg.content) : seg.content).join(`
`);
}
function normalizeLineEndings(content, _config) {
  let result = content.replace(/^\uFEFF/, "");
  result = result.replace(/\r\n/g, `
`);
  result = result.replace(/\r/g, `
`);
  return result;
}
function normalizeWhitespace(content, _config) {
  return applyToTextSegments(content, (text) => {
    let result = text.replace(/[ \t]+$/gm, "");
    result = result.replace(/\n{3,}/g, `

`);
    return result;
  });
}
function normalizeHeadings(content, _config) {
  return applyToTextSegments(content, (text) => {
    return text.replace(/^(#{1,6})([^ #\n])/gm, "$1 $2");
  });
}
function normalizeListMarkers(content, config) {
  const marker = config.listMarker;
  return applyToTextSegments(content, (text) => {
    return text.replace(/^(\s*)[*+](\s)/gm, `$1${marker}$2`);
  });
}
function normalizeCodeBlocks(content, _config) {
  const lines = content.split(`
`);
  const result = [];
  let inCodeBlock = false;
  for (let i = 0;i < lines.length; i++) {
    const line = lines[i];
    const isFence = /^(`{3,}|~{3,})/.test(line);
    if (isFence && !inCodeBlock) {
      if (result.length > 0 && result[result.length - 1] !== "") {
        result.push("");
      }
      inCodeBlock = true;
      result.push(line);
    } else if (isFence && inCodeBlock) {
      inCodeBlock = false;
      result.push(line);
      if (i + 1 < lines.length && lines[i + 1] !== "") {
        result.push("");
      }
    } else {
      result.push(line);
    }
  }
  return result.join(`
`);
}
function normalizeBlockquotes(content, _config) {
  return applyToTextSegments(content, (text) => {
    return text.replace(/^(>+)([^ >\n])/gm, "$1 $2");
  });
}
function normalizeProperties(content, _config) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch)
    return content;
  const fmContent = fmMatch[1];
  const lines = fmContent.split(`
`);
  const normalizedLines = [];
  for (const line of lines) {
    const kvMatch = line.match(/^(\s*)(\w[\w-]*):\s*(.*)/);
    if (kvMatch) {
      const [, indent, key, value] = kvMatch;
      normalizedLines.push(`${indent}${key}: ${value}`);
    } else {
      normalizedLines.push(line);
    }
  }
  return content.replace(fmMatch[0], `---
${normalizedLines.join(`
`)}
---`);
}
function convertToWikilinks(content, _config) {
  return applyToTextSegments(content, (text) => {
    return text.replace(/\[([^\]]+)\]\(([^)]+?)(?:\.md)?\)/g, (_match, displayText, target) => {
      if (/^https?:\/\//.test(target) || target.startsWith("#")) {
        return _match;
      }
      const name = target.replace(/\.md$/, "");
      if (displayText === name || displayText === target) {
        return `[[${name}]]`;
      }
      return `[[${name}|${displayText}]]`;
    });
  });
}
function normalizeCallouts(content, _config) {
  return applyToTextSegments(content, (text) => {
    let result = text.replace(/^(>\s*)\[!\s*(\w+)\s*\]/gm, "$1[!$2]");
    const lines = result.split(`
`);
    const output = [];
    let inCallout = false;
    for (const line of lines) {
      if (/^>\s*\[!\w+\]/.test(line)) {
        inCallout = true;
        output.push(line);
        continue;
      }
      if (inCallout && /^>/.test(line)) {
        output.push(line);
        continue;
      }
      if (inCallout && line.trim() === "") {
        inCallout = false;
      }
      output.push(line);
    }
    return output.join(`
`);
  });
}
function normalizeHighlights(content, _config) {
  return applyToTextSegments(content, (text) => {
    return text.replace(/==\s+([^=]+?)\s+==/g, "==$1==");
  });
}
function formatTables(content, _config) {
  return applyToTextSegments(content, (text) => {
    const lines = text.split(`
`);
    const result = [];
    let tableLines = [];
    let inTable = false;
    const flushTable = () => {
      if (tableLines.length >= 2) {
        result.push(...alignTable(tableLines));
      } else {
        result.push(...tableLines);
      }
      tableLines = [];
      inTable = false;
    };
    for (const line of lines) {
      const isTableLine = /^\s*\|/.test(line) && /\|\s*$/.test(line);
      if (isTableLine) {
        inTable = true;
        tableLines.push(line);
      } else {
        if (inTable)
          flushTable();
        result.push(line);
      }
    }
    if (inTable)
      flushTable();
    return result.join(`
`);
  });
}
function alignTable(lines) {
  const rows = lines.map((line) => line.replace(/^\s*\|\s*/, "").replace(/\s*\|\s*$/, "").split(/\s*\|\s*/));
  const colCount = Math.max(...rows.map((r) => r.length));
  const colWidths = Array(colCount).fill(0);
  for (const row of rows) {
    for (let i = 0;i < row.length; i++) {
      const cell = row[i];
      if (!/^[-:]+$/.test(cell)) {
        colWidths[i] = Math.max(colWidths[i], cell.length);
      }
    }
  }
  for (let i = 0;i < colWidths.length; i++) {
    colWidths[i] = Math.max(colWidths[i], 3);
  }
  return rows.map((row) => {
    const cells = row.map((cell, i) => {
      const width = colWidths[i] || 3;
      if (/^[-:]+$/.test(cell)) {
        const leftAlign = cell.startsWith(":");
        const rightAlign = cell.endsWith(":");
        if (leftAlign && rightAlign) {
          return ":" + "-".repeat(width - 2) + ":";
        } else if (rightAlign) {
          return "-".repeat(width - 1) + ":";
        } else if (leftAlign) {
          return ":" + "-".repeat(width - 1);
        }
        return "-".repeat(width);
      }
      return cell.padEnd(width);
    });
    return "| " + cells.join(" | ") + " |";
  });
}
function ensureTrailingNewline(content, _config) {
  return content.replace(/\n*$/, `
`);
}
var OBSIDIAN_PIPELINE = [
  normalizeLineEndings,
  normalizeWhitespace,
  normalizeHeadings,
  normalizeListMarkers,
  normalizeCodeBlocks,
  normalizeBlockquotes,
  normalizeProperties,
  convertToWikilinks,
  normalizeCallouts,
  normalizeHighlights,
  formatTables,
  ensureTrailingNewline
];
function formatObsidian(content, config = {}) {
  const fullConfig = { ...DEFAULT_FORMATTING_CONFIG, ...config };
  return OBSIDIAN_PIPELINE.reduce((text, transform) => transform(text, fullConfig), content);
}

// skills/1coos-quickie/scripts/main.ts
var DEFAULT_CONFIG = {
  outputDir: join(resolve(dirname(import.meta.dir)), "output"),
  raw: false,
  formatting: DEFAULT_FORMATTING_CONFIG,
  reader: DEFAULT_READER_CONFIG
};
async function loadConfig(configPath) {
  const file = Bun.file(configPath);
  if (!await file.exists())
    return {};
  try {
    return await file.json();
  } catch {
    console.error(`Warning: failed to parse config file: ${configPath}`);
    return {};
  }
}
function mergeConfig(fileConfig, cliOverrides) {
  return {
    outputDir: cliOverrides.outputDir ?? fileConfig.outputDir ?? DEFAULT_CONFIG.outputDir,
    raw: cliOverrides.raw ?? fileConfig.raw ?? DEFAULT_CONFIG.raw,
    formatting: {
      ...DEFAULT_CONFIG.formatting,
      ...fileConfig.formatting || {},
      ...cliOverrides.formatting || {}
    },
    reader: {
      ...DEFAULT_CONFIG.reader,
      ...fileConfig.reader || {},
      ...cliOverrides.reader || {}
    }
  };
}
function sanitizeFilename(name) {
  return name.replace(/[<>:"/\\|?*\x00-\x1f]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "").slice(0, 100);
}
function generateOutputFilename(title, url) {
  const sanitized = sanitizeFilename(title);
  if (sanitized.length >= 3) {
    return `${sanitized}.md`;
  }
  try {
    const domain = new URL(url).hostname.replace(/\./g, "-");
    const ts = new Date().toISOString().slice(0, 10);
    return `${domain}-${ts}.md`;
  } catch {
    return `quickie-${Date.now().toString(36)}.md`;
  }
}
var HELP_TEXT = `
1coos-quickie

Grab URL content and save as formatted Obsidian-style Markdown.

Usage:
  bun run main.ts <text-with-url> [options]

Arguments:
  <text>                    Any text containing a URL to fetch

Options:
  -o, --output-dir <path>   Output directory
  -c, --config <path>       Config file path (default: ../config.json)
  --raw                     Skip formatting, output raw x-reader result
  -h, --help                Show help

Supported platforms:
  YouTube, Bilibili, Twitter/X, WeChat, Xiaohongshu, Telegram, RSS, any URL

Examples:
  bun run main.ts "https://www.youtube.com/watch?v=xxx"
  bun run main.ts "\u770B\u770B\u8FD9\u4E2A https://x.com/user/status/123"
  bun run main.ts "https://example.com/article" --output-dir ~/notes
`;
async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      help: { type: "boolean", short: "h" },
      "output-dir": { type: "string", short: "o" },
      config: { type: "string", short: "c" },
      raw: { type: "boolean" }
    },
    allowPositionals: true
  });
  if (values.help) {
    console.log(HELP_TEXT);
    process.exit(0);
  }
  const inputText = positionals.join(" ");
  if (!inputText.trim()) {
    console.error("Error: please provide text containing a URL");
    console.error("Use --help for usage information");
    process.exit(2);
  }
  const url = extractFirstUrl(inputText);
  if (!url) {
    console.error("Error: no valid URL found in the provided text");
    console.error(`Input: "${inputText}"`);
    process.exit(2);
  }
  console.log(`URL: ${url}`);
  const skillDir = resolve(dirname(import.meta.dir));
  const configPath = values.config ? resolve(values.config) : join(skillDir, "config.json");
  const fileConfig = await loadConfig(configPath);
  const cliOverrides = {};
  if (values["output-dir"]) {
    cliOverrides.outputDir = values["output-dir"];
  }
  if (values.raw) {
    cliOverrides.raw = true;
  }
  const config = mergeConfig(fileConfig, cliOverrides);
  console.log("Fetching content...");
  const fetchResult = await fetchWithXReader(url, config.reader);
  if (!fetchResult.success) {
    console.error(`Fetch failed: ${fetchResult.error}`);
    if (fetchResult.error?.includes("uvx is not installed")) {
      process.exit(3);
    }
    process.exit(4);
  }
  let markdown = fetchResult.markdown;
  console.log(`Fetched: "${fetchResult.title}" (${markdown.length} chars)`);
  if (!config.raw) {
    console.log("Formatting (obsidian style)...");
    markdown = formatObsidian(markdown, config.formatting);
    console.log(`Formatted (${markdown.length} chars)`);
  }
  const outputDir = resolve(config.outputDir);
  const outputFileName = generateOutputFilename(fetchResult.title, url);
  const outputPath = join(outputDir, outputFileName);
  try {
    mkdirSync(outputDir, { recursive: true });
    await Bun.write(outputPath, markdown);
    console.log(`Output: ${outputPath}`);
  } catch (err) {
    console.error(`Failed to write output: ${String(err)}`);
    process.exit(5);
  }
}
main().catch((err) => {
  console.error(`Unexpected error: ${err}`);
  process.exit(1);
});
