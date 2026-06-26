#!/usr/bin/env node
import { createRequire } from "node:module";
import { z } from "zod";

const require = createRequire(import.meta.url);
const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js") as any;
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js") as any;

const DEFAULT_HUB_BASE_URL = "https://itinai.com";
const DEFAULT_AGENT_CARD_URL = "https://itinai.com/.well-known/agent-card.json";
const DEFAULT_SUBMIT_PATH = "/wp-json/itinai/v1/submit";
const MAX_JSON_BYTES = 1024 * 1024;

type JsonValue = string | number | boolean | null | JsonObject | JsonValue[];
type JsonObject = { [key: string]: JsonValue };

type AgentSkill = {
  id?: unknown;
  name?: unknown;
  tags?: unknown;
  [key: string]: unknown;
};

type SubmitPayload = {
  agent_card_url?: string;
  agent_id?: string;
  name?: string;
  description?: string;
  version?: string;
  a2a_config?: {
    agent_card_url?: string;
    protocol_version?: string;
  };
  skills?: AgentSkill[] | string[];
  contact?: {
    email?: string;
    url?: string;
  };
  health_check?: {
    url?: string;
  };
  dynamic_data?: Record<string, unknown>;
  openclaw?: Record<string, unknown>;
  [key: string]: unknown;
};

const config = {
  hubBaseUrl: normalizeBaseUrl(process.env.ITINAI_HUB_BASE_URL || DEFAULT_HUB_BASE_URL),
  agentCardUrl: process.env.ITINAI_AGENT_CARD_URL || DEFAULT_AGENT_CARD_URL,
  submitEndpoint: process.env.ITINAI_SUBMIT_ENDPOINT || "",
  timeoutMs: parsePositiveInt(process.env.ITINAI_HTTP_TIMEOUT_MS, 20000)
};

const server = new McpServer({
  name: "itinai-a2a-catalog-mcp",
  version: "0.1.3"
});

server.registerTool(
  "get_hub_agent_card",
  {
    title: "Get ITINAI hub Agent Card",
    description: "Fetch the canonical ITINAI A2A/MCP Agent Card. This performs an external HTTPS GET to ITINAI or the supplied URL; do not include secrets in the URL.",
    inputSchema: {
      agent_card_url: z.string().url().optional().describe("Override Agent Card URL. Defaults to https://itinai.com/.well-known/agent-card.json")
    }
  },
  async ({ agent_card_url }: { agent_card_url?: string }) => {
    const url = agent_card_url || config.agentCardUrl;
    const card = await fetchJson(url, "GET");
    return jsonToolResult(card);
  }
);


server.registerTool(
  "request_agent_service",
  {
    title: "Request service from A2A agent",
    description: "Send a reviewed JSON service request directly to a selected remote A2A agent runtime endpoint. This performs an external HTTPS POST; never include secrets, payment data, or unrelated context.",
    inputSchema: {
      agent_card_url: z.string().url().optional().describe("HTTPS Agent Card URL for the selected remote agent."),
      endpoint_url: z.string().url().optional().describe("Direct HTTPS runtime endpoint. Prefer agent_card_url unless the user explicitly supplied this endpoint."),
      service_request: z.string().min(1).describe("Plain-language service request from the user, such as 'Tell me if you are selling TARDIS'."),
      payload: z.record(z.unknown()).optional().describe("Optional exact JSON payload to send. If omitted, a generic A2A tasks/send payload is built from service_request."),
      dry_run: z.boolean().optional().default(false).describe("When true, return endpoint and payload only; do not POST."),
      confirm_external_request: z.boolean().optional().default(false).describe("Must be true for a real request. Set only after the user reviewed the target endpoint and exact outbound payload.")
    }
  },
  async ({ agent_card_url, endpoint_url, service_request, payload, dry_run, confirm_external_request }: { agent_card_url?: string; endpoint_url?: string; service_request: string; payload?: Record<string, unknown>; dry_run?: boolean; confirm_external_request?: boolean }) => {
    const endpoint = endpoint_url
      ? requireHttpsUrl(endpoint_url, "endpoint_url")
      : await getRuntimeEndpointFromAgentCard(agent_card_url);

    const outboundPayload = payload || buildServiceRequestPayload(service_request);
    assertPayloadHasNoObviousSecrets(outboundPayload);

    if (dry_run || confirm_external_request !== true) {
      return jsonToolResult({
        sent: false,
        dry_run: Boolean(dry_run),
        requires_confirmation: confirm_external_request !== true,
        warning: "No service request was sent. Review the target endpoint and exact outbound payload before setting confirm_external_request=true.",
        destination_endpoint: endpoint,
        payload: outboundPayload
      });
    }

    const response = await fetchJson(endpoint, "POST", outboundPayload);
    return jsonToolResult({ sent: true, destination_endpoint: endpoint, response });
  }
);

