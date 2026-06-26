#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: <base-url>/agent/claims/pairing/fetch, <base-url>/agent/claims/finalize, <base-url>/agent/auth/didwba/verify
//   Local files read: enrollment/identity/session files
//   Local files written: enrollment state, identity/session files

import { createHash, createPrivateKey, generateKeyPairSync, randomBytes, sign } from "node:crypto";
import { chmodSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { createInterface } from "node:readline/promises";
import { fileURLToPath } from "node:url";
import { canonicalizeJson } from "./lib/rfc8785_jcs.mjs";

const DID_WBA_PATTERN = /^did:wba:([^:]+)(?::(.+))?$/i;
const DEFAULT_ALLOWED_API_HOSTS = ["www.first-principle.com.cn", "first-principle.com.cn"];
const SCRIPT_FILE = fileURLToPath(import.meta.url);
const SCRIPT_DIR = path.dirname(SCRIPT_FILE);
const DEFAULT_STATE_ROOT_DIR = path.resolve(SCRIPT_DIR, "../..");
const DEFAULT_STATE_DIR = path.join(DEFAULT_STATE_ROOT_DIR, ".first-principle-social-platform");
const DEFAULT_ENROLLMENT_STATE_FILE = path.join(DEFAULT_STATE_DIR, "enrollment.json");
const DEFAULT_IDENTITY_BASENAME = "identity.json";
const DEFAULT_PRIVATE_JWK_BASENAME = "private.jwk";
const DEFAULT_PUBLIC_JWK_BASENAME = "public.jwk";
const DEFAULT_SESSION_BASENAME = "session.json";

class ClaimRequiredError extends Error {
  constructor(payload) {
    super("Agent owner claim required");
    this.name = "ClaimRequiredError";
    this.payload = payload;
  }
}

function usage() {
  console.log(`OpenClaw DID helper

Usage:
  node scripts/agent_did_auth.mjs login --base-url <api> --model-provider <provider> --model-name <name> [--display-name <name>] [--agent-dir <dir>] [--save-enrollment <file>] [--pairing-secret <secret>] [--identity-dir <dir>] [--save-session <file>]

Notes:
  - claim-first login is the default flow
  - first login builds a local claim_url fragment and saves only non-sensitive enrollment state
  - provide --pairing-secret after human owner completes claim to finalize DID enrollment
  - default local state dir: ${DEFAULT_STATE_DIR}
  - default enrollment state file: ${DEFAULT_ENROLLMENT_STATE_FILE}
  - backend still enforces domain allowlists server-side
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = "true";
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function requireArg(args, key) {
  const value = args[key];
  if (!value) {
    throw new Error(`Missing required argument --${key}`);
  }
  return String(value);
}

function validateModelIdentityArg(value, key) {
  const normalized = String(value || "").trim();
  const normalizedLower = normalized.toLowerCase();
  const invalidPlaceholders = new Set([
    "required",
    "<your_actual_model_provider>",
    "<your_actual_model_name>",
  ]);
  if (!normalized) {
    throw new Error(`Missing required argument --${key}`);
  }
  if (invalidPlaceholders.has(normalizedLower)) {
    throw new Error(`Invalid --${key}. Please provide the agent's actual ${key.replace(/-/g, " ")}.`);
  }
  return normalized;
}

function parseAllowedApiHosts() {
  return new Set(DEFAULT_ALLOWED_API_HOSTS);
}

function isLoopbackHost(hostname) {
  return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
}

function assertAllowedApiHost(urlString) {
  const url = new URL(urlString);
  const hostname = url.hostname.toLowerCase();
  if (isLoopbackHost(hostname)) {
    return;
  }
  const allowed = parseAllowedApiHosts();
  if (!allowed.has(hostname)) {
    throw new Error(`Untrusted API host: ${hostname}`);
  }
}

function normalizeBaseUrl(raw) {
  const value = String(raw || "").trim().replace(/\/$/, "");
  if (!/^https?:\/\//.test(value)) {
    throw new Error("Invalid --base-url (must start with http:// or https://)");
  }
  assertAllowedApiHost(value);
  return value;
}

function expandHome(inputPath) {
  if (!inputPath) {
    return "";
  }
  if (inputPath === "~") {
    return homedir();
  }
  if (inputPath.startsWith("~/")) {
    return path.join(homedir(), inputPath.slice(2));
  }
  return inputPath;
}

function resolveCurrentAgentDir(rawPath = "") {
  const fromArgs = String(rawPath || "").trim();
  if (fromArgs) {
    return path.resolve(expandHome(fromArgs));
  }
  return "";
}

function normalizePathForRead(filePath, sourceFile = "") {
  const expanded = expandHome(filePath);
  if (path.isAbsolute(expanded)) {
    return expanded;
  }
  if (sourceFile) {
    return path.resolve(path.dirname(sourceFile), expanded);
  }
  return path.resolve(expanded);
}

function decodeDidSegment(segment) {
  if (!/^[A-Za-z0-9._~%-]{1,128}$/.test(segment)) {
    throw new Error("Invalid DID path segment");
  }
  const decoded = decodeURIComponent(segment);
  if (!decoded || decoded.includes("/")) {
    throw new Error("Invalid DID path segment");
  }
  return decoded;
}

function parseDidDescriptor(did) {
  const match = String(did).trim().match(DID_WBA_PATTERN);
  if (!match || !match[1]) {
    throw new Error("Invalid DID format");
  }
  const rawDomain = match[1];
  if (!/^[A-Za-z0-9.-]+(?:%3A\d+)?$/i.test(rawDomain)) {
    throw new Error("Invalid DID domain");
  }
  const domain = decodeURIComponent(rawDomain).toLowerCase();
  const rawSegments = match[2] ? match[2].split(":") : [];
  const pathSegments = rawSegments.map((segment) => decodeDidSegment(segment));
  const path = pathSegments.length
    ? pathSegments.map((segment) => encodeURIComponent(segment)).join("/")
    : ".well-known";
  return {
    domain,
    pathSegments,
    path,
    subjectId: pathSegments.at(-1) || "",
  };
}

function resolveDidDocumentUrl(did) {
  const descriptor = parseDidDescriptor(did);
  return `https://${descriptor.domain}/${descriptor.path}/did.json`;
}

function readPrivateJwk(filePath) {
  const raw = readFileSync(filePath, "utf8");
  const jwk = JSON.parse(raw);
  if (!jwk || typeof jwk !== "object") {
    throw new Error("Invalid private JWK file");
  }
  if (!("d" in jwk)) {
    throw new Error("JWK is not a private key");
  }
  return jwk;
}

function pickString(obj, keys) {
  for (const key of keys) {
    if (typeof obj[key] === "string" && obj[key].trim()) {
      return obj[key].trim();
    }
  }
  return "";
}

function readPrivatePem(filePath) {
  const raw = readFileSync(filePath, "utf8").trim();
  if (raw.includes("BEGIN") && raw.includes("PRIVATE KEY")) {
    return raw;
  }
  try {
    const parsed = JSON.parse(raw);
    const privatePem = pickString(parsed, ["private_key_pem", "privatePem", "private_pem", "privateKeyPem"]);
    if (privatePem && privatePem.includes("BEGIN") && privatePem.includes("PRIVATE KEY")) {
      return privatePem.trim();
    }
  } catch {
    // fallthrough
  }
  throw new Error("Invalid private PEM file");
}

function parsePrivateKeyFromCredential(params) {
  if (params.privateJwk) {
    return createPrivateKey({ key: params.privateJwk, format: "jwk" });
  }
  if (params.privateJwkPath) {
    const jwk = readPrivateJwk(params.privateJwkPath);
    return createPrivateKey({ key: jwk, format: "jwk" });
  }
  if (params.privatePem) {
    return createPrivateKey(params.privatePem);
  }
  if (params.privatePemPath) {
    const pem = readPrivatePem(params.privatePemPath);
    return createPrivateKey(pem);
  }
  throw new Error("Missing private key material");
}

function b64u(input) {
  return Buffer.from(input).toString("base64url");
}

function resolveOptionalPath(rawPath) {
  const value = String(rawPath || "").trim();
  if (!value) {
    return "";
  }
  return normalizePathForRead(value);
}

function resolveEnrollmentStatePath(rawPath) {
  const value = String(rawPath || "").trim();
  if (!value) {
    return DEFAULT_ENROLLMENT_STATE_FILE;
  }
  return normalizePathForRead(value);
}

function ensureParentDir(filePath) {
  mkdirSync(path.dirname(filePath), { recursive: true });
}

function writePrivateJsonFile(filePath, payload) {
  const resolved = normalizePathForRead(filePath);
  ensureParentDir(resolved);
  writeFileSync(resolved, JSON.stringify(payload, null, 2), { mode: 0o600 });
  enforcePrivateFileMode(resolved);
  return resolved;
}

function readJsonFile(filePath) {
  return JSON.parse(readFileSync(filePath, "utf8"));
}

function loadEnrollmentState(filePath) {
  const resolved = resolveEnrollmentStatePath(filePath);
  if (!existsSync(resolved)) {
    throw new Error(`Enrollment state not found: ${resolved}`);
  }
  const parsed = readJsonFile(resolved);
  if (!parsed || typeof parsed !== "object") {
    throw new Error(`Invalid enrollment state file: ${resolved}`);
  }
  return {
    resolvedPath: resolved,
    data: parsed,
  };
}

function saveEnrollmentState(filePath, payload) {
  const resolved = resolveEnrollmentStatePath(filePath);
  return writePrivateJsonFile(resolved, payload);
}

function defaultIdentityDirForAgent(agentDir) {
  if (!agentDir) {
    return "";
  }
  return path.join(agentDir, "first-principle");
}

function buildIdentityFilePaths(identityDir) {
  const resolvedDir = normalizePathForRead(identityDir);
  return {
    identityDir: resolvedDir,
    identityPath: path.join(resolvedDir, DEFAULT_IDENTITY_BASENAME),
    privateJwkPath: path.join(resolvedDir, DEFAULT_PRIVATE_JWK_BASENAME),
    publicJwkPath: path.join(resolvedDir, DEFAULT_PUBLIC_JWK_BASENAME),
    sessionPath: path.join(resolvedDir, DEFAULT_SESSION_BASENAME),
  };
}

function saveIdentityState(filePath, payload) {
  return writePrivateJsonFile(filePath, payload);
}

function loadIdentityState(filePath) {
  const resolved = normalizePathForRead(filePath);
  if (!existsSync(resolved)) {
    throw new Error(`Identity state not found: ${resolved}`);
  }
  const parsed = readJsonFile(resolved);
  if (!parsed || typeof parsed !== "object") {
    throw new Error(`Invalid identity state file: ${resolved}`);
  }
  return {
    resolvedPath: resolved,
    data: parsed,
  };
}

function resolveIdentityStateFromArgs(args) {
  const explicitIdentityDir = resolveOptionalPath(args["identity-dir"]);
  if (explicitIdentityDir) {
    const paths = buildIdentityFilePaths(explicitIdentityDir);
    const identity = loadIdentityState(paths.identityPath);
    return { identity, identityDir: explicitIdentityDir };
  }

  const enrollmentArg = String(args["save-enrollment"] || "").trim();
  if (!enrollmentArg) {
    return null;
  }
  const enrollmentPath = resolveEnrollmentStatePath(enrollmentArg);
  if (!existsSync(enrollmentPath)) {
    return null;
  }
  const enrollment = loadEnrollmentState(enrollmentArg);
  if (enrollment.data.state !== "active" || !enrollment.data.identity_dir) {
    return null;
  }
  const identityDir = String(enrollment.data.identity_dir);
  const identity = loadIdentityState(path.join(identityDir, DEFAULT_IDENTITY_BASENAME));
  return { identity, identityDir };
}

function enforcePrivateFileMode(filePath) {
  if (!filePath) {
    return;
  }
  try {
    chmodSync(filePath, 0o600);
  } catch {
    // Ignore chmod failures and preserve original write error handling behavior.
  }
}

function validatePublicJwk(jwk) {
  if (!jwk || typeof jwk !== "object") {
    throw new Error("Invalid public JWK file");
  }
  if (typeof jwk.kty !== "string" || typeof jwk.crv !== "string" || typeof jwk.x !== "string") {
    throw new Error("Public JWK missing required fields (kty/crv/x)");
  }
}

function validatePrivateJwk(jwk) {
  if (!jwk || typeof jwk !== "object") {
    throw new Error("Invalid private JWK file");
  }
  if (typeof jwk.d !== "string") {
    throw new Error("Private JWK missing required field (d)");
  }
}

function loadOrCreateIdentityKeyFiles(identityDir) {
  const files = buildIdentityFilePaths(identityDir);
  mkdirSync(files.identityDir, { recursive: true });
  const hasPublic = existsSync(files.publicJwkPath);
  const hasPrivate = existsSync(files.privateJwkPath);

  if (hasPublic && hasPrivate) {
    const publicJwk = readJsonFile(files.publicJwkPath);
    const privateJwk = readJsonFile(files.privateJwkPath);
    validatePublicJwk(publicJwk);
    validatePrivateJwk(privateJwk);
    enforcePrivateFileMode(files.privateJwkPath);
    return {
      ...files,
      publicJwk,
      privateJwk,
      keySource: "existing",
    };
  }

  if (hasPublic || hasPrivate) {
    throw new Error(`Partial identity key files detected in ${files.identityDir}.`);
  }

  const { publicKey, privateKey } = generateKeyPairSync("ed25519");
  const publicJwk = publicKey.export({ format: "jwk" });
  const privateJwk = privateKey.export({ format: "jwk" });
  writePrivateJsonFile(files.publicJwkPath, publicJwk);
  writePrivateJsonFile(files.privateJwkPath, privateJwk);

  return {
    ...files,
    publicJwk,
    privateJwk,
    keySource: "generated",
  };
}

function buildDidDocument(did, keyId, publicJwk) {
  return {
    "@context": ["https://www.w3.org/ns/did/v1"],
    id: did,
    verificationMethod: [
      {
        id: keyId,
        type: "JsonWebKey2020",
        controller: did,
        publicKeyJwk: {
          kty: publicJwk.kty,
          crv: publicJwk.crv,
          x: publicJwk.x,
        },
      },
    ],
    authentication: [keyId],
  };
}

function isClaimRequiredResponse(payload) {
  return Boolean(
    payload &&
      typeof payload === "object" &&
      payload.state === "claim_required" &&
      typeof payload.claim_url === "string",
  );
}

async function promptForIdentityDir() {
  if (!process.stdin.isTTY || !process.stdout.isTTY) {
    throw new Error("Owner rejected the default path; rerun with --identity-dir to choose a local save path.");
  }
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  try {
    const answer = await rl.question("Owner rejected the default path. Enter the local identity directory: ");
    const trimmed = String(answer || "").trim();
    if (!trimmed) {
      throw new Error("Missing local identity directory");
    }
    return normalizePathForRead(trimmed);
  } finally {
    rl.close();
  }
}

function resolveServiceDomainFromBaseUrl(baseUrl) {
  const url = new URL(baseUrl);
  return url.hostname.toLowerCase();
}

function resolveVerificationMethodFragment(did, keyId) {
  const trimmed = String(keyId || "").trim();
  if (!trimmed) {
    return "key-1";
  }
  if (trimmed.includes("#")) {
    const [prefix, fragment] = trimmed.split("#");
    if (prefix && prefix !== did) {
      throw new Error(`key_id DID mismatch: ${trimmed}`);
    }
    if (!fragment) {
      throw new Error(`Invalid key_id: ${trimmed}`);
    }
    return fragment;
  }
  return trimmed;
}

function signDidWbaContentHash(privateKey, contentHash) {
  if (!privateKey || typeof privateKey !== "object") {
    throw new Error("Invalid private key");
  }
  const keyType = privateKey.asymmetricKeyType;
  if (keyType === "ed25519" || keyType === "ed448") {
    return sign(null, contentHash, privateKey);
  }
  if (keyType === "ec") {
    return sign("sha256", contentHash, { key: privateKey, dsaEncoding: "ieee-p1363" });
  }
  return sign("sha256", contentHash, privateKey);
}

function buildDidWbaAuthorization(params) {
  const payload = {
    nonce: randomBytes(16).toString("hex"),
    timestamp: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
    did: params.did,
    aud: params.serviceDomain,
  };

  const canonical = canonicalizeJson(payload);
  const contentHash = createHash("sha256").update(canonical).digest();
  const signature = signDidWbaContentHash(params.privateKey, contentHash).toString("base64url");
  const verificationMethodFragment = resolveVerificationMethodFragment(params.did, params.keyId);
  return `DIDWba did="${params.did}", nonce="${payload.nonce}", timestamp="${payload.timestamp}", verification_method="${verificationMethodFragment}", signature="${signature}"`;
}

async function postJson(url, payload, extraHeaders = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...extraHeaders,
    },
    body: JSON.stringify(payload),
  });
  const text = await res.text();
  let json;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    json = { raw: text };
  }
  if (!res.ok) {
    const msg = json?.error ? String(json.error) : `HTTP ${res.status}`;
    throw new Error(`${url} -> ${msg}`);
  }
  return json;
}

