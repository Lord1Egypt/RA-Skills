import { basename } from "node:path";
import { readFile } from "node:fs/promises";
import AdmZip from "adm-zip";
import { ParsePipelineError, type PipelineErrorRecord, toPipelineErrorRecord } from "./parse-pipeline-error.js";
import {
  fetchWithZhipuRetry,
  getZhipuHttpRetryConfig,
  type ZhipuHttpProgressEvent
} from "./zhipu-http.js";

const createEndpoint = "https://open.bigmodel.cn/api/paas/v4/files/parser/create";
const resultEndpoint = "https://open.bigmodel.cn/api/paas/v4/files/parser/result";
const maxPollAttempts = 30;
const pollIntervalMs = 2_000;
const requestTimeoutMs = 30_000;

type JsonRecord = Record<string, unknown>;

export type ZhipuParserMode = "lite" | "export";

export type ParserExportAsset = {
  fileName: string;
  mimeType: string;
  buffer: Buffer;
};

export type ZhipuParserResult = {
  taskId: string;
  mode: ZhipuParserMode;
  provider: "zhipu_parser_lite" | "zhipu_parser_export";
  text: string | null;
  assets: ParserExportAsset[];
  branchErrors: PipelineErrorRecord[];
};

const imageMimeByExt: Record<string, string> = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".bmp": "image/bmp"
};

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

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

function readTaskId(payload: JsonRecord | null): string | null {
  if (!payload) {
    return null;
  }

  if (typeof payload.task_id === "string" && payload.task_id.trim()) {
    return payload.task_id;
  }

  if (payload.data && typeof payload.data === "object" && !Array.isArray(payload.data)) {
    const data = payload.data as JsonRecord;
    if (typeof data.task_id === "string" && data.task_id.trim()) {
      return data.task_id;
    }
  }

  return null;
}

function getToolType(mode: ZhipuParserMode): "lite" | "prime" {
  return mode === "export" ? "prime" : "lite";
}

function getRequestErrorCode(mode: ZhipuParserMode): string {
  return mode === "export" ? "ZHIPU_PARSER_EXPORT_FAILED" : "ZHIPU_PARSER_REQUEST_FAILED";
}

function getFailedErrorCode(mode: ZhipuParserMode): string {
  return mode === "export" ? "ZHIPU_PARSER_EXPORT_FAILED" : "ZHIPU_PARSER_FAILED";
}

function getTimeoutErrorCode(mode: ZhipuParserMode): string {
  return mode === "export" ? "ZHIPU_PARSER_EXPORT_FAILED" : "ZHIPU_PARSER_TIMEOUT";
}

function getEmptyErrorCode(mode: ZhipuParserMode): string {
  return mode === "export" ? "ZHIPU_PARSER_EXPORT_EMPTY_CONTENT" : "ZHIPU_PARSER_EMPTY_CONTENT";
}

function getInvalidResponseCode(mode: ZhipuParserMode): string {
  return mode === "export" ? "ZHIPU_PARSER_EXPORT_FAILED" : "ZHIPU_PARSER_INVALID_RESPONSE";
}

async function readResponseText(response: Response): Promise<string> {
  try {
    return await response.text();
  } catch {
    return "";
  }
}

async function createTask(input: {
  filePath: string;
  fileName: string;
  fileType: string;
  mimeType: string;
  apiKey: string;
  mode: ZhipuParserMode;
  onEvent?: (event: ZhipuHttpProgressEvent) => void;
}): Promise<string> {
  const retryConfig = getZhipuHttpRetryConfig();
  const form = new FormData();
  form.set(
    "file",
    new Blob([await readFile(input.filePath)], { type: input.mimeType }),
    input.fileName
  );
  form.set("tool_type", getToolType(input.mode));
  form.set("file_type", input.fileType);

  let response: Response;
  try {
    response = await fetchWithZhipuRetry({
      scope: `zhipu-parser:${input.apiKey.slice(-8)}`,
      url: createEndpoint,
      timeoutMs: requestTimeoutMs,
      maxAttempts: retryConfig.maxAttempts,
      baseDelayMs: retryConfig.baseDelayMs,
      maxDelayMs: retryConfig.maxDelayMs,
      minIntervalMs: retryConfig.minIntervalMs,
      onEvent: input.onEvent,
      label: `Zhipu parser create (${input.mode})`,
      init: {
        method: "POST",
        headers: {
          Authorization: `Bearer ${input.apiKey}`
        },
        body: form
      }
    });
  } catch (error) {
    throw new ParsePipelineError({
      code: getRequestErrorCode(input.mode),
      message: error instanceof Error ? error.message : "Zhipu parser create request failed",
      retryable: true
    });
  }

  const rawText = await readResponseText(response);
  const payload = parseJsonSafely(rawText);

  if (!response.ok) {
    throw new ParsePipelineError({
      code: getRequestErrorCode(input.mode),
      message: readMessage(payload, `Zhipu parser create request failed with status ${response.status}`),
      retryable: response.status >= 500
    });
  }

  const taskId = readTaskId(payload);
  if (!taskId) {
    throw new ParsePipelineError({
      code: getFailedErrorCode(input.mode),
      message: readMessage(payload, "Zhipu parser create response did not include task_id"),
      retryable: false
    });
  }

  return taskId;
}

