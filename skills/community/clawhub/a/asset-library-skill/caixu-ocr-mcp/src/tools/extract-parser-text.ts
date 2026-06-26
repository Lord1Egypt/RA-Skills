import { mkdtemp, mkdir, writeFile } from "node:fs/promises";
import { basename, join } from "node:path";
import { tmpdir } from "node:os";
import {
  type ExtractParserTextData,
  type ToolError,
  localFileSchema,
  makeToolResult
} from "@caixu/contracts";
import { toPipelineErrorRecord } from "./parse-pipeline-error.js";
import {
  getLiveFileType,
  getRuntimeConfig
} from "./low-level-common.js";
import { extractVisualTextTool } from "./extract-visual-text.js";
import { parseWithZhipuParser, type ZhipuParserMode } from "./zhipu-file-parser.js";

async function persistExportAssets(input: {
  fileName: string;
  assets: Array<{ fileName: string; mimeType: string; buffer: Buffer }>;
}) {
  const workDir = await mkdtemp(join(tmpdir(), "caixu-parser-export-"));
  const exportDir = join(workDir, `${basename(input.fileName)}-assets`);
  await mkdir(exportDir, { recursive: true });
  const persistedAssets = [];
  for (const asset of input.assets) {
    const assetPath = join(exportDir, asset.fileName);
    await writeFile(assetPath, asset.buffer);
    persistedAssets.push({
      file_name: asset.fileName,
      file_path: assetPath,
      mime_type: asset.mimeType
    });
  }
  return persistedAssets;
}

export async function extractParserTextTool(input: {
  file: unknown;
  mode?: ZhipuParserMode;
}) {
  const parsedFile = localFileSchema.safeParse(input.file);
  if (!parsedFile.success) {
    return makeToolResult<ExtractParserTextData>("failed", undefined, {
      errors: [
        {
          code: "EXTRACT_PARSER_TEXT_INVALID_INPUT",
          message: parsedFile.error.issues
            .map((issue) => `${issue.path.join(".") || "file"}: ${issue.message}`)
            .join("; "),
          retryable: false
        }
      ]
    });
  }

  const file = parsedFile.data;
  const config = getRuntimeConfig();
  const mode = input.mode ?? config.parserMode;
  const visualEngine = config.zhipuOcrEnabled ? "ocr" : "vlm";

  if (!config.parserApiKey) {
    return makeToolResult<ExtractParserTextData>("failed", undefined, {
      errors: [
        {
          code: "ZHIPU_API_KEY_MISSING",
          message: "CAIXU_ZHIPU_PARSER_API_KEY or ZHIPU_API_KEY is required.",
          retryable: false,
          file_id: file.file_id,
          file_name: file.file_name
        }
      ]
    });
  }

  try {
    const result = await parseWithZhipuParser({
      filePath: file.file_path,
      mimeType: file.mime_type,
      fileType: getLiveFileType(file.file_path),
      apiKey: config.parserApiKey,
      mode
    });
    const exportAssets =
      mode === "export" && result.assets.length > 0
        ? await persistExportAssets({
            fileName: file.file_name,
            assets: result.assets
          })
        : [];
    let text = result.text;
    let provider: ExtractParserTextData["provider"] = result.provider;
    const warnings: ToolError[] = result.branchErrors.map((error) => ({
      code: error.code,
      message: error.message,
      retryable: error.retryable,
      file_id: file.file_id,
      file_name: file.file_name
    }));

    if (file.mime_type === "application/pdf" && !text) {
      const visualResult = await extractVisualTextTool({
        engine: visualEngine,
        items: [
          {
            file_name: file.file_name,
            file_path: file.file_path,
            mime_type: file.mime_type
          }
        ]
      });

      const visualWarnings: ToolError[] = (visualResult.data?.warnings ?? []).map((warning) => ({
          code: warning.code,
          message: warning.message,
          retryable: warning.retryable,
          file_id: warning.file_id ?? file.file_id,
          file_name: warning.file_name ?? file.file_name,
          asset_id: warning.asset_id
      }));
      warnings.push(...visualWarnings);

      if (visualResult.data?.outputs?.length) {
        text = visualResult.data.outputs
          .map((output) => output.text?.trim() ?? "")
          .filter(Boolean)
          .join("\n\n")
          .trim() || null;
        provider = text ? visualResult.data.provider : provider;
      }

      if (visualResult.status === "failed" && !text) {
        return makeToolResult<ExtractParserTextData>("failed", undefined, {
          errors: [
            ...warnings,
            ...(visualResult.errors ?? [])
          ]
        });
      }
    }

    const data: ExtractParserTextData = {
      file,
      mode,
      provider:
        text && text !== result.text
          ? result.text
            ? "hybrid"
            : provider
          : provider,
      text,
      export_assets: exportAssets,
      warnings
    };
    const status =
      data.warnings.length > 0 || (!data.text && data.export_assets.length > 0)
        ? "partial"
        : "success";
    return makeToolResult(status, data);
  } catch (error) {
    const parsedError = toPipelineErrorRecord(error);
    if (file.mime_type === "application/pdf") {
      const visualResult = await extractVisualTextTool({
        engine: visualEngine,
        items: [
          {
            file_name: file.file_name,
            file_path: file.file_path,
            mime_type: file.mime_type
          }
        ]
      });

      if (visualResult.data?.outputs?.length) {
        const text = visualResult.data.outputs
          .map((output) => output.text?.trim() ?? "")
          .filter(Boolean)
          .join("\n\n")
          .trim();
        if (text) {
          const warnings = [
            {
              code: parsedError.code,
              message: parsedError.message,
              retryable: parsedError.retryable,
              file_id: file.file_id,
              file_name: file.file_name
            },
            ...(visualResult.data.warnings ?? [])
          ];
          return makeToolResult("partial", {
            file,
            mode,
            provider: visualResult.data.provider,
            text,
            export_assets: [],
            warnings
          } satisfies ExtractParserTextData);
        }
      }
    }

    return makeToolResult<ExtractParserTextData>("failed", undefined, {
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