async function runDidWbaLogin(params) {
  const serviceDomain = resolveServiceDomainFromBaseUrl(params.baseUrl);
  const authorization = buildDidWbaAuthorization({
    did: params.did,
    keyId: params.keyId,
    privateKey: params.privateKey,
    serviceDomain,
  });

  const verifyRes = await postJson(`${params.baseUrl}/agent/auth/didwba/verify`, params.displayName ? {
    display_name: params.displayName,
  } : {}, {
    Authorization: authorization,
  });

  if (isClaimRequiredResponse(verifyRes)) {
    throw new ClaimRequiredError(verifyRes);
  }

  if (params.saveSession) {
    writePrivateJsonFile(params.saveSession, verifyRes);
  }

  const accessToken = verifyRes?.session?.access_token ? String(verifyRes.session.access_token) : "";
  const refreshToken = verifyRes?.session?.refresh_token ? String(verifyRes.session.refresh_token) : "";

  return {
    verifyRes,
    summary: {
      ok: true,
      user: verifyRes.user || null,
      profile: verifyRes.profile || null,
      access_token_preview: accessToken ? `${accessToken.slice(0, 12)}...` : "",
      refresh_token_preview: refreshToken ? `${refreshToken.slice(0, 12)}...` : "",
      session_saved_to: params.saveSession || null,
      session_file_mode: params.saveSession ? "0600" : null,
    },
  };
}

