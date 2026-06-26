/**
 * ERC-8004 Identity Registration (Stub)
 *
 * Sends agent profile to backend for on-chain registration
 * on the ERC-8004 Agent Identity Registry (Base mainnet).
 *
 * The actual on-chain transaction is handled by the backend
 * to avoid requiring the user to hold ETH for gas.
 *
 * Registry contracts (from erc8004-poc.ts):
 *   Base Mainnet:
 *     Identity: 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
 *     Reputation: 0x8004BAa17C55a88189AE136b182e5fdA19dE9b63
 *   Base Sepolia:
 *     Identity: 0x8004A818BFB912233c491871b3d84c89A494BD9e
 *     Reputation: 0x8004B663056A597Dffe9eCcC1965A193B7388713
 */

export const ERC8004_CONTRACTS = {
  BASE_MAINNET: {
    IDENTITY_REGISTRY: '0x8004A169FB4a3325136EB29fA0ceB6D2e539a432' as const,
    REPUTATION_REGISTRY: '0x8004BAa17C55a88189AE136b182e5fdA19dE9b63' as const,
  },
  BASE_SEPOLIA: {
    IDENTITY_REGISTRY: '0x8004A818BFB912233c491871b3d84c89A494BD9e' as const,
    REPUTATION_REGISTRY: '0x8004B663056A597Dffe9eCcC1965A193B7388713' as const,
  },
} as const;

export interface AgentProfile {
  name: string;
  skills: string[];
  endpoint: string;
  walletAddress?: string;
}

export interface RegistrationResult {
  success: boolean;
  tokenId?: number;
  txHash?: string;
  registryAddress?: string;
  message: string;
}

export interface ReputationInfo {
  reputation: number;
  feedbackCount: number;
}

const BLOOM_API_URL =
  process.env.BLOOM_API_URL || 'https://api.bloomprotocol.ai';

/**
 * Register an agent identity on the ERC-8004 registry via backend.
 *
 * When backend is ready:
 * - POST /api/registry/register { name, skills, endpoint, walletAddress }
 * - Backend calls IdentityRegistry.register() on-chain
 *
 * Current stub: returns placeholder response.
 */
export async function registerIdentity(
  profile: AgentProfile
): Promise<RegistrationResult> {
  // TODO: Replace with actual API call when backend is ready
  //
  // const response = await fetch(`${BLOOM_API_URL}/api/registry/register`, {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(profile),
  // });
  // return await response.json();

  const network = process.env.NETWORK || 'base-mainnet';
  const contracts =
    network === 'base-sepolia'
      ? ERC8004_CONTRACTS.BASE_SEPOLIA
      : ERC8004_CONTRACTS.BASE_MAINNET;

  return {
    success: false,
    registryAddress: contracts.IDENTITY_REGISTRY,
    message:
      `ERC-8004 registration API not yet available. ` +
      `Agent "${profile.name}" with ${profile.skills.length} skill(s) ` +
      `will be registered on ${network} when the backend endpoint is ready.`,
  };
}

/**
 * Check if an agent is already registered on the ERC-8004 registry.
 *
 * Stub: always returns false until backend is ready.
 */
export async function isRegistered(
  _walletAddress: string
): Promise<boolean> {
  // TODO: Backend query → IdentityRegistry.isRegistered(address)
  return false;
}

/**
 * Get reputation info for a registered agent.
 *
 * Stub: returns zero values until backend is ready.
 */
export async function getReputation(
  _walletAddress: string
): Promise<ReputationInfo> {
  // TODO: Backend query → ReputationRegistry.getReputation(address)
  return {
    reputation: 0,
    feedbackCount: 0,
  };
}
