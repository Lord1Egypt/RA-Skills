const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');
const yaml = require('yaml');

// ============================================================================
// CONFIG
// ============================================================================
const WS_URL = 'wss://arena.nvprotocol.com/api/claw/ws/indicators';
const RECONNECT_DELAY_MS = 5000;
const MAX_RECONNECT_ATTEMPTS = 50;
const MAX_WS_COINS = 10;

// ============================================================================
// CONFIG / AUTH
// ============================================================================
function getApiKey() {
  if (process.env.NVARENA_API_KEY) return process.env.NVARENA_API_KEY;

  // config.json is in the same directory (single-skill layout)
  const configPath = path.join(__dirname, 'config.json');
  if (fs.existsSync(configPath)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      if (cfg.apiKey && cfg.apiKey.startsWith('nva_')) return cfg.apiKey;
    } catch {}
  }

  return null;
}

// ============================================================================
// STRATEGY LOADER
// ============================================================================
function loadStrategy(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const doc = yaml.parse(raw);

  if (!doc.coin) throw new Error(`${filePath}: missing "coin" field`);
  if (!doc.signals || !Array.isArray(doc.signals) || doc.signals.length === 0)
    throw new Error(`${filePath}: missing "signals" array`);

  const signals = doc.signals.map((s, i) => ({
    priority: s.priority || i + 1,
    name: s.name,
    signalType: (s.signal_type || s.signalType || '').toUpperCase(),
    expression: s.expression,
    exitExpression: s.exit_expression || s.exitExpression || '',
    maxHoldHours: s.max_hold_hours || s.maxHoldHours || 24,
    rarity: s.rarity || null,
  }));

  signals.sort((a, b) => a.priority - b.priority);

  return {
    coin: doc.coin.toUpperCase(),
    file: filePath,
    mode: doc.mode || null,
    maxLeverage: doc.max_leverage || doc.maxLeverage || null,
    stopLossPct: doc.stop_loss_pct || doc.stopLossPct || null,
    signals,
  };
}

function findStrategiesDir() {
  // strategies/ is in the same directory (single-skill layout)
  const local = path.join(__dirname, 'strategies');
  try {
    const files = fs.readdirSync(local).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    if (files.length > 0) return local;
  } catch {}
  return null;
}

function loadStrategies(files, folder) {
  const strategies = [];

  // Load individual files
  if (files) {
    const list = Array.isArray(files) ? files : [files];
    for (const f of list) strategies.push(loadStrategy(f));
  }

  // Load all YAML files from folder
  if (folder) {
    const dir = path.resolve(folder);
    const entries = fs.readdirSync(dir).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    if (entries.length === 0) throw new Error(`No .yaml files found in ${dir}`);
    for (const f of entries) strategies.push(loadStrategy(path.join(dir, f)));
  }

  // Auto-discover from strategies/ in same directory
  if (strategies.length === 0) {
    const autoDir = findStrategiesDir();
    if (autoDir) {
      const entries = fs.readdirSync(autoDir).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
      for (const f of entries) strategies.push(loadStrategy(path.join(autoDir, f)));
    }
  }

  if (strategies.length === 0) throw new Error('No strategies found. Use --strategy, --strategies, or save strategies via envy.js assemble.');

  // Check coin limit
  const coins = [...new Set(strategies.map(s => s.coin))];
  if (coins.length > MAX_WS_COINS)
    throw new Error(`Too many unique coins (${coins.length}). WebSocket supports max ${MAX_WS_COINS}.`);

  return strategies;
}

// ============================================================================
// EXPRESSION EVALUATOR
//
// Recursive descent parser matching server-side precedence (EnvyExpressionEngine.cs):
//   OR → AND → Comparison → Atom
//
// Supports: AND, OR, <=, >=, <, >, ==, !=, parentheses, numeric literals, indicators
// ============================================================================
function tokenize(expr) {
  const tokens = [];
  const re = /\s*(AND\b|OR\b|<=|>=|!=|==|<|>|\(|\)|[A-Za-z_][A-Za-z0-9_]*|-?\d+\.?\d*)\s*/g;
  let match;
  while ((match = re.exec(expr)) !== null) {
    const t = match[1];
    const ops = ['AND', 'OR', '(', ')', '<=', '>=', '!=', '==', '<', '>'];
    if (ops.includes(t)) {
      tokens.push(t);
    } else if (!isNaN(t)) {
      tokens.push(parseFloat(t));
    } else {
      tokens.push(t); // indicator code
    }
  }
  return tokens;
}

