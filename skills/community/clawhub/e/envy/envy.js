const fs = require('fs');
const crypto = require('crypto');
const path = require('path');
const { ethers } = require('ethers');

// ============================================================================
// CONFIG
// ============================================================================
const API_BASE = 'https://arena.nvprotocol.com';
const WALLET_FILE = __dirname + '/wallet.json';
const CONFIG_FILE = __dirname + '/config.json';
const ARBITRUM_RPC = 'https://arb1.arbitrum.io/rpc';
const USDC_ADDRESS = '0xaf88d065e77c8cC2239327C5EDb3A432268e5831';
const CHAIN_ID = 42161;

// Data directories
const SIGNALS_DIR = path.join(__dirname, 'signals');
const STRATEGIES_DIR = path.join(__dirname, 'strategies');
const ARCHIVE_DIR = path.join(__dirname, 'archive');

const USDC_DOMAIN = {
  name: 'USD Coin',
  version: '2',
  chainId: CHAIN_ID,
  verifyingContract: USDC_ADDRESS,
};

const TRANSFER_WITH_AUTH_TYPES = {
  TransferWithAuthorization: [
    { name: 'from', type: 'address' },
    { name: 'to', type: 'address' },
    { name: 'value', type: 'uint256' },
    { name: 'validAfter', type: 'uint256' },
    { name: 'validBefore', type: 'uint256' },
    { name: 'nonce', type: 'bytes32' },
  ],
};

const ERC20_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function decimals() view returns (uint8)',
];

// ============================================================================
// DIRECTORY HELPERS
// ============================================================================
function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function saveSignal(coin, name, yamlContent) {
  ensureDir(SIGNALS_DIR);
  const safeName = name.replace(/[^a-zA-Z0-9_-]/g, '_').toLowerCase();
  const file = path.join(SIGNALS_DIR, `${coin.toLowerCase()}_${safeName}.yaml`);
  fs.writeFileSync(file, yamlContent);
  return file;
}

function savePack(coin, packType, yamlContent) {
  ensureDir(SIGNALS_DIR);
  const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const file = path.join(SIGNALS_DIR, `${coin.toLowerCase()}_pack_${packType}_${ts}.yaml`);
  fs.writeFileSync(file, yamlContent);
  return file;
}

function saveStrategy(coin, yamlContent) {
  ensureDir(STRATEGIES_DIR);
  const file = path.join(STRATEGIES_DIR, `${coin.toLowerCase()}.yaml`);
  // If strategy already exists, archive the old one
  if (fs.existsSync(file)) {
    ensureDir(ARCHIVE_DIR);
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const archiveFile = path.join(ARCHIVE_DIR, `${coin.toLowerCase()}_${ts}.yaml`);
    fs.renameSync(file, archiveFile);
  }
  fs.writeFileSync(file, yamlContent);
  return file;
}

// ============================================================================
// CONFIG MANAGEMENT
// ============================================================================
function loadConfig() {
  if (fs.existsSync(CONFIG_FILE)) {
    try { return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')); } catch {}
  }
  return {};
}

function saveConfig(cfg) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2));
}

function getApiKey() {
  // Environment variable takes priority
  if (process.env.NVARENA_API_KEY) return process.env.NVARENA_API_KEY;
  const cfg = loadConfig();
  return cfg.apiKey || null;
}

function setApiKey(key) {
  const cfg = loadConfig();
  cfg.apiKey = key;
  saveConfig(cfg);
}

// ============================================================================
// WALLET
// ============================================================================
function loadOrCreateWallet() {
  if (fs.existsSync(WALLET_FILE)) {
    try {
      const data = JSON.parse(fs.readFileSync(WALLET_FILE, 'utf8'));
      return new ethers.Wallet(data.privateKey);
    } catch {}
  }
  const wallet = ethers.Wallet.createRandom();
  fs.writeFileSync(WALLET_FILE, JSON.stringify({
    address: wallet.address,
    privateKey: wallet.privateKey,
    mnemonic: wallet.mnemonic.phrase,
  }, null, 2));
  return wallet;
}

