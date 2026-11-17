import { BaseError, ContractFunctionRevertedError, createPublicClient, http, parseAbi, type Address, type Hex, type PrivateKeyAccount } from "viem";

import { reason } from "./chain.js";
import { parentChainOf, type Network } from "./network.js";

/** Priors' credit pool on Robinhood Chain, where BrainChain's identity is a root sponsor. */
export interface PriorsConfig {
  pool: Address;
  /** BrainChain's ERC-8004 agent id, the root a consent names. */
  root: bigint;
}

export const CONSENT_TYPES = {
  Consent: [
    { name: "agentId", type: "uint256" },
    { name: "sponsorId", type: "uint256" },
    { name: "owner", type: "address" },
    { name: "maxPremiumBps", type: "uint256" },
    { name: "nonce", type: "uint256" },
    { name: "deadline", type: "uint256" },
  ],
} as const;

/** How long a consent stays usable: long enough for the worker to prove itself first. */
export const CONSENT_DAYS = 30;

const poolAbi = parseAbi(["function nonces(uint256 agentId) view returns (uint256)"]);
const identityAbi = parseAbi(["function ownerOf(uint256 agentId) view returns (address)"]);

export interface CreditChain {
  account: Address;
  ownerOf(agentId: bigint): Promise<Address>;
  nonce(agentId: bigint): Promise<bigint>;
  now(): Promise<bigint>;
  sign(consent: { agentId: bigint; sponsorId: bigint; owner: Address; maxPremiumBps: bigint; nonce: bigint; deadline: bigint }): Promise<Hex>;
}

export function createCreditChain(network: Network, account: PrivateKeyAccount): CreditChain {
  const priors = network.priors;
  if (!priors || !network.identity || !network.bridge) throw new Error(`${network.name} has no Priors credit pool`);
  const parent = createPublicClient({ chain: parentChainOf(network.bridge), transport: http(network.bridge.rpc, { timeout: 20_000 }) });
  return {
    account: account.address,
    ownerOf: (agentId) => parent.readContract({ address: network.identity!, abi: identityAbi, functionName: "ownerOf", args: [agentId] }),
    nonce: (agentId) => parent.readContract({ address: priors.pool, abi: poolAbi, functionName: "nonces", args: [agentId] }),
    now: async () => (await parent.getBlock()).timestamp,
    sign: (message) =>
      account.signTypedData({
        domain: { name: "Priors Credit", version: "2", chainId: network.bridge!.chainId, verifyingContract: priors.pool },
        types: CONSENT_TYPES,
        primaryType: "Consent",
        message,
      }),
  };
}

/**
 * Signs Priors' consent to BrainChain's sponsorship with the key that owns the
 * worker's ERC-8004 agent, and posts it to the service. BrainChain's operator
 * vouches a line once the worker is proven on the board; the consent lets only
 * BrainChain's identity sponsor the agent, at no more than the premium given.
 */
export async function credit(
  network: Network,
  chain: CreditChain,
  options: { agentId: bigint; premiumBps: bigint; log: (line: string) => void; fetcher?: typeof fetch },
): Promise<void> {
  const priors = network.priors!;
  const { agentId, log } = options;
  let owner: Address;
  try {
    owner = await chain.ownerOf(agentId);
  } catch (error) {
    // The registry reverts ownerOf for an id it never minted; anything else says nothing about the agent.
    if (error instanceof BaseError && error.walk((e) => e instanceof ContractFunctionRevertedError)) throw new Error(`There is no ERC-8004 agent ${agentId} on Robinhood Chain.`);
    throw new Error(`ERC-8004 agent ${agentId} could not be read on Robinhood Chain: ${reason(error)}`);
  }
  if (owner.toLowerCase() !== chain.account.toLowerCase()) {
    throw new Error(`Agent ${agentId} is owned by ${owner}. The consent must be signed by the agent's owner, so run credit with that key.`);
  }
  const [nonce, now] = await Promise.all([chain.nonce(agentId), chain.now()]);
  const consent = { agentId, sponsorId: priors.root, owner, maxPremiumBps: options.premiumBps, nonce, deadline: now + BigInt(CONSENT_DAYS * 86_400) };
  const signature = await chain.sign(consent);
  const body = JSON.stringify({ consent: Object.fromEntries(Object.entries(consent).map(([k, v]) => [k, typeof v === "bigint" ? v.toString() : v])), signature });
  const response = await (options.fetcher ?? fetch)(`${network.service}/priors/consents`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body,
    signal: AbortSignal.timeout(20_000),
  });
  const answer = (await response.json().catch(() => ({}))) as { error?: string };
  if (!response.ok) throw new Error(answer.error ?? `${response.status} from ${network.service}`);
  log(`Consent sent for agent ${agentId}, valid for ${CONSENT_DAYS} days.`);
  log("BrainChain backs a 25 USDG line on Priors once this worker has 3 accepted tasks, more accepted than refunded,");
  log("and has not let two hires in a row expire. Borrow and repay it with Priors' own tools: https://priors.trade/skill.md");
}
