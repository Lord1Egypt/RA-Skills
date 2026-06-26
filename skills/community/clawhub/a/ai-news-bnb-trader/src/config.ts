import dotenv from 'dotenv';

dotenv.config();

const n = (k: string, d: number) => Number(process.env[k] ?? d);
const s = (k: string, d = '') => process.env[k] ?? d;
const b = (k: string, d: boolean) => (process.env[k] ?? String(d)).toLowerCase() === 'true';

export const config = {
  dryRun: b('DRY_RUN', true),
  chainId: n('CHAIN_ID', 56),
  rpcUrl: s('PRIVATE_RPC_URL') || s('RPC_URL', 'https://bsc-dataseed.binance.org'),
  evmPrivateKey: s('EVM_PRIVATE_KEY'),
  encryptedKeyPath: s('ENCRYPTED_KEY_PATH', './secrets/key.json'),
  keyPassphrase: s('KEY_PASSPHRASE'),

  newsMode: s('NEWS_MODE', 'poll') as 'poll' | 'ws',
  newsApiUrl: s('NEWS_API_URL'),
  newsWsUrl: s('NEWS_WS_URL'),
  newsPollSeconds: n('NEWS_POLL_SECONDS', 10),
  newsTimeoutMs: n('NEWS_TIMEOUT_MS', 8000),

  useOpenAI: b('USE_OPENAI', false),
  openaiApiKey: s('OPENAI_API_KEY'),
  openaiModel: s('OPENAI_MODEL', 'gpt-4o-mini'),
  openaiTimeoutMs: n('OPENAI_TIMEOUT_MS', 8000),
  minConf: n('MIN_CONF', 0.6),
  buyThreshold: n('BUY_THRESHOLD', 0.3),
  sellThreshold: n('SELL_THRESHOLD', 0.3),

  wbnb: s('WBNB', '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'),
  usdt: s('USDT', '0x55d398326f99059fF775485246999027B3197955'),
  busd: s('BUSD'),
  usdc: s('USDC'),
  quoteToken: s('QUOTE_TOKEN', 'USDT'),

  dexMode: s('DEX_MODE', 'oneinch'),
  oneInchApiBase: s('ONEINCH_API_BASE', 'https://api.1inch.dev/swap/v6.0/56'),
  oneInchApiKey: s('ONEINCH_API_KEY'),
  pancakeRouter: s('PANCAKE_ROUTER', '0x10ED43C718714eb63d5aA57B78B54704E256024E'),
  maxSlippageBps: n('MAX_SLIPPAGE_BPS', 50),
  deadlineSeconds: n('DEADLINE_SECONDS', 120),

  maxTradeUsd: n('MAX_TRADE_USD', 300),
  maxPositionPct: n('MAX_POSITION_PCT', 0.4),
  maxTradesPerDay: n('MAX_TRADES_PER_DAY', 8),
  maxDailyLossUsd: n('MAX_DAILY_LOSS_USD', 100),
  stopLossPct: n('STOP_LOSS_PCT', 0.03),
  takeProfitPct: n('TAKE_PROFIT_PCT', 0.05),
  cooldownSeconds: n('COOLDOWN_SECONDS', 120),
  maxConsecutiveFailures: n('MAX_CONSECUTIVE_FAILURES', 3),

  stateDir: s('STATE_DIR', './state-data'),
  logLevel: s('LOG_LEVEL', 'info')
};

export function validateConfig() {
  if (!config.evmPrivateKey && !config.keyPassphrase) {
    throw new Error('Missing key material. Set EVM_PRIVATE_KEY or KEY_PASSPHRASE + ENCRYPTED_KEY_PATH');
  }
  if (config.chainId !== 56) throw new Error('This skill is scoped to BSC chainId=56');
}
