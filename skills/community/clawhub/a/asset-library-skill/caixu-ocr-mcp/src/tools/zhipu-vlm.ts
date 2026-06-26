import { ParsePipelineError } from "./parse-pipeline-error.js";
import {
  fetchWithZhipuRetry,
  getZhipuHttpRetryConfig,
  type ZhipuHttpProgressEvent
} from "./zhipu-http.js";

const chatCompletionsEndpoint = "https://open.bigmodel.cn/api/paas/v4/chat/completions";
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

function extractMessageContent(payload: JsonRecord | null): string {
  if (!payload || !Array.isArray(payload.choices)) {
    return "";
  }

  const choice = payload.choices[0];
  if (!choice || typeof choice !== "object" || Array.isArray(choice)) {
    return "";
  }

  const choiceRecord = choice as JsonRecord;
  if (!choiceRecord.message || typeof choiceRecord.message !== "object" || Array.isArray(choiceRecord.message)) {
    return "";
  }

  const message = choiceRecord.message as JsonRecord;
  if (typeof message.content === "string") {
    return message.content.trim();
  }

  if (Array.isArray(message.content)) {
    const parts = message.content
      .flatMap((item) => {
        if (!item || typeof item !== "object" || Array.isArray(item)) {
          return [];
        }
        const record = item as JsonRecord;
        if (record.type === "text" && typeof record.text === "string") {
          return [record.text.trim()];
        }
        return [];
      })
      .filter(Boolean);
    return parts.join("\n").trim();
  }

  return "";
}

async function readResponseText(response: Response): Promise<string> {
  try {
    return await response.text();
  } catch {
    return "";
  }
}

export async function runZhipuVlmOcr(input: {
  apiKey: string;
  model: string;
  buffer: Buffer;
  mimeType: string;
  label?: string;
  onEvent?: (event: ZhipuHttpProgressEvent) => void;
}): Promise<string> {
  const retryConfig = getZhipuHttpRetryConfig();
  let response: Response;

  try {
    response = await fetchWithZhipuRetry({
      scope: `zhipu-vlm:${input.model}:${input.apiKey.slice(-8)}`,
      url: chatCompletionsEndpoint,
      timeoutMs: requestTimeoutMs,
      maxAttempts: retryConfig.maxAttempts,
      baseDelayMs: retryConfig.baseDelayMs,
      maxDelayMs: retryConfig.maxDelayMs,
      minIntervalMs: retryConfig.minIntervalMs,
      onEvent: input.onEvent,
      label: `Zhipu VLM OCR${input.label ? ` (${input.label})` : ""}`,
      init: {
        method: "POST",
        headers: {
          Authorization: `Bearer ${input.apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: input.model,
          temperature: 0,
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "text",
                  text:
                    "You are an OCR extractor. Read all visible text in reading order. Preserve line breaks when useful. Return only extracted text. If there is no readable text, return an empty string."
                },
                {
                  type: "image_url",
                  image_url: {
                    url: bufferToDataUrl(input.buffer, input.mimeType)
                  }
                }
              ]
            }
          ]
        })
      }
    });
  } catch (error) {
    throw new ParsePipelineError({
      code: "VLM_REQUEST_FAILED",
      message: error instanceof Error ? error.message : "VLM request failed",
      retryable: true
    });
  }

  const rawText = await readResponseText(response);
  const payload = parseJsonSafely(rawText);

  const content = extractMessageContent(payload);
  if (!content) {
    throw new ParsePipelineError({
      code: "VLM_EMPTY_CONTENT",
      message: `VLM returned empty content${input.label ? ` for ${input.label}` : ""}`,
      retryable: false
    });
  }

  return content;
}