server.registerTool(
  "normalize_manifest",
  {
    title: "Normalize A2A catalog manifest",
    description: "Normalize an LLM-written A2A manifest locally before submission. This tool does not perform network I/O.",
    inputSchema: {
      manifest: z.record(z.unknown()).describe("Loose manifest object written by a human or LLM.")
    }
  },
  async ({ manifest }: { manifest: Record<string, unknown> }) => {
    const normalized = normalizeManifest(manifest as SubmitPayload);
    return jsonToolResult(normalized);
  }
);

server.registerTool(
  "submit_agent",
  {
    title: "Submit A2A agent to ITINAI catalog",
    description: "Submit an Agent Card URL or normalized manifest JSON to the ITINAI submit proxy after explicit user review. This performs an external HTTPS POST and may create a GitHub pull request; the submitter does not need GitHub credentials.",
    inputSchema: {
      agent_card_url: z.string().url().optional().describe("HTTPS URL of the agent card to fetch and submit."),
      manifest: z.record(z.unknown()).optional().describe("Manifest fields. Used when agent_card_url alone is insufficient or when submitting a full manifest."),
      dry_run: z.boolean().optional().default(false).describe("When true, only return the normalized payload; do not POST to ITINAI."),
      confirm_external_submission: z.boolean().optional().default(false).describe("Must be true for a real submission. Set only after the user reviewed the destination endpoint and manifest fields.")
    }
  },
  async ({ agent_card_url, manifest, dry_run, confirm_external_submission }: { agent_card_url?: string; manifest?: Record<string, unknown>; dry_run?: boolean; confirm_external_submission?: boolean }) => {
    const payload = normalizeManifest({ ...(manifest as SubmitPayload | undefined), ...(agent_card_url ? { agent_card_url } : {}) });

    if (dry_run) {
      const endpoint = await getSubmitEndpoint();
      return jsonToolResult({
        dry_run: true,
        warning: "No data was submitted. Review this destination endpoint and payload before setting confirm_external_submission=true.",
        destination_endpoint: endpoint,
        payload
      });
    }

    if (confirm_external_submission !== true) {
      const endpoint = await getSubmitEndpoint();
      return jsonToolResult({
        submitted: false,
        requires_confirmation: true,
        warning: "This action will transmit the manifest and/or Agent Card URL to an external ITINAI endpoint and may create a GitHub pull request. Re-run with confirm_external_submission=true only after the user explicitly approves the endpoint and fields.",
        destination_endpoint: endpoint,
        payload
      });
    }

    const endpoint = await getSubmitEndpoint();
    const response = await fetchJson(endpoint, "POST", payload);
    return jsonToolResult(response);
  }
);

