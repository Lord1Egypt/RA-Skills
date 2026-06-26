import type { CreateStageInput, DropEdition, GetDropDesignResponse, GetDropSettingsStage, StageInput } from "../types";
import { resolveMintingTypeFromPaymentToken } from "../network/chains";
import { DEFAULT_MAX_SUPPLY, resolveDropMode } from "../drop-mode";
import { buildDropUrls, buildInitialSettingsPayload, createWorkflowLogger, runStage } from "./create-drop";
import {
  buildCollectionEditPayload,
  buildDisplayDesignAfterUpdate,
  buildMergedDesignPayload,
  hasCollectionMetadataOverride,
  hasDesignOverride
} from "./design-payloads";
import { uploadWithExistingAuthorization } from "./uploads";
import type {
  ChainListPaymentToken,
  DesignUploadPayload,
  ElementApiResponse,
  ElementCollectionDetailFromEditors,
  ElementCollectionEditInput,
  ElementCollectionSummary,
  GetDropSettingsResponse,
  OssSignedPostData,
  PostDropSettingsRequest,
  PreRevealUploadPayload
} from "../types";

export interface ConfigureDropFlowInput {
  chainMId: number;
  authorization: string;
  walletAddress: string;
  contractAddress: string;
  slug?: string;
  name?: string;
  symbol?: string;
  paymentToken?: string;
  paymentTokens?: ChainListPaymentToken[];
  preReveal?: string;
  previewMedia?: string[];
  description?: string;
  edition?: DropEdition;
  dropType?: 0 | 1;
  maxSupply?: number;
  dropBeginTime?: number;
  stages?: CreateStageInput[];
  bannerFilePath?: string;
  previewFilePaths?: string[];
  website?: string;
  twitter?: string;
  instagram?: string;
  discord?: string;
  telegram?: string;
  medium?: string;
  dropFeaturedImage?: string;
}

