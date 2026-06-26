import { createHash } from "node:crypto";
import { basename, extname, resolve } from "node:path";
import { access, readdir, stat } from "node:fs/promises";
import type { Dirent } from "node:fs";
import type { LocalFile, LocalFileRoute } from "@caixu/contracts";
import type { PdfRenderer } from "./pdf-render.js";

const textExtensions = new Set([
  ".txt",
  ".md",
  ".json",
  ".csv",
  ".tsv",
  ".yaml",
  ".yml"
]);

const officeExtensions = new Set([
  ".doc",
  ".docx",
  ".xls",
  ".xlsx",
  ".ppt",
  ".pptx"
]);

const imageExtensions = new Set([".png", ".jpg", ".jpeg"]);
const skippedExtensions = new Set([".zip", ".mhtml", ".tif", ".tiff"]);

const mimeByExt: Record<string, string> = {
  ".txt": "text/plain",
  ".md": "text/markdown",
  ".json": "application/json",
  ".csv": "text/csv",
  ".tsv": "text/tab-separated-values",
  ".yaml": "application/yaml",
  ".yml": "application/yaml",
  ".pdf": "application/pdf",
  ".doc": "application/msword",
  ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".xls": "application/vnd.ms-excel",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".ppt": "application/vnd.ms-powerpoint",
  ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg"
};

export type RuntimeConfig = {
  parserMode: "lite" | "export";
  zhipuOcrEnabled: boolean;
  vlmModel: string;
  vlmPdfRenderer: PdfRenderer;
  visualPreprocessEnabled: boolean;
  visualPreprocessThresholdBytes: number;
  visualPreprocessMaxWidth: number;
  parserApiKey: string;
  ocrApiKey: string;
  vlmApiKey: string;
};

function normalizeBooleanEnv(value: string | undefined, defaultValue: boolean): boolean {
  if (typeof value !== "string") {
    return defaultValue;
  }
  const normalized = value.trim().toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "off"].includes(normalized)) {
    return false;
  }
  return defaultValue;
}

function normalizeIntegerEnv(value: string | undefined, fallback: number, minimum = 0): number {
  const parsed = Number.parseInt(value?.trim() ?? "", 10);
  if (!Number.isFinite(parsed) || parsed < minimum) {
    return fallback;
  }
  return parsed;
}

export function getRuntimeConfig(): RuntimeConfig {
  const fallbackApiKey = process.env.ZHIPU_API_KEY?.trim() ?? "";
  return {
    parserMode: process.env.CAIXU_ZHIPU_PARSER_MODE === "export" ? "export" : "lite",
    zhipuOcrEnabled: normalizeBooleanEnv(process.env.CAIXU_ZHIPU_OCR_ENABLED, false),
    vlmModel: process.env.CAIXU_VLM_MODEL?.trim() || "glm-4.6v",
    vlmPdfRenderer: process.env.CAIXU_VLM_PDF_RENDERER === "pdftocairo" ? "pdftocairo" : "pdftoppm",
    visualPreprocessEnabled: normalizeBooleanEnv(
      process.env.CAIXU_VISUAL_PREPROCESS_ENABLED,
      true
    ),
    visualPreprocessThresholdBytes: normalizeIntegerEnv(
      process.env.CAIXU_VISUAL_PREPROCESS_THRESHOLD_BYTES,
      0,
      0
    ),
    visualPreprocessMaxWidth: normalizeIntegerEnv(
      process.env.CAIXU_VISUAL_PREPROCESS_MAX_WIDTH,
      1600,
      256
    ),
    parserApiKey:
      process.env.CAIXU_ZHIPU_PARSER_API_KEY?.trim() || fallbackApiKey,
    ocrApiKey:
      process.env.CAIXU_ZHIPU_OCR_API_KEY?.trim() ||
      process.env.CAIXU_ZHIPU_PARSER_API_KEY?.trim() ||
      fallbackApiKey,
    vlmApiKey:
      process.env.CAIXU_ZHIPU_VLM_API_KEY?.trim() || fallbackApiKey
  };
}

export function isTextExtension(extension: string): boolean {
  return textExtensions.has(extension.toLowerCase());
}

export function isImageExtension(extension: string): boolean {
  return imageExtensions.has(extension.toLowerCase());
}

export function isOfficeExtension(extension: string): boolean {
  return officeExtensions.has(extension.toLowerCase());
}

export function guessMimeType(filePath: string): string {
  return mimeByExt[extname(filePath).toLowerCase()] ?? "application/octet-stream";
}

export function getLiveFileType(filePath: string): string {
  return extname(filePath).replace(/^\./u, "").toUpperCase();
}

export function summarizeText(text: string): string {
  const compact = text.replace(/\s+/g, " ").trim();
  return compact.length <= 160 ? compact : `${compact.slice(0, 157)}...`;
}

export function createDeterministicFileId(filePath: string): string {
  const normalizedPath = resolve(filePath);
  return `file_${createHash("sha1").update(normalizedPath).digest("hex").slice(0, 12)}`;
}

export function classifySuggestedRoute(filePath: string, mimeType: string, config: RuntimeConfig): {
  route: LocalFileRoute;
  skipReason: string | null;
} {
  const extension = extname(filePath).toLowerCase();
  const fileName = basename(filePath);

  if (fileName.startsWith("~$")) {
    return {
      route: "skip",
      skipReason: "office_temporary_lock_file"
    };
  }

  if (isTextExtension(extension) || mimeType.startsWith("text/")) {
    return { route: "text", skipReason: null };
  }

  if (extension === ".pdf" || isOfficeExtension(extension)) {
    return {
      route: config.parserMode === "export" ? "parser_export" : "parser_lite",
      skipReason: null
    };
  }

  if (isImageExtension(extension)) {
    return {
      route: config.zhipuOcrEnabled ? "ocr" : "vlm",
      skipReason: null
    };
  }

  if (skippedExtensions.has(extension)) {
    return {
      route: "skip",
      skipReason: `unsupported_${extension.replace(/^\./u, "")}_for_ingestion`
    };
  }

  return {
    route: "skip",
    skipReason: "unsupported_file_type"
  };
}

async function walkFiles(dir: string, out: string[] = []): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = resolve(dir, entry.name);
    if (entry.isDirectory()) {
      await walkFiles(full, out);
    } else if (entry.isFile()) {
      out.push(full);
    }
  }
  return out;
}

export async function listLocalFiles(inputRoot: string): Promise<LocalFile[]> {
  const resolvedRoot = resolve(inputRoot);
  await access(resolvedRoot);
  const filePaths = (await walkFiles(resolvedRoot)).sort((left, right) =>
    left.localeCompare(right)
  );
  const config = getRuntimeConfig();
  const files: LocalFile[] = [];

  for (const filePath of filePaths) {
    const fileStat = await stat(filePath);
    const mimeType = guessMimeType(filePath);
    const extension = extname(filePath).toLowerCase() || "(none)";
    const route = classifySuggestedRoute(filePath, mimeType, config);

    files.push({
      file_id: createDeterministicFileId(filePath),
      file_name: basename(filePath),
      file_path: filePath,
      mime_type: mimeType,
      extension,
      size_bytes: fileStat.size,
      suggested_route: route.route,
      skip_reason: route.skipReason
    });
  }

  return files;
}

export type VisualInputItem = {
  file_name: string;
  file_path: string;
  mime_type: string;
};
