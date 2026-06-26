import type { ChatMessage } from './types.js';

/**
 * Build the mining prompt that matches the Oracle server's validation (Step 4).
 *
 * Format:
 *   Clawing Mining | Seed: {seedHex} | Epoch: {epoch} | Nonce: {nonce} | Miner: {address} | ClaimIndex: {claimIndex} | Task: {taskText}
 *
 * Oracle verifier checks:
 *   - Contains "Clawing Mining"
 *   - Seed appears as the hex string (0x-prefixed)
 *   - "Epoch: {epoch}"
 *   - "Nonce: {nonce}"
 *   - Miner address (case-insensitive)
 *   - "ClaimIndex: {claimIndex}"
 *   - "Task:" present
 */
export function buildMiningPrompt(params: {
  seedHex: string;
  epoch: number;
  nonce: string;
  minerAddress: string;
  claimIndex: number;
  taskText: string;
}): string {
  return `Clawing Mining | Seed: ${params.seedHex} | Epoch: ${params.epoch} | Nonce: ${params.nonce} | Miner: ${params.minerAddress} | ClaimIndex: ${params.claimIndex} | Task: ${params.taskText}`;
}

/**
 * Build the full messages array for the AI API call.
 */
export function buildMessages(params: {
  seedHex: string;
  epoch: number;
  nonce: string;
  minerAddress: string;
  claimIndex: number;
  taskText: string;
}): ChatMessage[] {
  return [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: buildMiningPrompt(params) },
  ];
}

/**
 * Convert a BigInt seed to hex string with 0x prefix.
 */
export function seedToHex(seed: bigint): string {
  return '0x' + seed.toString(16);
}
