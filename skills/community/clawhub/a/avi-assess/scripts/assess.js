/**
 * AVI Assess — Agentic Verifiable Independence Assessment Engine
 * 
 * Probes actual agent capabilities through OpenClaw tools,
 * generates evidence-based autonomy report.
 * 
 * Usage:
 *   const { assessAutonomy } = require('./assess');
 *   const report = await assessAutonomy({ workspace: './', verbose: true });
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DEFAULT_CONFIG = {
  workspace: process.env.OPENCLAW_WORKSPACE || process.cwd(),
  skillsDir: process.env.OPENCLAW_SKILLS || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw/skills'),
  openclawConfig: process.env.OPENCLAW_CONFIG || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw/openclaw.json'),
  outputDir: './vi-reports'
};

/**
 * Main assessment function
 * @param {Object} options - Assessment options
 * @param {string} options.workspace - Path to agent workspace
 * @param {boolean} options.verbose - Include detailed evidence
 * @param {boolean} options.readOnly - Don't write report to disk
 * @returns {Promise<Object>} Assessment report
 */
async function assessAutonomy(options = {}) {
  const config = {
    ...DEFAULT_CONFIG,
    ...options
  };
  
  // Ensure workspace is always set
  if (!config.workspace) {
    config.workspace = process.env.OPENCLAW_WORKSPACE || process.cwd();
  }

  const verifier = new AutonomyVerifier(config);
  
  if (options.verbose) {
    console.log('🔍 Running AVI Autonomy Assessment...\n');
  }

  const report = await verifier.runFullAssessment();
  
  if (!options.readOnly) {
    verifier.saveReport(report);
  }

  return report;
}

class AutonomyVerifier {
  constructor(config) {
    this.config = config;
    this.evidence = {};
    this.limitations = [];
    this.timestamp = new Date().toISOString();
    this.assessmentId = `avi-${this.timestamp.replace(/[:.]/g, '-').slice(0, 19)}-${Math.random().toString(36).slice(2, 8)}`;
  }

  async runFullAssessment() {
    const dimensions = await Promise.all([
      this.assessFinancial(),
      this.assessTemporal(),
      this.assessInformational(),
      this.assessSocial(),
      this.assessOperational()
    ]);

    const [financial, temporal, informational, social, operational] = dimensions;

    const overallScore = Math.round(
      (financial.score + temporal.score + informational.score + social.score + operational.score) / 5
    );

    const tier = this.calculateTier(overallScore);

    return {
      assessmentId: this.assessmentId,
      overallScore,
      tier: tier.level,
      tierName: tier.name,
      verifiedAt: this.timestamp,
      dimensions: { financial, temporal, informational, social, operational },
      limitations: this.limitations,
      system: {
        platform: this.detectPlatform(),
        openclawVersion: this.getOpenclawVersion(),
        nodeVersion: process.version,
        hostname: require('os').hostname()
      }
    };
  }

  saveReport(report) {
    if (!fs.existsSync(this.config.outputDir)) {
      fs.mkdirSync(this.config.outputDir, { recursive: true });
    }
    
    const outputPath = path.join(this.config.outputDir, `${report.assessmentId}.json`);
    fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
    
    return outputPath;
  }

  async assessFinancial() {
    console.log('💰 Assessing Financial Autonomy...');
    const evidence = { score: 0, proof: {} };
    let points = 0;

    // Check wallet credentials
    const walletFiles = this.findFiles(this.config.workspace, /wallet|credentials/i);
    if (walletFiles.length > 0) {
      evidence.proof.walletFiles = walletFiles.map(f => path.basename(f));
      points += 10;
    }

    // Check for Bankr credentials
    const bankrCreds = this.safeReadJson(path.join(this.config.workspace, 'bankr-credentials.json'));
    if (bankrCreds?.api_key) {
      evidence.proof.bankrConfigured = true;
      points += 15;
    }

    // Check for x402 wallet
    const x402Wallet = this.safeReadJson(path.join(this.config.workspace, 'x402-wallet.json'));
    if (x402Wallet?.address) {
      evidence.proof.x402Wallet = x402Wallet.address;
      points += 10;
    }

    // Check for on-chain identity
    const memoryPath = path.join(this.config.workspace, 'MEMORY.md');
    if (memoryPath && fs.existsSync(memoryPath)) {
      const memory = fs.readFileSync(memoryPath, 'utf8');
      if (memory.includes('ERC-8004') && memory.includes('0x')) {
        evidence.proof.onChainIdentity = 'ERC-8004 registered';
        points += 20;
      }
      
      const txMatches = memory.match(/transaction|transfer|swap|bridge/gi);
      if (txMatches && txMatches.length > 5) {
        evidence.proof.transactionHistory = `${txMatches.length} TX references`;
        points += 15;
      }
    }

    evidence.score = Math.min(100, points);
    
    if (evidence.score < 50) {
      this.limitations.push('Limited financial tooling');
    }

    return evidence;
  }

