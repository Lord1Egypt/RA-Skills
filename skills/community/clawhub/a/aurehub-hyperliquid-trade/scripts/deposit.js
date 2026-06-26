#!/usr/bin/env node
/**
 * deposit.js <amount_usdc> [--account N] [--confirmed]
 *
 * Bridges USDC from Arbitrum One -> Hyperliquid L1.
 * The same wallet address receives USDC on HL within ~1 minute.
 *
 * Without --confirmed: preview only (shows balance, amount, fees).
 * With    --confirmed: executes the transfer.
 *
 * Requirements:
 *   ARBITRUM_RPC_URL=<rpc_url>  in ~/.aurehub/.env
 *
 * Minimum deposit: 5 USDC (amounts below are permanently lost by the bridge).
 */

import { JsonRpcProvider, parseUnits, formatUnits, Contract } from 'ethers';
import { loadConfig } from './lib/config.js';
import { createSigner } from './lib/signer.js';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/** HL bridge contract on Arbitrum One. Accepts plain USDC transfers. */
const BRIDGE_ADDRESS = '0x2df1c51e09aecf9cacb7bc98cb1742757f163df7';

/** Native USDC on Arbitrum One (not USDC.e bridged variant). */
const USDC_ADDRESS = '0xaf88d065e77c8cC2239327C5EDb3A432268e5831';

const ARBITRUM_CHAIN_ID = 42161n;
const MIN_DEPOSIT_USDC = 5.0;

const USDC_ABI = [
  'function balanceOf(address owner) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'function decimals() view returns (uint8)',
  'event Transfer(address indexed from, address indexed to, uint256 value)',
];

// ---------------------------------------------------------------------------
// CLI argument parsing
// ---------------------------------------------------------------------------

function extractAccount(argv) {
  const i = argv.indexOf('--account');
  if (i === -1) return { account: undefined, rest: argv };
  const raw = argv[i + 1];
  const v = parseInt(raw, 10);
  if (Number.isNaN(v) || v < 0 || String(v) !== raw) {
    stderr({ error: '--account must be a non-negative integer' });
    process.exit(1);
  }
  return { account: v, rest: [...argv.slice(0, i), ...argv.slice(i + 2)] };
}

function stdout(obj) { process.stdout.write(JSON.stringify(obj) + '\n'); }
function stderr(obj) { process.stderr.write(JSON.stringify(obj) + '\n'); }

const { account: accountIdx, rest: cleanArgs } = extractAccount(process.argv.slice(2));
const confirmed = cleanArgs.includes('--confirmed');
const positional = cleanArgs.filter(a => !a.startsWith('--'));

const amountArg = positional[0];
if (!amountArg) {
  stderr({ error: 'Usage: deposit.js <amount_usdc> [--account N] [--confirmed]' });
  process.exit(1);
}

const amount = parseFloat(amountArg);
if (!isFinite(amount) || amount <= 0) {
  stderr({ error: `Invalid amount: "${amountArg}". Must be a positive number.` });
  process.exit(1);
}

