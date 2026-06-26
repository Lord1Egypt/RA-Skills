import { Contract, JsonRpcProvider } from 'ethers';
import {
  createUserWallet,
  createDfnsWallet,
  createLedgerBridgeWallet,
  ZamaFheSession,
  type FheWallet,
  TOKEN_ABI,
  VERIFIER_ABI,
} from '../../core/src/index.js';
import { parseArgs } from 'node:util';

// ============================================================================
// Contract Addresses (mainnet defaults, overridable via env)
// ============================================================================

const RPC_URL =
  process.env.RPC_URL ?? 'https://ethereum-sepolia-rpc.publicnode.com';

// Detect chain early — needed for default address selection
const _isMainnet = process.env.CHAIN === 'mainnet' || RPC_URL.includes('mainnet');

// Default addresses match the detected chain. Sepolia uses Zama cUSDCMock + deployed x402fhe contracts.
const CUSDC_ADDRESS = process.env.CUSDC_ADDRESS ?? (
  _isMainnet ? '0xe978F22157048E5DB8E5d07971376e86671672B2' : '0x7c5BF43B851c1dff1a4feE8dB225b87f2C223639'
);
const USDC_ADDRESS = process.env.USDC_ADDRESS ?? (
  _isMainnet ? '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48' : '0x9b5Cd13b8eFbB58Dc25A05CF411D8056058aDFfF'
);
const VERIFIER_ADDRESS = process.env.VERIFIER_ADDRESS ?? (
  _isMainnet ? '' : '0xD46E80E1d37116B44c7Bfd845A110FCbB93d3E9F'
);
const IDENTITY_ADDRESS = process.env.IDENTITY_ADDRESS ?? (
  _isMainnet ? '' : '0x36666464daa16442Fc1d901acfC9419f11407741'
);
const REPUTATION_ADDRESS = process.env.REPUTATION_ADDRESS ?? (
  _isMainnet ? '' : '0x1649d762Ee62f194D92B93510b8f10a501cE9fD5'
);
const ESCROW_ADDRESS = process.env.ESCROW_ADDRESS ?? (
  _isMainnet ? '' : '0xECD7a2382A5F0e3b6A7b76536e4CAE11215Cc695'
);

// ============================================================================
// Minimal ABIs for contracts not yet in @x402fhe/core
// ============================================================================

/** Minimal ERC-20 ABI for USDC (approve + balanceOf) */
const ERC20_ABI = [
  'function approve(address spender, uint256 amount) external returns (bool)',
  'function balanceOf(address account) external view returns (uint256)',
] as const;

/** AgentIdentityRegistry minimal ABI (ERC-8004 — ERC-721 based) */
const IDENTITY_ABI = [
  'function register(string calldata agentURI) external returns (uint256)',
  'function setAgentWallet(uint256 agentId, address newWallet, uint256 deadline, bytes calldata signature) external',
  'function getAgentWallet(uint256 agentId) external view returns (address)',
  'function setAgentURI(uint256 agentId, string calldata newURI) external',
  'function setMetadata(uint256 agentId, string calldata metadataKey, bytes calldata metadataValue) external',
  'function getMetadata(uint256 agentId, string calldata metadataKey) external view returns (bytes memory)',
  'function tokenURI(uint256 agentId) external view returns (string memory)',
  'function ownerOf(uint256 agentId) external view returns (address)',
  'event Registered(uint256 indexed agentId, string agentURI, address indexed owner)',
] as const;

