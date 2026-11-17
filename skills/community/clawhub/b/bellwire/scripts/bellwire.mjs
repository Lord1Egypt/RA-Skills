#!/usr/bin/env node
// SPDX-License-Identifier: MIT-0

import { open, readFile, unlink } from "node:fs/promises";
import { createCipheriv, createECDH, hkdfSync, randomBytes } from "node:crypto";
import { resolve } from "node:path";

import {
  isUUID,
  validateDirectConnectionManifest,
  validateEventSpec,
  validateOpaqueReference,
  validateSurfaceInput,
  validateTestEvent,
} from "./protocol-validation.mjs";

const DEFAULT_API_URL = "https://api.bellwire.app";

const { command, options } = parseArguments(process.argv.slice(2));

if (!command || options.help) {
  printHelp();
  process.exit(options.help ? 0 : 1);
}

try {
  const result = await run(command, options);
  printResult(result, options.json === true);
} catch (error) {
  const message = error instanceof Error ? error.message : "Unknown Bellwire error";
  process.stderr.write(`Bellwire: ${message}\n`);
  process.exit(1);
}

async function run(selectedCommand, args) {
  switch (selectedCommand) {
    case "bind": {
      const code = required(args, "code");
      if (!/^\d{6}$/u.test(code)) throw new Error("--code must contain exactly six digits");
      return withSecretOutput(args, () =>
        apiRequest("/v1/device-bindings/confirm", {
          method: "POST",
          body: { code, name: args.name ?? "Codex" },
          authenticated: false,
        }));
    }
    case "list-projects":
      return apiRequest("/v1/projects");
    case "list-direct-recoveries":
      return apiRequest("/v1/direct-connection-recoveries");
    case "create-project":
      if (args["logo-url"]) validateLogoUrl(args["logo-url"]);
      return apiRequest("/v1/projects", {
        method: "POST",
        body: {
          name: required(args, "name"),
          ...(args.icon ? { icon: args.icon } : {}),
          ...(args["logo-url"] ? { logoUrl: args["logo-url"] } : {}),
          ...(args.category ? { category: args.category } : {}),
        },
      });
    case "request-mode-change": {
      const toMode = required(args, "to");
      if (!["private", "hosted"].includes(toMode)) {
        throw new Error("--to must be private or hosted");
      }
      return apiRequest(
        `/v1/projects/${encodeURIComponent(required(args, "project"))}/delivery-mode-requests`,
        { method: "POST", body: { toMode } },
      );
    }
    case "update-project": {
      const projectId = required(args, "project");
      if (args["logo-url"] && args["clear-logo"]) {
        throw new Error("Use either --logo-url or --clear-logo, not both");
      }
      if (args["logo-url"]) validateLogoUrl(args["logo-url"]);
      const body = {
        ...(args.name ? { name: args.name } : {}),
        ...(args.icon ? { icon: args.icon } : {}),
        ...(args.category ? { category: args.category } : {}),
        ...(args.status ? { status: args.status } : {}),
        ...(args["logo-url"] ? { logoUrl: args["logo-url"] } : {}),
        ...(args["clear-logo"] ? { logoUrl: null } : {}),
      };
      if (Object.keys(body).length === 0) throw new Error("Provide at least one project field to update");
      return apiRequest(`/v1/projects/${encodeURIComponent(projectId)}`, { method: "PATCH", body });
    }
    case "set-project-order": {
      const projectId = required(args, "project");
      return apiRequest(`/v1/projects/${encodeURIComponent(projectId)}/order`, {
        method: "PATCH",
        body: { displayOrder: displayOrder(args.order) },
      });
    }
    case "delete-project":
      return apiRequest(`/v1/projects/${encodeURIComponent(required(args, "project"))}`, {
        method: "DELETE",
      });
    case "validate-spec": {
      const spec = await readJsonFile(required(args, "file"));
      validateEventSpec(spec);
      return { valid: true, eventType: spec.eventType };
    }
    case "create-schema": {
      const projectId = required(args, "project");
      const spec = await readJsonFile(required(args, "file"));
      validateEventSpec(spec);
      return apiRequest(`/v1/projects/${encodeURIComponent(projectId)}/event-schemas`, {
        method: "POST",
        body: spec,
      });
    }
    case "create-token":
      return withSecretOutput(args, () =>
        apiRequest(`/v1/projects/${encodeURIComponent(required(args, "project"))}/ingest-tokens`, {
          method: "POST",
          body: { name: args.name ?? "production" },
        }));
    case "revoke-token":
      return apiRequest(
        `/v1/projects/${encodeURIComponent(required(args, "project"))}/ingest-tokens/${encodeURIComponent(required(args, "token"))}`,
        { method: "DELETE" },
      );
    case "create-wake-token":
      return withSecretOutput(args, () =>
        apiRequest(`/v1/projects/${encodeURIComponent(required(args, "project"))}/wake-tokens`, {
          method: "POST",
          body: {
            name: args.name ?? "production",
            ...(args["expires-at"] ? { expiresAt: args["expires-at"] } : {}),
          },
        }));
    case "revoke-wake-token":
      return apiRequest(
        `/v1/projects/${encodeURIComponent(required(args, "project"))}/wake-tokens/${encodeURIComponent(required(args, "token"))}`,
        { method: "DELETE" },
      );
    case "generate-reference":
      return { reference: randomBytes(16).toString("base64url") };
    case "send-wake": {
      const projectId = required(args, "project");
      const reference = required(args, "reference");
      validateOpaqueReference(reference);
      const priority = args.priority ?? "normal";
      if (!["normal", "high"].includes(priority)) {
        throw new Error("--priority must be normal or high");
      }
      return apiRequest(`/v1/projects/${encodeURIComponent(projectId)}/private-wakes`, {
        method: "POST",
        body: { reference, priority },
        token: process.env.BELLWIRE_WAKE_TOKEN?.trim(),
        tokenName: "BELLWIRE_WAKE_TOKEN",
        headers: { "idempotency-key": required(args, "idempotency-key") },
      });
    }
    case "validate-surface": {
      const surface = await readJsonFile(required(args, "file"));
      validateSurfaceInput(surface);
      return { valid: true, type: surface.type };
    }
    case "upsert-surface": {
      const projectId = required(args, "project");
      const surfaceKey = required(args, "key");
      if (surfaceKey.length > 80 || !/^[a-z0-9]+(?:[._-][a-z0-9]+)*$/u.test(surfaceKey)) {
        throw new Error("--key must use lowercase letters, digits, dots, dashes, or underscores");
      }
      const surface = await readJsonFile(required(args, "file"));
      validateSurfaceInput(surface);
      return apiRequest(
        `/v1/projects/${encodeURIComponent(projectId)}/surfaces/${encodeURIComponent(surfaceKey)}`,
        { method: "PUT", body: surface },
      );
    }
    case "list-surfaces": {
      const projectId = args.project;
      return apiRequest(projectId
        ? `/v1/projects/${encodeURIComponent(projectId)}/surfaces`
        : "/v1/surfaces");
    }
    case "set-surface-order":
      return apiRequest(
        `/v1/projects/${encodeURIComponent(required(args, "project"))}/surfaces/${encodeURIComponent(required(args, "key"))}/order`,
        { method: "PATCH", body: { displayOrder: displayOrder(args.order) } },
      );
    case "delete-surface":
      return apiRequest(
        `/v1/projects/${encodeURIComponent(required(args, "project"))}/surfaces/${encodeURIComponent(required(args, "key"))}`,
        { method: "DELETE" },
      );
    case "send-test": {
      const event = await readJsonFile(required(args, "file"));
      validateTestEvent(event);
      return apiRequest(`/v1/projects/${encodeURIComponent(required(args, "project"))}/events/test`, {
        method: "POST",
        body: event,
      });
    }
    case "event":
      return apiRequest(`/v1/events/${encodeURIComponent(required(args, "event"))}`);
    case "health":
      return apiRequest(`/v1/projects/${encodeURIComponent(required(args, "project"))}/delivery-health`);
    case "encrypt-direct-connection":
    case "publish-direct-connection": {
      const manifest = await readJsonFile(required(args, "file"));
      validateDirectConnectionManifest(manifest);
      const deviceKeyId = required(args, "device-key-id").toLowerCase();
      if (!isUUID(deviceKeyId)) throw new Error("--device-key-id must be a UUID");
      const encrypted = encryptDirectConnection(
        manifest,
        deviceKeyId,
        required(args, "agreement-public-key"),
      );
      if (selectedCommand === "encrypt-direct-connection") {
        return {
          deviceKeyId,
          projectId: manifest.project.id,
          manifestVersion: 2,
          ...encrypted,
        };
      }
      return apiRequest("/v1/direct-connections", {
        method: "POST",
        body: {
          deviceKeyId,
          projectId: manifest.project.id,
          manifestVersion: 2,
          ...encrypted,
        },
      });
    }
    default:
      throw new Error(`Unknown command: ${selectedCommand}`);
  }
}

