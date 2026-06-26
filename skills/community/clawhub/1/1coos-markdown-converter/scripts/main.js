// @bun
// skills/1coos-markdown-converter/scripts/main.ts
import { parseArgs } from "util";
import { resolve, dirname, basename, extname, join } from "path";
import { mkdirSync } from "fs";

// skills/1coos-markdown-converter/scripts/converter.ts
var DEFAULT_CONVERTER_CONFIG = {
  timeout: 60000,
  charset: "UTF-8"
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
async function convertToMarkdown(inputPath, config = {}) {
  const fullConfig = { ...DEFAULT_CONVERTER_CONFIG, ...config };
  const file = Bun.file(inputPath);
  if (!await file.exists()) {
    return {
      success: false,
      markdown: "",
      error: `File not found: ${inputPath}`
    };
  }
  if (!await checkUvxAvailable()) {
    return {
      success: false,
      markdown: "",
      error: "uvx is not installed. Please install uv first: https://docs.astral.sh/uv/getting-started/installation/"
    };
  }
  const args = ["uvx", "markitdown[all]", inputPath];
  if (fullConfig.charset) {
    args.push("-c", fullConfig.charset);
  }
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
        error: `Conversion timed out (${fullConfig.timeout / 1000}s)`
      };
    }
    if (result.exitCode !== 0) {
      return {
        success: false,
        markdown: "",
        error: `markitdown failed (exit ${result.exitCode}): ${result.stderr.trim()}`
      };
    }
    const markdown = result.stdout;
    if (!markdown.trim()) {
      return {
        success: false,
        markdown: "",
        error: "Conversion produced empty output \u2014 file format may not be supported"
      };
    }
    return { success: true, markdown };
  } catch (err) {
    return {
      success: false,
      markdown: "",
      error: `Conversion error: ${String(err)}`
    };
  }
}

