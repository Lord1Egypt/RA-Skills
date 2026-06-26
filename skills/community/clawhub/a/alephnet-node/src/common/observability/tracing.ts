/**
 * Distributed Tracing System
 * 
 * Provides W3C Trace Context compatible distributed tracing for the AlephNet system.
 * Supports:
 * - Trace and span creation
 * - Context propagation
 * - Span attributes and events
 * - Export to various backends
 */

import { generateId } from '../hash';

// ═══════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════

export type SpanKind = 'internal' | 'server' | 'client' | 'producer' | 'consumer';
export type SpanStatus = 'unset' | 'ok' | 'error';

export interface SpanContext {
  traceId: string;
  spanId: string;
  traceFlags: number;
  traceState?: string;
}

export interface SpanEvent {
  name: string;
  timestamp: number;
  attributes?: Record<string, string | number | boolean>;
}

export interface SpanLink {
  context: SpanContext;
  attributes?: Record<string, string | number | boolean>;
}

export interface SpanData {
  name: string;
  context: SpanContext;
  parentSpanId?: string;
  kind: SpanKind;
  startTime: number;
  endTime?: number;
  status: SpanStatus;
  statusMessage?: string;
  attributes: Record<string, string | number | boolean>;
  events: SpanEvent[];
  links: SpanLink[];
}

export interface TraceExporter {
  export(spans: SpanData[]): Promise<void>;
  shutdown(): Promise<void>;
}

// ═══════════════════════════════════════════════════════════════════════════
// SPAN
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Represents a unit of work in a distributed trace
 */
export class Span {
  private data: SpanData;
  private ended: boolean = false;
  private tracer: Tracer;
  
  constructor(
    tracer: Tracer,
    name: string,
    context: SpanContext,
    kind: SpanKind,
    parentSpanId?: string,
    links?: SpanLink[]
  ) {
    this.tracer = tracer;
    this.data = {
      name,
      context,
      parentSpanId,
      kind,
      startTime: Date.now(),
      status: 'unset',
      attributes: {},
      events: [],
      links: links || []
    };
  }
  
  /**
   * Get the span context
   */
  getContext(): SpanContext {
    return { ...this.data.context };
  }
  
  /**
   * Set an attribute on the span
   */
  setAttribute(key: string, value: string | number | boolean): this {
    if (!this.ended) {
      this.data.attributes[key] = value;
    }
    return this;
  }
  
  /**
   * Set multiple attributes
   */
  setAttributes(attributes: Record<string, string | number | boolean>): this {
    if (!this.ended) {
      Object.assign(this.data.attributes, attributes);
    }
    return this;
  }
  
  /**
   * Add an event to the span
   */
  addEvent(name: string, attributes?: Record<string, string | number | boolean>): this {
    if (!this.ended) {
      this.data.events.push({
        name,
        timestamp: Date.now(),
        attributes
      });
    }
    return this;
  }
  
  /**
   * Set the span status
   */
  setStatus(status: SpanStatus, message?: string): this {
    if (!this.ended) {
      this.data.status = status;
      this.data.statusMessage = message;
    }
    return this;
  }
  
  /**
   * Record an exception
   */
  recordException(error: Error): this {
    if (!this.ended) {
      this.addEvent('exception', {
        'exception.type': error.name,
        'exception.message': error.message,
        'exception.stacktrace': error.stack || ''
      });
      this.setStatus('error', error.message);
    }
    return this;
  }
  
  /**
   * Update the span name
   */
  updateName(name: string): this {
    if (!this.ended) {
      this.data.name = name;
    }
    return this;
  }
  
  /**
   * Check if the span is recording
   */
  isRecording(): boolean {
    return !this.ended;
  }
  
  /**
   * End the span
   */
  end(endTime?: number): void {
    if (this.ended) return;
    
    this.data.endTime = endTime || Date.now();
    this.ended = true;
    this.tracer.onSpanEnd(this.data);
  }
  
  /**
   * Get the span data (for exporting)
   */
  getData(): SpanData {
    return { ...this.data };
  }
  