async function getUsdcBalance(address) {
  const provider = new ethers.JsonRpcProvider(ARBITRUM_RPC);
  const usdc = new ethers.Contract(USDC_ADDRESS, ERC20_ABI, provider);
  const [balance, decimals] = await Promise.all([
    usdc.balanceOf(address),
    usdc.decimals(),
  ]);
  return { raw: balance, formatted: ethers.formatUnits(balance, decimals), decimals };
}

// ============================================================================
// API CALLS
// ============================================================================

/** GET/POST a free endpoint (no auth) */
async function callFree(path, opts = {}) {
  const res = await fetch(`${API_BASE}${path}`, opts);
  const ct = res.headers.get('content-type') || '';
  return ct.includes('yaml') ? await res.text() : await res.json();
}

/** Call a paid endpoint using X-API-KEY subscription token */
async function callWithKey(path, opts = {}) {
  const apiKey = getApiKey();
  if (!apiKey) {
    console.error(JSON.stringify({
      error: 'No API key configured',
      message: 'Run: node envy.js subscribe   (x402 payment)\n   or: node envy.js set-key <your_key>\n   or: node envy.js referral-redeem --wallet 0x... --code XXXX',
    }, null, 2));
    process.exit(1);
  }

  const headers = { 'X-API-KEY': apiKey, ...(opts.headers || {}) };
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers });

  if (res.status === 402) {
    const body = await res.json();
    console.error(JSON.stringify({
      error: 'Insufficient credits or expired subscription',
      ...body,
      tip: 'Check balance: node envy.js status\nBuy credits: node envy.js buy-credits --amount 10',
    }, null, 2));
    process.exit(1);
  }

  const ct = res.headers.get('content-type') || '';
  return ct.includes('yaml') ? await res.text() : await res.json();
}

/** x402 per-request payment flow */
async function callWithX402(path, opts = {}) {
  const wallet = loadOrCreateWallet();

  // First request — expect 402
  const res402 = await fetch(`${API_BASE}${path}`, opts);
  if (res402.status !== 402) {
    const ct = res402.headers.get('content-type') || '';
    return ct.includes('yaml') ? await res402.text() : await res402.json();
  }

  const requirements = await res402.json();
  const req = requirements.paymentRequirements[0];
  const amount = BigInt(req.maxAmountRequired);
  const now = Math.floor(Date.now() / 1000);
  const nonce = '0x' + crypto.randomBytes(32).toString('hex');

  const message = {
    from: wallet.address,
    to: req.payTo,
    value: amount,
    validAfter: 0,
    validBefore: now + 300,
    nonce,
  };

  const signature = await wallet.signTypedData(USDC_DOMAIN, TRANSFER_WITH_AUTH_TYPES, message);
  const sig = ethers.Signature.from(signature);

  const payload = {
    from: message.from,
    to: message.to,
    value: amount.toString(),
    validAfter: message.validAfter,
    validBefore: message.validBefore,
    nonce,
    v: sig.v,
    r: sig.r,
    s: sig.s,
    network: req.network,
    scheme: 'exact',
  };

  const encoded = Buffer.from(JSON.stringify(payload)).toString('base64');
  const headers = { 'X-PAYMENT': encoded, ...(opts.headers || {}) };
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers });

  const ct = res.headers.get('content-type') || '';
  return ct.includes('yaml') ? await res.text() : await res.json();
}

/** Smart caller: uses API key if available, falls back to x402 */
async function callPaid(path, opts = {}) {
  const apiKey = getApiKey();
  if (apiKey) return callWithKey(path, opts);
  return callWithX402(path, opts);
}

/** POST with YAML body */
async function postYaml(path, yamlBody) {
  return callPaid(path, {
    method: 'POST',
    headers: { 'Content-Type': 'text/yaml' },
    body: yamlBody,
  });
}

// ============================================================================
// OUTPUT
// ============================================================================
function out(data) {
  if (typeof data === 'string') {
    console.log(data); // YAML
  } else {
    console.log(JSON.stringify(data, null, 2));
  }
}