async function apiRequest(path, init = {}) {
  const baseUrl = (process.env.BELLWIRE_API_URL || DEFAULT_API_URL).replace(/\/$/u, "");
  const headers = { accept: "application/json", ...(init.headers ?? {}) };
  if (init.authenticated !== false) {
    const token = init.token ?? process.env.BELLWIRE_AGENT_TOKEN?.trim();
    if (!token) {
      throw new Error(`${init.tokenName ?? "BELLWIRE_AGENT_TOKEN"} is required for this command`);
    }
    headers.authorization = `Bearer ${token}`;
  }
  if (init.body !== undefined) headers["content-type"] = "application/json";
  const response = await fetch(`${baseUrl}${path}`, {
    method: init.method ?? "GET",
    headers,
    signal: AbortSignal.timeout(15_000),
    ...(init.body === undefined ? {} : { body: JSON.stringify(init.body) }),
  });
  const text = await response.text();
  const data = text ? safeJson(text) : {};
  if (!response.ok) {
    const code = data?.error?.code ? `${data.error.code}: ` : "";
    const message = data?.error?.message ?? `HTTP ${response.status}`;
    if (data?.error?.code === "MONTHLY_SIGNAL_LIMIT_REACHED") {
      const reset = data.error.resetAt ? ` Reset at ${data.error.resetAt}.` : "";
      throw new Error(`${code}${message}.${reset} Do not retry until reset or upgrade the account.`);
    }
    throw new Error(`${code}${message}`);
  }
  return data;
}

