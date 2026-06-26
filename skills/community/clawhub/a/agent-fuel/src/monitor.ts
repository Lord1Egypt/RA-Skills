/**
 * Agent Fuel — Balance Monitor & Auto Top-Up
 * 
 * Monitors agent wallet balance and triggers MoonPay purchases
 * when balance drops below configured threshold.
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface FuelConfig {
  chain: string;
  currency: string;
  minBalance: number;
  topUpAmount: number;
  maxDailySpend: number;
  alertThreshold: number;
  x402Enabled: boolean;
  x402MaxPerRequest: number;
}

interface SpendingLog {
  date: string;
  totalSpent: number;
  transactions: Array<{
    timestamp: string;
    amount: number;
    type: 'top-up' | 'x402' | 'send';
    reason: string;
    txHash?: string;
  }>;
}

const CONFIG_PATH = path.join(process.env.HOME || '~', 'clawd/.secrets/agent-fuel.json');
const LOG_PATH = path.join(process.env.HOME || '~', 'clawd/memory/agent-fuel-spending.json');

function loadConfig(): FuelConfig {
  const defaults: FuelConfig = {
    chain: 'base',
    currency: 'USDC',
    minBalance: 5.0,
    topUpAmount: 20.0,
    maxDailySpend: 100.0,
    alertThreshold: 2.0,
    x402Enabled: true,
    x402MaxPerRequest: 0.10,
  };

  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
    return { ...defaults, ...JSON.parse(raw) };
  } catch {
    return defaults;
  }
}

function getBalance(config: FuelConfig): number {
  try {
    const output = execSync(`mp wallet balance --chain ${config.chain} --json`, {
      encoding: 'utf-8',
      timeout: 30000,
    });
    const data = JSON.parse(output);
    const token = data.balances?.find((b: any) => 
      b.symbol.toUpperCase() === config.currency.toUpperCase()
    );
    return token ? parseFloat(token.balance) : 0;
  } catch (err) {
    console.error('Failed to check balance:', err);
    return -1;
  }
}

function getDailySpend(): number {
  try {
    const raw = fs.readFileSync(LOG_PATH, 'utf-8');
    const log: SpendingLog = JSON.parse(raw);
    const today = new Date().toISOString().split('T')[0];
    if (log.date === today) {
      return log.totalSpent;
    }
    return 0;
  } catch {
    return 0;
  }
}

function logTransaction(amount: number, type: string, reason: string, txHash?: string) {
  const today = new Date().toISOString().split('T')[0];
  let log: SpendingLog;

  try {
    const raw = fs.readFileSync(LOG_PATH, 'utf-8');
    log = JSON.parse(raw);
    if (log.date !== today) {
      log = { date: today, totalSpent: 0, transactions: [] };
    }
  } catch {
    log = { date: today, totalSpent: 0, transactions: [] };
  }

  log.totalSpent += amount;
  log.transactions.push({
    timestamp: new Date().toISOString(),
    amount,
    type: type as any,
    reason,
    txHash,
  });

  fs.writeFileSync(LOG_PATH, JSON.stringify(log, null, 2));
}

function topUp(config: FuelConfig): boolean {
  const dailySpend = getDailySpend();
  
  if (dailySpend + config.topUpAmount > config.maxDailySpend) {
    console.log(`⚠️ Daily spend limit would be exceeded ($${dailySpend} + $${config.topUpAmount} > $${config.maxDailySpend})`);
    return false;
  }

  try {
    console.log(`⛽ Topping up: $${config.topUpAmount} ${config.currency} on ${config.chain}...`);
    const output = execSync(
      `mp buy --amount ${config.topUpAmount} --currency ${config.currency} --chain ${config.chain} --json`,
      { encoding: 'utf-8', timeout: 60000 }
    );
    const result = JSON.parse(output);
    logTransaction(config.topUpAmount, 'top-up', 'Auto top-up: balance below threshold', result.txHash);
    console.log(`✅ Top-up complete. TX: ${result.txHash || 'pending'}`);
    return true;
  } catch (err) {
    console.error('❌ Top-up failed:', err);
    return false;
  }
}

export function checkAndFuel(): { balance: number; action: string } {
  const config = loadConfig();
  const balance = getBalance(config);

  if (balance < 0) {
    return { balance: -1, action: 'error: could not check balance' };
  }

  if (balance < config.alertThreshold) {
    console.log(`🚨 CRITICAL: Balance $${balance} below alert threshold $${config.alertThreshold}`);
  }

  if (balance < config.minBalance) {
    console.log(`⛽ Balance $${balance} below minimum $${config.minBalance}. Initiating top-up...`);
    const success = topUp(config);
    return {
      balance,
      action: success ? `topped-up $${config.topUpAmount}` : 'top-up failed (check limits)',
    };
  }

  return { balance, action: 'ok' };
}

/**
 * x402 Payment Handler
 * Intercepts 402 responses and handles payment automatically
 */
export async function handleX402(
  url: string,
  paymentHeader: string,
  config?: FuelConfig
): Promise<{ paid: boolean; amount: number }> {
  const cfg = config || loadConfig();
  
  if (!cfg.x402Enabled) {
    return { paid: false, amount: 0 };
  }

  try {
    // Parse payment requirements from header
    const requirements = JSON.parse(Buffer.from(paymentHeader, 'base64').toString());
    const amount = parseFloat(requirements.amount);

    if (amount > cfg.x402MaxPerRequest) {
      console.log(`⚠️ x402 payment $${amount} exceeds max per request $${cfg.x402MaxPerRequest}`);
      return { paid: false, amount };
    }

    // Check daily limit
    const dailySpend = getDailySpend();
    if (dailySpend + amount > cfg.maxDailySpend) {
      return { paid: false, amount };
    }

    // Execute payment via MoonPay wallet
    const output = execSync(
      `mp send --to ${requirements.payTo} --amount ${amount} --currency ${cfg.currency} --chain ${cfg.chain} --json`,
      { encoding: 'utf-8', timeout: 30000 }
    );
    const result = JSON.parse(output);
    
    logTransaction(amount, 'x402', `x402 payment to ${url}`, result.txHash);
    return { paid: true, amount };
  } catch (err) {
    console.error('x402 payment failed:', err);
    return { paid: false, amount: 0 };
  }
}

// CLI entry point
if (require.main === module) {
  const result = checkAndFuel();
  console.log(JSON.stringify(result, null, 2));
}
