import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-proto';
import { LogRecord as SdkLogRecord } from '@opentelemetry/sdk-logs';
import type { PluginConfig } from './types.js';

const LOG_PREFIX = '[tracehub-logs]';

export class LogHubExporter {
  private exporter: OTLPLogExporter;
  private batch: SdkLogRecord[] = [];
  private flushTimer: ReturnType<typeof setTimeout> | null = null;
  private maxSize: number;
  private delayMs: number;
  private debug: boolean;
  private logsSent = 0;
  private exportErrors = 0;

  constructor(config: PluginConfig, debug = false) {
    this.debug = debug;

    if (this.debug) {
      console.log(`${LOG_PREFIX} initializing log exporter`);
      console.log(`${LOG_PREFIX}   url: ${config.logs_endpoint}`);
      console.log(`${LOG_PREFIX}   timeout: ${config.export_timeout_ms}ms`);
      console.log(`${LOG_PREFIX}   headers: ${config.headers ? Object.keys(config.headers).join(', ') : 'none'}`);
      console.log(`${LOG_PREFIX}   batch: ${config.batch_max_size} max, ${config.batch_delay_ms}ms delay`);
    }

    this.exporter = new OTLPLogExporter({
      url: config.logs_endpoint,
      timeoutMillis: config.export_timeout_ms,
      headers: config.headers,
    });

    this.maxSize = config.batch_max_size;
    this.delayMs = config.batch_delay_ms;
  }

  enqueue(records: SdkLogRecord[]): void {
    this.batch.push(...records);

    if (this.debug) {
      console.log(`${LOG_PREFIX} enqueued ${records.length} log record(s) (batch: ${this.batch.length}/${this.maxSize})`);
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
      console.log(`${LOG_PREFIX} flushing ${toExport.length} log record(s) to endpoint...`);
    }

    this.exporter.export(toExport, (result) => {
      if (result.error) {
        this.exportErrors++;
        console.error(`${LOG_PREFIX} export FAILED (${this.exportErrors} total errors): ${result.error.message}`);
        if (result.error.stack) {
          console.error(`${LOG_PREFIX} stack:`, result.error.stack);
        }
      } else {
        this.logsSent += toExport.length;
        console.log(`${LOG_PREFIX} export OK — ${toExport.length} log record(s) sent (${this.logsSent} total)`);
      }
    });
  }

  getStats(): { logsSent: number; exportErrors: number; batchPending: number } {
    return {
      logsSent: this.logsSent,
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
