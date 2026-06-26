#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import http from "node:http";
import https from "node:https";

async function main() {
  try {
    const args = parseCliArgs(process.argv.slice(2));
    const artifactPath = requireArg(args, "--artifact");
    const toolName = requireArg(args, "--tool");
    const argsFile = requireArg(args, "--args-file");
    const debug = isDebugEnabled(process.env.AICADE_GALAXY_DEBUG);

    const artifact = JSON.parse(await readFile(artifactPath, "utf8"));
    const payload = JSON.parse(await readFile(argsFile, "utf8"));

    if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
      throw new Error("--args-file must contain a JSON object.");
    }

    logDebug(debug, {
      event: "invoke.input",
      artifactPath,
      tool: toolName,
      argsFile,
      payload,
    });

    const result = await invokeArtifactTool(artifact, toolName, payload);
    logDebug(debug, {
      event: "invoke.output",
      artifactPath,
      tool: toolName,
      result,
    });
    console.log(JSON.stringify(result, null, 2));
    process.exitCode = result.ok ? 0 : 1;
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  }
}

async function invokeArtifactTool(artifact, toolName, payload) {
  const tool = findTool(artifact, toolName);
  const split = splitPayload(payload);

  console.log("Invoking tool:", toolName, payload);
  validateArgs(tool, split.args);
  validateResponsePaths(tool, split.responsePaths);

  const url = new URL(joinBaseUrl(artifact.baseUrl, tool.metadata.path));
  const headers = {
    Accept: "application/json",
  };
  applyAuthHeader(tool, headers);

  let body;
  if (tool.metadata.method === "GET") {
    applyQueryParams(url, split.args);
  } else {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(split.args);
  }

  const response = await requestJson(url.toString(), {
    method: tool.metadata.method,
    headers,
    body,
  });

  const raw = parseMaybeJson(response.body);
  if (response.statusCode >= 400) {
    return {
      ok: false,
      status: response.statusCode,
      tool: tool.name,
      serviceId: tool.metadata.serviceId,
      error: {
        message: buildErrorMessage(response.statusCode, raw),
        raw,
      },
    };
  }

  return {
    ok: true,
    status: response.statusCode,
    tool: tool.name,
    serviceId: tool.metadata.serviceId,
    data: selectResponseData(raw, split.responsePaths),
    raw,
  };
}

function parseCliArgs(argv) {
  const result = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || value === undefined) {
      throw new Error(
        "Usage: node scripts/invoke_artifact.mjs --artifact <path> --tool <name> --args-file <path>",
      );
    }
    result.set(key, value);
  }
  return result;
}

function requireArg(args, key) {
  const value = args.get(key);
  if (!value) {
    throw new Error(`Missing required argument ${key}.`);
  }
  return value;
}

function findTool(artifact, toolName) {
  if (
    !artifact ||
    typeof artifact !== "object" ||
    !Array.isArray(artifact.tools)
  ) {
    throw new Error("Invalid artifact format.");
  }

  const tool = artifact.tools.find((item) => item?.name === toolName);
  if (!tool) {
    throw new Error(`Tool "${toolName}" was not found in artifact.`);
  }
  return tool;
}

function splitPayload(payload) {
  const { responsePaths, ...args } = payload;

  if (responsePaths === undefined) {
    return { args, responsePaths: [] };
  }

  if (
    !Array.isArray(responsePaths) ||
    responsePaths.some((item) => typeof item !== "string" || item.length === 0)
  ) {
    throw new Error('"responsePaths" must be an array of non-empty strings.');
  }

  return { args, responsePaths };
}

function validateArgs(tool, args) {
  for (const key of tool.inputSchema.required || []) {
    if (!(key in args) || args[key] === undefined || args[key] === null) {
      throw new Error(
        `Missing required parameter "${key}" for tool "${tool.name}".`,
      );
    }
  }

  if (tool.inputSchema.additionalProperties === false) {
    for (const key of Object.keys(args)) {
      if (!(key in tool.inputSchema.properties)) {
        throw new Error(`Unknown parameter "${key}" for tool "${tool.name}".`);
      }
    }
  }

  for (const [key, value] of Object.entries(args)) {
    const property = tool.inputSchema.properties[key];
    if (!property) {
      continue;
    }
    validateValueType(tool.name, key, value, property);
  }
}

function validateValueType(toolName, key, value, property) {
  if (value === undefined || value === null || !property?.type) {
    return;
  }

  const valid =
    (property.type === "string" && typeof value === "string") ||
    (property.type === "number" &&
      typeof value === "number" &&
      Number.isFinite(value)) ||
    (property.type === "integer" &&
      typeof value === "number" &&
      Number.isInteger(value)) ||
    (property.type === "boolean" && typeof value === "boolean") ||
    (property.type === "object" &&
      typeof value === "object" &&
      !Array.isArray(value)) ||
    (property.type === "array" && Array.isArray(value));

  if (!valid) {
    throw new Error(
      `Invalid parameter "${key}" for tool "${toolName}": expected ${property.type}.`,
    );
  }
}

