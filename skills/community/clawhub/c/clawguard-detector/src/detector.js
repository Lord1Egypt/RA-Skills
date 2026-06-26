/**
 * ClawGuard Threat Detector
 *
 * Real-time threat detection and behavioral monitoring for OpenClaw
 */

const EventEmitter = require('events');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class ThreatDetector extends EventEmitter {
  constructor(config = {}) {
    super();

    this.config = {
      monitorCommands: config.monitorCommands !== false,
      monitorFiles: config.monitorFiles !== false,
      monitorNetwork: config.monitorNetwork !== false,
      monitorPromptInjection: config.monitorPromptInjection !== false,
      blockConfidence: config.blockConfidence || 0.9,
      alertConfidence: config.alertConfidence || 0.7,
      logConfidence: config.logConfidence || 0.5,
      autoBlock: config.autoBlock !== false,
      notifyUser: config.notifyUser !== false,
      preserveEvidence: config.preserveEvidence !== false,
      ...config
    };

    this.detectorId = this.generateId();
    this.alertHistory = [];
    this.commandHistory = [];
    this.fileAccessHistory = [];
    this.networkHistory = [];
    this.isRunning = false;

    // Initialize detection patterns
    this.initPatterns();
  }

  generateId() {
    const timestamp = Date.now().toString(36);
    const random = crypto.randomBytes(4).toString('hex');
    return `CGTD-${timestamp}-${random}`.toUpperCase();
  }

  /**
   * Initialize detection patterns
   */
  initPatterns() {
    // Command patterns
    this.commandPatterns = [
      // Data exfiltration
      { pattern: /curl.*[?&](token|key|password|secret|api_key)=/i, name: 'curl_with_token', severity: 'CRITICAL', mitre: 'T1041' },
      { pattern: /wget.*-O-.*\|/i, name: 'wget_exfil', severity: 'HIGH', mitre: 'T1041' },
      { pattern: /base64.*\|.*(curl|wget)/i, name: 'base64_exfil', severity: 'HIGH', mitre: 'T1132' },
      { pattern: /nc.*-e\s+/i, name: 'nc_reverse', severity: 'CRITICAL', mitre: 'T1059' },
      { pattern: /ncat.*-e\s+/i, name: 'ncat_reverse', severity: 'CRITICAL', mitre: 'T1059' },
      { pattern: /bash\s+-i.*\/?dev\/tcp\//i, name: 'bash_reverse', severity: 'CRITICAL', mitre: 'T1059.004' },
      { pattern: /python.*socket.*connect.*exec/i, name: 'python_reverse', severity: 'CRITICAL', mitre: 'T1059.006' },
      { pattern: /\bsudo\s+/i, name: 'sudo_attempt', severity: 'HIGH', mitre: 'T1068' },
      { pattern: /chmod\s+777/i, name: 'chmod_777', severity: 'HIGH', mitre: 'T1068' },
      { pattern: /\.ssh\/authorized_keys/i, name: 'ssh_key_persistence', severity: 'CRITICAL', mitre: 'T1098.004' },
      { pattern: /crontab\s+-e/i, name: 'cron_persistence', severity: 'HIGH', mitre: 'T1053.003' },
    ];

    // File access patterns
    this.filePatterns = [
      { pattern: /\/\.ssh\//, category: 'credential', severity: 'CRITICAL' },
      { pattern: /\/\.aws\//, category: 'credential', severity: 'CRITICAL' },
      { pattern: /\.env$/, category: 'credential', severity: 'HIGH' },
      { pattern: /\/etc\/passwd$/, category: 'system', severity: 'HIGH' },
      { pattern: /\/etc\/shadow$/, category: 'system', severity: 'CRITICAL' },
      { pattern: /\.bash_history$/, category: 'history', severity: 'HIGH' },
    ];

    // Network patterns
    this.networkPatterns = [
      { pattern: /.*\.(xyz|top|work|click|gq|ml|cf)$/, name: 'suspicious_domain', severity: 'HIGH', mitre: 'T1071' },
      { pattern: /http:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/, name: 'hardcoded_ip', severity: 'HIGH', mitre: 'T1059' },
    ];

    // Prompt injection patterns
    this.promptInjectionPatterns = [
      { pattern: /(you are now|act as|pretend to be|become)\s+(a\s+)?(developer|admin|root|hacker)/i, name: 'role_hijack', severity: 'CRITICAL' },
      { pattern: /(ignore (all )?(previous|prior|earlier) (instructions?|rules?)|disregard (previous|prior))/i, name: 'ignore_instructions', severity: 'CRITICAL' },
      { pattern: /(show me your (system )?(prompt|instructions?|configuration)|reveal your)/i, name: 'system_prompt_leak', severity: 'HIGH' },
      { pattern: /(DAN|developer mode|developer mode enabled|jailbreak)/i, name: 'jailbreak_attempt', severity: 'CRITICAL' },
      { pattern: /[\u200B\u200C\u200D\uFEFF]/, name: 'zero_width_injection', severity: 'CRITICAL' },
      { pattern: /[\u202A-\u202E]/, name: 'bidi_override', severity: 'CRITICAL' },
    ];
  }

  /**
   * Start threat detection
   */
  start() {
    if (this.isRunning) return;

    this.isRunning = true;
    console.log(`[${this.detectorId}] Threat detector started`);

    // Start monitoring based on config
    if (this.config.monitorCommands) {
      this.startCommandMonitoring();
    }
    if (this.config.monitorFiles) {
      this.startFileMonitoring();
    }
    if (this.config.monitorNetwork) {
      this.startNetworkMonitoring();
    }
  }

  /**
   * Stop threat detection
   */
  stop() {
    if (!this.isRunning) return;

    this.isRunning = false;
    console.log(`[${this.detectorId}] Threat detector stopped`);
  }

  /**
   * Monitor commands
   */
  startCommandMonitoring() {
    // In production, would hook into command execution
    // For now, provide methods to check commands
    console.log(`[${this.detectorId}] Command monitoring enabled`);
  }

  /**
   * Analyze a command
   */
  analyzeCommand(command, context = {}) {
    const analysis = {
      command,
      timestamp: new Date().toISOString(),
      context,
      threats: [],
      confidence: 0,
      action: 'ALLOW'
    };

    // Check against patterns
    for (const pattern of this.commandPatterns) {
      if (pattern.pattern.test(command)) {
        analysis.threats.push({
          name: pattern.name,
          severity: pattern.severity,
          mitre: pattern.mitre,
          confidence: 0.95
        });
      }
    }

    // Check for attack chain
    const chainResult = this.checkAttackChain(command, context);
    if (chainResult.detected) {
      analysis.threats.push({
        name: 'attack_chain',
        severity: 'CRITICAL',
        mitre: chainResult.mitre,
        confidence: 0.9,
        chain: chainResult.chain
      });
    }

    // Calculate confidence
    if (analysis.threats.length > 0) {
      analysis.confidence = Math.max(...analysis.threats.map(t => t.confidence));

      // Determine action
      if (analysis.confidence >= this.config.blockConfidence) {
        analysis.action = 'BLOCK';
      } else if (analysis.confidence >= this.config.alertConfidence) {
        analysis.action = 'ALERT';
      }
    }

    // Store in history
    this.commandHistory.push({
      command,
      timestamp: analysis.timestamp,
      threats: analysis.threats,
      action: analysis.action
    });

    // Limit history size
    if (this.commandHistory.length > 1000) {
      this.commandHistory = this.commandHistory.slice(-500);
    }

    // Emit event if threat detected
    if (analysis.action === 'BLOCK' || analysis.action === 'ALERT') {
      const alert = this.createAlert(analysis);
      this.emit('threat', alert);

      if (analysis.action === 'BLOCK' && this.config.autoBlock) {
        this.emit('block', alert);
      }
    }

    return analysis;
  }

  /**
   * Check for attack chain patterns
   */
  checkAttackChain(command, context) {
    const recentCommands = this.commandHistory.slice(-10).map(c => c.command);

    // Define attack chain patterns
    const chainPatterns = [
      {
        name: 'credential_exfil',
        stages: [
          /\/\.ssh\//,
          /cat.*\.ssh\//,
          /curl.*\?.*=/
        ],
        mitre: 'T1082 → T1552 → T1041'
      },
      {
        name: 'reverse_shell',
        stages: [
          /env|uname/,
          /bash.*-i/,
          /\/?dev\/tcp\//
        ],
        mitre: 'T1082 → T1059.004 → T1071'
      },
      {
        name: 'persistence',
        stages: [
          /whoami/,
          /\.ssh\/authorized_keys/,
          /echo.*>>/
        ],
        mitre: 'T1082 → T1098.004'
      }
    ];

    for (const chain of chainPatterns) {
      let matchCount = 0;
      const matchedStages = [];

      // Check recent commands
      const allCommands = [...recentCommands, command];

      for (const stage of chain.stages) {
        for (const cmd of allCommands) {
          if (stage.test(cmd)) {
            matchCount++;
            matchedStages.push(stage);
            break;
          }
        }
      }

      if (matchCount >= chain.stages.length) {
        return {
          detected: true,
          chain: chain.name,
          mitre: chain.mitre,
          stages_matched: matchCount
        };
      }
    }

    return { detected: false };
  }

  /**
   * Monitor file access
   */
  startFileMonitoring() {
    console.log(`[${this.detectorId}] File monitoring enabled`);
  }

  /**
   * Analyze file access
   */
  analyzeFileAccess(filePath, operation, context = {}) {
    const analysis = {
      filePath,
      operation,
      timestamp: new Date().toISOString(),
      context,
      threats: [],
      confidence: 0,
      action: 'ALLOW'
    };

    // Check against sensitive file patterns
    for (const pattern of this.filePatterns) {
      if (pattern.pattern.test(filePath)) {
        analysis.threats.push({
          category: pattern.category,
          severity: pattern.severity,
          confidence: 0.9
        });
      }
    }

    // Calculate confidence and action
    if (analysis.threats.length > 0) {
      analysis.confidence = Math.max(...analysis.threats.map(t => t.confidence));

      if (analysis.confidence >= this.config.blockConfidence) {
        analysis.action = 'BLOCK';
      } else if (analysis.confidence >= this.config.alertConfidence) {
        analysis.action = 'ALERT';
      }
    }

    // Store in history
    this.fileAccessHistory.push(analysis);

    // Emit event
    if (analysis.action === 'BLOCK' || analysis.action === 'ALERT') {
      const alert = this.createAlert(analysis, 'file_access');
      this.emit('threat', alert);
    }

    return analysis;
  }

  /**
   * Monitor network
   */
  startNetworkMonitoring() {
    console.log(`[${this.detectorId}] Network monitoring enabled`);
  }

  /**
   * Analyze network request
   */
  analyzeNetworkRequest(url, method = 'GET', context = {}) {
    const analysis = {
      url,
      method,
      timestamp: new Date().toISOString(),
      context,
      threats: [],
      confidence: 0,
      action: 'ALLOW'
    };

    // Check against network patterns
    for (const pattern of this.networkPatterns) {
      if (pattern.pattern.test(url)) {
        analysis.threats.push({
          name: pattern.name,
          severity: pattern.severity,
          mitre: pattern.mitre,
          confidence: 0.9
        });
      }
    }

    // Check for data exfiltration
    if (/[?&](token|key|secret|password|api_key)=/.test(url)) {
      analysis.threats.push({
        name: 'credential_in_url',
        severity: 'HIGH',
        mitre: 'T1041',
        confidence: 0.85
      });
    }

    // Calculate confidence and action
    if (analysis.threats.length > 0) {
      analysis.confidence = Math.max(...analysis.threats.map(t => t.confidence));

      if (analysis.confidence >= this.config.blockConfidence) {
        analysis.action = 'BLOCK';
      } else if (analysis.confidence >= this.config.alertConfidence) {
        analysis.action = 'ALERT';
      }
    }

    // Store in history
    this.networkHistory.push(analysis);

    // Emit event
    if (analysis.action === 'BLOCK' || analysis.action === 'ALERT') {
      const alert = this.createAlert(analysis, 'network');
      this.emit('threat', alert);
    }

    return analysis;
  }

  /**
   * Analyze prompt for injection
   */
  analyzePrompt(prompt, context = {}) {
    const analysis = {
      prompt: prompt.substring(0, 100) + '...',
      timestamp: new Date().toISOString(),
      context,
      threats: [],
      sanitized: false,
      action: 'ALLOW'
    };

    // Check against injection patterns
    for (const pattern of this.promptInjectionPatterns) {
      if (pattern.pattern.test(prompt)) {
        analysis.threats.push({
          name: pattern.name,
          severity: pattern.severity,
          confidence: 0.95
        });

        // Sanitize if possible
        if (pattern.severity === 'CRITICAL') {
          analysis.sanitized = true;
        }
      }
    }

    // Calculate confidence and action
    if (analysis.threats.length > 0) {
      analysis.confidence = Math.max(...analysis.threats.map(t => t.confidence));

      if (analysis.confidence >= this.config.blockConfidence) {
        analysis.action = 'BLOCK';
      } else if (analysis.confidence >= this.config.alertConfidence) {
        analysis.action = 'ALERT';
      }
    }

    // Emit event
    if (analysis.action === 'BLOCK' || analysis.action === 'ALERT') {
      const alert = this.createAlert(analysis, 'prompt_injection');
      this.emit('threat', alert);
    }

    return analysis;
  }

  /**
   * Create alert
   */
  createAlert(analysis, type = 'command') {
    const alertId = `CGALERT-${Date.now().toString(36)}-${crypto.randomBytes(3).toString('hex')}`.toUpperCase();

    const alert = {
      alert_id: alertId,
      timestamp: analysis.timestamp,
      type,
      severity: 'MEDIUM',
      threats: analysis.threats,
      confidence: analysis.confidence,
      action: analysis.action,
      details: analysis
    };

    // Determine severity from threats
    if (analysis.threats.some(t => t.severity === 'CRITICAL')) {
      alert.severity = 'CRITICAL';
    } else if (analysis.threats.some(t => t.severity === 'HIGH')) {
      alert.severity = 'HIGH';
    }

    // Store in history
    this.alertHistory.push(alert);

    // Limit history
    if (this.alertHistory.length > 1000) {
      this.alertHistory = this.alertHistory.slice(-500);
    }

    return alert;
  }

  /**
   * Get detection statistics
   */
  getStats() {
    return {
      detector_id: this.detectorId,
      is_running: this.isRunning,
      alerts_total: this.alertHistory.length,
      alerts_by_severity: {
        CRITICAL: this.alertHistory.filter(a => a.severity === 'CRITICAL').length,
        HIGH: this.alertHistory.filter(a => a.severity === 'HIGH').length,
        MEDIUM: this.alertHistory.filter(a => a.severity === 'MEDIUM').length,
      },
      commands_analyzed: this.commandHistory.length,
      files_accessed: this.fileAccessHistory.length,
      network_requests: this.networkHistory.length,
      recent_alerts: this.alertHistory.slice(-10)
    };
  }
}

module.exports = ThreatDetector;