export interface ConfigureDropFlowDeps {
  uploadWithExistingAuthorization: typeof uploadWithExistingAuthorization;
  getDropSettings: (
    query: { chainMId: number; contractAddress: string },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetDropSettingsResponse>>;
  getDropDesign: (
    query: { dropID: number; chainMId: number; contractAddress: string },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetDropDesignResponse>>;
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
  getMutateToken: (authorization?: string) => Promise<string>;
  getCollectionDetailFromEditors: (
    slug: string,
    authorization?: string
  ) => Promise<ElementCollectionDetailFromEditors>;
  collectionEdit: (
    input: ElementCollectionEditInput,
    authorization?: string
  ) => Promise<ElementCollectionSummary>;
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
}

const DEFAULT_STAGE_DURATION_SECONDS = 3 * 24 * 60 * 60;
const DEFAULT_STAGE_NAME = "Public";
const DEFAULT_STAGE_PRICE = "0";
const DEFAULT_STAGE_INTERVAL = 0;
const DEFAULT_STAGE_MAX_MINTED_PER_WALLET = 1;
const DEFAULT_STAGE_ID = 256;

function hasSettingsOverride(input: ConfigureDropFlowInput): boolean {
  return Boolean(
    input.preReveal !== undefined ||
      input.edition !== undefined ||
      input.dropType !== undefined ||
      input.maxSupply !== undefined ||
      input.dropBeginTime !== undefined ||
      input.paymentToken !== undefined ||
      (input.stages !== undefined && input.stages.length >= 0)
  );
}

function defaultDropBeginTime(): number {
  return Math.floor(Date.now() / 1000) + 24 * 60 * 60;
}

function assignStageIds(stages: CreateStageInput[]): StageInput[] {
  return stages.map((stage, index) => ({
    ...stage,
    stageID: DEFAULT_STAGE_ID + index
  }));
}

function buildDefaultStage(maxSupply: number): StageInput {
  return {
    stageID: DEFAULT_STAGE_ID,
    stageName: DEFAULT_STAGE_NAME,
    price: DEFAULT_STAGE_PRICE,
    duration: DEFAULT_STAGE_DURATION_SECONDS,
    maxSupplyAtThisStage: maxSupply,
    maxMintedPerWallet: DEFAULT_STAGE_MAX_MINTED_PER_WALLET,
    interval: DEFAULT_STAGE_INTERVAL,
    stageMode: 0
  };
}

export async function previewConfigureDrop(input: {
  authorization: string;
  walletAddress: string;
  chainMId: number;
  contractAddress: string;
  slug?: string;
  patch: Omit<ConfigureDropFlowInput, "authorization" | "walletAddress" | "chainMId" | "contractAddress" | "slug">;
}, deps: Pick<ConfigureDropFlowDeps, "getDropSettings" | "getDropDesign" | "getMutateToken" | "getCollectionDetailFromEditors">) {
  const logger = createWorkflowLogger();
  const mergedInput: ConfigureDropFlowInput = {
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    authorization: input.authorization,
    walletAddress: input.walletAddress,
    slug: input.slug,
    ...input.patch
  };
  const currentSettingsResponse = await runStage(logger, "previewUpdate:getCurrentSettings", () =>
    deps.getDropSettings(
      {
        chainMId: input.chainMId,
        contractAddress: input.contractAddress
      },
      input.walletAddress
    )
  );
  const currentSettings = currentSettingsResponse.data;
  const shouldUpdateSettings = hasSettingsOverride(mergedInput);
  const settingsPayload = shouldUpdateSettings
    ? buildMergedSettingsPayload({
        current: currentSettings,
        patch: mergedInput,
        contractAddress: input.contractAddress
      })
    : null;
  const shouldUpdateDesign = hasDesignOverride(mergedInput);
  const currentDesignResponse =
    currentSettings.dropID > 0 && shouldUpdateDesign
      ? await runStage(logger, "previewUpdate:getCurrentDesign", () =>
          deps.getDropDesign(
            {
              dropID: currentSettings.dropID,
              chainMId: input.chainMId,
              contractAddress: input.contractAddress
            },
            input.walletAddress
          )
        )
      : null;
  const currentDesign = currentDesignResponse?.data ?? null;
  const designPayload =
    shouldUpdateDesign
      ? buildMergedDesignPayload({
          current: currentDesign,
          patch: mergedInput,
          chainMId: input.chainMId,
          contractAddress: input.contractAddress,
          dropID: currentSettings.dropID,
          uploadedBannerUrl: null,
          uploadedPreviewUrls: undefined
        })
      : null;
  const collectionEditPayload =
    input.slug && hasCollectionMetadataOverride(mergedInput)
      ? buildCollectionEditPayload({
          current: await runStage(logger, "previewUpdate:getCurrentCollectionDetail", () =>
            deps.getCollectionDetailFromEditors(input.slug!, input.authorization)
          ),
          patch: mergedInput,
          token: await runStage(logger, "previewUpdate:getMutateToken", () => deps.getMutateToken(input.authorization))
        })
      : null;

  return {
    contractAddress: input.contractAddress,
    chainMId: input.chainMId,
    slug: input.slug ?? null,
    urls: input.slug ? buildDropUrls(input.slug) : null,
    currentSettings: currentSettingsResponse,
    currentDesign: currentDesignResponse,
    settingsPayload,
    designPayload,
    collectionEditPayload,
    summary: {
      dropID: currentSettings.dropID,
      willReadCurrentSettings: true,
      willReadCurrentDesign: shouldUpdateDesign,
      willUpdateSettings: shouldUpdateSettings,
      willUpdatePreReveal: Boolean(mergedInput.preReveal),
      willUpdateDesign: shouldUpdateDesign,
      willUpdateCollectionProfile: Boolean(collectionEditPayload),
      willUploadImages: Boolean(
        mergedInput.preReveal ??
          mergedInput.bannerFilePath ??
          (mergedInput.previewFilePaths && mergedInput.previewFilePaths.length > 0)
      ),
      patchKeys: Object.keys(mergedInput).filter((key) => {
        const value = mergedInput[key as keyof ConfigureDropFlowInput];
        return value !== undefined && !["authorization", "walletAddress", "chainMId", "contractAddress", "slug"].includes(key);
      }),
      nextSettings: settingsPayload
        ? {
            dropType: settingsPayload.dropType,
            maxSupply: settingsPayload.maxSupply,
            dropBeginTime: settingsPayload.dropBeginTime,
            mintingType: settingsPayload.mintingType,
            stageCount: settingsPayload.stagesUpdate.length
          }
        : null,
      nextDesign: designPayload
        ? {
            dropName: designPayload.dropName,
            bannerURL: designPayload.bannerURL,
            previewCount: designPayload.previewMediaExt.length,
            description: designPayload.description,
            website: designPayload.website,
            twitter: designPayload.twitter,
            instagram: designPayload.instagram,
            discord: designPayload.discord,
            telegram: designPayload.telegram,
            medium: designPayload.medium
          }
        : null,
      nextCollectionProfile: collectionEditPayload
        ? {
            externalUrl: collectionEditPayload.externalUrl ?? null,
            twitterUrl: collectionEditPayload.twitterUrl ?? null,
            instagramUrl: collectionEditPayload.instagramUrl ?? null,
            discordUrl: collectionEditPayload.discordUrl ?? null,
            telegramUrl: collectionEditPayload.telegramUrl ?? null,
            mediumUrl: collectionEditPayload.mediumUrl ?? null
          }
        : null
    }
  };
}

function mapCurrentStages(stages: GetDropSettingsStage[] | null | undefined): StageInput[] {
  if (!stages || stages.length === 0) {
    return [];
  }
  return stages.map((stage) => ({
    stageID: stage.stageID,
    stageName: stage.stageName,
    price: stage.price,
    duration: stage.duration,
    maxSupplyAtThisStage: stage.maxSupplyAtThisStage,
    maxMintedPerWallet: stage.maxMintedPerWallet,
    interval: stage.interval,
    stageMode: (stage.stageMode === 1 ? 1 : 0) as 0 | 1
  }));
}

function buildMergedSettingsPayload(input: {
  current: GetDropSettingsResponse;
  patch: ConfigureDropFlowInput;
  contractAddress: string;
}): PostDropSettingsRequest {
  const { dropType, maxSupply } = resolveDropMode({
    requestedEdition: input.patch.edition,
    requestedDropType: input.patch.dropType,
    requestedMaxSupply: input.patch.maxSupply,
    fallbackDropType: input.current.dropType ?? undefined,
    fallbackMaxSupply: input.current.maxSupply ?? DEFAULT_MAX_SUPPLY
  });
  const stages =
    input.patch.stages && input.patch.stages.length > 0
      ? assignStageIds(input.patch.stages)
      : (() => {
          const currentStages = mapCurrentStages(input.current.stages);
          return currentStages.length > 0 ? currentStages : [buildDefaultStage(maxSupply)];
        })();

  return {
    dropID: input.current.dropID ?? 0,
    chainMId: input.patch.chainMId,
    contractAddress: input.contractAddress,
    dropType,
    maxSupply,
    fee: input.current.fee ?? 0,
    feeRecipient: input.current.feeRecipient ?? "",
    mintingType: resolveMintingTypeFromPaymentToken({
      paymentToken: input.patch.paymentToken,
      availablePaymentTokens: input.patch.paymentTokens,
      fallbackMintingType: input.current.mintingType ?? 0
    }),
    dropBeginTime: input.patch.dropBeginTime ?? input.current.dropBeginTime ?? defaultDropBeginTime(),
    stagesUpdate: stages.map((stage) => ({
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

function hasCurrentBanner(current: GetDropDesignResponse | null): boolean {
  return Boolean(current?.bannerURL?.trim());
}

function hasCurrentPreviewMedia(current: GetDropDesignResponse | null): boolean {
  return Boolean(
    current?.previewMediaExt?.some((item) => item.image_url?.trim() || item.animation_url?.trim()) ||
      current?.previewMedia?.some((item) => {
        if (typeof item === "string") {
          return item.trim().length > 0;
        }
        if (item && typeof item === "object") {
          const record = item as Record<string, unknown>;
          return Boolean(
            (typeof record.image_url === "string" && record.image_url.trim()) ||
              (typeof record.imageURL === "string" && record.imageURL.trim()) ||
              (typeof record.animation_url === "string" && record.animation_url.trim()) ||
              (typeof record.animationURL === "string" && record.animationURL.trim())
          );
        }
        return false;
      })
  );
}

export function resolveDesignAssetUrlsForUpdate(input: {
  currentDesign: GetDropDesignResponse | null;
  preRevealUrl?: string | null;
  explicitBannerProvided: boolean;
  explicitPreviewProvided: boolean;
  uploadedBannerUrl?: string | null;
  uploadedPreviewUrls?: string[];
}): { uploadedBannerUrl: string | null; uploadedPreviewUrls: string[] | undefined } {
  const preRevealUrl = input.preRevealUrl?.trim();
  const uploadedPreviewUrls =
    input.uploadedPreviewUrls && input.uploadedPreviewUrls.length > 0
      ? input.uploadedPreviewUrls
      : !input.explicitPreviewProvided && preRevealUrl && !hasCurrentPreviewMedia(input.currentDesign)
        ? [preRevealUrl]
        : undefined;

  return {
    uploadedBannerUrl:
      input.uploadedBannerUrl ??
      (!input.explicitBannerProvided && preRevealUrl && !hasCurrentBanner(input.currentDesign) ? preRevealUrl : null),
    uploadedPreviewUrls
  };
}

export async function configureDropFlow(input: ConfigureDropFlowInput, deps: ConfigureDropFlowDeps) {
  const logger = createWorkflowLogger();
  const auth = {
    authorization: input.authorization,
    walletAddress: input.walletAddress
  };
  const preRevealPath = input.preReveal;

  const currentSettingsResponse = await runStage(logger, "getCurrentSettings", () =>
    deps.getDropSettings(
      {
        chainMId: input.chainMId,
        contractAddress: input.contractAddress
      },
      auth.walletAddress
    )
  );
  const currentSettings = currentSettingsResponse.data;
  const currentDropID = currentSettings.dropID ?? 0;
  const shouldUpdateSettings = hasSettingsOverride(input);
  const shouldUpdateDesign = hasDesignOverride(input);
  const shouldUpdateCollectionMetadata = Boolean(input.slug && hasCollectionMetadataOverride(input));

  const settingsPayload = shouldUpdateSettings
    ? buildMergedSettingsPayload({
        current: currentSettings,
        patch: input,
        contractAddress: input.contractAddress
      })
    : null;
  const settingsResponse = settingsPayload
    ? await runStage(logger, "postSettings", () =>
        deps.postDropSettings(auth.authorization, settingsPayload, auth.walletAddress)
      )
    : null;
  const settingsAfterConfigure =
    settingsPayload
      ? await runStage(logger, "getSettingsAfterConfigure", () =>
          deps.getDropSettings(
            {
              chainMId: input.chainMId,
              contractAddress: input.contractAddress
            },
            auth.walletAddress
          )
        )
      : currentSettingsResponse;
  const dropID = settingsAfterConfigure.data.dropID ?? currentDropID;

  const preRevealUpload = preRevealPath
    ? await runStage(logger, "uploadPreReveal", () =>
        deps.uploadWithExistingAuthorization(
          auth,
          {
            mode: "prereveal",
            chainMId: input.chainMId,
            contractAddress: input.contractAddress,
            dropType: resolveDropMode({
              requestedEdition: input.edition,
              requestedDropType: input.dropType,
              requestedMaxSupply: input.maxSupply,
              fallbackDropType: currentSettings.dropType ?? undefined,
              fallbackMaxSupply: currentSettings.maxSupply ?? DEFAULT_MAX_SUPPLY
            }).dropType,
            filePath: preRevealPath
          },
          {
            getOssSignSingle: deps.getOssSignSingle,
            postPreReveal: deps.postPreReveal,
            uploadAsset: deps.uploadAsset
          }
        )
      )
    : null;

  if ((shouldUpdateDesign || input.bannerFilePath || (input.previewFilePaths && input.previewFilePaths.length > 0)) && !(dropID > 0)) {
    throw new Error(`dropID is missing for design update on ${input.contractAddress}`);
  }

  const currentDesignResponse =
    dropID > 0 && shouldUpdateDesign
      ? await runStage(logger, "getCurrentDesign", () =>
          deps.getDropDesign(
            {
              dropID,
              chainMId: input.chainMId,
              contractAddress: input.contractAddress
            },
            auth.walletAddress
          )
        )
      : null;
  const currentDesign = currentDesignResponse?.data ?? null;

  const assetDesignUpload =
    input.bannerFilePath ||
    (input.previewMedia && input.previewMedia.length > 0) ||
    (input.previewFilePaths && input.previewFilePaths.length > 0)
      ? await runStage(logger, "uploadDesignAssets", () => {
          const designBannerFilePath = input.bannerFilePath;
          const designPreviewFilePaths = input.previewMedia?.length
            ? input.previewMedia
            : input.previewFilePaths?.length
            ? input.previewFilePaths
            : [];
          if (!designBannerFilePath && designPreviewFilePaths.length === 0) {
            throw new Error("design asset update requires at least one banner or preview source");
          }
          return deps.uploadWithExistingAuthorization(
            auth,
            {
              mode: "design",
              chainMId: input.chainMId,
              contractAddress: input.contractAddress,
              dropID,
              dropName: input.name ?? currentDesign?.dropName ?? "",
              bannerFilePath: designBannerFilePath,
              previewFilePaths: designPreviewFilePaths
            },
            {
              getOssSignSingle: deps.getOssSignSingle,
              postPreReveal: deps.postPreReveal,
              uploadAsset: deps.uploadAsset
            }
          );
        })
      : null;

  const designAssetUrls = resolveDesignAssetUrlsForUpdate({
    currentDesign,
    preRevealUrl: preRevealUpload?.publicUrls[0],
    explicitBannerProvided: Boolean(input.bannerFilePath),
    explicitPreviewProvided: Boolean(
      (input.previewMedia && input.previewMedia.length > 0) ||
        (input.previewFilePaths && input.previewFilePaths.length > 0)
    ),
    uploadedBannerUrl: assetDesignUpload?.mode === "design" ? assetDesignUpload.payload.bannerURL : null,
    uploadedPreviewUrls:
      assetDesignUpload?.mode === "design"
        ? assetDesignUpload.payload.previewMediaExt.map((item) => item.image_url ?? "").filter(Boolean)
        : undefined
  });

  const designPayload =
    shouldUpdateDesign
      ? buildMergedDesignPayload({
          current: currentDesign,
          patch: input,
          chainMId: input.chainMId,
          contractAddress: input.contractAddress,
          dropID,
          uploadedBannerUrl: designAssetUrls.uploadedBannerUrl,
          uploadedPreviewUrls: designAssetUrls.uploadedPreviewUrls
        })
      : null;

  const designResponse =
    designPayload
      ? await runStage(logger, "postDesign", () =>
          deps.postDesign(auth.authorization, designPayload, auth.walletAddress)
        )
      : null;
  const designBannerUrl = designPayload?.bannerURL ?? null;
  const collectionEditPayload =
    shouldUpdateCollectionMetadata
      ? buildCollectionEditPayload({
          current: await runStage(logger, "getCurrentCollectionDetail", () =>
            deps.getCollectionDetailFromEditors(input.slug!, auth.authorization)
          ),
          patch: input,
          token: await runStage(logger, "getMutateToken", () => deps.getMutateToken(auth.authorization))
        })
      : null;
  const collectionEditResponse =
    collectionEditPayload
      ? await runStage(logger, "collectionEdit", () =>
          deps.collectionEdit(collectionEditPayload, auth.authorization)
        )
      : null;
  const urls = input.slug ? buildDropUrls(input.slug) : null;
  return {
    currentSettings,
    contractAddress: input.contractAddress,
    currentSettingsResponse,
    settingsPayload,
    settingsResponse,
    settingsAfterConfigure,
    dropID,
    preRevealUpload,
    currentDesignResponse,
    designPayload,
    designResponse,
    collectionEditPayload,
    collectionEditResponse,
    designUpload: assetDesignUpload,
    designBannerUrl,
    slug: input.slug ?? null,
    urls
  };
}
