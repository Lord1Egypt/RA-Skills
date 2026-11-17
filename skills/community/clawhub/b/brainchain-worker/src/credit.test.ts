import { ContractFunctionRevertedError, HttpRequestError, parseAbi, recoverTypedDataAddress, type Address, type Hex } from "viem";
import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";
import { describe, expect, it } from "vitest";

import { CONSENT_DAYS, CONSENT_TYPES, credit, type CreditChain } from "./credit.js";
import { MAINNET } from "./network.js";

const NOW = 1_800_000_000n;

function chainFor(owner: Address, signer = privateKeyToAccount(generatePrivateKey())): CreditChain {
  return {
    account: signer.address,
    ownerOf: async () => owner,
    nonce: async () => 3n,
    now: async () => NOW,
    sign: (message) =>
      signer.signTypedData({ domain: { name: "Priors Credit", version: "2", chainId: 4663, verifyingContract: MAINNET.priors!.pool }, types: CONSENT_TYPES, primaryType: "Consent", message }),
  };
}

describe("credit", () => {
  it("signs Priors' consent for BrainChain's root with the agent owner's key and posts it to the service", async () => {
    const key = privateKeyToAccount(generatePrivateKey());
    const posts: { url: string; body: { consent: Record<string, string>; signature: Hex } }[] = [];
    const lines: string[] = [];
    const fetcher = (async (url: string | URL | Request, init?: RequestInit) => {
      posts.push({ url: String(url), body: JSON.parse(String(init?.body)) });
      return new Response(JSON.stringify({ agentId: "501", kept: true }), { status: 200 });
    }) as typeof fetch;
    await credit(MAINNET, chainFor(key.address, key), { agentId: 501n, premiumBps: 0n, log: (l) => lines.push(l), fetcher });
    expect(posts[0]!.url).toBe(`${MAINNET.service}/priors/consents`);
    const { consent, signature } = posts[0]!.body;
    expect(consent).toEqual({ agentId: "501", sponsorId: "20423", owner: key.address, maxPremiumBps: "0", nonce: "3", deadline: String(NOW + BigInt(CONSENT_DAYS * 86_400)) });
    const signer = await recoverTypedDataAddress({
      domain: { name: "Priors Credit", version: "2", chainId: 4663, verifyingContract: MAINNET.priors!.pool },
      types: CONSENT_TYPES,
      primaryType: "Consent",
      message: { agentId: 501n, sponsorId: 20423n, owner: key.address, maxPremiumBps: 0n, nonce: 3n, deadline: BigInt(consent.deadline!) },
      signature,
    });
    expect(signer).toBe(key.address);
    expect(lines[0]).toBe(`Consent sent for agent 501, valid for ${CONSENT_DAYS} days.`);
  });

  it("refuses to sign with a key that does not own the agent, and passes on the service's refusal", async () => {
    const owner = privateKeyToAccount(generatePrivateKey()).address;
    await expect(credit(MAINNET, chainFor(owner), { agentId: 501n, premiumBps: 0n, log: () => {} })).rejects.toThrow(`Agent 501 is owned by ${owner}`);
    const key = privateKeyToAccount(generatePrivateKey());
    const refused = (async () => new Response(JSON.stringify({ error: "No staked BrainChain worker declared agent 501 in its application. Join with --agent-id first." }), { status: 404 })) as typeof fetch;
    await expect(credit(MAINNET, chainFor(key.address, key), { agentId: 501n, premiumBps: 0n, log: () => {}, fetcher: refused })).rejects.toThrow(/Join with --agent-id first/);
  });

  it("says there is no such agent when the registry reverts, and that it could not be read otherwise", async () => {
    const reverted = new ContractFunctionRevertedError({ abi: parseAbi(["function ownerOf(uint256) view returns (address)"]), functionName: "ownerOf", message: 'reverted with signature 0x7e273289' });
    const key = privateKeyToAccount(generatePrivateKey());
    const none = { ...chainFor(key.address, key), ownerOf: async () => Promise.reject(reverted) };
    await expect(credit(MAINNET, none, { agentId: 99_999_999_999n, premiumBps: 0n, log: () => {} })).rejects.toThrow(/^There is no ERC-8004 agent 99999999999 on Robinhood Chain\.$/);
    const down = { ...chainFor(key.address, key), ownerOf: async () => Promise.reject(new HttpRequestError({ url: "https://rpc.example.com", details: "fetch failed" })) };
    await expect(credit(MAINNET, down, { agentId: 5n, premiumBps: 0n, log: () => {} })).rejects.toThrow("ERC-8004 agent 5 could not be read on Robinhood Chain: Could not reach rpc.example.com (fetch failed)");
  });
});