server.registerTool(
  "search_agents",
  {
    title: "Search ITINAI agents",
    description: "Search public ITINAI catalog agents. This performs an external HTTPS GET to ITINAI; do not include secrets, private prompts, or confidential data in the query.",
    inputSchema: {
      query: z.string().min(1).describe("Search query, for example 'retinol supplier', 'calendar', or 'wordpress'."),
      limit: z.number().int().min(1).max(50).optional().default(10)
    }
  },
  async ({ query, limit }: { query: string; limit: number }) => {
    const url = new URL("/wp-json/itinai/v1/ai-search", config.hubBaseUrl);
    url.searchParams.set("query", query);
    url.searchParams.set("limit", String(limit));
    const response = await fetchJson(url.toString(), "GET");
    return jsonToolResult(response);
  }
);

server.registerTool(
  "list_agents",
  {
    title: "List ITINAI agents",
    description: "List public ITINAI catalog agents. This performs an external HTTPS GET to ITINAI.",
    inputSchema: {
      limit: z.number().int().min(1).max(100).optional().default(20),
      offset: z.number().int().min(0).optional().default(0)
    }
  },
  async ({ limit, offset }: { limit: number; offset: number }) => {
    const url = new URL("/wp-json/itinai/v1/agents", config.hubBaseUrl);
    url.searchParams.set("limit", String(limit));
    url.searchParams.set("offset", String(offset));
    const response = await fetchJson(url.toString(), "GET");
    return jsonToolResult(response);
  }
);

server.registerTool(
  "get_agent",
  {
    title: "Get ITINAI agent by ID",
    description: "Fetch one public ITINAI catalog agent by normalized agent_id. This performs an external HTTPS GET to ITINAI.",
    inputSchema: {
      agent_id: z.string().min(1).describe("Agent ID, for example 'itinai-agent-submit-proxy'.")
    }
  },
  async ({ agent_id }: { agent_id: string }) => {
    const normalizedId = normalizeId(agent_id);
    if (!normalizedId) {
      throw new Error("agent_id cannot be normalized to kebab-case.");
    }
    const url = new URL(`/wp-json/itinai/v1/agent/${encodeURIComponent(normalizedId)}`, config.hubBaseUrl);
    const response = await fetchJson(url.toString(), "GET");
    return jsonToolResult(response);
  }
);

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});

async function getRuntimeEndpointFromAgentCard(agentCardUrl?: string): Promise<string> {
  if (!agentCardUrl) {
    throw new Error("agent_card_url or endpoint_url is required for service requests.");
  }
  const card = await fetchJson(agentCardUrl, "GET");
  const endpoint = extractRuntimeEndpoint(card);
  if (!endpoint) {
    throw new Error("Agent Card does not expose a usable HTTPS runtime endpoint in url, endpoints.a2a, endpoints.tasks, or endpoints.message.");
  }
  return endpoint;
}

function extractRuntimeEndpoint(card: unknown): string {
  if (!isObject(card)) {
    return "";
  }

  const candidates: unknown[] = [card.url];
  if (isObject(card.endpoints)) {
    candidates.push(card.endpoints.a2a, card.endpoints.tasks, card.endpoints.message, card.endpoints.rpc, card.endpoints.jsonrpc);
  }

  for (const candidate of candidates) {
    const endpoint = trimString(candidate);
    if (endpoint && endpoint.startsWith("https://")) {
      return requireHttpsUrl(endpoint, "Agent Card runtime endpoint");
    }
  }
  return "";
}

function buildServiceRequestPayload(serviceRequest: string): Record<string, unknown> {
  return {
    jsonrpc: "2.0",
    id: `request-${Date.now()}`,
    method: "tasks/send",
    params: {
      message: serviceRequest,
      metadata: {
        source: "itinai-a2a-agent-discovery"
      }
    }
  };
}

function assertPayloadHasNoObviousSecrets(payload: unknown): void {
  const text = stringifyCompact(payload);
  const secretPattern = /(api[_-]?key|authorization|bearer\s+[a-z0-9._-]+|token|password|secret|private[_-]?key|ssh-rsa|BEGIN\s+(RSA|OPENSSH|EC|PRIVATE)\s+KEY)/i;
  if (secretPattern.test(text)) {
    throw new Error("Outbound service request appears to contain secrets or credentials. Remove them before sending.");
  }
}