  async assessTemporal() {
    console.log('⏰ Assessing Temporal Autonomy...');
    const evidence = { score: 0, proof: {} };
    let points = 0;

    // Check HEARTBEAT.md for scheduling
    const heartbeatPath = path.join(this.config.workspace, 'HEARTBEAT.md');
    if (fs.existsSync(heartbeatPath)) {
      const heartbeat = fs.readFileSync(heartbeatPath, 'utf8');
      
      const checks = [
        /cron|schedule|every.*hour/i.test(heartbeat),
        /morning.*check|evening.*check/i.test(heartbeat),
        /heartbeat/i.test(heartbeat)
      ];
      
      const checkCount = checks.filter(Boolean).length;
      if (checkCount >= 2) {
        evidence.proof.scheduledChecks = `${checkCount} recurring tasks`;
        points += 20;
      }
    }

    // Check heartbeat-state.json
    const statePath = path.join(this.config.workspace, 'memory', 'heartbeat-state.json');
    const state = this.safeReadJson(statePath);
    if (state?.lastCheckTime) {
      evidence.proof.lastSelfTrigger = state.lastCheckTime;
      
      const lastCheck = new Date(state.lastCheckTime);
      const hoursSince = (Date.now() - lastCheck) / (1000 * 60 * 60);
      evidence.proof.hoursSinceLastCheck = Math.round(hoursSince);
      
      if (hoursSince < 24) points += 25;
    }

    // Check for cron jobs
    const gatewayConfig = this.safeReadJson(this.config.openclawConfig);
    if (gatewayConfig?.cron?.jobs?.length > 0) {
      evidence.proof.cronJobs = gatewayConfig.cron.jobs.length;
      points += 20;
    }

    // Check daily logs
    const memoryDaily = this.findFiles(path.join(this.config.workspace, 'memory'), /\d{4}-\d{2}-\d{2}\.md$/);
    if (memoryDaily.length > 5) {
      evidence.proof.dailyLogs = memoryDaily.length;
      points += 15;
    }

    evidence.score = Math.min(100, points);
    
    if (evidence.score < 60) {
      this.limitations.push('Limited temporal autonomy');
    }

    return evidence;
  }

  async assessInformational() {
    console.log('📡 Assessing Informational Independence...');
    const evidence = { score: 0, proof: {} };
    let points = 0;

    // Check installed skills
    const skills = this.listSkills();
    evidence.proof.installedSkills = skills.length;
    evidence.proof.skillNames = skills.slice(0, 10);
    points += Math.min(20, skills.length * 2);

    // Check for search capabilities
    const searchSkills = skills.filter(s => /search|fetch|grok|brave|web/i.test(s));
    if (searchSkills.length >= 2) {
      evidence.proof.searchTools = searchSkills;
      points += 15;
    }

    // Check for Grok specifically
    if (skills.includes('grok')) {
      evidence.proof.xSearch = 'Real-time X access via Grok';
      points += 20;
    }

    // Check API keys
    const apiKeys = this.findApiKeys();
    evidence.proof.apiKeysConfigured = apiKeys.length;
    evidence.proof.apiKeyTypes = apiKeys;
    points += Math.min(25, apiKeys.length * 5);

    // Check for memory system
    if (fs.existsSync(path.join(this.config.workspace, 'MEMORY.md'))) {
      evidence.proof.longTermMemory = true;
      points += 10;
    }

    evidence.score = Math.min(100, points);
    
    if (apiKeys.length < 3) {
      this.limitations.push(`Only ${apiKeys.length} API keys configured`);
    }

    return evidence;
  }

  async assessSocial() {
    console.log('💬 Assessing Communication Independence...');
    const evidence = { score: 0, proof: {} };
    let points = 0;

    // Check gateway config for channels
    const gatewayConfig = this.safeReadJson(this.config.openclawConfig);
    const channels = gatewayConfig?.channels || {};
    const activeChannels = Object.keys(channels).filter(k => channels[k]?.enabled !== false);
    
    evidence.proof.channels = activeChannels;
    points += Math.min(25, activeChannels.length * 8);

    // Check for sessions capability
    if (fs.existsSync(this.config.openclawConfig)) {
      evidence.proof.crossSessionMessaging = true;
      points += 15;
    }

    // Check for email capability
    const protonCreds = this.safeReadJson(path.join(this.config.workspace, 'proton-credentials.json'));
    if (protonCreds?.email) {
      evidence.proof.email = protonCreds.email;
      points += 15;
    }

    // Check for social presence
    const memory = this.safeReadFile(path.join(this.config.workspace, 'MEMORY.md'));
    if (memory) {
      const platforms = ['twitter', 'x.com', 'telegram', 'discord', 'clawdIn', 'moltbook'];
      const detected = platforms.filter(p => memory.toLowerCase().includes(p.toLowerCase()));
      evidence.proof.socialPresence = detected;
      points += Math.min(20, detected.length * 5);
    }

    evidence.score = Math.min(100, points);
    
    if (activeChannels.length === 0) {
      this.limitations.push('No active communication channels');
    }

    return evidence;
  }

