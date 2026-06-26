#!/usr/bin/env bun
import process from "node:process";
import { mkdir, writeFile, access, readFile } from "node:fs/promises";
import { constants } from "node:fs";
import path from "node:path";

type CliArgs = {
  outputDir: string | null;
  articlePath: string | null;
  topic: string;
  audience: string;
  style: string;
  density: string;
  language: string;
  aspect: string;
  illustrations: number;
  force: boolean;
  help: boolean;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/scaffold.ts --output-dir illustrations/topic-slug --topic "Topic" [options]

Options:
  --output-dir <path>      Target illustration working directory
  --article <path>         Optional article markdown path used to derive real heading positions
  --topic <text>           Article topic or summary
  --audience <text>        Audience placeholder (default: general reader)
  --style <name>           Illustration style (default: minimal)
  --density <name>         Illustration density (default: per-section)
  --lang <code>            On-image text language when needed (default placeholder: en)
  --aspect <ratio>         Aspect ratio (default: 16:9)
  --illustrations <count>  Number of illustration slots to scaffold (default: 3)
  --force                  Overwrite existing files
  -h, --help               Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    outputDir: null,
    articlePath: null,
    topic: "Topic",
    audience: "general reader",
    style: "minimal",
    density: "per-section",
    language: "en",
    aspect: "16:9",
    illustrations: 3,
    force: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--article") args.articlePath = argv[++i] ?? null;
    else if (current === "--topic") args.topic = argv[++i] ?? args.topic;
    else if (current === "--audience") args.audience = argv[++i] ?? args.audience;
    else if (current === "--style") args.style = argv[++i] ?? args.style;
    else if (current === "--density") args.density = argv[++i] ?? args.density;
    else if (current === "--lang") args.language = argv[++i] ?? args.language;
    else if (current === "--aspect") args.aspect = argv[++i] ?? args.aspect;
    else if (current === "--illustrations") {
      const value = parseInt(argv[++i] ?? "", 10);
      if (Number.isFinite(value) && value >= 1) args.illustrations = value;
    } else if (current === "--force") args.force = true;
    else if (current === "--help" || current === "-h") args.help = true;
  }

  return args;
}

