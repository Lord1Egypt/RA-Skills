import type { PluginConfig, PayloadMode } from './types.js';

const VALID_MODES: PayloadMode[] = ['metadata', 'debug', 'full'];

export function validate(raw: unknown): PluginConfig {
  if (typeof raw !== 'object' || raw === null) {
    throw new Error('Plugin config must be an object');
  }

  const obj = raw as Record<string, unknown>;

  if (typeof obj.traces_endpoint !== 'string' || !obj.traces_endpoint) {
    throw new Error('Plugin config requires a non-empty "traces_endpoint" string');
  }

  const mode = (obj.payload_mode ?? 'metadata') as PayloadMode;
  if (!VALID_MODES.includes(mode)) {
    throw new Error(`Invalid payload_mode "${mode}". Must be one of: ${VALID_MODES.join(', ')}`);
  }

  const headers = buildHeaders(obj);

  return {
    traces_endpoint: obj.traces_endpoint.replace(/\/+$/, ''),
    logs_endpoint: typeof obj.logs_endpoint === 'string' && obj.logs_endpoint
      ? obj.logs_endpoint.replace(/\/+$/, '')
      : undefined,
    headers: Object.keys(headers).length > 0 ? headers : undefined,
    payload_mode: mode,
    batch_delay_ms: typeof obj.batch_delay_ms === 'number' ? obj.batch_delay_ms : 2000,
    batch_max_size: typeof obj.batch_max_size === 'number' ? obj.batch_max_size : 50,
    export_timeout_ms: typeof obj.export_timeout_ms === 'number' ? obj.export_timeout_ms : 30000,
    enabled: typeof obj.enabled === 'boolean' ? obj.enabled : true,
    debug: typeof obj.debug === 'boolean' ? obj.debug : undefined,
    model_map: typeof obj.model_map === 'object' && obj.model_map !== null
      ? Object.fromEntries(
          Object.entries(obj.model_map as Record<string, unknown>)
            .filter((entry): entry is [string, string] => typeof entry[1] === 'string'),
        )
      : undefined,
    model_pricing: parseModelPricing(obj.model_pricing),
  };
}

function buildHeaders(obj: Record<string, unknown>): Record<string, string> {
  const headers: Record<string, string> = {};

  if (typeof obj.headers === 'object' && obj.headers !== null) {
    for (const [k, v] of Object.entries(obj.headers as Record<string, unknown>)) {
      if (typeof v === 'string') headers[k] = v;
    }
  }

  if (typeof obj.authorization === 'string' && obj.authorization) {
    headers['Authorization'] ??= obj.authorization;
  }
  if (typeof obj.workspace_id === 'string' && obj.workspace_id) {
    headers['X-Workspace-Id'] ??= obj.workspace_id;
  }
  if (typeof obj.application_id === 'string' && obj.application_id) {
    headers['X-Application-Id'] ??= obj.application_id;
  }

  return headers;
}

function parseModelPricing(
  raw: unknown,
): Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }> | undefined {
  if (typeof raw !== 'object' || raw === null) return undefined;
  const result: Record<string, { input: number; output: number; cacheRead?: number; cacheWrite?: number }> = {};
  for (const [key, val] of Object.entries(raw as Record<string, unknown>)) {
    if (typeof val !== 'object' || val === null) continue;
    const v = val as Record<string, unknown>;
    if (typeof v.input !== 'number' || typeof v.output !== 'number') continue;
    result[key] = {
      input: v.input,
      output: v.output,
      ...(typeof v.cacheRead === 'number' ? { cacheRead: v.cacheRead } : {}),
      ...(typeof v.cacheWrite === 'number' ? { cacheWrite: v.cacheWrite } : {}),
    };
  }
  return Object.keys(result).length > 0 ? result : undefined;
}

/** Serialize config back to a plain object for writing to openclaw.json */
export function serializeConfig(config: PluginConfig): Record<string, unknown> {
  const out: Record<string, unknown> = {
    traces_endpoint: config.traces_endpoint,
    payload_mode: config.payload_mode,
    enabled: config.enabled,
    batch_delay_ms: config.batch_delay_ms,
    batch_max_size: config.batch_max_size,
    export_timeout_ms: config.export_timeout_ms,
  };

  if (config.logs_endpoint) out.logs_endpoint = config.logs_endpoint;
  if (config.headers) out.headers = config.headers;
  if (config.model_map && Object.keys(config.model_map).length > 0) {
    out.model_map = config.model_map;
  }
  if (config.model_pricing && Object.keys(config.model_pricing).length > 0) {
    out.model_pricing = config.model_pricing;
  }

  return out;
}
