/**
 * Metrics Collection System
 * 
 * Provides comprehensive metrics collection for the AlephNet system including:
 * - Counters: Monotonically increasing values (e.g., request count)
 * - Gauges: Point-in-time values (e.g., active connections)
 * - Histograms: Distribution of values (e.g., request latency)
 * - Timers: Duration measurements
 * 
 * Supports multiple backends: memory, Prometheus-compatible export
 */

// ═══════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════

export interface MetricLabels {
  [key: string]: string;
}

export interface MetricOptions {
  name: string;
  help: string;
  labels?: string[];
}

export interface HistogramOptions extends MetricOptions {
  buckets?: number[];
}

export interface MetricValue {
  value: number;
  timestamp: number;
  labels: MetricLabels;
}

export interface HistogramValue {
  count: number;
  sum: number;
  buckets: Map<number, number>;
  labels: MetricLabels;
}

// ═══════════════════════════════════════════════════════════════════════════
// COUNTER
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Counter: A monotonically increasing value.
 * Use for: request counts, error counts, events processed
 */
export class Counter {
  private values: Map<string, MetricValue> = new Map();
  
  constructor(public readonly options: MetricOptions) {}
  
  /**
   * Increment the counter by 1 or a specified amount
   */
  inc(labels: MetricLabels = {}, value: number = 1): void {
    if (value < 0) {
      throw new Error('Counter cannot be decreased');
    }
    const key = this.labelsToKey(labels);
    const existing = this.values.get(key);
    
    if (existing) {
      existing.value += value;
      existing.timestamp = Date.now();
    } else {
      this.values.set(key, {
        value,
        timestamp: Date.now(),
        labels
      });
    }
  }
  
  /**
   * Get current value for labels
   */
  get(labels: MetricLabels = {}): number {
    const key = this.labelsToKey(labels);
    return this.values.get(key)?.value ?? 0;
  }
  
  /**
   * Get all values
   */
  getAll(): MetricValue[] {
    return Array.from(this.values.values());
  }
  
  /**
   * Reset counter (for testing)
   */
  reset(): void {
    this.values.clear();
  }
  
  private labelsToKey(labels: MetricLabels): string {
    return Object.entries(labels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}="${v}"`)
      .join(',');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// GAUGE
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Gauge: A value that can increase or decrease.
 * Use for: active connections, queue size, memory usage
 */
export class Gauge {
  private values: Map<string, MetricValue> = new Map();
  
  constructor(public readonly options: MetricOptions) {}
  
  /**
   * Set the gauge to a specific value
   */
  set(labels: MetricLabels, value: number): void;
  set(value: number): void;
  set(labelsOrValue: MetricLabels | number, maybeValue?: number): void {
    const labels = typeof labelsOrValue === 'number' ? {} : labelsOrValue;
    const value = typeof labelsOrValue === 'number' ? labelsOrValue : maybeValue!;
    
    const key = this.labelsToKey(labels);
    this.values.set(key, {
      value,
      timestamp: Date.now(),
      labels
    });
  }
  
  /**
   * Increment the gauge
   */
  inc(labels: MetricLabels = {}, value: number = 1): void {
    const key = this.labelsToKey(labels);
    const existing = this.values.get(key);
    
    if (existing) {
      existing.value += value;
      existing.timestamp = Date.now();
    } else {
      this.set(labels, value);
    }
  }
  
  /**
   * Decrement the gauge
   */
  dec(labels: MetricLabels = {}, value: number = 1): void {
    this.inc(labels, -value);
  }
  
  /**
   * Get current value for labels
   */
  get(labels: MetricLabels = {}): number {
    const key = this.labelsToKey(labels);
    return this.values.get(key)?.value ?? 0;
  }
  
  /**
   * Get all values
   */
  getAll(): MetricValue[] {
    return Array.from(this.values.values());
  }
  
  /**
   * Reset gauge (for testing)
   */
  reset(): void {
    this.values.clear();
  }
  
  /**
   * Set to current time (useful for last_updated metrics)
   */
  setToCurrentTime(labels: MetricLabels = {}): void {
    this.set(labels, Date.now());
  }
  
  private labelsToKey(labels: MetricLabels): string {
    return Object.entries(labels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}="${v}"`)
      .join(',');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// HISTOGRAM
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Default bucket boundaries for latency histograms (in ms)
 */
export const DEFAULT_LATENCY_BUCKETS = [
  0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10
];

/**
 * Histogram: Tracks the distribution of observed values.
 * Use for: request latency, response sizes
 */
export class Histogram {
  private values: Map<string, HistogramValue> = new Map();
  public readonly buckets: number[];
  
