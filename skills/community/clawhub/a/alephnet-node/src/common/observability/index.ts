/**
 * Observability Module
 * 
 * Exports metrics and tracing functionality for the AlephNet system.
 */

// Metrics
export {
  // Types
  MetricLabels,
  MetricOptions,
  HistogramOptions,
  MetricValue,
  HistogramValue,
  MetricType,
  
  // Classes
  Counter,
  Gauge,
  Histogram,
  Summary,
  MetricsRegistry,
  
  // Constants
  DEFAULT_LATENCY_BUCKETS,
  
  // Functions
  getMetrics,
  createCounter,
  createGauge,
  createHistogram,
  
  // AlephNet-specific metrics
  alephMetrics
} from './metrics';

// Tracing
export {
  // Types
  SpanKind,
  SpanStatus,
  SpanContext,
  SpanEvent,
  SpanLink,
  SpanData,
  TraceExporter,
  TracerOptions,
  
  // Classes
  Span,
  Tracer,
  ConsoleTraceExporter,
  MemoryTraceExporter,
  OTLPJsonExporter,
  
  // Constants
  TRACE_PARENT_HEADER,
  TRACE_STATE_HEADER,
  
  // Context propagation
  parseTraceparent,
  formatTraceparent,
  extractTraceContext,
  injectTraceContext,
  
  // Global tracer
  initTracer,
  getTracer,
  startSpan,
  withSpan
} from './tracing';
