const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const readline = require('readline');
const yaml = require('yaml');

// ============================================================================
// PATHS
// ============================================================================
const CONFIG_FILE = path.join(__dirname, 'controller.yaml');
const STATE_FILE = path.join(__dirname, 'state.json');
const WALLET_FILE = path.join(__dirname, 'wallet.json');
const STRATEGIES_DIR = path.join(__dirname, 'strategies');

// ============================================================================
// CONFIG LOADER
// ============================================================================
function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error(`[controller] No config found. Creating default: ${CONFIG_FILE}`);
    const defaultConfig = `# Envy Controller Config
executor: paper                  # paper | hyperliquid | auto
confirm: false                   # require human confirmation before trades?

risk:
  reserve_pct: 20                # % of balance to keep as cash reserve
  max_positions: 3               # max concurrent open positions
  max_daily_loss_pct: 5          # stop trading for the day if hit
  max_hold_hours: 48             # force close if position held longer (uses lower of this or signal's)
  entry_end_action: hold         # hold | close — what to do when entry signal lost

# Portfolio allocation — % of tradeable capital per coin
# If omitted, equal weight across all coins with strategies
# allocations:
#   BTC: 40
#   ETH: 35
#   SOL: 25
`;
    fs.writeFileSync(CONFIG_FILE, defaultConfig);
  }

  const raw = fs.readFileSync(CONFIG_FILE, 'utf8');
  const doc = yaml.parse(raw);

  return {
    executor: (doc.executor || 'paper').toLowerCase(),
    confirm: doc.confirm || false,
    risk: {
      reservePct: doc.risk?.reserve_pct ?? 20,
      maxPositions: doc.risk?.max_positions ?? 3,
      maxDailyLossPct: doc.risk?.max_daily_loss_pct ?? 5,
      maxHoldHours: doc.risk?.max_hold_hours ?? 48,
      entryEndAction: (doc.risk?.entry_end_action || 'hold').toLowerCase(),
    },
    allocations: doc.allocations || null,
  };
}

// ============================================================================
// STATE MANAGER
// ============================================================================
class StateManager {
  constructor() {
    this.state = {
      positions: [],       // [{ id, coin, direction, signal, entryTime, entryPrice, size, sizeUsd }]
      dailyPnl: 0,
      dailyDate: null,
      tradeHistory: [],    // last 100 trades
      totalPnl: 0,
      totalTrades: 0,
    };
    this.load();
  }

  load() {
    if (fs.existsSync(STATE_FILE)) {
      try {
        this.state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
      } catch {
        console.error('[controller] Corrupt state.json — starting fresh');
      }
    }
    // Reset daily PnL if new day
    const today = new Date().toISOString().slice(0, 10);
    if (this.state.dailyDate !== today) {
      this.state.dailyPnl = 0;
      this.state.dailyDate = today;
    }
  }

  save() {
    fs.writeFileSync(STATE_FILE, JSON.stringify(this.state, null, 2));
  }

  get positions() { return this.state.positions; }
  get dailyPnl() { return this.state.dailyPnl; }
  get openCount() { return this.state.positions.length; }

  hasPosition(coin) {
    return this.state.positions.some(p => p.coin === coin);
  }

  getPosition(coin) {
    return this.state.positions.find(p => p.coin === coin);
  }

  openPosition(pos) {
    this.state.positions.push({
      id: `${pos.coin}_${Date.now()}`,
      coin: pos.coin,
      direction: pos.direction,
      signal: pos.signal,
      priority: pos.priority,
      entryTime: new Date().toISOString(),
      entryPrice: pos.entryPrice,
      size: pos.size,
      sizeUsd: pos.sizeUsd,
      maxHoldHours: pos.maxHoldHours,
    });
    this.state.totalTrades++;
    this.save();
  }