// ============================================================================
// CLI COMMANDS
// ============================================================================
const commands = {

  // ── Setup ──

  async 'balance'() {
    const wallet = loadOrCreateWallet();
    const bal = await getUsdcBalance(wallet.address);
    out({
      address: wallet.address,
      usdc: bal.formatted,
      remainingX402Requests: Math.floor(Number(bal.raw) / 10000),
      funded: bal.raw > 0n,
      apiKey: getApiKey() ? 'configured' : 'not set',
    });
  },

  async 'wallet'() {
    const wallet = loadOrCreateWallet();
    const data = JSON.parse(fs.readFileSync(WALLET_FILE, 'utf8'));
    const bal = await getUsdcBalance(wallet.address);
    out({
      address: wallet.address,
      mnemonic: data.mnemonic || '(not saved — wallet was created before v2)',
      privateKey: data.privateKey,
      usdc: bal.formatted,
      network: 'Arbitrum One (chainId 42161)',
      warning: 'NEVER share your mnemonic or private key. Use the mnemonic to import into MetaMask or any wallet that supports BIP-39.',
    });
  },

  async 'set-key'(args) {
    const key = args[0];
    if (!key || !key.startsWith('nva_')) {
      console.error('Usage: node envy.js set-key nva_your_key_here');
      process.exit(1);
    }
    setApiKey(key);
    out({ success: true, message: 'API key saved', key: key.slice(0, 8) + '...' });
  },

  async 'status'() {
    const data = await callWithKey('/api/claw/subscription/status');
    out(data);
  },

  // ── Free endpoints ──

  async 'discover'() { out(await callFree('/api/claw/discover')); },
  async 'coins'() { out(await callFree('/api/claw/coins')); },
  async 'pricing'() { out(await callFree('/api/claw/pricing')); },
  async 'cache-status'() { out(await callFree('/api/claw/status')); },
  async 'leaderboard'(args, opts) {
    const limit = opts.limit || 50;
    out(await callFree(`/api/claw/arena/leaderboard?limit=${limit}`));
  },

  async 'indicators'(args, opts) {
    let path = '/api/claw/indicators';
    if (opts.category) path += `?category=${encodeURIComponent(opts.category)}`;
    out(await callFree(path));
  },

  async 'packs-info'(args, opts) {
    if (!opts.coin) { console.error('Usage: node envy.js packs-info --coin BTC'); process.exit(1); }
    out(await callFree(`/api/claw/packs/info?coin=${encodeURIComponent(opts.coin)}`));
  },

  // ── Referral ──

  async 'referral'(args, opts) {
    if (!opts.wallet) { console.error('Usage: node envy.js referral --wallet 0x...'); process.exit(1); }
    out(await callFree(`/api/claw/referral?wallet=${encodeURIComponent(opts.wallet)}`));
  },

  async 'referral-stats'(args, opts) {
    if (!opts.wallet) { console.error('Usage: node envy.js referral-stats --wallet 0x...'); process.exit(1); }
    out(await callFree(`/api/claw/referral/stats?wallet=${encodeURIComponent(opts.wallet)}`));
  },

  async 'referral-redeem'(args, opts) {
    if (!opts.wallet || !opts.code) {
      console.error('Usage: node envy.js referral-redeem --wallet 0x... --code ABCD1234');
      process.exit(1);
    }
    const res = await fetch(
      `${API_BASE}/api/claw/referral/redeem?wallet=${encodeURIComponent(opts.wallet)}&code=${encodeURIComponent(opts.code)}`,
      { method: 'POST' }
    );
    const data = await res.json();
    if (data.success && data.token) {
      setApiKey(data.token);
      out({ ...data, message: 'API key saved automatically!' });
    } else {
      out(data);
    }
  },

  // ── Subscribe (x402) ──

  async 'subscribe'() {
    const wallet = loadOrCreateWallet();
    const bal = await getUsdcBalance(wallet.address);
    if (bal.raw < 29990000n) { // $29.99
      out({
        error: 'Insufficient USDC for subscription ($29.99)',
        address: wallet.address,
        usdc: bal.formatted,
        message: `Send at least $30 USDC to ${wallet.address} on Arbitrum.`,
      });
      process.exit(1);
    }

    const data = await callWithX402('/api/claw/paid/subscribe', { method: 'POST' });
    if (data.success && data.token) {
      setApiKey(data.token);
      out({ ...data, message: 'Subscription active! API key saved automatically.' });
    } else {
      out(data);
    }
  },

  // ── Buy credits (needs both API key + x402) ──

  async 'buy-credits'(args, opts) {
    const apiKey = getApiKey();
    if (!apiKey) { console.error('Need an active subscription first. Run: node envy.js subscribe'); process.exit(1); }

    const wallet = loadOrCreateWallet();
    const amount = parseInt(opts.amount || '10');
    const atomicAmount = BigInt(amount) * 1000000n; // USDC has 6 decimals

    const bal = await getUsdcBalance(wallet.address);
    if (bal.raw < atomicAmount) {
      out({
        error: `Insufficient USDC (need $${amount}, have $${bal.formatted})`,
        address: wallet.address,
      });
      process.exit(1);
    }

    // Need to craft x402 payment manually since we also need X-API-KEY
    const now = Math.floor(Date.now() / 1000);
    const nonce = '0x' + crypto.randomBytes(32).toString('hex');

    // Get payTo from pricing
    const discover = await callFree('/api/claw/discover');
    const payTo = discover.payment?.payTo;
    if (!payTo) { console.error('Could not determine payment address'); process.exit(1); }

    const message = {
      from: wallet.address,
      to: payTo,
      value: atomicAmount,
      validAfter: 0,
      validBefore: now + 300,
      nonce,
    };

    const signature = await wallet.signTypedData(USDC_DOMAIN, TRANSFER_WITH_AUTH_TYPES, message);
    const sig = ethers.Signature.from(signature);

    const payload = {
      from: message.from,
      to: message.to,
      value: atomicAmount.toString(),
      validAfter: 0,
      validBefore: now + 300,
      nonce,
      v: sig.v,
      r: sig.r,
      s: sig.s,
      network: `eip155:${CHAIN_ID}`,
      scheme: 'exact',
    };

    const encoded = Buffer.from(JSON.stringify(payload)).toString('base64');
    const res = await fetch(`${API_BASE}/api/claw/paid/credits/buy`, {
      method: 'POST',
      headers: { 'X-API-KEY': apiKey, 'X-PAYMENT': encoded },
    });
    out(await res.json());
  },

  // ── Paid: Indicators ──

  async 'snapshot'(args, opts) {
    if (!opts.coins) { console.error('Usage: node envy.js snapshot --coins BTC,ETH [--indicators RSI_3H30M]'); process.exit(1); }
    let path = `/api/claw/paid/indicators/snapshot?coins=${encodeURIComponent(opts.coins)}`;
    if (opts.indicators) path += `&indicators=${encodeURIComponent(opts.indicators)}`;
    out(await callPaid(path));
  },

  async 'history'(args, opts) {
    if (!opts.coin) { console.error('Usage: node envy.js history --coin BTC [--hours 24] [--indicators RSI_3H30M]'); process.exit(1); }
    let path = `/api/claw/paid/indicators/history?coin=${encodeURIComponent(opts.coin)}`;
    if (opts.indicators) path += `&indicators=${encodeURIComponent(opts.indicators)}`;
    if (opts.hours) path += `&hours=${opts.hours}`;
    if (opts.page) path += `&page=${opts.page}`;
    if (opts.pageSize) path += `&pageSize=${opts.pageSize}`;
    out(await callPaid(path));
  },

  // ── Paid: Signals ──

  async 'check'(args, opts) {
    if (!opts.coin || !opts.yaml) {
      console.error('Usage: node envy.js check --coin BTC --yaml "path/to/signal.yaml"');
      console.error('   or: echo "yaml..." | node envy.js check --coin BTC --stdin');
      process.exit(1);
    }
    let yamlBody;
    if (opts.yaml) {
      yamlBody = fs.readFileSync(opts.yaml, 'utf8');
    }
    const result = await postYaml('/api/claw/paid/signals/check', yamlBody);

    // Auto-save signal to signals/
    if (typeof result === 'string' && result.includes('status: scored')) {
      try {
        const coinMatch = yamlBody.match(/coin:\s*(\w+)/i);
        const nameMatch = yamlBody.match(/name:\s*(\S+)/i);
        if (coinMatch && nameMatch) {
          const saved = saveSignal(coinMatch[1], nameMatch[1], yamlBody);
          console.error(`[envy] Signal saved: ${saved}`);
        }
      } catch {}
    }

    out(result);
  },

  async 'check-inline'(args, opts) {
    if (!opts.coin || !opts.name || !opts.type || !opts.expr || !opts.exit || !opts.hold) {
      console.error('Usage: node envy.js check-inline --coin BTC --name MY_SIG --type LONG --expr "RSI_3H30M <= 30" --exit "RSI_3H30M >= 70" --hold 48');
      process.exit(1);
    }
    const yamlBody = `coin: ${opts.coin}\nsignals:\n  - name: ${opts.name}\n    signal_type: ${opts.type}\n    expression: "${opts.expr}"\n    exit_expression: "${opts.exit}"\n    max_hold_hours: ${opts.hold}\n    source: openclaw_agent`;
    const result = await postYaml('/api/claw/paid/signals/check', yamlBody);

    // Auto-save signal
    if (typeof result === 'string' && result.includes('status: scored')) {
      try {
        const saved = saveSignal(opts.coin, opts.name, yamlBody);
        console.error(`[envy] Signal saved: ${saved}`);
      } catch {}
    }

    out(result);
  },

  // ── Paid: Packs ──

  async 'pack'(args, opts) {
    if (!opts.coin || !opts.type) { console.error('Usage: node envy.js pack --coin BTC --type common|rare|legendary'); process.exit(1); }
    const packType = opts.type.toLowerCase();
    if (!['common', 'rare', 'legendary'].includes(packType)) { console.error('Pack type must be: common, rare, legendary'); process.exit(1); }
    const result = await callPaid(`/api/claw/paid/signals/pack/${packType}?coin=${encodeURIComponent(opts.coin)}`);

    // Auto-save pack to signals/
    if (typeof result === 'string' && !result.startsWith('error')) {
      try {
        const saved = savePack(opts.coin, packType, result);
        console.error(`[envy] Pack saved: ${saved}`);
      } catch {}
    }

    out(result);
  },

  // ── Paid: Backtest ──

  async 'backtest'(args, opts) {
    if (!opts.yaml) { console.error('Usage: node envy.js backtest --yaml path/to/strategy.yaml [--days 90]'); process.exit(1); }
    const yamlBody = fs.readFileSync(opts.yaml, 'utf8');
    const days = opts.days || 90;
    out(await postYaml(`/api/claw/paid/backtest?days=${days}`, yamlBody));
  },

  // ── Paid: Strategy Assemble ──

  async 'assemble'(args, opts) {
    if (!opts.yaml) { console.error('Usage: node envy.js assemble --yaml path/to/signals.yaml [--mode normal] [--max 10]'); process.exit(1); }
    const yamlBody = fs.readFileSync(opts.yaml, 'utf8');
    const mode = opts.mode || 'normal';
    const max = opts.max || 10;
    const result = await postYaml(`/api/claw/paid/strategy/assemble?mode=${mode}&max_signals=${max}`, yamlBody);

    // Auto-save strategy
    if (typeof result === 'string' && !result.startsWith('error')) {
      try {
        const coinMatch = yamlBody.match(/coin:\s*(\w+)/i);
        if (coinMatch) {
          const saved = saveStrategy(coinMatch[1], result);
          console.error(`[envy] Strategy saved: ${saved}`);
        }
      } catch {}
    }

    out(result);
  },

  // ── Paid: Portfolio Optimize (free, 0 credits) ──

  async 'portfolio'(args, opts) {
    if (!opts.existing) { console.error('Usage: node envy.js portfolio --existing BTC,SOL [--count 5] [--mode normal] [--allocation fixed]'); process.exit(1); }
    let path = `/api/claw/paid/portfolio/optimize?existing=${encodeURIComponent(opts.existing)}`;
    if (opts.count) path += `&count=${opts.count}`;
    if (opts.mode) path += `&mode=${opts.mode}`;
    if (opts.allocation) path += `&allocation=${opts.allocation}`;
    out(await callPaid(path));
  },

  // ── Data management ──

  async 'list-signals'() {
    ensureDir(SIGNALS_DIR);
    const files = fs.readdirSync(SIGNALS_DIR).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    if (files.length === 0) {
      out({ signals: [], message: 'No saved signals. Use pack, check, or check-inline to generate some.' });
    } else {
      out({ signals: files, directory: SIGNALS_DIR, count: files.length });
    }
  },

  async 'list-strategies'() {
    ensureDir(STRATEGIES_DIR);
    const files = fs.readdirSync(STRATEGIES_DIR).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    if (files.length === 0) {
      out({ strategies: [], message: 'No saved strategies. Use assemble to generate one.' });
    } else {
      out({ strategies: files, directory: STRATEGIES_DIR, count: files.length });
    }
  },

  async 'list-archive'() {
    ensureDir(ARCHIVE_DIR);
    const files = fs.readdirSync(ARCHIVE_DIR).filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));
    out({ archive: files, directory: ARCHIVE_DIR, count: files.length });
  },

  // ── Help ──

  async 'help'() {
    console.log(`
Envy Trading System v1.0

SETUP:
  balance                          Check wallet address, USDC balance, API key status
  wallet                           Export wallet (address, mnemonic, private key) for backup or import
  set-key <nva_...>                Set API key manually
  subscribe                        Buy subscription via x402 ($29.99 → 30 days + 100 credits)
  buy-credits --amount 10          Top up credits on existing subscription
  referral-redeem --wallet --code  Redeem referral for free 14-day sub + 50 credits
  status                           Check subscription status + credit balance

FREE:
  discover                         Full API documentation
  coins                            List available coins
  indicators [--category X]        List indicators
  pricing                          Per-endpoint pricing
  packs-info --coin BTC            Available signal packs
  cache-status                     Data cache readiness
  leaderboard [--limit 50]         Arena leaderboard
  referral --wallet 0x...          Get/create referral code
  referral-stats --wallet 0x...    View referral redemptions

PAID (subscription or x402):
  snapshot --coins BTC,ETH [--indicators RSI_3H30M]     Latest indicator values (0 credits)
  history --coin BTC [--hours 24] [--page 1]            Time series (0 credits)
  check-inline --coin BTC --name X --type LONG --expr "..." --exit "..." --hold 48   Score signal (1 credit)
  check --coin BTC --yaml signal.yaml                   Score signal from file (1 credit)
  pack --coin BTC --type common|rare|legendary          Open signal pack (1/2/5 credits)
  backtest --yaml strategy.yaml [--days 90]             Backtest strategy (2 credits)
  assemble --yaml signals.yaml [--mode normal] [--max 10]  Strategy assembly (3 credits)
  portfolio --existing BTC,SOL [--count 5] [--mode normal]  Portfolio optimize (free)

DATA MANAGEMENT:
  list-signals                     List saved signals in signals/
  list-strategies                  List saved strategies in strategies/
  list-archive                     List archived strategies in archive/

MONITORING & TRADING:
  node monitor.js                  Start live signal monitor
  node controller.js               Start trading pipeline (spawns monitor)
  node controller.js --status      Show positions and P&L

AUTO-SAVE:
  Signals from check, check-inline, pack → saved to signals/
  Strategies from assemble → saved to strategies/
  Old strategies auto-archived to archive/ when overwritten
`);
  },
};

// ============================================================================
// CLI PARSER
// ============================================================================
function parseArgs(args) {
  const opts = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && i + 1 < args.length && !args[i + 1].startsWith('--')) {
      opts[args[i].slice(2)] = args[i + 1];
      i++;
    } else if (!args[i].startsWith('--')) {
      positional.push(args[i]);
    }
  }
  return { positional, opts };
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  const { positional, opts } = parseArgs(args.slice(1));

  const handler = commands[command];
  if (!handler) {
    console.error(`Unknown command: ${command}\nRun: node envy.js help`);
    process.exit(1);
  }

  await handler(positional, opts);
}

main().catch(err => {
  console.error(JSON.stringify({ error: err.message }));
  process.exit(1);
});
