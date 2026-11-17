#!/usr/bin/env node
// SPDX-License-Identifier: MIT-0

import { readFile } from "node:fs/promises";
import { randomBytes, randomUUID, webcrypto } from "node:crypto";
import { pathToFileURL } from "node:url";

import {
  isUUID,
  validateDirectConnectionManifest,
  validateDirectInboxResponse,
  validateDirectSurfacesResponse,
  validateOpaqueReference,
  validatePrivateEvent,
} from "./protocol-validation.mjs";

const LIMITS = {
  notification: 64 * 1024,
  inbox: 1024 * 1024,
  surfaces: 1024 * 1024,
};

export async function runDirectConformance(options) {
  const manifest = JSON.parse(await readFile(options.manifestPath, "utf8"));
  validateDirectConnectionManifest(manifest);
  if (!isUUID(options.deviceKeyId)) throw new Error("--device-key-id must be a UUID");
  const privateKey = await importPrivateKey(options.signingPrivateKey);
  const checks = [];
  let securityCandidate;

  if (manifest.capabilities.includes("notification_detail")) {
    if (!options.reference) {
      throw new Error("--reference is required for notification_detail conformance");
    }
    validateOpaqueReference(options.reference);
    const url = endpointURL(
      manifest,
      "notification",
      new URLSearchParams({ ref: options.reference }),
    );
    const value = await signedJSON(url, manifest.connectionId, options.deviceKeyId, privateKey, LIMITS.notification);
    validatePrivateEvent(value.json, options.reference);
    securityCandidate = value.request;
    checks.push({ endpoint: "notification", ok: true, bytes: value.bytes });
  }

  if (manifest.capabilities.includes("inbox")) {
    const value = await signedJSON(
      endpointURL(manifest, "inbox", new URLSearchParams({ limit: "50" })),
      manifest.connectionId,
      options.deviceKeyId,
      privateKey,
      LIMITS.inbox,
    );
    validateDirectInboxResponse(value.json);
    securityCandidate ??= value.request;
    checks.push({ endpoint: "inbox", ok: true, bytes: value.bytes, events: value.json.events.length });
  }

  if (manifest.capabilities.includes("surfaces")) {
    const value = await signedJSON(
      endpointURL(manifest, "surfaces"),
      manifest.connectionId,
      options.deviceKeyId,
      privateKey,
      LIMITS.surfaces,
    );
    validateDirectSurfacesResponse(value.json, manifest.project.id);
    securityCandidate ??= value.request;
    checks.push({ endpoint: "surfaces", ok: true, bytes: value.bytes, surfaces: value.json.surfaces.length });
  }

  if (!securityCandidate) throw new Error("Manifest must enable at least one supported capability");
  await verifySecurityFailures(
    securityCandidate,
    manifest.connectionId,
    options.deviceKeyId,
    privateKey,
  );
  checks.push({
    endpoint: "security",
    ok: true,
    cases: ["replayed_nonce", "stale_timestamp", "unknown_key", "tampered_query"],
  });

  return { protocolVersion: 2, connectionId: manifest.connectionId, checks };
}

async function signedJSON(url, connectionId, keyId, privateKey, maximumBytes) {
  const request = await signedRequest(url, connectionId, keyId, privateKey);
  const response = await fetch(request.url, {
    headers: request.headers,
    signal: AbortSignal.timeout(8_000),
  });
  const bytes = new Uint8Array(await response.arrayBuffer());
  if (bytes.byteLength > maximumBytes) {
    throw new Error(`${url.pathname} response exceeds ${maximumBytes} bytes`);
  }
  if (!response.ok) throw new Error(`${url.pathname} returned HTTP ${response.status}`);
  let json;
  try {
    json = JSON.parse(new TextDecoder().decode(bytes));
  } catch {
    throw new Error(`${url.pathname} did not return valid JSON`);
  }
  if (!isRecord(json)) throw new Error(`${url.pathname} must return a JSON object`);
  return { json, bytes: bytes.byteLength, request };
}