  constructor(public readonly options: HistogramOptions) {
    this.buckets = options.buckets || DEFAULT_LATENCY_BUCKETS;
    this.buckets.sort((a, b) => a - b);
  }
  
  /**
   * Observe a value
   */
  observe(labels: MetricLabels, value: number): void;
  observe(value: number): void;
  observe(labelsOrValue: MetricLabels | number, maybeValue?: number): void {
    const labels = typeof labelsOrValue === 'number' ? {} : labelsOrValue;
    const value = typeof labelsOrValue === 'number' ? labelsOrValue : maybeValue!;
    
    const key = this.labelsToKey(labels);
    let hist = this.values.get(key);
    
    if (!hist) {
      hist = {
        count: 0,
        sum: 0,
        buckets: new Map(this.buckets.map(b => [b, 0])),
        labels
      };
      this.values.set(key, hist);
    }
    
    hist.count++;
    hist.sum += value;
    
    // Increment all buckets where value <= bucket boundary
    for (const bucket of this.buckets) {
      if (value <= bucket) {
        hist.buckets.set(bucket, (hist.buckets.get(bucket) || 0) + 1);
      }
    }
  }
  
  /**
   * Start a timer that observes duration when stopped
   */
  startTimer(labels: MetricLabels = {}): () => number {
    const start = process.hrtime.bigint();
    return () => {
      const end = process.hrtime.bigint();
      const durationMs = Number(end - start) / 1e6;
      this.observe(labels, durationMs / 1000); // Convert to seconds
      return durationMs;
    };
  }
  
  /**
   * Get histogram data for labels
   */
  get(labels: MetricLabels = {}): HistogramValue | undefined {
    const key = this.labelsToKey(labels);
    return this.values.get(key);
  }
  
  /**
   * Get all histogram values
   */
  getAll(): HistogramValue[] {
    return Array.from(this.values.values());
  }
  
  /**
   * Get percentile value (approximate)
   */
  percentile(labels: MetricLabels, p: number): number | undefined {
    const hist = this.get(labels);
    if (!hist || hist.count === 0) return undefined;
    
    const target = Math.ceil(hist.count * p);
    let cumulative = 0;
    
    for (const bucket of this.buckets) {
      cumulative = hist.buckets.get(bucket) || 0;
      if (cumulative >= target) {
        return bucket;
      }
    }
    
    return this.buckets[this.buckets.length - 1];
  }
  
  /**
   * Get mean value
   */
  mean(labels: MetricLabels = {}): number | undefined {
    const hist = this.get(labels);
    if (!hist || hist.count === 0) return undefined;
    return hist.sum / hist.count;
  }
  
  /**
   * Reset histogram (for testing)
   */
  reset(): void {
    this.values.clear();
  }
  
  private labelsToKey(labels: MetricLabels): string {
    return Object.entries(labels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}="${v}"`)
      .join(',');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// SUMMARY
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Summary: Like histogram but calculates quantiles on the client side.
 * More accurate quantiles but uses more memory.
 */
export class Summary {
  private values: Map<string, { observations: number[]; labels: MetricLabels }> = new Map();
  private maxObservations: number;
  
  constructor(
    public readonly options: MetricOptions,
    maxObservations: number = 1000
  ) {
    this.maxObservations = maxObservations;
  }
  
  /**
   * Observe a value
   */
  observe(labels: MetricLabels, value: number): void;
  observe(value: number): void;
  observe(labelsOrValue: MetricLabels | number, maybeValue?: number): void {
    const labels = typeof labelsOrValue === 'number' ? {} : labelsOrValue;
    const value = typeof labelsOrValue === 'number' ? labelsOrValue : maybeValue!;
    
    const key = this.labelsToKey(labels);
    let data = this.values.get(key);
    
    if (!data) {
      data = { observations: [], labels };
      this.values.set(key, data);
    }
    
    data.observations.push(value);
    
    // Keep only the most recent observations
    if (data.observations.length > this.maxObservations) {
      data.observations = data.observations.slice(-this.maxObservations);
    }
  }
  
  /**
   * Get quantile value
   */
  quantile(labels: MetricLabels, q: number): number | undefined {
    const data = this.values.get(this.labelsToKey(labels));
    if (!data || data.observations.length === 0) return undefined;
    
    const sorted = [...data.observations].sort((a, b) => a - b);
    const index = Math.floor(sorted.length * q);
    return sorted[Math.min(index, sorted.length - 1)];
  }
  
  /**
   * Get count
   */
  count(labels: MetricLabels = {}): number {
    const data = this.values.get(this.labelsToKey(labels));
    return data?.observations.length ?? 0;
  }
  
  /**
   * Get sum
   */
  sum(labels: MetricLabels = {}): number {
    const data = this.values.get(this.labelsToKey(labels));
    if (!data) return 0;
    return data.observations.reduce((a, b) => a + b, 0);
  }
  
  /**
   * Reset summary (for testing)
   */
  reset(): void {
    this.values.clear();
  }
  
  private labelsToKey(labels: MetricLabels): string {
    return Object.entries(labels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}="${v}"`)
      .join(',');
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// METRICS REGISTRY
// ═══════════════════════════════════════════════════════════════════════════

export type MetricType = Counter | Gauge | Histogram | Summary;

/**
 * Central registry for all metrics
 */
export class MetricsRegistry {
  private static instance: MetricsRegistry;
  private metrics: Map<string, MetricType> = new Map();
  private prefix: string = '';
  