// skills/1coos-markdown-converter/scripts/formatter.ts
var DEFAULT_FORMATTING_CONFIG = {
  maxWidth: 80,
  listMarker: "-",
  emphasisMarker: "*",
  strongMarker: "**",
  codeBlockStyle: "fenced"
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
function ensureTrailingNewline(content, _config) {
  return content.replace(/\n*$/, `
`);
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
        const formatted = alignTable(tableLines);
        result.push(...formatted);
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
function strictHeadingLevels(content, _config) {
  return applyToTextSegments(content, (text) => {
    const lines = text.split(`
`);
    let lastLevel = 0;
    const result = [];
    for (const line of lines) {
      const match = line.match(/^(#{1,6})\s/);
      if (match) {
        let level = match[1].length;
        if (lastLevel > 0 && level > lastLevel + 1) {
          level = lastLevel + 1;
        }
        lastLevel = level;
        result.push("#".repeat(level) + line.slice(match[1].length));
      } else {
        result.push(line);
      }
    }
    return result.join(`
`);
  });
}
function removeExcessiveFormatting(content, _config) {
  return applyToTextSegments(content, (text) => {
    let result = text.replace(/\*\*\*\*/g, "");
    result = result.replace(/\*\*/g, (match, offset, str) => {
      const after = str.slice(offset + 2);
      if (after.startsWith("**"))
        return "";
      return match;
    });
    result = result.replace(/(?<!\*)\*([^*]*)\*(?!\*)/g, (match, inner) => {
      return inner.trim() === "" ? "" : match;
    });
    return result;
  });
}
function simplifyLinks(content, _config) {
  return applyToTextSegments(content, (text) => {
    return text.replace(/\[([^\]]+)\]\((\1)\)/g, "<$1>");
  });
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
    for (let i = 0;i < lines.length; i++) {
      const line = lines[i];
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
function normalizeHighlights(content, _config) {
  return applyToTextSegments(content, (text) => {
    return text.replace(/==\s+([^=]+?)\s+==/g, "==$1==");
  });
}
var COMMON_TRANSFORMS = [
  normalizeLineEndings,
  normalizeWhitespace,
  normalizeHeadings,
  normalizeListMarkers,
  normalizeCodeBlocks,
  normalizeBlockquotes
];
var STYLE_PIPELINES = {
  github: [...COMMON_TRANSFORMS, formatTables, ensureTrailingNewline],
  commonmark: [
    ...COMMON_TRANSFORMS,
    strictHeadingLevels,
    ensureTrailingNewline
  ],
  clean: [
    ...COMMON_TRANSFORMS,
    removeExcessiveFormatting,
    simplifyLinks,
    ensureTrailingNewline
  ],
  obsidian: [
    ...COMMON_TRANSFORMS,
    normalizeProperties,
    convertToWikilinks,
    normalizeCallouts,
    normalizeHighlights,
    formatTables,
    ensureTrailingNewline
  ]
};
function formatMarkdown(content, style = "obsidian", config = {}) {
  const fullConfig = { ...DEFAULT_FORMATTING_CONFIG, ...config };
  const pipeline = STYLE_PIPELINES[style];
  if (!pipeline) {
    throw new Error(`Unsupported style: ${style}`);
  }
  return pipeline.reduce((text, transform) => transform(text, fullConfig), content);
}

// skills/1coos-markdown-converter/scripts/main.ts
var DEFAULT_CONFIG = {
  style: "obsidian",
  outputDir: join(resolve(dirname(import.meta.dir)), "output"),
  convertOnly: false,
  formatting: DEFAULT_FORMATTING_CONFIG,
  converter: DEFAULT_CONVERTER_CONFIG
};
async function loadConfig(configPath) {
  const file = Bun.file(configPath);
  if (!await file.exists()) {
    return {};
  }
  try {
    return await file.json();
  } catch {
    console.error(`Warning: failed to parse config file: ${configPath}`);
    return {};
  }
}
function mergeConfig(fileConfig, cliOverrides) {
  return {
    style: cliOverrides.style ?? fileConfig.style ?? DEFAULT_CONFIG.style,
    outputDir: cliOverrides.outputDir ?? fileConfig.outputDir ?? DEFAULT_CONFIG.outputDir,
    convertOnly: cliOverrides.convertOnly ?? fileConfig.convertOnly ?? DEFAULT_CONFIG.convertOnly,
    formatting: {
      ...DEFAULT_CONFIG.formatting,
      ...fileConfig.formatting || {},
      ...cliOverrides.formatting || {}
    },
    converter: {
      ...DEFAULT_CONFIG.converter,
      ...fileConfig.converter || {},
      ...cliOverrides.converter || {}
    }
  };
}
var HELP_TEXT = `
1coos-markdown-converter

Convert files to beautifully formatted Markdown.

Usage:
  bun run main.ts <file-path> [options]

Arguments:
  <file-path>              Path to the file to convert

Options:
  -s, --style <style>      Formatting style: obsidian (default), github, commonmark, clean
  -o, --output-dir <path>   Output directory (default: skills/1coos-markdown-converter/output)
  -c, --config <path>      Config file path (default: ../config.json)
  --convert-only           Convert only, skip formatting step
  -h, --help               Show help

Supported formats:
  PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx/.xls),
  HTML, CSV, JSON, XML, Images (OCR), Audio (transcription), ZIP, EPub

Examples:
  bun run main.ts report.pdf
  bun run main.ts doc.docx --style clean --output-dir ~/notes
  bun run main.ts data.xlsx --convert-only
`;
var VALID_STYLES = ["obsidian", "github", "commonmark", "clean"];
async function main() {
  const { values, positionals } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      help: { type: "boolean", short: "h" },
      style: { type: "string", short: "s" },
      "output-dir": { type: "string", short: "o" },
      config: { type: "string", short: "c" },
      "convert-only": { type: "boolean" }
    },
    allowPositionals: true
  });
  if (values.help) {
    console.log(HELP_TEXT);
    process.exit(0);
  }
  if (positionals.length === 0) {
    console.error("Error: please provide a file path to convert");
    console.error("Use --help for usage information");
    process.exit(2);
  }
  const inputPath = resolve(positionals[0]);
  const inputFile = Bun.file(inputPath);
  if (!await inputFile.exists()) {
    console.error(`Error: file not found: ${inputPath}`);
    process.exit(2);
  }
  const skillDir = resolve(dirname(import.meta.dir));
  const configPath = values.config ? resolve(values.config) : join(skillDir, "config.json");
  const fileConfig = await loadConfig(configPath);
  const cliOverrides = {};
  if (values.style) {
    if (!VALID_STYLES.includes(values.style)) {
      console.error(`Error: invalid style "${values.style}", available: ${VALID_STYLES.join(", ")}`);
      process.exit(2);
    }
    cliOverrides.style = values.style;
  }
  if (values["output-dir"]) {
    cliOverrides.outputDir = values["output-dir"];
  }
  if (values["convert-only"]) {
    cliOverrides.convertOnly = true;
  }
  const config = mergeConfig(fileConfig, cliOverrides);
  const outputDir = resolve(config.outputDir);
  const outputFileName = basename(inputPath, extname(inputPath)) + ".md";
  const outputPath = join(outputDir, outputFileName);
  console.log(`Converting: ${inputPath}`);
  const convertResult = await convertToMarkdown(inputPath, config.converter);
  if (!convertResult.success) {
    console.error(`Conversion failed: ${convertResult.error}`);
    process.exit(4);
  }
  let markdown = convertResult.markdown;
  console.log(`Converted (${markdown.length} chars)`);
  if (!config.convertOnly) {
    console.log(`Formatting (${config.style} style)...`);
    markdown = formatMarkdown(markdown, config.style, config.formatting);
    console.log(`Formatted (${markdown.length} chars)`);
  }
  mkdirSync(outputDir, { recursive: true });
  await Bun.write(outputPath, markdown);
  console.log(`Output: ${outputPath}`);
}
main().catch((err) => {
  console.error(`Unexpected error: ${err}`);
  process.exit(1);
});