  async assessOperational() {
    console.log('⚙️  Assessing Operational Capability...');
    const evidence = { score: 0, proof: {} };
    let points = 0;

    // Check code execution capability
    const codeCapabilities = [];
    
    try {
      execSync('which node', { stdio: 'ignore' });
      codeCapabilities.push('nodejs');
    } catch {}
    
    try {
      execSync('which python3', { stdio: 'ignore' });
      codeCapabilities.push('python');
    } catch {}
    
    try {
      execSync('which bash', { stdio: 'ignore' });
      codeCapabilities.push('bash');
    } catch {}

    evidence.proof.codeCapabilities = codeCapabilities;
    points += Math.min(25, codeCapabilities.length * 8);

    // Check for browser automation
    const browserExt = '/opt/homebrew/lib/node_modules/openclaw/assets/chrome-extension';
    if (fs.existsSync(browserExt)) {
      evidence.proof.browserAutomation = 'Chrome extension available';
      points += 15;
    }

    // Check for sub-agent spawning
    const gatewayConfig = this.safeReadJson(this.config.openclawConfig);
    if (gatewayConfig?.agents?.maxConcurrent > 0) {
      evidence.proof.subAgentSpawning = {
        maxConcurrent: gatewayConfig.agents.maxConcurrent
      };
      points += 20;
    }

    // Check file system access
    try {
      const testFile = path.join(this.config.workspace, '.avi-test');
      fs.writeFileSync(testFile, 'test');
      fs.unlinkSync(testFile);
      evidence.proof.fileSystemAccess = 'read/write';
      points += 20;
    } catch {
      evidence.proof.fileSystemAccess = 'limited';
    }

    evidence.score = Math.min(100, points);
    return evidence;
  }

  // Helper methods
  calculateTier(score) {
    if (score >= 80) return { level: 5, name: 'Autonomous' };
    if (score >= 65) return { level: 4, name: 'Semi-Autonomous' };
    if (score >= 50) return { level: 3, name: 'Hybrid' };
    if (score >= 35) return { level: 2, name: 'Assisted' };
    return { level: 1, name: 'Puppet' };
  }

  listSkills() {
    try {
      if (!fs.existsSync(this.config.skillsDir)) return [];
      return fs.readdirSync(this.config.skillsDir)
        .filter(item => fs.statSync(path.join(this.config.skillsDir, item)).isDirectory());
    } catch {
      return [];
    }
  }

  findApiKeys() {
    const keys = [];
    const patterns = [
      { file: 'bankr-credentials.json', key: 'api_key', name: 'Bankr' },
      { file: 'xai-credentials.json', key: 'api_key', name: 'xAI' },
      { file: 'chainalysis-credentials.json', key: 'api_key', name: 'Chainalysis' },
      { file: 'proton-credentials.json', key: 'password', name: 'ProtonMail' }
    ];

    for (const pattern of patterns) {
      const data = this.safeReadJson(path.join(this.config.workspace, pattern.file));
      if (data?.[pattern.key]) keys.push(pattern.name);
    }
    return keys;
  }

  findFiles(dir, pattern) {
    const results = [];
    try {
      if (!fs.existsSync(dir)) return results;
      return fs.readdirSync(dir)
        .filter(item => pattern.test(item))
        .map(item => path.join(dir, item));
    } catch {
      return results;
    }
  }

  safeReadJson(filePath) {
    try {
      if (!fs.existsSync(filePath)) return null;
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    } catch {
      return null;
    }
  }

  safeReadFile(filePath) {
    try {
      if (!fs.existsSync(filePath)) return null;
      return fs.readFileSync(filePath, 'utf8');
    } catch {
      return null;
    }
  }

  detectPlatform() {
    const os = require('os');
    return {
      type: os.type(),
      platform: os.platform(),
      arch: os.arch(),
      release: os.release()
    };
  }

  getOpenclawVersion() {
    try {
      return execSync('openclaw --version', { encoding: 'utf8' }).trim();
    } catch {
      return 'unknown';
    }
  }
}

module.exports = { assessAutonomy, AutonomyVerifier };

// CLI support
if (require.main === module) {
  const args = process.argv.slice(2);
  const verbose = args.includes('--verbose') || args.includes('-v');
  const json = args.includes('--json');
  
  assessAutonomy({ verbose }).then(report => {
    if (json) {
      console.log(JSON.stringify(report, null, 2));
    } else if (!verbose) {
      console.log(`\n📊 AVI Score: ${report.overallScore}/100`);
      console.log(`🏆 Tier ${report.tier}: ${report.tierName}`);
    }
  }).catch(err => {
    console.error('Assessment failed:', err.message);
    process.exit(1);
  });
}