  private constructor() {}
  
  /**
   * Get the singleton instance
   */
  static getInstance(): MetricsRegistry {
    if (!MetricsRegistry.instance) {
      MetricsRegistry.instance = new MetricsRegistry();
    }
    return MetricsRegistry.instance;
  }
  
  /**
   * Set a prefix for all metric names
   */
  setPrefix(prefix: string): void {
    this.prefix = prefix;
  }
  
  /**
   * Register a counter
   */
  counter(options: MetricOptions): Counter {
    const name = this.prefix + options.name;
    const existing = this.metrics.get(name);
    if (existing instanceof Counter) {
      return existing;
    }
    const counter = new Counter({ ...options, name });
    this.metrics.set(name, counter);
    return counter;
  }
  
  /**
   * Register a gauge
   */
  gauge(options: MetricOptions): Gauge {
    const name = this.prefix + options.name;
    const existing = this.metrics.get(name);
    if (existing instanceof Gauge) {
      return existing;
    }
    const gauge = new Gauge({ ...options, name });
    this.metrics.set(name, gauge);
    return gauge;
  }
  
  /**
   * Register a histogram
   */
  histogram(options: HistogramOptions): Histogram {
    const name = this.prefix + options.name;
    const existing = this.metrics.get(name);
    if (existing instanceof Histogram) {
      return existing;
    }
    const histogram = new Histogram({ ...options, name });
    this.metrics.set(name, histogram);
    return histogram;
  }
  
  /**
   * Register a summary
   */
  summary(options: MetricOptions, maxObservations?: number): Summary {
    const name = this.prefix + options.name;
    const existing = this.metrics.get(name);
    if (existing instanceof Summary) {
      return existing;
    }
    const summary = new Summary({ ...options, name }, maxObservations);
    this.metrics.set(name, summary);
    return summary;
  }
  
  /**
   * Get a metric by name
   */
  get(name: string): MetricType | undefined {
    return this.metrics.get(this.prefix + name);
  }
  
  /**
   * Get all metrics
   */
  getAll(): Map<string, MetricType> {
    return new Map(this.metrics);
  }
  
  /**
   * Export metrics in Prometheus text format
   */
  toPrometheusFormat(): string {
    const lines: string[] = [];
    
    for (const [name, metric] of this.metrics) {
      if (metric instanceof Counter) {
        lines.push(`# HELP ${name} ${metric.options.help}`);
        lines.push(`# TYPE ${name} counter`);
        for (const value of metric.getAll()) {
          const labels = this.formatLabels(value.labels);
          lines.push(`${name}${labels} ${value.value}`);
        }
      } else if (metric instanceof Gauge) {
        lines.push(`# HELP ${name} ${metric.options.help}`);
        lines.push(`# TYPE ${name} gauge`);
        for (const value of metric.getAll()) {
          const labels = this.formatLabels(value.labels);
          lines.push(`${name}${labels} ${value.value}`);
        }
      } else if (metric instanceof Histogram) {
        lines.push(`# HELP ${name} ${metric.options.help}`);
        lines.push(`# TYPE ${name} histogram`);
        for (const hist of metric.getAll()) {
          const baseLabels = this.formatLabels(hist.labels);
          for (const [bucket, count] of hist.buckets) {
            const bucketLabels = hist.labels 
              ? `${baseLabels.slice(0, -1)},le="${bucket}"}` 
              : `{le="${bucket}"}`;
            lines.push(`${name}_bucket${bucketLabels} ${count}`);
          }
          lines.push(`${name}_bucket${baseLabels ? `${baseLabels.slice(0, -1)},le="+Inf"}` : '{le="+Inf"}'} ${hist.count}`);
          lines.push(`${name}_sum${baseLabels} ${hist.sum}`);
          lines.push(`${name}_count${baseLabels} ${hist.count}`);
        }
      } else if (metric instanceof Summary) {
        lines.push(`# HELP ${name} ${metric.options.help}`);
        lines.push(`# TYPE ${name} summary`);
        // Summary exports would include quantiles
      }
      lines.push('');
    }
    
