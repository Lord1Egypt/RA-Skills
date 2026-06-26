import { JsonRpcProvider, Wallet, formatUnits, parseUnits, Contract } from 'ethers';
import { config, validateConfig } from './config.js';
import { logger } from './utils/logger.js';
import { JsonStore } from './state/store.js';
import { fetchNews } from './news/fetcher.js';
import { RuleSignalModel } from './signals/rule-model.js';
import { OpenAISignalModel } from './signals/openai-model.js';
import { ISignalModel } from './signals/interface.js';
import { decide } from './strategy/decision-engine.js';
import { riskCheck } from './risk/risk-manager.js';
import { OneInchDex } from './dex/oneinch.js';
import { decryptPrivateKey } from './wallet/key-manager.js';

const ERC20 = [
  'function balanceOf(address) view returns (uint256)',
  'function decimals() view returns (uint8)',
  'function symbol() view returns (string)',
  'function approve(address spender, uint256 amount) returns (bool)'
];

function getPrivateKey() {
  if (config.evmPrivateKey) return config.evmPrivateKey;
  if (config.keyPassphrase) return decryptPrivateKey(config.encryptedKeyPath, config.keyPassphrase);
  throw new Error('No private key available');
}

async function status(store: JsonStore) {
  validateConfig();
  const provider = new JsonRpcProvider(config.rpcUrl, config.chainId);
  const wallet = new Wallet(getPrivateKey(), provider);
  const quote = config.quoteToken === 'USDT' ? config.usdt : (config.quoteToken === 'BUSD' ? config.busd : config.usdc);
  const q = new Contract(quote, ERC20, provider);
  const w = new Contract(config.wbnb, ERC20, provider);
  const qBal = await q.balanceOf(wallet.address);
  const wBal = await w.balanceOf(wallet.address);
  const qDec = await q.decimals();
  const wDec = await w.decimals();

  const dayStart = new Date(); dayStart.setUTCHours(0,0,0,0);
  const today = store.state.trades.filter(t => t.ts >= Math.floor(dayStart.getTime()/1000));
  const pnl = today.reduce((a, t) => a + (t.side === 'SELL_WBNB' ? t.amountInUsd : -t.amountInUsd), 0);

  console.log(JSON.stringify({
    address: wallet.address,
    quoteBalance: Number(formatUnits(qBal, qDec)),
    wbnbBalance: Number(formatUnits(wBal, wDec)),
    tradesToday: today.length,
    estDailyPnlUsd: pnl,
    panic: store.state.panic,
    safeMode: store.state.safeMode,
    consecutiveFailures: store.state.consecutiveFailures
  }, null, 2));
}

async function revokeApprovals() {
  validateConfig();
  const provider = new JsonRpcProvider(config.rpcUrl, config.chainId);
  const wallet = new Wallet(getPrivateKey(), provider);
  const tokens = [config.usdt, config.busd, config.usdc, config.wbnb].filter(Boolean);
  for (const t of tokens) {
    const c = new Contract(t, ERC20, wallet);
    if (config.dryRun) {
      logger.info('[DRY-RUN] approve 0', t, config.pancakeRouter);
      continue;
    }
    const tx = await c.approve(config.pancakeRouter, 0n);
    await tx.wait();
    logger.info('revoked', t, tx.hash);
  }
}

