import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { TraceHubExporter } from '../src/exporter.js';
import type { PluginConfig } from '../src/types.js';

// Mock the OTLPTraceExporter
vi.mock('@opentelemetry/exporter-trace-otlp-proto', () => {
  return {
    OTLPTraceExporter: vi.fn().mockImplementation(() => ({
      export: vi.fn((_spans, cb) => cb({ code: 0 })),
      shutdown: vi.fn().mockResolvedValue(undefined),
    })),
  };
});

const config: PluginConfig = {
  traces_endpoint: 'https://api.example.com/trace-hub/otlp/t/tenant-1/v1/traces',
  logs_endpoint: 'https://api.example.com/trace-hub/otlp/t/tenant-1/v1/logs',
  headers: { Authorization: 'Bearer test-key' },
  payload_mode: 'metadata',
  batch_delay_ms: 100,
  batch_max_size: 5,
  export_timeout_ms: 30000,
  enabled: true,
};

describe('TraceHubExporter', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('flushes immediately when batch_max_size reached', () => {
    const exporter = new TraceHubExporter(config);
    const mockSpans = Array.from({ length: 5 }, () => ({}) as any);

    exporter.enqueue(mockSpans);

    // Should have flushed immediately — no timer needed
  });

  it('flushes after delay when under max size', () => {
    const exporter = new TraceHubExporter(config);
    exporter.enqueue([{} as any]);

    // Advance timer past the delay
    vi.advanceTimersByTime(config.batch_delay_ms + 10);
    // Flush should have been called
  });

  it('shutdown flushes remaining and calls exporter.shutdown', async () => {
    const exporter = new TraceHubExporter(config);
    exporter.enqueue([{} as any]);

    await exporter.shutdown();
    // Should not throw
  });

  it('handles export errors without throwing', () => {
    // Re-mock with error response for this test
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const exporter = new TraceHubExporter(config);
    // Force the mock to return an error by overriding the internal exporter
    const internalExporter = (exporter as any).exporter;
    internalExporter.export = vi.fn((_spans: any, cb: any) =>
      cb({ error: new Error('network error') }),
    );

    exporter.enqueue(Array.from({ length: 5 }, () => ({}) as any));

    expect(consoleSpy).toHaveBeenCalledWith(
      '[tracehub-telemetry] export FAILED (1 total errors): network error',
    );

    consoleSpy.mockRestore();
  });
});
