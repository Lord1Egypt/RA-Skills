#!/usr/bin/env bun
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";

interface CliArgs {
  comicDir: string;
  output?: string;
  json: boolean;
}

interface PageInfo {
  filename: string;
  path: string;
  index: number;
  kind: "cover" | "page";
}

function printHelp(): void {
  console.log(`Usage: bun scripts/merge-to-pdf.ts <comic-dir> [options]

Options:
  -o, --output <path>   Output PDF path
      --json            JSON output
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs | null {
  const args: CliArgs = {
    comicDir: "",
    json: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") {
      printHelp();
      process.exit(0);
    }
    if (arg === "-o" || arg === "--output") {
      args.output = argv[++i];
      continue;
    }
    if (arg === "--json") {
      args.json = true;
      continue;
    }
    if (!arg.startsWith("-") && !args.comicDir) {
      args.comicDir = arg;
    }
  }

  if (!args.comicDir) {
    printHelp();
    return null;
  }

  return args;
}

function findComicPages(comicDir: string): PageInfo[] {
  if (!existsSync(comicDir)) {
    throw new Error(`Comic directory not found: ${comicDir}`);
  }

  const pagePattern = /^(\d+)-(cover|page)(-[\w-]+)?\.(png|jpg|jpeg)$/i;
  const pages = readdirSync(comicDir)
    .filter((filename) => pagePattern.test(filename))
    .map((filename) => {
      const match = filename.match(pagePattern);
      return {
        filename,
        path: join(comicDir, filename),
        index: Number.parseInt(match?.[1] ?? "0", 10),
        kind: (match?.[2] ?? "page") as "cover" | "page",
      };
    })
    .sort((a, b) => a.index - b.index || (a.kind === "cover" ? -1 : 1));

  if (pages.length === 0) {
    throw new Error(`No comic pages found in ${comicDir}. Expected files like 00-cover-topic.png or 01-page-topic.jpg.`);
  }

  return pages;
}

function toErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

function isMissingPdfLibError(error: unknown): boolean {
  const message = toErrorMessage(error);
  return message.includes("pdf-lib") && (message.includes("Cannot find package") || message.includes("Cannot find module"));
}

async function loadPdfDocument() {
  try {
    const module = await import("pdf-lib");
    return module.PDFDocument;
  } catch (error) {
    if (isMissingPdfLibError(error)) {
      throw new Error(
        "Missing local dependency `pdf-lib` for comic PDF merging. Run `npm run bootstrap` in the comic skill directory, then retry this command."
      );
    }
    throw error;
  }
}

async function createPdf(pages: PageInfo[], outputPath: string): Promise<void> {
  const PDFDocument = await loadPdfDocument();
  const pdf = await PDFDocument.create();
  pdf.setAuthor("comic");
  pdf.setSubject("Generated comic pages");

  for (const page of pages) {
    const bytes = readFileSync(page.path);
    const lower = page.filename.toLowerCase();
    const embedded = lower.endsWith(".png")
      ? await pdf.embedPng(bytes)
      : await pdf.embedJpg(bytes);

    const pdfPage = pdf.addPage([embedded.width, embedded.height]);
    pdfPage.drawImage(embedded, {
      x: 0,
      y: 0,
      width: embedded.width,
      height: embedded.height,
    });
  }

  await Bun.write(outputPath, await pdf.save());
}

function defaultOutputPath(comicDir: string): string {
  return join(comicDir, `${basename(resolve(comicDir))}.pdf`);
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (!args) {
    process.exit(1);
  }

  const comicDir = resolve(args.comicDir);
  const outputPath = resolve(args.output ?? defaultOutputPath(comicDir));
  const pages = findComicPages(comicDir);

  await createPdf(pages, outputPath);

  if (args.json) {
    console.log(
      JSON.stringify(
        {
          comicDir,
          output: outputPath,
          totalPages: pages.length,
          files: pages.map((page) => page.filename),
        },
        null,
        2
      )
    );
    return;
  }

  console.log(`Created PDF: ${outputPath}`);
  console.log(`Pages: ${pages.length}`);
}

main().catch((error) => {
  console.error(toErrorMessage(error));
  process.exit(1);
});
