import dotenv from 'dotenv';
import { ethers } from 'ethers';

dotenv.config();

// F-08: MinerConfig no longer stores privateKey — use wallet object instead
export interface MinerConfig {
  wallet: ethers.Wallet;
  minerAddress: string;
  aiApiKey: string;
  aiApiUrl: string;
  aiModel: string;
  oracleUrl: string;
  rpcUrl: string;
  poaiwMintAddress: string;
  maxGasPriceGwei: number;
  taskPrompt: string;
}

export function loadConfig(): MinerConfig {
  const privateKey = requireEnv('PRIVATE_KEY');
  const rpcUrl = envOrDefault('RPC_URL', 'https://eth.llamarpc.com');
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const wallet = new ethers.Wallet(privateKey, provider);

  // F-02: Enforce HTTPS for Oracle URL in production
  const oracleUrl = envOrDefault('ORACLE_URL', 'https://oracle.minewithclaw.com');
  if (
    !oracleUrl.startsWith('https://') &&
    !oracleUrl.startsWith('http://localhost') &&
    !oracleUrl.startsWith('http://127.0.0.1')
  ) {
    throw new Error(
      `ORACLE_URL must use HTTPS (got: ${oracleUrl}). ` +
      `Only localhost URLs are allowed over plain HTTP.`
    );
  }

  // F-03: Validate maxGasPriceGwei is a finite positive number
  const maxGasPriceGwei = parseFloat(envOrDefault('MAX_GAS_PRICE_GWEI', '2'));
  if (!Number.isFinite(maxGasPriceGwei) || maxGasPriceGwei <= 0) {
    throw new Error(
      `MAX_GAS_PRICE_GWEI must be a finite positive number (got: ${envOrDefault('MAX_GAS_PRICE_GWEI', '2')})`
    );
  }

  return {
    wallet,
    minerAddress: wallet.address,
    aiApiKey: requireEnv('AI_API_KEY'),
    aiApiUrl: envOrDefault('AI_API_URL', 'https://api.x.ai/v1/chat/completions'),
    aiModel: envOrDefault('AI_MODEL', 'grok-4.1-fast'),
    oracleUrl,
    rpcUrl,
    poaiwMintAddress: ethers.getAddress(envOrDefault('POAIW_MINT_ADDRESS', '0x511351940d99f3012c79c613478e8f2c887a8259')),
    maxGasPriceGwei,
    taskPrompt: envOrDefault('TASK_PROMPT', 'Write a detailed, comprehensive analysis of the following topic. Include multiple perspectives, examples, and nuanced arguments. Your response should be thorough and substantive.'),
  };
}

function requireEnv(key: string): string {
  const val = process.env[key];
  if (!val) throw new Error(`Missing required environment variable: ${key}`);
  return val;
}

function envOrDefault(key: string, defaultVal: string): string {
  return process.env[key] || defaultVal;
}
