import { ParsePipelineError } from "./parse-pipeline-error.js";
import {
  fetchWithZhipuRetry,
  getZhipuHttpRetryConfig,
  type ZhipuHttpProgressEvent
} from "./zhipu-http.js";

const layoutParsingEndpoint = "https://open.bigmodel.cn/api/paas/v4/layout_parsing";
const requestTimeoutMs = 120_000;

type JsonRecord = Record<string, unknown>;

function parseJsonSafely(rawText: string): JsonRecord | null {
  try {
    const parsed = JSON.parse(rawText);
    if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
      return parsed as JsonRecord;
    }
  } catch {
    return null;
  }

  return null;
}

function readMessage(payload: JsonRecord | null, fallback: string): string {
  if (!payload) {
    return fallback;
  }

  if (payload.error && typeof payload.error === "object" && !Array.isArray(payload.error)) {
    const error = payload.error as JsonRecord;
    if (typeof error.message === "string" && error.message.trim()) {
      return error.message;
    }
  }

  if (typeof payload.message === "string" && payload.message.trim()) {
    return payload.message;
  }

  return fallback;
}

function bufferToDataUrl(buffer: Buffer, mimeType: string): string {
  return `data:${mimeType};base64,${buffer.toString("base64")}`;
}

function collapseLayoutDetails(payload: JsonRecord | null): string {
  if (!payload || !Array.isArray(payload.layout_details)) {
    return "";
  }

  const lines: string[] = [];
  for (const page of payload.layout_details) {
    if (!Array.isArray(page)) {
      continue;
    }
    for (const item of page) {
      if (!item || typeof item !== "object" || Array.isArray(item)) {
        continue;
      }
      const record = item as JsonRecord;
      if (typeof record.content === "string" && record.content.trim()) {
        lines.push(record.content.trim());
      }
    }
  }

  return lines.join("\n").trim();
}

async function readResponseText(response: Response): Promise<string> {
  try {
    return await response.text();
  } catch {
    return "";
  }
}

export async function runZhipuLayoutOcr(input: {
  apiKey: string;
  buffer: Buffer;
  mimeType: string;
  onEvent?: (event: ZhipuHttpProgressEvent) => void;
}): Promise<string> {
  const retryConfig = getZhipuHttpRetryConfig();
  let response: Response;

  try {
    response = await fetchWithZhipuRetry({
      scope: `zhipu-ocr:${input.apiKey.slice(-8)}`,
      url: layoutParsingEndpoint,
      timeoutMs: requestTimeoutMs,
      maxAttempts: retryConfig.maxAttempts,
      baseDelayMs: retryConfig.baseDelayMs,
      maxDelayMs: retryConfig.maxDelayMs,
      minIntervalMs: retryConfig.minIntervalMs,
      onEvent: input.onEvent,
      label: "Zhipu layout_parsing OCR",
      init: {
        method: "POST",
        headers: {
          Authorization: `Bearer ${input.apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "glm-ocr",
          file: bufferToDataUrl(input.buffer, input.mimeType),
          return_crop_images: false,
          need_layout_visualization: false
        })
      }
    });
  } catch (error) {
    throw new ParsePipelineError({
      code: "ZHIPU_OCR_REQUEST_FAILED",
      message: error instanceof Error ? error.message : "Zhipu OCR request failed",
      retryable: true
    });
  }

  const rawText = await readResponseText(response);
  const payload = parseJsonSafely(rawText);

  const mdResults =
    payload && typeof payload.md_results === "string" ? payload.md_results.trim() : "";
  const layoutText = collapseLayoutDetails(payload);
  const text = mdResults || layoutText;

  if (!text) {
    throw new ParsePipelineError({
      code: "ZHIPU_OCR_EMPTY_CONTENT",
      message: "Zhipu OCR returned empty content",
      retryable: false
    });
  }

  return text;
}