async function pollResult(input: {
  taskId: string;
  apiKey: string;
  mode: ZhipuParserMode;
  formatType: "text" | "download_link";
  allowEmpty: boolean;
  onEvent?: (event: ZhipuHttpProgressEvent) => void;
}): Promise<string | null> {
  for (let attempt = 0; attempt < maxPollAttempts; attempt += 1) {
    const retryConfig = getZhipuHttpRetryConfig();
    let response: Response;

    try {
      response = await fetchWithZhipuRetry({
        scope: `zhipu-parser:${input.apiKey.slice(-8)}`,
        url: `${resultEndpoint}/${input.taskId}/${input.formatType}`,
        timeoutMs: requestTimeoutMs,
        maxAttempts: retryConfig.maxAttempts,
        baseDelayMs: retryConfig.baseDelayMs,
        maxDelayMs: retryConfig.maxDelayMs,
        minIntervalMs: retryConfig.minIntervalMs,
        onEvent: input.onEvent,
        label: `Zhipu parser polling (${input.mode})`,
        init: {
          headers: {
            Authorization: `Bearer ${input.apiKey}`
          }
        }
      });
    } catch (error) {
      throw new ParsePipelineError({
        code: getRequestErrorCode(input.mode),
        message: error instanceof Error ? error.message : "Zhipu parser polling failed",
        retryable: true,
        taskId: input.taskId
      });
    }

    const rawText = await readResponseText(response);
    const payload = parseJsonSafely(rawText);

    if (!response.ok) {
      throw new ParsePipelineError({
        code: getRequestErrorCode(input.mode),
        message: readMessage(payload, `Zhipu parser polling failed with status ${response.status}`),
        retryable: response.status >= 500,
        taskId: input.taskId
      });
    }

    const status = payload && typeof payload.status === "string" ? payload.status : null;
    if (status === "processing") {
      await sleep(pollIntervalMs);
      continue;
    }

    if (status === "failed") {
      throw new ParsePipelineError({
        code: getFailedErrorCode(input.mode),
        message: readMessage(payload, "Zhipu parser reported failure"),
        retryable: false,
        taskId: input.taskId
      });
    }

    if (status !== "succeeded" && status !== null) {
      throw new ParsePipelineError({
        code: getInvalidResponseCode(input.mode),
        message: `Unexpected Zhipu parser status: ${status}`,
        retryable: false,
        taskId: input.taskId
      });
    }

    if (input.formatType === "download_link") {
      const url =
        payload && typeof payload.parsing_result_url === "string"
          ? payload.parsing_result_url.trim()
          : "";
      if (!url) {
        if (input.allowEmpty) {
          return null;
        }
        throw new ParsePipelineError({
          code: getInvalidResponseCode(input.mode),
          message: "Zhipu parser did not return parsing_result_url",
          retryable: false,
          taskId: input.taskId
        });
      }
      return url;
    }

    const content =
      payload && typeof payload.content === "string" ? payload.content.trim() : rawText.trim();
    if (!content) {
      if (input.allowEmpty) {
        return null;
      }
      throw new ParsePipelineError({
        code: getEmptyErrorCode(input.mode),
        message: "Zhipu parser returned empty text content",
        retryable: false,
        taskId: input.taskId
      });
    }
    return content;
  }

  throw new ParsePipelineError({
    code: getTimeoutErrorCode(input.mode),
    message: `Timed out while waiting for Zhipu parser task ${input.taskId}`,
    retryable: true,
    taskId: input.taskId
  });
}

