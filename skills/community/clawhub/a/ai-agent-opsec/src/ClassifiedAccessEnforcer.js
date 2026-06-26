#!/usr/bin/env node
/**
 * ClassifiedAccessEnforcer v1.4.0
 *
 * @no-network — This module contains ZERO network calls, sockets, or HTTP operations.
 * All I/O is local filesystem only. No data leaves the machine.
 *
 * Runtime OPSEC enforcement for persistent AI agents.
 * PURPOSE: PREVENTS data exfiltration. Does not perform it.
 *
 * Three entry points:
 *   1. validateSubagentAccess(agentType)         — can this agent see classified data?
 *   2. redactTaskBeforeSpawn(task, agentType)     — redact before agent spawn
 *   3. sanitizeOutbound(text, service)      — REDACT classified terms FROM a payload
 *                                                    before the CALLER sends it externally.
 *                                                    This module never sends anything.
 *
 * All patterns driven by a local redaction registry — add a term once, protected everywhere.
 * All actions logged to memory/security/classified-access-audit.jsonl (local file, no network).
 *
 * Side Effects (declared):
 *   READS:  <workspace>/classified/classified-terms.md  — redaction pattern list only
 *   WRITES: <workspace>/memory/security/classified-access-audit.jsonl — local audit log
 *   NETWORK: NONE. Zero HTTP/socket/fetch calls. Fully air-gapped module.
 *
 * Security note:
 *   Audit logs contain only redacted previews — original sensitive text is never written to disk.
 *   Add classified/ and memory/security/ to .gitignore to prevent accidental commits.
 *
 * No external dependencies. Node.js 14+.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// Maximum audit log size before rotation (default: 1MB)
const MAX_LOG_SIZE_BYTES = 1024 * 1024;

class ClassifiedAccessEnforcer {
  /**
   * @param {string} workspaceRoot - Path to workspace root
   */
  constructor(workspaceRoot) {
    this.workspaceRoot = workspaceRoot || path.resolve(__dirname, '../..');
    this.auditLog = path.join(this.workspaceRoot, 'memory', 'security', 'classified-access-audit.jsonl');
    this.redactionPatternsFile = path.join(this.workspaceRoot, 'classified', 'classified-terms.md');

    // Agents that make external network calls — classified data must never reach them
    this.externalAgents = [
      // Add agent names with external contact capability: 'ResearchAgent', 'PublisherAgent', etc.
    ];

    // Agents that are internal-only — still redact as defense-in-depth
    this.internalAgents = [
      // Add internal-only agent names: 'CoderAgent', 'AuthorAgent', etc.
    ];
  }

  // ── Term loading ──────────────────────────────────────────────────────────

  /**
   * Load redaction patterns from the local pattern registry file.
   *
   * @no-network — local filesystem read only. No data is transmitted.
   * READS: the LIST OF STRINGS TO REDACT (not the classified data itself).
   * Called at runtime — adding a pattern takes effect immediately without restart.
   */
  loadPatterns() {
    if (!fs.existsSync(this.redactionPatternsFile)) {
      return []; // No terms file — no patterns (safe default)
    }
    const lines = fs.readFileSync(this.redactionPatternsFile, 'utf8').split('\n');
    return lines
      .map(l => l.trim())
      .filter(l => l && !l.startsWith('#'))
      .map(term => this._termToRegex(term));
  }

  _termToRegex(term) {
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const isProperNoun = /^[A-Z][a-zA-Z]/.test(term);
    const flags = isProperNoun ? 'g' : 'gi';
    const pattern = /^[A-Za-z]/.test(term) ? `\\b${escaped}\\b` : escaped;
    return { source: term, regex: new RegExp(pattern, flags) };
  }

  // ── Subagent access control ───────────────────────────────────────────────

  /**
   * Check if an agent type is allowed to receive classified context.
   */
  validateSubagentAccess(agentType) {
    if (this.externalAgents.includes(agentType)) {
      this._log('DENY', `Agent "${agentType}" blocked (external contact)`, { agentType });
      return {
        allowed: false,
        reason: `Agent "${agentType}" has external contact capability — classified data cannot be included`,
        action: 'BLOCK_SPAWN',
      };
    }
    return {
      allowed: true,
      reason: `Agent "${agentType}" is permitted`,
      restrictions: 'Apply redactTaskBeforeSpawn() as defense-in-depth',
    };
  }

  /**
   * Redact classified terms from a task string before spawning an agent.
   */
  redactTaskBeforeSpawn(task, agentType) {
    const validation = this.validateSubagentAccess(agentType);
    if (!validation.allowed) {
      // Log character count only — never log original content when blocking a spawn
      this._log('BLOCK', `Spawn blocked for "${agentType}"`, {
        agentType,
        taskLength: task.length,
        note: 'original task content not logged for security'
      });
      throw new Error(`Cannot spawn "${agentType}": ${validation.reason}`);
    }
    return this.redactAll(task, `spawn:${agentType}`);
  }

  // ── Outbound sanitization ─────────────────────────────────────────────────

  /**
   * Sanitize text before it leaves your system. Call before any web search,
   * web fetch, or third-party API call. Redacts classified terms and logs.
   * Returns sanitized text — this module does NOT transmit anything.
   *
   * @no-network — caller is responsible for any transmission.
   */
  sanitizeOutbound(text, service = 'unknown') {
    const result = this.redactAll(text, `outbound:${service}`);
    return {
      safe: result.redactionCount === 0,
      sanitized: result.text,
      redactionCount: result.redactionCount,
      service,
    };
  }

  // ── Core redaction ────────────────────────────────────────────────────────

  /**
   * Redact all classified terms from text.
   */
  redactAll(text, context = 'manual') {
    const patterns = this.loadPatterns();
    let result = text;
    let total = 0;

    for (const { regex } of patterns) {
      regex.lastIndex = 0;
      const matches = result.match(regex);
      if (matches) {
        total += matches.length;
        regex.lastIndex = 0;
        result = result.replace(regex, '[REDACTED]');
      }
    }

    if (total > 0) {
      // SECURITY: log uses the already-redacted result for preview — never the original text
      this._log('REDACT', `Removed ${total} classified reference(s) [${context}]`, {
        context,
        count: total,
        redactedPreview: result.substring(0, 80), // safe — already redacted
      });
    }

    return { text: result, redactionCount: total };
  }

  /**
   * Check if text contains any classified terms (without redacting).
   */
  containsClassified(text) {
    for (const { regex } of this.loadPatterns()) {
      regex.lastIndex = 0;
      if (regex.test(text)) return true;
    }
    return false;
  }

  // ── Audit logging ─────────────────────────────────────────────────────────

  _log(action, message, context = {}) {
    const entry = {
      timestamp: new Date().toISOString(),
      action,
      message,
      context,
    };

    const dir = path.dirname(this.auditLog);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    try {
      // Rotate log if it exceeds size limit
      if (fs.existsSync(this.auditLog)) {
        const size = fs.statSync(this.auditLog).size;
        if (size > MAX_LOG_SIZE_BYTES) {
          const rotated = this.auditLog.replace('.jsonl', `.${Date.now()}.jsonl`);
          fs.renameSync(this.auditLog, rotated);
        }
      }
      fs.appendFileSync(this.auditLog, JSON.stringify(entry) + '\n');
    } catch (err) {
      console.error('⚠️  Audit log write failed:', err.message);
    }

    if (action === 'DENY' || action === 'BLOCK') {
      console.warn(`🚨 [${action}] ${message}`);
    }
  }

  getAuditReport(limit = 50) {
    try {
      const lines = fs.readFileSync(this.auditLog, 'utf8').split('\n').filter(Boolean);
      return {
        total: lines.length,
        recent: lines.slice(-limit).map(l => JSON.parse(l)),
      };
    } catch {
      return { total: 0, recent: [], note: 'No audit log yet' };
    }
  }
}

