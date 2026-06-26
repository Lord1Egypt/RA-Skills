/**
 * Audit Trail Skill
 * Immutable, hash-chained logging of all agent actions
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

export default {
  name: 'audit-trail',
  version: '1.0.0',
  emoji: '📜',

  config: {
    logDir: '.security/audit-trail',
    retentionDays: 365,
    compressionDays: 7,
    maxEntrySize: 10000,
    secretPatterns: [
      /password[:=]\s*[^\s]+/gi,
      /token[:=]\s*[^\s]+/gi,
      /api[_-]?key[:=]\s*[^\s]+/gi,
      /secret[:=]\s*[^\s]+/gi,
      /bearer\s+[a-zA-Z0-9_-]{20,}/gi,
      /gh[pousr]_[a-zA-Z0-9]{36,}/g,
      /AKIA[0-9A-Z]{16}/g
    ]
  },

  async execute(input = {}) {
    const mode = input.mode || 'log'; // 'log', 'verify', 'query', 'report'
    const targetDir = input.path || process.cwd();

    try {
      switch (mode) {
        case 'log':
          return await this.logAction(input.entry, targetDir);
        case 'verify':
          return await this.verifyChain(targetDir);
        case 'query':
          return await this.queryLog(input.query, targetDir);
        case 'report':
          return await this.generateReport(input.since, targetDir);
        default:
          return { success: false, error: `Unknown mode: ${mode}` };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  /**
   * Log a single action
   */
  async logAction(entry, targetDir) {
    const logDir = path.join(targetDir, this.config.logDir);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }

    const today = new Date().toISOString().split('T')[0];
    const logFile = path.join(logDir, `${today}.jsonl`);

    // Get previous hash for chain
    let prevHash = 'sha256:0000000000000000000000000000000000000000000000000000000000000000';
    let sequence = 1;

    if (fs.existsSync(logFile)) {
      const lines = fs.readFileSync(logFile, 'utf-8').trim().split('\n').filter(Boolean);
      if (lines.length > 0) {
        const lastEntry = JSON.parse(lines[lines.length - 1]);
        prevHash = lastEntry.hash;
        sequence = parseInt(lastEntry.id.split('-').pop()) + 1;
      }
    }

    // Sanitize entry (redact secrets)
    const sanitized = this.sanitizeEntry(entry);

    // Build complete log entry
    const logEntry = {
      id: `ACT-${today.replace(/-/g, '')}-${String(sequence).padStart(6, '0')}`,
      ts: new Date().toISOString(),
      agent: entry.agent || 'openclaw-main',
      session: entry.session || 'unknown',
      type: entry.type || 'unknown',
      tool: entry.tool || null,
      args: sanitized,
      skill: entry.skill || null,
      channel: entry.channel || null,
      user_hash: entry.user ? this.hashUser(entry.user) : null,
      outcome: entry.outcome || 'unknown',
      duration_ms: entry.duration_ms || 0,
      prev_hash: prevHash,
      hash: null // Will be computed
    };

    // Compute hash
    const hashData = JSON.stringify({
      id: logEntry.id,
      ts: logEntry.ts,
      type: logEntry.type,
      tool: logEntry.tool,
      outcome: logEntry.outcome,
      prev_hash: prevHash
    });
    logEntry.hash = `sha256:${crypto.createHash('sha256').update(hashData).digest('hex')}`;

    // Append to log file
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');

    return {
      success: true,
      logged: true,
      entry: {
        id: logEntry.id,
        ts: logEntry.ts,
        hash: logEntry.hash
      }
    };
  },

  /**
   * Verify chain integrity
   */
  async verifyChain(targetDir) {
    const logDir = path.join(targetDir, this.config.logDir);
    
    if (!fs.existsSync(logDir)) {
      return { success: true, verified: true, files: 0, entries: 0 };
    }

    const results = {
      success: true,
      verified: true,
      files: 0,
      entries: 0,
      broken: [],
      details: []
    };

    const logFiles = fs.readdirSync(logDir)
      .filter(f => f.endsWith('.jsonl'))
      .sort();

    for (const file of logFiles) {
      const filePath = path.join(logDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.trim().split('\n').filter(Boolean);
      
      results.files++;
      
      let prevHash = 'sha256:0000000000000000000000000000000000000000000000000000000000000000';
      
      for (let i = 0; i < lines.length; i++) {
        const entry = JSON.parse(lines[i]);
        results.entries++;

        // Verify chain link
        if (entry.prev_hash !== prevHash) {
          results.verified = false;
          results.broken.push({
            file,
            line: i + 1,
            id: entry.id,
            expected_prev: prevHash,
            actual_prev: entry.prev_hash
          });
        }

        // Verify hash
        const hashData = JSON.stringify({
          id: entry.id,
          ts: entry.ts,
          type: entry.type,
          tool: entry.tool,
          outcome: entry.outcome,
          prev_hash: entry.prev_hash
        });
        const computedHash = `sha256:${crypto.createHash('sha256').update(hashData).digest('hex')}`;
        
        if (computedHash !== entry.hash) {
          results.verified = false;
          results.broken.push({
            file,
            line: i + 1,
            id: entry.id,
            error: 'hash_mismatch',
            expected: entry.hash,
            computed: computedHash
          });
        }

        prevHash = entry.hash;
      }
    }

    // Write integrity check log
    const integrityFile = path.join(logDir, 'integrity-check.log');
    fs.writeFileSync(integrityFile, JSON.stringify({
      checked: new Date().toISOString(),
      verified: results.verified,
      files: results.files,
      entries: results.entries,
      broken: results.broken
    }, null, 2));

    return results;
  },

  /**
   * Query log entries
   */
  async queryLog(query, targetDir) {
    const logDir = path.join(targetDir, this.config.logDir);
    
    if (!fs.existsSync(logDir)) {
      return { success: true, matches: [], count: 0 };
    }

    const matches = [];
    const logFiles = fs.readdirSync(logDir)
      .filter(f => f.endsWith('.jsonl'))
      .sort().reverse();

    for (const file of logFiles) {
      const filePath = path.join(logDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.trim().split('\n').filter(Boolean);

      for (const line of lines) {
        const entry = JSON.parse(line);
        
        if (this.matchesQuery(entry, query)) {
          matches.push(entry);
          if (query.limit && matches.length >= query.limit) {
            break;
          }
        }
      }

      if (query.limit && matches.length >= query.limit) {
        break;
      }
    }

    return {
      success: true,
      matches,
      count: matches.length
    };
  },

  /**
   * Generate compliance report
   */
  async generateReport(since, targetDir) {
    const logDir = path.join(targetDir, this.config.logDir);
    
    if (!fs.existsSync(logDir)) {
      return { success: true, report: null, message: 'No logs found' };
    }

    const report = {
      generated: new Date().toISOString(),
      since: since || 'all time',
      summary: {
        totalActions: 0,
        byType: {},
        byOutcome: {},
        byTool: {},
        bySkill: {},
        errors: 0
      },
      timeline: []
    };

    const logFiles = fs.readdirSync(logDir)
      .filter(f => f.endsWith('.jsonl'))
      .sort();

    for (const file of logFiles) {
      const date = file.replace('.jsonl', '');
      if (since && date < since) continue;

      const filePath = path.join(logDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.trim().split('\n').filter(Boolean);
      
      const dayStats = { date, count: 0, byType: {} };

      for (const line of lines) {
        const entry = JSON.parse(line);
        report.summary.totalActions++;
        dayStats.count++;

        // Count by type
        report.summary.byType[entry.type] = (report.summary.byType[entry.type] || 0) + 1;
        dayStats.byType[entry.type] = (dayStats.byType[entry.type] || 0) + 1;

        // Count by outcome
        report.summary.byOutcome[entry.outcome] = (report.summary.byOutcome[entry.outcome] || 0) + 1;

        // Count by tool
        if (entry.tool) {
          report.summary.byTool[entry.tool] = (report.summary.byTool[entry.tool] || 0) + 1;
        }

        // Count by skill
        if (entry.skill) {
          report.summary.bySkill[entry.skill] = (report.summary.bySkill[entry.skill] || 0) + 1;
        }

        // Count errors
        if (entry.outcome === 'failure' || entry.type === 'error') {
          report.summary.errors++;
        }
      }

      report.timeline.push(dayStats);
    }

    // Write report
    const reportFile = path.join(logDir, `report-${new Date().toISOString().split('T')[0]}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

    return {
      success: true,
      report,
      reportFile
    };
  },

  /**
   * Sanitize entry (redact secrets)
   */
  sanitizeEntry(entry) {
    if (!entry.args) return entry.args;
    
    let sanitized = JSON.stringify(entry.args);
    
    for (const pattern of this.config.secretPatterns) {
      sanitized = sanitized.replace(pattern, '[REDACTED]');
    }
    
    // Limit size
    if (sanitized.length > this.config.maxEntrySize) {
      sanitized = sanitized.slice(0, this.config.maxEntrySize) + '...[TRUNCATED]';
    }
    
    return JSON.parse(sanitized);
  },

  /**
   * Hash user identifier
   */
  hashUser(user) {
    return `sha256:${crypto.createHash('sha256').update(user).digest('hex').slice(0, 16)}`;
  },

  /**
   * Check if entry matches query
   */
  matchesQuery(entry, query) {
    if (query.type && entry.type !== query.type) return false;
    if (query.tool && entry.tool !== query.tool) return false;
    if (query.skill && entry.skill !== query.skill) return false;
    if (query.outcome && entry.outcome !== query.outcome) return false;
    if (query.channel && entry.channel !== query.channel) return false;
    if (query.since && entry.ts < query.since) return false;
    if (query.until && entry.ts > query.until) return false;
    
    return true;
  },

  async validate(input) {
    return typeof input === 'object';
  }
};