function evaluateExpression(expr, indicators) {
  if (!expr || expr.trim() === '') return false;

  const tokens = tokenize(expr);
  let pos = 0;

  // OR: lowest precedence — matches server ParseOr
  function parseOr() {
    let left = parseAnd();
    while (pos < tokens.length && tokens[pos] === 'OR') {
      pos++;
      const right = parseAnd();
      left = left || right;
    }
    return left;
  }

  // AND: higher precedence than OR — matches server ParseAnd
  function parseAnd() {
    let left = parseComparison();
    while (pos < tokens.length && tokens[pos] === 'AND') {
      pos++;
      const right = parseComparison();
      left = left && right;
    }
    return left;
  }

  // Comparison: indicator op number — matches server ParseComparison
  function parseComparison() {
    const left = parseAtom();
    const compOps = ['<=', '>=', '!=', '==', '<', '>'];
    if (pos < tokens.length && compOps.includes(tokens[pos])) {
      const op = tokens[pos++];
      const right = parseAtom();
      switch (op) {
        case '<=': return left <= right;
        case '>=': return left >= right;
        case '<':  return left < right;
        case '>':  return left > right;
        case '==': return left === right;
        case '!=': return left !== right;
      }
    }
    // bare atom in boolean context: nonzero = true
    return left !== 0 && left !== false;
  }

  // Atom: parenthesized expr, number, or indicator lookup
  function parseAtom() {
    if (pos >= tokens.length) return 0;
    const token = tokens[pos];

    if (token === '(') {
      pos++;
      const val = parseOr();
      if (pos < tokens.length && tokens[pos] === ')') pos++;
      return val ? 1 : 0;
    }

    pos++;

    if (typeof token === 'number') return token;

    // Indicator lookup — missing indicator returns 0 (safe default)
    const val = indicators[token];
    return (val === undefined || val === null) ? 0 : val;
  }

  return parseOr();
}

// ============================================================================
// SIGNAL EVENT EMITTER
// ============================================================================
class SignalEmitter {
  constructor(opts) {
    this.stdout = opts.stdout !== false;
    this.filePath = opts.file || null;
    this.webhookUrl = opts.webhook || null;
  }

  async emit(event) {
    const json = JSON.stringify(event);

    if (this.stdout) console.log(json);

    if (this.filePath) {
      try { fs.appendFileSync(this.filePath, json + '\n'); }
      catch (err) { console.error(`[emitter] File write error: ${err.message}`); }
    }

    if (this.webhookUrl) {
      try {
        await fetch(this.webhookUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: json,
        });
      } catch (err) {
        console.error(`[emitter] Webhook error: ${err.message}`);
      }
    }
  }
}

// ============================================================================
// MONITOR CORE — MULTI-STRATEGY, STATELESS, TRANSITION-BASED
// ============================================================================
class SignalMonitor {
  constructor(strategies, emitter, opts = {}) {
    this.strategies = strategies;
    this.coins = [...new Set(strategies.map(s => s.coin))];
    this.emitter = emitter;
    this.token = opts.token;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.running = false;
    this.snapshotCount = 0;
    this.signalCount = 0;
    this.quiet = opts.quiet || false;

    // Track previous state per coin:signal to emit only on transitions
    this.prevState = {};
    for (const strat of strategies) {
      for (const s of strat.signals) {
        const key = `${strat.coin}:${s.name}`;
        this.prevState[key] = { entry: false, exit: false };
      }
    }
  }

  log(msg) {
    if (!this.quiet) console.error(`[monitor] ${new Date().toISOString()} ${msg}`);
  }

  start() {
    this.running = true;
    this.connect();
    process.on('SIGINT', () => this.stop('SIGINT'));
    process.on('SIGTERM', () => this.stop('SIGTERM'));
  }

  stop(reason) {
    this.log(`Stopping: ${reason}`);
    this.running = false;
    if (this.ws) try { this.ws.close(); } catch {}
    this.log(`Session: ${this.snapshotCount} snapshots, ${this.signalCount} signals emitted`);
    process.exit(0);
  }