  closePosition(coin, exitPrice, reason) {
    const idx = this.state.positions.findIndex(p => p.coin === coin);
    if (idx === -1) return null;

    const pos = this.state.positions.splice(idx, 1)[0];
    const pnlPct = pos.direction === 'LONG'
      ? ((exitPrice - pos.entryPrice) / pos.entryPrice) * 100
      : ((pos.entryPrice - exitPrice) / pos.entryPrice) * 100;
    const pnlUsd = pos.sizeUsd * (pnlPct / 100);

    this.state.dailyPnl += pnlUsd;
    this.state.totalPnl += pnlUsd;

    const trade = {
      ...pos,
      exitTime: new Date().toISOString(),
      exitPrice,
      pnlPct: Math.round(pnlPct * 100) / 100,
      pnlUsd: Math.round(pnlUsd * 100) / 100,
      reason,
    };

    this.state.tradeHistory.unshift(trade);
    if (this.state.tradeHistory.length > 100) this.state.tradeHistory.pop();

    this.save();
    return trade;
  }

  getExpiredPositions(maxHoldHours) {
    const now = Date.now();
    return this.state.positions.filter(p => {
      const holdMs = now - new Date(p.entryTime).getTime();
      const limit = Math.min(p.maxHoldHours || maxHoldHours, maxHoldHours) * 60 * 60 * 1000;
      return holdMs >= limit;
    });
  }

  summary() {
    return {
      openPositions: this.state.positions.length,
      positions: this.state.positions.map(p => ({
        coin: p.coin,
        direction: p.direction,
        signal: p.signal,
        entryPrice: p.entryPrice,
        sizeUsd: p.sizeUsd,
        holdMinutes: Math.round((Date.now() - new Date(p.entryTime).getTime()) / 60000),
      })),
      dailyPnl: Math.round(this.state.dailyPnl * 100) / 100,
      totalPnl: Math.round(this.state.totalPnl * 100) / 100,
      totalTrades: this.state.totalTrades,
      recentTrades: this.state.tradeHistory.slice(0, 5),
    };
  }
}

// ============================================================================
// BINANCE PRICE FALLBACK
// ============================================================================
async function getBinancePrice(coin) {
  try {
    const symbol = coin.toUpperCase() + 'USDT';
    const res = await fetch(`https://api.binance.com/api/v3/ticker/price?symbol=${symbol}`);
    if (!res.ok) return 0;
    const data = await res.json();
    const price = parseFloat(data.price);
    return isNaN(price) ? 0 : price;
  } catch {
    return 0;
  }
}

// ============================================================================
// EXECUTOR INTERFACE
// ============================================================================

// ── Paper Executor ──
class PaperExecutor {
  constructor(state) {
    this.state = state;
    this.positions = {};
    this.priceCache = {};
    this.logFile = path.join(__dirname, 'paper_trades.jsonl');

    // Restore in-memory positions from state on restart
    for (const pos of state.positions) {
      this.positions[pos.coin] = {
        direction: pos.direction,
        size: pos.size,
        sizeUsd: pos.sizeUsd,
        entryPrice: pos.entryPrice,
      };
    }
  }

  get name() { return 'paper'; }

  get balanceUsd() {
    return this.state.state.paperBalanceUsd ?? 10000;
  }

  set balanceUsd(val) {
    this.state.state.paperBalanceUsd = val;
    this.state.save();
  }

  async init() {
    if (this.state.state.paperBalanceUsd === undefined) {
      this.state.state.paperBalanceUsd = 10000;
      this.state.save();
    }
    console.error(`[executor:paper] Paper trading mode — balance: $${this.balanceUsd.toFixed(2)}`);
  }

  async getBalance() {
    const positionValue = Object.values(this.positions)
      .reduce((sum, p) => sum + p.sizeUsd, 0);
    return {
      equity: this.balanceUsd + positionValue,
      available: this.balanceUsd,
      currency: 'USD',
    };
  }

  async getPositions() {
    return Object.entries(this.positions).map(([coin, p]) => ({
      coin, side: p.direction, size: p.size,
      entryPrice: p.entryPrice, pnl: 0,
    }));
  }

