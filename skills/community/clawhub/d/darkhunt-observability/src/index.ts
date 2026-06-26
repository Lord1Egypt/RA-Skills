import { validate } from './config.js';
import { buildResource } from './resource.js';
import { SpanBuffer } from './span-buffer.js';
import { TraceHubExporter } from './exporter.js';
import { registerHooks, registerDiscoveryHooks, resolveSessionKey } from './hooks-adapter.js';
import { registerTracehubCli } from './cli.js';
import { LogHubExporter } from './log-exporter.js';
import { registerLogHooks } from './log-hooks.js';
import type { OpenClawPluginApi } from './hooks-adapter.js';

export default {
  id: 'darkhunt-observability',
  name: 'Darkhunt Observability',
  description: 'Exports OTel trace spans and logs to Trace Hub via OTLP/protobuf',

  configSchema: {
    jsonSchema: {
      type: 'object',
      properties: {
        traces_endpoint: { type: 'string', description: 'Full OTLP traces URL' },
        logs_endpoint: { type: 'string', description: 'Full OTLP logs URL' },
        headers: { type: 'object', additionalProperties: { type: 'string' } },
        authorization: { type: 'string' },
        workspace_id: { type: 'string' },
        application_id: { type: 'string' },
        payload_mode: { type: 'string', enum: ['metadata', 'debug', 'full'], default: 'metadata' },
        batch_delay_ms: { type: 'number', default: 2000 },
        batch_max_size: { type: 'number', default: 50 },
        export_timeout_ms: { type: 'number', default: 30000 },
        enabled: { type: 'boolean', default: true },
        model_map: { type: 'object', additionalProperties: { type: 'string' }, description: 'Map Bedrock ARN patterns to friendly model names for pricing' },
        model_pricing: { type: 'object', description: 'Override per-model pricing (per 1M tokens). Keys: model names, values: {input, output, cacheRead?, cacheWrite?}' },
      },
      required: [],
    },
    uiHints: {
      traces_endpoint: { label: 'Traces Endpoint', placeholder: 'https://api.example.com/trace-hub/otlp/t/{tenantId}/v1/traces' },
      logs_endpoint: { label: 'Logs Endpoint', placeholder: 'https://api.example.com/trace-hub/otlp/t/{tenantId}/v1/logs' },
      authorization: { label: 'Authorization', sensitive: true, placeholder: 'Bearer <token>' },
      workspace_id: { label: 'Workspace ID', placeholder: 'a0000000-0000-0000-0000-000000000003' },
      application_id: { label: 'Application ID', placeholder: 'c34512ba-cbe0-4c55-875e-469425d5d895' },
      payload_mode: { label: 'Payload Mode', help: 'metadata=structural only, debug=truncated content, full=everything (recommended)' },
      batch_delay_ms: { label: 'Batch Delay (ms)', advanced: true },
      batch_max_size: { label: 'Batch Max Size', advanced: true },
      export_timeout_ms: { label: 'Export Timeout (ms)', advanced: true },
      model_map: { label: 'Model Map', advanced: true, help: 'Map Bedrock inference profile IDs or ARN substrings to model names (e.g. {"ekadx6q1kayx": "claude-sonnet-4-6"})' },
      model_pricing: { label: 'Model Pricing', advanced: true, help: 'Override pricing per 1M tokens (e.g. {"claude-sonnet-4-6": {"input": 3.00, "output": 15.00}})' },
    },
  },

  hooks: [
    'message_received', 'before_agent_start', 'agent_end',
    'llm_input', 'llm_output', 'before_tool_call', 'after_tool_call',
    'shutdown',
  ],

  register(api: OpenClawPluginApi) {
    // Register CLI commands (always, even if plugin disabled)
    if (api.registerCli) {
      api.registerCli(
        ({ program, config, logger }: any) => {
          registerTracehubCli({ program, config, logger });
        },
        { commands: ['tracehub'] },
      );
    }

    const rawConfig = api.pluginConfig ?? {};

    // If no traces_endpoint configured, skip telemetry but keep CLI available
    if (!(rawConfig as any).traces_endpoint) {
      if (api.logger) {
        api.logger.info('[tracehub-telemetry] No traces_endpoint configured. Run "openclaw tracehub setup" to configure.');
      }
      return;
    }

    const config = validate(rawConfig);
    if (!config.enabled) return;

    const debug = config.debug === true || process.env.TRACEHUB_DEBUG === '1';

    const resource = buildResource(
      api.version,
      api.processOwner,
      process.env.DEPLOYMENT_ENVIRONMENT ?? process.env.NODE_ENV,
      (rawConfig as any).workspace_id,
      (rawConfig as any).application_id,
      rawConfig as Record<string, unknown>,
    );

    const exporter = new TraceHubExporter(config, debug);
    const buffer = new SpanBuffer(resource, config.payload_mode, (spans) =>
      exporter.enqueue(spans),
    );

    if (debug && api.logger) {
      api.logger.info('[tracehub-telemetry] Debug mode enabled (TRACEHUB_DEBUG=1)');
      api.logger.info(`[tracehub-telemetry] Exporting to: ${config.traces_endpoint}`);
    }

    registerHooks(api, buffer, undefined, config.model_map, config.model_pricing);

    // Discovery hooks disabled — session_start/session_end/message_sent arrive
    // as empty shells after OTLP mapping (wrong sessionId, userId="node", no metadata).
    // Re-enable when trace-hub can map their attributes into the schema.

    // ── Log export (OTLP logs endpoint) ──────────────────────────
    let logExporter: LogHubExporter | undefined;
    if (config.logs_endpoint) {
      logExporter = new LogHubExporter(config, debug);
      registerLogHooks(api, logExporter, config.payload_mode, resource, config.model_map, config.model_pricing);
      if (api.logger) {
        api.logger.info(`[tracehub-logs] Log export enabled`);
      }
    }

    // Tap into runtime event streams for deeper visibility
    registerRuntimeEvents(api, buffer, debug);

    // Debug: discover ALL events OpenClaw emits (not just the ones we handle)
    if (debug && api.logger) {
      registerEventDiscovery(api);
    }

    const staleInterval = setInterval(() => buffer.flushStale(5 * 60 * 1000), 60_000);
    if (staleInterval.unref) staleInterval.unref();

    api.on('shutdown', async () => {
      clearInterval(staleInterval);
      buffer.flushStale(0);
      await exporter.shutdown();
      if (logExporter) {
        await logExporter.shutdown();
      }
    });
  },
};

