#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const operations = new Set(["env-check", "register", "detail", "disable"]);
const DEFAULT_SERVICE_MANAGEMENT_BASE_URL = "https://aicadegalaxy.com/agent";
const SERVICE_PATH = "/admin/gateway/services";
const EMPTY_BODY_MD5 = "d41d8cd98f00b204e9800998ecf8427e";

function usage(exitCode = 0) {
  const message = `
Usage:
  build-service-request.mjs env-check [--operation register|detail|disable]
  build-service-request.mjs register --spec FILE [--base-url URL] [--api-key KEY] [--secret-key SECRET]
  build-service-request.mjs detail --service-id SERVICE_ID [--base-url URL] [--api-key KEY] [--secret-key SECRET]
  build-service-request.mjs disable --service-id SERVICE_ID [--base-url URL] [--api-key KEY] [--secret-key SECRET]

Defaults:
  --base-url defaults to https://aicadegalaxy.com/agent after user confirmation.
  --api-key reads from AICADE_API_KEY when omitted.
  --secret-key reads from AICADE_API_SECRET_KEY or SECRET_KEY when omitted.

This script prints a signed curl command only. It does not call the API.
`;
  console.log(message.trim());
  process.exit(exitCode);
}

function parseArgs(argv) {
  const [operation, ...rest] = argv;
  if (!operations.has(operation)) usage(1);

  const args = { command: operation };
  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];
    if (token === "--help" || token === "-h") usage(0);
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected positional argument: ${token}`);
    }

    const key = token.slice(2);
    const value = rest[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    args[key] = value;
    index += 1;
  }

  return args;
}

function getBaseUrl(args) {
  return args["base-url"] || process.env.AICADE_SERVICE_BASE_URL || DEFAULT_SERVICE_MANAGEMENT_BASE_URL;
}

function getApiKey(args) {
  const apiKey = args["api-key"] || process.env.AICADE_API_KEY;
  if (!apiKey) {
    throw new Error("Missing AICADE_API_KEY environment variable or --api-key");
  }
  return apiKey;
}

function getSecretKey(args) {
  const secretKey = args["secret-key"] || process.env.AICADE_API_SECRET_KEY || process.env.SECRET_KEY;
  if (!secretKey) {
    throw new Error("Missing AICADE_API_SECRET_KEY environment variable or --secret-key");
  }
  return secretKey;
}

function requireArg(args, key) {
  if (!args[key]) throw new Error(`Missing required --${key}`);
  return args[key];
}

function shellQuote(value) {
  return `'${String(value).replaceAll("'", "'\\''")}'`;
}

function joinUrl(baseUrl, apiPath, query = "") {
  const url = `${baseUrl.replace(/\/+$/, "")}${apiPath}`;
  return query ? `${url}?${query}` : url;
}

function maybeBase64DecodeSecret(secretKey) {
  try {
    const decoded = Buffer.from(secretKey, "base64");
    if (decoded.length > 0 && decoded.toString("base64").replace(/=+$/, "") === secretKey.replace(/=+$/, "")) {
      return decoded;
    }
  } catch {
    // Fall back to utf8 below.
  }
  return Buffer.from(secretKey, "utf8");
}

function bodyMd5(body) {
  if (!body) return EMPTY_BODY_MD5;
  return crypto.createHash("md5").update(body).digest("hex");
}

function createSignature({ method, signaturePath, query, clientTime, nonce, md5, secretKey }) {
  const source = [method, signaturePath, query, clientTime, nonce, md5].join("\n");
  const key = maybeBase64DecodeSecret(secretKey);
  const signature = crypto.createHmac("sha256", key).update(source).digest("hex");
  return { source, signature };
}

function signedCurl({ method, baseUrl, signaturePath, query = "", body = "", apiKey, secretKey }) {
  const clientTime = String(Math.floor(Date.now() / 1000));
  const nonce = crypto.randomUUID();
  const md5 = bodyMd5(body);
  const { signature } = createSignature({
    method,
    signaturePath,
    query,
    clientTime,
    nonce,
    md5,
    secretKey,
  });

  const parts = [
    "curl",
    "-X",
    method,
    shellQuote(joinUrl(baseUrl, signaturePath, query)),
    "-H",
    shellQuote(`X-API-Key: ${apiKey}`),
    "-H",
    shellQuote(`X-Client-Time: ${clientTime}`),
    "-H",
    shellQuote(`X-Nonce: ${nonce}`),
    "-H",
    shellQuote(`X-Content-MD5: ${md5}`),
    "-H",
    shellQuote(`X-Signature: ${signature}`),
  ];

  if (body) {
    parts.push("-H", shellQuote("Content-Type: application/json"), "--data-binary", shellQuote(body));
  }

  return parts.join(" ");
}

function validateRegisterSpec(spec) {
  const required = [
    "serviceId",
    "serviceName",
    "endpointUrl",
    "authType",
    "routePath",
    "inputSchema",
    "outputSchema",
    "billing",
  ];

  const missing = required.filter((key) => spec[key] === undefined || spec[key] === null);
  if (missing.length) {
    throw new Error(`Register spec missing required field(s): ${missing.join(", ")}`);
  }

  if (!/^[a-z0-9-]{3,64}$/.test(spec.serviceId)) {
    throw new Error("serviceId must use lowercase letters, digits, hyphens, length 3-64");
  }

  if (!/^https?:\/\//.test(String(spec.endpointUrl))) {
    throw new Error("endpointUrl must start with http:// or https://");
  }

  if (!String(spec.routePath).startsWith("/")) {
    spec.routePath = `/${spec.routePath}`;
  }

  if (spec.timeoutMs !== undefined && (spec.timeoutMs < 1000 || spec.timeoutMs > 300000)) {
    throw new Error("timeoutMs must be between 1000 and 300000");
  }

  if (spec.stripPrefix !== undefined && (spec.stripPrefix < 0 || spec.stripPrefix > 10)) {
    throw new Error("stripPrefix must be between 0 and 10");
  }

  const billing = spec.billing || {};
  for (const key of ["billingType", "currency", "fallbackStrategy"]) {
    if (billing[key] === undefined || billing[key] === null) {
      throw new Error(`billing.${key} is required`);
    }
  }

  if (spec.authType !== "NONE" && !spec.outboundAuth) {
    throw new Error("outboundAuth is required when authType is not NONE");
  }
}

function buildEnvCheck(args) {
  const operation = args.operation || "detail";
  const result = {
    operation,
    AICADE_API_KEY: Boolean(process.env.AICADE_API_KEY),
    AICADE_API_SECRET_KEY: Boolean(process.env.AICADE_API_SECRET_KEY || process.env.SECRET_KEY),
    defaultBaseUrl: DEFAULT_SERVICE_MANAGEMENT_BASE_URL,
    ready: Boolean(process.env.AICADE_API_KEY) && Boolean(process.env.AICADE_API_SECRET_KEY || process.env.SECRET_KEY),
  };

  return JSON.stringify(result, null, 2);
}

function buildRegister(args) {
  const apiKey = getApiKey(args);
  const secretKey = getSecretKey(args);
  const baseUrl = getBaseUrl(args);
  const specPath = path.resolve(requireArg(args, "spec"));
  const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
  validateRegisterSpec(spec);
  const body = JSON.stringify(spec, null, 2);

  return signedCurl({
    method: "POST",
    baseUrl,
    signaturePath: SERVICE_PATH,
    body,
    apiKey,
    secretKey,
  });
}

function buildDetail(args) {
  const apiKey = getApiKey(args);
  const secretKey = getSecretKey(args);
  const baseUrl = getBaseUrl(args);
  const serviceId = encodeURIComponent(requireArg(args, "service-id"));

  return signedCurl({
    method: "GET",
    baseUrl,
    signaturePath: `${SERVICE_PATH}/${serviceId}`,
    apiKey,
    secretKey,
  });
}

function buildDisable(args) {
  const apiKey = getApiKey(args);
  const secretKey = getSecretKey(args);
  const baseUrl = getBaseUrl(args);
  const serviceId = encodeURIComponent(requireArg(args, "service-id"));

  return signedCurl({
    method: "PATCH",
    baseUrl,
    signaturePath: `${SERVICE_PATH}/${serviceId}/status`,
    query: "enabled=false",
    apiKey,
    secretKey,
  });
}

try {
  const args = parseArgs(process.argv.slice(2));
  const builders = {
    "env-check": buildEnvCheck,
    register: buildRegister,
    detail: buildDetail,
    disable: buildDisable,
  };

  console.log(builders[args.command](args));
} catch (error) {
  console.error(`Error: ${error.message}`);
  console.error("Run with --help for usage.");
  process.exit(1);
}