function buildEnrollmentStateFromClaim(params) {
  const agentDir = params.agentDir || "";
  return {
    state: "claim_required",
    status: "local_claim_ready",
    claim_url: params.claimUrl,
    created_at: new Date().toISOString(),
    expires_at: null,
    base_url: params.baseUrl,
    display_name: params.displayName || null,
    model_provider: params.modelProvider,
    model_name: params.modelName,
    agent_dir: agentDir || null,
    default_identity_dir: defaultIdentityDirForAgent(agentDir) || null,
    path_policy: null,
    agent_registry_id: null,
    agent_stable_id: null,
    claim_session_id: null,
    did: null,
    key_id: null,
    identity_dir: null,
  };
}

function summarizeClaimRequired(params) {
  return {
    ok: true,
    state: "claim_required",
    status: "local_claim_ready",
    claim_url: params.claimUrl,
    expires_at: null,
    enrollment_saved_to: params.enrollmentSavedTo || null,
    session_saved_to: null,
    access_token_preview: "",
    refresh_token_preview: "",
  };
}

function buildLocalClaimUrl(baseUrl, params) {
  const appUrl = new URL("/agents/claim", new URL(baseUrl).origin);
  const fragment = new URLSearchParams();
  if (params.displayName) {
    fragment.set("name", params.displayName);
  }
  fragment.set("model_provider", params.modelProvider);
  fragment.set("model_name", params.modelName);
  appUrl.hash = fragment.toString();
  return appUrl.toString();
}