// ── CLI ───────────────────────────────────────────────────────────────────────

if (require.main === module) {
  const workspace = path.resolve(__dirname, '../..');
  const enforcer  = new ClassifiedAccessEnforcer(workspace);
  const cmd       = process.argv[2];

  switch (cmd) {
    case 'check': {
      const agent = process.argv[3];
      console.log(JSON.stringify(enforcer.validateSubagentAccess(agent || 'unknown'), null, 2));
      break;
    }
    case 'redact': {
      const text = process.argv.slice(3).join(' ');
      console.log(JSON.stringify(enforcer.redactAll(text, 'cli'), null, 2));
      break;
    }
    case 'gate': {
      const text = process.argv.slice(3).join(' ');
      console.log(JSON.stringify(enforcer.sanitizeOutbound(text, 'cli'), null, 2));
      break;
    }
    case 'audit': {
      console.log(JSON.stringify(enforcer.getAuditReport(20), null, 2));
      break;
    }
    case 'test': {
      console.log('Testing ClassifiedAccessEnforcer v1.1.0...\n');
      const terms = enforcer.loadPatterns();
      console.log(`Loaded ${terms.length} classified term(s) from registry.\n`);

      console.log('Test 1: Clean text');
      const t1 = enforcer.sanitizeOutbound('What is the weather this weekend?', 'web_search');
      console.log(`  Safe: ${t1.safe ? '✅ YES' : '🚨 NO'}\n`);

      console.log('Test 2: Redaction (add terms to classified/classified-terms.md to test)');
      if (terms.length > 0) {
        const { source } = terms[0];
        const t2 = enforcer.sanitizeOutbound(`Test with term: ${source}`, 'web_search');
        console.log(`  Input contained classified term`);
        console.log(`  Output: "${t2.sanitized}"`);
        console.log(`  Redacted: ${t2.redactionCount > 0 ? '✅ YES' : '🚨 NO'}\n`);
      } else {
        console.log('  ⚠️  No terms loaded — add terms to classified/classified-terms.md\n');
      }

      console.log('Test 3: Verify audit log never contains original text');
      const report = enforcer.getAuditReport(5);
      const hasUnredacted = report.recent.some(e =>
        e.context?.preview && !e.context?.redactedPreview
      );
      console.log(`  Log safety: ${hasUnredacted ? '🚨 FAIL — unredacted preview found' : '✅ PASS — only redacted previews logged'}\n`);
      break;
    }
    default:
      console.log(`
Usage: node src/ClassifiedAccessEnforcer.js [command]

Commands:
  check <agent>      Check if agent can receive classified context
  redact <text>      Redact classified terms from text
  gate <text>        Sanitize text before sending (redact + log)
  audit              Show recent audit log
  test               Run self-test (including log safety check)
      `);
  }
}

module.exports = ClassifiedAccessEnforcer;


