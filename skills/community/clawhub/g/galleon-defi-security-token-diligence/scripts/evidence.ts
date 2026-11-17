/** Copyright (c) 2026 Galleon Labs. MIT licensed; see ../LICENSE. */
import { open } from "node:fs/promises";
import { constants } from "node:fs";
import { createHash } from "node:crypto";

export const AREAS = [
  "controls",
  "launch",
  "liquidity",
  "exits",
  "fees",
  "treasury",
  "metadata",
] as const;
type Area = (typeof AREAS)[number];
type Target = { chainId: string; address: string };
type Pin = {
  number: string;
  hash: string;
  timestamp: string;
  header: { number: string; hash: string; timestamp: string };
};
type Evidence = {
  id: string;
  status: "observed" | "unknown";
  source: string;
  query: string;
  artifact: string | null;
  target: Target;
  blockHash: string;
  value: unknown;
};
type Metadata = {
  status: "observed" | "unknown";
  value: string | null;
  reason: string;
  evidence: string[];
};
export type Report = {
  schemaVersion: 1;
  execution: {
    realSigning: false;
    broadcast: false;
    simulation: "none" | "disposable-fork";
  };
  historicalPins: Pin[];
  requested: Target;
  observed: Target;
  reported: Target;
  pin: Pin;
  evidence: Evidence[];
  contracts: {
    id: string;
    address: string;
    role:
      | "token"
      | "implementation"
      | "admin"
      | "beacon"
      | "pool"
      | "treasury"
      | "other";
    status: "observed" | "unknown";
    evidence: string[];
  }[];
  metadata: Record<"name" | "symbol" | "decimals" | "totalSupply", Metadata>;
  coverage: {
    id: Area;
    status: "complete" | "partial" | "unknown";
    note: string;
    evidence: string[];
  }[];
  findings: {
    id: string;
    area: Area;
    status: "pass" | "risk" | "unknown";
    summary: string;
    evidence: string[];
  }[];
};
const ADDRESS = /^0x[0-9a-f]{40}$/;
const HASH = /^0x[0-9a-f]{64}$/;
const QUANTITY = /^0x(?:0|[1-9a-f][0-9a-f]*)$/;
const DECIMAL = /^(?:0|[1-9][0-9]*)$/;
const ID = /^[a-z][a-z0-9-]{0,79}$/;
const MAX_BYTES = 1024 * 1024;
const SELECTORS = {
  name: "0x06fdde03",
  symbol: "0x95d89b41",
  decimals: "0x313ce567",
  totalSupply: "0x18160ddd",
};
function assert(ok: unknown, message: string): asserts ok {
  if (!ok) throw new Error(message);
}
function object(
  value: unknown,
  keys: string[],
  path: string,
): asserts value is Record<string, any> {
  assert(
    value !== null && typeof value === "object" && !Array.isArray(value),
    `${path}: expected object`,
  );
  const actual = Object.keys(value);
  assert(
    actual.length === keys.length && actual.every((k) => keys.includes(k)),
    `${path}: missing or unexpected fields`,
  );
}
function text(value: unknown, path: string): asserts value is string {
  assert(
    typeof value === "string" &&
      value.trim().length > 0 &&
      value.length <= 8192,
    `${path}: expected bounded nonempty text`,
  );
}
function target(value: unknown, path: string): asserts value is Target {
  object(value, ["chainId", "address"], path);
  assert(
    typeof value.chainId === "string" &&
      /^[1-9][0-9]{0,77}$/.test(value.chainId),
    `${path}: invalid chain ID`,
  );
  assert(
    typeof value.address === "string" && ADDRESS.test(value.address),
    `${path}: require lowercase EVM address`,
  );
}
function sameTarget(a: Target, b: Target): boolean {
  return a.chainId === b.chainId && a.address === b.address;
}
function list(value: unknown, path: string): asserts value is any[] {
  assert(
    Array.isArray(value) && value.length <= 1000,
    `${path}: expected bounded array`,
  );
}
function keyed(value: unknown, path: string): asserts value is any[] {
  list(value, path);
  const ids = new Set();
  for (const entry of value) {
    assert(
      entry &&
        typeof entry.id === "string" &&
        ID.test(entry.id) &&
        !ids.has(entry.id),
      `${path}: invalid or duplicate ID`,
    );
    ids.add(entry.id);
  }
}
function header(value: unknown): asserts value is Pin["header"] {
  object(value, ["number", "hash", "timestamp"], "pin.header");
  assert(
    typeof value.number === "string" &&
      QUANTITY.test(value.number) &&
      typeof value.hash === "string" &&
      HASH.test(value.hash) &&
      !/^0x([0-9a-f])\1{63}$/.test(value.hash) &&
      typeof value.timestamp === "string" &&
      QUANTITY.test(value.timestamp),
    "invalid captured header or placeholder hash",
  );
}
function utc(timestamp: string): string {
  const milliseconds = BigInt(timestamp) * 1000n;
  assert(
    milliseconds <= 8640000000000000n,
    "header timestamp outside date range",
  );
  return new Date(Number(milliseconds)).toISOString();
}
/** Checks internal consistency only. A fabricated but consistent report can pass. */
export function validate(value: unknown): Report {
  object(
    value,
    [
      "schemaVersion",
      "execution",
      "historicalPins",
      "requested",
      "observed",
      "reported",
      "pin",
      "evidence",
      "contracts",
      "metadata",
      "coverage",
      "findings",
    ],
    "report",
  );
  assert(value.schemaVersion === 1, "unsupported schema version");
  object(
    value.execution,
    ["realSigning", "broadcast", "simulation"],
    "execution",
  );
  assert(
    value.execution.realSigning === false &&
      value.execution.broadcast === false &&
      ["none", "disposable-fork"].includes(value.execution.simulation),
    "real signing or broadcast declarations forbidden",
  );
  for (const key of ["requested", "observed", "reported"])
    target(value[key], key);
  assert(
    sameTarget(value.requested, value.observed) &&
      sameTarget(value.requested, value.reported),
    "requested, observed and reported targets differ",
  );
  object(value.pin, ["number", "hash", "timestamp", "header"], "pin");
  header(value.pin.header);
  assert(
    value.pin.number === value.pin.header.number &&
      value.pin.hash === value.pin.header.hash &&
      value.pin.timestamp === utc(value.pin.header.timestamp),
    "pin does not match captured header",
  );
  list(value.historicalPins, "historicalPins");
  const pins = new Map<string, Pin>([[value.pin.hash, value.pin as Pin]]);
  for (const pin of value.historicalPins) {
    object(pin, ["number", "hash", "timestamp", "header"], "historical pin");
    header(pin.header);
    assert(
      pin.number === pin.header.number &&
        pin.hash === pin.header.hash &&
        pin.timestamp === utc(pin.header.timestamp),
      "historical pin does not match captured header",
    );
    assert(
      !pins.has(pin.hash) &&
        BigInt(pin.number) < BigInt(value.pin.number) &&
        BigInt(pin.header.timestamp) <= BigInt(value.pin.header.timestamp),
      "historical pin must be unique and older than primary pin",
    );
    pins.set(pin.hash, pin as Pin);
  }
  keyed(value.evidence, "evidence");
  const evidence = new Map<string, Evidence>();
  for (const item of value.evidence) {
    object(
      item,
      [
        "id",
        "status",
        "source",
        "query",
        "artifact",
        "target",
        "blockHash",
        "value",
      ],
      "evidence entry",
    );
    assert(
      ["observed", "unknown"].includes(item.status),
      "invalid evidence status",
    );
    text(item.source, "source");
    text(item.query, "query");
    assert(
      item.artifact === null ||
        (typeof item.artifact === "string" &&
          item.artifact.length > 0 &&
          item.artifact.length <= 8192),
      "invalid artifact reference",
    );
    target(item.target, "evidence target");
    assert(
      sameTarget(value.requested, item.target) && pins.has(item.blockHash),
      "evidence target or block mismatch",
    );
    assert(
      item.status !== "unknown" || item.value === null,
      "unknown evidence must have null value",
    );
    evidence.set(item.id, item as Evidence);
  }
  const chain = evidence.get("chain-id");
  assert(
    chain?.status === "observed" &&
      chain.blockHash === value.pin.hash &&
      chain.query === "eth_chainId" &&
      typeof chain.value === "string" &&
      QUANTITY.test(chain.value) &&
      BigInt(chain.value).toString() === value.observed.chainId,
    "missing or mismatched chain observation",
  );
  const captured = evidence.get("block-header");
  assert(
    captured?.status === "observed" &&
      captured.blockHash === value.pin.hash &&
      captured.query === "eth_getBlockByNumber" &&
      JSON.stringify(canonical(captured.value)) ===
        JSON.stringify(canonical(value.pin.header)),
    "missing or mismatched captured header evidence",
  );
  for (const pin of value.historicalPins)
    assert(
      value.evidence.some(
        (item: Evidence) =>
          item.status === "observed" &&
          item.blockHash === pin.hash &&
          item.query === "eth_getBlockByNumber" &&
          JSON.stringify(canonical(item.value)) ===
            JSON.stringify(canonical(pin.header)),
      ),
      "historical pin lacks matching header evidence",
    );
  function refs(input: unknown, requireObserved: boolean): void {
    list(input, "evidence references");
    assert(
      new Set(input).size === input.length &&
        input.every((id) => typeof id === "string" && evidence.has(id)),
      "unknown or duplicate evidence reference",
    );
    if (requireObserved)
      assert(
        input.length > 0 &&
          input.every((id) => evidence.get(id)?.status === "observed"),
        "observed claim requires observed evidence",
      );
  }
  keyed(value.contracts, "contracts");
  assert(value.contracts.length > 0, "missing material target contract");
  for (const contract of value.contracts) {
    object(
      contract,
      ["id", "address", "role", "status", "evidence"],
      "contract",
    );
    assert(
      ADDRESS.test(contract.address) &&
        [
          "token",
          "implementation",
          "admin",
          "beacon",
          "pool",
          "treasury",
          "other",
        ].includes(contract.role) &&
        ["observed", "unknown"].includes(contract.status),
      "invalid contract scope",
    );
    refs(contract.evidence, contract.status === "observed");
  }
  assert(
    value.contracts.some(
      (c: any) => c.role === "token" && c.address === value.requested.address,
    ),
    "target token missing from scope",
  );
  for (const contract of value.contracts.filter(
    (c: any) => c.role === "token" && c.status === "observed",
  ))
    assert(
      contract.evidence.some((id: string) => {
        const item = evidence.get(id)!;
        return (
          item.blockHash === value.pin.hash &&
          item.query === `eth_getCode ${contract.address}` &&
          typeof item.value === "string" &&
          /^0x(?:[0-9a-f]{2})+$/.test(item.value)
        );
      }),
      "observed token contract requires matching runtime code evidence",
    );
  object(
    value.metadata,
    ["name", "symbol", "decimals", "totalSupply"],
    "metadata",
  );
  for (const key of ["name", "symbol", "decimals", "totalSupply"]) {
    const item = value.metadata[key];
    object(item, ["status", "value", "reason", "evidence"], `metadata.${key}`);
    assert(
      ["observed", "unknown"].includes(item.status),
      "invalid metadata status",
    );
    text(item.reason, "metadata reason");
    if (item.status === "unknown")
      assert(item.value === null, "unknown metadata must have null value");
    else {
      text(item.value, "metadata value");
      if (key === "decimals" || key === "totalSupply")
        assert(
          DECIMAL.test(item.value) &&
            BigInt(item.value) < 2n ** (key === "decimals" ? 8n : 256n),
          "invalid metadata integer",
        );
    }
    refs(item.evidence, item.status === "observed");
    if (item.status === "observed")
      assert(
        item.evidence.some((id: string) => {
          const entry = evidence.get(id)!;
          if (
            entry.blockHash !== value.pin.hash ||
            entry.query !==
              `eth_call ${value.requested.address} ${SELECTORS[key as keyof typeof SELECTORS]}`
          )
            return false;
          try {
            return (
              decodeMetadata(
                entry.value,
                key === "decimals" || key === "totalSupply",
                key === "decimals",
              ) === item.value
            );
          } catch {
            return false;
          }
        }),
        "metadata value does not match captured getter evidence",
      );
  }
  keyed(value.coverage, "coverage");
  assert(
    value.coverage.length === AREAS.length &&
      AREAS.every((id) => value.coverage.some((c: any) => c.id === id)),
    "required coverage area missing",
  );
  for (const item of value.coverage) {
    object(item, ["id", "status", "note", "evidence"], "coverage");
    assert(
      ["complete", "partial", "unknown"].includes(item.status),
      "invalid coverage status",
    );
    text(item.note, "coverage note");
    refs(item.evidence, item.status !== "unknown");
    if (item.id === "metadata" && item.status === "complete")
      assert(
        Object.values(value.metadata).every(
          (m: any) => m.status === "observed",
        ),
        "unknown metadata cannot have complete coverage",
      );
  }
  keyed(value.findings, "findings");
  for (const item of value.findings) {
    object(item, ["id", "area", "status", "summary", "evidence"], "finding");
    assert(
      AREAS.includes(item.area) &&
        ["pass", "risk", "unknown"].includes(item.status),
      "invalid finding",
    );
    text(item.summary, "finding summary");
    refs(item.evidence, item.status !== "unknown");
    if (item.status === "pass")
      assert(
        value.coverage.find((c: any) => c.id === item.area)?.status ===
          "complete",
        "unknown or partial coverage cannot pass",
      );
  }
  return value as Report;
}
// Object keys are unordered; arbitrary payload arrays retain their exact sequence.
function canonical(value: any): any {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object")
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((k) => [k, canonical(value[k])]),
    );
  return value;
}
export function compare(beforeInput: unknown, afterInput: unknown) {
  const before = validate(beforeInput),
    after = validate(afterInput);
  assert(
    sameTarget(before.requested, after.requested),
    "cannot compare different targets",
  );
  const equal = (a: unknown, b: unknown) =>
    JSON.stringify(canonical(a)) === JSON.stringify(canonical(b));
  const changes: {
    section: string;
    id: string;
    change: "added" | "removed" | "changed";
    before: unknown;
    after: unknown;
  }[] = [];
  for (const key of ["execution", "historicalPins"] as const) {
    const a =
      key === "historicalPins"
        ? [...before.historicalPins].sort((x, y) =>
            x.hash.localeCompare(y.hash),
          )
        : before[key];
    const b =
      key === "historicalPins"
        ? [...after.historicalPins].sort((x, y) => x.hash.localeCompare(y.hash))
        : after[key];
    if (!equal(a, b))
      changes.push({
        section: key,
        id: key,
        change: "changed",
        before: a,
        after: b,
      });
  }
  for (const section of [
    "contracts",
    "coverage",
    "findings",
    "evidence",
  ] as const) {
    // The pin is reported separately; preserve substantive query/artifact/value changes.
    const normalize = (item: any, report: Report) =>
      section !== "evidence"
        ? { ...item, evidence: [...item.evidence].sort() }
        : item.blockHash !== report.pin.hash
          ? item
          : item.id === "block-header"
            ? { ...item, blockHash: null, value: null }
            : { ...item, blockHash: null };
    const a = new Map(
      before[section].map((item) => [item.id, normalize(item, before)]),
    );
    const b = new Map(
      after[section].map((item) => [item.id, normalize(item, after)]),
    );
    for (const id of [...new Set([...a.keys(), ...b.keys()])].sort())
      if (!equal(a.get(id), b.get(id)))
        changes.push({
          section,
          id,
          change: !a.has(id) ? "added" : !b.has(id) ? "removed" : "changed",
          before: a.get(id) ?? null,
          after: b.get(id) ?? null,
        });
  }
  for (const key of Object.keys(
    before.metadata,
  ) as (keyof Report["metadata"])[])
    if (
      !equal(
        {
          ...before.metadata[key],
          evidence: [...before.metadata[key].evidence].sort(),
        },
        {
          ...after.metadata[key],
          evidence: [...after.metadata[key].evidence].sort(),
        },
      )
    )
      changes.push({
        section: "metadata",
        id: key,
        change: "changed",
        before: before.metadata[key],
        after: after.metadata[key],
      });
  const pinChanged = !equal(before.pin, after.pin);
  const backward = BigInt(after.pin.number) < BigInt(before.pin.number);
  const sameHeightDifferentHash =
    before.pin.number === after.pin.number &&
    before.pin.hash !== after.pin.hash;
  return {
    target: before.requested,
    pin: {
      changed: pinChanged,
      before: before.pin,
      after: after.pin,
      backward,
      sameHeightDifferentHash,
    },
    substantiveChange: changes.length > 0,
    pinOnly: pinChanged && changes.length === 0,
    changes,
    note: "Removed findings and reduced or unknown coverage are not resolutions. Higher block numbers do not prove canonical ancestry. Comparison checks supplied evidence, not chain truth.",
  };
}

