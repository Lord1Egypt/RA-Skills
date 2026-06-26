#!/usr/bin/env bun
import path from "node:path";
import process from "node:process";
import { readdir, readFile, writeFile, access } from "node:fs/promises";
import { constants } from "node:fs";
import { fileURLToPath } from "node:url";
import {
  buildWorkflowNegativePrompt,
  resolveWorkflowStyle,
} from "./visual-policy.ts";

const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const defaultNamespace = process.env.IMAGE_SKILL_NAMESPACE?.trim() || path.basename(skillDir);

type CliArgs = {
  outlinePath: string | null;
  promptsDir: string | null;
  outputPath: string | null;
  imagesDir: string | null;
  projectPath: string;
  model: string | null;
  style: string | null;
  aspectRatio: string;
  quality: string;
  jobs: number | null;
  help: boolean;
};

type OutlineEntry = {
  index: number;
  filename: string;
};

type PromptMeta = {
  styleDirection?: string;
  aspect?: string;
  referenceImage?: string;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/build-batch.ts --outline outline.md --prompts prompts --output batch.json --images-dir images [--model <model>]

Options:
  --outline <path>     Path to outline.md
  --prompts <path>     Path to prompts directory
  --output <path>      Path to output batch.json
  --images-dir <path>  Directory for generated images
  --project <path>     Project directory used for local .image-skills lookup (default: cwd)
  --model <id>         Model key for bundled runtime batch tasks. Falls back to IMAGE_GEN_DEFAULT_MODEL or .image-skills/${defaultNamespace}/EXTEND.md
  --style <name>       Explicit bundled runtime style override
  --ar <ratio>         Aspect ratio for all tasks (default: 16:9)
  --quality <level>    Quality for all tasks (default: 2k)
  --jobs <count>       Suggested worker count metadata (optional)
  -h, --help           Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    outlinePath: null,
    promptsDir: null,
    outputPath: null,
    imagesDir: null,
    projectPath: process.cwd(),
    model: null,
    style: null,
    aspectRatio: "16:9",
    quality: "2k",
    jobs: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--outline") args.outlinePath = argv[++i] ?? null;
    else if (current === "--prompts") args.promptsDir = argv[++i] ?? null;
    else if (current === "--output") args.outputPath = argv[++i] ?? null;
    else if (current === "--images-dir") args.imagesDir = argv[++i] ?? null;
    else if (current === "--project") args.projectPath = argv[++i] ?? args.projectPath;
    else if (current === "--model") args.model = argv[++i] ?? null;
    else if (current === "--style") args.style = argv[++i] ?? null;
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

function parseOutline(content: string): OutlineEntry[] {
  const entries: OutlineEntry[] = [];
  const blocks = content.replace(/\r\n/g, "\n").split(/^## Illustration\s+/m).slice(1);

  for (const block of blocks) {
    const indexMatch = block.match(/^(\d+)/);
    const filenameMatch = block.match(/\*\*Filename\*\*:\s*(.+)/);
    if (indexMatch && filenameMatch) {
      entries.push({
        index: parseInt(indexMatch[1]!, 10),
        filename: filenameMatch[1]!.trim(),
      });
    }
  }
  return entries;
}

async function findPromptFile(promptsDir: string, entry: OutlineEntry): Promise<string | null> {
  const files = await readdir(promptsDir);
  const prefix = String(entry.index).padStart(2, "0");
  const match = files.find((file) => file.startsWith(prefix) && file.endsWith(".md"));
  return match ? path.join(promptsDir, match) : null;
}

function parsePromptMeta(content: string): PromptMeta {
  const normalized = content.replace(/\r\n/g, "\n");
  const styleMatch = normalized.match(/^Style direction:\s*(.+?)(?:\.\s*|$)/im);
  const aspectMatch = normalized.match(/^- aspect ratio:\s*(.+?)$/im) ?? normalized.match(/^Aspect ratio:\s*(.+?)(?:\.\s*|$)/im);
  const referenceMatch = normalized.match(/^- reference image:\s*(.+)$/im);
  return {
    styleDirection: styleMatch?.[1]?.trim(),
    aspect: aspectMatch?.[1]?.trim(),
    referenceImage: referenceMatch?.[1]?.trim(),
  };
}

function resolveReferencePath(promptsDir: string, referenceImage: string): string {
  const t = referenceImage.trim();
  if (/^https?:\/\//i.test(t)) return t;
  if (path.isAbsolute(t)) return t;
  return path.resolve(path.dirname(promptsDir), t);
}

async function maybeAssertReferenceExists(referencePath: string): Promise<boolean> {
  if (/^https?:\/\//i.test(referencePath.trim())) return true;
  try {
    await access(referencePath, constants.F_OK);
    return true;
  } catch {
    console.warn(
      `Warning: shared illustration reference is missing: ${referencePath}. Proceeding without --ref. ` +
        `Generate/upload a public URL later if you need stronger consistency.`
    );
    return false;
  }
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

  const outlineContent = await readFile(args.outlinePath, "utf8");
  const entries = parseOutline(outlineContent);

  if (entries.length === 0) {
    console.error("No illustration entries found in outline.");
    process.exit(1);
  }

  const tasks = [];
  for (const entry of entries) {
    const promptFile = await findPromptFile(args.promptsDir, entry);
    if (!promptFile) {
      console.error(`Warning: No prompt file found for illustration ${entry.index}, skipping.`);
      continue;
    }

    const imageDir = args.imagesDir ?? path.dirname(args.outputPath);
    const promptContent = await readFile(promptFile, "utf8");
    const meta = parsePromptMeta(promptContent);
    const task: Record<string, unknown> = {
      id: `illustration-${String(entry.index).padStart(2, "0")}`,
      promptFiles: [promptFile],
      image: path.join(imageDir, entry.filename),
      model: resolvedModel.value,
      ar: meta.aspect ?? args.aspectRatio,
      quality: args.quality,
      negative_prompt: buildWorkflowNegativePrompt("article"),
    };
    const style = resolveWorkflowStyle("article", args.style, meta.styleDirection);
    if (style) task.style = style;
    if (meta.referenceImage && meta.referenceImage.toLowerCase() !== "none") {
      const resolvedRef = resolveReferencePath(args.promptsDir, meta.referenceImage);
      const ok = await maybeAssertReferenceExists(resolvedRef);
      if (ok) task.ref = [resolvedRef];
    }
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