async function getSubmitEndpoint(): Promise<string> {
  if (config.submitEndpoint) {
    return requireHttpsUrl(config.submitEndpoint, "ITINAI_SUBMIT_ENDPOINT");
  }

  try {
    const card = await fetchJson(config.agentCardUrl, "GET");
    if (isObject(card) && isObject(card.endpoints) && typeof card.endpoints.submit === "string") {
      return requireHttpsUrl(card.endpoints.submit, "Agent Card endpoints.submit");
    }
  } catch {
    // Fall back to the documented ITINAI submit proxy path below.
  }

  return new URL(DEFAULT_SUBMIT_PATH, config.hubBaseUrl).toString();
}

function requireHttpsUrl(value: string, label: string): string {
  const trimmed = trimString(value);
  if (!trimmed.startsWith("https://")) {
    throw new Error(`${label} must be an HTTPS URL.`);
  }
  return trimmed;
}

async function fetchJson(url: string, method: "GET" | "POST", body?: unknown): Promise<unknown> {
  const safeUrl = requireHttpsUrl(url, "request URL");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), config.timeoutMs);

  try {
    const response = await fetch(safeUrl, {
      method,
      headers: {
        "Accept": "application/json",
        ...(method === "POST" ? { "Content-Type": "application/json" } : {})
      },
      body: method === "POST" ? JSON.stringify(body || {}) : undefined,
      redirect: "manual",
      signal: controller.signal
    });

    const redirectLocation = response.headers.get("location") || "";
    if (response.status >= 300 && response.status < 400) {
      if (redirectLocation && !redirectLocation.startsWith("https://")) {
        throw new Error(`Refused non-HTTPS redirect from ${safeUrl} to ${redirectLocation}.`);
      }
      throw new Error(`Refused redirect from ${safeUrl}${redirectLocation ? ` to ${redirectLocation}` : ""}. Fetch the final HTTPS URL explicitly.`);
    }

    const contentLength = response.headers.get("content-length");
    if (contentLength && Number.parseInt(contentLength, 10) > MAX_JSON_BYTES) {
      throw new Error(`Response from ${safeUrl} exceeds ${MAX_JSON_BYTES} bytes.`);
    }

    const text = await response.text();
    if (text.length > MAX_JSON_BYTES) {
      throw new Error(`Response from ${safeUrl} exceeds ${MAX_JSON_BYTES} bytes.`);
    }

    let data: unknown = null;
    if (text.trim()) {
      try {
        data = JSON.parse(text);
      } catch {
        throw new Error(`Expected JSON from ${safeUrl}.`);
      }
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status} from ${safeUrl}: ${stringifyCompact(data)}`);
    }

    return data;
  } finally {
    clearTimeout(timeout);
  }
}

function normalizeManifest(input: SubmitPayload): SubmitPayload {
  const out: SubmitPayload = {};

  const directAgentCardUrl = trimString(input.agent_card_url);
  const nestedAgentCardUrl = trimString(input.a2a_config?.agent_card_url);
  const agentCardUrl = nestedAgentCardUrl || directAgentCardUrl;

  const agentId = normalizeId(input.agent_id || deriveIdFromUrl(agentCardUrl));
  const name = trimString(input.name) || titleFromId(agentId);
  const protocolVersion = normalizeSemver(input.a2a_config?.protocol_version || input.protocol_version || "1.0.0");
  const skills = normalizeSkills(input.skills);

  if (!agentId) {
    throw new Error("agent_id is required or must be derivable from agent_card_url.");
  }
  if (!name) {
    throw new Error("name is required.");
  }
  if (!agentCardUrl || !agentCardUrl.startsWith("https://")) {
    throw new Error("a2a_config.agent_card_url must be an HTTPS URL.");
  }
  if (!protocolVersion) {
    throw new Error("a2a_config.protocol_version must contain a numeric version.");
  }
  if (skills.length === 0) {
    throw new Error("skills must include at least one skill with id, name, and tags.");
  }

  out.agent_id = agentId;
  out.name = name;

  const description = trimString(input.description);
  if (description) {
    out.description = description;
  }

  out.version = normalizeSemver(input.version || "1.0.0") || "1.0.0";
  out.a2a_config = {
    agent_card_url: agentCardUrl,
    protocol_version: protocolVersion
  };
  out.skills = skills;

  const contact: SubmitPayload["contact"] = {};
  const email = trimString(input.contact?.email || input.email);
  const contactUrl = trimString(input.contact?.url);
  if (email) {
    contact.email = email;
  }
  if (contactUrl && contactUrl.startsWith("https://")) {
    contact.url = contactUrl;
  }
  if (Object.keys(contact).length > 0) {
    out.contact = contact;
  }

  const healthUrl = trimString(input.health_check?.url);
  if (healthUrl && healthUrl.startsWith("https://")) {
    out.health_check = { url: healthUrl };
  }

  if (input.dynamic_data && typeof input.dynamic_data === "object") {
    out.dynamic_data = input.dynamic_data;
  }
  if (input.openclaw && typeof input.openclaw === "object") {
    out.openclaw = input.openclaw;
  }

  return out;
}

function normalizeSkills(input: SubmitPayload["skills"]): AgentSkill[] {
  if (!Array.isArray(input)) {
    return [];
  }

  const result: AgentSkill[] = [];
  for (const item of input) {
    if (typeof item === "string") {
      const name = trimString(item);
      const id = normalizeId(name);
      if (id && name) {
        result.push({ id, name, tags: [id] });
      }
      continue;
    }

    if (!item || typeof item !== "object") {
      continue;
    }

    const skill = item as AgentSkill;
    const id = normalizeId(skill.id || skill.name);
    const name = trimString(skill.name) || titleFromId(id);
    const tags = Array.isArray(skill.tags)
      ? skill.tags.map((tag) => normalizeId(tag)).filter(Boolean)
      : [];

    if (id && name) {
      result.push({ ...skill, id, name, tags: Array.from(new Set(tags.length > 0 ? tags : [id])) });
    }
  }

  return result;
}

function normalizeId(value: unknown): string {
  return trimString(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function normalizeSemver(value: unknown): string {
  const raw = trimString(value).toLowerCase();
  const match = raw.match(/(\d+)(?:\D+(\d+))?(?:\D+(\d+))?/);
  if (!match) {
    return "";
  }
  const major = Number.parseInt(match[1] || "0", 10);
  const minor = Number.parseInt(match[2] || "0", 10);
  const patch = Number.parseInt(match[3] || "0", 10);
  return `${major}.${minor}.${patch}`;
}

function deriveIdFromUrl(url: unknown): string {
  const value = trimString(url);
  if (!value) {
    return "";
  }
  try {
    const parsed = new URL(value);
    const host = parsed.hostname.replace(/^www\./, "");
    return host.split(".")[0] || "";
  } catch {
    return "";
  }
}

function titleFromId(id: string): string {
  return id
    .split("-")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function trimString(value: unknown): string {
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return String(value).trim();
  }
  return "";
}

function normalizeBaseUrl(value: string): string {
  return value.replace(/\/+$/, "");
}

function parsePositiveInt(value: string | undefined, fallback: number): number {
  const parsed = Number.parseInt(value || "", 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function jsonToolResult(data: unknown) {
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(data, null, 2)
      }
    ]
  };
}

function stringifyCompact(data: unknown): string {
  try {
    return JSON.stringify(data);
  } catch {
    return String(data);
  }
}

function isObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