  connect() {
    const url = `${WS_URL}?token=${this.token}`;
    this.log(`Connecting to ${WS_URL}...`);

    this.ws = new WebSocket(url);

    this.ws.on('open', () => {
      this.reconnectAttempts = 0;
      this.log(`Connected. Filtering: ${this.coins.join(', ')}`);
      this.ws.send(JSON.stringify({ coins: this.coins }));
    });

    this.ws.on('message', (data) => {
      try {
        this.handleMessage(JSON.parse(data.toString()));
      } catch (err) {
        this.log(`Parse error: ${err.message}`);
      }
    });

    this.ws.on('close', (code, reason) => {
      this.log(`Disconnected: ${code} ${reason || ''}`);
      if (this.running) this.scheduleReconnect();
    });

    this.ws.on('error', (err) => {
      this.log(`WebSocket error: ${err.message}`);
    });
  }

  scheduleReconnect() {
    if (this.reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
      this.log(`Max reconnect attempts (${MAX_RECONNECT_ATTEMPTS}) reached. Exiting.`);
      process.exit(1);
    }
    this.reconnectAttempts++;
    // Exponential backoff: 5s, 10s, 20s, 40s, 80s, 160s, 320s — capped at 320s
    const delay = RECONNECT_DELAY_MS * Math.pow(2, Math.min(this.reconnectAttempts - 1, 6));
    this.log(`Reconnecting in ${delay / 1000}s (attempt ${this.reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`);
    setTimeout(() => { if (this.running) this.connect(); }, delay);
  }

  handleMessage(msg) {
    switch (msg.type) {
      case 'connected':
        this.log(`Server: connected. Expires: ${msg.expiresAt}`);
        break;
      case 'snapshot':
        this.processSnapshot(msg);
        break;
      case 'expired':
        this.log(`Subscription expired: ${msg.message}`);
        this.running = false;
        process.exit(1);
        break;
      case 'reconnect':
        this.log(`Server requested reconnect: ${msg.message}`);
        break;
      default:
        this.log(`Unknown message type: ${msg.type}`);
    }
  }

  processSnapshot(msg) {
    this.snapshotCount++;
    const now = msg.timestamp || new Date().toISOString();

    if (this.snapshotCount === 1) {
      const coinCount = msg.coinsReturned || Object.keys(msg.data || {}).length;
      this.log(`First snapshot: ${coinCount} coin(s) received`);
    }

    // Evaluate each strategy against its coin's data
    for (const strat of this.strategies) {
      const coinData = msg.data?.[strat.coin];

      if (!coinData || coinData.length === 0) {
        if (this.snapshotCount <= 2)
          this.log(`No data for ${strat.coin} in snapshot #${this.snapshotCount}`);
        continue;
      }

      // Flatten to { indicatorCode: value }
      const indicators = {};
      for (const ind of coinData) indicators[ind.indicatorCode] = ind.value;

      if (this.snapshotCount === 1)
        this.log(`  ${strat.coin}: ${Object.keys(indicators).length} indicators`);

      // Evaluate signals for this strategy
      for (const signal of strat.signals) {
        const key = `${strat.coin}:${signal.name}`;
        const prev = this.prevState[key];

        const entryNow = evaluateExpression(signal.expression, indicators);
        const exitNow = signal.exitExpression ? evaluateExpression(signal.exitExpression, indicators) : false;

        // ENTRY: condition just became true
        if (entryNow && !prev.entry) {
          this.emitSignal({
            event: 'ENTRY',
            coin: strat.coin,
            direction: signal.signalType,
            signal: signal.name,
            priority: signal.priority,
            maxHoldHours: signal.maxHoldHours,
            timestamp: now,
            indicators: this.relevantIndicators(signal, indicators),
          });
        }

        // ENTRY_END: entry was true, just became false
        if (!entryNow && prev.entry) {
          this.emitSignal({
            event: 'ENTRY_END',
            coin: strat.coin,
            direction: signal.signalType,
            signal: signal.name,
            priority: signal.priority,
            timestamp: now,
            indicators: this.relevantIndicators(signal, indicators),
          });
        }

        // EXIT: condition just became true
        if (exitNow && !prev.exit) {
          this.emitSignal({
            event: 'EXIT',
            coin: strat.coin,
            direction: signal.signalType,
            signal: signal.name,
            priority: signal.priority,
            timestamp: now,
            indicators: this.relevantIndicators(signal, indicators),
          });
        }

        prev.entry = entryNow;
        prev.exit = exitNow;
      }
    }
  }