async function start(store: JsonStore) {
  validateConfig();
  const provider = new JsonRpcProvider(config.rpcUrl, config.chainId);
  const wallet = new Wallet(getPrivateKey(), provider);
  const quote = config.quoteToken === 'USDT' ? config.usdt : (config.quoteToken === 'BUSD' ? config.busd : config.usdc);
  if (!quote) throw new Error(`QUOTE_TOKEN ${config.quoteToken} address missing`);

  const model: ISignalModel = (config.useOpenAI && config.openaiApiKey)
    ? new OpenAISignalModel(config.openaiApiKey, config.openaiModel, config.openaiTimeoutMs)
    : new RuleSignalModel();
  const fallback = new RuleSignalModel();
  const dex = new OneInchDex(provider, wallet, config.oneInchApiBase, config.oneInchApiKey, config.dryRun);

  logger.info('bot start', `addr=${wallet.address}`, `dryRun=${config.dryRun}`);

  let failures = store.state.consecutiveFailures;

  while (true) {
    try {
      const items = await fetchNews(config.newsApiUrl, config.newsTimeoutMs);
      for (const news of items) {
        if (store.hasNews(news.id)) continue;
        store.markNews(news.id);

        const s = await model.analyze(news).catch(() => fallback.analyze(news));
        const d = decide(s, config.buyThreshold, config.sellThreshold, config.minConf);
        logger.info('news', news.id, news.source, news.title, JSON.stringify(s), d.why);
        if (!d.side) continue;

        const q = new Contract(quote, ERC20, provider);
        const w = new Contract(config.wbnb, ERC20, provider);
        const qDec = await q.decimals();
        const wDec = await w.decimals();
        const qBal = Number(formatUnits(await q.balanceOf(wallet.address), qDec));
        const wBal = Number(formatUnits(await w.balanceOf(wallet.address), wDec));

        const orderUsd = Math.min(config.maxTradeUsd, qBal);
        if (orderUsd <= 1) continue;

        const amountIn = d.side === 'BUY_WBNB' ? parseUnits(String(orderUsd), qDec) : parseUnits(String(Math.min(wBal, orderUsd / 600)), wDec);
        const from = d.side === 'BUY_WBNB' ? quote : config.wbnb;
        const to = d.side === 'BUY_WBNB' ? config.wbnb : quote;

        const qt = await dex.quote(from, to, amountIn);

        const dayStart = new Date(); dayStart.setUTCHours(0,0,0,0);
        const today = store.state.trades.filter(t => t.ts >= Math.floor(dayStart.getTime()/1000));
        const pnl = today.reduce((a, t) => a + (t.side === 'SELL_WBNB' ? t.amountInUsd : -t.amountInUsd), 0);

        const risk = riskCheck(store, {
          nowTs: Math.floor(Date.now()/1000),
          usdBalance: qBal,
          wbnbUsdValue: wBal * 600,
          orderUsd,
          estSlippageBps: qt.slippageBps,
          dailyPnlUsd: pnl,
          cooldownSeconds: config.cooldownSeconds,
          maxTradesPerDay: config.maxTradesPerDay,
          maxDailyLossUsd: config.maxDailyLossUsd,
          maxPositionPct: config.maxPositionPct,
          maxTradeUsd: config.maxTradeUsd,
          maxSlippageBps: config.maxSlippageBps
        });

        if (!risk.ok) {
          logger.warn('risk rejected', risk.reason ?? 'unknown');
          continue;
        }

        const res = await dex.swap(from, to, amountIn, config.maxSlippageBps);
        store.addTrade({
          id: news.id,
          ts: Math.floor(Date.now()/1000),
          side: d.side,
          amountInUsd: orderUsd,
          px: 600,
          txHash: res.txHash,
          reason: `${d.why}; ${s.reason}`
        });
      }

      failures = 0;
      store.state.consecutiveFailures = 0;
      store.save();
      await new Promise((r) => setTimeout(r, config.newsPollSeconds * 1000));
    } catch (e) {
      failures += 1;
      store.state.consecutiveFailures = failures;
      if (failures >= config.maxConsecutiveFailures) store.state.safeMode = true;
      store.save();
      logger.error('loop error', String(e), `failures=${failures}`);
      await new Promise((r) => setTimeout(r, Math.min(30000, 1000 * failures)));
    }
  }
}

(async () => {
  const cmd = process.argv[2] ?? 'start';
  const store = new JsonStore(config.stateDir);
  if (cmd === 'status') return status(store);
  if (cmd === 'panic') {
    store.state.panic = true;
    store.save();
    logger.warn('panic enabled');
    return;
  }
  if (cmd === 'revoke-approvals') return revokeApprovals();
  if (cmd === 'start') return start(store);
  throw new Error(`Unknown command: ${cmd}`);
})();