  /**
   * Get duration in milliseconds
   */
  getDuration(): number | undefined {
    if (!this.data.endTime) return undefined;
    return this.data.endTime - this.data.startTime;
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// TRACER
// ═══════════════════════════════════════════════════════════════════════════

export interface TracerOptions {
  serviceName: string;
  serviceVersion?: string;
  exporters?: TraceExporter[];
  sampleRate?: number;
  maxSpansPerTrace?: number;
}

/**
 * Creates and manages spans
 */
export class Tracer {
  private serviceName: string;
  private serviceVersion: string;
  private exporters: TraceExporter[];
  private sampleRate: number;
  private maxSpansPerTrace: number;
  private pendingSpans: SpanData[] = [];
  private flushInterval: NodeJS.Timeout | null = null;
  private spanCounts: Map<string, number> = new Map();
  
  constructor(options: TracerOptions) {
    this.serviceName = options.serviceName;
    this.serviceVersion = options.serviceVersion || '1.0.0';
    this.exporters = options.exporters || [];
    this.sampleRate = options.sampleRate ?? 1.0;
    this.maxSpansPerTrace = options.maxSpansPerTrace ?? 1000;
    
    // Start flush interval
    this.flushInterval = setInterval(() => this.flush(), 5000);
  }
  
  /**
   * Start a new span
   */
  startSpan(
    name: string,
    options?: {
      kind?: SpanKind;
      parent?: SpanContext;
      links?: SpanLink[];
      attributes?: Record<string, string | number | boolean>;
    }
  ): Span {
    const kind = options?.kind ?? 'internal';
    const parent = options?.parent;
    
    // Generate trace ID or inherit from parent
    const traceId = parent?.traceId || this.generateTraceId();
    const spanId = this.generateSpanId();
    
    // Check sampling
    const sampled = this.shouldSample(traceId);
    
    // Check span limit per trace
    const currentCount = this.spanCounts.get(traceId) || 0;
    if (currentCount >= this.maxSpansPerTrace) {
      // Return a no-op span
      return new Span(this, name, { traceId, spanId, traceFlags: 0 }, kind);
    }
    this.spanCounts.set(traceId, currentCount + 1);
    
    const context: SpanContext = {
      traceId,
      spanId,
      traceFlags: sampled ? 1 : 0
    };
    
    const span = new Span(
      this,
      name,
      context,
      kind,
      parent?.spanId,
      options?.links
    );
    
    // Add service attributes
    span.setAttributes({
      'service.name': this.serviceName,
      'service.version': this.serviceVersion
    });
    
    if (options?.attributes) {
      span.setAttributes(options.attributes);
    }
    
    return span;
  }
  
  /**
   * Create a child span from a parent context
   */
  startChildSpan(
    name: string,
    parentContext: SpanContext,
    options?: {
      kind?: SpanKind;
      attributes?: Record<string, string | number | boolean>;
    }
  ): Span {
    return this.startSpan(name, {
      ...options,
      parent: parentContext
    });
  }
  
  /**
   * Execute a function within a span
   */
  async withSpan<T>(
    name: string,
    fn: (span: Span) => Promise<T>,
    options?: {
      kind?: SpanKind;
      parent?: SpanContext;
      attributes?: Record<string, string | number | boolean>;
    }
  ): Promise<T> {
    const span = this.startSpan(name, options);
    try {
      const result = await fn(span);
      span.setStatus('ok');
      return result;
    } catch (error) {
      span.recordException(error as Error);
      throw error;
    } finally {
      span.end();
    }
  }
  
  /**
   * Synchronous version of withSpan
   */
  withSpanSync<T>(
    name: string,
    fn: (span: Span) => T,
    options?: {
      kind?: SpanKind;
      parent?: SpanContext;
      attributes?: Record<string, string | number | boolean>;
    }
  ): T {
    const span = this.startSpan(name, options);
    try {
      const result = fn(span);
      span.setStatus('ok');
      return result;
    } catch (error) {
      span.recordException(error as Error);
      throw error;
    } finally {
      span.end();
    }
  }
  
  /**
   * Called when a span ends
   */
  onSpanEnd(spanData: SpanData): void {
    // Only collect if sampled
    if (spanData.context.traceFlags & 1) {
      this.pendingSpans.push(spanData);
    }
    
    // Flush if we have enough spans
    if (this.pendingSpans.length >= 100) {
      this.flush();
    }
  }
  
  /**
   * Flush pending spans to exporters
   */
  async flush(): Promise<void> {
    if (this.pendingSpans.length === 0) return;
    
    const spansToExport = [...this.pendingSpans];
    this.pendingSpans = [];
    
    await Promise.all(
      this.exporters.map(exporter => 
        exporter.export(spansToExport).catch(err => {
          console.error('Failed to export spans:', err);
        })
      )
    );
  }
  
  /**
   * Shutdown the tracer
   */
  async shutdown(): Promise<void> {
    if (this.flushInterval) {
      clearInterval(this.flushInterval);
      this.flushInterval = null;
    }
    
    await this.flush();
    
    await Promise.all(
      this.exporters.map(exporter => exporter.shutdown())
    );
  }
  
  /**
   * Add an exporter
   */
  addExporter(exporter: TraceExporter): void {
    this.exporters.push(exporter);
  }
  
  private generateTraceId(): string {
    return generateId('trace');
  }
  
  private generateSpanId(): string {
    return generateId('span').substring(0, 16);
  }
  
  private shouldSample(traceId: string): boolean {
    if (this.sampleRate >= 1.0) return true;
    if (this.sampleRate <= 0) return false;
    
    // Deterministic sampling based on trace ID
    const hash = traceId.split('').reduce((acc, char) => {
      return ((acc << 5) - acc) + char.charCodeAt(0);
    }, 0);
    
    return (Math.abs(hash) % 100) < (this.sampleRate * 100);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// CONTEXT PROPAGATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * W3C Trace Context header names
 */
export const TRACE_PARENT_HEADER = 'traceparent';
export const TRACE_STATE_HEADER = 'tracestate';

/**
 * Parse W3C traceparent header
 */
export function parseTraceparent(header: string): SpanContext | null {
  // Format: 00-{trace-id}-{parent-id}-{trace-flags}
  const match = header.match(/^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$/);
  if (!match) return null;
  
  return {
    traceId: match[1],
    spanId: match[2],
    traceFlags: parseInt(match[3], 16)
  };
}

/**
 * Format SpanContext as W3C traceparent header
 */
export function formatTraceparent(context: SpanContext): string {
  const traceFlags = context.traceFlags.toString(16).padStart(2, '0');
  return `00-${context.traceId}-${context.spanId}-${traceFlags}`;
}

/**
 * Extract trace context from HTTP headers
 */
export function extractTraceContext(headers: Record<string, string | undefined>): SpanContext | null {
  const traceparent = headers[TRACE_PARENT_HEADER] || headers['Traceparent'];
  if (!traceparent) return null;
  
  const context = parseTraceparent(traceparent);
  if (!context) return null;
  
  context.traceState = headers[TRACE_STATE_HEADER] || headers['Tracestate'];
  return context;
}

/**
 * Inject trace context into HTTP headers
 */
export function injectTraceContext(
  context: SpanContext,
  headers: Record<string, string>
): Record<string, string> {
  headers[TRACE_PARENT_HEADER] = formatTraceparent(context);
  if (context.traceState) {
    headers[TRACE_STATE_HEADER] = context.traceState;
  }
  return headers;
}

// ═══════════════════════════════════════════════════════════════════════════
// EXPORTERS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Console exporter for development
 */
export class ConsoleTraceExporter implements TraceExporter {
  async export(spans: SpanData[]): Promise<void> {
    for (const span of spans) {
      const duration = span.endTime ? span.endTime - span.startTime : 0;
      console.log(
        `[TRACE] ${span.name} ` +
        `trace=${span.context.traceId.substring(0, 8)} ` +
        `span=${span.context.spanId.substring(0, 8)} ` +
        `duration=${duration}ms ` +
        `status=${span.status}`
      );
    }
  }
  
  async shutdown(): Promise<void> {
    // No-op
  }
}

/**
 * Memory exporter for testing
 */
export class MemoryTraceExporter implements TraceExporter {
  private spans: SpanData[] = [];
  
  async export(spans: SpanData[]): Promise<void> {
    this.spans.push(...spans);
  }
  
  async shutdown(): Promise<void> {
    // No-op
  }
  
  getSpans(): SpanData[] {
    return [...this.spans];
  }
  
  getSpansByTrace(traceId: string): SpanData[] {
    return this.spans.filter(s => s.context.traceId === traceId);
  }
  
  getSpanByName(name: string): SpanData | undefined {
    return this.spans.find(s => s.name === name);
  }
  
  clear(): void {
    this.spans = [];
  }
}

/**
 * OTLP-compatible JSON exporter (for Jaeger, Zipkin, etc.)
 */
export class OTLPJsonExporter implements TraceExporter {
  private endpoint: string;
  private headers: Record<string, string>;
  
  constructor(endpoint: string, headers?: Record<string, string>) {
    this.endpoint = endpoint;
    this.headers = headers || {};
  }
  
  async export(spans: SpanData[]): Promise<void> {
    const payload = {
      resourceSpans: [{
        resource: {
          attributes: []
        },
        scopeSpans: [{
          scope: {
            name: 'alephnet-tracer',
            version: '1.0.0'
          },
          spans: spans.map(this.convertSpan)
        }]
      }]
    };
    
    try {
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...this.headers
        },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        throw new Error(`OTLP export failed: ${response.status}`);
      }
    } catch (error) {
      console.error('Failed to export to OTLP endpoint:', error);
    }
  }
  
  async shutdown(): Promise<void> {
    // No-op
  }
  
  private convertSpan(span: SpanData): object {
    return {
      traceId: span.context.traceId,
      spanId: span.context.spanId,
      parentSpanId: span.parentSpanId,
      name: span.name,
      kind: span.kind === 'internal' ? 1 : span.kind === 'server' ? 2 : span.kind === 'client' ? 3 : 1,
      startTimeUnixNano: span.startTime * 1e6,
      endTimeUnixNano: (span.endTime || span.startTime) * 1e6,
      attributes: Object.entries(span.attributes).map(([key, value]) => ({
        key,
        value: { stringValue: String(value) }
      })),
      events: span.events.map(e => ({
        name: e.name,
        timeUnixNano: e.timestamp * 1e6,
        attributes: Object.entries(e.attributes || {}).map(([key, value]) => ({
          key,
          value: { stringValue: String(value) }
        }))
      })),
      status: {
        code: span.status === 'ok' ? 1 : span.status === 'error' ? 2 : 0,
        message: span.statusMessage
      }
    };
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// GLOBAL TRACER
// ═══════════════════════════════════════════════════════════════════════════

let globalTracer: Tracer | null = null;

/**
 * Initialize the global tracer
 */
export function initTracer(options: TracerOptions): Tracer {
  globalTracer = new Tracer(options);
  return globalTracer;
}

/**
 * Get the global tracer
 */
export function getTracer(): Tracer {
  if (!globalTracer) {
    globalTracer = new Tracer({
      serviceName: 'alephnet',
      exporters: []
    });
  }
  return globalTracer;
}

/**
 * Convenience function to start a span
 */
export function startSpan(
  name: string,
  options?: {
    kind?: SpanKind;
    parent?: SpanContext;
    attributes?: Record<string, string | number | boolean>;
  }
): Span {
  return getTracer().startSpan(name, options);
}

/**
 * Convenience function to execute with a span
 */
export async function withSpan<T>(
  name: string,
  fn: (span: Span) => Promise<T>,
  options?: {
    kind?: SpanKind;
    parent?: SpanContext;
    attributes?: Record<string, string | number | boolean>;
  }
): Promise<T> {
  return getTracer().withSpan(name, fn, options);
}
