import { getElementBlockChainByChainMId } from "../auth/jwt";
import type { ElementChainCollectionSummary } from "../types";

export interface WaitForCollectionContractInput {
  chainMId: number;
  contractAddress: string;
  pollIntervalMs?: number;
  timeoutMs?: number;
}

export interface WaitForCollectionContractDeps {
  getCollectionContract: (input: {
    address: string;
    blockChain: {
      chain: string;
      chainId: string;
    };
  }) => Promise<ElementChainCollectionSummary | null>;
  sleep?: (ms: number) => Promise<void>;
  now?: () => number;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}

async function defaultSleep(ms: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

export async function waitForCollectionContract(
  input: WaitForCollectionContractInput,
  deps: WaitForCollectionContractDeps
) {
  const pollIntervalMs = input.pollIntervalMs ?? 5_000;
  const timeoutMs = input.timeoutMs ?? 10 * 60 * 1000;
  const sleep = deps.sleep ?? defaultSleep;
  const now = deps.now ?? Date.now;
  const blockChain = getElementBlockChainByChainMId(input.chainMId);
  const startedAt = now();
  let attempts = 0;

  while (true) {
    attempts += 1;
    deps.logger?.("collectionContract:poll", {
      attempt: attempts,
      contractAddress: input.contractAddress,
      elapsedMs: now() - startedAt
    });
    const collection = await deps.getCollectionContract({
      address: input.contractAddress,
      blockChain
    });

    if (collection) {
      deps.logger?.("collectionContract:resolved", {
        attempt: attempts,
        contractAddress: input.contractAddress,
        slug: collection.slug,
        collectionId: collection.id,
        elapsedMs: now() - startedAt
      });
      return {
        contractAddress: input.contractAddress,
        blockChain,
        attempts,
        elapsedMs: now() - startedAt,
        collection
      };
    }

    if (now() - startedAt >= timeoutMs) {
      throw new Error(
        `CollectionContract timed out after ${attempts} attempts (${timeoutMs}ms) for ${input.contractAddress}`
      );
    }

    await sleep(pollIntervalMs);
  }
}
