import type {
  CallbackUpdateProjectConfigRequest,
  ElementApiResponse,
  EncodedTransaction,
  ExecutedTransactionResult,
  GetDropSettingsResponse,
  GetPreRevealIPFSResponse,
  GetTempURLResponse,
  PostDropSettingsRequest,
  StageMode,
  SetProjectConfigRequest
} from "../types";

export interface WaitForPreRevealIPFSInput {
  chainMId: number;
  contractAddress: string;
  dropID: number;
  walletAddress: string;
  pollIntervalMs?: number;
  timeoutMs?: number;
}

export interface WaitForPreRevealIPFSDeps {
  getPreRevealIPFS: (
    query: { chainMId: number; contractAddress: string; dropID: number },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetPreRevealIPFSResponse>>;
  sleep?: (ms: number) => Promise<void>;
  now?: () => number;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}

export interface WaitForPublishedInput {
  chainMId: number;
  contractAddress: string;
  dropID: number;
  walletAddress: string;
  expectedPublished?: number;
  expectedIsPaused?: boolean;
  pollIntervalMs?: number;
  timeoutMs?: number;
}

export interface WaitForPublishedDeps {
  postCallbackUpdateProjectConfig: (
    body: CallbackUpdateProjectConfigRequest
  ) => Promise<ElementApiResponse<null>>;
  getDropSettings: (
    query: { chainMId: number; contractAddress: string },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetDropSettingsResponse>>;
  sleep?: (ms: number) => Promise<void>;
  now?: () => number;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}

export interface ResolvePublishPreRevealInput {
  authorization: string;
  walletAddress: string;
  chainMId: number;
  contractAddress: string;
  dropID: number;
  pollIntervalMs?: number;
  timeoutMs?: number;
}

export interface ResolvePublishPreRevealDeps {
  getTempURL: (
    authorization: string,
    query: { chainMId: number; contractAddress: string; dropID: number; page: number; pageSize: number },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetTempURLResponse>>;
  getPreRevealIPFS: (
    query: { chainMId: number; contractAddress: string; dropID: number },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetPreRevealIPFSResponse>>;
  sleep?: (ms: number) => Promise<void>;
  now?: () => number;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}

export interface PublishDropFlowInput {
  authorization: string;
  walletAddress: string;
  rpcUrl: string;
  chainMId: number;
  contractAddress: string;
  dropID: number;
  isPaused?: boolean;
  getSettingsPollIntervalMs?: number;
  getSettingsTimeoutMs?: number;
  preRevealIPFSPollIntervalMs?: number;
  preRevealIPFSTimeoutMs?: number;
}

export interface PublishDropFlowDeps {
  getDropSettings: (
    query: { chainMId: number; contractAddress: string },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetDropSettingsResponse>>;
  getPreRevealIPFS: (
    query: { chainMId: number; contractAddress: string; dropID: number },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetPreRevealIPFSResponse>>;
  getTempURL: (
    authorization: string,
    query: { chainMId: number; contractAddress: string; dropID: number; page: number; pageSize: number },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetTempURLResponse>>;
  postDropSettings: (
    authorization: string,
    body: PostDropSettingsRequest,
    walletAddress: string
  ) => Promise<ElementApiResponse<null>>;
  postSetProjectConfig: (
    authorization: string,
    body: SetProjectConfigRequest,
    walletAddress: string
  ) => Promise<ElementApiResponse<EncodedTransaction>>;
  sendTransaction: (input: {
    rpcUrl: string;
    transaction: EncodedTransaction;
    waitConfirmations?: number;
    logger?: (message: string, meta?: Record<string, unknown>) => void;
  }) => Promise<ExecutedTransactionResult>;
  postCallbackUpdateProjectConfig: (
    body: CallbackUpdateProjectConfigRequest
  ) => Promise<ElementApiResponse<null>>;
  sleep?: (ms: number) => Promise<void>;
  now?: () => number;
  logger?: (message: string, meta?: Record<string, unknown>) => void;
}

async function defaultSleep(ms: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

export function extractPreRevealImageUrl(tempURL: GetTempURLResponse | null | undefined): string {
  return tempURL?.preReveal?.image_url?.trim() ?? tempURL?.preReveal?.imageURL?.trim() ?? "";
}

export function extractPreRevealAnimationUrl(tempURL: GetTempURLResponse | null | undefined): string {
  return tempURL?.preReveal?.animation_url?.trim() ?? tempURL?.preReveal?.animationURL?.trim() ?? "";
}

export function assertPreRevealImageUrlExists(input: {
  contractAddress: string;
  preRevealImageUrl: string;
}) {
  if (!input.preRevealImageUrl) {
    throw new Error(
      `publish requires a configured prereveal image URL for ${input.contractAddress}; ` +
        `the current prereveal media resource is empty, so rerun upload/preReveal and retry publish`
    );
  }
}

export function buildPostDropSettingsPayloadFromSettings(input: {
  settings: GetDropSettingsResponse;
  chainMId: number;
  contractAddress: string;
}): PostDropSettingsRequest {
  return {
    dropID: input.settings.dropID,
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropType: input.settings.dropType,
    maxSupply: input.settings.maxSupply ?? 0,
    fee: input.settings.fee ?? 0,
    feeRecipient: input.settings.feeRecipient ?? "",
    mintingType: input.settings.mintingType,
    dropBeginTime: input.settings.dropBeginTime ?? 0,
    stagesUpdate: input.settings.stages.map((stage) => ({
      stageID: stage.stageID,
      stageName: stage.stageName,
      price: stage.price,
      interval: stage.interval,
      duration: stage.duration,
      maxMintedPerWallet: stage.maxMintedPerWallet,
      maxSupplyAtThisStage: stage.maxSupplyAtThisStage,
      stageMode: stage.stageMode as StageMode | null,
      allowListsNew: []
    }))
  };
}

export function buildSetProjectConfigPayload(input: {
  settings: GetDropSettingsResponse;
  chainMId: number;
  contractAddress: string;
  preRevealIPFS: string;
  isPaused?: boolean;
}): SetProjectConfigRequest {
  return {
    isPaused: input.isPaused ?? false,
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    nftAddress: input.contractAddress,
    dropBeginTime: input.settings.dropBeginTime ?? 0,
    maxSupply: String(input.settings.maxSupply ?? 0),
    baseURI: input.preRevealIPFS,
    mintingType: input.settings.mintingType,
    stages: input.settings.stages.map((stage) => ({
      stageID: stage.stageID,
      stageName: stage.stageName,
      stageMode: stage.stageMode,
      price: stage.price,
      address: stage.address ?? "0x0000000000000000000000000000000000000000",
      duration: stage.duration,
      maxSupplyAtThisStage: stage.maxSupplyAtThisStage,
      maxMintedPerWallet: stage.maxMintedPerWallet,
      interval: stage.interval,
      enableCallFromContract: stage.enableCallFromContract,
      enableMintToOther: stage.enableMintToOther
    }))
  };
}

export async function waitForPreRevealIPFS(
  input: WaitForPreRevealIPFSInput,
  deps: WaitForPreRevealIPFSDeps
) {
  const pollIntervalMs = input.pollIntervalMs ?? 5_000;
  const timeoutMs = input.timeoutMs ?? 10 * 60 * 1000;
  const sleep = deps.sleep ?? defaultSleep;
  const now = deps.now ?? Date.now;
  const startedAt = now();
  let attempts = 0;

  while (true) {
    attempts += 1;
    deps.logger?.("preRevealIPFS:poll", {
      attempt: attempts,
      dropID: input.dropID,
      elapsedMs: now() - startedAt
    });
    const response = await deps.getPreRevealIPFS(
      {
        chainMId: input.chainMId,
        contractAddress: input.contractAddress,
        dropID: input.dropID
      },
      input.walletAddress
    );
    const preRevealIPFS = response.data?.preRevealIPFS ?? "";
    if (preRevealIPFS) {
      deps.logger?.("preRevealIPFS:resolved", {
        attempt: attempts,
        dropID: input.dropID,
        preRevealIPFS,
        elapsedMs: now() - startedAt
      });
      return {
        preRevealIPFS,
        attempts,
        elapsedMs: now() - startedAt
      };
    }
    if (now() - startedAt >= timeoutMs) {
      throw new Error(
        `preRevealIPFS timed out after ${attempts} attempts (${timeoutMs}ms) for drop ${input.dropID}; ` +
          `if prereveal OSS to IPFS promotion is stuck, run upload/preReveal again and retry publish`
      );
    }
    await sleep(pollIntervalMs);
  }
}

export async function resolvePublishPreRevealIPFS(
  input: ResolvePublishPreRevealInput,
  deps: ResolvePublishPreRevealDeps
) {
  deps.logger?.("publish:prereveal:read-temp-url", {
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropID: input.dropID
  });
  const tempURLResponse = await deps.getTempURL(
    input.authorization,
    {
      chainMId: input.chainMId,
      contractAddress: input.contractAddress,
      dropID: input.dropID,
      page: 1,
      pageSize: 1
    },
    input.walletAddress
  );
  assertPreRevealImageUrlExists({
    contractAddress: input.contractAddress,
    preRevealImageUrl: extractPreRevealImageUrl(tempURLResponse.data)
  });

  deps.logger?.("publish:prereveal:trigger-and-poll-ipfs", {
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropID: input.dropID
  });
  const preRevealIPFS = await waitForPreRevealIPFS(
    {
      chainMId: input.chainMId,
      contractAddress: input.contractAddress,
      dropID: input.dropID,
      walletAddress: input.walletAddress,
      pollIntervalMs: input.pollIntervalMs,
      timeoutMs: input.timeoutMs
    },
    {
      getPreRevealIPFS: deps.getPreRevealIPFS,
      sleep: deps.sleep,
      now: deps.now,
      logger: deps.logger
    }
  );

  return {
    tempURL: tempURLResponse.data,
    preRevealIPFS
  };
}

export async function waitForPublishedSettings(
  input: WaitForPublishedInput,
  deps: WaitForPublishedDeps
) {
  const pollIntervalMs = input.pollIntervalMs ?? 5_000;
  const timeoutMs = input.timeoutMs ?? 10 * 60 * 1000;
  const expectedPublished = input.expectedPublished ?? 1;
  const expectedIsPaused = input.expectedIsPaused;
  const sleep = deps.sleep ?? defaultSleep;
  const now = deps.now ?? Date.now;
  const startedAt = now();
  let attempts = 0;

  while (true) {
    attempts += 1;
    deps.logger?.("publishedSettings:callback", {
      attempt: attempts,
      dropID: input.dropID,
      contractAddress: input.contractAddress,
      elapsedMs: now() - startedAt
    });
    const callbackResponse = await deps.postCallbackUpdateProjectConfig({
      dropId: input.dropID,
      chainMId: input.chainMId,
      contractAddress: input.contractAddress
    });
    deps.logger?.("publishedSettings:poll", {
      attempt: attempts,
      dropID: input.dropID,
      contractAddress: input.contractAddress,
      callbackCode: callbackResponse.code,
      elapsedMs: now() - startedAt
    });
    const response = await deps.getDropSettings(
      {
        chainMId: input.chainMId,
        contractAddress: input.contractAddress
      },
      input.walletAddress
    );
    const publishedMatches = (response.data?.published ?? 0) === expectedPublished;
    const pausedMatches =
      expectedIsPaused === undefined ? true : (response.data?.isPaused ?? false) === expectedIsPaused;
    if (publishedMatches && pausedMatches) {
      const finalSettingsResponse = await deps.getDropSettings(
        {
          chainMId: input.chainMId,
          contractAddress: input.contractAddress
        },
        input.walletAddress
      );
      deps.logger?.("publishedSettings:resolved", {
        attempt: attempts,
        dropID: input.dropID,
        contractAddress: input.contractAddress,
        expectedPublished,
        expectedIsPaused,
        published: finalSettingsResponse.data?.published ?? 0,
        isPaused: finalSettingsResponse.data?.isPaused ?? false,
        elapsedMs: now() - startedAt
      });
      return {
        settings: finalSettingsResponse.data,
        callbackResponse,
        attempts,
        elapsedMs: now() - startedAt
      };
    }
    if (now() - startedAt >= timeoutMs) {
      throw new Error(
          `published settings timed out after ${attempts} attempts (${timeoutMs}ms) for ${input.contractAddress}; ` +
          `expected published=${expectedPublished}` +
          `${expectedIsPaused === undefined ? "" : ` and isPaused=${expectedIsPaused}`}, ` +
          `got published=${response.data?.published ?? 0} and isPaused=${response.data?.isPaused ?? false}`
      );
    }
    await sleep(pollIntervalMs);
  }
}

export async function publishDropFlow(
  input: PublishDropFlowInput,
  deps: PublishDropFlowDeps
) {
  deps.logger?.("publish:start", {
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropID: input.dropID
  });
  const settingsBeforePublishResponse = await deps.getDropSettings(
    {
      chainMId: input.chainMId,
      contractAddress: input.contractAddress
    },
    input.walletAddress
  );
  const settingsBeforePublish = settingsBeforePublishResponse.data;
  const preRevealResolution = await resolvePublishPreRevealIPFS(
    {
      authorization: input.authorization,
      chainMId: input.chainMId,
      contractAddress: input.contractAddress,
      dropID: input.dropID,
      walletAddress: input.walletAddress,
      pollIntervalMs: input.preRevealIPFSPollIntervalMs,
      timeoutMs: input.preRevealIPFSTimeoutMs
    },
    {
      getTempURL: deps.getTempURL,
      getPreRevealIPFS: deps.getPreRevealIPFS,
      sleep: deps.sleep,
      now: deps.now,
      logger: deps.logger
    }
  );

  const postSettingsPayload = buildPostDropSettingsPayloadFromSettings({
    settings: settingsBeforePublish,
    chainMId: input.chainMId,
    contractAddress: input.contractAddress
  });
  const postSettingsResponse = await deps.postDropSettings(
    input.authorization,
    postSettingsPayload,
    input.walletAddress
  );

  const setProjectConfigPayload = buildSetProjectConfigPayload({
    settings: settingsBeforePublish,
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    preRevealIPFS: preRevealResolution.preRevealIPFS.preRevealIPFS,
    isPaused: input.isPaused
  });
  const setProjectConfigResponse = await deps.postSetProjectConfig(
    input.authorization,
    setProjectConfigPayload,
    input.walletAddress
  );
  if (setProjectConfigResponse.code !== 0) {
    throw new Error(`setProjectConfig failed: ${setProjectConfigResponse.message}`);
  }
  const setProjectConfigTransaction = await deps.sendTransaction({
    rpcUrl: input.rpcUrl,
    transaction: setProjectConfigResponse.data,
    logger: deps.logger
  });

  const callbackPayload = {
    dropId: input.dropID,
    chainMId: input.chainMId,
    contractAddress: input.contractAddress
  };

  const published = await waitForPublishedSettings(
    {
      chainMId: input.chainMId,
      contractAddress: input.contractAddress,
      dropID: input.dropID,
      walletAddress: input.walletAddress,
      expectedPublished: 1,
      expectedIsPaused: setProjectConfigPayload.isPaused,
      pollIntervalMs: input.getSettingsPollIntervalMs,
      timeoutMs: input.getSettingsTimeoutMs
    },
    {
      postCallbackUpdateProjectConfig: deps.postCallbackUpdateProjectConfig,
      getDropSettings: deps.getDropSettings,
      sleep: deps.sleep,
      now: deps.now,
      logger: deps.logger
    }
  );

  return {
    settingsBeforePublish,
    tempURLBeforePublish: preRevealResolution.tempURL,
    preRevealIPFS: preRevealResolution.preRevealIPFS,
    postSettingsPayload,
    postSettingsResponse,
    setProjectConfigPayload,
    setProjectConfigResponse,
    setProjectConfigTransaction,
    callbackPayload,
    published
  };
}