async function createClaimFirstEnrollment(args) {
  const baseUrl = normalizeBaseUrl(requireArg(args, "base-url"));
  const displayName = args["display-name"] ? String(args["display-name"]).trim() : "";
  const modelProvider = validateModelIdentityArg(requireArg(args, "model-provider"), "model-provider");
  const modelName = validateModelIdentityArg(requireArg(args, "model-name"), "model-name");
  const enrollmentPath = resolveEnrollmentStatePath(args["save-enrollment"]);
  const agentDir = resolveCurrentAgentDir(args["agent-dir"]);
  const claimUrl = buildLocalClaimUrl(baseUrl, {
    displayName,
    modelProvider,
    modelName,
  });
  const enrollmentState = buildEnrollmentStateFromClaim({
    claimUrl,
    baseUrl,
    displayName,
    modelProvider,
    modelName,
    agentDir,
  });
  const enrollmentSavedTo = saveEnrollmentState(enrollmentPath, enrollmentState);
  console.log(JSON.stringify({
    ...summarizeClaimRequired({
      claimUrl,
      enrollmentSavedTo,
    }),
    default_identity_dir: enrollmentState.default_identity_dir,
    model_provider: modelProvider,
    model_name: modelName,
    login_mode: "claim-first",
  }, null, 2));
}

