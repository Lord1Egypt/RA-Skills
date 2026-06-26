import { mkdtemp, mkdir, writeFile } from "node:fs/promises";
import { basename, join } from "node:path";
import { tmpdir } from "node:os";
import {
  type RenderPdfPagesData,
  localFileSchema,
  makeToolResult
} from "@caixu/contracts";
import { toPipelineErrorRecord } from "./parse-pipeline-error.js";
import { getRuntimeConfig } from "./low-level-common.js";
import { renderPdfToPngBuffers, type PdfRenderer } from "./pdf-render.js";

export async function renderPdfPagesTool(input: {
  file: unknown;
  renderer?: PdfRenderer;
}) {
  const parsedFile = localFileSchema.safeParse(input.file);
  if (!parsedFile.success) {
    return makeToolResult<RenderPdfPagesData>("failed", undefined, {
      errors: [
        {
          code: "RENDER_PDF_PAGES_INVALID_INPUT",
          message: parsedFile.error.issues
            .map((issue) => `${issue.path.join(".") || "file"}: ${issue.message}`)
            .join("; "),
          retryable: false
        }
      ]
    });
  }

  const file = parsedFile.data;
  const renderer = input.renderer ?? getRuntimeConfig().vlmPdfRenderer;

  try {
    const renderedPages = await renderPdfToPngBuffers({
      filePath: file.file_path,
      renderer
    });
    const workDir = await mkdtemp(join(tmpdir(), "caixu-rendered-pdf-"));
    const pageDir = join(workDir, `${basename(file.file_name)}-pages`);
    await mkdir(pageDir, { recursive: true });
    const pages = [];
    for (const [index, page] of renderedPages.entries()) {
      const pagePath = join(pageDir, page.fileName);
      await writeFile(pagePath, page.buffer);
      pages.push({
        page_number: index + 1,
        file_name: page.fileName,
        file_path: pagePath,
        mime_type: page.mimeType
      });
    }
    return makeToolResult("success", {
      file,
      pages
    } satisfies RenderPdfPagesData);
  } catch (error) {
    const parsedError = toPipelineErrorRecord(error);
    return makeToolResult<RenderPdfPagesData>("failed", undefined, {
      errors: [
        {
          code: parsedError.code,
          message: parsedError.message,
          retryable: parsedError.retryable,
          file_id: file.file_id,
          file_name: file.file_name
        }
      ]
    });
  }
}
