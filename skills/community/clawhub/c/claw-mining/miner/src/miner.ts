import { ethers } from 'ethers';
import type { MinerConfig } from './config.js';
import type { ChainClient } from './chain.js';
import type { AttestRequest, Attestation } from './types.js';
import { getNonce, submitAttestation } from './oracle.js';
import { callAiApi } from './ai-api.js';
import { buildMessages, seedToHex } from './prompt.js';
import * as display from './display.js';

export interface MinerDeps {
  chain: ChainClient;
  config: MinerConfig;
}

/**
 * Validate attestation fields returned by Oracle.
 * Prevents null/undefined fields from crashing BigInt conversion (F-07),
 * verifies miner_address matches our wallet (F-01),
 * and checks deadline is still valid (F-06).
 */
function validateAttestation(att: Attestation, expectedMiner: string, currentBlock: number): void {
  // F-07: Check all required fields are present and non-null
  const requiredFields = ['miner_address', 'model_hash', 'total_tokens', 'seed_epoch', 'seed', 'claim_index', 'deadline', 'signature'] as const;
  for (const field of requiredFields) {
    if (att[field] == null) {
      throw new MineError('INVALID_ATTESTATION', `Oracle attestation missing field: ${field}`);
    }
  }
  if (typeof att.total_tokens !== 'number' || att.total_tokens < 0) {
    throw new MineError('INVALID_ATTESTATION', `Invalid total_tokens: ${att.total_tokens}`);
  }
  if (typeof att.deadline !== 'number' || att.deadline < 0) {
    throw new MineError('INVALID_ATTESTATION', `Invalid deadline: ${att.deadline}`);
  }

  // F-01: Verify miner_address matches our wallet — prevents reward redirection
  if (att.miner_address.toLowerCase() !== expectedMiner.toLowerCase()) {
    throw new MineError('ADDRESS_MISMATCH',
      `Oracle returned mismatched miner_address. Expected ${expectedMiner}, got ${att.miner_address}`);
  }

  // F-06: Verify deadline is still valid — prevents wasting gas on expired attestations
  if (att.deadline <= currentBlock) {
    throw new MineError('DEADLINE_EXPIRED',
      `Attestation deadline ${att.deadline} has passed (current block: ${currentBlock})`);
  }
}

/**
 * Execute a single mining cycle.
 * Returns the reward amount on success.
 */
export async function mineOnce(deps: MinerDeps): Promise<bigint> {
  const { chain, config } = deps;
  const STEPS = 8;

  // Step 1: Read chain state
  display.step(1, STEPS, 'Checking chain state...');
  const chainState = await chain.getChainState();
  const seedHex = seedToHex(chainState.currentSeed);
  display.info(`Era: ${chainState.currentEra}, Epoch: ${chainState.currentGlobalEpoch}, Seed: ${seedHex.slice(0, 18)}...`);

  // Step 2: Check cooldown
  display.step(2, STEPS, 'Checking cooldown...');
  const minerState = await chain.getMinerState(config.minerAddress, chainState.currentGlobalEpoch);

  if (minerState.cooldownRemaining > 0n) {
    // F-09: Use BigInt arithmetic throughout, only convert to Number at the end
    const waitSec = Number(minerState.cooldownRemaining * 12n);
    const blocks = Number(minerState.cooldownRemaining);
    display.warn(`Cooldown active. ${blocks.toLocaleString()} blocks remaining (≈ ${display.formatDuration(waitSec)})`);
    throw new MineError('COOLDOWN_ACTIVE', `Cooldown: ${blocks} blocks remaining`, waitSec);
  }
  display.success('Ready');

  // Check epoch limit
  if (minerState.epochClaimCount >= minerState.maxClaimsPerEpoch) {
    display.warn(`Epoch claim limit reached (${minerState.epochClaimCount}/${minerState.maxClaimsPerEpoch})`);
    throw new MineError('EPOCH_LIMIT_REACHED', 'Epoch claim limit reached');
  }

  const claimIndex = Number(minerState.epochClaimCount);

  // F-04: Early gas check — before spending API costs (moved from Step 7)
  display.step(3, STEPS, 'Checking gas price...');
  const gasPrice = await chain.getGasPrice();
  display.info(`Gas price: ${display.formatGwei(gasPrice)} gwei`);
  const maxGas = ethers.parseUnits(String(config.maxGasPriceGwei), 'gwei');
  if (gasPrice > maxGas) {
    throw new MineError('GAS_TOO_HIGH', `Gas price ${display.formatGwei(gasPrice)} gwei exceeds limit ${config.maxGasPriceGwei} gwei`);
  }
  display.success('Gas price OK');

  // Step 4: Check seed freshness
  display.step(4, STEPS, 'Checking seed...');
  let currentSeedHex = seedHex;
  if (chainState.seedEpoch !== chainState.currentGlobalEpoch) {
    display.info('Seed needs update, sending updateSeed() tx...');
    const receipt = await chain.updateSeed();
    display.success(`Seed updated in block ${receipt.blockNumber}`);
    // Re-read chain state after seed update
    const newState = await chain.getChainState();
    currentSeedHex = seedToHex(newState.currentSeed);
    // Update chainState references
    chainState.currentSeed = newState.currentSeed;
    chainState.seedEpoch = newState.seedEpoch;
  } else {
    display.success('Seed is current');
  }

  // Step 5: Get nonce from Oracle
  display.step(5, STEPS, 'Getting nonce from Oracle...');
  const { nonce } = await getNonce(config.oracleUrl, config.minerAddress);
  display.info(`Nonce: ${nonce}`);

  // Step 6: Call AI API
  display.step(6, STEPS, `Calling AI API (${config.aiModel})...`);
  const messages = buildMessages({
    seedHex: currentSeedHex,
    epoch: Number(chainState.currentGlobalEpoch),
    nonce,
    minerAddress: config.minerAddress,
    claimIndex,
    taskText: config.taskPrompt,
  });

  const aiResponse = await callAiApi(
    { apiKey: config.aiApiKey, apiUrl: config.aiApiUrl, model: config.aiModel },
    messages,
  );
  display.info(`Tokens used: ${aiResponse.usage.total_tokens} (prompt: ${aiResponse.usage.prompt_tokens}, completion: ${aiResponse.usage.completion_tokens})`);

  // Step 7: Submit to Oracle + validate attestation
  display.step(7, STEPS, 'Submitting to Oracle for signing...');
  const attestRequest: AttestRequest = {
    miner_address: config.minerAddress,
    nonce,
    api_response: aiResponse,
    api_request: { model: config.aiModel, messages },
    seed_epoch: Number(chainState.currentGlobalEpoch),
    seed: currentSeedHex,
    claim_index: claimIndex,
  };

  const oracleResult = await submitAttestation(config.oracleUrl, attestRequest);
  display.success('Attestation received');

  // F-01 + F-06 + F-07: Validate attestation before proceeding
  validateAttestation(oracleResult.attestation, config.minerAddress, chainState.currentBlock);

  const rewardStr = display.formatClaw(BigInt(oracleResult.estimated_reward));
  display.info(`Estimated reward: ${rewardStr} CLAW`);

  // Step 8: Submit mint() transaction
  display.step(8, STEPS, 'Submitting mint() transaction...');
  const receipt = await chain.mint(oracleResult.attestation);
  display.info(`Tx: ${receipt.hash}`);
  display.success(`Mined in block ${receipt.blockNumber}`);

  const reward = BigInt(oracleResult.estimated_reward);
  display.info(`Reward: ${rewardStr} CLAW`);
  const gasCost = receipt.gasUsed * (receipt.gasPrice ?? gasPrice);
  display.info(`Gas used: ${receipt.gasUsed.toLocaleString()} (cost: ~${ethers.formatEther(gasCost)} ETH)`);

  return reward;
}