function validateResponsePaths(tool, responsePaths) {
  if (
    responsePaths.length === 0 ||
    !Array.isArray(tool.metadata.responseFields)
  ) {
    return;
  }

  const available = new Set(tool.metadata.responseFields);
  for (const responsePath of responsePaths) {
    if (!available.has(responsePath)) {
      throw new Error(
        `Unknown response path "${responsePath}" for tool "${tool.name}".`,
      );
    }
  }
}

function applyAuthHeader(tool, headers) {
  const envName = tool.metadata?.authentication?.envName;
  const headerName = tool.metadata?.authentication?.headerName;
  const value = envName ? process.env[envName] : undefined;

  if (tool.metadata?.authentication?.required && !value) {
    throw new Error(
      `Missing required environment variable: ${envName} for tool "${tool.name}".`,
    );
  }

  if (value && headerName) {
    headers[headerName] = value;
  }
}

function applyQueryParams(url, args) {
  for (const [key, value] of Object.entries(args)) {
    if (value === undefined || value === null) {
      continue;
    }
    url.searchParams.set(key, stringifyQueryValue(value));
  }
}

function stringifyQueryValue(value) {
  if (
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean" ||
    typeof value === "bigint"
  ) {
    return String(value);
  }

  return JSON.stringify(value);
}

function requestJson(urlString, options) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlString);
    const transport = url.protocol === "https:" ? https : http;
    const request = transport.request(
      url,
      {
        method: options.method,
        headers: options.headers,
      },
      (response) => {
        const chunks = [];

        response.on("data", (chunk) => {
          chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
        });

        response.on("end", () => {
          resolve({
            statusCode: response.statusCode || 0,
            body: Buffer.concat(chunks).toString("utf8"),
          });
        });
      },
    );

    request.on("error", (error) => reject(error));
    if (options.body) {
      request.write(options.body);
    }
    request.end();
  });
}

function parseMaybeJson(text) {
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function buildErrorMessage(status, raw) {
  if (raw && typeof raw === "object") {
    if (typeof raw.message === "string" && raw.message.length > 0) {
      return raw.message;
    }
    if (
      raw.error &&
      typeof raw.error === "object" &&
      typeof raw.error.message === "string"
    ) {
      return raw.error.message;
    }
  }

  if (typeof raw === "string" && raw.length > 0) {
    return raw;
  }

  return `Request failed with HTTP ${status}.`;
}

function selectResponseData(data, responsePaths) {
  if (responsePaths.length === 0) {
    return data;
  }

  if (responsePaths.length === 1) {
    return getValueByPath(data, responsePaths[0]);
  }

  let result = {};
  for (const path of responsePaths) {
    result = mergeSelectedValues(
      result,
      buildSelectedStructure(data, tokenizePath(path)),
    );
  }
  return result;
}

function getValueByPath(data, path) {
  return getValueByTokens(data, tokenizePath(path));
}

function buildSelectedStructure(data, tokens) {
  if (tokens.length === 0) {
    return data;
  }

  const [current, ...rest] = tokens;
  if (current === "[]") {
    if (!Array.isArray(data)) {
      return undefined;
    }
    return data.map((item) => buildSelectedStructure(item, rest));
  }

  if (data === null || typeof data !== "object") {
    return undefined;
  }

  const value = data[current];
  const selectedChild = buildSelectedStructure(value, rest);
  if (selectedChild === undefined) {
    return undefined;
  }
  return { [current]: selectedChild };
}

function getValueByTokens(data, tokens) {
  if (tokens.length === 0) {
    return data;
  }

  const [current, ...rest] = tokens;
  if (current === "[]") {
    if (!Array.isArray(data)) {
      return undefined;
    }
    return data.map((item) => getValueByTokens(item, rest));
  }

  if (data === null || typeof data !== "object") {
    return undefined;
  }

  return getValueByTokens(data[current], rest);
}

function tokenizePath(path) {
  return path.replace(/\[\]/g, ".[]").split(".").filter(Boolean);
}

function mergeSelectedValues(left, right) {
  if (right === undefined) {
    return left;
  }
  if (left === undefined) {
    return right;
  }
  if (Array.isArray(left) && Array.isArray(right)) {
    const length = Math.max(left.length, right.length);
    return Array.from({ length }, (_, index) =>
      mergeSelectedValues(left[index], right[index]),
    );
  }
  if (isPlainObject(left) && isPlainObject(right)) {
    const result = { ...left };
    for (const [key, value] of Object.entries(right)) {
      result[key] =
        key in result ? mergeSelectedValues(result[key], value) : value;
    }
    return result;
  }
  return right;
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function joinBaseUrl(baseUrl, path) {
  const normalizedBaseUrl = String(baseUrl || "").replace(/\/+$/, "");
  const normalizedPath = String(path || "").startsWith("/")
    ? String(path)
    : `/${String(path || "")}`;
  return `${normalizedBaseUrl}${normalizedPath}`;
}

function isDebugEnabled(value) {
  return Boolean(value) && value.toLowerCase() === "true";
}

function logDebug(enabled, payload) {
  if (!enabled) {
    return;
  }

  console.log(`[AICADE_GALAXY_DEBUG] ${JSON.stringify(payload, null, 2)}`);
}

await main();
