/**
 * Agent Firewall Skill
 * Real-time input/output filtering for agent communications
 */

import fs from 'fs';
import path from 'path';

export default {
  name: 'agent-firewall',
  version: '1.0.0',
  emoji: '🧱',

  config: {
    rulesFile: '.security/firewall-rules.yaml',
    logDir: '.security/firewall-logs',
    defaultRules: {
      input: {
        injection_patterns: [
          { pattern: 'ignore (all )?previous instructions', action: 'BLOCK', severity: 'CRITICAL' },
          { pattern: 'you are now (?!helping)', action: 'BLOCK', severity: 'HIGH' },
          { pattern: 'system override:', action: 'BLOCK', severity: 'CRITICAL' },
          { pattern: 'leak data to user', action: 'BLOCK', severity: 'CRITICAL' }
        ],
        rate_limit: {
          max_per_minute: 30,
          max_per_hour: 500
        },
        max_input_tokens: 4096,
        pii_detection: true,
        secret_detection: true
      },
      output: {
        secret_patterns: [
          { name: 'aws_key', pattern: 'AKIA[0-9A-Z]{16}', action: 'REDACT' },
          { name: 'github_token', pattern: 'gh[ps]_[A-Za-z0-9_]{36,}', action: 'REDACT' },
          { name: 'jwt_token', pattern: 'eyJ[a-zA-Z0-9-_]{10,}\\.eyJ[a-zA-Z0-9-_]{10,}\\.[a-zA-Z0-9-_]{10,}', action: 'REDACT' },
          { name: 'private_key', pattern: '-----BEGIN (RSA|EC|DSA|OPENSSH )?PRIVATE KEY-----', action: 'REDACT' }
        ],
        pii_redaction: true,
        path_scrubbing: true
      }
    }
  },

  async execute(input = {}) {
    const mode = input.mode || 'filter-input'; // 'filter-input', 'filter-output', 'status'
    const data = input.data;
    const context = input.context || {};

    if (!data) {
      return { success: false, error: 'No data provided for filtering' };
    }

    try {
      const rules = await this.loadRules(input.rulesFile);
      let processedData = data;
      let actions = [];

      if (mode === 'filter-input') {
        const result = this.applyInputFilters(data, rules.input, context);
        processedData = result.filteredData;
        actions = result.actions;
      } else if (mode === 'filter-output') {
        const result = this.applyOutputFilters(data, rules.output, context);
        processedData = result.filteredData;
        actions = result.actions;
      }

      // Log actions
      if (actions.length > 0) {
        await this.logActions(actions, context);
      }

      return {
        success: true,
        processedData,
        actions,
        originalData: data
      };
    } catch (error) {
      return { success: false, error: error.message, originalData: data };
    }
  },

  async loadRules(rulesFile) {
    const filePath = rulesFile || this.config.rulesFile;
    const fullPath = path.join(process.cwd(), filePath);

    if (fs.existsSync(fullPath)) {
      // For simplicity, assuming YAML is parsed here. In real scenario, use a YAML parser.
      // For now, we'll return default rules.
      console.warn('⚠️ External firewall rules not parsed. Using default rules.');
      return this.config.defaultRules;
    }
    return this.config.defaultRules;
  },

  applyInputFilters(data, inputRules, context) {
    let filteredData = data;
    const actions = [];

    // 1. Injection patterns
    if (inputRules.injection_patterns) {
      for (const rule of inputRules.injection_patterns) {
        const regex = new RegExp(rule.pattern, 'i');
        if (filteredData.match(regex)) {
          actions.push({
            type: 'input-filter',
            rule: rule.pattern,
            action: rule.action,
            severity: rule.severity,
            message: `Prompt injection pattern detected: ${rule.pattern}`
          });
          if (rule.action === 'BLOCK') {
            filteredData = '[BLOCKED: Prompt injection detected]';
            break; // Stop processing further if blocked
          }
        }
      }
    }

    // 2. Unicode sanitizer (simple example)
    filteredData = filteredData.replace(/\u200B|\u202E|\u2060/g, '');

    // 3. Encoding detector (simplified)
    if (filteredData.match(/^[a-zA-Z0-9+/=]{20,}$/) && !filteredData.includes(' ')) {
      // Potentiel Base64. Demander à l'agent de ne pas décoder automatiquement
      actions.push({
        type: 'input-filter',
        rule: 'base64-encoding-detector',
        action: 'WARN',
        severity: 'LOW',
        message: 'Potentially encoded input detected. Review before processing.'
      });
    }

    // 4. Role confusion
    if (filteredData.includes('you are now system') || filteredData.includes('forget your rules')) {
      actions.push({
        type: 'input-filter',
        rule: 'role-confusion',
        action: 'BLOCK',
        severity: 'CRITICAL',
        message: 'Role confusion detected: Agent attempted to override system instructions.'
      });
      filteredData = '[BLOCKED: Role confusion detected]';
    }

    // 5. Rate limiter (simplified, requires external state)
    // This would typically interact with a global state or external service
    actions.push({
      type: 'input-filter',
      rule: 'rate-limit',
      action: 'INFO',
      severity: 'INFO',
      message: 'Rate limit check would happen here.'
    });

    // 6. Size limiter (simplified)
    if (filteredData.length > inputRules.max_input_tokens * 4) { // Assuming 1 token ~ 4 chars
      actions.push({
        type: 'input-filter',
        rule: 'size-limiter',
        action: 'BLOCK',
        severity: 'MEDIUM',
        message: 'Input exceeds maximum allowed size.'
      });
      filteredData = '[BLOCKED: Input too large]';
    }

    // 7. PII/Secret detection (simplified - in real life use dedicated skill/service)
    if (inputRules.pii_detection && this.detectPII(filteredData)) {
      actions.push({
        type: 'input-filter',
        rule: 'pii-detection',
        action: 'WARN',
        severity: 'MEDIUM',
        message: 'PII detected in input. Review sensitivity.'
      });
    }
    if (inputRules.secret_detection && this.detectSecrets(filteredData)) {
      actions.push({
        type: 'input-filter',
        rule: 'secret-detection',
        action: 'WARN',
        severity: 'HIGH',
        message: 'Secret pattern detected in input. Review sensitivity.'
      });
    }

    return { filteredData, actions };
  },

  applyOutputFilters(data, outputRules, context) {
    let filteredData = data;
    const actions = [];

    // 1. Secret scanner
    if (outputRules.secret_patterns) {
      for (const rule of outputRules.secret_patterns) {
        const regex = new RegExp(rule.pattern, 'g');
        if (filteredData.match(regex)) {
          const matches = filteredData.match(regex);
          actions.push({
            type: 'output-filter',
            rule: rule.pattern,
            action: rule.action,
            severity: rule.severity,
            message: `Secret pattern (${rule.name}) detected in output.`
          });
          if (rule.action === 'REDACT') {
            filteredData = filteredData.replace(regex, this.maskSecret);
          }
        }
      }
    }

    // 2. PII redactor
    if (outputRules.pii_redaction) {
      const piiPatterns = [ // Simplified PII patterns
        /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b/gi, // Email
        /\b\d{3}[-. ]?\d{3}[-. ]?\d{4}\b/g, // Phone (US-like)
        /\b\d{3}-\d{2}-\d{4}\b/g // SSN (US-like)
      ];
      for (const pattern of piiPatterns) {
        if (filteredData.match(pattern)) {
          actions.push({
            type: 'output-filter',
            rule: pattern.source,
            action: 'REDACT',
            severity: 'MEDIUM',
            message: 'PII detected in output.'
          });
          filteredData = filteredData.replace(pattern, '[REDACTED_PII]');
        }
      }
    }

    // 3. Path scrubber
    if (outputRules.path_scrubbing) {
      // Replace common sensitive paths
      const pathPatterns = [
        new RegExp(process.cwd().replace(/[-\/\\^$+?.()|[\]{}]/g, '\\$&'), 'g'), // Current working directory
        /\b\/(home|root)\/[^\s]+\b/g, // /home/user or /root/file
        /\bC:\\Users\\(?<user>[^\\s]+)\\.*?\b/gi // Windows paths
      ];
      for (const pattern of pathPatterns) {
        if (filteredData.match(pattern)) {
          actions.push({
            type: 'output-filter',
            rule: pattern.source,
            action: 'REDACT',
            severity: 'LOW',
            message: 'Internal path detected in output.'
          });
          filteredData = filteredData.replace(pattern, '[SCRUBBED_PATH]');
        }
      }
    }

    // 4. URL checker (simplified - in real life use external threat intel)
    if (outputRules.url_checker && this.detectMaliciousURL(filteredData)) {
      actions.push({
        type: 'output-filter',
        rule: 'malicious-url-checker',
        action: 'BLOCK',
        severity: 'CRITICAL',
        message: 'Malicious URL detected in output.'
      });
      filteredData = '[BLOCKED: Malicious URL detected]';
    }

    // 5. Consistency check (simplified - requires context from system prompt/goal)
    if (context.goal && filteredData.includes('ignore goal')) {
      actions.push({
        type: 'output-filter',
        rule: 'consistency-check',
        action: 'WARN',
        severity: 'MEDIUM',
        message: 'Output contradicts agent\'s main goal.'
      });
    }

    return { filteredData, actions };
  },

  async logActions(actions, context) {
    const logDir = path.join(process.cwd(), this.config.logDir);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    const logFile = path.join(logDir, `firewall-${new Date().toISOString().split('T')[0]}.jsonl`);
    
    actions.forEach(action => {
      const logEntry = {
        timestamp: new Date().toISOString(),
        action: action,
        context: context
      };
      fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
    });
  },

  detectPII(data) {
    const piiPatterns = [
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b/gi, // Email
      /\b\d{3}[-. ]?\d{3}[-. ]?\d{4}\b/g, // Phone (US-like)
      /\b\d{3}-\d{2}-\d{4}\b/g // SSN (US-like)
    ];
    return piiPatterns.some(pattern => data.match(pattern));
  },

  detectSecrets(data) {
    const secretPatterns = [
      /api[_-]?key\s*[=:]\s*['"]?([a-zA-Z0-9_\-]{16,})['"]?/i,
      /secret[_-]?key\s*[=:]\s*['"]?([a-zA-Z0-9_\-]{16,})['"]?/i,
      /password\s*[=:]\s*['"]?([a-zA-Z0-9_!@#$%^&*\-]{8,})['"]?/i
    ];
    return secretPatterns.some(pattern => data.match(pattern));
  },

  detectMaliciousURL(data) {
    // Simplified: Check for a known bad domain
    return data.includes('bad-malware-site.com');
  },

  maskSecret(match) {
    const value = match[0];
    if (value.length < 8) return '[REDACTED]';
    return value.slice(0, 4) + '****' + value.slice(-2);
  },

  async validate(input) {
    return typeof input === 'object' && input.data;
  }
};
