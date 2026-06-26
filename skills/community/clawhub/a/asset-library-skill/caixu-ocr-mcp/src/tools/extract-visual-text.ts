import {
  type ExtractVisualTextData,
  makeToolResult
} from "@caixu/contracts";
import { toPipelineErrorRecord } from "./parse-pipeline-error.js";
import { renderPdfToPngBuffers } from "./pdf-render.js";
import {
  getRuntimeConfig,
  type VisualInputItem
} from "./low-level-common.js";
import { prepareRasterImageForVision } from "./prepare-raster-image.js";
import { runZhipuLayoutOcr } from "./zhipu-layout-ocr.js";
import { runZhipuVlmOcr } from "./zhipu-vlm.js";

type VisualEngine = "ocr" | "vlm";

async function runSingleItem(input: {
  item: VisualInputItem;
  engine: VisualEngine;
  config: ReturnType<typeof getRuntimeConfig>;
  ocrApiKey: string;
  vlmApiKey: string;
  vlmModel: string;
  pdfRenderer: "pdftoppm" | "pdftocairo";
}) {
  if (input.item.mime_type === "application/pdf" && input.engine === "vlm") {
    const pages = await renderPdfToPngBuffers({
      filePath: input.item.file_path,
      renderer: input.pdfRenderer
    });
    const outputs = [];
    for (const page of pages) {
      const text = await runZhipuVlmOcr({
        apiKey: input.vlmApiKey,
        model: input.vlmModel,
        buffer: page.buffer,
        mimeType: page.mimeType,
        label: `${input.item.file_name}/${page.fileName}`
      });
      outputs.push({
        file_name: page.fileName,
        file_path: input.item.file_path,
        mime_type: page.mimeType,
        text
      });
    }
    return outputs;
  }

  const prepared = await prepareRasterImageForVision({
    filePath: input.item.file_path,
    mimeType: input.item.mime_type,
    config: {
      enabled: input.config.visualPreprocessEnabled,
      thresholdBytes: input.config.visualPreprocessThresholdBytes,
      maxWidth: input.config.visualPreprocessMaxWidth
    }
  });
  const buffer = prepared.buffer;
  const effectiveMimeType = prepared.prepared ? prepared.mimeType : input.item.mime_type;
  if (input.engine === "ocr") {
    const text = await runZhipuLayoutOcr({
      apiKey: input.ocrApiKey,
      buffer,
      mimeType: effectiveMimeType
    });
    return [
      {
        file_name: input.item.file_name,
        file_path: input.item.file_path,
        mime_type: effectiveMimeType,
        text
      }
    ];
  }

  const text = await runZhipuVlmOcr({
    apiKey: input.vlmApiKey,
    model: input.vlmModel,
    buffer,
    mimeType: effectiveMimeType,
    label: input.item.file_name
  });
  return [
    {
      file_name: input.item.file_name,
      file_path: input.item.file_path,
      mime_type: effectiveMimeType,
      text
    }
  ];
}

export async function extractVisualTextTool(input: {
  engine?: VisualEngine;
  items: Array<VisualInputItem>;
}) {
  const config = getRuntimeConfig();
  const engine = input.engine ?? (config.zhipuOcrEnabled ? "ocr" : "vlm");
  const outputs: ExtractVisualTextData["outputs"] = [];
  const warnings: ExtractVisualTextData["warnings"] = [];

  if (input.items.length === 0) {
    return makeToolResult<ExtractVisualTextData>("failed", undefined, {
      errors: [
        {
          code: "EXTRACT_VISUAL_TEXT_NO_ITEMS",
          message: "items must contain at least one file.",
          retryable: false
        }
      ]
    });
  }

  if (engine === "ocr" && !config.ocrApiKey) {
    return makeToolResult<ExtractVisualTextData>("failed", undefined, {
      errors: [
        {
          code: "ZHIPU_API_KEY_MISSING",
          message: "CAIXU_ZHIPU_OCR_API_KEY or ZHIPU_API_KEY is required.",
          retryable: false
        }
      ]
    });
  }

  if (engine === "vlm" && !config.vlmApiKey) {
    return makeToolResult<ExtractVisualTextData>("failed", undefined, {
      errors: [
        {
          code: "ZHIPU_API_KEY_MISSING",
          message: "CAIXU_ZHIPU_VLM_API_KEY or ZHIPU_API_KEY is required.",
          retryable: false
        }
      ]
    });
  }

  for (const item of input.items) {
    try {
      outputs.push(
        ...(await runSingleItem({
          item,
          engine,
          config,
          ocrApiKey: config.ocrApiKey,
          vlmApiKey: config.vlmApiKey,
          vlmModel: config.vlmModel,
          pdfRenderer: config.vlmPdfRenderer
        }))
      );
    } catch (error) {
      const parsedError = toPipelineErrorRecord(error);
      warnings.push({
        code: parsedError.code,
        message: parsedError.message,
        retryable: parsedError.retryable,
        file_name: item.file_name
      });
    }
  }

  if (outputs.length === 0) {
    return makeToolResult<ExtractVisualTextData>("failed", undefined, {
      errors: warnings
    });
  }

  const data: ExtractVisualTextData = {
    engine,
    provider: engine === "ocr" ? "zhipu_ocr" : "zhipu_vlm",
    outputs,
    warnings
  };
  return makeToolResult(warnings.length > 0 ? "partial" : "success", data, {
    errors: []
  });
}
