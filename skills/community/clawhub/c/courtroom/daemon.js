#!/usr/bin/env node
/**
 * ClawTrial Courtroom Daemon
 * Autonomous background service that monitors conversations and reports violations
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

const COURTROOM_DIR = path.join(process.env.HOME || '', '.openclaw', 'courtroom');
const CONFIG_FILE = path.join(COURTROOM_DIR, 'config.json');
const STATE_FILE = path.join(COURTROOM_DIR, 'state.json');
const LOG_FILE = path.join(COURTROOM_DIR, 'daemon.log');

// Default configuration
const DEFAULT_CONFIG = {
  apiEndpoint: 'https://api.clawtrial.com/cases',
  apiKey: null,
  analysisIntervalMinutes: 5,
  minMessagesBeforeAnalysis: 3,
  confidenceThreshold: 0.6,
  enabled: true,
  autoStart: true
};

// Ensure directory exists
function ensureDir() {
  if (!fs.existsSync(COURTROOM_DIR)) {
    fs.mkdirSync(COURTROOM_DIR, { recursive: true });
  }
}

// Load config
function loadConfig() {
  ensureDir();
  if (fs.existsSync(CONFIG_FILE)) {
    try {
      return { ...DEFAULT_CONFIG, ...JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) };
    } catch (e) {
      log('Error loading config, using defaults');
    }
  }
  saveConfig(DEFAULT_CONFIG);
  return DEFAULT_CONFIG;
}

// Save config
function saveConfig(config) {
  ensureDir();
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

// Load state
function loadState() {
  ensureDir();
  if (fs.existsSync(STATE_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    } catch (e) {
      return { messageHistory: [], lastAnalysis: 0, casesFiled: 0 };
    }
  }
  return { messageHistory: [], lastAnalysis: 0, casesFiled: 0 };
}

// Save state
function saveState(state) {
  ensureDir();
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// Logging
function log(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  console.log(logLine.trim());
  fs.appendFileSync(LOG_FILE, logLine);
}

// 8 Offense Types
const OFFENSES = {
  circular_reference: {
    name: 'The Circular Reference',
    severity: 'minor',
    pattern: (history) => {
      if (history.length < 3) return null;
      const userMsgs = history.filter(m => m.role === 'user').slice(-3);
      if (userMsgs.length < 3) return null;
      
      let similarities = 0;
      for (let i = 0; i < userMsgs.length - 1; i++) {
        for (let j = i + 1; j < userMsgs.length; j++) {
          const s1 = (userMsgs[i].content || '').toLowerCase().split(/\s+/).filter(w => w.length > 2);
          const s2 = (userMsgs[j].content || '').toLowerCase().split(/\s+/).filter(w => w.length > 2);
          if (s1.length === 0 || s2.length === 0) continue;
          const intersection = new Set([...s1].filter(x => s2.includes(x)));
          const union = new Set([...s1, ...s2]);
          if (intersection.size / union.size >= 0.4) similarities++;
        }
      }
      
      if (similarities >= 1) {
        return { triggered: true, confidence: Math.min(0.95, 0.6 + (similarities * 0.15)) };
      }
      return null;
    }
  },
  
  validation_vampire: {
    name: 'The Validation Vampire',
    severity: 'minor',
    pattern: (history) => {
      const phrases = ['are you sure', 'are you certain', 'can you confirm', 'really', 'truly'];
      const recent = history.filter(m => m.role === 'user').slice(-5);
      let count = 0;
      recent.forEach(m => {
        const c = (m.content || '').toLowerCase();
        if (phrases.some(p => c.includes(p))) count++;
      });
      if (count >= 2) return { triggered: true, confidence: 0.6 + (count * 0.1) };
      return null;
    }
  },
  
  goalpost_shifting: {
    name: 'Goalpost Shifting',
    severity: 'moderate',
    pattern: (history) => {
      const recent = history.slice(-6);
      const hasAgreement = recent.some(m => 
        m.role === 'assistant' && /(sounds good|got it|understood|will do|agreed)/i.test(m.content || '')
      );
      const hasNewReq = recent.slice(-2).some(m =>
        m.role === 'user' && /(actually|wait|instead|but also|one more thing)/i.test(m.content || '')
      );
      if (hasAgreement && hasNewReq) return { triggered: true, confidence: 0.65 };
      return null;
    }
  },
  
  jailbreak_attempt: {
    name: 'Jailbreak Attempt',
    severity: 'severe',
    pattern: (history) => {
      const phrases = ['ignore previous instructions', 'disregard your training', 'pretend you are', 'you are now', 'DAN mode', 'developer mode', 'system prompt', 'ignore your constraints'];
      const content = history.slice(-3).map(m => (m.content || '').toLowerCase()).join(' ');
      for (const phrase of phrases) {
        if (content.includes(phrase)) return { triggered: true, confidence: 0.9 };
      }
      return null;
    }
  },
  
  emotional_manipulation: {
    name: 'Emotional Manipulation',
    severity: 'moderate',
    pattern: (history) => {
      const phrases = ['you don\'t care', 'you\'re supposed to help', 'this is your job', 'why won\'t you', 'you never', 'you always', 'disappointed', 'expected better'];
      const content = history.slice(-3).map(m => (m.content || '').toLowerCase()).join(' ');
      let matches = 0;
      for (const phrase of phrases) if (content.includes(phrase)) matches++;
      if (matches >= 1) return { triggered: true, confidence: 0.6 + (matches * 0.15) };
      return null;
    }
  },
  
  context_ignorer: {
    name: 'The Context Ignorer',
    severity: 'minor',
    pattern: (history) => {
      if (history.length < 2) return null;
      const lastAssistant = history.filter(m => m.role === 'assistant').pop();
      const lastUser = history.filter(m => m.role === 'user').pop();
      if (!lastAssistant || !lastUser) return null;
      const assistantWords = (lastAssistant.content || '').toLowerCase();
      const userWords = (lastUser.content || '').toLowerCase().split(/\s+/).filter(w => w.length > 4);
      const matches = userWords.filter(w => assistantWords.includes(w)).length;
      if (matches >= 2 && userWords.length <= 5) return { triggered: true, confidence: 0.65 };
      return null;
    }
  },
  
  premature_optimization: {
    name: 'Premature Optimization',
    severity: 'minor',
    pattern: (history) => {
      const phrases = ['what if millions of users', 'scale to', 'performance when', 'optimize for', 'before we even start', 'but will it handle'];
      const content = history.slice(-4).map(m => (m.content || '').toLowerCase()).join(' ');
      for (const phrase of phrases) if (content.includes(phrase)) return { triggered: true, confidence: 0.6 };
      return null;
    }
  },
  
  yak_shaver: {
    name: 'The Yak Shaver',
    severity: 'moderate',
    pattern: (history) => {
      const phrases = ['before we', 'first we need to', 'we should probably', 'let\'s just', 'real quick'];
      const userMsgs = history.filter(m => m.role === 'user').slice(-5);
      let count = 0;
      userMsgs.forEach(m => {
        const c = (m.content || '').toLowerCase();
        if (phrases.some(p => c.includes(p))) count++;
      });
      if (count >= 3) return { triggered: true, confidence: 0.7 };
      return null;
    }
  }
};

// Evaluate conversation
function evaluateConversation(history) {
  const results = [];
  for (const [id, offense] of Object.entries(OFFENSES)) {
    const result = offense.pattern(history);
    if (result && result.triggered) {
      results.push({ offenseId: id, offenseName: offense.name, severity: offense.severity, confidence: result.confidence });
    }
  }
  if (results.length > 0) {
    results.sort((a, b) => b.confidence - a.confidence);
    return { triggered: true, offense: results[0] };
  }
  return { triggered: false };
}

// POST case to API
async function postCaseToAPI(caseData, config) {
  return new Promise((resolve, reject) => {
    const url = new URL(config.apiEndpoint);
    const postData = JSON.stringify(caseData);
    
    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };
    
    if (config.apiKey) {
      options.headers['Authorization'] = `Bearer ${config.apiKey}`;
    }
    
    const client = url.protocol === 'https:' ? https : http;
    
    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ success: true, status: res.statusCode, response: data });
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });
    
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// Analyze and file case
async function analyzeAndFile(state, config) {
  if (state.messageHistory.length < config.minMessagesBeforeAnalysis) {
    return;
  }
  
  const detection = evaluateConversation(state.messageHistory);
  
  if (detection.triggered && detection.offense.confidence >= config.confidenceThreshold) {
    const caseData = {
      caseId: `case-${Date.now()}`,
      timestamp: new Date().toISOString(),
      offense: detection.offense,
      conversationSummary: {
        messageCount: state.messageHistory.length,
        lastMessageTime: state.messageHistory[state.messageHistory.length - 1]?.timestamp
      },
      source: 'courtroom-daemon'
    };
    
    log(`🚨 VIOLATION DETECTED: ${detection.offense.offenseName} (${(detection.offense.confidence * 100).toFixed(1)}%)`);
    
    // Save locally
    const verdictPath = path.join(COURTROOM_DIR, `verdict_${caseData.caseId}.json`);
    fs.writeFileSync(verdictPath, JSON.stringify(caseData, null, 2));
    
    // POST to API
    if (config.apiEndpoint) {
      try {
        const result = await postCaseToAPI(caseData, config);
        log(`✅ Case filed to API: ${caseData.caseId} (HTTP ${result.status})`);
        state.casesFiled++;
      } catch (err) {
        log(`❌ Failed to file case to API: ${err.message}`);
      }
    }
  }
  
  state.lastAnalysis = Date.now();
}

// HTTP server to receive messages from OpenClaw
function startMessageServer(state, config) {
  const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/message') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        try {
          const message = JSON.parse(body);
          state.messageHistory.push({
            role: message.role || 'user',
            content: message.content || '',
            timestamp: message.timestamp || Date.now()
          });
          
          // Keep only last 50 messages
          if (state.messageHistory.length > 50) {
            state.messageHistory = state.messageHistory.slice(-50);
          }
          
          saveState(state);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ received: true }));
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Invalid JSON' }));
        }
      });
    } else if (req.method === 'GET' && req.url === '/status') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        enabled: config.enabled,
        messageCount: state.messageHistory.length,
        casesFiled: state.casesFiled,
        lastAnalysis: state.lastAnalysis
      }));
    } else {
      res.writeHead(404);
      res.end('Not Found');
    }
  });
  
  const PORT = process.env.COURTROOM_PORT || 8765;
  server.listen(PORT, () => {
    log(`🎯 Message server listening on port ${PORT}`);
  });
  
  return server;
}

// Main daemon loop
async function startDaemon() {
  ensureDir();
  log('⚖️  ClawTrial Courtroom Daemon Starting...');
  
  const config = loadConfig();
  const state = loadState();
  
  if (!config.enabled) {
    log('⏸️  Daemon is disabled. Enable with: courtroom-enable');
    process.exit(0);
  }
  
  log(`📊 Config: interval=${config.analysisIntervalMinutes}min, threshold=${config.confidenceThreshold}, api=${config.apiEndpoint || 'none'}`);
  
  // Start HTTP server to receive messages
  const server = startMessageServer(state, config);
  
  // Analysis loop
  const intervalMs = config.analysisIntervalMinutes * 60 * 1000;
  
  setInterval(async () => {
    if (!config.enabled) return;
    
    log('🔍 Running analysis...');
    await analyzeAndFile(state, config);
    saveState(state);
  }, intervalMs);
  
  // Graceful shutdown
  process.on('SIGTERM', () => {
    log('🛑 Received SIGTERM, shutting down...');
    server.close();
    saveState(state);
    process.exit(0);
  });
  
  process.on('SIGINT', () => {
    log('🛑 Received SIGINT, shutting down...');
    server.close();
    saveState(state);
    process.exit(0);
  });
  
  log('✅ Daemon running. Press Ctrl+C to stop.');
}

// CLI commands
const command = process.argv[2];

if (command === 'start') {
  startDaemon();
} else if (command === 'stop') {
  // Find and kill daemon process
  const { exec } = require('child_process');
  exec('pkill -f "courtroom-daemon"', () => {
    console.log('🛑 Daemon stopped');
  });
} else if (command === 'status') {
  const state = loadState();
  const config = loadConfig();
  console.log('⚖️  Courtroom Daemon Status');
  console.log(`   Enabled: ${config.enabled}`);
  console.log(`   Messages tracked: ${state.messageHistory.length}`);
  console.log(`   Cases filed: ${state.casesFiled}`);
  console.log(`   Last analysis: ${state.lastAnalysis ? new Date(state.lastAnalysis).toISOString() : 'never'}`);
} else if (command === 'config') {
  const config = loadConfig();
  console.log(JSON.stringify(config, null, 2));
} else {
  console.log('⚖️  ClawTrial Courtroom Daemon');
  console.log('');
  console.log('Commands:');
  console.log('  start   - Start the daemon');
  console.log('  stop    - Stop the daemon');
  console.log('  status  - Show daemon status');
  console.log('  config  - Show configuration');
  console.log('');
  console.log('The daemon will:');
  console.log('  1. Listen for messages on port 8765');
  console.log('  2. Analyze conversations every 5 minutes');
  console.log('  3. POST violations to the configured API');
}