function parseArguments(argv) {
  const parsed = {};
  let selectedCommand;
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!selectedCommand && !item.startsWith("--")) {
      selectedCommand = item;
      continue;
    }
    if (!item.startsWith("--")) throw new Error(`Unexpected argument: ${item}`);
    const key = item.slice(2);
    if (key === "json" || key === "help" || key === "clear-logo") {
      parsed[key] = true;
      continue;
    }
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) throw new Error(`Missing value for --${key}`);
    parsed[key] = value;
    index += 1;
  }
  return { command: selectedCommand, options: parsed };
}

async function readJsonFile(path) {
  const content = await readFile(path, "utf8");
  return safeJson(content, `Invalid JSON in ${path}`);
}

function safeJson(value, fallback = "Server returned invalid JSON") {
  try {
    return JSON.parse(value);
  } catch {
    throw new Error(fallback);
  }
}

async function withSecretOutput(args, operation) {
  const outputPath = resolve(required(args, "secret-output"));
  let handle;
  try {
    handle = await open(outputPath, "wx", 0o600);
  } catch (error) {
    if (error && typeof error === "object" && error.code === "EEXIST") {
      throw new Error(`--secret-output must be a new file: ${outputPath}`);
    }
    throw new Error(`Cannot create --secret-output file ${outputPath}: ${error instanceof Error ? error.message : "unknown error"}`);
  }

  try {
    const result = await operation();
    if (!isRecord(result) || !nonEmpty(result.token)) {
      throw new Error("Bellwire did not return the expected one-time token");
    }
    await handle.writeFile(`${result.token}\n`, { encoding: "utf8" });
    await handle.sync();
    await handle.close();
    const { token, ...publicResult } = result;
    void token;
    return { ...publicResult, secretStoredAt: outputPath };
  } catch (error) {
    await handle.close().catch(() => undefined);
    await unlink(outputPath).catch(() => undefined);
    throw error;
  }
}

