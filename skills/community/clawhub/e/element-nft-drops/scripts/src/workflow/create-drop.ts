import { normalizeCreateDropInput } from "../schema";
import { resolveMintingTypeFromPaymentToken } from "../network/chains";
import { HttpRequestError } from "../api/http";
import { redactKnownSecrets } from "../env";
import { buildMergedDesignPayload } from "./design-payloads";
import { createTokenFlow } from "./create-token";
import { postCreateCollectionFlow } from "./post-create-collection";
import { uploadWithExistingAuthorization } from "./uploads";
import type {
  CreateDropInput,
  ElementApiResponse,
  EncodedTransaction,
  GetDropSettingsResponse,
  OssSignedPostData,
  ExecutedTransactionResult,
  DesignUploadPayload,
  PreRevealUploadPayload,
  ElementCollectionDetailFromEditors,
  ElementChainCollectionSummary,
  ElementCollectionSummary,
  ElementCollectionEditInput,
  DropInput,
  PostDropSettingsRequest,
  ChainListPaymentToken
} from "../types";

export type WorkflowLogger = (message: string, meta?: Record<string, unknown>) => void;

export interface CreateDropFlowInput extends CreateDropInput {
  chainName?: string;
  paymentTokens?: ChainListPaymentToken[];
  bannerFilePath?: string;
  previewFilePaths?: string[];
  pollIntervalMs?: number;
  timeoutMs?: number;
  preRevealIPFSPollIntervalMs?: number;
  preRevealIPFSTimeoutMs?: number;
}

export function createWorkflowLogger(): WorkflowLogger {
  return (message, meta = {}) => {
    if (!message.endsWith(":failed")) {
      return;
    }
    const timestamp = new Date().toISOString();
    console.error(`[element-drop] ${timestamp} ${message} ${JSON.stringify(meta)}`);
  };
}

export function buildDropUrls(slug: string) {
  return {
    dropUrl: `https://element.market/drop/${slug}`,
    collectionUrl: `https://element.market/collections/${slug}`,
    editUrl: `https://element.market/collections/${slug}/edit/drop`
  };
}

export function buildCreatedDropSummary(result: {
  chainName?: string;
  symbol?: string;
  contractAddress: string;
  dropID: number;
  slug: string;
  urls: {
    dropUrl: string;
    collectionUrl: string;
    editUrl: string;
  };
  createToken: {
    transaction: {
      hash: string;
    };
  };
}) {
  return {
    chainName: result.chainName ?? null,
    symbol: result.symbol ?? null,
    contractAddress: result.contractAddress,
    dropID: result.dropID,
    slug: result.slug,
    createTransactionHash: result.createToken.transaction.hash,
    dropUrl: result.urls.dropUrl,
    collectionUrl: result.urls.collectionUrl,
    editUrl: result.urls.editUrl,
    nextRecommendedAction:
      result.chainName && result.slug
        ? {
            action: "publish-drop",
            description:
              "The drop is configured but not live yet. Preview publish, then publish after explicit confirmation.",
            payload: {
              chainName: result.chainName,
              slug: result.slug
            }
          }
        : null
  };
}

export async function runStage<T>(
  logger: WorkflowLogger,
  stage: string,
  fn: () => Promise<T>
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    const message = redactKnownSecrets(error instanceof Error ? error.message : String(error));
    const httpMeta =
      error instanceof HttpRequestError
        ? {
            method: error.method,
            url: error.url,
            status: error.status,
            attempts: error.attempts,
            maxAttempts: error.maxAttempts,
            durationMs: error.durationMs,
            timedOut: error.timedOut,
            retriable: error.retriable
          }
        : undefined;
    logger(`${stage}:failed`, {
      error: message,
      ...(httpMeta ? { http: httpMeta } : {})
    });

    const suffix = httpMeta
      ? ` [${httpMeta.method} ${httpMeta.url}; attempts=${httpMeta.attempts}/${httpMeta.maxAttempts}; status=${httpMeta.status ?? "network"}; timeout=${httpMeta.timedOut}; durationMs=${httpMeta.durationMs}]`
      : "";
    throw new Error(`${stage} failed: ${message}${suffix}`);
  }
}

