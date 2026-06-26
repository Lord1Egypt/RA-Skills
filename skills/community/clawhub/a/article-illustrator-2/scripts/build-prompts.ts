#!/usr/bin/env bun
import path from "node:path";
import process from "node:process";
import { mkdir, readFile, writeFile } from "node:fs/promises";

type CliArgs = {
  outlinePath: string | null;
  outputDir: string | null;
  topic: string;
  audience: string;
  style: string;
  density: string;
  language: string;
  aspect: string;
  help: boolean;
};

type OutlineMeta = {
  seriesReference: string;
  seriesAnchors: string[];
};

type OutlineEntry = {
  index: number;
  position: string;
  purpose: string;
  visualContent: string;
  continuityAnchors: string[];
  filename: string;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/build-prompts.ts --outline outline.md --output-dir prompts [options]

Options:
  --outline <path>      Path to outline.md
  --output-dir <path>   Directory for generated prompt files
  --topic <text>        Article topic or section family (default: article section)
  --audience <text>     Target audience (default: general reader)
  --style <name>        Style direction (default: minimal)
  --density <name>      Density (default: per-section)
  --lang <code>         On-image text language when needed (default placeholder: en)
  --aspect <ratio>      Aspect ratio (default: 16:9)
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    outlinePath: null,
    outputDir: null,
    topic: "article section",
    audience: "general reader",
    style: "minimal",
    density: "per-section",
    language: "en",
    aspect: "16:9",
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--outline") args.outlinePath = argv[++i] ?? null;
    else if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--topic") args.topic = argv[++i] ?? args.topic;
    else if (current === "--audience") args.audience = argv[++i] ?? args.audience;
    else if (current === "--style") args.style = argv[++i] ?? args.style;
    else if (current === "--density") args.density = argv[++i] ?? args.density;
    else if (current === "--lang") args.language = argv[++i] ?? args.language;
    else if (current === "--aspect") args.aspect = argv[++i] ?? args.aspect;
    else if (current === "--help" || current === "-h") args.help = true;
  }

  return args;
}

function extractBullets(block: string, label: string): string[] {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = block.match(new RegExp(`\\*\\*${escaped}\\*\\*:\\s*\\n((?:- .+\\n?)*)`, "m"));
  if (!match?.[1]) return [];
  return match[1]
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "))
    .map((line) => line.slice(2).trim())
    .filter(Boolean);
}