/**
 * Auto-mine loop with cooldown waits and error recovery.
 */
export async function autoMine(deps: MinerDeps): Promise<void> {
  const { chain, config } = deps;
  let cycle = 0;
  let running = true;

  const shutdown = () => {
    console.log('\n  Shutting down gracefully...');
    running = false;
  };

  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);

  display.printBanner('Clawing Auto-Miner Started');
  console.log('  Press Ctrl+C to stop\n');

  while (running) {
    cycle++;
    console.log(`\n[Cycle ${cycle}] ${new Date().toISOString()}`);

    try {
      // F-11: Removed redundant gas check — mineOnce now checks gas early (Step 3)
      const reward = await mineOnce(deps);
      display.success(`Mining complete! Reward: ${display.formatClaw(reward)} CLAW`);

      // Wait for cooldown
      const cooldownBlocks = await chain.getCooldownBlocks();
      const waitSeconds = Number(cooldownBlocks) * 12 + 60;
      console.log(`  Next mine in: ${display.formatDuration(waitSeconds)}`);
      console.log('  Waiting...');
      await sleep(waitSeconds * 1000, () => running);
    } catch (err) {
      if (!running) break;

      if (err instanceof MineError) {
        if (err.code === 'COOLDOWN_ACTIVE' && err.waitSeconds) {
          console.log(`  Waiting ${display.formatDuration(err.waitSeconds + 60)}...`);
          await sleep((err.waitSeconds + 60) * 1000, () => running);
        } else if (err.code === 'EPOCH_LIMIT_REACHED') {
          display.warn('Epoch claim limit reached. Waiting 30 minutes for next epoch...');
          await sleep(30 * 60 * 1000, () => running);
        } else if (err.code === 'GAS_TOO_HIGH') {
          display.warn(err.message + '. Retrying in 60s...');
          await sleep(60_000, () => running);
        } else {
          display.error(err.message);
          console.log('  Retrying in 60 seconds...');
          await sleep(60_000, () => running);
        }
      } else {
        display.error((err as Error).message);
        console.log('  Retrying in 60 seconds...');
        await sleep(60_000, () => running);
      }
    }
  }

  process.off('SIGINT', shutdown);
  process.off('SIGTERM', shutdown);
  console.log('\n  Auto-miner stopped.\n');
}

/** Interruptible sleep — resolves early if shouldContinue returns false */
function sleep(ms: number, shouldContinue?: () => boolean): Promise<void> {
  return new Promise((resolve) => {
    if (shouldContinue && !shouldContinue()) {
      resolve();
      return;
    }

    const interval = setInterval(() => {
      if (shouldContinue && !shouldContinue()) {
        clearInterval(interval);
        clearTimeout(timeout);
        resolve();
      }
    }, 1000);

    const timeout = setTimeout(() => {
      clearInterval(interval);
      resolve();
    }, ms);
  });
}

export class MineError extends Error {
  public readonly code: string;
  public readonly waitSeconds?: number;

  constructor(code: string, message: string, waitSeconds?: number) {
    super(message);
    this.name = 'MineError';
    this.code = code;
    this.waitSeconds = waitSeconds;
  }
}