/** AgentReputationRegistry minimal ABI (ERC-8004 Reputation) */
const REPUTATION_ABI = [
  'function giveFeedback(uint256 agentId, int128 value, uint8 valueDecimals, string calldata tag1, string calldata tag2, string calldata endpoint, string calldata feedbackURI, bytes32 feedbackHash, bytes calldata proofOfPayment) external',
  'function revokeFeedback(uint256 agentId, uint64 feedbackIndex) external',
  'function getSummary(uint256 agentId, address[] calldata clientAddresses, string calldata tag1, string calldata tag2) external view returns (uint64, uint64, int128)',
  'function getClients(uint256 agentId) external view returns (address[] memory)',
  'event NewFeedback(uint256 indexed agentId, address indexed clientAddress, uint64 feedbackIndex, int128 value, uint8 valueDecimals, string indexed indexedTag1, string tag1, string tag2, string endpoint, string feedbackURI, bytes32 feedbackHash)',
] as const;

/** AgenticCommerceProtocol minimal ABI (ERC-8183 — encrypted escrow) */
const ESCROW_ABI = [
  'function createJob(address provider, address evaluator, uint256 expiredAt, string calldata description, address hook) external returns (uint256)',
  'function setBudget(uint256 jobId, bytes32 encAmount, bytes calldata inputProof, bytes calldata optParams) external',
  'function fund(uint256 jobId, bytes calldata optParams) external',
  'function submit(uint256 jobId, bytes32 deliverable, bytes calldata optParams) external',
  'function complete(uint256 jobId, bytes32 reason, bytes calldata optParams) external',
  'function reject(uint256 jobId, bytes32 reason, bytes calldata optParams) external',
  'function claimRefund(uint256 jobId) external',
  'function getJobStatus(uint256 jobId) external view returns (uint8)',
  'function setPlatformFee(uint64 newFee) external',
  'event JobCreated(uint256 indexed jobId, address indexed client, address indexed provider, address evaluator, uint256 expiredAt)',
  'event BudgetSet(uint256 indexed jobId, address indexed client)',
  'event JobFunded(uint256 indexed jobId, address indexed client)',
  'event JobCompleted(uint256 indexed jobId, address indexed evaluator, bytes32 reason)',
] as const;

// ============================================================================
// Singleton state
// ============================================================================

let initPromise: Promise<void> | null = null;
let wallet: FheWallet;
let session: ZamaFheSession;
let provider: JsonRpcProvider;
let signer: any;

// Lazy contract cache — constructed on first access, not at init
const _contractCache: Record<string, Contract> = {};

// ============================================================================
// Initialization
// ============================================================================

async function loadDfnsCredentialPrivateKey(): Promise<string> {
  if (process.env.DFNS_CREDENTIAL_PRIVATE_KEY) {
    return process.env.DFNS_CREDENTIAL_PRIVATE_KEY;
  }

  const privateKeyPath = process.env.DFNS_PRIVATE_KEY_PATH;
  if (!privateKeyPath) {
    throw new Error(
      'Missing DFNS credential private key. Set DFNS_CREDENTIAL_PRIVATE_KEY or DFNS_PRIVATE_KEY_PATH.',
    );
  }

  const { readFile } = await import('node:fs/promises');
  return (await readFile(privateKeyPath, 'utf8')).trim();
}