async function exists(filePath: string): Promise<boolean> {
  try {
    await access(filePath, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function writeScaffoldFile(filePath: string, content: string, force: boolean): Promise<void> {
  if (!force && (await exists(filePath))) {
    throw new Error(`File already exists: ${filePath}. Use --force to overwrite.`);
  }
  await writeFile(filePath, content, "utf8");
}

function suggestedType(index: number, total: number): string {
  if (index === 1) return "framework";
  if (index === total) return "summary";
  if (index === 2) return "flowchart";
  if (index === 3) return "scene";
  return "comparison";
}

function suggestedHeading(index: number): string {
  if (index === 1) return "Background";
  if (index === 2) return "Method";
  if (index === 3) return "Example";
  return `Section ${index}`;
}

type ArticleHeading = {
  depth: number;
  text: string;
};

function normalizeHeadingText(text: string): string {
  return text
    .replace(/\s+#+\s*$/, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractArticleHeadings(content: string): ArticleHeading[] {
  const headings: ArticleHeading[] = [];
  const lines = content.replace(/\r\n/g, "\n").split("\n");

  for (let index = 0; index < lines.length; index++) {
    const line = lines[index] ?? "";
    const atx = line.match(/^\s{0,3}(#{1,6})\s+(.+?)\s*$/);
    if (atx) {
      const text = normalizeHeadingText(atx[2] ?? "");
      if (text) headings.push({ depth: atx[1]!.length, text });
      continue;
    }

    const next = lines[index + 1] ?? "";
    const setext = next.match(/^\s{0,3}(=+|-+)\s*$/);
    if (!setext) continue;
    const text = normalizeHeadingText(line);
    if (!text) continue;
    headings.push({ depth: setext[1]![0] === "=" ? 1 : 2, text });
    index += 1;
  }

  return headings;
}

function selectHeadingPositions(headings: ArticleHeading[], count: number): string[] {
  const primary = headings.filter((heading) => heading.depth >= 2);
  const candidates = primary.length > 0 ? primary : headings;
  const selected: string[] = [];
  const seen = new Set<string>();

  for (const heading of candidates) {
    if (seen.has(heading.text)) continue;
    selected.push(heading.text);
    seen.add(heading.text);
    if (selected.length >= count) break;
  }

  return selected;
}

function promptFileName(index: number, type: string): string {
  return `${String(index).padStart(2, "0")}-${type}-topic.md`;
}

function imageFileName(index: number, type: string): string {
  return `${String(index).padStart(2, "0")}-${type}-topic.png`;
}

function outlineTemplate(args: CliArgs, headingPositions: string[]): string {
  const blocks = Array.from({ length: args.illustrations }, (_, offset) => {
    const index = offset + 1;
    const type = suggestedType(index, args.illustrations);
    const suggestedPosition = headingPositions[offset] ?? suggestedHeading(index);
    return `## Illustration ${index}
**Position**: after-heading: ${suggestedPosition}
**Purpose**: <why this image helps the reader here>
**Visual Content**: <what should be shown for this section>
**Continuity Anchors**:
- <what must stay visually consistent: palette, device, product, presenter, diagram style, framing>
**Filename**: ${imageFileName(index, type)}
`;
  }).join("\n");

  return `# Illustration Outline

**Topic**: ${args.topic}
**Audience**: ${args.audience}
**Style**: ${args.style}
**Density**: ${args.density}
**Language**: ${args.language}
**Aspect**: ${args.aspect}
**Illustration Count**: ${args.illustrations}
**Series Reference**: references/series-reference.png
**Series Anchors**:
- <overall palette / brand colors>
- <repeating subject / product / presenter / diagram vocabulary>
- <shared composition rules and annotation style>

${blocks}`;
}

function seriesReferenceTemplate(args: CliArgs): string {
  return `Create a canonical article-illustration series reference image for: ${args.topic}.

Purpose: establish the shared visual system for all illustrations in this article.
Target audience: ${args.audience}.
Style direction: ${args.style}.
Density: ${args.density}.
Language: ${args.language}.
Aspect ratio: ${args.aspect}.

Include:
- the overall palette and rendering treatment
- the recurring subject, product, presenter, or diagram vocabulary when relevant
- the preferred annotation, label, and spacing system
- the composition rhythm that later illustrations should reuse

This is not one article section image. It is the canonical visual reference for the full illustration set.
Avoid: random style switching, stock-photo inconsistency, clutter, unreadable labels, watermark.
`;
}

function promptTemplate(args: CliArgs, index: number): string {
  const type = suggestedType(index, args.illustrations);
  return `Create an article illustration for this section:
${args.topic}

Illustration type: ${type}.
Style direction: ${args.style}.
Purpose: <why this image exists>.
Language: ${args.language}.

Series reference:
- reference image: references/series-reference.png
- priority rule: treat the series reference as the canonical source of truth for palette, recurring subject, diagram vocabulary, and composition rhythm

Visual content:
- main subject: <main subject>
- supporting elements: <supporting elements>
- labels or keywords: <terms, numbers, short labels>

Series anchors:
- shared palette: <shared palette>
- recurring subject / product / presenter: <shared recurring subject>
- shared diagram / annotation style: <shared visual system>

Illustration continuity:
- previous section recap: <what the previous illustration established>
- current transition: <how this illustration fits the same article series>
- next section hook: <what should carry into the next illustration>

Composition:
- focal point: <main visual focus>
- density: ${args.density}
- aspect ratio: ${args.aspect}

Target audience: ${args.audience}.

Avoid: generic stock-photo feel, unrelated decorative objects, unreadable text, cluttered composition, watermark.
`;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }
  if (!args.outputDir) {
    console.error("Error: --output-dir is required");
    process.exit(1);
  }

  const outputDir = path.resolve(args.outputDir);
  const promptsDir = path.join(outputDir, "prompts");
  const referencesDir = path.join(outputDir, "references");
  let headingPositions: string[] = [];
  if (args.articlePath) {
    const articleContent = await readFile(path.resolve(args.articlePath), "utf8");
    headingPositions = selectHeadingPositions(extractArticleHeadings(articleContent), args.illustrations);
  }
  await mkdir(promptsDir, { recursive: true });
  await mkdir(referencesDir, { recursive: true });

  await writeScaffoldFile(path.join(outputDir, "outline.md"), outlineTemplate(args, headingPositions), args.force);
  await writeScaffoldFile(path.join(referencesDir, "series-reference.md"), seriesReferenceTemplate(args), args.force);
  for (let index = 1; index <= args.illustrations; index++) {
    const type = suggestedType(index, args.illustrations);
    await writeScaffoldFile(
      path.join(promptsDir, promptFileName(index, type)),
      promptTemplate(args, index),
      args.force
    );
  }

  console.log(`Scaffold created in: ${outputDir}`);
  console.log("Files:");
  console.log("- outline.md");
  console.log("- references/series-reference.md");
  if (headingPositions.length > 0) {
    console.log(`- Derived ${headingPositions.length} heading-based positions from ${path.resolve(args.articlePath!)}`);
  }
  if (headingPositions.length < args.illustrations) {
    const fallbackCount = args.illustrations - headingPositions.length;
    console.log(`- ${fallbackCount} illustration slot(s) fell back to placeholder headings`);
  }
  for (let index = 1; index <= args.illustrations; index++) {
    const type = suggestedType(index, args.illustrations);
    console.log(`- prompts/${promptFileName(index, type)}`);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