  async getPrice(coin) {
    // 1) Try envy.js snapshot (NVArena indicator)
    try {
      const envyPath = path.join(__dirname, 'envy.js');
      if (fs.existsSync(envyPath)) {
        const result = await execCommand('node', [envyPath, 'snapshot', '--coins', coin, '--indicators', 'CLOSE_PRICE_15M']);
        const data = JSON.parse(result);
        const priceInd = data?.snapshot?.[coin]?.find(i => i.indicatorCode === 'CLOSE_PRICE_15M');
        if (priceInd && priceInd.value > 0) {
          this.priceCache[coin] = priceInd.value;
          return priceInd.value;
        }
      }
    } catch {}

    // 2) Fallback: Binance public ticker
    try {
      const binancePrice = await getBinancePrice(coin);
      if (binancePrice > 0) {
        console.error(`[executor:paper] Price for ${coin} via Binance fallback: $${binancePrice}`);
        this.priceCache[coin] = binancePrice;
        return binancePrice;
      }
    } catch {}

    // 3) Last resort: cached price
    if (this.priceCache[coin] && this.priceCache[coin] > 0) {
      console.error(`[executor:paper] Price for ${coin} via cache (stale): $${this.priceCache[coin]}`);
      return this.priceCache[coin];
    }

    return 0;
  }

  async marketBuy(coin, sizeUsd) {
    const price = await this.getPrice(coin);
    if (price <= 0) {
      console.error(`[executor:paper] SKIP marketBuy ${coin} — price unavailable`);
      return { orderId: null, filled: 0, price: 0 };
    }
    const size = sizeUsd / price;
    this.balanceUsd -= sizeUsd;
    this.positions[coin] = { direction: 'LONG', size, sizeUsd, entryPrice: price };
    const trade = { action: 'BUY', coin, size, sizeUsd, price, timestamp: new Date().toISOString() };
    this.logTrade(trade);
    return { orderId: `paper_${Date.now()}`, filled: size, price };
  }

  async marketSell(coin, sizeUsd) {
    const price = await this.getPrice(coin);
    if (price <= 0) {
      console.error(`[executor:paper] SKIP marketSell ${coin} — price unavailable`);
      return { orderId: null, filled: 0, price: 0 };
    }
    const size = sizeUsd / price;
    this.balanceUsd -= sizeUsd;
    this.positions[coin] = { direction: 'SHORT', size, sizeUsd, entryPrice: price };
    const trade = { action: 'SELL', coin, size, sizeUsd, price, timestamp: new Date().toISOString() };
    this.logTrade(trade);
    return { orderId: `paper_${Date.now()}`, filled: size, price };
  }

  async closePosition(coin) {
    const pos = this.positions[coin];
    if (!pos) return { orderId: null, filled: 0, price: 0 };
    const price = await this.getPrice(coin);
    if (price <= 0) {
      console.error(`[executor:paper] SKIP close ${coin} — price unavailable, position kept open`);
      return { orderId: null, filled: 0, price: 0 };
    }
    this.balanceUsd += pos.sizeUsd;
    const pnlPct = pos.direction === 'LONG'
      ? (price - pos.entryPrice) / pos.entryPrice
      : (pos.entryPrice - price) / pos.entryPrice;
    this.balanceUsd += pos.sizeUsd * pnlPct;
    delete this.positions[coin];
    const trade = { action: 'CLOSE', coin, size: pos.size, price, pnlPct: Math.round(pnlPct * 10000) / 100, timestamp: new Date().toISOString() };
    this.logTrade(trade);
    return { orderId: `paper_${Date.now()}`, filled: pos.size, price };
  }

  logTrade(trade) {
    try { fs.appendFileSync(this.logFile, JSON.stringify(trade) + '\n'); } catch {}
  }
}

// ── Hyperliquid Executor ──
class HyperliquidExecutor {
  constructor(scriptPath, address, privateKey) {
    this.scriptPath = scriptPath;
    this.address = address;
    this.privateKey = privateKey;
  }

