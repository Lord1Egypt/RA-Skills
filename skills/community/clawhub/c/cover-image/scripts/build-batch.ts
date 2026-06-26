#!/usr/bin/env bun
import path from "node:path";
import process from "node:process";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import {
  buildWorkflowNegativePrompt,
  resolveWorkflowStyle,
} from "./visual-policy.ts";

const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const defaultNamespace = process.env.IMAGE_SKILL_NAMESPACE?.trim() || path.basename(skillDir);

type CliArgs = {
  promptsDir: string | null;
  outputPath: string | null;
  imagesDir: string | null;
  projectPath: string;
  model: string | null;
  style: string | null;
  aspectRatio: string;
  quality: string;
  ref: string | null;
  jobs: number | null;
  help: boolean;
};

type PromptEntry = {
  order: number;
  promptPath: string;
  imageFilename: string;
};

type PromptMeta = {
  rendering?: string;
  aspect?: string;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/build-batch.ts --prompts prompts --output batch.json [--model <model>] [options]

Options:
  --prompts <path>       Path to prompts directory
  --output <path>        Path to output batch.json
  --images-dir <path>    Directory for generated images
  --project <path>       Project directory used for local .image-skills lookup (default: cwd)
  --model <id>           Model key for bundled runtime batch tasks. Falls back to IMAGE_GEN_DEFAULT_MODEL or .image-skills/${defaultNamespace}/EXTEND.md
  --style <name>         Explicit bundled runtime style override
  --ref <path>           Optional shared reference image
  --ar <ratio>           Default aspect ratio when prompt files omit it (default: 16:9)
  --quality <level>      Quality for all tasks (default: 2k)
  --jobs <count>         Suggested worker count metadata (optional)
  -h, --help             Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    promptsDir: null,
    outputPath: null,
    imagesDir: null,
    projectPath: process.cwd(),
    model: null,
    style: null,
    aspectRatio: "16:9",
    quality: "2k",
    ref: null,
    jobs: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--prompts") args.promptsDir = argv[++i] ?? null;
    else if (current === "--output") args.outputPath = argv[++i] ?? null;
    else if (current === "--images-dir") args.imagesDir = argv[++i] ?? null;
    else if (current === "--project") args.projectPath = argv[++i] ?? args.projectPath;
    else if (current === "--model") args.model = argv[++i] ?? null;
    else if (current === "--style") args.style = argv[++i] ?? null;
    else if (current === "--ref") args.ref = argv[++i] ?? null;
    else if (current === "--ar") args.aspectRatio = argv[++i] ?? args.aspectRatio;
    else if (current === "--quality") args.quality = argv[++i] ?? args.quality;
    else if (current === "--jobs") {
      const value = argv[++i];
      args.jobs = value ? parseInt(value, 10) : null;
    } else if (current === "--help" || current === "-h") {
      args.help = true;
    }
  }

  return args;
}

type ResolvedModel = {
  value: string;
  source: "arg" | "env" | "extend";
};

function parseDefaultModel(content: string): string | null {
  const match = content.replace(/\r\n/g, "\n").match(/^default_model:\s*["']?([^"'\n]+)["']?\s*$/m);
  return match?.[1]?.trim() || null;
}

async function resolveModel(args: CliArgs): Promise<ResolvedModel | null> {
  if (args.model?.trim()) {
    return { value: args.model.trim(), source: "arg" };
  }

  const envModel = process.env.IMAGE_GEN_DEFAULT_MODEL?.trim();
  if (envModel) {
    return { value: envModel, source: "env" };
  }

  const extendPath = path.resolve(args.projectPath, ".image-skills", defaultNamespace, "EXTEND.md");
  try {
    const extendContent = await readFile(extendPath, "utf8");
    const extendModel = parseDefaultModel(extendContent);
    if (extendModel) {
      return { value: extendModel, source: "extend" };
    }
  } catch {
    // Missing local config is fine; callers can still provide --model explicitly.
  }

  return null;
}

function sortPromptFilenames(a: string, b: string): number {
  const matchA = a.match(/^(\d+)/);
  const matchB = b.match(/^(\d+)/);
  if (matchA && matchB) {
    const order = parseInt(matchA[1]!, 10) - parseInt(matchB[1]!, 10);
    if (order !== 0) return order;
  } else if (matchA) {
    return -1;
  } else if (matchB) {
    return 1;
  }
  return a.localeCompare(b);
}

async function collectPromptEntries(promptsDir: string): Promise<PromptEntry[]> {
  const files = await readdir(promptsDir);
  return files
    .filter((filename) => filename.toLowerCase().endsWith(".md"))
    .sort(sortPromptFilenames)
    .map((filename, index) => {
      const baseName = filename.replace(/\.md$/i, "");
      return {
        order: index + 1,
        promptPath: path.join(promptsDir, filename),
        imageFilename: `${baseName}.png`,
      };
    });
}

function parsePromptMeta(content: string): PromptMeta {
  const normalized = content.replace(/\r\n/g, "\n");
  const renderingMatch = normalized.match(/^Rendering style:\s*(.+?)(?:\.\s*|$)/im);
  const aspectMatch = normalized.match(/^Aspect ratio:\s*(.+?)(?:\.\s*|$)/im);
  return {
    rendering: renderingMatch?.[1]?.trim().toLowerCase(),
    aspect: aspectMatch?.[1]?.trim(),
  };
}

function resolveStyle(explicitStyle: string | null, rendering: string | undefined): string | null {
  return resolveWorkflowStyle("cover", explicitStyle, rendering);
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }

  if (!args.promptsDir) {
    console.error("Error: --prompts is required");
    process.exit(1);
  }
  if (!args.outputPath) {
    console.error("Error: --output is required");
    process.exit(1);
  }
  const resolvedModel = await resolveModel(args);
  if (!resolvedModel) {
    console.error(
      `Error: --model is required unless IMAGE_GEN_DEFAULT_MODEL or .image-skills/${defaultNamespace}/EXTEND.md provides default_model`
    );
    process.exit(1);
  }

  const entries = await collectPromptEntries(args.promptsDir);
  if (entries.length === 0) {
    console.error("No cover prompt files found in prompts directory.");
    process.exit(1);
  }

  const imageDir = args.imagesDir ?? path.dirname(args.outputPath);
  const tasks = [];

  for (const entry of entries) {
    const promptContent = await readFile(entry.promptPath, "utf8");
    const meta = parsePromptMeta(promptContent);
    const task: Record<string, unknown> = {
      id: `cover-${String(entry.order).padStart(2, "0")}`,
      promptFiles: [entry.promptPath],
      image: path.join(imageDir, entry.imageFilename),
      model: resolvedModel.value,
      ar: meta.aspect ?? args.aspectRatio,
      quality: args.quality,
      negative_prompt: buildWorkflowNegativePrompt("cover"),
    };
    const style = resolveStyle(args.style, meta.rendering);
    if (style) task.style = style;
    if (args.ref) task.ref = [args.ref];
    tasks.push(task);
  }

  const output: Record<string, unknown> = { tasks };
  if (args.jobs) output.jobs = args.jobs;

  await writeFile(args.outputPath, JSON.stringify(output, null, 2) + "\n");
  console.log(`Batch file written: ${args.outputPath} (${tasks.length} tasks, model: ${resolvedModel.value} via ${resolvedModel.source})`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
