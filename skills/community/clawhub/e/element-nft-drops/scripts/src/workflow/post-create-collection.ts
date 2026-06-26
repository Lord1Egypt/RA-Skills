import { waitForCollectionContract } from "./wait-collection-contract";
import { buildCollectionEditPayload, type CollectionMetadataPatch } from "./design-payloads";
import type {
  ElementChainCollectionSummary,
  ElementCollectionDetailFromEditors,
  ElementCollectionEditInput,
  ElementCollectionSummary
} from "../types";

export interface PostCreateCollectionInput {
  chainMId: number;
  contractAddress: string;
  authorization?: string;
  imageFilePath?: string;
  collectionMetadata?: CollectionMetadataPatch;
  pollIntervalMs?: number;
  timeoutMs?: number;
}

export interface PostCreateCollectionDeps {
  getCollectionContract: (input: {
    address: string;
    blockChain: {
      chain: string;
      chainId: string;
    };
  }) => Promise<ElementChainCollectionSummary | null>;
  getMutateToken: (authorization?: string) => Promise<string>;
  getCollectionDetailFromEditors: (
    slug: string,
    authorization?: string
  ) => Promise<ElementCollectionDetailFromEditors>;
  collectionEdit: (input: ElementCollectionEditInput, authorization?: string) => Promise<ElementCollectionSummary>;
  sleep?: (ms: number) => Promise<void>;
  now?: () => number;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}

export async function postCreateCollectionFlow(
  input: PostCreateCollectionInput,
  deps: PostCreateCollectionDeps
) {
  const collectionContract = await waitForCollectionContract(
    {
      chainMId: input.chainMId,
      contractAddress: input.contractAddress,
      pollIntervalMs: input.pollIntervalMs,
      timeoutMs: input.timeoutMs
    },
    {
      getCollectionContract: deps.getCollectionContract,
      sleep: deps.sleep,
      now: deps.now,
      logger: deps.logger
    }
  );

  deps.logger?.("postCreateCollection:get mutate token", {
    contractAddress: input.contractAddress
  });
  const mutateToken = await deps.getMutateToken(input.authorization);
  deps.logger?.("postCreateCollection:get detail", {
    slug: collectionContract.collection.slug
  });
  const collectionDetail = await deps.getCollectionDetailFromEditors(
    collectionContract.collection.slug,
    input.authorization
  );
  deps.logger?.("postCreateCollection:collection edit", {
    collectionId: collectionContract.collection.id,
    slug: collectionContract.collection.slug
  });
  const collectionEdit = await deps.collectionEdit(
    buildCollectionEditPayload({
      current: collectionDetail,
      patch: input.collectionMetadata ?? {},
      token: mutateToken,
      imageFilePath: input.imageFilePath
    }),
    input.authorization
  );

  return {
    collectionContract,
    mutateToken,
    collectionDetail,
    collectionEdit
  };
}