function parseOutline(content: string): { meta: OutlineMeta; entries: OutlineEntry[] } {
  const normalized = content.replace(/\r\n/g, "\n");
  const meta: OutlineMeta = {
    seriesReference: normalized.match(/\*\*Series Reference\*\*:\s*(.+)/)?.[1]?.trim() ?? "references/series-reference.png",
    seriesAnchors: extractBullets(normalized, "Series Anchors"),
  };
  const blocks = normalized.split(/^## Illustration\s+/m).slice(1);
  const entries = blocks.map((block) => {
    const firstBreak = block.indexOf("\n");
    const index = Number.parseInt((firstBreak === -1 ? block : block.slice(0, firstBreak)).trim(), 10);
    const body = firstBreak === -1 ? "" : block.slice(firstBreak + 1);
    return {
      index,
      position: body.match(/\*\*Position\*\*:\s*(.+)/)?.[1]?.trim() ?? "",
      purpose: body.match(/\*\*Purpose\*\*:\s*(.+)/)?.[1]?.trim() ?? "",
      visualContent: body.match(/\*\*Visual Content\*\*:\s*(.+)/)?.[1]?.trim() ?? "",
      continuityAnchors: extractBullets(body, "Continuity Anchors"),
      filename: body.match(/\*\*Filename\*\*:\s*(.+)/)?.[1]?.trim() ?? "",
    };
  }).filter((entry) => Number.isFinite(entry.index) && entry.filename);
  return { meta, entries };
}

function inferTypeFromFilename(filename: string): string {
  const base = filename.replace(/\.(png|jpg|jpeg|webp)$/i, "");
  const parts = base.split("-");
  return parts[1] || "illustration";
}

function promptFileName(index: number, type: string): string {
  return `${String(index).padStart(2, "0")}-${type}-topic.md`;
}

function buildPrompt(
  entry: OutlineEntry,
  args: CliArgs,
  meta: OutlineMeta,
  previousEntry: OutlineEntry | null,
  nextEntry: OutlineEntry | null,
): string {
  const type = inferTypeFromFilename(entry.filename);
  const headingHint = entry.position.startsWith("after-heading:")
    ? entry.position.slice("after-heading:".length).trim()
    : entry.position.startsWith("before-heading:")
      ? entry.position.slice("before-heading:".length).trim()
      : args.topic;
  const seriesAnchors = meta.seriesAnchors.length
    ? meta.seriesAnchors.map((anchor) => `- ${anchor}`).join("\n")
    : "- <shared palette>\n- <shared recurring subject>\n- <shared diagram vocabulary>";
  const continuityAnchors = entry.continuityAnchors.length
    ? entry.continuityAnchors.map((anchor) => `- ${anchor}`).join("\n")
    : "- Keep the same palette, composition system, and recurring subject as the rest of the article illustrations.";
  const previousRecap = previousEntry
    ? `${previousEntry.purpose || "<previous illustration purpose>"} | ${previousEntry.visualContent || "<previous visual content>"}`
    : "Opening visual setup for the article.";
  const nextHook = nextEntry
    ? `${nextEntry.purpose || "<next illustration purpose>"} | ${nextEntry.visualContent || "<next visual content>"}`
    : "Final illustration or article wrap-up.";

  return `Create an article illustration for this section:
${headingHint || args.topic}

Illustration type: ${type}.
Style direction: ${args.style}.
Purpose: ${entry.purpose || "support the article section"}.
Language: ${args.language}.

Series reference:
- reference image: ${meta.seriesReference}
- priority rule: treat the series reference as the canonical source of truth for palette, recurring subject, diagram vocabulary, and composition rhythm

Visual content:
- main subject: ${entry.visualContent || "<main subject>"}
- supporting elements: <supporting elements>
- labels or keywords: <terms, numbers, short labels>

Series anchors:
${seriesAnchors}

Illustration continuity:
- previous section recap: ${previousRecap}
- current transition: keep the same article-level visual system and subject logic
- next section hook: ${nextHook}
- illustration-specific anchors:
${continuityAnchors}

Composition:
- focal point: ${entry.visualContent || "<main visual focus>"}
- density: ${args.density}
- aspect ratio: ${args.aspect}

Target audience: ${args.audience}.
Article topic: ${args.topic}.

Avoid: generic stock-photo feel, unrelated decorative objects, unreadable text, cluttered composition, watermark.
`;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }
  if (!args.outlinePath) {
    console.error("Error: --outline is required");
    process.exit(1);
  }
  if (!args.outputDir) {
    console.error("Error: --output-dir is required");
    process.exit(1);
  }

  const outline = await readFile(path.resolve(args.outlinePath), "utf8");
  const { meta, entries } = parseOutline(outline);
  if (entries.length === 0) {
    console.error("No illustration entries found in outline.");
    process.exit(1);
  }

  const outputDir = path.resolve(args.outputDir);
  await mkdir(outputDir, { recursive: true });

  for (const entry of entries) {
    const type = inferTypeFromFilename(entry.filename);
    const filePath = path.join(outputDir, promptFileName(entry.index, type));
    const previousEntry = entries.find((candidate) => candidate.index === entry.index - 1) ?? null;
    const nextEntry = entries.find((candidate) => candidate.index === entry.index + 1) ?? null;
    await writeFile(filePath, buildPrompt(entry, args, meta, previousEntry, nextEntry), "utf8");
  }

  console.log(`Prompts written: ${outputDir} (${entries.length} files)`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
