import chalk from 'chalk';
import { ethers } from 'ethers';
import type { ChainState, MinerChainState } from './types.js';

const LINE = '═'.repeat(43);

export function printBanner(title: string): void {
  console.log(chalk.cyan(LINE));
  console.log(chalk.cyan.bold(`  ${title}`));
  console.log(chalk.cyan(LINE));
}

export function printStatus(params: {
  minerAddress: string;
  ethBalance: bigint;
  chainState: ChainState;
  minerState: MinerChainState;
  oracleUrl: string;
  oracleHealthy: boolean;
}): void {
  const { minerAddress, ethBalance, chainState, minerState, oracleUrl, oracleHealthy } = params;
  const seedHex = '0x' + chainState.currentSeed.toString(16);
  const seedCurrent = chainState.seedEpoch === chainState.currentGlobalEpoch;
  const cooldownReady = minerState.cooldownRemaining === 0n;
  const claims = Number(minerState.epochClaimCount);
  const maxClaims = Number(minerState.maxClaimsPerEpoch);

  printBanner('Clawing Miner Status');

  console.log(`  ${chalk.gray('Miner:')}        ${minerAddress}`);
  console.log(`  ${chalk.gray('Balance:')}      ${ethers.formatEther(ethBalance)} ETH`);
  console.log('');
  console.log(`  ${chalk.gray('Era:')}          ${chainState.currentEra}`);
  console.log(`  ${chalk.gray('Epoch:')}        ${chainState.currentGlobalEpoch}`);
  console.log(`  ${chalk.gray('Seed:')}         ${seedHex.length > 18 ? seedHex.slice(0, 18) + '...' : seedHex}`);
  console.log(`  ${chalk.gray('Seed Epoch:')}   ${chainState.seedEpoch} ${seedCurrent ? chalk.green('(current ✓)') : chalk.yellow('(needs update)')}`);
  console.log(`  ${chalk.gray('Era Model:')}    ${chainState.eraModelHash.slice(0, 18)}...`);
  console.log('');

  if (cooldownReady) {
    console.log(`  ${chalk.gray('Cooldown:')}     ${chalk.green('Ready ✓')}`);
  } else {
    const blocks = Number(minerState.cooldownRemaining);
    const hours = (blocks * 12 / 3600).toFixed(1);
    console.log(`  ${chalk.gray('Cooldown:')}     ${chalk.yellow(`${blocks.toLocaleString()} blocks remaining ≈ ${hours} hours`)}`);
  }

  console.log(`  ${chalk.gray('Claims:')}       ${claims}/${maxClaims} this epoch`);
  console.log('');

  const oracleStatus = oracleHealthy ? chalk.green('healthy ✓') : chalk.red('unreachable ✗');
  console.log(`  ${chalk.gray('Oracle:')}       ${oracleUrl} (${oracleStatus})`);

  console.log(chalk.cyan(LINE));
}

export function step(num: number, total: number, msg: string): void {
  console.log(chalk.blue(`[${num}/${total}]`) + ` ${msg}`);
}

export function info(msg: string): void {
  console.log(`  ${msg}`);
}

export function success(msg: string): void {
  console.log(`  ${chalk.green('✓')} ${msg}`);
}

export function warn(msg: string): void {
  console.log(`  ${chalk.yellow('⚠')} ${msg}`);
}

export function error(msg: string): void {
  console.log(`  ${chalk.red('✗')} ${msg}`);
}

export function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

export function formatClaw(wei: bigint): string {
  // CLAW has 18 decimals like ETH
  const formatted = ethers.formatEther(wei);
  const num = parseFloat(formatted);
  return num.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export function formatGwei(wei: bigint): string {
  return ethers.formatUnits(wei, 'gwei');
}