// ── Runtime event streams ───────────────────────────────────────

function registerRuntimeEvents(api: OpenClawPluginApi, buffer: SpanBuffer, debug: boolean): void {
  const rt = (api as any).runtime;
  if (!rt?.events) return;

  const log = api.logger;

  // onAgentEvent — fires for every agent lifecycle event
  if (typeof rt.events.onAgentEvent === 'function') {
    try {
      rt.events.onAgentEvent((event: any) => {
        if (debug && log) {
          const type = event?.stream ?? 'unknown';
          const phase = event?.data?.phase ?? event?.data?.delta?.slice(0, 20) ?? '';
          log.info(`[tracehub:agent-event] stream=${type} phase=${phase} seq=${event?.seq}`);
        }

        // Feed structured events into the span buffer
        if (event?.runId && event?.stream) {
          buffer.onRuntimeEvent({
            runId: event.runId,
            stream: event.stream,
            data: event.data,
            sessionKey: resolveSessionKey(event.sessionKey ?? ''),
            ts: event.ts ?? Date.now(),
          });
        }
      });
      if (log) log.info('[tracehub] Registered runtime.events.onAgentEvent callback');
    } catch (err: any) {
      if (log) log.error(`[tracehub] Failed to register onAgentEvent: ${err.message}`);
    }
  }

  // onSessionTranscriptUpdate — fires when session transcript changes
  if (typeof rt.events.onSessionTranscriptUpdate === 'function') {
    try {
      rt.events.onSessionTranscriptUpdate((event: any) => {
        if (debug && log) {
          const keys = Object.keys(event ?? {}).join(', ');
          log.info(`[tracehub:transcript] keys=${keys}`);
          log.info(`[tracehub:transcript] payload=${JSON.stringify(event)?.slice(0, 1500)}`);
        }

        // Emit transcript update as a discovery span with structural metadata
        try {
          const resolved = event ? { ...event, sessionKey: resolveSessionKey(event.sessionKey ?? '') } : {};
          buffer.onTranscriptUpdate(resolved);
        } catch (err: any) {
          if (log) log.error(`[tracehub:transcript] Error processing update: ${err.message}`);
        }
      });
      if (log) log.info('[tracehub] Registered runtime.events.onSessionTranscriptUpdate callback');
    } catch (err: any) {
      if (log) log.error(`[tracehub] Failed to register onSessionTranscriptUpdate: ${err.message}`);
    }
  }
}