async function signedRequest(
  url,
  connectionId,
  keyId,
  privateKey,
  {
    timestamp = String(Math.floor(Date.now() / 1_000)),
    nonce = randomBytes(24).toString("base64url"),
  } = {},
) {
  const canonical = [
    "GET",
    `${url.pathname}${url.search}`,
    timestamp,
    nonce,
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  ].join("\n");
  const signature = Buffer.from(await webcrypto.subtle.sign(
    { name: "ECDSA", hash: "SHA-256" },
    privateKey,
    new TextEncoder().encode(canonical),
  )).toString("base64");
  return {
    url,
    headers: {
      accept: "application/json",
      "x-bellwire-connection": connectionId,
      "x-bellwire-key-id": keyId,
      "x-bellwire-timestamp": timestamp,
      "x-bellwire-nonce": nonce,
      "x-bellwire-signature": signature,
    },
  };
}

async function verifySecurityFailures(candidate, connectionId, keyId, privateKey) {
  const fingerprints = [];
  fingerprints.push(await expectUnauthorized(candidate.url, candidate.headers, "replayed nonce"));

  const stale = await signedRequest(candidate.url, connectionId, keyId, privateKey, {
    timestamp: String(Math.floor(Date.now() / 1_000) - 6 * 60),
  });
  fingerprints.push(await expectUnauthorized(stale.url, stale.headers, "stale timestamp"));

  const unknownKey = await signedRequest(
    candidate.url,
    connectionId,
    randomUUID(),
    privateKey,
  );
  fingerprints.push(await expectUnauthorized(unknownKey.url, unknownKey.headers, "unknown key"));

  const signedOriginal = await signedRequest(candidate.url, connectionId, keyId, privateKey);
  const tampered = new URL(signedOriginal.url);
  tampered.searchParams.set("bellwire_conformance_tampered", "1");
  fingerprints.push(await expectUnauthorized(tampered, signedOriginal.headers, "tampered query"));
  if (new Set(fingerprints).size !== 1) {
    throw new Error("Authentication failures must return the same HTTP 401 response");
  }
}

async function expectUnauthorized(url, headers, label) {
  const response = await fetch(url, {
    headers,
    signal: AbortSignal.timeout(8_000),
  });
  const body = await response.text();
  if (response.status !== 401) {
    throw new Error(`${label} must return the uniform HTTP 401 response, got ${response.status}`);
  }
  if (Buffer.byteLength(body) > 8 * 1024) throw new Error(`${label} returned an oversized authentication error`);
  return `${response.headers.get("content-type") ?? ""}\n${body}`;
}

function endpointURL(manifest, name, search) {
  const path = manifest.endpoints[name];
  if (typeof path !== "string" || !path.startsWith("/") || path.startsWith("//")) {
    throw new Error(`endpoints.${name} must be an absolute path`);
  }
  const url = new URL(path, manifest.baseUrl);
  if (url.origin !== new URL(manifest.baseUrl).origin) {
    throw new Error(`endpoints.${name} must remain on baseUrl`);
  }
  if (search) {
    for (const [key, value] of search) url.searchParams.set(key, value);
  }
  return url;
}

async function importPrivateKey(encoded) {
  if (!encoded) throw new Error("BELLWIRE_SIGNING_PRIVATE_KEY is required");
  return webcrypto.subtle.importKey(
    "pkcs8",
    Buffer.from(encoded, "base64"),
    { name: "ECDSA", namedCurve: "P-256" },
    false,
    ["sign"],
  );
}

function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function parseArguments(argv) {
  const result = {};
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || !value) throw new Error(`Invalid argument: ${key ?? ""}`);
    result[key.slice(2)] = value;
  }
  return result;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const args = parseArguments(process.argv.slice(2));
    const result = await runDirectConformance({
      manifestPath: args.manifest,
      deviceKeyId: args["device-key-id"],
      reference: args.reference,
      signingPrivateKey: process.env.BELLWIRE_SIGNING_PRIVATE_KEY,
    });
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) {
    process.stderr.write(`Bellwire conformance: ${error instanceof Error ? error.message : "unknown error"}\n`);
    process.exitCode = 1;
  }
}