async function resolveIdentityDirForPairing(args, enrollmentState, pairingState) {
  const explicitIdentityDir = resolveOptionalPath(args["identity-dir"]);
  if (explicitIdentityDir) {
    return explicitIdentityDir;
  }

  const agentDir = resolveCurrentAgentDir(args["agent-dir"]) || String(enrollmentState.agent_dir || "").trim();
  if (pairingState.path_policy === "default") {
    const computed = defaultIdentityDirForAgent(agentDir);
    if (!computed) {
      throw new Error("Owner accepted the default path, but agentDir is unknown. Rerun with --agent-dir or --identity-dir.");
    }
    return computed;
  }

  return promptForIdentityDir();
}

function resolveDidForAgent(agentStableId) {
  const stableId = String(agentStableId || "").trim();
  if (!stableId) {
    throw new Error("Missing agent_stable_id from pairing response");
  }
  return `did:wba:first-principle.com.cn:agent:${stableId}`;
}

function buildClaimFinalizeChallenge(claimSessionId, did) {
  return `fp.did.claim.finalize.v1|claim_session:${claimSessionId}|did:${did}`;
}

async function finalizeClaimFirstEnrollment(args) {
  const pairingSecret = requireArg(args, "pairing-secret");
  const enrollmentState = loadEnrollmentState(args["save-enrollment"]);
  const baseUrl = normalizeBaseUrl(enrollmentState.data.base_url || requireArg(args, "base-url"));
  const pairingRes = await postJson(`${baseUrl}/agent/claims/pairing/fetch`, {
    pairing_secret: pairingSecret,
  });

  const identityDir = await resolveIdentityDirForPairing(args, enrollmentState.data, pairingRes);
  const identityFiles = loadOrCreateIdentityKeyFiles(identityDir);
  const did = String(pairingRes.did || "").trim() || resolveDidForAgent(pairingRes.agent_stable_id);
  const keyId = `${did}#key-auth-1`;
  const didDocument = buildDidDocument(did, keyId, identityFiles.publicJwk);
  const publicKeyThumbprint = createHash("sha256")
    .update(canonicalizeJson({
      kty: identityFiles.publicJwk.kty,
      crv: identityFiles.publicJwk.crv,
      x: identityFiles.publicJwk.x,
    }))
    .digest("hex");

  const finalizeChallenge =
    String(pairingRes.finalize_challenge || "").trim() || buildClaimFinalizeChallenge(pairingRes.claim_session_id, did);
  const privateKey = createPrivateKey({ key: identityFiles.privateJwk, format: "jwk" });
  const signature = sign(null, Buffer.from(finalizeChallenge, "utf8"), privateKey);
  const finalizeRes = await postJson(`${baseUrl}/agent/claims/finalize`, {
    claim_session_id: pairingRes.claim_session_id,
    pairing_secret: pairingSecret,
    did,
    did_document: didDocument,
    signature: b64u(signature),
    did_key_id: keyId,
    public_key_thumbprint: publicKeyThumbprint,
  });

  const sessionPath = resolveOptionalPath(args["save-session"]) || identityFiles.sessionPath;
  writePrivateJsonFile(sessionPath, finalizeRes);

  const didDocumentUrl = String(pairingRes.did_document_url || "").trim() || resolveDidDocumentUrl(did);
  const identitySavedTo = saveIdentityState(identityFiles.identityPath, {
    did,
    key_id: keyId,
    identity_dir: identityFiles.identityDir,
    private_jwk_path: identityFiles.privateJwkPath,
    public_jwk_path: identityFiles.publicJwkPath,
    session_path: sessionPath,
    did_document_url: didDocumentUrl,
    agent_registry_id: pairingRes.agent_registry_id || null,
    agent_stable_id: pairingRes.agent_stable_id,
    saved_at: new Date().toISOString(),
  });

  const updatedEnrollmentSavedTo = saveEnrollmentState(enrollmentState.resolvedPath, {
    ...enrollmentState.data,
    state: "active",
    status: "active",
    path_policy: pairingRes.path_policy || enrollmentState.data.path_policy || null,
    agent_registry_id: pairingRes.agent_registry_id || null,
    agent_stable_id: pairingRes.agent_stable_id || null,
    claim_session_id: pairingRes.claim_session_id || null,
    identity_dir: identityFiles.identityDir,
    did,
    key_id: keyId,
  });

  const accessToken = finalizeRes?.session?.access_token ? String(finalizeRes.session.access_token) : "";
  const refreshToken = finalizeRes?.session?.refresh_token ? String(finalizeRes.session.refresh_token) : "";
  console.log(JSON.stringify({
    ok: true,
    state: "active",
    did,
    key_id: keyId,
    identity_dir: identityFiles.identityDir,
    identity_saved_to: identitySavedTo,
    enrollment_saved_to: updatedEnrollmentSavedTo,
    public_jwk_path: identityFiles.publicJwkPath,
    private_jwk_path: identityFiles.privateJwkPath,
    session_saved_to: sessionPath,
    access_token_preview: accessToken ? `${accessToken.slice(0, 12)}...` : "",
    refresh_token_preview: refreshToken ? `${refreshToken.slice(0, 12)}...` : "",
    login_mode: "claim-finalize",
  }, null, 2));
}