async function downloadExportBundle(input: {
  apiKey: string;
  downloadUrl: string;
  onEvent?: (event: ZhipuHttpProgressEvent) => void;
}): Promise<{ assets: ParserExportAsset[]; bundleText: string | null }> {
  const retryConfig = getZhipuHttpRetryConfig();
  let response: Response;
  try {
    response = await fetchWithZhipuRetry({
      scope: `zhipu-parser:${input.apiKey.slice(-8)}`,
      url: input.downloadUrl,
      timeoutMs: requestTimeoutMs,
      maxAttempts: retryConfig.maxAttempts,
      baseDelayMs: retryConfig.baseDelayMs,
      maxDelayMs: retryConfig.maxDelayMs,
      minIntervalMs: retryConfig.minIntervalMs,
      onEvent: input.onEvent,
      label: "Zhipu parser export download",
      init: {
        headers: {
          Authorization: `Bearer ${input.apiKey}`
        }
      }
    });
  } catch (error) {
    throw new ParsePipelineError({
      code: "ZHIPU_PARSER_EXPORT_FAILED",
      message: error instanceof Error ? error.message : "Failed to download parser export bundle",
      retryable: true
    });
  }

  const buffer = Buffer.from(await response.arrayBuffer());
  const zip = new AdmZip(buffer);
  const entries = zip.getEntries().filter((entry) => !entry.isDirectory);
  const assets: ParserExportAsset[] = [];
  let bundleText: string | null = null;

  for (const entry of entries) {
    const entryName = entry.entryName;
    const lowerName = entryName.toLowerCase();
    const extMatch = lowerName.match(/(\.[a-z0-9]+)$/u);
    const ext = extMatch?.[1] ?? "";

    if (!bundleText && [".md", ".txt", ".html"].includes(ext)) {
      const text = entry.getData().toString("utf8").trim();
      if (text) {
        bundleText = text;
      }
      continue;
    }

    if (ext in imageMimeByExt) {
      assets.push({
        fileName: basename(entryName),
        mimeType: imageMimeByExt[ext] ?? "application/octet-stream",
        buffer: entry.getData()
      });
    }
  }

  return {
    assets,
    bundleText
  };
}

export async function parseWithZhipuParser(input: {
  filePath: string;
  mimeType: string;
  fileType: string;
  apiKey: string;
  mode: ZhipuParserMode;
  onEvent?: (event: ZhipuHttpProgressEvent) => void;
}): Promise<ZhipuParserResult> {
  const taskId = await createTask({
    filePath: input.filePath,
    fileName: basename(input.filePath),
    fileType: input.fileType,
    mimeType: input.mimeType,
    apiKey: input.apiKey,
    mode: input.mode,
    onEvent: input.onEvent
  });

  if (input.mode === "lite") {
    const text = await pollResult({
      taskId,
      apiKey: input.apiKey,
      mode: input.mode,
      formatType: "text",
      allowEmpty: false,
      onEvent: input.onEvent
    });

    return {
      taskId,
      mode: "lite",
      provider: "zhipu_parser_lite",
      text,
      assets: [],
      branchErrors: []
    };
  }

  const branchErrors: PipelineErrorRecord[] = [];
  let text: string | null = null;
  let bundleText: string | null = null;
  let assets: ParserExportAsset[] = [];

  try {
    text = await pollResult({
      taskId,
      apiKey: input.apiKey,
      mode: input.mode,
      formatType: "text",
      allowEmpty: true,
      onEvent: input.onEvent
    });
  } catch (error) {
    branchErrors.push(toPipelineErrorRecord(error));
  }

  try {
    const downloadUrl = await pollResult({
      taskId,
      apiKey: input.apiKey,
      mode: input.mode,
      formatType: "download_link",
      allowEmpty: true,
      onEvent: input.onEvent
    });

    if (downloadUrl) {
      const bundle = await downloadExportBundle({
        apiKey: input.apiKey,
        downloadUrl,
        onEvent: input.onEvent
      });
      assets = bundle.assets;
      bundleText = bundle.bundleText;
    }
  } catch (error) {
    branchErrors.push(toPipelineErrorRecord(error));
  }

  const resolvedText = text?.trim() ? text.trim() : bundleText?.trim() ? bundleText.trim() : null;
  if (!resolvedText && assets.length === 0) {
    if (branchErrors.length > 0) {
      const [firstError] = branchErrors;
      throw new ParsePipelineError({
        code: firstError.code,
        message: firstError.message,
        retryable: firstError.retryable,
        taskId
      });
    }

    throw new ParsePipelineError({
      code: "ZHIPU_PARSER_EXPORT_EMPTY_CONTENT",
      message: "Zhipu parser export returned no text and no assets",
      retryable: false,
      taskId
    });
  }

  return {
    taskId,
    mode: "export",
    provider: "zhipu_parser_export",
    text: resolvedText,
    assets,
    branchErrors
  };
}
