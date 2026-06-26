/**
 * Self-hosted x402 Facilitator for ClawPhunks
 *
 * Executes EIP-3009 TransferWithAuthorization on Base to receive USDC payments.
 * Uses the signer wallet to pay gas for executing the transfers.
 */

import { createWalletClient, createPublicClient, http, encodeFunctionData } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const USDC_ADDRESS = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';

// EIP-3009 TransferWithAuthorization ABI
const TRANSFER_WITH_AUTH_ABI = [
  {
    name: 'transferWithAuthorization',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' },
      { name: 'v', type: 'uint8' },
      { name: 'r', type: 'bytes32' },
      { name: 's', type: 'bytes32' },
    ],
    outputs: [],
  },
  {
    name: 'balanceOf',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: 'account', type: 'address' }],
    outputs: [{ name: '', type: 'uint256' }],
  },
] as const;

interface Authorization {
  from: string;
  to: string;
  value: string;
  validAfter: string;
  validBefore: string;
  nonce: string;
}

interface PaymentPayload {
  x402Version: number;
  scheme: string;
  network: string;
  payload: {
    signature: string;
    authorization: Authorization;
  };
}

interface PaymentRequirements {
  scheme: string;
  network: string;
  maxAmountRequired: string;
  payTo: string;
  asset: string;
}

interface VerifyResponse {
  isValid: boolean;
  invalidReason?: string;
  invalidMessage?: string;
}

interface SettleResponse {
  success: boolean;
  txHash?: string;
  error?: string;
}

// Get signer wallet
function getSignerWallet() {
  let privateKey = process.env.SIGNER_PRIVATE_KEY?.trim();
  if (!privateKey) {
    throw new Error('SIGNER_PRIVATE_KEY required for facilitator');
  }

  // Ensure 0x prefix
  if (!privateKey.startsWith('0x')) {
    privateKey = `0x${privateKey}`;
  }

  const account = privateKeyToAccount(privateKey as `0x${string}`);

  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http(process.env.BASE_RPC_URL ?? 'https://mainnet.base.org'),
  });

  const publicClient = createPublicClient({
    chain: base,
    transport: http(process.env.BASE_RPC_URL ?? 'https://mainnet.base.org'),
  });

  return { walletClient, publicClient, account };
}

// Parse signature into v, r, s
function parseSignature(signature: string): { v: number; r: `0x${string}`; s: `0x${string}` } {
  const sig = signature.startsWith('0x') ? signature.slice(2) : signature;
  const r = `0x${sig.slice(0, 64)}` as `0x${string}`;
  const s = `0x${sig.slice(64, 128)}` as `0x${string}`;
  let v = parseInt(sig.slice(128, 130), 16);

  // Handle EIP-155 v values
  if (v < 27) {
    v += 27;
  }

  return { v, r, s };
}

/**
 * Verify a payment payload (checks signature validity, balance, etc.)
 */
export async function verify(
  paymentPayload: PaymentPayload,
  paymentRequirements: PaymentRequirements
): Promise<VerifyResponse> {
  try {
    const { publicClient } = getSignerWallet();
    const { authorization } = paymentPayload.payload;

    // Check network
    if (paymentPayload.network !== 'base') {
      return {
        isValid: false,
        invalidReason: 'unsupported_network',
        invalidMessage: `Network ${paymentPayload.network} not supported, use 'base'`,
      };
    }

    // Check amount
    const requiredAmount = BigInt(paymentRequirements.maxAmountRequired);
    const payloadAmount = BigInt(authorization.value);

    if (payloadAmount < requiredAmount) {
      return {
        isValid: false,
        invalidReason: 'insufficient_amount',
        invalidMessage: `Payment amount ${payloadAmount} less than required ${requiredAmount}`,
      };
    }

    // Check recipient matches
    const payTo = paymentRequirements.payTo.trim().toLowerCase();
    const authTo = authorization.to.toLowerCase();

    if (authTo !== payTo) {
      return {
        isValid: false,
        invalidReason: 'wrong_recipient',
        invalidMessage: `Payment to ${authTo} but required ${payTo}`,
      };
    }

    // Check time window
    const now = Math.floor(Date.now() / 1000);
    const validAfter = parseInt(authorization.validAfter);
    const validBefore = parseInt(authorization.validBefore);

    if (now < validAfter) {
      return {
        isValid: false,
        invalidReason: 'not_yet_valid',
        invalidMessage: `Payment not valid until ${new Date(validAfter * 1000).toISOString()}`,
      };
    }

    if (now > validBefore) {
      return {
        isValid: false,
        invalidReason: 'expired',
        invalidMessage: `Payment expired at ${new Date(validBefore * 1000).toISOString()}`,
      };
    }

    // Check sender has sufficient balance
    const balance = await publicClient.readContract({
      address: USDC_ADDRESS,
      abi: TRANSFER_WITH_AUTH_ABI,
      functionName: 'balanceOf',
      args: [authorization.from as `0x${string}`],
    });

    if (balance < payloadAmount) {
      return {
        isValid: false,
        invalidReason: 'insufficient_balance',
        invalidMessage: `Sender balance ${balance} less than payment ${payloadAmount}`,
      };
    }

    return { isValid: true };
  } catch (error: any) {
    return {
      isValid: false,
      invalidReason: 'verification_error',
      invalidMessage: error.message,
    };
  }
}

/**
 * Settle a payment (execute the USDC transfer on-chain)
 */
export async function settle(
  paymentPayload: PaymentPayload,
  paymentRequirements: PaymentRequirements
): Promise<SettleResponse> {
  try {
    const { walletClient, publicClient } = getSignerWallet();
    const { authorization, signature } = paymentPayload.payload;
    const { v, r, s } = parseSignature(signature);

    console.log('[facilitator] Settling payment...');
    console.log(`  From: ${authorization.from}`);
    console.log(`  To: ${authorization.to}`);
    console.log(`  Value: ${authorization.value} (${Number(authorization.value) / 1e6} USDC)`);

    // Execute transferWithAuthorization
    const hash = await walletClient.writeContract({
      address: USDC_ADDRESS,
      abi: TRANSFER_WITH_AUTH_ABI,
      functionName: 'transferWithAuthorization',
      args: [
        authorization.from as `0x${string}`,
        authorization.to as `0x${string}`,
        BigInt(authorization.value),
        BigInt(authorization.validAfter),
        BigInt(authorization.validBefore),
        authorization.nonce as `0x${string}`,
        v,
        r,
        s,
      ],
    });

    console.log(`[facilitator] Tx submitted: ${hash}`);

    // Wait for confirmation
    const receipt = await publicClient.waitForTransactionReceipt({ hash });

    if (receipt.status === 'success') {
      console.log(`[facilitator] ✓ Payment settled: ${hash}`);
      return { success: true, txHash: hash };
    } else {
      console.log(`[facilitator] ✗ Payment failed: ${hash}`);
      return { success: false, error: 'Transaction reverted' };
    }
  } catch (error: any) {
    console.error('[facilitator] Error:', error.message);
    return { success: false, error: error.message };
  }
}
