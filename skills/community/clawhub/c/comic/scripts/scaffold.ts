#!/usr/bin/env bun
import process from "node:process";
import { mkdir, writeFile, access } from "node:fs/promises";
import { constants } from "node:fs";
import path from "node:path";

type CliArgs = {
  outputDir: string | null;
  title: string;
  topic: string;
  art: string;
  tone: string;
  layout: string;
  aspect: string;
  contentScope: string;
  language: string;
  panelsPerPage: number;
  pages: number;
  force: boolean;
  help: boolean;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/scaffold.ts --output-dir comic/topic-slug --title "Comic Title" [options]

Options:
  --output-dir <path>   Target comic working directory
  --title <text>        Comic title
  --topic <text>        Topic summary (default: same as title)
  --art <name>          Art style (default: ligne-claire)
  --tone <name>         Tone (default: neutral)
  --layout <name>       Layout (default: standard)
  --aspect <ratio>      Aspect ratio (default: 3:4)
  --scope <name>        Total content scope (default: standard)
  --lang <code>         On-page text language when needed (default placeholder: en)
  --panels <count>      Target panel count per page (default: 3)
  --pages <count>       Number of content pages, excluding cover (default: 4)
  --force               Overwrite existing files
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    outputDir: null,
    title: "Comic Title",
    topic: "Comic Title",
    art: "ligne-claire",
    tone: "neutral",
    layout: "standard",
    aspect: "3:4",
    contentScope: "standard",
    language: "en",
    panelsPerPage: 3,
    pages: 4,
    force: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--title") args.title = argv[++i] ?? args.title;
    else if (current === "--topic") args.topic = argv[++i] ?? args.topic;
    else if (current === "--art") args.art = argv[++i] ?? args.art;
    else if (current === "--tone") args.tone = argv[++i] ?? args.tone;
    else if (current === "--layout") args.layout = argv[++i] ?? args.layout;
    else if (current === "--aspect") args.aspect = argv[++i] ?? args.aspect;
    else if (current === "--scope") args.contentScope = argv[++i] ?? args.contentScope;
    else if (current === "--lang") args.language = argv[++i] ?? args.language;
    else if (current === "--panels") {
      const value = parseInt(argv[++i] ?? "", 10);
      if (Number.isFinite(value) && value >= 1) args.panelsPerPage = value;
    }
    else if (current === "--pages") {
      const value = parseInt(argv[++i] ?? "", 10);
      if (Number.isFinite(value) && value >= 1) args.pages = value;
    } else if (current === "--force") args.force = true;
    else if (current === "--help" || current === "-h") args.help = true;
  }

  if (args.topic === "Comic Title") {
    args.topic = args.title;
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

function promptFileName(index: number): string {
  return `${String(index).padStart(2, "0")}-page.md`;
}

function storyboardTemplate(args: CliArgs): string {
  const pageBlocks = Array.from({ length: args.pages }, (_, offset) => {
    const page = offset + 1;
    const imageName = `${String(page).padStart(2, "0")}-page-topic.png`;
    return `## Page ${page}
**Filename**: ${imageName}
**Core Message**: <what this page must convey>
**Scene**: <location and situation>
**Characters**:
- <character 1>
- <character 2>
**Continuity Anchors**:
- <what must stay the same from the previous page: outfit, prop, location, time of day, injuries, etc.>
**Panel Count**: ${args.panelsPerPage}
**Panel Plan**:
- Panel 1: Title + one-sentence setup
- Panel 2: Main explanation with one example
- Panel 3: Mini summary + next-step hint
**Page Hook**: <transition to next page>
`;
  }).join("\n");

  return `---
title: "${args.title}"
topic: "${args.topic}"
art: "${args.art}"
tone: "${args.tone}"
layout: "${args.layout}"
aspect: "${args.aspect}"
content_scope: "${args.contentScope}"
language: "${args.language}"
panels_per_page: ${args.panelsPerPage}
page_count: ${args.pages}
---

# ${args.title}

**Character Reference**: characters/characters.png

## Cover
**Filename**: 00-cover-topic.png
**Core Message**: <one-line hook>
**Visual Focus**: <main cover concept>
**Prompt Notes**:
- <note 1>
- <note 2>

${pageBlocks}`;
}

function characterTemplate(args: CliArgs): string {
  return `# Character Definitions - ${args.title}

**Art**: ${args.art}
**Tone**: ${args.tone}
**Content Scope**: ${args.contentScope}
**Language**: ${args.language}

---

## Character 1: <Name>

**Role**: <protagonist | mentor | antagonist | narrator>
**Age**: <age or age range>

**Appearance**:
- Face shape: <face shape>
- Hair: <hair style, color, and length>
- Eyes: <eye features>
- Build: <body type and posture>
- Distinguishing features: <glasses, scar, beard, signature accessory>

**Costume**:
- Default outfit: <default clothing>
- Color palette: <main colors>
- Accessories: <tools, bag, hat, and so on>

**Expression Range**:
- Neutral: <description>
- Happy/Excited: <description>
- Thinking/Confused: <description>
- Determined: <description>

---

## Reference Sheet Prompt

Character reference sheet in ${args.art} style:

[ROW 1 - <Name>]
- Front view: <description>
- 3/4 view: <description>
- Expression sheet: Neutral | Happy | Focused | Worried

COLOR PALETTE:
- <Name>: <color list>

White background, clear labels under each character.
`;
}

function coverPromptTemplate(args: CliArgs): string {
  return `Create a comic cover about: ${args.topic}.

Comic role: cover.
Art style: ${args.art}.
Tone: ${args.tone}.
Layout: ${args.layout}.
Aspect ratio: ${args.aspect}.
Content scope: ${args.contentScope}.
Language: ${args.language}.

Character reference:
- reference image: none
- consistency rule: keep faces, costume colors, accessories, and silhouette stable across pages
- priority rule: treat the reference sheet as the canonical source of truth for character design; do not redesign the cast from scratch on later pages

Core message: A clear, beginner-friendly explanation of the topic.
Visual focus: One clear hero panel summarizing the topic.
Prompt notes:
- Keep layout clean and readable
- Keep character designs consistent

Avoid: inconsistent character appearance, unreadable text, cluttered composition, watermark.
`;
}

function pagePromptTemplate(args: CliArgs, page: number): string {
  return `Create a comic page about: ${args.topic}.

Comic role: page.
Art style: ${args.art}.
Tone: ${args.tone}.
Layout: ${args.layout}.
Aspect ratio: ${args.aspect}.
Content scope: ${args.contentScope}.
Language: ${args.language}.

Character reference:
- reference image: none
- consistency rule: keep faces, costume colors, accessories, and silhouette stable across pages
- priority rule: treat the reference sheet as the canonical source of truth for faces, outfits, props, and palette; do not redesign characters on later pages

Characters:
- Character 1: A friendly narrator/host explaining the topic
- Character 2: A curious learner asking short questions

Continuity anchors:
- Keep the same two characters, palette, and line style
- Same outfits; consistent lighting; no scene jump unless stated

Scene:
- location: Simple indoor setting for page ${page}>
- key action: The narrator explains the next key point
- emotional beat: Curious and encouraging

Story continuity:
- previous page recap: The narrator introduced the topic ${page}>
- current page transition: Continue with a concrete example
- next page hook: Tease the next key takeaway

Panel structure:
- Panel count target: ${args.panelsPerPage}.
- Panel 1: Title + one-sentence setup
- Panel 2: Main explanation with one example
- Panel 3: Mini summary + next-step hint

Text treatment: narration-only.
If text is used, keep it sparse, readable, and native to the target language.

Avoid: inconsistent character appearance, overcrowded tiny panels, unreadable text, broken anatomy, random extra limbs, watermark.
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
  const charactersDir = path.join(outputDir, "characters");
  await mkdir(promptsDir, { recursive: true });
  await mkdir(charactersDir, { recursive: true });

  await writeScaffoldFile(
    path.join(outputDir, "analysis.md"),
    `# Analysis

- Topic: ${args.topic}
- Audience: <target audience>
- Main arc: <main story or knowledge arc>
- Total content scope: ${args.contentScope}
- Target page count: ${args.pages}
- Target panels per page: ${args.panelsPerPage}
- Preferred aspect ratio: ${args.aspect}
`,
    args.force,
  );
  await writeScaffoldFile(path.join(outputDir, "storyboard.md"), storyboardTemplate(args), args.force);
  await writeScaffoldFile(path.join(charactersDir, "characters.md"), characterTemplate(args), args.force);
  await writeScaffoldFile(path.join(promptsDir, "00-cover.md"), coverPromptTemplate(args), args.force);

  for (let page = 1; page <= args.pages; page++) {
    await writeScaffoldFile(path.join(promptsDir, promptFileName(page)), pagePromptTemplate(args, page), args.force);
  }

  console.log(`Scaffold created in: ${outputDir}`);
  console.log("Files:");
  console.log("- analysis.md");
  console.log("- storyboard.md");
  console.log("- characters/characters.md");
  console.log("- prompts/00-cover.md");
  for (let page = 1; page <= args.pages; page++) {
    console.log(`- prompts/${promptFileName(page)}`);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
