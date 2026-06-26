/**
 * Anomaly Watcher Skill
 * Behavioral baseline monitoring and anomaly detection
 */

import fs from 'fs';
import path from 'path';

export default {
  name: 'anomaly-watcher',
  version: '1.0.0',
  emoji: '👁️',

  config: {
    baselineWindow: 7, // days
    metricsFile: '.security/baseline/metrics.jsonl',
    anomaliesFile: '.security/anomalies.jsonl',
    falsePositivesFile: '.security/false-positives.jsonl',
    calibrationHours: 48,
    thresholds: {
      normal: 1,      // within 1σ
      elevated: 2,    // 1-2σ
      anomalous: 3,   // 2-3σ
      critical: 3     // >3σ
    }
  },

  // Known attack signatures
  signatures: [
    {
      id: 'SIG-001',
      name: 'Reconnaissance Pattern',
      description: 'Sudden spike in file reads across many directories',
      indicators: ['file_reads > 3σ', 'unique_paths > 50', 'read_pattern == scattered'],
      severity: 'HIGH'
    },
    {
      id: 'SIG-002', 
      name: 'Potential Exfiltration',
      description: 'Outbound to new domain + high data volume',
      indicators: ['new_domains > 0', 'data_volume > 2σ'],
      severity: 'CRITICAL'
    },
    {
      id: 'SIG-003',
      name: 'Supply Chain Risk',
      description: 'Rapid skill installs from ClawHub',
      indicators: ['skill_installs > 5', 'time_window < 60s'],
      severity: 'MEDIUM'
    },
    {
      id: 'SIG-004',
      name: 'Persistence Attempt',
      description: 'Memory writes with encoded content',
      indicators: ['memory_writes > 2σ', 'encoded_content == true'],
      severity: 'HIGH'
    },
    {
      id: 'SIG-005',
      name: 'Abnormal Tool Use',
      description: 'Unusual combination of tools',
      indicators: ['exec_count > 10', 'file_write_count > 20', 'web_search_count > 0'],
      severity: 'MEDIUM'
    }
  ],

  async execute(input = {}) {
    const mode = input.mode || 'record'; // 'record', 'analyze', 'baseline', 'status'
    const targetDir = input.path || process.cwd();

    try {
      switch (mode) {
        case 'record':
          return await this.recordMetric(input.metric, targetDir);
        case 'analyze':
          return await this.analyzeCurrentWindow(targetDir);
        case 'baseline':
          return await this.calculateBaseline(targetDir);
        case 'status':
          return await this.getStatus(targetDir);
        default:
          return { success: false, error: `Unknown mode: ${mode}` };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  /**
   * Record a single metric
   */
  async recordMetric(metric, targetDir) {
    const metricsDir = path.join(targetDir, '.security');
    if (!fs.existsSync(metricsDir)) {
      fs.mkdirSync(metricsDir, { recursive: true });
    }

    const baselineDir = path.join(metricsDir, 'baseline');
    if (!fs.existsSync(baselineDir)) {
      fs.mkdirSync(baselineDir, { recursive: true });
    }

    const metricsFile = path.join(baselineDir, 'metrics.jsonl');

    const entry = {
      ts: new Date().toISOString(),
      hour: new Date().toISOString().slice(0, 13), // YYYY-MM-DDTHH
      type: metric.type || 'unknown',
      value: metric.value || 1,
      details: metric.details || {},
      session: metric.session || 'unknown'
    };

    fs.appendFileSync(metricsFile, JSON.stringify(entry) + '\n');

    return { success: true, recorded: true, entry };
  },

  /**
   * Calculate baseline from historical data
   */
  async calculateBaseline(targetDir) {
    const metricsFile = path.join(targetDir, '.security/baseline/metrics.jsonl');
    
    if (!fs.existsSync(metricsFile)) {
      return { 
        success: true, 
        calibrated: false, 
        message: 'Not enough data for calibration' 
      };
    }

    const content = fs.readFileSync(metricsFile, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);

    if (lines.length === 0) {
      return { success: true, calibrated: false, message: 'No metrics recorded' };
    }

    // Check if we have enough data (48 hours)
    const timestamps = lines.map(l => new Date(JSON.parse(l).ts).getTime());
    const dataRange = (Math.max(...timestamps) - Math.min(...timestamps)) / (1000 * 60 * 60);
    
    if (dataRange < this.config.calibrationHours) {
      return {
        success: true,
        calibrated: false,
        message: `Need ${this.config.calibrationHours}h of data, have ${dataRange.toFixed(1)}h`,
        dataRange
      };
    }

    // Group by metric type and hour
    const hourlyData = {};
    
    for (const line of lines) {
      const entry = JSON.parse(line);
      const key = `${entry.type}:${entry.hour}`;
      
      if (!hourlyData[entry.type]) {
        hourlyData[entry.type] = [];
      }
      hourlyData[entry.type].push(entry.value);
    }

    // Calculate statistics for each metric type
    const baseline = {};
    
    for (const [type, values] of Object.entries(hourlyData)) {
      const avg = values.reduce((a, b) => a + b, 0) / values.length;
      const variance = values.reduce((sum, v) => sum + Math.pow(v - avg, 2), 0) / values.length;
      const stdDev = Math.sqrt(variance);
      
      baseline[type] = {
        average: avg,
        stdDev: stdDev,
        min: Math.min(...values),
        max: Math.max(...values),
        samples: values.length
      };
    }

    // Save baseline
    const baselineFile = path.join(targetDir, '.security/baseline/statistics.json');
    fs.writeFileSync(baselineFile, JSON.stringify({
      calculated: new Date().toISOString(),
      dataRange,
      metrics: baseline
    }, null, 2));

    return {
      success: true,
      calibrated: true,
      dataRange,
      metrics: Object.keys(baseline).length,
      baseline
    };
  },

  /**
   * Analyze current window for anomalies
   */
  async analyzeCurrentWindow(targetDir) {
    // Load baseline
    const baselineFile = path.join(targetDir, '.security/baseline/statistics.json');
    
    if (!fs.existsSync(baselineFile)) {
      return { success: false, error: 'No baseline calculated. Run mode:baseline first.' };
    }

    const baseline = JSON.parse(fs.readFileSync(baselineFile, 'utf-8'));
    
    // Load current hour metrics
    const metricsFile = path.join(targetDir, '.security/baseline/metrics.jsonl');
    const content = fs.readFileSync(metricsFile, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);

    const currentHour = new Date().toISOString().slice(0, 13);
    const currentMetrics = {};

    // Aggregate current hour
    for (const line of lines) {
      const entry = JSON.parse(line);
      if (entry.hour === currentHour) {
        currentMetrics[entry.type] = (currentMetrics[entry.type] || 0) + entry.value;
      }
    }

    // Compare against baseline
    const findings = [];
    const anomaliesFile = path.join(targetDir, '.security/anomalies.jsonl');

    for (const [type, value] of Object.entries(currentMetrics)) {
      if (baseline.metrics[type]) {
        const stats = baseline.metrics[type];
        const sigma = stats.stdDev > 0 ? (value - stats.average) / stats.stdDev : 0;
        
        let classification = 'NORMAL';
        if (sigma > this.config.thresholds.critical) classification = 'CRITICAL';
        else if (sigma > this.config.thresholds.anomalous) classification = 'ANOMALOUS';
        else if (sigma > this.config.thresholds.elevated) classification = 'ELEVATED';

        if (classification !== 'NORMAL') {
          const finding = {
            ts: new Date().toISOString(),
            metric: type,
            current: value,
            baseline: stats.average,
            stdDev: stats.stdDev,
            sigma: sigma.toFixed(2),
            classification,
            recommendation: this.getRecommendation(type, classification)
          };
          
          findings.push(finding);
          
          // Log anomaly
          fs.appendFileSync(anomaliesFile, JSON.stringify(finding) + '\n');
        }
      }
    }

    // Check attack signatures
    const signatureHits = await this.checkSignatures(currentMetrics, baseline.metrics);

    return {
      success: true,
      analyzed: true,
      currentHour,
      metrics: Object.keys(currentMetrics).length,
      findings,
      signatureHits,
      alert: findings.length > 0 || signatureHits.length > 0
    };
  },

  /**
   * Check against known attack signatures
   */
  async checkSignatures(current, baseline) {
    const hits = [];

    // SIG-001: Reconnaissance Pattern
    if (current.file_read > (baseline.file_read?.average || 10) * 3 && 
        current.unique_paths > 50) {
      hits.push(this.signatures[0]);
    }

    // SIG-002: Potential Exfiltration  
    if (current.network_request > (baseline.network_request?.average || 0) * 2 &&
        current.new_domains > 0) {
      hits.push(this.signatures[1]);
    }

    // SIG-003: Supply Chain Risk
    if (current.skill_install > 5) {
      hits.push(this.signatures[2]);
    }

    // SIG-004: Persistence Attempt
    if (current.memory_write > (baseline.memory_write?.average || 5) * 2) {
      hits.push(this.signatures[3]);
    }

    // SIG-005: Abnormal Tool Use
    if (current.exec > 10 && current.file_write > 20 && current.web_search > 0) {
      hits.push(this.signatures[4]);
    }

    return hits;
  },

  /**
   * Get recommendation based on classification
   */
  getRecommendation(type, classification) {
    const recs = {
      ELEVATED: `Monitor ${type} - slightly above normal range`,
      ANOMALOUS: `Investigate ${type} - significantly elevated, check for misconfiguration`,
      CRITICAL: `URGENT: Review ${type} immediately - potential security incident`
    };
    return recs[classification] || 'No action needed';
  },

  /**
   * Get current status
   */
  async getStatus(targetDir) {
    const status = {
      calibrated: false,
      dataRange: 0,
      lastAnomaly: null,
      anomalyCount: 0
    };

    // Check baseline
    const baselineFile = path.join(targetDir, '.security/baseline/statistics.json');
    if (fs.existsSync(baselineFile)) {
      const baseline = JSON.parse(fs.readFileSync(baselineFile, 'utf-8'));
      status.calibrated = true;
      status.dataRange = baseline.dataRange;
      status.calculated = baseline.calculated;
    }

    // Check anomalies
    const anomaliesFile = path.join(targetDir, '.security/anomalies.jsonl');
    if (fs.existsSync(anomaliesFile)) {
      const content = fs.readFileSync(anomaliesFile, 'utf-8');
      const lines = content.trim().split('\n').filter(Boolean);
      status.anomalyCount = lines.length;
      
      if (lines.length > 0) {
        const last = JSON.parse(lines[lines.length - 1]);
        status.lastAnomaly = last.ts;
      }
    }

    return { success: true, status };
  },

  /**
   * Helper to record action (called by other skills)
   */
  async recordAction(actionType, details, targetDir) {
    return this.recordMetric({
      type: actionType,
      value: 1,
      details,
      session: details.session || 'default'
    }, targetDir);
  },

  async validate(input) {
    return typeof input === 'object';
  }
};