  get name() { return 'hyperliquid'; }

  async init() {
    const bal = await this.getBalance();
    console.error(`[executor:hyperliquid] Connected. Equity: $${bal.equity}`);
  }

  async getBalance() {
    const env = { HYPERLIQUID_ADDRESS: this.address };
    const result = await execCommand('node', [this.scriptPath, 'balance'], env);
    return JSON.parse(result);
  }

  async getPositions() {
    const env = { HYPERLIQUID_ADDRESS: this.address };
    const result = await execCommand('node', [this.scriptPath, 'positions'], env);
    return JSON.parse(result);
  }

  async getPrice(coin) {
    const result = await execCommand('node', [this.scriptPath, 'price', coin]);
    const data = JSON.parse(result);
    return data?.price || data?.mid || 0;
  }

  async marketBuy(coin, sizeUsd) {
    const price = await this.getPrice(coin);
    const size = price > 0 ? sizeUsd / price : 0;
    const env = { HYPERLIQUID_PRIVATE_KEY: this.privateKey };
    const result = await execCommand('node', [this.scriptPath, 'market-buy', coin, size.toFixed(6)], env);
    return JSON.parse(result);
  }

  async marketSell(coin, sizeUsd) {
    const price = await this.getPrice(coin);
    const size = price > 0 ? sizeUsd / price : 0;
    const env = { HYPERLIQUID_PRIVATE_KEY: this.privateKey };
    const result = await execCommand('node', [this.scriptPath, 'market-sell', coin, size.toFixed(6)], env);
    return JSON.parse(result);
  }

  async closePosition(coin) {
    const positions = await this.getPositions();
    const pos = (Array.isArray(positions) ? positions : []).find(p =>
      p.coin?.toUpperCase() === coin.toUpperCase());
    if (!pos) return { orderId: null, filled: 0, price: 0 };

    const env = { HYPERLIQUID_PRIVATE_KEY: this.privateKey };
    const size = Math.abs(pos.size || pos.szi || 0);
    const action = (pos.side === 'long' || pos.direction === 'LONG') ? 'market-sell' : 'market-buy';
    const result = await execCommand('node', [this.scriptPath, action, coin, size.toFixed(6)], env);
    return JSON.parse(result);
  }
}

// ============================================================================
// EXECUTOR DISCOVERY
// ============================================================================

/**
 * Find a script in sibling skill folders (for external skills like Hyperliquid).
 * This is the ONLY discovery that scans siblings — everything internal uses __dirname.
 */
function findExternalSkillScript(filename) {
  const skillsDir = path.dirname(__dirname);
  try {
    const siblings = fs.readdirSync(skillsDir);
    for (const name of siblings) {
      const candidate = path.join(skillsDir, name, filename);
      if (fs.existsSync(candidate)) return candidate;
      const scriptsCandidate = path.join(skillsDir, name, 'scripts', filename);
      if (fs.existsSync(scriptsCandidate)) return scriptsCandidate;
    }
  } catch {}
  return null;
}

/**
 * Load wallet credentials from wallet.json (created by envy.js).
 * Returns { address, privateKey } or null if file doesn't exist.
 */
function loadWallet() {
  if (!fs.existsSync(WALLET_FILE)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(WALLET_FILE, 'utf8'));
    if (data.address && data.privateKey) return { address: data.address, privateKey: data.privateKey };
  } catch {}
  return null;
}