export interface CreateDropFlowDeps {
  createTokenFlow: typeof createTokenFlow;
  postCreateCollectionFlow: typeof postCreateCollectionFlow;
  uploadWithExistingAuthorization: typeof uploadWithExistingAuthorization;
  getDropSettings: (
    query: { chainMId: number; contractAddress: string },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetDropSettingsResponse>>;
  postDropSettings: (
    authorization: string,
    body: PostDropSettingsRequest,
    walletAddress: string
  ) => Promise<ElementApiResponse<null>>;
  getOssSignSingle: (
    authorization: string,
    query: { chainMId: number; contractAddress: string; mediaType: "prereveal" | "design" },
    walletAddress?: string
  ) => Promise<ElementApiResponse<OssSignedPostData>>;
  postPreReveal: (
    authorization: string,
    body: PreRevealUploadPayload,
    walletAddress?: string
  ) => Promise<ElementApiResponse<null>>;
  postDesign: (
    authorization: string,
    body: DesignUploadPayload,
    walletAddress?: string
  ) => Promise<ElementApiResponse<null>>;
  uploadAsset: (input: {
    filePath: string;
    fileName: string;
    oss: OssSignedPostData;
  }) => Promise<{
    sourcePath: string;
    fileName: string;
    objectKey: string;
    publicUrl: string;
  }>;
  createAuthorization: (chainMId: number) => Promise<{
    authorization: string;
    walletAddress: string;
    nonce: string;
    loginMessage: string;
    identity: {
      address: string;
      blockChain: {
        chain: string;
        chainId: string;
      };
    };
  }>;
  deriveAddress: (input: { privateKey: string }) => Promise<string>;
  resolveRpcUrl: (chainMId: number) => Promise<string>;
  createAuthorizationForToken: (input: {
    privateKey: string;
    walletAddress?: string;
    chainMId: number;
  }) => Promise<{
    authorization: string;
    nonce: string;
    message: string;
    identity: {
      address: string;
      blockChain: {
        chain: string;
        chainId: string;
      };
    };
  }>;
  postCreateToken: (
    authorization: string,
    body: { chainMId: number; name: string; symbol: string },
    walletAddress?: string
  ) => Promise<ElementApiResponse<EncodedTransaction>>;
  sendTransaction: (input: {
    rpcUrl: string;
    transaction: EncodedTransaction;
    waitConfirmations?: number;
  }) => Promise<ExecutedTransactionResult>;
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
}

export function buildInitialSettingsPayload(input: {
  normalized: Pick<DropInput, "chainMId" | "dropType" | "maxSupply" | "dropBeginTime" | "stages" | "paymentToken">;
  contractAddress: string;
  availablePaymentTokens?: ChainListPaymentToken[];
}): PostDropSettingsRequest {
  return {
    dropID: 0,
    chainMId: input.normalized.chainMId,
    contractAddress: input.contractAddress,
    dropType: input.normalized.dropType,
    maxSupply: input.normalized.maxSupply,
    fee: 0,
    feeRecipient: "",
    mintingType: resolveMintingTypeFromPaymentToken({
      paymentToken: input.normalized.paymentToken,
      availablePaymentTokens: input.availablePaymentTokens
    }),
    dropBeginTime: input.normalized.dropBeginTime,
    stagesUpdate: input.normalized.stages.map((stage) => ({
      stageID: stage.stageID,
      stageName: stage.stageName,
      price: stage.price,
      interval: stage.interval,
      duration: stage.duration,
      maxMintedPerWallet: stage.maxMintedPerWallet,
      maxSupplyAtThisStage: stage.maxSupplyAtThisStage,
      stageMode: stage.stageMode,
      allowListsNew: []
    }))
  };
}

export async function createDropFlow(input: CreateDropFlowInput, deps: CreateDropFlowDeps) {
  const logger = createWorkflowLogger();
  const normalized = normalizeCreateDropInput(input);

  const createToken = await runStage(logger, "createToken", () =>
    deps.createTokenFlow(normalized, {
      deriveAddress: deps.deriveAddress,
      resolveRpcUrl: deps.resolveRpcUrl,
      createAuthorization: deps.createAuthorizationForToken,
      postCreateToken: deps.postCreateToken,
      sendTransaction: deps.sendTransaction,
      logger
    })
  );

  const contractAddress = createToken.transaction.contractAddress;
  if (!contractAddress) {
    throw new Error("contractAddress missing from createToken transaction receipt");
  }

  const postCreateCollection = await runStage(logger, "postCreateCollection", () =>
    deps.postCreateCollectionFlow(
      {
        chainMId: normalized.chainMId,
        contractAddress,
        authorization: createToken.preflight.authorization,
        imageFilePath: normalized.preReveal,
        collectionMetadata: {
          description: normalized.description,
          website: input.website,
          twitter: input.twitter,
          instagram: input.instagram,
          discord: input.discord,
          telegram: input.telegram,
          medium: input.medium
        },
        pollIntervalMs: input.pollIntervalMs,
        timeoutMs: input.timeoutMs
      },
      {
        getCollectionContract: deps.getCollectionContract,
        getMutateToken: deps.getMutateToken,
        getCollectionDetailFromEditors: deps.getCollectionDetailFromEditors,
        collectionEdit: deps.collectionEdit,
        logger
      }
    )
  );

  const auth = {
    authorization: createToken.preflight.authorization,
    walletAddress: createToken.preflight.walletAddress
  };

  const initialSettingsPayload = buildInitialSettingsPayload({
    normalized,
    contractAddress,
    availablePaymentTokens: input.paymentTokens
  });
  const initialSettings = await runStage(logger, "postInitialSettings", () =>
    deps.postDropSettings(auth.authorization, initialSettingsPayload, auth.walletAddress)
  );

  const settingsAfterCreate = await runStage(logger, "getSettingsAfterCreate", () =>
    deps.getDropSettings(
      {
        chainMId: normalized.chainMId,
        contractAddress
      },
      auth.walletAddress
    )
  );
  const dropID = settingsAfterCreate.data.dropID;
  if (!(dropID > 0)) {
    throw new Error(`getSettingsAfterCreate returned invalid dropID for ${contractAddress}: ${dropID}`);
  }

  const preRevealUpload = await runStage(logger, "uploadPreReveal", () =>
    deps.uploadWithExistingAuthorization(
      auth,
      {
        mode: "prereveal",
        chainMId: normalized.chainMId,
        contractAddress,
        dropType: normalized.dropType,
        filePath: normalized.preReveal
      },
      {
        getOssSignSingle: deps.getOssSignSingle,
        postPreReveal: deps.postPreReveal,
        uploadAsset: deps.uploadAsset
      }
    )
  );

  const designBannerFilePath = input.bannerFilePath ?? normalized.preReveal;
  const designPreviewFilePaths = input.previewMedia?.length
    ? input.previewMedia
    : input.previewFilePaths?.length
      ? input.previewFilePaths
    : [normalized.preReveal];
  const designUpload = await runStage(logger, "uploadDesign", () =>
    deps.uploadWithExistingAuthorization(
      auth,
      {
        mode: "design",
        chainMId: normalized.chainMId,
        contractAddress,
        dropID,
        dropName: normalized.name,
        bannerFilePath: designBannerFilePath,
        previewFilePaths: designPreviewFilePaths
      },
      {
        getOssSignSingle: deps.getOssSignSingle,
        postPreReveal: deps.postPreReveal,
        uploadAsset: deps.uploadAsset
      }
    )
  );
  if (designUpload.mode !== "design") {
    throw new Error("uploadDesign returned a non-design payload");
  }
  const designPayload = buildMergedDesignPayload({
    current: {
      dropID,
      dropName: designUpload.payload.dropName,
      bannerURL: designUpload.payload.bannerURL,
      previewMedia: [],
      previewMediaExt: designUpload.payload.previewMediaExt,
      description: "",
      website: "",
      twitter: "",
      instagram: "",
      discord: "",
      telegram: "",
      medium: "",
      dropFeaturedImage: "",
      details: []
    },
    patch: {
      name: normalized.name,
      description: normalized.description,
      website: input.website,
      twitter: input.twitter,
      instagram: input.instagram,
      discord: input.discord,
      telegram: input.telegram,
      medium: input.medium,
      dropFeaturedImage: input.dropFeaturedImage
    },
    chainMId: normalized.chainMId,
    contractAddress,
    dropID
  });
  const designResponse = await runStage(logger, "postDesign", () =>
    deps.postDesign(auth.authorization, designPayload, auth.walletAddress)
  );
  const designBannerUrl = designPayload.bannerURL;
  const designPreviewCount = designPayload.previewMediaExt.length;

  const slug = postCreateCollection.collectionContract.collection.slug;
  const urls = buildDropUrls(slug);
  return {
    normalized,
    contractAddress,
    createToken,
    postCreateCollection,
    preRevealUpload,
    initialSettingsPayload,
    initialSettings,
    settingsAfterCreate,
    dropID,
    slug,
    urls,
    designUpload: {
      ...designUpload,
      payload: designPayload
    },
    designResponse,
    designBannerUrl,
    summary: buildCreatedDropSummary({
      chainName: input.chainName,
      symbol: normalized.symbol,
      contractAddress,
      dropID,
      slug,
      urls,
      createToken
    })
  };
}
