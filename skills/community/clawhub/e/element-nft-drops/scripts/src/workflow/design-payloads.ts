import type {
  DesignUploadPayload,
  ElementCollectionDetailFromEditors,
  ElementCollectionEditInput,
  GetDropDesignResponse
} from "../types";
import { normalizeSocialLinkSuffix, normalizeWebsiteUrl } from "./links";

export interface CollectionMetadataPatch {
  description?: string;
  website?: string;
  twitter?: string;
  instagram?: string;
  discord?: string;
  telegram?: string;
  medium?: string;
}

export interface DesignPayloadPatch extends CollectionMetadataPatch {
  name?: string;
  preReveal?: string;
  previewMedia?: string[];
  bannerFilePath?: string;
  previewFilePaths?: string[];
  dropFeaturedImage?: string;
}

const EMPTY_DESIGN: GetDropDesignResponse = {
  dropID: 0,
  dropName: "",
  bannerURL: "",
  previewMedia: [],
  previewMediaExt: [],
  description: "",
  website: "",
  twitter: "",
  instagram: "",
  discord: "",
  telegram: "",
  medium: "",
  dropFeaturedImage: "",
  details: []
};

export function hasCollectionMetadataOverride(input: CollectionMetadataPatch): boolean {
  return Boolean(
    input.description !== undefined ||
      input.website !== undefined ||
      input.twitter !== undefined ||
      input.instagram !== undefined ||
      input.discord !== undefined ||
      input.telegram !== undefined ||
      input.medium !== undefined
  );
}

export function hasDesignOverride(input: DesignPayloadPatch): boolean {
  return Boolean(
    input.preReveal !== undefined ||
      input.previewMedia !== undefined ||
      input.bannerFilePath ||
      (input.previewFilePaths && input.previewFilePaths.length > 0) ||
      input.name !== undefined ||
      input.description !== undefined ||
      input.dropFeaturedImage !== undefined
  );
}

export function buildCollectionEditPayload(input: {
  current: ElementCollectionDetailFromEditors;
  patch: CollectionMetadataPatch;
  token: string;
  imageFilePath?: string;
}): ElementCollectionEditInput {
  return {
    collectionId: input.current.id,
    token: input.token,
    imageFilePath: input.imageFilePath,
    image: input.imageFilePath ? null : undefined,
    description: input.patch.description ?? input.current.description ?? undefined,
    externalUrl: normalizeWebsiteUrl(input.patch.website ?? input.current.externalUrl) || undefined,
    twitterUrl: normalizeSocialLinkSuffix("twitter", input.patch.twitter ?? input.current.twitterUrl) || undefined,
    instagramUrl:
      normalizeSocialLinkSuffix("instagram", input.patch.instagram ?? input.current.instagramUrl) || undefined,
    discordUrl: normalizeSocialLinkSuffix("discord", input.patch.discord ?? input.current.discordUrl) || undefined,
    telegramUrl:
      normalizeSocialLinkSuffix("telegram", input.patch.telegram ?? input.current.telegramUrl) || undefined,
    mediumUrl: normalizeSocialLinkSuffix("medium", input.patch.medium ?? input.current.mediumUrl) || undefined,
    categories: input.current.categories.map((item) => item.id),
    paymentTokens: input.current.paymentTokens.map((item) => item.id)
  };
}

export function buildMergedDesignPayload(input: {
  current: GetDropDesignResponse | null;
  patch: DesignPayloadPatch;
  chainMId: number;
  contractAddress: string;
  dropID: number;
  uploadedBannerUrl?: string | null;
  uploadedPreviewUrls?: string[];
}): DesignUploadPayload {
  const current = input.current ?? EMPTY_DESIGN;
  return {
    dropID: input.dropID,
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropName: input.patch.name ?? current.dropName,
    bannerURL: input.uploadedBannerUrl ?? current.bannerURL ?? "",
    previewMediaExt: (() => {
      if (input.uploadedPreviewUrls && input.uploadedPreviewUrls.length > 0) {
        return input.uploadedPreviewUrls.map((url) => ({
          image_url: url,
          animation_url: ""
        }));
      }
      return current.previewMediaExt.map((item) => ({
        image_url: item.image_url ?? "",
        animation_url: item.animation_url ?? ""
      }));
    })(),
    dropFeaturedImage: input.patch.dropFeaturedImage ?? current.dropFeaturedImage ?? "",
    description: input.patch.description ?? current.description ?? "",
    website: normalizeWebsiteUrl(input.patch.website ?? current.website),
    twitter: normalizeSocialLinkSuffix("twitter", input.patch.twitter ?? current.twitter),
    instagram: normalizeSocialLinkSuffix("instagram", input.patch.instagram ?? current.instagram),
    discord: normalizeSocialLinkSuffix("discord", input.patch.discord ?? current.discord),
    telegram: normalizeSocialLinkSuffix("telegram", input.patch.telegram ?? current.telegram),
    medium: normalizeSocialLinkSuffix("medium", input.patch.medium ?? current.medium),
    detailsUpdate: current.details ?? []
  };
}

export function buildDisplayDesignAfterUpdate(input: {
  current: GetDropDesignResponse | null;
  designPayload: DesignUploadPayload | null;
  collectionEditPayload: ElementCollectionEditInput | null;
}) {
  const hasAnyUpdate = Boolean(input.current || input.designPayload || input.collectionEditPayload);
  if (!hasAnyUpdate) {
    return null;
  }

  const current = input.current ?? EMPTY_DESIGN;
  const design = input.designPayload;
  const collection = input.collectionEditPayload;

  return {
    bannerURL: design?.bannerURL ?? current.bannerURL ?? "",
    previewMediaExt: design?.previewMediaExt ?? current.previewMediaExt ?? [],
    description: design?.description ?? current.description ?? "",
    website: collection?.externalUrl ?? design?.website ?? current.website ?? "",
    twitter: collection?.twitterUrl ?? design?.twitter ?? current.twitter ?? "",
    instagram: collection?.instagramUrl ?? design?.instagram ?? current.instagram ?? "",
    discord: collection?.discordUrl ?? design?.discord ?? current.discord ?? "",
    telegram: collection?.telegramUrl ?? design?.telegram ?? current.telegram ?? "",
    medium: collection?.mediumUrl ?? design?.medium ?? current.medium ?? "",
    dropFeaturedImage: design?.dropFeaturedImage ?? current.dropFeaturedImage ?? ""
  };
}