function createExecutor(config, state) {
  const type = config.executor;

  if (type === 'paper') {
    return new PaperExecutor(state);
  }

  if (type === 'hyperliquid') {
    const scriptPath = findExternalSkillScript('hyperliquid.mjs');
    if (!scriptPath) throw new Error('Hyperliquid skill not found. Install it: npx clawhub@latest install hyperliquid');

    // Read from wallet.json first, fall back to env vars
    const wallet = loadWallet();
    const address = wallet?.address || process.env.HYPERLIQUID_ADDRESS;
    const privateKey = wallet?.privateKey || process.env.HYPERLIQUID_PRIVATE_KEY;

    if (!privateKey) throw new Error('No wallet found. Run "node envy.js balance" to create one, or set HYPERLIQUID_PRIVATE_KEY env var.');
    if (!address) throw new Error('No wallet address found.');

    console.error(`[controller] Using wallet: ${address.slice(0, 6)}...${address.slice(-4)}`);
    return new HyperliquidExecutor(scriptPath, address, privateKey);
  }

  if (type === 'auto') {
    const scriptPath = findExternalSkillScript('hyperliquid.mjs');
    if (scriptPath) {
      const wallet = loadWallet();
      const address = wallet?.address || process.env.HYPERLIQUID_ADDRESS;
      const privateKey = wallet?.privateKey || process.env.HYPERLIQUID_PRIVATE_KEY;

      if (address && privateKey) {
        console.error(`[controller] Auto-discovered Hyperliquid executor, wallet: ${address.slice(0, 6)}...${address.slice(-4)}`);
        return new HyperliquidExecutor(scriptPath, address, privateKey);
      }
    }
    console.error('[controller] No live executor found — falling back to paper mode');
    return new PaperExecutor(state);
  }

  throw new Error(`Unknown executor: ${type}. Must be: paper, hyperliquid, auto`);
}

// ============================================================================
// HELPER: Shell exec
// ============================================================================
function execCommand(cmd, args, envVars = {}) {
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, {
      env: { ...process.env, ...envVars },
      timeout: 30000,
    });
    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', d => stdout += d);
    proc.stderr.on('data', d => stderr += d);
    proc.on('close', code => {
      if (code !== 0) reject(new Error(`${cmd} exited ${code}: ${stderr}`));
      else resolve(stdout.trim());
    });
    proc.on('error', reject);
  });
}

// ============================================================================
// CONTROLLER CORE
// ============================================================================
class Controller {
  constructor(config, executor, state, coinCount) {
    this.config = config;
    this.executor = executor;
    this.state = state;
    this.coinCount = coinCount;
    this.running = false;
    this.monitorProc = null;
    this.holdCheckInterval = null;
  }

  log(msg) {
    console.error(`[controller] ${new Date().toISOString()} ${msg}`);
  }

  async start() {
    this.running = true;
    this.log(`Envy Controller v1.0`);
    this.log(`Executor: ${this.executor.name}`);
    this.log(`Risk: reserve ${this.config.risk.reservePct}%, max ${this.config.risk.maxPositions} positions, max hold ${this.config.risk.maxHoldHours}h`);
    this.log(`Entry end action: ${this.config.risk.entryEndAction}`);

    await this.executor.init();

    try {
      const bal = await this.executor.getBalance();
      this.log(`Balance: $${bal.equity} (available: $${bal.available})`);
    } catch (err) {
      this.log(`Warning: Could not fetch balance: ${err.message}`);
    }

    await this.syncPositions();

    if (this.state.openCount > 0) {
      this.log(`Resuming with ${this.state.openCount} open position(s):`);
      for (const p of this.state.positions)
        this.log(`  ${p.coin} ${p.direction} via ${p.signal} (${Math.round((Date.now() - new Date(p.entryTime).getTime()) / 60000)}m)`);
    }

    this.holdCheckInterval = setInterval(() => this.checkHoldTimers(), 60000);

    this.startMonitor();

    process.on('SIGINT', () => this.stop('SIGINT'));
    process.on('SIGTERM', () => this.stop('SIGTERM'));
  }

  async stop(reason) {
    this.log(`Stopping: ${reason}`);
    this.running = false;

    if (this.holdCheckInterval) clearInterval(this.holdCheckInterval);
    if (this.monitorProc) {
      this.monitorProc.kill('SIGTERM');
      this.monitorProc = null;
    }

    const summary = this.state.summary();
    this.log(`Session summary:`);
    this.log(`  Open positions: ${summary.openPositions}`);
    this.log(`  Daily P&L: $${summary.dailyPnl}`);
    this.log(`  Total P&L: $${summary.totalPnl}`);
    this.log(`  Total trades: ${summary.totalTrades}`);

    process.exit(0);
  }