// ── Event discovery (debug mode only) ──────────────────────────

const KNOWN_HOOKS = new Set([
  'message_received', 'before_agent_start', 'agent_end',
  'llm_input', 'llm_output', 'before_tool_call', 'after_tool_call',
  'shutdown',
]);

function registerEventDiscovery(api: OpenClawPluginApi): void {
  const log = api.logger!;
  const seen = new Set<string>();

  // Try wildcard/catch-all patterns that EventEmitter-like systems support
  const wildcards = ['*', '**', 'all'];
  for (const w of wildcards) {
    try {
      api.on(w, (evt: any, ctx: any) => {
        const eventName = evt?._event ?? evt?.event ?? evt?.type ?? w;
        if (!seen.has(eventName)) {
          seen.add(eventName);
          log.info(`[tracehub:discovery] NEW EVENT via ${w}: "${eventName}"`);
        }
        if (!KNOWN_HOOKS.has(eventName)) {
          log.info(`[tracehub:discovery] UNKNOWN EVENT: "${eventName}" evt_keys=${Object.keys(evt ?? {}).join(',')} ctx_keys=${Object.keys(ctx ?? {}).join(',')}`);
          log.info(`[tracehub:discovery] evt=${JSON.stringify(evt)?.slice(0, 500)}`);
        }
      });
      log.info(`[tracehub:discovery] Registered wildcard listener: "${w}"`);
    } catch {
      // Wildcard not supported
    }
  }

  // Register listeners for suspected events we haven't seen
  const suspects = [
    'agent_start', 'agent_error',
    'tool_call', 'tool_result', 'tool_error',
    'media_received', 'media_processed', 'image_received',
    'message_sent', 'message_delivered', 'message_error',
    'session_start', 'session_end', 'session_created',
    'cron_start', 'cron_end', 'cron_trigger',
    'memory_search', 'memory_result',
    'subagent_start', 'subagent_end',
    'before_message_send', 'after_message_send',
    'before_session_start', 'after_session_start',
    'before_cron_run', 'after_cron_run',
    'image_upload', 'file_upload', 'media_upload',
    'notebooklm_query', 'external_service_call',
  ];

  for (const name of suspects) {
    try {
      api.on(name, (evt: any, ctx: any) => {
        log.info(`[tracehub:discovery] ★ FOUND: "${name}"`);
        log.info(`[tracehub:discovery]   evt_keys: ${Object.keys(evt ?? {}).join(', ')}`);
        log.info(`[tracehub:discovery]   ctx_keys: ${Object.keys(ctx ?? {}).join(', ')}`);
        log.info(`[tracehub:discovery]   evt: ${JSON.stringify(evt)?.slice(0, 800)}`);
        log.info(`[tracehub:discovery]   ctx: ${JSON.stringify(ctx)?.slice(0, 800)}`);
      });
    } catch {
      // Event name not supported
    }
  }

  log.info(`[tracehub:discovery] Registered ${suspects.length} suspect event listeners`);

  // Introspect the api object
  const apiObj = api as any;
  try {
    // Log all api methods/properties
    const allKeys = new Set<string>();
    let obj = apiObj;
    while (obj && obj !== Object.prototype) {
      Object.getOwnPropertyNames(obj).forEach((k: string) => allKeys.add(k));
      obj = Object.getPrototypeOf(obj);
    }
    log.info(`[tracehub:discovery] api all props: ${[...allKeys].join(', ')}`);
  } catch (err: any) {
    log.info(`[tracehub:discovery] introspection error: ${err.message}`);
  }

  // ── Deep introspect: runtime ──────────────────────────────────
  try {
    const rt = apiObj.runtime;
    if (rt) {
      log.info(`[tracehub:discovery] runtime type: ${typeof rt}`);
      const rtKeys = new Set<string>();
      let obj = rt;
      while (obj && obj !== Object.prototype) {
        Object.getOwnPropertyNames(obj).forEach((k: string) => rtKeys.add(k));
        obj = Object.getPrototypeOf(obj);
      }
      log.info(`[tracehub:discovery] runtime all props: ${[...rtKeys].join(', ')}`);

      // Inspect each runtime property type/value
      for (const k of rtKeys) {
        try {
          const val = rt[k];
          const t = typeof val;
          if (t === 'function') {
            log.info(`[tracehub:discovery] runtime.${k}: function(${val.length} args)`);
          } else if (t === 'object' && val !== null) {
            const subKeys = Object.keys(val).slice(0, 20);
            log.info(`[tracehub:discovery] runtime.${k}: object { ${subKeys.join(', ')} }`);
            // Go one level deeper for interesting objects
            if (subKeys.length > 0 && subKeys.length < 15) {
              for (const sk of subKeys) {
                const sv = val[sk];
                if (typeof sv === 'function') {
                  log.info(`[tracehub:discovery]   runtime.${k}.${sk}: function(${sv.length} args)`);
                } else if (typeof sv === 'object' && sv !== null) {
                  log.info(`[tracehub:discovery]   runtime.${k}.${sk}: object { ${Object.keys(sv).slice(0, 10).join(', ')} }`);
                } else {
                  log.info(`[tracehub:discovery]   runtime.${k}.${sk}: ${t} = ${JSON.stringify(sv)?.slice(0, 200)}`);
                }
              }
            }
          } else if (t === 'string' || t === 'number' || t === 'boolean') {
            log.info(`[tracehub:discovery] runtime.${k}: ${t} = ${JSON.stringify(val)?.slice(0, 200)}`);
          }
        } catch (e: any) {
          log.info(`[tracehub:discovery] runtime.${k}: error reading — ${e.message}`);
        }
      }
    } else {
      log.info(`[tracehub:discovery] runtime: not available`);
    }
  } catch (err: any) {
    log.info(`[tracehub:discovery] runtime introspection error: ${err.message}`);
  }

  // ── Deep introspect: registerHook ─────────────────────────────
  try {
    if (typeof apiObj.registerHook === 'function') {
      log.info(`[tracehub:discovery] registerHook: function(${apiObj.registerHook.length} args)`);
      log.info(`[tracehub:discovery] registerHook.toString(): ${apiObj.registerHook.toString().slice(0, 500)}`);
    }
  } catch (err: any) {
    log.info(`[tracehub:discovery] registerHook introspection error: ${err.message}`);
  }

  // ── Deep introspect: registerTool ─────────────────────────────
  try {
    if (typeof apiObj.registerTool === 'function') {
      log.info(`[tracehub:discovery] registerTool: function(${apiObj.registerTool.length} args)`);
      log.info(`[tracehub:discovery] registerTool.toString(): ${apiObj.registerTool.toString().slice(0, 500)}`);
    }
  } catch (err: any) {
    log.info(`[tracehub:discovery] registerTool introspection error: ${err.message}`);
  }

  // ── Deep introspect: on (event system) ────────────────────────
  try {
    log.info(`[tracehub:discovery] on: function(${apiObj.on.length} args)`);
    log.info(`[tracehub:discovery] on.toString(): ${apiObj.on.toString().slice(0, 500)}`);
  } catch (err: any) {
    log.info(`[tracehub:discovery] on introspection error: ${err.message}`);
  }

  // ── Introspect: config object ─────────────────────────────────
  try {
    if (apiObj.config && typeof apiObj.config === 'object') {
      log.info(`[tracehub:discovery] config keys: ${Object.keys(apiObj.config).slice(0, 30).join(', ')}`);
    }
  } catch (err: any) {
    log.info(`[tracehub:discovery] config introspection error: ${err.message}`);
  }

  // ── Introspect: source ────────────────────────────────────────
  try {
    if (apiObj.source) {
      log.info(`[tracehub:discovery] source type: ${typeof apiObj.source}`);
      if (typeof apiObj.source === 'object') {
        log.info(`[tracehub:discovery] source keys: ${Object.keys(apiObj.source).slice(0, 20).join(', ')}`);
      } else {
        log.info(`[tracehub:discovery] source: ${JSON.stringify(apiObj.source)?.slice(0, 200)}`);
      }
    }
  } catch (err: any) {
    log.info(`[tracehub:discovery] source introspection error: ${err.message}`);
  }
}