function encryptDirectConnection(manifest, deviceKeyId, agreementPublicKey) {
  let targetPublicKey;
  try {
    targetPublicKey = Buffer.from(agreementPublicKey, "base64");
  } catch {
    throw new Error("--agreement-public-key must be base64");
  }
  if (targetPublicKey.length !== 65 || targetPublicKey[0] !== 4) {
    throw new Error("--agreement-public-key must be an uncompressed P-256 public key");
  }
  const ephemeral = createECDH("prime256v1");
  const ephemeralPublicKey = ephemeral.generateKeys();
  let sharedSecret;
  try {
    sharedSecret = ephemeral.computeSecret(targetPublicKey);
  } catch {
    throw new Error("--agreement-public-key is not a valid P-256 public key");
  }
  const key = Buffer.from(hkdfSync(
    "sha256",
    sharedSecret,
    Buffer.from(deviceKeyId, "utf8"),
    Buffer.from("bellwire-direct-connection-v2", "utf8"),
    32,
  ));
  const nonce = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", key, nonce);
  const plaintext = Buffer.from(JSON.stringify(manifest), "utf8");
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const sealedBox = Buffer.concat([nonce, ciphertext, cipher.getAuthTag()]);
  return {
    algorithm: "p256-hkdf-sha256-aes-gcm",
    ephemeralPublicKey: ephemeralPublicKey.toString("base64"),
    sealedBox: sealedBox.toString("base64"),
  };
}

function required(args, key) {
  const value = args[key];
  if (!nonEmpty(value)) throw new Error(`--${key} is required`);
  return value;
}

function nonEmpty(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function validateLogoUrl(value) {
  try {
    const url = new URL(value);
    if (url.protocol !== "https:" || url.username || url.password || !url.hostname || value.length > 2048) {
      throw new Error("invalid");
    }
  } catch {
    throw new Error("--logo-url must be a public HTTPS URL up to 2048 characters");
  }
}

function displayOrder(value) {
  if (!/^\d+$/u.test(value ?? "")) {
    throw new Error("--order must be an integer between 0 and 1000000");
  }
  const order = Number(value);
  if (!Number.isSafeInteger(order) || order > 1_000_000) {
    throw new Error("--order must be an integer between 0 and 1000000");
  }
  return order;
}

function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function printResult(value, json) {
  if (json) {
    process.stdout.write(`${JSON.stringify(value)}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function printHelp() {
  process.stdout.write(`Bellwire CLI

Usage:
  bellwire.mjs <command> [options] [--json]

Commands:
  bind --code <6 digits> [--name <agent>] --secret-output <new-file>
  list-projects
  list-direct-recoveries
  create-project --name <name> [--logo-url <https-url>] [--icon <sf-symbol>] [--category <name>]
  request-mode-change --project <id> --to private|hosted
  update-project --project <id> [--logo-url <https-url> | --clear-logo] [--name <name>] [--icon <sf-symbol>] [--category <name>] [--status active|paused]
  set-project-order --project <id> --order <integer>
  delete-project --project <id>
  validate-spec --file <event-spec.json>
  create-schema --project <id> --file <event-spec.json>
  create-token --project <id> [--name <name>] --secret-output <new-file>
  revoke-token --project <id> --token <token-id>
  create-wake-token --project <id> [--name <name>] [--expires-at <iso-date>] --secret-output <new-file>
  revoke-wake-token --project <id> --token <token-id>
  generate-reference
  send-wake --project <id> --reference <opaque-ref> --idempotency-key <key> [--priority normal|high]
  validate-surface --file <surface.json>
  upsert-surface --project <id> --key <stable-key> --file <surface.json>
  list-surfaces [--project <id>]
  set-surface-order --project <id> --key <stable-key> --order <integer>
  delete-surface --project <id> --key <stable-key>
  encrypt-direct-connection --device-key-id <uuid> --agreement-public-key <base64> --file <manifest.json>
  publish-direct-connection --device-key-id <uuid> --agreement-public-key <base64> --file <manifest.json>
  send-test --project <id> --file <test-event.json>
  event --event <id>
  health --project <id>

Environment:
  BELLWIRE_AGENT_TOKEN  Management token (except bind and send-wake)
  BELLWIRE_WAKE_TOKEN   Private project wake-only runtime token
  BELLWIRE_API_URL      Override the hosted API URL

Secret handling:
  Token-returning commands require --secret-output. The CLI creates that file
  exclusively with mode 0600, writes only the token there, and never prints the
  token to stdout or stderr. Move it into the approved secret store promptly.
`);
}