  async syncPositions() {
    try {
      const execPositions = await this.executor.getPositions();
      const execCoins = new Set(
        (Array.isArray(execPositions) ? execPositions : [])
          .map(p => (p.coin || '').toUpperCase())
          .filter(Boolean)
      );

      for (const coin of execCoins) {
        if (!this.state.hasPosition(coin)) {
          this.log(`ORPHAN detected on executor: ${coin} — not tracked by controller`);
        }
      }

      for (const pos of this.state.positions) {
        if (!execCoins.has(pos.coin)) {
          this.log(`STALE position in state: ${pos.coin} ${pos.direction} — not found on executor, cleaning up`);
          this.state.closePosition(pos.coin, pos.entryPrice, 'stale_cleanup');
        }
      }
    } catch (err) {
      this.log(`Warning: Could not sync positions: ${err.message}`);
    }
  }

  startMonitor() {
    // monitor.js is in the same directory
    const monitorPath = path.join(__dirname, 'monitor.js');
    if (!fs.existsSync(monitorPath)) {
      this.log('ERROR: Cannot find monitor.js');
      process.exit(1);
    }

    this.log(`Starting monitor: ${monitorPath}`);
    this.monitorProc = spawn('node', [monitorPath], {
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    const rl = readline.createInterface({ input: this.monitorProc.stdout });
    rl.on('line', (line) => {
      try {
        const event = JSON.parse(line);
        this.log(`>> SIGNAL RECEIVED: ${event.event} ${event.direction} ${event.coin} via ${event.signal}`);
        this.processSignal(event);
      } catch (err) {
        this.log(`Failed to parse monitor output: ${line.slice(0, 100)}`);
      }
    });

    const monitorStderr = readline.createInterface({ input: this.monitorProc.stderr });
    monitorStderr.on('line', (line) => {
      console.error(`  [monitor] ${line}`);
    });

    this.monitorProc.on('close', (code) => {
      this.log(`Monitor exited with code ${code}`);
      if (this.running) {
        this.log('Restarting monitor in 5s...');
        setTimeout(() => { if (this.running) this.startMonitor(); }, 5000);
      }
    });
  }

  async processSignal(event) {
    const { event: type, coin, direction, signal, priority, maxHoldHours, indicators } = event;

    switch (type) {
      case 'ENTRY':
        await this.handleEntry(coin, direction, signal, priority, maxHoldHours || this.config.risk.maxHoldHours, indicators);
        break;
      case 'EXIT':
        await this.handleExit(coin, direction, signal, indicators);
        break;
      case 'ENTRY_END':
        await this.handleEntryEnd(coin, direction, signal, indicators);
        break;
      default:
        this.log(`Unknown event type: ${type}`);
    }
  }

  async handleEntry(coin, direction, signal, priority, maxHoldHours, indicators) {
    if (this.state.hasPosition(coin)) {
      this.log(`SKIP ENTRY ${direction} ${coin} via ${signal} — already have ${coin} position`);
      return;
    }

    if (this.state.openCount >= this.config.risk.maxPositions) {
      this.log(`SKIP ENTRY ${direction} ${coin} via ${signal} — max positions (${this.config.risk.maxPositions}) reached`);
      return;
    }

    const bal = await this.executor.getBalance();
    const dailyLossLimit = bal.equity * (this.config.risk.maxDailyLossPct / 100);
    if (Math.abs(this.state.dailyPnl) >= dailyLossLimit && this.state.dailyPnl < 0) {
      this.log(`SKIP ENTRY ${direction} ${coin} via ${signal} — daily loss limit hit ($${Math.round(this.state.dailyPnl)})`);
      return;
    }

    const tradeable = bal.available * (1 - this.config.risk.reservePct / 100);
    const allocation = this.getAllocation(coin);
    const sizeUsd = tradeable * (allocation / 100);

    if (sizeUsd < 1) {
      this.log(`SKIP ENTRY ${direction} ${coin} via ${signal} — position size too small ($${sizeUsd.toFixed(2)})`);
      return;
    }

    this.log(`ENTRY ${direction} ${coin} via ${signal} — size: $${sizeUsd.toFixed(2)}`);

    try {
      let result;
      if (direction === 'LONG') {
        result = await this.executor.marketBuy(coin, sizeUsd);
      } else {
        result = await this.executor.marketSell(coin, sizeUsd);
      }

      // Guard: if executor couldn't get a price, don't record the position
      if (!result.orderId) {
        this.log(`ABORT ENTRY ${direction} ${coin} via ${signal} — executor returned no fill (price unavailable)`);
        return;
      }

      const price = result.price || 0;
      const holdLimit = Math.min(maxHoldHours, this.config.risk.maxHoldHours);

      this.state.openPosition({
        coin, direction, signal, priority,
        entryPrice: price,
        size: result.filled || 0,
        sizeUsd,
        maxHoldHours: holdLimit,
      });

      this.log(`FILLED ${direction} ${coin} @ $${price} (size: ${result.filled}, order: ${result.orderId})`);

      console.log(JSON.stringify({
        event: 'POSITION_OPENED',
        coin, direction, signal, priority,
        price, sizeUsd: Math.round(sizeUsd * 100) / 100,
        maxHoldHours: holdLimit,
        timestamp: new Date().toISOString(),
      }));
    } catch (err) {
      this.log(`ERROR executing ${direction} ${coin}: ${err.message}`);
    }
  }

  async handleExit(coin, direction, signal, indicators) {
    if (!this.state.hasPosition(coin)) return;

    const pos = this.state.getPosition(coin);

    this.log(`EXIT ${coin} via ${signal} — closing ${pos.direction} position`);

    try {
      const result = await this.executor.closePosition(coin);

      // Guard: if executor couldn't close (price unavailable), don't remove from state
      if (!result.orderId) {
        this.log(`DEFER EXIT ${coin} — price unavailable, will retry on next signal or hold timer`);
        return;
      }

      const exitPrice = result.price || 0;
      const trade = this.state.closePosition(coin, exitPrice, 'exit_signal');

      if (trade) {
        this.log(`CLOSED ${pos.direction} ${coin} @ $${exitPrice} | P&L: ${trade.pnlPct}% ($${trade.pnlUsd})`);

        console.log(JSON.stringify({
          event: 'POSITION_CLOSED',
          coin, direction: pos.direction, signal,
          entryPrice: trade.entryPrice,
          exitPrice,
          pnlPct: trade.pnlPct,
          pnlUsd: trade.pnlUsd,
          reason: 'exit_signal',
          holdMinutes: Math.round((Date.now() - new Date(trade.entryTime).getTime()) / 60000),
          timestamp: new Date().toISOString(),
        }));
      }
    } catch (err) {
      this.log(`ERROR closing ${coin}: ${err.message}`);
    }
  }

  async handleEntryEnd(coin, direction, signal, indicators) {
    if (!this.state.hasPosition(coin)) return;

    const action = this.config.risk.entryEndAction;

    if (action === 'close') {
      this.log(`ENTRY_END ${coin} via ${signal} — entry lost, closing per config`);
      await this.handleExit(coin, direction, signal, indicators);
    } else {
      this.log(`ENTRY_END ${coin} via ${signal} — entry lost, holding per config`);
    }
  }

  async checkHoldTimers() {
    const expired = this.state.getExpiredPositions(this.config.risk.maxHoldHours);

    for (const pos of expired) {
      this.log(`MAX HOLD exceeded: ${pos.coin} ${pos.direction} (${Math.round((Date.now() - new Date(pos.entryTime).getTime()) / 3600000)}h) — force closing`);

      try {
        const result = await this.executor.closePosition(pos.coin);

        // Guard: if executor couldn't close, skip — will retry next minute
        if (!result.orderId) {
          this.log(`DEFER force close ${pos.coin} — price unavailable, will retry next cycle`);
          continue;
        }

        const exitPrice = result.price || 0;
        const trade = this.state.closePosition(pos.coin, exitPrice, 'max_hold_exceeded');

        if (trade) {
          this.log(`FORCE CLOSED ${pos.direction} ${pos.coin} @ $${exitPrice} | P&L: ${trade.pnlPct}% ($${trade.pnlUsd})`);

          console.log(JSON.stringify({
            event: 'POSITION_CLOSED',
            coin: pos.coin, direction: pos.direction, signal: pos.signal,
            entryPrice: trade.entryPrice,
            exitPrice,
            pnlPct: trade.pnlPct,
            pnlUsd: trade.pnlUsd,
            reason: 'max_hold_exceeded',
            holdMinutes: Math.round((Date.now() - new Date(trade.entryTime).getTime()) / 60000),
            timestamp: new Date().toISOString(),
          }));
        }
      } catch (err) {
        this.log(`ERROR force closing ${pos.coin}: ${err.message}`);
      }
    }
  }

  getAllocation(coin) {
    if (this.config.allocations && this.config.allocations[coin] !== undefined) {
      return this.config.allocations[coin];
    }
    return 100 / (this.coinCount || this.config.risk.maxPositions);
  }
}

// ============================================================================
// CLI
// ============================================================================
function parseArgs(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && i + 1 < args.length && !args[i + 1].startsWith('--')) {
      opts[args[i].slice(2)] = args[i + 1];
      i++;
    } else if (args[i].startsWith('--')) {
      opts[args[i].slice(2)] = true;
    }
  }
  return opts;
}