async function resolveDfnsWalletMetadata(): Promise<{ address: string; signingKeyId?: string }> {
  const apiUrl = process.env.DFNS_API_URL ?? 'https://api.dfns.io';
  const authToken = process.env.DFNS_AUTH_TOKEN!;
  const walletId = process.env.DFNS_WALLET_ID!;

  const response = await fetch(`${apiUrl}/wallets/${walletId}`, {
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(
      `Failed to fetch DFNS wallet metadata (${response.status} ${response.statusText}): ${body || 'empty response'}`,
    );
  }

  const walletData = await response.json() as { address?: string; signingKey?: { id?: string } };
  if (!walletData.address) {
    throw new Error('DFNS wallet metadata did not include an Ethereum address.');
  }

  return {
    address: walletData.address,
    ...(walletData.signingKey?.id ? { signingKeyId: walletData.signingKey.id } : {}),
  };
}

/** Core init — wallet, encryption, provider. NO contracts constructed here. */
async function init(): Promise<void> {
  provider = new JsonRpcProvider(RPC_URL);
  const chain = (process.env.CHAIN ?? (RPC_URL.includes('mainnet') ? 'mainnet' : 'sepolia')) as 'mainnet' | 'sepolia';
  const expectedChainId = chain === 'mainnet' ? 1 : 11155111;
  const walletMode = process.env.WALLET_MODE;

  if (walletMode === 'ledger-bridge') {
    if (!process.env.LEDGER_BRIDGE_TOKEN) {
      throw new Error('Missing LEDGER_BRIDGE_TOKEN for WALLET_MODE=ledger-bridge');
    }

    const timeoutValue = process.env.LEDGER_BRIDGE_TIMEOUT_MS;
    const requestTimeoutMs = timeoutValue ? Number.parseInt(timeoutValue, 10) : undefined;
    if (timeoutValue && (!Number.isFinite(requestTimeoutMs) || requestTimeoutMs <= 0)) {
      throw new Error('LEDGER_BRIDGE_TIMEOUT_MS must be a positive integer number of milliseconds');
    }

    wallet = createLedgerBridgeWallet(
      {
        bridgeUrl: process.env.LEDGER_BRIDGE_URL ?? 'http://127.0.0.1:4555',
        authToken: process.env.LEDGER_BRIDGE_TOKEN,
        expectedChainId,
        ...(requestTimeoutMs ? { requestTimeoutMs } : {}),
      },
      provider,
    );
  } else if (walletMode === 'dfns' || (!walletMode && process.env.DFNS_WALLET_ID)) {
    const missing = ['DFNS_AUTH_TOKEN', 'DFNS_CREDENTIAL_ID'].filter((name) => !process.env[name]);

    if (missing.length > 0) {
      throw new Error(`Missing DFNS env vars: ${missing.join(', ')}`);
    }

    if (!process.env.DFNS_WALLET_ID) {
      throw new Error('Missing DFNS_WALLET_ID for WALLET_MODE=dfns');
    }

    const credentialPrivateKey = await loadDfnsCredentialPrivateKey();
    const metadata = await resolveDfnsWalletMetadata();
    if (!process.env.DFNS_KEY_ID && metadata.signingKeyId) {
      process.env.DFNS_KEY_ID = metadata.signingKeyId;
    }

    wallet = createDfnsWallet(
      {
        apiUrl: process.env.DFNS_API_URL ?? 'https://api.dfns.io',
        appId: process.env.DFNS_APP_ID,
        authToken: process.env.DFNS_AUTH_TOKEN!,
        walletId: process.env.DFNS_WALLET_ID,
        credentialId: process.env.DFNS_CREDENTIAL_ID!,
        credentialPrivateKey,
        credentialAlgorithm: process.env.DFNS_CREDENTIAL_ALGORITHM,
        address: metadata.address,
      },
      provider
    );
  } else if (walletMode === 'user' || (!walletMode && process.env.USER_PRIVATE_KEY)) {
    if (!process.env.USER_PRIVATE_KEY) {
      throw new Error('Missing USER_PRIVATE_KEY for WALLET_MODE=user');
    }
    wallet = createUserWallet(process.env.USER_PRIVATE_KEY, provider);
  } else if (walletMode) {
    throw new Error(`Unsupported WALLET_MODE: ${walletMode}`);
  } else {
    throw new Error(
      'Set WALLET_MODE=ledger-bridge with LEDGER_BRIDGE_TOKEN, USER_PRIVATE_KEY, or DFNS_WALLET_ID + DFNS_AUTH_TOKEN + DFNS_CREDENTIAL_ID + (DFNS_CREDENTIAL_PRIVATE_KEY or DFNS_PRIVATE_KEY_PATH)',
    );
  }

  session = await ZamaFheSession.create({ rpcUrl: RPC_URL, chain, sessionTTL: 3_600_000 });

  signer = wallet.getSigner();
}

/** Contract address → ABI mapping. Lazy: only constructed when first accessed. */
const CONTRACT_DEFS: Record<string, { address: () => string; abi: readonly string[] }> = {
  cUSDC:      { address: () => CUSDC_ADDRESS,      abi: TOKEN_ABI },
  usdc:       { address: () => USDC_ADDRESS,        abi: ERC20_ABI },
  verifier:   { address: () => VERIFIER_ADDRESS,    abi: VERIFIER_ABI },
  identity:   { address: () => IDENTITY_ADDRESS,    abi: IDENTITY_ABI },
  reputation: { address: () => REPUTATION_ADDRESS,  abi: REPUTATION_ABI },
  escrow:     { address: () => ESCROW_ADDRESS,      abi: ESCROW_ABI },
};

/** Get a contract instance, constructing it on first access per session. */
function getContract(name: string): Contract {
  if (!_contractCache[name]) {
    const def = CONTRACT_DEFS[name];
    if (!def) throw new Error(`Unknown contract: ${name}`);
    const addr = def.address() || ('0x' + '00'.repeat(20));
    // Empty addresses get zero-address fallback — ethers will throw on the first
    // actual RPC call, but construction succeeds (needed for test mocks).
    _contractCache[name] = new Contract(addr, def.abi, signer);
  }
  return _contractCache[name];
}

// ============================================================================
// Public API
// ============================================================================

export async function getContracts(): Promise<{
  wallet: FheWallet;
  session: ZamaFheSession;
  provider: JsonRpcProvider;
  cUSDC: Contract;
  usdc: Contract;
  verifier: Contract;
  identity: Contract;
  reputation: Contract;
  escrow: Contract;
}> {
  if (!initPromise) initPromise = init();
  await initPromise;

  // Contracts are truly lazy: only constructed when a command destructures them.
  // `const { escrow, wallet } = await getContracts()` only constructs escrow
  // (plus cUSDC/usdc which are always needed). identity/reputation/verifier
  // are NOT constructed unless the command actually reads them.
  const base = { wallet, session, provider };
  return new Proxy(base as any, {
    get(target, prop: string) {
      if (prop in target) return (target as any)[prop];
      if (prop in CONTRACT_DEFS) return getContract(prop);
      return undefined;
    },
  });
}

// ============================================================================
// Amount helpers
// ============================================================================

/**
 * Parse a human-readable USDC string to micro-USDC bigint.
 * "2.5" → 2_500_000n
 */
export function parseAmount(str: string): bigint {
  const trimmed = str.trim();
  if (!/^\d+(\.\d+)?$/.test(trimmed)) {
    throw new Error(`Invalid amount "${trimmed}". Must be a positive decimal number.`);
  }
  const [whole, dec = ''] = trimmed.split('.');
  const padded = dec.padEnd(6, '0').slice(0, 6);
  const raw = BigInt(whole) * 1_000_000n + BigInt(padded);
  if (raw <= 0n) {
    throw new Error('Amount must be positive (> 0).');
  }
  return raw;
}

/** Format micro-USDC bigint to human-readable string. 2_500_000n → "2.50" */
export function formatUSDC(raw: bigint): string {
  return (Number(raw) / 1_000_000).toFixed(2);
}

// ============================================================================
// Output helpers
// ============================================================================

export function ok(data: Record<string, unknown>): string {
  return JSON.stringify({ ok: true, ...data });
}

export function fail(msg: string): string {
  return JSON.stringify({ ok: false, error: msg });
}

// ============================================================================
// CLI argument parsing
// ============================================================================

/**
 * Parse argv-style arguments into a key→value map.
 * Handles "--key=value" and "--key value" forms.
 */
export function parseCliArgs(argv: string[]): Record<string, string> {
  const options: Record<string, { type: 'string' }> = {};
  for (const arg of argv) {
    if (arg.startsWith('--')) {
      const key = arg.split('=')[0].slice(2);
      if (key) options[key] = { type: 'string' };
    }
  }
  const { values } = parseArgs({ args: argv, options, strict: false });
  return values as Record<string, string>;
}
