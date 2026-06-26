#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import http from "node:http";
import https from "node:https";

const DEFAULT_OUTPUT_DIR = "output";
const OUTPUT_FILE_NAME = "aicade-galaxy-skill.json";
const DEFAULT_SERVICES_PATH = "/admin/gateway/services";

async function main() {
  try {
    const config = await loadConfig();
    const services = await discoverServices(config);
    const artifact = buildArtifact(config, services);

    const outputPath = config.outputPath;
    await mkdir(dirname(outputPath), { recursive: true });
    await writeFile(
      outputPath,
      `${JSON.stringify(artifact, null, 2)}\n`,
      "utf8",
    );

    console.log(`artifact written: ${outputPath}`);
    console.log(
      JSON.stringify(
        {
          baseUrl: config.baseUrl,
          toolCount: artifact.toolCount,
          toolNames: artifact.tools.map((tool) => tool.name),
        },
        null,
        2,
      ),
    );
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error("Failed to export AICADE Galaxy artifact.");
    console.error(message);
    if (isAuthLikeError(message)) {
      console.error(
        "Check whether AICADE_GALAXY_API_KEY is configured correctly in .env.",
      );
    }
    process.exitCode = 1;
  }
}

async function loadConfig() {
  const env = await loadEnv(".env");

  const baseUrl = env.AICADE_GALAXY_BASE_URL || env.CLAWHUB_BASE_URL;
  const apiKey = env.AICADE_GALAXY_API_KEY;
  const outputDir = env.AICADE_GALAXY_OUTPUT_PATH || DEFAULT_OUTPUT_DIR;
  const debug = isDebugEnabled(env.AICADE_GALAXY_DEBUG);

  if (!baseUrl) {
    throw new Error(
      'Missing required environment variable: AICADE_GALAXY_BASE_URL. Run "node scripts/setup_env.mjs" or "python3 scripts/setup_env.py", or update .env.',
    );
  }

  if (!apiKey) {
    throw new Error(
      'Missing required environment variable: AICADE_GALAXY_API_KEY. Run "node scripts/setup_env.mjs" or "python3 scripts/setup_env.py", or update .env.',
    );
  }

  return {
    baseUrl: baseUrl.replace(/\/+$/, ""),
    servicesPath: DEFAULT_SERVICES_PATH,
    outputPath: joinPath(outputDir, OUTPUT_FILE_NAME),
    apiKey,
    debug,
  };
}

async function loadEnv(path) {
  try {
    const content = await readFile(path, "utf8");
    return parseEnv(content);
  } catch {
    return {};
  }
}

function parseEnv(content) {
  const result = {};

  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }

    const equalsIndex = line.indexOf("=");
    if (equalsIndex <= 0) {
      continue;
    }

    const key = line.slice(0, equalsIndex).trim();
    const value = line.slice(equalsIndex + 1).trim();
    result[key] = stripQuotes(value);
  }

  return result;
}

function stripQuotes(value) {
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }

  return value;
}

async function discoverServices(config) {
  const url = joinUrl(config.baseUrl, config.servicesPath);
  const headers = {
    Accept: "application/json",
    "X-API-Key": config.apiKey,
  };
  logDebug(config, {
    event: "request",
    method: "GET",
    url,
    headers,
  });
  const response = await requestJson(url, headers);
  logDebug(config, {
    event: "response",
    method: "GET",
    url,
    statusCode: response.statusCode,
    contentType: response.contentType,
    bodyPreview: previewText(response.body),
  });

  let payload;
  try {
    payload = JSON.parse(response.body);
  } catch (error) {
    throw new Error(
      `Failed to parse services response as JSON. Content-Type=${response.contentType}. Body preview=${previewText(response.body)}`,
    );
  }

  if (!payload || typeof payload !== "object" || !Array.isArray(payload.data)) {
    throw new Error("Invalid services response shape");
  }

  return payload.data;
}

function requestJson(urlString, headers) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlString);
    const transport = url.protocol === "https:" ? https : http;
    const request = transport.request(
      url,
      {
        method: "GET",
        headers,
      },
      (response) => {
        const chunks = [];

        response.on("data", (chunk) => {
          chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
        });

        response.on("end", () => {
          const body = Buffer.concat(chunks).toString("utf8");
          const contentType = String(response.headers["content-type"] || "");
          const statusCode = response.statusCode || 0;

          if (statusCode >= 400) {
            reject(
              new Error(
                `Failed to discover services: HTTP ${statusCode}. Content-Type=${contentType}. Body preview=${previewText(body)}`,
              ),
            );
            return;
          }

          resolve({ body, contentType, statusCode });
        });
      },
    );

    request.on("error", (error) => {
      reject(new Error(`Failed to discover services: ${error.message}`));
    });

    request.end();
  });
}

function buildArtifact(config, services) {
  const tools = [];
  for (const service of services) {
    const tool = buildTool(service);
    if (tool) {
      tools.push(tool);
    }
  }

  return {
    version: "1.0",
    generatedAt: new Date().toISOString(),
    baseUrl: config.baseUrl,
    toolCount: tools.length,
    tools,
  };
}

