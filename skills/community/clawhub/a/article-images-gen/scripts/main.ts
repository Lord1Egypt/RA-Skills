#!/usr/bin/env bun
/**
 * Simple single-image generation entry point
 */

import process from "node:process";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { generateImage } from "./image-generator";

type CliArgs = {
  prompt: string | null;
  promptFiles: string | null;
  image: string | null;
  outputDir: string | null;
  help: boolean;
};

function printUsage(): void {
  console.log(`Usage:
  bun scripts/main.ts --prompt "your prompt here"
  bun scripts/main.ts --promptfiles prompt.md
  bun scripts/main.ts --help

Options:
  --prompt <text>        Direct prompt for image generation
  --promptfiles <files>  Comma-separated list of prompt files to read
  --image <path>         Output image path (used with --promptfiles)
  --output-dir <path>    Output directory for generated images
  -h, --help             Show help
`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    prompt: null,
    promptFiles: null,
    image: null,
    outputDir: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--prompt") {
      args.prompt = argv[++i] ?? null;
    } else if (current === "--promptfiles") {
      args.promptFiles = argv[++i] ?? null;
    } else if (current === "--image") {
      args.image = argv[++i] ?? null;
    } else if (current === "--output-dir") {
      args.outputDir = argv[++i] ?? null;
    } else if (current === "--help" || current === "-h") {
      args.help = true;
    }
  }

  return args;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printUsage();
    return;
  }

  const outDir = args.outputDir || "/tmp/imageGen/opencli";
  await mkdir(outDir, { recursive: true });

  if (args.prompt) {
    // Direct prompt mode
    console.log("Generating image (Gemini → Grok fallback)...");

    const result = await generateImage(args.prompt, { outputDir: outDir });

    if (args.image && result.imagePath !== args.image) {
      await writeFile(args.image, await readFile(result.imagePath));
      console.log(`Image copied to: ${args.image}`);
    } else {
      console.log(`Image saved to: ${result.imagePath}`);
    }
    return;
  }

  if (args.promptFiles) {
    // Batch prompt files mode
    const files = args.promptFiles.split(",");
    for (const file of files) {
      const promptContent = await readFile(file.trim(), "utf8");
      const promptText = promptContent.replace(/^---\n[\s\S]*?\n---\n/, "").trim();

      console.log(`Generating image (Gemini → Grok fallback)...`);

      const result = await generateImage(promptText, { outputDir: outDir });

      const outputFile = args.image || file.trim().replace(".md", ".png");
      if (result.imagePath !== outputFile) {
        await writeFile(outputFile, await readFile(result.imagePath));
      }
      console.log(`Image saved to: ${result.imagePath}`);
    }
    return;
  }

  printUsage();
}

main().catch((error) => {
  console.error("Fatal error:", error instanceof Error ? error.message : String(error));
  process.exit(1);
});
