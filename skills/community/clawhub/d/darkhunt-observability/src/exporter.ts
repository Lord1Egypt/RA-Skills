import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import type { PluginConfig } from './types.js';

const LOG_PREFIX = '[tracehub-telemetry]';

export class TraceHubExporter {
  private exporter: OTLPTraceExporter;
  private batch: ReadableSpan[] = [];
  private flushTimer: ReturnType<typeof setTimeout> | null = null;
  private maxSize: number;
  private delayMs: number;
  private debug: boolean;
  private spansSent = 0;
  private exportErrors = 0;

  constructor(config: PluginConfig, debug = false) {
    this.debug = debug;

    if (this.debug) {
      console.log(`${LOG_PREFIX} initializing exporter`);
      console.log(`${LOG_PREFIX}   url: ${config.traces_endpoint}`);
      console.log(`${LOG_PREFIX}   timeout: ${config.export_timeout_ms}ms`);
      console.log(`${LOG_PREFIX}   headers: ${config.headers ? Object.keys(config.headers).join(', ') : 'none'}`);
      console.log(`${LOG_PREFIX}   batch: ${config.batch_max_size} max, ${config.batch_delay_ms}ms delay`);
    }

    this.exporter = new OTLPTraceExporter({
      url: config.traces_endpoint,
      timeoutMillis: config.export_timeout_ms,
      headers: config.headers,
    });

    this.maxSize = config.batch_max_size;
    this.delayMs = config.batch_delay_ms;
  }

  enqueue(spans: ReadableSpan[]): void {
    this.batch.push(...spans);

    if (this.debug) {
      const names = spans.map(s => s.name).join(', ');
      console.log(`${LOG_PREFIX} enqueued ${spans.length} span(s): [${names}] (batch: ${this.batch.length}/${this.maxSize})`);
    }

    if (this.batch.length >= this.maxSize) {
      this.flush();
      return;
    }

    if (!this.flushTimer) {
      this.flushTimer = setTimeout(() => this.flush(), this.delayMs);
    }
  }

  flush(): void {
    if (this.flushTimer) {
      clearTimeout(this.flushTimer);
      this.flushTimer = null;
    }

    if (this.batch.length === 0) return;

    const toExport = this.batch;
    this.batch = [];

    if (this.debug) {
      console.log(`${LOG_PREFIX} flushing ${toExport.length} span(s) to endpoint...`);
    }

    this.exporter.export(toExport, (result) => {
      if (result.error) {
        this.exportErrors++;
        console.error(`${LOG_PREFIX} export FAILED (${this.exportErrors} total errors): ${result.error.message}`);
        if (result.error.stack) {
          console.error(`${LOG_PREFIX} stack:`, result.error.stack);
        }
      } else {
        this.spansSent += toExport.length;
        console.log(`${LOG_PREFIX} export OK — ${toExport.length} span(s) sent (${this.spansSent} total)`);
      }
    });
  }

  getStats(): { spansSent: number; exportErrors: number; batchPending: number } {
    return {
      spansSent: this.spansSent,
      exportErrors: this.exportErrors,
      batchPending: this.batch.length,
    };
  }

  async shutdown(): Promise<void> {
    this.flush();
    try {
      await this.exporter.shutdown();
    } catch (err) {
      console.error(`${LOG_PREFIX} shutdown error:`, (err as Error).message);
    }
  }
}
