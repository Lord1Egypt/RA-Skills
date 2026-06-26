import { execFile } from "node:child_process";
import { mkdtemp, readdir, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import { ParsePipelineError } from "./parse-pipeline-error.js";

const execFileAsync = promisify(execFile);

export type PdfRenderer = "pdftoppm" | "pdftocairo";

export type RenderedPdfImage = {
  fileName: string;
  mimeType: "image/png";
  buffer: Buffer;
};

function sortPageImages(left: string, right: string): number {
  const leftMatch = left.match(/-(\d+)\.png$/u);
  const rightMatch = right.match(/-(\d+)\.png$/u);
  const leftPage = leftMatch ? Number.parseInt(leftMatch[1] ?? "0", 10) : 0;
  const rightPage = rightMatch ? Number.parseInt(rightMatch[1] ?? "0", 10) : 0;
  return leftPage - rightPage || left.localeCompare(right);
}

export async function renderPdfToPngBuffers(input: {
  filePath: string;
  renderer: PdfRenderer;
}): Promise<RenderedPdfImage[]> {
  const workDir = await mkdtemp(join(tmpdir(), "caixu-pdf-render-"));
  const outputPrefix = join(workDir, "page");

  try {
    const args =
      input.renderer === "pdftocairo"
        ? ["-png", input.filePath, outputPrefix]
        : ["-png", input.filePath, outputPrefix];

    await execFileAsync(input.renderer, args, {
      timeout: 120_000,
      maxBuffer: 16 * 1024 * 1024
    });

    const files = (await readdir(workDir))
      .filter((name) => name.toLowerCase().endsWith(".png"))
      .sort(sortPageImages);

    if (files.length === 0) {
      throw new ParsePipelineError({
        code: "PDF_RENDER_FAILED",
        message: `PDF renderer ${input.renderer} did not produce any PNG pages`,
        retryable: false
      });
    }

    return Promise.all(
      files.map(async (fileName) => ({
        fileName,
        mimeType: "image/png" as const,
        buffer: await readFile(join(workDir, fileName))
      }))
    );
  } catch (error) {
    if (error instanceof ParsePipelineError) {
      throw error;
    }

    throw new ParsePipelineError({
      code: "PDF_RENDER_FAILED",
      message:
        error instanceof Error
          ? `Failed to render PDF via ${input.renderer}: ${error.message}`
          : `Failed to render PDF via ${input.renderer}`,
      retryable: false
    });
  } finally {
    await rm(workDir, { recursive: true, force: true });
  }
}