function printUsage() {
  console.error(`
Envy Controller v1.1

USAGE:
  node controller.js                    Start with controller.yaml config
  node controller.js --status           Show current positions and P&L
  node controller.js --reset            Clear all positions, P&L, and trade history
  node controller.js --help             Show this help

CONFIG:
  Edit controller.yaml to set executor, risk rules, and allocations.
  Default config is created on first run.

EXECUTORS:
  paper              Simulated trading, no real funds (default)
  hyperliquid        Live trading via Hyperliquid skill (install separately)
  auto               Try Hyperliquid, fall back to paper

WALLET:
  Reads wallet from wallet.json (created by envy.js) automatically.
  No need to set environment variables for Hyperliquid trading.
  To go live: install hyperliquid skill, set executor to hyperliquid, fund wallet on Hyperliquid.
`);
}

function countStrategyCoins() {
  try {
    const files = fs.readdirSync(STRATEGIES_DIR).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    return files.length;
  } catch {}
  return 0;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));

  if (opts.help) {
    printUsage();
    process.exit(0);
  }

  // Reset: clear state and trade log
  if (opts.reset) {
    const files = [STATE_FILE, path.join(__dirname, 'paper_trades.jsonl')];
    for (const f of files) {
      if (fs.existsSync(f)) {
        fs.unlinkSync(f);
        console.error(`[controller] Deleted: ${f}`);
      }
    }
    console.error('[controller] State reset. Positions, P&L, and trade history cleared.');
    process.exit(0);
  }

  const config = loadConfig();
  const state = new StateManager();

  if (opts.status) {
    const summary = state.summary();
    console.log(JSON.stringify(summary, null, 2));
    process.exit(0);
  }

  let executor;
  try {
    executor = createExecutor(config, state);
  } catch (err) {
    console.error(`[controller] Executor error: ${err.message}`);
    process.exit(1);
  }

  const coinCount = countStrategyCoins();

  const controller = new Controller(config, executor, state, coinCount);
  await controller.start();
}

main().catch(err => {
  console.error(`[controller] Fatal: ${err.message}`);
  process.exit(1);
});