    return lines.join('\n');
  }
  
  /**
   * Reset all metrics (for testing)
   */
  reset(): void {
    for (const metric of this.metrics.values()) {
      metric.reset();
    }
  }
  
  /**
   * Clear all metrics (for testing)
   */
  clear(): void {
    this.metrics.clear();
  }
  
  private formatLabels(labels: MetricLabels): string {
    const entries = Object.entries(labels);
    if (entries.length === 0) return '';
    return '{' + entries.map(([k, v]) => `${k}="${v}"`).join(',') + '}';
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// CONVENIENCE EXPORTS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Get the global metrics registry
 */
export function getMetrics(): MetricsRegistry {
  return MetricsRegistry.getInstance();
}

/**
 * Create a counter
 */
export function createCounter(name: string, help: string, labels?: string[]): Counter {
  return getMetrics().counter({ name, help, labels });
}

/**
 * Create a gauge
 */
export function createGauge(name: string, help: string, labels?: string[]): Gauge {
  return getMetrics().gauge({ name, help, labels });
}

/**
 * Create a histogram
 */
export function createHistogram(
  name: string, 
  help: string, 
  buckets?: number[],
  labels?: string[]
): Histogram {
  return getMetrics().histogram({ name, help, buckets, labels });
}

// ═══════════════════════════════════════════════════════════════════════════
// ALEPHNET SPECIFIC METRICS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Pre-defined AlephNet metrics
 */
export const alephMetrics = {
  // Node metrics
  nodeHeartbeats: () => createCounter(
    'aleph_node_heartbeats_total',
    'Total number of heartbeats sent'
  ),
  
  nodeActiveConnections: () => createGauge(
    'aleph_node_active_connections',
    'Number of active peer connections'
  ),
  
  // Message metrics
  messagesReceived: () => createCounter(
    'aleph_messages_received_total',
    'Total messages received',
    ['type', 'domain']
  ),
  
  messagesSent: () => createCounter(
    'aleph_messages_sent_total',
    'Total messages sent',
    ['type', 'domain']
  ),
  
  messageLatency: () => createHistogram(
    'aleph_message_latency_seconds',
    'Message processing latency in seconds',
    [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1]
  ),
  
  // SRIA metrics
  sriaInferenceTime: () => createHistogram(
    'aleph_sria_inference_seconds',
    'SRIA inference time in seconds',
    [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
  ),
  
  sriaFreeEnergy: () => createGauge(
    'aleph_sria_free_energy',
    'Current SRIA free energy level'
  ),
  
  // GMF metrics
  gmfObjectCount: () => createGauge(
    'aleph_gmf_object_count',
    'Number of objects in the GMF'
  ),
  
  gmfWriteLatency: () => createHistogram(
    'aleph_gmf_write_latency_seconds',
    'GMF write latency in seconds'
  ),
  
  // Consensus metrics
  consensusRounds: () => createCounter(
    'aleph_consensus_rounds_total',
    'Total consensus rounds completed',
    ['outcome']
  ),
  
  consensusLatency: () => createHistogram(
    'aleph_consensus_latency_seconds',
    'Consensus round latency in seconds'
  ),
  
  // Wallet metrics
  walletTransactions: () => createCounter(
    'aleph_wallet_transactions_total',
    'Total wallet transactions',
    ['type']
  ),
  
  walletBalance: () => createGauge(
    'aleph_wallet_balance',
    'Current wallet balance',
    ['tier']
  ),
  
  // Error metrics
  errors: () => createCounter(
    'aleph_errors_total',
    'Total errors',
    ['type', 'component']
  )
};