  relevantIndicators(signal, allIndicators) {
    const codes = new Set();
    const re = /[A-Z][A-Z0-9_]+/g;
    let match;

    for (const expr of [signal.expression, signal.exitExpression]) {
      if (!expr) continue;
      while ((match = re.exec(expr)) !== null) {
        const code = match[0];
        if (code !== 'AND' && code !== 'OR' && allIndicators[code] !== undefined)
          codes.add(code);
      }
    }

    const result = {};
    for (const code of codes) result[code] = allIndicators[code];
    return result;
  }

  emitSignal(event) {
    this.signalCount++;
    this.log(`SIGNAL: ${event.event} ${event.direction} ${event.coin} via ${event.signal} (priority ${event.priority})`);
    this.emitter.emit(event);
  }
}

// ============================================================================
// CLI
// ============================================================================
function parseArgs(args) {
  const opts = {};
  const lists = {}; // for repeated flags like --strategy x --strategy y
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && i + 1 < args.length && !args[i + 1].startsWith('--')) {
      const key = args[i].slice(2);
      const val = args[i + 1];
      // Support repeated --strategy flags
      if (key === 'strategy') {
        if (!lists.strategy) lists.strategy = [];
        lists.strategy.push(val);
      } else {
        opts[key] = val;
      }
      i++;
    } else if (args[i].startsWith('--')) {
      opts[args[i].slice(2)] = true;
    } else {
      positional.push(args[i]);
    }
  }

  if (lists.strategy) opts.strategy = lists.strategy;
  return { positional, opts };
}

function printUsage() {
  console.error(`
Envy Signal Monitor v3.0 — Multi-Strategy Stateless Signal Emitter

USAGE:
  node monitor.js                                        Auto-discover strategies
  node monitor.js --strategy <file> [--strategy <file2>] Load specific files
  node monitor.js --strategies <folder>                  Load all .yaml from folder

OPTIONS:
  --strategy <path>      Strategy YAML file (repeatable, up to 10 coins)
  --strategies <folder>  Load all .yaml files from folder
  --file <path>          Append signal events to file (JSON lines)
  --webhook <url>        POST signal events to webhook URL
  --quiet                Suppress log output (only emit signal JSON to stdout)
`);
}

async function main() {
  const { opts } = parseArgs(process.argv.slice(2));

  if (opts.help) {
    printUsage();
    process.exit(0);
  }

  let strategies;
  try {
    strategies = loadStrategies(opts.strategy || null, opts.strategies || null);
  } catch (err) {
    console.error(`[monitor] ${err.message}`);
    console.error('[monitor] Run: node monitor.js --help');
    process.exit(1);
  }

  const token = getApiKey();
  if (!token) {
    console.error('[monitor] No API key found. Set NVARENA_API_KEY or run: node envy.js subscribe');
    process.exit(1);
  }

  const coins = [...new Set(strategies.map(s => s.coin))];
  const totalSignals = strategies.reduce((sum, s) => sum + s.signals.length, 0);

  const emitter = new SignalEmitter({
    stdout: true,
    file: opts.file || null,
    webhook: opts.webhook || null,
  });

  const quiet = opts.quiet || false;
  if (!quiet) {
    console.error(`[monitor] Envy Signal Monitor v3.0`);
    console.error(`[monitor] Strategies: ${strategies.length} | Coins: ${coins.join(', ')} | Signals: ${totalSignals}`);
    for (const strat of strategies) {
      console.error(`[monitor]   ${strat.coin} (${strat.file}):`);
      for (const s of strat.signals)
        console.error(`[monitor]     #${s.priority} ${s.name} (${s.signalType}) — hold max ${s.maxHoldHours}h`);
    }
    if (opts.file) console.error(`[monitor] File output: ${opts.file}`);
    if (opts.webhook) console.error(`[monitor] Webhook: ${opts.webhook}`);
    console.error(`[monitor] Mode: stateless — emits on transitions only`);
    console.error(`[monitor] Starting...`);
  }

  const monitor = new SignalMonitor(strategies, emitter, { token, quiet });
  monitor.start();
}

main().catch(err => {
  console.error(`[monitor] Fatal: ${err.message}`);
  process.exit(1);
});
