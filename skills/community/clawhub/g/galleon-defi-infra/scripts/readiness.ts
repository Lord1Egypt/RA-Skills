/** Read-only EVM endpoint diagnosis. No signer, subprocess, payment or arbitrary RPC method. */
export type ReadinessInput = {
  rpcUrl?: string | undefined;
  chainId: number;
  maxAgeSeconds?: number | undefined;
};
export type ReadinessReport = {
  ok: boolean;
  code: "ready" | "missing_rpc" | "invalid_config" | "http_error" | "rpc_error" | "invalid_response" | "request_failed" | "chain_mismatch" | "stale_block" | "future_block";
  chainId?: number;
  blockNumber?: string;
  blockAgeSeconds?: number;
  requests: number;
};
export type Transport = (input: string | URL, init?: RequestInit) => Promise<Response>;
const MAX_BYTES = 65_536;
const QUANTITY = /^0x(?:0|[1-9a-fA-F][0-9a-fA-F]*)$/;

class ProbeError extends Error {
  constructor(readonly code: ReadinessReport["code"]) { super(code); }
}
function quantity(value: unknown): bigint {
  if (typeof value !== "string" || value.length > 66 || !QUANTITY.test(value)) throw new ProbeError("invalid_response");
  return BigInt(value);
}
function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) throw new ProbeError("invalid_response");
  return value as Record<string, unknown>;
}
async function boundedJson(response: Response): Promise<unknown> {
  if (!response.body) throw new ProbeError("invalid_response");
  const reader = response.body.getReader();
  let bytes = 0;
  const decoder = new TextDecoder();
  let body = "";
  try {
    for (;;) {
      const chunk = await reader.read();
      if (chunk.done) break;
      bytes += chunk.value.byteLength;
      if (bytes > MAX_BYTES) throw new ProbeError("invalid_response");
      body += decoder.decode(chunk.value, { stream: true });
    }
    body += decoder.decode();
    return JSON.parse(body) as unknown;
  } catch (error) {
    if (error instanceof ProbeError) throw error;
    throw new ProbeError("invalid_response");
  } finally {
    await reader.cancel().catch(() => {});
  }
}

/** Caller supplies the intended endpoint. HTTPS is required except literal localhost loopback. */
export async function diagnoseRpc(
  input: ReadinessInput,
  transport: Transport = fetch,
  nowMilliseconds: number = Date.now(),
): Promise<ReadinessReport> {
  let requests = 0;
  const fail = (code: ReadinessReport["code"]): ReadinessReport => ({ ok: false, code, requests });
  const maxAge = input.maxAgeSeconds ?? 120;
  if (!Number.isSafeInteger(input.chainId) || input.chainId <= 0 || !Number.isSafeInteger(maxAge) || maxAge < 1 || maxAge > 86_400 || !Number.isSafeInteger(nowMilliseconds) || nowMilliseconds < 0) return fail("invalid_config");
  if (!input.rpcUrl?.trim()) return fail("missing_rpc");
  let endpoint: URL;
  try { endpoint = new URL(input.rpcUrl); } catch { return fail("invalid_config"); }
  const loopback = ["localhost", "127.0.0.1", "[::1]"].includes(endpoint.hostname);
  if ((endpoint.protocol !== "https:" && !(endpoint.protocol === "http:" && loopback)) || endpoint.username || endpoint.password || endpoint.hash) return fail("invalid_config");
  const rpc = async (method: "eth_chainId" | "eth_getBlockByNumber", params: unknown[]): Promise<unknown> => {
    const id = ++requests;
    const controller = new AbortController();
    let timer: ReturnType<typeof setTimeout> | undefined;
    const timeout = new Promise<never>((_, reject) => {
      timer = setTimeout(() => { controller.abort(); reject(new ProbeError("request_failed")); }, 5_000);
    });
    try {
      return await Promise.race([(async () => {
        const response = await transport(endpoint, {
          method: "POST", redirect: "error", signal: controller.signal,
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
        });
        if (!response.ok) {
          await response.body?.cancel().catch(() => {});
          throw new ProbeError("http_error");
        }
        const body = object(await boundedJson(response));
        if (body.jsonrpc !== "2.0" || body.id !== id) throw new ProbeError("invalid_response");
        if (Object.hasOwn(body, "error")) throw new ProbeError("rpc_error");
        return body.result;
      })(), timeout]);
    } finally { clearTimeout(timer); }
  };
  try {
    const chain = quantity(await rpc("eth_chainId", []));
    if (chain !== BigInt(input.chainId)) return fail("chain_mismatch");
    const block = object(await rpc("eth_getBlockByNumber", ["latest", false]));
    const height = quantity(block.number);
    const timestamp = quantity(block.timestamp);
    if (timestamp > BigInt(Number.MAX_SAFE_INTEGER)) return fail("invalid_response");
    const age = Math.floor(nowMilliseconds / 1_000) - Number(timestamp);
    const code = age < -30 ? "future_block" : age > maxAge ? "stale_block" : "ready";
    return { ok: code === "ready", code, chainId: input.chainId, blockNumber: height.toString(), blockAgeSeconds: age, requests };
  } catch (error) {
    return fail(error instanceof ProbeError ? error.code : "request_failed");
  }
}

const PRESENCE_KEYS = ["DEFI_RPC_URL", "ALCHEMY_API_KEY", "ALCHEMY_NETWORK"] as const;
/** Values, names supplied by callers, filesystem paths and provider errors never enter this output. */
export function credentialPresence(environment: Record<string, string | undefined>): Record<string, boolean> {
  return Object.fromEntries(PRESENCE_KEYS.map((key) => [key, Boolean(environment[key]?.trim())]));
}