if (amount < MIN_DEPOSIT_USDC) {
  stderr({
    error: `Minimum deposit is ${MIN_DEPOSIT_USDC} USDC. `
      + `Depositing less than the minimum is permanently lost by the bridge.`,
  });
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

try {
  const cfg = loadConfig();

  const arbitrumRpc = cfg.env.ARBITRUM_RPC_URL || process.env.ARBITRUM_RPC_URL;
  if (!arbitrumRpc) {
    stderr({
      error: 'ARBITRUM_RPC_URL not configured.',
      fix: 'Add ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc to ~/.aurehub/.env',
    });
    process.exit(1);
  }

  const provider = new JsonRpcProvider(arbitrumRpc);

  // Verify we're on Arbitrum One
  const network = await provider.getNetwork();
  if (network.chainId !== ARBITRUM_CHAIN_ID) {
    stderr({
      error: `Wrong network. Expected Arbitrum One (chainId 42161), got chainId ${network.chainId}.`,
      fix: 'Check ARBITRUM_RPC_URL in ~/.aurehub/.env -- it must point to Arbitrum One.',
    });
    process.exit(1);
  }

  const wallet = await createSigner(cfg, provider, { accountIndex: accountIdx });
  const address = await wallet.getAddress();

  const usdc = new Contract(USDC_ADDRESS, USDC_ABI, wallet);
  const decimalsOnChain = Number(await usdc.decimals());
  if (decimalsOnChain !== 6) {
    stderr({ error: `Unexpected USDC decimals: ${decimalsOnChain}. Expected 6. Check USDC_ADDRESS constant.` });
    process.exit(1);
  }
  const decimals = 6; // USDC is always 6; assertion above guards against RPC lying
  // Use the original string arg to avoid IEEE-754 float precision loss on large amounts
  const amountWei = parseUnits(amountArg, decimals);
  // Re-check minimum in wei space (exact integer arithmetic, guards against float edge cases)
  const minDepositWei = parseUnits(String(MIN_DEPOSIT_USDC), decimals);
  if (amountWei < minDepositWei) {
    stderr({ error: `Amount is below the ${MIN_DEPOSIT_USDC} USDC minimum after conversion.` });
    process.exit(1);
  }

  // Fetch balances in parallel
  const [usdcBalance, ethBalance] = await Promise.all([
    usdc.balanceOf(address),
    provider.getBalance(address),
  ]);

  const usdcFormatted = formatUnits(usdcBalance, decimals);
  const ethFormatted = formatUnits(ethBalance, 18);

  // Pre-flight checks
  if (usdcBalance < amountWei) {
    stderr({
      error: `Insufficient USDC on Arbitrum. Have ${parseFloat(usdcFormatted).toFixed(2)} USDC, need ${amount} USDC.`,
      hint: 'This script requires native USDC (not USDC.e). '
        + `Native USDC contract: ${USDC_ADDRESS}. `
        + 'If you only have USDC.e, swap it to native USDC first (e.g. via Uniswap on Arbitrum).',
    });
    process.exit(1);
  }

  if (ethBalance === 0n) {
    stderr({
      error: 'No ETH on Arbitrum One for gas fees.',
      fix: 'Bridge a small amount of ETH to Arbitrum One (0.001 ETH is enough for many deposits).',
    });
    process.exit(1);
  }

  // Confirmation thresholds from hyperliquid.yaml risk section
  const risk = cfg?.yaml?.risk ?? {};
  const toFinitePos = (v, fb) => (typeof v === 'number' && isFinite(v) && v > 0 ? v : fb);
  const confirmThreshold = toFinitePos(risk.confirm_trade_usd, 100);
  const largeThreshold = toFinitePos(risk.large_trade_usd, 1000);

  // Output preview
  stdout({
    preview: true,
    action: 'Deposit USDC -> Hyperliquid L1',
    from_address: address,
    to_hl_address: address,
    amount_usdc: amount,
    usdc_balance_arb: parseFloat(usdcFormatted),
    eth_balance_arb: ethFormatted,
    network: 'Arbitrum One',
    destination: 'Hyperliquid L1',
    bridge: BRIDGE_ADDRESS,
    estimated_credit_time: '~1 minute',
    requiresConfirm: amount >= confirmThreshold,
    requiresDoubleConfirm: amount >= largeThreshold,
  });

  if (!confirmed) process.exit(0);

  // Execute: transfer USDC to bridge contract
  const tx = await usdc.transfer(BRIDGE_ADDRESS, amountWei);
  stdout({ type: 'submitted', txHash: tx.hash, status: 'pending' });

  let receipt;
  try {
    receipt = await tx.wait(1);
  } catch (waitErr) {
    // Transaction was broadcast but confirmation failed (RPC drop, timeout, etc.)
    // The txHash is already on stdout -- user can verify on Arbiscan.
    stderr({
      error: `Transaction broadcast but confirmation failed: ${waitErr.message}`,
      txHash: tx.hash,
      action: 'Check https://arbiscan.io for the transaction status before retrying.',
    });
    process.exit(1);
  }

  // Verify the Transfer event was emitted -- guards against non-reverting ERC-20 failures
  const transferLog = receipt.logs.find(log => {
    if (log.address.toLowerCase() !== USDC_ADDRESS.toLowerCase()) return false;
    try { return usdc.interface.parseLog(log)?.name === 'Transfer'; } catch { return false; }
  });
  if (!transferLog) {
    stderr({
      error: 'Transaction confirmed but no Transfer event found. Bridge credit is uncertain.',
      txHash: receipt.hash,
      action: 'Check https://arbiscan.io and contact Hyperliquid support if USDC did not arrive.',
    });
    process.exit(1);
  }

  stdout({
    type: 'confirmed',
    txHash: receipt.hash,
    blockNumber: receipt.blockNumber,
    gasUsed: receipt.gasUsed.toString(),
    amount_usdc: amount,
    from: address,
    status: 'success',
    note: 'USDC will appear on Hyperliquid L1 within ~1 minute. Check with: node balance.js perp',
  });

  process.exit(0);
} catch (err) {
  stderr({ error: err.message });
  process.exit(1);
}