function buildTool(service) {
  if (!service?.enabled) {
    return null;
  }

  const inputSchema = service.inputSchema || {};
  const method = String(inputSchema.method || "").toUpperCase();
  if (method !== "GET" && method !== "POST") {
    return null;
  }

  const properties = isRecord(inputSchema.properties)
    ? inputSchema.properties
    : {};
  const required = Array.isArray(inputSchema.required)
    ? inputSchema.required
    : [];

  const outputSchema = service.outputSchema || {};
  const responseProperties = isRecord(outputSchema.properties)
    ? outputSchema.properties
    : {};
  const responseFields = listResponsePaths(responseProperties);

  return {
    name: createToolName(
      String(service.serviceId || service.name || "service"),
    ),
    description: buildToolDescription(
      service,
      method,
      properties,
      required,
      responseFields,
    ),
    inputSchema: {
      type: "object",
      properties: {
        ...properties,
        responsePaths: buildResponsePathsProperty(responseFields),
      },
      required: required.filter((key) => hasOwn(properties, key)),
      additionalProperties: false,
    },
    metadata: {
      serviceId: service.serviceId,
      title: service.title || service.serviceName || service.name,
      method,
      path: service.routePath,
      authentication: {
        type: "apiKeyHeader",
        required: true,
        headerName: "X-API-Key",
        envName: "AICADE_GALAXY_API_KEY",
      },
      responseFields,
      invocationProtocol: {
        reservedFields: ["responsePaths"],
        responsePathsField: "responsePaths",
      },
    },
  };
}

function createToolName(serviceId) {
  return Array.from(serviceId, (ch) =>
    /[A-Za-z0-9_]/.test(ch) ? ch : "_",
  ).join("");
}

function buildToolDescription(
  service,
  method,
  properties,
  required,
  responseFields,
) {
  const parts = [
    service.title || service.serviceName || service.name || "AICADE service",
    service.description || "",
    method === "GET"
      ? "Use query parameters and expect a JSON response."
      : "Use a JSON request body and expect a JSON response.",
  ];

  const names = Object.keys(properties);
  if (names.length > 0) {
    parts.push(`Parameters: ${names.join(", ")}.`);

    const requiredNames = required.filter((name) => hasOwn(properties, name));
    const optionalNames = names.filter((name) => !requiredNames.includes(name));

    if (requiredNames.length > 0) {
      parts.push(`Required parameters: ${requiredNames.join(", ")}.`);
    }

    if (optionalNames.length > 0) {
      parts.push(`Optional parameters: ${optionalNames.join(", ")}.`);
    }
  }

  if (responseFields.length > 0) {
    parts.push(
      `Optional reserved field: responsePaths. Selectable response fields: ${responseFields.join(", ")}. Use responsePaths to request only the fields you need.`,
    );
  } else {
    parts.push(
      "Optional reserved field: responsePaths. Response selection is supported, but this service does not declare output fields.",
    );
  }

  return parts.filter(Boolean).join(" ");
}

function buildResponsePathsProperty(responseFields) {
  let description =
    "Optional. Select one or more response field paths to return.";
  if (responseFields.length > 0) {
    description = `${description} Available values: ${responseFields.join(", ")}.`;
  }

  return {
    type: "array",
    description,
    items: {
      type: "string",
    },
  };
}

function listResponsePaths(properties) {
  const paths = [];
  for (const [key, prop] of Object.entries(properties)) {
    walkSchemaProperty(key, prop, paths);
  }
  return paths;
}

function walkSchemaProperty(currentPath, prop, paths) {
  paths.push(currentPath);

  if (prop?.type === "object" && isRecord(prop.properties)) {
    for (const [key, child] of Object.entries(prop.properties)) {
      walkSchemaProperty(`${currentPath}.${key}`, child, paths);
    }
  }

  if (prop?.type === "array" && isRecord(prop.items)) {
    paths.push(`${currentPath}[]`);
    if (prop.items.type === "object" && isRecord(prop.items.properties)) {
      for (const [key, child] of Object.entries(prop.items.properties)) {
        walkSchemaProperty(`${currentPath}[].${key}`, child, paths);
      }
    }
  }
}

function joinUrl(baseUrl, path) {
  const normalizedPath = path.startsWith("/") ? path.slice(1) : path;
  return `${baseUrl}/${normalizedPath}`;
}

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function hasOwn(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function isAuthLikeError(message) {
  return (
    message.includes("401") ||
    message.includes("403") ||
    message.includes("X-API-Key") ||
    message.includes("AICADE_GALAXY_API_KEY")
  );
}

function isDebugEnabled(value) {
  if (!value) {
    return false;
  }

  return value.toLowerCase() === "true";
}

function logDebug(config, payload) {
  if (!config.debug) {
    return;
  }

  console.log(`[AICADE_GALAXY_DEBUG] ${JSON.stringify(payload, null, 2)}`);
}

function previewText(text, limit = 240) {
  const compact = text.split(/\s+/).filter(Boolean).join(" ");
  if (compact.length <= limit) {
    return compact;
  }
  return `${compact.slice(0, limit)}...`;
}

function dirname(path) {
  const normalized = path.replace(/\\/g, "/");
  const index = normalized.lastIndexOf("/");
  return index === -1 ? "." : normalized.slice(0, index) || ".";
}

function joinPath(dir, file) {
  const normalizedDir = dir.replace(/[\\/]+$/, "");
  if (!normalizedDir) {
    return file;
  }
  return `${normalizedDir}/${file}`;
}

await main();
