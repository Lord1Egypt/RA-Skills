#!/usr/bin/env bun
import { readFile, writeFile, copyFile } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";

interface CliArgs {
  article: string | null;
  outline: string | null;
  imagesDir: string | null;
  output: string | null;
  onMissingAnchor: "end" | "skip" | "fail";
  json: boolean;
}

interface OutlineEntry {
  index: number;
  position: string;
  filename: string;
  description: string;
}

interface InsertResult {
  index: number;
  filename: string;
  position: string;
  status: "inserted" | "skipped" | "failed";
  reason?: string;
}

interface HeadingMatch {
  heading: string;
  start: number;
  end: number;
}

interface ResultSummary {
  inserted: number;
  insertedWithFallback: number;
  skipped: number;
  failed: number;
}

function printHelp(): void {
  console.log(`Usage: bun scripts/insert-images.ts --article <file> --outline <file> [options]

Options:
  --article <path>      Article markdown path
  --outline <path>      Outline markdown path
  --images-dir <path>   Directory containing generated images (default: outline directory)
  -o, --output <path>   Write updated article to a new path
  --on-missing-anchor <mode>
                       What to do when a heading or text anchor is missing: end|skip|fail (default: end)
  --json                JSON output
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs | null {
  const args: CliArgs = {
    article: null,
    outline: null,
    imagesDir: null,
    output: null,
    onMissingAnchor: "end",
    json: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") {
      printHelp();
      process.exit(0);
    }
    if (arg === "--article") {
      args.article = argv[++i] ?? null;
      continue;
    }
    if (arg === "--outline") {
      args.outline = argv[++i] ?? null;
      continue;
    }
    if (arg === "--images-dir") {
      args.imagesDir = argv[++i] ?? null;
      continue;
    }
    if (arg === "-o" || arg === "--output") {
      args.output = argv[++i] ?? null;
      continue;
    }
    if (arg === "--on-missing-anchor") {
      const value = (argv[++i] ?? "").trim().toLowerCase();
      if (value === "end" || value === "skip" || value === "fail") {
        args.onMissingAnchor = value;
      } else {
        throw new Error(`Invalid --on-missing-anchor: ${value || "(empty)"}`);
      }
      continue;
    }
    if (arg === "--json") {
      args.json = true;
      continue;
    }
  }

  if (!args.article || !args.outline) {
    printHelp();
    return null;
  }
  return args;
}

function parseOutline(content: string): OutlineEntry[] {
  const entries: OutlineEntry[] = [];
  const blocks = content.replace(/\r\n/g, "\n").split(/^## Illustration\s+/m).slice(1);

  for (const block of blocks) {
    const firstBreak = block.indexOf("\n");
    const indexText = firstBreak === -1 ? block.trim() : block.slice(0, firstBreak).trim();
    const body = firstBreak === -1 ? "" : block.slice(firstBreak + 1);
    const index = Number.parseInt(indexText, 10);
    const position = body.match(/\*\*Position\*\*:\s*(.+)/)?.[1]?.trim();
    const filename = body.match(/\*\*Filename\*\*:\s*(.+)/)?.[1]?.trim();
    const description = (
      body.match(/\*\*Description\*\*:\s*(.+)/)?.[1]
      ?? body.match(/\*\*Purpose\*\*:\s*(.+)/)?.[1]
      ?? body.match(/\*\*Visual Content\*\*:\s*(.+)/)?.[1]
      ?? `Illustration ${index}`
    ).trim();

    if (!position || !filename) {
      continue;
    }

    entries.push({ index, position, filename, description });
  }

  return entries.sort((a, b) => a.index - b.index);
}

function escapeRegExp(text: string): string {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalizeHeadingText(text: string): string {
  return text
    .toLowerCase()
    .replace(/^\d+(?:[.)-]\s*|\s+)/, "")
    .replace(/[^\p{L}\p{N}\s-]+/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeInsertedBlock(markdown: string): string {
  return markdown.trim() + "\n";
}

function buildImageMarkdown(description: string, relativePath: string): string {
  const alt = description.replace(/\s+/g, " ").trim();
  return `![${alt}](${relativePath})`;
}

function alreadyInserted(article: string, relativePath: string): boolean {
  return article.includes(`](${relativePath})`);
}

function insertAtEnd(article: string, block: string): string {
  return `${article.trimEnd()}\n\n${normalizeInsertedBlock(block)}`;
}

function extractHeadings(article: string): HeadingMatch[] {
  const normalized = article.replace(/\r\n/g, "\n");
  const headings: HeadingMatch[] = [];
  const lines = normalized.split("\n");
  let offset = 0;

  for (let index = 0; index < lines.length; index++) {
    const line = lines[index] ?? "";
    const atx = line.match(/^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$/);
    if (atx) {
      headings.push({
        heading: atx[1]!.trim(),
        start: offset,
        end: offset + line.length,
      });
      offset += line.length + 1;
      continue;
    }

    const next = lines[index + 1] ?? "";
    const setext = next.match(/^\s{0,3}(=+|-+)\s*$/);
    if (setext && line.trim()) {
      headings.push({
        heading: line.trim(),
        start: offset,
        end: offset + line.length,
      });
      offset += line.length + 1;
      offset += next.length + 1;
      index += 1;
      continue;
    }

    offset += line.length + 1;
  }

  return headings;
}

function insertByHeading(
  article: string,
  heading: string,
  block: string,
  mode: "before" | "after"
): { article: string; matchedHeading?: string } | null {
  const headings = extractHeadings(article);
  const exact = headings.find((candidate) => candidate.heading === heading);
  const target = exact
    ?? headings.find((candidate) => normalizeHeadingText(candidate.heading) === normalizeHeadingText(heading));

  if (!target) {
    return null;
  }

  if (mode === "before") {
    return {
      article: `${article.slice(0, target.start)}${normalizeInsertedBlock(block)}\n${article.slice(target.start)}`,
      matchedHeading: target.heading,
    };
  }

  return {
    article: `${article.slice(0, target.end)}\n\n${normalizeInsertedBlock(block)}${article.slice(target.end)}`,
    matchedHeading: target.heading,
  };
}

function insertAfterText(article: string, snippet: string, block: string): string | null {
  const index = article.indexOf(snippet);
  if (index === -1) {
    return null;
  }
  const end = index + snippet.length;
  return `${article.slice(0, end)}\n\n${normalizeInsertedBlock(block)}${article.slice(end)}`;
}

function resolveMissingAnchor(
  article: string,
  entry: OutlineEntry,
  imageMarkdown: string,
  reason: string,
  strategy: CliArgs["onMissingAnchor"]
): { article: string; status: InsertResult } {
  if (strategy === "end") {
    return {
      article: insertAtEnd(article, imageMarkdown),
      status: {
        index: entry.index,
        filename: entry.filename,
        position: entry.position,
        status: "inserted",
        reason: `${reason}; appended at end`,
      },
    };
  }

  if (strategy === "skip") {
    return {
      article,
      status: {
        index: entry.index,
        filename: entry.filename,
        position: entry.position,
        status: "skipped",
        reason,
      },
    };
  }

  return {
    article,
    status: { index: entry.index, filename: entry.filename, position: entry.position, status: "failed", reason },
  };
}

function applyEntry(
  article: string,
  entry: OutlineEntry,
  imageMarkdown: string,
  onMissingAnchor: CliArgs["onMissingAnchor"]
): { article: string; status: InsertResult } {
  const raw = entry.position.trim();
  if (raw === "end") {
    return {
      article: insertAtEnd(article, imageMarkdown),
      status: { index: entry.index, filename: entry.filename, position: entry.position, status: "inserted" },
    };
  }

  if (raw.startsWith("after-heading:")) {
    const heading = raw.slice("after-heading:".length).trim();
    const next = insertByHeading(article, heading, imageMarkdown, "after");
    if (next) {
      const matchedReason =
        next.matchedHeading && next.matchedHeading !== heading
          ? `Heading matched via normalized lookup: ${next.matchedHeading}`
          : undefined;
      return {
        article: next.article,
        status: {
          index: entry.index,
          filename: entry.filename,
          position: entry.position,
          status: "inserted",
          reason: matchedReason,
        },
      };
    }
    return resolveMissingAnchor(article, entry, imageMarkdown, `Heading not found: ${heading}`, onMissingAnchor);
  }

  if (raw.startsWith("before-heading:")) {
    const heading = raw.slice("before-heading:".length).trim();
    const next = insertByHeading(article, heading, imageMarkdown, "before");
    if (next) {
      const matchedReason =
        next.matchedHeading && next.matchedHeading !== heading
          ? `Heading matched via normalized lookup: ${next.matchedHeading}`
          : undefined;
      return {
        article: next.article,
        status: {
          index: entry.index,
          filename: entry.filename,
          position: entry.position,
          status: "inserted",
          reason: matchedReason,
        },
      };
    }
    return resolveMissingAnchor(article, entry, imageMarkdown, `Heading not found: ${heading}`, onMissingAnchor);
  }

  if (raw.startsWith("after-text:")) {
    const snippet = raw.slice("after-text:".length).trim();
    const next = insertAfterText(article, snippet, imageMarkdown);
    if (next) {
      return {
        article: next,
        status: { index: entry.index, filename: entry.filename, position: entry.position, status: "inserted" },
      };
    }
    return resolveMissingAnchor(article, entry, imageMarkdown, `Text snippet not found: ${snippet}`, onMissingAnchor);
  }

  return {
    article,
    status: { index: entry.index, filename: entry.filename, position: entry.position, status: "failed", reason: `Unsupported position syntax: ${raw}` },
  };
}

function summarizeResults(results: InsertResult[]): ResultSummary {
  return {
    inserted: results.filter((result) => result.status === "inserted").length,
    insertedWithFallback: results.filter(
      (result) => result.status === "inserted" && Boolean(result.reason)
    ).length,
    skipped: results.filter((result) => result.status === "skipped").length,
    failed: results.filter((result) => result.status === "failed").length,
  };
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (!args) {
    process.exit(1);
  }

  const articlePath = resolve(args.article);
  const outlinePath = resolve(args.outline);
  const outputPath = resolve(args.output ?? articlePath);
  const imagesDir = resolve(args.imagesDir ?? dirname(outlinePath));

  const [articleContent, outlineContent] = await Promise.all([
    readFile(articlePath, "utf8"),
    readFile(outlinePath, "utf8"),
  ]);

  const entries = parseOutline(outlineContent);
  if (entries.length === 0) {
    throw new Error("No valid illustration entries found in outline.");
  }

  let nextArticle = articleContent.replace(/\r\n/g, "\n");
  const results: InsertResult[] = [];

  for (const entry of entries) {
    const imagePath = join(imagesDir, entry.filename);
    const relativePath = relative(dirname(outputPath), imagePath).replaceAll("\\", "/");
    const imageMarkdown = buildImageMarkdown(entry.description, relativePath);

    if (alreadyInserted(nextArticle, relativePath)) {
      results.push({
        index: entry.index,
        filename: entry.filename,
        position: entry.position,
        status: "skipped",
        reason: "Image already referenced in article",
      });
      continue;
    }

    const applied = applyEntry(nextArticle, entry, imageMarkdown, args.onMissingAnchor);
    nextArticle = applied.article;
    results.push(applied.status);
  }

  if (!args.output) {
    const backupPath = `${articlePath}.backup-${Date.now()}.md`;
    await copyFile(articlePath, backupPath);
  }

  await writeFile(outputPath, nextArticle, "utf8");

  if (args.json) {
    const summary = summarizeResults(results);
    console.log(
      JSON.stringify(
        {
          article: articlePath,
          output: outputPath,
          outline: outlinePath,
          imagesDir,
          summary,
          warnings: results.filter((result) => Boolean(result.reason)).map((result) => ({
            index: result.index,
            filename: result.filename,
            message: result.reason,
          })),
          results,
        },
        null,
        2
      )
    );
    return;
  }

  const summary = summarizeResults(results);
  console.log(`Updated article: ${outputPath}`);
  console.log(
    `Summary: inserted ${summary.inserted} (${summary.insertedWithFallback} with fallback), skipped ${summary.skipped}, failed ${summary.failed}`
  );
  for (const result of results) {
    const suffix = result.reason ? ` (${result.reason})` : "";
    console.log(`[${result.status}] #${result.index} ${result.filename}${suffix}`);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
