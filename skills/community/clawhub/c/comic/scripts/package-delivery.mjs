#!/usr/bin/env bun
import { copyFile, mkdir, readdir, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import process from "node:process";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const PAGE_PATTERN = /^(\d+)-(cover|page)(-[\w-]+)?\.(png|jpg|jpeg|webp)$/i;

function printUsage() {
  console.log(`Usage:
  npx -y bun scripts/package-delivery.mjs <comic-dir> [options]

Options:
  --output-dir <path>        Delivery directory (default: <comic-dir>/delivery)
  --zip <path>               Explicit zip output path
  --inline-threshold <n>     Max images to inline in preview.md before recommending zip (default: 4)
  --json                     Print JSON summary
  -h, --help                 Show help`);
}

function parseArgs(argv) {
  const args = {
    comicDir: null,
    outputDir: null,
    zipPath: null,
    inlineThreshold: 4,
    json: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--zip") args.zipPath = argv[++i] ?? null;
    else if (current === "--inline-threshold") {
      const value = Number.parseInt(argv[++i] ?? "", 10);
      if (Number.isFinite(value) && value >= 1) args.inlineThreshold = value;
    } else if (current === "--json") args.json = true;
    else if (current === "-h" || current === "--help") args.help = true;
    else if (!current.startsWith("-") && !args.comicDir) args.comicDir = current;
  }

  return args;
}

function toErrorMessage(error) {
  return error instanceof Error ? error.message : String(error);
}

async function collectComicAssets(comicDir) {
  const files = await readdir(comicDir);
  const pages = files
    .filter((filename) => PAGE_PATTERN.test(filename))
    .map((filename) => {
      const match = filename.match(PAGE_PATTERN);
      return {
        filename,
        sourcePath: path.join(comicDir, filename),
        index: Number.parseInt(match?.[1] ?? "0", 10),
        kind: (match?.[2] ?? "page").toLowerCase(),
      };
    })
    .sort((a, b) => a.index - b.index || (a.kind === "cover" ? -1 : 1));

  if (pages.length === 0) {
    throw new Error(`No comic page images found in ${comicDir}. Expected files like 00-cover-topic.png or 01-page-topic.jpg.`);
  }

  const pdfs = files.filter((filename) => filename.toLowerCase().endsWith(".pdf")).sort();
  return {
    pages,
    pdf: pdfs[0] ? { filename: pdfs[0], sourcePath: path.join(comicDir, pdfs[0]) } : null,
  };
}

function buildPreviewMarkdown({ pageCount, previewEntries, omittedCount, hasZip }) {
  const lines = [
    "# Comic Delivery Preview",
    "",
    `- Total images: ${pageCount}`,
    `- Previewed inline: ${previewEntries.length}`,
  ];

  if (omittedCount > 0) {
    lines.push(`- Additional images not inlined: ${omittedCount}`);
  }
  if (hasZip) {
    lines.push("- A zip bundle is available for bulk delivery.");
  }

  lines.push("", "## Preview");
  for (const entry of previewEntries) {
    lines.push("", `### ${entry.filename}`, "", `![](./pages/${entry.filename})`);
  }

  return `${lines.join("\n")}\n`;
}

async function createZipBundle({ deliveryDir, zipPath, includePdf }) {
  const entries = ["preview.md", "manifest.json", "pages"];
  if (includePdf) entries.push(includePdf);
  await execFileAsync("zip", ["-rq", zipPath, ...entries], { cwd: deliveryDir });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }
  if (!args.comicDir) {
    console.error("Error: comic directory is required");
    printUsage();
    process.exit(1);
  }

  const comicDir = path.resolve(args.comicDir);
  if (!existsSync(comicDir)) {
    throw new Error(`Comic directory not found: ${comicDir}`);
  }

  const { pages, pdf } = await collectComicAssets(comicDir);
  const deliveryDir = path.resolve(args.outputDir ?? path.join(comicDir, "delivery"));
  const pagesDir = path.join(deliveryDir, "pages");
  await mkdir(pagesDir, { recursive: true });

  for (const page of pages) {
    await copyFile(page.sourcePath, path.join(pagesDir, page.filename));
  }

  let pdfTarget = null;
  if (pdf) {
    pdfTarget = pdf.filename;
    await copyFile(pdf.sourcePath, path.join(deliveryDir, pdf.filename));
  }

  const shouldZip = Boolean(args.zipPath) || pages.length > args.inlineThreshold;
  const previewEntries = pages.slice(0, shouldZip ? Math.min(3, pages.length) : pages.length);
  const previewPath = path.join(deliveryDir, "preview.md");
  await writeFile(
    previewPath,
    buildPreviewMarkdown({
      pageCount: pages.length,
      previewEntries,
      omittedCount: pages.length - previewEntries.length,
      hasZip: shouldZip,
    }),
    "utf8",
  );

  const zipPath = shouldZip
    ? path.resolve(args.zipPath ?? path.join(deliveryDir, `${path.basename(comicDir)}-delivery.zip`))
    : null;

  const manifest = {
    comicDir,
    deliveryDir,
    totalImages: pages.length,
    previewedImages: previewEntries.length,
    omittedFromPreview: pages.length - previewEntries.length,
    previewPath,
    zipPath,
    pdfPath: pdfTarget ? path.join(deliveryDir, pdfTarget) : null,
    pages: pages.map((page) => ({
      filename: page.filename,
      sourcePath: page.sourcePath,
      deliveryPath: path.join(pagesDir, page.filename),
      index: page.index,
      kind: page.kind,
    })),
  };

  const manifestPath = path.join(deliveryDir, "manifest.json");
  await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");

  if (zipPath) {
    await createZipBundle({
      deliveryDir,
      zipPath,
      includePdf: pdfTarget,
    });
  }

  if (args.json) {
    console.log(JSON.stringify({ ...manifest, manifestPath }, null, 2));
    return;
  }

  console.log(`Delivery directory: ${deliveryDir}`);
  console.log(`Manifest: ${manifestPath}`);
  console.log(`Preview: ${previewPath}`);
  if (zipPath) console.log(`Zip bundle: ${zipPath}`);
  if (pdfTarget) console.log(`PDF copy: ${path.join(deliveryDir, pdfTarget)}`);
}

main().catch((error) => {
  console.error(toErrorMessage(error));
  process.exit(1);
});
