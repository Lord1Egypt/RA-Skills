/**
 * Metrics 监控模块
 * 收集和报告性能指标
 */

class Metrics {
  constructor() {
    this.counters = new Map();
    this.gauges = new Map();
    this.histograms = new Map();
    this.timers = new Map();
  }

  /**
   * 增加计数器
   */
  inc(name, labels = {}, value = 1) {
    const key = this._key(name, labels);
    const current = this.counters.get(key) || 0;
    this.counters.set(key, current + value);
  }

  /**
   * 设置仪表盘值
   */
  gauge(name, labels = {}, value) {
    const key = this._key(name, labels);
    this.gauges.set(key, value);
  }

  /**
   * 记录直方图
   */
  histogram(name, labels = {}, value) {
    const key = this._key(name, labels);
    if (!this.histograms.has(key)) {
      this.histograms.set(key, []);
    }
    this.histograms.get(key).push(value);
  }

  /**
   * 开始计时
   */
  startTimer(name, labels = {}) {
    const start = Date.now();
    return {
      end: () => {
        const duration = Date.now() - start;
        this.histogram(name, labels, duration);
        return duration;
      }
    };
  }

  /**
   * 获取报告
   */
  report() {
    const report = {
      counters: Object.fromEntries(this.counters),
      gauges: Object.fromEntries(this.gauges),
      histograms: {}
    };

    // 计算直方图统计
    for (const [key, values] of this.histograms) {
      if (values.length === 0) continue;
      
      const sorted = [...values].sort((a, b) => a - b);
      const sum = sorted.reduce((a, b) => a + b, 0);
      
      report.histograms[key] = {
        count: sorted.length,
        sum: sum,
        avg: sum / sorted.length,
        min: sorted[0],
        max: sorted[sorted.length - 1],
        p50: sorted[Math.floor(sorted.length * 0.5)],
        p95: sorted[Math.floor(sorted.length * 0.95)],
        p99: sorted[Math.floor(sorted.length * 0.99)]
      };
    }

    return report;
  }

  /**
   * 生成 Prometheus 格式
   */
  toPrometheus() {
    const lines = [];
    
    // Counters
    for (const [key, value] of this.counters) {
      const { name, labels } = this._parseKey(key);
      lines.push(`# TYPE ${name} counter`);
      lines.push(`${name}${this._formatLabels(labels)} ${value}`);
    }
    
    // Gauges
    for (const [key, value] of this.gauges) {
      const { name, labels } = this._parseKey(key);
      lines.push(`# TYPE ${name} gauge`);
      lines.push(`${name}${this._formatLabels(labels)} ${value}`);
    }
    
    // Histograms
    for (const [key, stats] of Object.entries(this.report().histograms)) {
      const { name, labels } = this._parseKey(key);
      lines.push(`# TYPE ${name} histogram`);
      lines.push(`${name}_count${this._formatLabels(labels)} ${stats.count}`);
      lines.push(`${name}_sum${this._formatLabels(labels)} ${stats.sum}`);
      lines.push(`${name}_avg${this._formatLabels(labels)} ${stats.avg.toFixed(2)}`);
    }
    
    return lines.join('\n');
  }

  _key(name, labels) {
    const labelStr = Object.entries(labels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}=${v}`)
      .join(',');
    return labelStr ? `${name}{${labelStr}}` : name;
  }

  _parseKey(key) {
    const match = key.match(/^(.+?)\{(.+?)\}$/);
    if (!match) return { name: key, labels: {} };
    
    const labels = {};
    match[2].split(',').forEach(pair => {
      const [k, v] = pair.split('=');
      labels[k] = v;
    });
    
    return { name: match[1], labels };
  }

  _formatLabels(labels) {
    if (Object.keys(labels).length === 0) return '';
    const pairs = Object.entries(labels).map(([k, v]) => `${k}="${v}"`);
    return `{${pairs.join(',')}}`;
  }

  /**
   * 重置所有指标
   */
  reset() {
    this.counters.clear();
    this.gauges.clear();
    this.histograms.clear();
    this.timers.clear();
  }
}

// 单例
const metrics = new Metrics();

module.exports = { Metrics, metrics };