export async function rpc(
  url: string,
  method: string,
  params: unknown[],
  id: number,
  options: { timeoutMs?: number; maxBytes?: number } = {},
): Promise<unknown> {
  assert(
    ["eth_chainId", "eth_getBlockByNumber", "eth_getCode", "eth_call"].includes(
      method,
    ),
    "RPC method not allowed",
  );
  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    // URL parser errors can embed the secret-bearing input in their message.
    throw new Error("RPC URL is invalid");
  }
  assert(
    parsed.protocol === "https:" ||
      (parsed.protocol === "http:" &&
        ["localhost", "127.0.0.1", "[::1]"].includes(parsed.hostname)),
    "RPC requires HTTPS or loopback HTTP",
  );
  assert(
    !parsed.username && !parsed.password && !parsed.hash,
    "RPC URL userinfo and fragment not allowed",
  );
  const controller = new AbortController(),
    timer = setTimeout(() => controller.abort(), options.timeoutMs ?? 10_000);
  const maxBytes = options.maxBytes ?? MAX_BYTES;
  try {
    const response = await fetch(url, {
      method: "POST",
      redirect: "error",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", method, params, id }),
      signal: controller.signal,
    });
    assert(response.ok, `RPC HTTP ${response.status}`);
    const reader = response.body?.getReader();
    assert(reader, "RPC response missing body");
    let length = 0;
    const chunks: Uint8Array[] = [];
    try {
      while (true) {
        const chunk = await reader.read();
        if (chunk.done) break;
        length += chunk.value.byteLength;
        assert(length <= maxBytes, "RPC response too large");
        chunks.push(chunk.value);
      }
    } finally {
      await reader.cancel();
    }
    const bytes = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) {
      bytes.set(chunk, offset);
      offset += chunk.length;
    }
    const body = JSON.parse(
      new TextDecoder("utf-8", { fatal: true }).decode(bytes),
    );
    assert(
      body && body.jsonrpc === "2.0" && body.id === id && !Array.isArray(body),
      "invalid RPC response identity",
    );
    assert(!Object.hasOwn(body, "error"), "RPC returned an error");
    assert(Object.hasOwn(body, "result"), "RPC result missing");
    return body.result;
  } catch (error) {
    // Network exceptions and provider messages can contain secret-bearing URLs.
    const safe =
      error instanceof Error && /^(RPC |invalid RPC)/.test(error.message)
        ? error.message
        : "RPC transport or response failure";
    throw new Error(safe);
  } finally {
    clearTimeout(timer);
  }
}
function hexBytes(value: unknown): asserts value is string {
  assert(
    typeof value === "string" && /^0x(?:[0-9a-fA-F]{2})*$/.test(value),
    "invalid ABI bytes",
  );
}
export function decodeMetadata(
  value: unknown,
  integer: boolean,
  decimals = false,
): string {
  hexBytes(value);
  const hex = value.slice(2);
  if (integer) {
    assert(hex.length === 64, "expected one ABI integer word");
    const n = BigInt(value);
    assert(!decimals || n <= 255n, "decimals outside uint8");
    return n.toString();
  }
  assert(
    hex.length >= 128 &&
      hex.length % 64 === 0 &&
      BigInt(`0x${hex.slice(0, 64)}`) === 32n,
    "expected canonical dynamic ABI string",
  );
  const n = BigInt(`0x${hex.slice(64, 128)}`);
  assert(n > 0n && n <= 4096n, "metadata string length out of bounds");
  const length = Number(n);
  assert(
    hex.length === 128 + Math.ceil(length / 32) * 64 &&
      /^0*$/.test(hex.slice(128 + length * 2)),
    "invalid ABI string padding or length",
  );
  const result = new TextDecoder("utf-8", { fatal: true }).decode(
    Uint8Array.from(Buffer.from(hex.slice(128, 128 + length * 2), "hex")),
  );
  assert(
    result.trim().length > 0 && !/[\u0000-\u001f\u007f]/.test(result),
    "unsafe metadata string",
  );
  return result;
}
export async function collect(
  chainId: string,
  address: string,
  url: string,
): Promise<Report> {
  const requested = { chainId, address: address.toLowerCase() };
  target(requested, "requested");
  let id = 0;
  const call = (method: string, params: unknown[]) =>
    rpc(url, method, params, ++id);
  const chain = await call("eth_chainId", []);
  assert(
    typeof chain === "string" &&
      QUANTITY.test(chain) &&
      BigInt(chain).toString() === chainId,
    "RPC chain differs from requested chain",
  );
  const raw: any = await call("eth_getBlockByNumber", ["latest", false]);
  const captured = {
    number: raw?.number,
    hash: raw?.hash,
    timestamp: raw?.timestamp,
  };
  header(captured);
  const pin: Pin = {
    number: captured.number,
    hash: captured.hash,
    timestamp: utc(captured.timestamp),
    header: captured,
  };
  const evidence: Evidence[] = [];
  const add = (
    entryId: string,
    query: string,
    value: unknown,
    status: "observed" | "unknown" = "observed",
  ) =>
    evidence.push({
      id: entryId,
      status,
      source: "configured RPC (URL intentionally omitted)",
      query,
      artifact: null,
      target: requested,
      blockHash: pin.hash,
      value,
    });
  add("chain-id", "eth_chainId", chain);
  add("block-header", "eth_getBlockByNumber", captured);
  const block = { blockHash: pin.hash, requireCanonical: true };
  const code = await call("eth_getCode", [requested.address, block]);
  hexBytes(code);
  assert(code !== "0x", "target has no runtime code at captured block");
  add("runtime-code", `eth_getCode ${requested.address}`, code.toLowerCase());
  add(
    "runtime-code-sha256",
    `SHA-256 bytes from eth_getCode ${requested.address}`,
    createHash("sha256")
      .update(Uint8Array.from(Buffer.from(code.slice(2), "hex")))
      .digest("hex"),
  );
  const metadata = {} as Report["metadata"];
  const calls = SELECTORS;
  for (const [key, data] of Object.entries(calls) as [
    keyof Report["metadata"],
    string,
  ][]) {
    const entryId = `metadata-${key.toLowerCase()}`;
    const query = `eth_call ${requested.address} ${data}`;
    try {
      const rawValue = await call("eth_call", [
        { to: requested.address, data, gas: "0x186a0" },
        block,
      ]);
      const value = decodeMetadata(
        rawValue,
        key === "decimals" || key === "totalSupply",
        key === "decimals",
      );
      add(entryId, query, rawValue);
      metadata[key] = {
        status: "observed",
        value,
        reason:
          "Strict ABI decode of captured RPC return; untrusted token-provided metadata.",
        evidence: [entryId],
      };
    } catch {
      add(entryId, query, null, "unknown");
      metadata[key] = {
        status: "unknown",
        value: null,
        reason:
          "Read or strict ABI decoding failed. No fallback or inferred value.",
        evidence: [entryId],
      };
    }
  }
  const completeMetadata = Object.values(metadata).every(
    (item) => item.status === "observed",
  );
  return validate({
    schemaVersion: 1,
    execution: { realSigning: false, broadcast: false, simulation: "none" },
    historicalPins: [],
    requested,
    observed: requested,
    reported: requested,
    pin,
    evidence,
    contracts: [
      {
        id: "target-token",
        address: requested.address,
        role: "token",
        status: "observed",
        evidence: ["runtime-code"],
      },
    ],
    metadata,
    coverage: AREAS.map((area) => ({
      id: area,
      status:
        area === "metadata"
          ? completeMetadata
            ? "complete"
            : Object.values(metadata).some((item) => item.status === "observed")
              ? "partial"
              : "unknown"
          : "unknown",
      note:
        area === "metadata"
          ? "Only name, symbol, decimals and raw totalSupply getter responses; identity and supply economics require investigation."
          : "Not collected. Material related contracts, proxy/control roles, history and economic checks require separate investigation.",
      evidence:
        area === "metadata"
          ? Object.values(metadata).flatMap((item) =>
              item.status === "observed" ? item.evidence : [],
            )
          : [],
    })),
    findings: [
      {
        id: "bounded-snapshot",
        area: "controls",
        status: "unknown",
        summary:
          "Runtime code exists. Proxy identity, privileged controls, material pools and all economic diligence remain unresolved.",
        evidence: ["runtime-code"],
      },
    ],
  });
}
export async function load(path: string): Promise<unknown> {
  const file = await open(path, constants.O_RDONLY | constants.O_NONBLOCK);
  try {
    const info = await file.stat();
    assert(info.isFile(), "report must be a regular file");
    assert(info.size <= MAX_BYTES, "report file too large");
    const buffer = new Uint8Array(MAX_BYTES + 1);
    let length = 0;
    while (length <= MAX_BYTES) {
      const { bytesRead } = await file.read(
        buffer,
        length,
        buffer.length - length,
        null,
      );
      if (bytesRead === 0) break;
      length += bytesRead;
    }
    assert(length <= MAX_BYTES, "report file too large");
    return JSON.parse(
      new TextDecoder("utf-8", { fatal: true }).decode(
        buffer.subarray(0, length),
      ),
    );
  } finally {
    await file.close();
  }
}
if (import.meta.main) {
  try {
    const [command, ...args] = process.argv.slice(2);
    let result: unknown;
    if (command === "validate" && args.length === 1) {
      validate(await load(args[0]!));
      result = {
        valid: true,
        note: "Internal consistency only; not a security verdict or proof of RPC truth.",
      };
    } else if (command === "compare" && args.length === 2)
      result = compare(await load(args[0]!), await load(args[1]!));
    else if (command === "collect" && args.length === 2) {
      const url = process.env.DEFI_RPC_URL;
      assert(url, "DEFI_RPC_URL is required");
      result = await collect(args[0]!, args[1]!, url);
    } else
      throw new Error(
        "Usage: evidence.ts validate REPORT | compare BEFORE AFTER | collect DECIMAL_CHAIN_ID TOKEN_ADDRESS (DEFI_RPC_URL environment variable)",
      );
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) {
    process.stderr.write(
      `${error instanceof Error ? error.message : "Evidence helper failed"}\n`,
    );
    process.exitCode = 1;
  }
}
