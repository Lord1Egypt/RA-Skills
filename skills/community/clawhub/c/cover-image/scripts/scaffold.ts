#!/usr/bin/env bun
import process from "node:process";
import { mkdir, writeFile, access } from "node:fs/promises";
import { constants } from "node:fs";
import path from "node:path";

type CliArgs = {
  outputDir: string | null;
  topic: string;
  concept: string;
  type: string;
  palette: string;
  rendering: string;
  text: string;
  mood: string;
  aspect: string;
  language: string;
  force: boolean;
  help: boolean;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/scaffold.ts --output-dir cover-image/topic-slug --topic "Topic" [options]

Options:
  --output-dir <path>   Target cover-image working directory
  --topic <text>        Main topic or title placeholder
  --concept <text>      Primary concept placeholder
  --type <name>         Cover type (default: conceptual)
  --palette <name>      Color palette (default: elegant)
  --rendering <name>    Rendering style (default: editorial)
  --text <level>        Text treatment (default: title-only)
  --mood <level>        Mood level (default: balanced)
  --aspect <ratio>      Aspect ratio (default: 16:9)
  --lang <code>         On-canvas text language when needed (default placeholder: en)
  --force               Overwrite existing files
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    outputDir: null,
    topic: "Topic",
    concept: "Primary concept",
    type: "conceptual",
    palette: "elegant",
    rendering: "editorial",
    text: "title-only",
    mood: "balanced",
    aspect: "16:9",
    language: "en",
    force: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--topic") args.topic = argv[++i] ?? args.topic;
    else if (current === "--concept") args.concept = argv[++i] ?? args.concept;
    else if (current === "--type") args.type = argv[++i] ?? args.type;
    else if (current === "--palette") args.palette = argv[++i] ?? args.palette;
    else if (current === "--rendering") args.rendering = argv[++i] ?? args.rendering;
    else if (current === "--text") args.text = argv[++i] ?? args.text;
    else if (current === "--mood") args.mood = argv[++i] ?? args.mood;
    else if (current === "--aspect") args.aspect = argv[++i] ?? args.aspect;
    else if (current === "--lang") args.language = argv[++i] ?? args.language;
    else if (current === "--force") args.force = true;
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

function briefTemplate(args: CliArgs): string {
  return `# Cover Brief

- Topic: ${args.topic}
- Primary concept: ${args.concept}
- Target audience: <target audience>
- Cover type: ${args.type}
- Palette: ${args.palette}
- Rendering: ${args.rendering}
- Text treatment: ${args.text}
- Mood: ${args.mood}
- Aspect ratio: ${args.aspect}
- Language: ${args.language}
- Reference images: none
`;
}

function promptTemplate(args: CliArgs): string {
  return `[one-sentence topic]

Create a cover image for an article about: ${args.topic}.
Primary concept: ${args.concept}.

Composition type: ${args.type}.
Visual focus: <main visual element>.
Aspect ratio: ${args.aspect}.

Color palette: ${args.palette}.
Rendering style: ${args.rendering}.
Mood: ${args.mood}.
Language: ${args.language}.

Text treatment: ${args.text}.
If text is needed, reserve clean title space and avoid dense tiny text.

Avoid: low contrast clutter, awkward anatomy, unreadable small text, watermarks, distorted hands.
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
  await mkdir(promptsDir, { recursive: true });

  await writeScaffoldFile(path.join(outputDir, "brief.md"), briefTemplate(args), args.force);
  await writeScaffoldFile(path.join(promptsDir, "cover.md"), promptTemplate(args), args.force);

  console.log(`Scaffold created in: ${outputDir}`);
  console.log("Files:");
  console.log("- brief.md");
  console.log("- prompts/cover.md");
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