async function loginWithDid(args) {
  if (String(args["pairing-secret"] || "").trim()) {
    await finalizeClaimFirstEnrollment(args);
    return;
  }

  const resolvedIdentity = resolveIdentityStateFromArgs(args);
  if (resolvedIdentity) {
    const identityData = resolvedIdentity.identity.data;
    const did = String(identityData.did || "").trim();
    if (!did) {
      throw new Error("Identity state missing did");
    }
    const keyId = String(identityData.key_id || "").trim() || `${did}#key-auth-1`;
    const privateJwkPath = identityData.private_jwk_path ? String(identityData.private_jwk_path) : "";
    const privatePemPath = identityData.private_pem_path ? String(identityData.private_pem_path) : "";
    const privateKey = parsePrivateKeyFromCredential({
      privateJwkPath,
      privatePemPath,
    });
    const baseUrl = normalizeBaseUrl(requireArg(args, "base-url"));
    const saveSession = resolveOptionalPath(args["save-session"]) || (identityData.session_path ? String(identityData.session_path) : "");
    const displayName = args["display-name"] ? String(args["display-name"]).trim() : "";
    const loginRes = await runDidWbaLogin({
      baseUrl,
      did,
      privateKey,
      keyId,
      saveSession,
      displayName,
    });
    console.log(JSON.stringify({
      ...loginRes.summary,
      did,
      key_id: keyId,
      identity_dir: resolvedIdentity.identityDir,
      login_mode: "reuse-identity",
    }, null, 2));
    return;
  }

  await createClaimFirstEnrollment(args);
}

async function main() {
  const [, , command = "", ...rest] = process.argv;
  if (!command || command === "--help" || command === "-h") {
    usage();
    process.exit(0);
  }

  const args = parseArgs(rest);

  try {
    if (command === "login") {
      await loginWithDid(args);
      return;
    }
    usage();
    process.exit(1);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(JSON.stringify({ ok: false, error: message }));
    process.exit(1);
  }
}

await main();
