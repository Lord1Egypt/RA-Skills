#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function printUsage() {
  console.log(`Usage:
  node scripts/illustrate-article.mjs --article article.md --output-dir illustrations/topic [options]

Options:
  --article <path>             Article markdown to illustrate
  --output-dir <path>          Working directory for outline, prompts, batch, and images
  --project <path>             Project directory used for .image-skills lookup (default: cwd)
  --article-output <path>      Optional output markdown path; defaults to in-place update with backup
  --topic <text>               Topic override; defaults to article title or file name
  --audience <text>            Audience hint (default: general reader)
  --style <name>               Illustration style (default: minimal)
  --density <name>             Illustration density (default: per-section)
  --lang <code>                On-image text language (default: en)
  --aspect <ratio>             Aspect ratio used for prompts and batch (default: 16:9)
  --quality <level>            Batch quality (default: 2k)
  --illustrations <count>      Number of illustration slots to scaffold (default: 3)
  --model <id>                 Optional explicit model override
  --jobs <count>               Optional batch jobs metadata
  --on-missing-anchor <mode>   insert-images behavior: end|skip|fail (default: end)
  --force                      Overwrite scaffold files if they already exist
  --help, -h                   Show help`);
}

function parseArgs(argv) {
  const args = {
    article: null,
    outputDir: null,
    project: process.cwd(),
    articleOutput: null,
    topic: null,
    audience: "general reader",
    style: "minimal",
    density: "per-section",
    language: "en",
    aspect: "16:9",
    quality: "2k",
    illustrations: 3,
    model: null,
    jobs: null,
    onMissingAnchor: "end",
    force: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (current === "--article") args.article = argv[++i] ?? null;
    else if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--project") args.project = argv[++i] ?? args.project;
    else if (current === "--article-output") args.articleOutput = argv[++i] ?? null;
    else if (current === "--topic") args.topic = argv[++i] ?? null;
    else if (current === "--audience") args.audience = argv[++i] ?? args.audience;
    else if (current === "--style") args.style = argv[++i] ?? args.style;
    else if (current === "--density") args.density = argv[++i] ?? args.density;
    else if (current === "--lang") args.language = argv[++i] ?? args.language;
    else if (current === "--aspect") args.aspect = argv[++i] ?? args.aspect;
    else if (current === "--quality") args.quality = argv[++i] ?? args.quality;
    else if (current === "--illustrations") {
      const value = parseInt(argv[++i] ?? "", 10);
      if (Number.isFinite(value) && value >= 1) args.illustrations = value;
    } else if (current === "--model") args.model = argv[++i] ?? null;
    else if (current === "--jobs") {
      const value = argv[++i];
      args.jobs = value ? parseInt(value, 10) : null;
    } else if (current === "--on-missing-anchor") {
      const value = (argv[++i] ?? "").trim().toLowerCase();
      if (value === "end" || value === "skip" || value === "fail") args.onMissingAnchor = value;
      else throw new Error(`Invalid --on-missing-anchor: ${value || "(empty)"}`);
    } else if (current === "--force") args.force = true;
    else if (current === "--help" || current === "-h") args.help = true;
  }

  return args;
}

function detectTopic(articlePath) {
  const content = fs.readFileSync(articlePath, "utf8").replace(/\r\n/g, "\n");
  const atx = content.match(/^\s{0,3}#\s+(.+?)\s*#*\s*$/m);
  if (atx?.[1]?.trim()) return atx[1].trim();

  const lines = content.split("\n");
  for (let index = 0; index < lines.length - 1; index++) {
    const line = lines[index]?.trim();
    const underline = lines[index + 1]?.trim();
    if (line && underline && (/^=+$/.test(underline) || /^-+$/.test(underline))) {
      return line;
    }
  }

  return path.basename(articlePath, path.extname(articlePath));
}

function runStep(label, command, args) {
  console.error(`\n[article-illustrator] ${label}`);
  console.error(`> ${command} ${args.map((value) => JSON.stringify(value)).join(" ")}`);
  const result = spawnSync(command, args, {
    cwd: skillDir,
    stdio: "inherit",
    env: process.env,
  });
  if (result.status !== 0) {
    throw new Error(`${label} failed with exit code ${result.status ?? "unknown"}`);
  }
}

function maybePushArg(args, flag, value) {
  if (value !== null && value !== undefined && value !== "") {
    args.push(flag, String(value));
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }
  if (!args.article) throw new Error("--article is required");
  if (!args.outputDir) throw new Error("--output-dir is required");

  const articlePath = path.resolve(args.article);
  const outputDir = path.resolve(args.outputDir);
  const projectDir = path.resolve(args.project);
  const outlinePath = path.join(outputDir, "outline.md");
  const promptsDir = path.join(outputDir, "prompts");
  const batchPath = path.join(outputDir, "batch.json");
  const imagesDir = path.join(outputDir, "images");
  const topic = args.topic?.trim() || detectTopic(articlePath);

  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(imagesDir, { recursive: true });

  runStep("ensure-ready", "npm", ["run", "ensure-ready", "--", "--project", projectDir, "--workflow", "article"]);

  const scaffoldArgs = [
    "run",
    "scaffold",
    "--",
    "--output-dir",
    outputDir,
    "--article",
    articlePath,
    "--topic",
    topic,
    "--audience",
    args.audience,
    "--style",
    args.style,
    "--density",
    args.density,
    "--lang",
    args.language,
    "--aspect",
    args.aspect,
    "--illustrations",
    String(args.illustrations),
  ];
  if (args.force) scaffoldArgs.push("--force");
  runStep("scaffold", "npm", scaffoldArgs);

  runStep("build-prompts", "npm", [
    "run",
    "build-prompts",
    "--",
    "--outline",
    outlinePath,
    "--output-dir",
    promptsDir,
    "--topic",
    topic,
    "--audience",
    args.audience,
    "--style",
    args.style,
    "--density",
    args.density,
    "--lang",
    args.language,
    "--aspect",
    args.aspect,
  ]);

  const batchArgs = [
    "run",
    "build-batch",
    "--",
    "--outline",
    outlinePath,
    "--prompts",
    promptsDir,
    "--output",
    batchPath,
    "--images-dir",
    imagesDir,
    "--project",
    projectDir,
    "--ar",
    args.aspect,
    "--quality",
    args.quality,
  ];
  maybePushArg(batchArgs, "--model", args.model);
  maybePushArg(batchArgs, "--style", args.style);
  maybePushArg(batchArgs, "--jobs", args.jobs);
  runStep("build-batch", "npm", batchArgs);

  runStep("generate", "npm", [
    "run",
    "generate",
    "--",
    "--project",
    projectDir,
    "--batchfile",
    batchPath,
    "--json",
  ]);

  const insertArgs = [
    "run",
    "insert-images",
    "--",
    "--article",
    articlePath,
    "--outline",
    outlinePath,
    "--images-dir",
    imagesDir,
    "--on-missing-anchor",
    args.onMissingAnchor,
  ];
  maybePushArg(insertArgs, "--output", args.articleOutput ? path.resolve(args.articleOutput) : null);
  runStep("insert-images", "npm", insertArgs);

  console.log(JSON.stringify({
    article: articlePath,
    topic,
    outputDir,
    outline: outlinePath,
    promptsDir,
    batch: batchPath,
    imagesDir,
    articleOutput: args.articleOutput ? path.resolve(args.articleOutput) : articlePath,
  }, null, 2));
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
