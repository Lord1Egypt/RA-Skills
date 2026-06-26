#!/usr/bin/env bun
/**
 * article-images-gen - 文案插图专家
 *
 * 专业的文章配图生成工具，专注于生成高质量的手绘风格插图
 * 使用阿里百炼 Qwen-Image 生成
 */

import path from "node:path";
import process from "node:process";
import { readFile, writeFile, mkdir, access, copyFile } from "node:fs/promises";
import { generateImage } from "./image-generator";
import { generateOutline, generatePromptFiles } from "./article-analyzer";

type CliArgs = {
  articlePath: string | null;
  density: "minimal" | "balanced" | "per-section" | "rich" | null;
  outputDir: string | null;
  help: boolean;
};

const DENSITY_OPTIONS = ["minimal", "balanced", "per-section", "rich"] as const;

function printUsage(): void {
  console.log(`Usage:
  bun scripts/illustrator.ts path/to/article.md
  bun scripts/illustrator.ts path/to/article.md --density balanced
  bun scripts/illustrator.ts --help

Options:
  --density <level>    Image density: minimal (1-2), balanced (3-4), per-section, rich (5+)
  --output-dir <path>  Override output directory
  -h, --help           Show help

Density Levels:
  minimal      Core concepts only (1-2 images)
  balanced     Major sections (3-4 images)
  per-section  At least 1 per section (recommended)
  rich         Comprehensive coverage (5+ images)
`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    articlePath: null,
    density: null,
    outputDir: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--density") {
      args.density = argv[++i] as CliArgs["density"];
    } else if (current === "--output-dir") {
      args.outputDir = argv[++i] ?? null;
    } else if (current === "--help" || current === "-h") {
      args.help = true;
    } else if (!current.startsWith("-") && !args.articlePath) {
      args.articlePath = current;
    }
  }

  return args;
}

async function fileExists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

function determineOutputDir(articlePath: string, overrideDir: string | null): string {
  if (overrideDir) {
    return overrideDir;
  }
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, "");
  const articleName = path.basename(articlePath, path.extname(articlePath));
  return `/tmp/imageGen/${today}/${articleName}`;
}

async function generateIllustrationsForArticle(
  articlePath: string,
  articleContent: string,
  density: string,
  outputDir: string
): Promise<void> {
  console.log(`\n📄 Analyzing article: ${articlePath}`);
  console.log(`📊 Density: ${density}`);
  console.log(`📁 Output: ${outputDir}\n`);

  // Step 1: Generate outline
  console.log("Step 1: Generating outline...");
  const outline = await generateOutline(articlePath, articleContent, density, outputDir);
  console.log(`  ✓ Outline saved to ${outputDir}/outline.md`);
  console.log(`  ✓ ${outline.image_count} illustrations planned\n`);

  // Step 2: Generate prompt files
  console.log("Step 2: Generating prompt files...");
  const promptFiles = await generatePromptFiles(outline, articleContent, outputDir);
  console.log(`  ✓ ${promptFiles.length} prompt files saved to ${outputDir}/prompts/\n`);

  // Step 3: Generate images
  console.log("Step 3: Generating images...");
  let successCount = 0;
  let failureCount = 0;

  for (const position of outline.positions) {
    const promptFile = promptFiles.find((f) =>
      f.includes(position.filename.replace(".png", ".md"))
    );

    if (!promptFile) {
      console.log(`  ✗ Illustration ${position.index}: prompt file not found`);
      failureCount++;
      continue;
    }

    const promptContent = await readFile(promptFile, "utf8");
    const promptText = promptContent.replace(/^---\n[\s\S]*?\n---\n/, "").trim();
    const outputPath = path.join(outputDir, position.filename);

    try {
      const result = await generateImage(promptText, { outputDir });
      // Copy the generated image to the expected output path
      await copyFile(result.imagePath, outputPath);
      console.log(`  ✓ Illustration ${position.index}: ${position.filename}`);
      successCount++;
    } catch (error) {
      console.log(
        `  ✗ Illustration ${position.index}: ${error instanceof Error ? error.message : String(error)}`
      );
      failureCount++;
    }

    // Avoid rate limiting between requests
    if (position.index < outline.positions.length) {
      await new Promise((resolve) => setTimeout(resolve, 15000));
    }
  }

  // Step 4: Update article
  console.log("\nStep 4: Updating article...");
  await updateArticleWithImages(articlePath, outline.positions, outputDir);
  console.log(`  ✓ Article updated with ${successCount} image references\n`);

  // Summary
  console.log("=".repeat(50));
  console.log("Article Illustration Complete!");
  console.log(`Article: ${articlePath}`);
  console.log(`Style: Hand-drawn Minimalist`);
  console.log(`Density: ${density}`);
  console.log(`Location: ${outputDir}`);
  console.log(`Images: ${successCount}/${outline.image_count} generated`);
  if (failureCount > 0) {
    console.log(`Failed: ${failureCount}`);
  }
}

async function updateArticleWithImages(
  articlePath: string,
  positions: Array<{ index: number; section: string; filename: string }>,
  outputDir: string
): Promise<void> {
  const content = await readFile(articlePath, "utf8");
  const lines = content.split("\n");
  const newLines: string[] = [];

  const articleDir = path.dirname(articlePath);
  const getRelativeImagePath = (filename: string) => {
    const imagePath = path.join(outputDir, filename);
    return path.relative(articleDir, imagePath);
  };

  for (const line of lines) {
    newLines.push(line);

    const headingMatch = line.match(/^##+\s+(.+)$/);
    if (headingMatch) {
      const heading = headingMatch[1]!.trim();
      const position = positions.find((p) => p.section === heading);
      if (position) {
        const relativePath = getRelativeImagePath(position.filename);
        newLines.push(`![${position.section}](${relativePath})`);
        newLines.push("");
      }
    }
  }

  const backupPath = `${articlePath}.bak-${Date.now()}`;
  await copyFile(articlePath, backupPath);
  console.log(`  Backup created: ${backupPath}`);

  await writeFile(articlePath, newLines.join("\n"));
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.articlePath) {
    printUsage();
    return;
  }

  if (!(await fileExists(args.articlePath))) {
    console.error(`Error: Article not found: ${args.articlePath}`);
    process.exit(1);
  }

  const density = args.density || "per-section";
  if (!DENSITY_OPTIONS.includes(density)) {
    console.error(`Error: Invalid density "${density}". Options: ${DENSITY_OPTIONS.join(", ")}`);
    process.exit(1);
  }

  const outputDir = determineOutputDir(args.articlePath, args.outputDir);
  const articleContent = await readFile(args.articlePath, "utf8");

  await generateIllustrationsForArticle(args.articlePath, articleContent, density, outputDir);
}

main().catch((error) => {
  console.error("Fatal error:", error instanceof Error ? error.message : String(error));
  process.exit(1);
});
