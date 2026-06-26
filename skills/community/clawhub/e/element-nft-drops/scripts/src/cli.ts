import { readFile } from "node:fs/promises";
import { stdin as input } from "node:process";
import { createElementApiClient } from "./api/element";
import { createElementGraphqlClient } from "./api/graphql";
import { buildElementAuthorization, deriveWalletAddress, getElementIdentityByChainMId } from "./auth/jwt";
import { normalizeCreateDropInput } from "./schema";
import { deriveEditionFromMaxSupply } from "./drop-mode";
import {
  getElementChainNameByChainMId,
  resolveElementChain,
  resolvePaymentToken,
  resolvePaymentTokenFromMintingType
} from "./network/chains";
import { getRpcUrlForChainMId } from "./network/rpc";
import { sendEncodedTransaction } from "./network/transaction";
import { createDropFlow } from "./workflow/create-drop";
import { previewDropFlow } from "./workflow/preview-drop";
import { configureDropFlow, previewConfigureDrop } from "./workflow/configure-drop";
import { buildDisplayDesignAfterUpdate } from "./workflow/design-payloads";
import { createTokenFlow } from "./workflow/create-token";
import { postCreateCollectionFlow } from "./workflow/post-create-collection";
import {
  extractPreRevealAnimationUrl,
  extractPreRevealImageUrl,
  buildPostDropSettingsPayloadFromSettings,
  buildSetProjectConfigPayload,
  publishDropFlow,
  resolvePublishPreRevealIPFS,
  waitForPreRevealIPFS,
  waitForPublishedSettings
} from "./workflow/publish-drop";
import { formatSocialLinkForDisplay, normalizeWebsiteUrl } from "./workflow/links";
import { uploadSingleAsset, uploadWithExistingAuthorization } from "./workflow/uploads";
import { verifyRefGraphqlExamples } from "./workflow/verify-ref-graphql";
import { waitForCollectionContract } from "./workflow/wait-collection-contract";
import { getRequiredWalletPrivateKey, redactKnownSecrets } from "./env";

const ZERO_ADDRESS = "0x0000000000000000000000000000000000000000";

type CliOperationContext = {
  command?: string;
  chainName?: unknown;
  symbol?: unknown;
  slug?: unknown;
  contractAddress?: unknown;
};

let activeOperationContext: CliOperationContext = {};

function setActiveOperationContext(command: string, payload: Record<string, unknown>) {
  activeOperationContext = {
    command,
    chainName: payload.chainName ?? null,
    symbol: payload.symbol ?? null,
    slug: payload.slug ?? null,
    contractAddress: payload.contractAddress ?? null
  };
}

async function readStdin(): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of input) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf8");
}

const FORBIDDEN_SECRET_PAYLOAD_KEYS = new Set([
  "privateKey",
  "walletPrivateKey",
  "ELEMENT_WALLET_PRIVATE_KEY",
  "mnemonic",
  "seedPhrase"
]);

function assertNoSecretPayloadKeys(value: unknown, path = "$") {
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoSecretPayloadKeys(item, `${path}[${index}]`));
    return;
  }

  if (typeof value !== "object" || value === null) {
    return;
  }

  for (const [key, nestedValue] of Object.entries(value)) {
    const nextPath = `${path}.${key}`;
    if (FORBIDDEN_SECRET_PAYLOAD_KEYS.has(key)) {
      throw new Error(
        `Refusing secret input at ${nextPath}; provide wallet private key only through ELEMENT_WALLET_PRIVATE_KEY`
      );
    }
    assertNoSecretPayloadKeys(nestedValue, nextPath);
  }
}

async function readJsonArg(path?: string) {
  const payload = path ? JSON.parse(await readFile(path, "utf8")) : JSON.parse(await readStdin());
  assertNoSecretPayloadKeys(payload);
  return payload;
}

function getPayloadPath(args: string[]) {
  return args.find((arg) => !arg.startsWith("--"));
}

function listDefinedKeys(input: Record<string, unknown>, excludedKeys: string[] = []) {
  return Object.keys(input).filter((key) => input[key] !== undefined && !excludedKeys.includes(key));
}

function isElementDropCollection(sourceType: string | null | undefined): boolean {
  return typeof sourceType === "string" && sourceType.includes("ELEMENT_DROP");
}

function summarizeEncodedTransaction(input: {
  step: string;
  description: string;
  transaction: { to: string; value: string; data: string };
}) {
  return {
    step: input.step,
    description: input.description,
    to: input.transaction.to,
    value: input.transaction.value,
    dataPrefix: input.transaction.data.slice(0, 18),
    dataLength: input.transaction.data.length
  };
}

function summarizeSupportedPaymentToken(token: {
  name: string;
  symbol?: string;
  TokenAddress: string;
  SerId: number;
} | null) {
  if (!token) {
    return null;
  }

  return {
    name: token.name,
    symbol: token.symbol ?? null,
    address: token.TokenAddress
  };
}

function summarizeNativePaymentToken(currency: unknown) {
  if (typeof currency !== "string" || currency.trim().length === 0) {
    return null;
  }
  return {
    name: currency,
    symbol: currency,
    address: ZERO_ADDRESS
  };
}

function summarizeResolvedPaymentToken(input: {
  mintingType?: unknown;
  availablePaymentTokens?: unknown[];
  currency?: unknown;
}) {
  const mintingType = typeof input.mintingType === "number" ? input.mintingType : undefined;
  const token = summarizeSupportedPaymentToken(
    resolvePaymentTokenFromMintingType({
      mintingType,
      availablePaymentTokens: Array.isArray(input.availablePaymentTokens)
        ? (input.availablePaymentTokens as never[])
        : []
    }) as never
  );
  if (token) {
    return token;
  }
  if (mintingType === undefined || mintingType <= 0) {
    return summarizeNativePaymentToken(input.currency);
  }
  return null;
}

function summarizeEdition(maxSupply: unknown) {
  const edition = deriveEditionFromMaxSupply(maxSupply);
  if (edition === "limited") {
    return { value: 0, label: "limited" };
  }
  if (edition === "open") {
    return { value: 1, label: "open" };
  }
  return { value: null, label: null };
}

function summarizeTimestamp(timestamp: unknown) {
  if (typeof timestamp !== "number" || !Number.isFinite(timestamp) || timestamp <= 0) {
    return null;
  }
  return {
    unix: timestamp,
    iso: new Date(timestamp * 1000).toISOString()
  };
}

function summarizeStage(stage: Record<string, unknown>) {
  return {
    stageName: stage.stageName ?? null,
    price: stage.price ?? null,
    duration: stage.duration ?? null,
    maxSupplyAtThisStage: stage.maxSupplyAtThisStage ?? null,
    maxMintedPerWallet: stage.maxMintedPerWallet ?? null,
    interval: stage.interval ?? null,
    stageMode: stage.stageMode ?? null,
    enableCallFromContract:
      typeof stage.enableCallFromContract === "boolean" ? stage.enableCallFromContract : null,
    enableMintToOther:
      typeof stage.enableMintToOther === "boolean" ? stage.enableMintToOther : null
  };
}

function summarizeSettingsSnapshot(input: {
  maxSupply?: unknown;
  totalMint?: unknown;
  dropBeginTime?: unknown;
  dropType?: unknown;
  mintingType?: unknown;
  stages?: unknown;
  availablePaymentTokens?: unknown[];
  currency?: unknown;
}) {
  const edition = summarizeEdition(input.maxSupply);
  const paymentToken = summarizeResolvedPaymentToken({
    mintingType: input.mintingType,
    availablePaymentTokens: input.availablePaymentTokens,
    currency: input.currency
  });

  return {
    maxSupply: edition.label === "open" ? null : input.maxSupply ?? null,
    totalMint: input.totalMint ?? null,
    dropBeginTime: summarizeTimestamp(input.dropBeginTime),
    edition,
    paymentToken,
    stageCount: Array.isArray(input.stages) ? input.stages.length : 0,
    stages: Array.isArray(input.stages)
      ? input.stages.map((stage) => summarizeStage(stage as Record<string, unknown>))
      : []
  };
}

function summarizeDesignSnapshot(input: {
  bannerURL?: unknown;
  previewMediaExt?: unknown;
  description?: unknown;
  website?: unknown;
  twitter?: unknown;
  instagram?: unknown;
  discord?: unknown;
  telegram?: unknown;
  medium?: unknown;
  dropFeaturedImage?: unknown;
}) {
  const previewMediaExt = Array.isArray(input.previewMediaExt) ? input.previewMediaExt : [];
  return {
    bannerURL: input.bannerURL ?? null,
    previewMediaCount: previewMediaExt.length,
    previewMediaExt: previewMediaExt.map((item) => ({
      image_url:
        typeof item === "object" && item !== null && "image_url" in item ? (item.image_url ?? null) : null,
      animation_url:
        typeof item === "object" && item !== null && "animation_url" in item ? (item.animation_url ?? null) : null
    })),
    description: input.description ?? null,
    website: normalizeWebsiteUrl(typeof input.website === "string" ? input.website : undefined) || null,
    twitter:
      formatSocialLinkForDisplay("twitter", typeof input.twitter === "string" ? input.twitter : undefined) || null,
    instagram:
      formatSocialLinkForDisplay("instagram", typeof input.instagram === "string" ? input.instagram : undefined) ||
      null,
    discord:
      formatSocialLinkForDisplay("discord", typeof input.discord === "string" ? input.discord : undefined) || null,
    telegram:
      formatSocialLinkForDisplay("telegram", typeof input.telegram === "string" ? input.telegram : undefined) ||
      null,
    medium:
      formatSocialLinkForDisplay("medium", typeof input.medium === "string" ? input.medium : undefined) || null,
    dropFeaturedImage: input.dropFeaturedImage ?? null
  };
}

function shouldRepublishUpdatedDrop(input: {
  published?: unknown;
  isPaused?: unknown;
  willUpdateSettings?: unknown;
  willUpdatePreReveal?: unknown;
}) {
  return (
    input.published === 1 &&
    input.isPaused === false &&
    Boolean(input.willUpdateSettings || input.willUpdatePreReveal)
  );
}

function summarizePublishState(input: { published?: unknown; isPaused?: unknown }) {
  if (input.published !== 1) {
    return {
      status: "draft",
      label: "draft"
    };
  }
  if (input.isPaused === true) {
    return {
      status: "paused",
      label: "paused"
    };
  }
  return {
    status: "live",
    label: "live"
  };
}

function summarizePublishTargetState(isPaused: unknown) {
  return isPaused === true
    ? {
        status: "paused",
        label: "publish but keep paused"
      }
    : {
        status: "live",
        label: "publish live"
      };
}

function buildSigningSafetyNote() {
  return {
    privateKeyHandling:
      "The private key is used only for local signing in this script and is never sent over the network.",
    reminder:
      "Network requests may carry derived wallet address, auth token, or signed transactions, but not the raw private key."
  };
}

function buildCreateDropDryRunPreview(
  payload: Record<string, unknown>,
  input: {
    onchainPreview?: {
      createToken?: { to: string; value: string; data: string };
      walletAddress?: string;
    };
  } = {}
) {
  const normalized = normalizeCreateDropInput(payload as never);
  const paymentTokens = Array.isArray(payload.paymentTokens)
    ? payload.paymentTokens.map((token) =>
        typeof token === "object" && token !== null
          ? {
              name: "name" in token ? token.name : undefined,
              address: "TokenAddress" in token ? token.TokenAddress : undefined
            }
          : token
      )
    : [];
  const selectedPaymentTokenRaw =
    typeof payload.paymentToken === "string"
      ? (resolvePaymentToken({
          paymentToken: payload.paymentToken,
          availablePaymentTokens: Array.isArray(payload.paymentTokens) ? (payload.paymentTokens as never[]) : []
        }) as never)
      : null;
  const selectedPaymentToken =
    summarizeSupportedPaymentToken(selectedPaymentTokenRaw) ?? summarizeNativePaymentToken(payload.currency);

  return {
    command: "create-drop",
    previewOnly: true,
    required: {
      chainName: payload.chainName ?? null,
      name: payload.name ?? null,
      symbol: payload.symbol ?? null,
      preReveal: payload.preReveal ?? null
    },
    settingsPreview: summarizeSettingsSnapshot({
      maxSupply: normalized.maxSupply,
      dropBeginTime: normalized.dropBeginTime,
      dropType: normalized.dropType,
      mintingType: selectedPaymentTokenRaw ? (selectedPaymentTokenRaw as { SerId: number }).SerId << 4 : null,
      stages: normalized.stages,
      availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
      currency: payload.currency
    }),
    designPreview: {
      preRevealSource: payload.preReveal ?? null,
      bannerFilePath: payload.bannerFilePath ?? null,
      previewMediaSources:
        Array.isArray(payload.previewMedia) && payload.previewMedia.length > 0
          ? payload.previewMedia
          : Array.isArray(payload.previewFilePaths) && payload.previewFilePaths.length > 0
          ? payload.previewFilePaths
          : [payload.preReveal ?? null].filter(Boolean),
      description: normalized.description || null,
      website: payload.website ?? null,
      twitter: payload.twitter ?? null,
      instagram: payload.instagram ?? null,
      discord: payload.discord ?? null,
      telegram: payload.telegram ?? null,
      medium: payload.medium ?? null,
      dropFeaturedImage: payload.dropFeaturedImage ?? null,
      note: "Create flow uploads and sets prereveal, settings, and initial design before stopping."
    },
    resolvedChain: {
      chainName: payload.chainName ?? null,
      currency: payload.currency ?? null,
      supportedPaymentTokens: paymentTokens
    },
    selectedPaymentToken,
    onchainRisk: {
      hasBlockchainTransaction: true,
      executionRequiresExplicitConfirmation: true,
      note: "This flow deploys a new contract onchain."
    },
    signingSafety: buildSigningSafetyNote(),
    chainOperationNotice: {
      walletAddress: input.onchainPreview?.walletAddress ?? null,
      requiresSignature: true,
      note: "The deployment transaction is prepared for preview only and is not broadcast."
    },
    transactionPreview: input.onchainPreview?.createToken
      ? [
          summarizeEncodedTransaction({
            step: "createToken",
            description: "Deploy the drop contract",
            transaction: input.onchainPreview.createToken
          })
        ]
      : [],
    willUploadImages: true,
    willSendTransactions: true,
    willModifyAvailability: false
  };
}

function buildUpdateDropDryRunPreview(payload: Record<string, unknown>) {
  const patchKeys = listDefinedKeys(payload, [
    "authorization",
    "walletAddress",
    "chainMId",
    "contractAddress",
    "slug",
    "getSettingsPollIntervalMs",
    "getSettingsTimeoutMs"
  ]);
  const hasPreRevealPatch = Boolean(payload.preReveal);
  const hasPreviewMediaPatch = Array.isArray(payload.previewMedia) && payload.previewMedia.length > 0;
  const hasPreviewFilePathsPatch = Array.isArray(payload.previewFilePaths) && payload.previewFilePaths.length > 0;
  const hasDesignPatch = Boolean(
    hasPreviewMediaPatch ||
      payload.bannerFilePath ||
      hasPreviewFilePathsPatch ||
      (payload.name ??
        payload.description ??
        payload.dropFeaturedImage)
  );
  const hasCollectionMetadataPatch = Boolean(
    payload.website ??
      payload.twitter ??
      payload.instagram ??
      payload.discord ??
      payload.telegram ??
      payload.medium
  );

  return {
    command: "update-drop",
    previewOnly: true,
    target: {
      chainName: payload.chainName ?? null,
      slug: payload.slug ?? null
    },
    resolvedTarget: {
      contractAddress: payload.contractAddress ?? null
    },
    resolvedChain: {
      chainName: payload.chainName ?? null,
      currency: payload.currency ?? null,
      supportedPaymentTokens: Array.isArray(payload.paymentTokens)
        ? payload.paymentTokens.map((token) =>
            typeof token === "object" && token !== null
              ? {
                  name: "name" in token ? token.name : undefined,
                  address: "TokenAddress" in token ? token.TokenAddress : undefined
                }
              : token
          )
        : []
    },
    patchKeys,
    patchPreview: {
      settings: {
        preReveal: payload.preReveal ?? null,
        dropType: payload.dropType ?? null,
        maxSupply: payload.maxSupply ?? null,
        dropBeginTime: summarizeTimestamp(payload.dropBeginTime),
        paymentToken: payload.paymentToken ?? null,
        stages:
          Array.isArray(payload.stages) && payload.stages.length > 0
            ? payload.stages.map((stage) => summarizeStage(stage as Record<string, unknown>))
            : []
      },
      design: {
        previewMedia:
          Array.isArray(payload.previewMedia) && payload.previewMedia.length > 0 ? payload.previewMedia : [],
        bannerFilePath: payload.bannerFilePath ?? null,
        previewFilePaths:
          Array.isArray(payload.previewFilePaths) && payload.previewFilePaths.length > 0 ? payload.previewFilePaths : [],
        name: payload.name ?? null,
        description: payload.description ?? null,
        website: payload.website ?? null,
        twitter: payload.twitter ?? null,
        instagram: payload.instagram ?? null,
        discord: payload.discord ?? null,
        telegram: payload.telegram ?? null,
        medium: payload.medium ?? null,
        dropFeaturedImage: payload.dropFeaturedImage ?? null
      }
    },
    willReadCurrentSettings: true,
    willReadCurrentDesign: hasDesignPatch,
    willUpdatePreReveal: hasPreRevealPatch,
    onchainRisk: {
      hasBlockchainTransaction: false,
      executionRequiresExplicitConfirmation: false,
      note: "This flow updates remote settings, prereveal, design, or collection profile fields and does not send an onchain transaction by itself."
    },
    signingSafety: buildSigningSafetyNote(),
    transactionPreview: [],
    willUploadImages: Boolean(
      payload.preReveal || hasPreviewMediaPatch || payload.bannerFilePath || hasPreviewFilePathsPatch
    ),
    willUpdateSettings: true,
    willUpdateDesign: hasDesignPatch,
    willUpdateCollectionProfile: hasCollectionMetadataPatch,
    willSendTransactions: false,
    willModifyAvailability: false
  };
}

function buildPublishDropDryRunPreview(
  payload: Record<string, unknown>,
  input: {
    onchainPreview?: {
      setProjectConfig?: { to: string; value: string; data: string };
      walletAddress?: string;
      setProjectConfigPayload?: { isPaused?: boolean };
      settings?: {
        maxSupply?: number;
        totalMint?: number;
        dropBeginTime?: number;
        dropType?: number;
        mintingType?: number;
        stages?: unknown[];
        isPaused?: boolean;
      };
      tempURL?: {
        preReveal?: {
          imageURL?: string;
          animationURL?: string;
        };
      };
    };
  } = {}
) {
  return {
    command: "publish-drop",
    previewOnly: true,
    target: {
      chainName: payload.chainName ?? null,
      slug: payload.slug ?? null
    },
    resolvedTarget: {
      contractAddress: payload.contractAddress ?? null
    },
    resolvedChain: {
      chainName: payload.chainName ?? null,
      currency: payload.currency ?? null,
      supportedPaymentTokens: Array.isArray(payload.paymentTokens)
        ? payload.paymentTokens.map((token) =>
            typeof token === "object" && token !== null
              ? {
                  name: "name" in token ? token.name : undefined,
                  address: "TokenAddress" in token ? token.TokenAddress : undefined
                }
              : token
          )
        : []
    },
    selectedPaymentToken: summarizeSupportedPaymentToken(
      resolvePaymentTokenFromMintingType({
        mintingType: input.onchainPreview?.settings?.mintingType,
        availablePaymentTokens: Array.isArray(payload.paymentTokens) ? (payload.paymentTokens as never[]) : []
      }) as never
    ) ?? summarizeNativePaymentToken(payload.currency),
    onchainRisk: {
      hasBlockchainTransaction: true,
      executionRequiresExplicitConfirmation: true,
      note: "This flow sends the publish transaction onchain and can make the drop live."
    },
    signingSafety: buildSigningSafetyNote(),
    chainOperationNotice: {
      walletAddress: input.onchainPreview?.walletAddress ?? null,
      requiresSignature: true,
      note:
        input.onchainPreview?.setProjectConfigPayload?.isPaused === true
          ? "The publish transaction is prepared for preview only, will keep the drop paused, and is not broadcast."
          : "The publish transaction is prepared for preview only and is not broadcast."
    },
    publishTarget: {
      state: summarizePublishTargetState(
        input.onchainPreview?.setProjectConfigPayload?.isPaused ?? payload.isPaused
      )
    },
    preRevealCheck: {
      imageURL: input.onchainPreview?.tempURL ? extractPreRevealImageUrl(input.onchainPreview.tempURL as never) : null,
      animationURL:
        input.onchainPreview?.tempURL ? extractPreRevealAnimationUrl(input.onchainPreview.tempURL as never) : null
    },
    publishSequence: [
      "Read current prereveal media status and confirm prereveal OSS image exists",
      "Trigger/check prereveal OSS to IPFS resolution",
      "Poll preRevealIPFS until it becomes non-empty",
      "Prepare postSettings payload from current settings",
      "Encode setProjectConfig with resolved preRevealIPFS",
      "Broadcast publish transaction only during confirmed execution",
      "Alternate callback/updateProjectConfig and edit/settings polling until publish state is synchronized"
    ],
    settingsPreview: input.onchainPreview?.settings
      ? summarizeSettingsSnapshot({
          maxSupply: input.onchainPreview.settings.maxSupply,
          totalMint: input.onchainPreview.settings.totalMint,
          dropBeginTime: input.onchainPreview.settings.dropBeginTime,
          dropType: input.onchainPreview.settings.dropType,
          mintingType: input.onchainPreview.settings.mintingType,
          stages: input.onchainPreview.settings.stages,
          availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
          currency: payload.currency
        })
      : null,
    publishModeNote:
      input.onchainPreview?.setProjectConfigPayload?.isPaused === true
        ? "This publish will leave the drop paused."
        : "This publish will make the drop live.",
    transactionPreview: input.onchainPreview?.setProjectConfig
      ? [
          summarizeEncodedTransaction({
            step: "setProjectConfig",
            description: "Publish the drop onchain",
            transaction: input.onchainPreview.setProjectConfig
          })
        ]
      : [],
    willUploadImages: false,
    willSendTransactions: true,
    willModifyAvailability: true
  };
}

function printHelp() {
  console.log(`element-drop scripts

Lifecycle commands:
  create-drop    Create a new drop, upload prereveal and initial design, and stop before publish.
  preview-drop   Read-only preview of the current settings, design, and prereveal media.
  update-drop    Update only the fields the user explicitly provides.
  publish-drop   Publish an already configured drop.
  list-chains    Read-only list of Element-supported chains and payment tokens.
  list-user-collections  Read-only list of a user's collections on a supported chain.
  list-user-drops  Read-only list of a user's Element Drops on a supported chain.
  get-contract-by-slug   Read-only resolve of collection contract address by slug.

Global flags:
  --preview       Preview a state-changing lifecycle command without mutating anything.

Advanced utilities (not the default user-facing path):
  create-token
  post-create-collection
  get-settings
  post-settings
  get-design
  post-design
  upload-prereveal
  upload-design
  wait-collection-contract
  wait-prereveal-ipfs
  verify-ref-graphql

Minimal lifecycle payloads:

  create-drop
    {
      "chainName": "base",
      "name": "My Drop",
      "symbol": "F",
      "preReveal": "/absolute/path/to/image.png"
    }

  preview-drop
    {
      "chainName": "base",
      "slug": "ffffff-510bce"
    }

  update-drop
    {
      "chainName": "base",
      "slug": "my-drop-510bce",
      "paymentToken": "ETH",
      "maxSupply": 999,
      "previewMedia": [
        "/absolute/path/to/preview-1.png"
      ]
    }

  publish-drop
    {
      "chainName": "base",
      "slug": "my-drop-510bce"
    }

  list-user-drops
    {
      "chainName": "base"
    }
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const commandArgs = args.slice(1);
  const dryRun = commandArgs.includes("--dry-run") || commandArgs.includes("--preview");
  const filePath = getPayloadPath(commandArgs);
  const api = createElementApiClient();
  const graphql = createElementGraphqlClient();

  if (!command || command === "help" || command === "--help" || command === "-h") {
    printHelp();
    return;
  }

  async function resolvePayloadChain<T extends Record<string, unknown>>(payload: T): Promise<T & {
    chainMId: number;
    chainName: string;
    paymentTokens: unknown[];
    currency: string;
  }> {
    activeOperationContext = {
      command,
      chainName: payload.chainName ?? payload.chainMId ?? null,
      symbol: payload.symbol ?? null,
      slug: payload.slug ?? null,
      contractAddress: payload.contractAddress ?? null
    };
    const resolved = await resolveElementChain(
      {
        chainName: typeof payload.chainName === "string" ? payload.chainName : undefined,
        chainMId: typeof payload.chainMId === "number" ? payload.chainMId : undefined
      },
      {
        getChainsWithGas: api.getChainsWithGas
      }
    );

    return {
      ...payload,
      chainMId: resolved.chainMId,
      chainName: resolved.chainName,
      paymentTokens: resolved.paymentTokens,
      currency: resolved.currency
    };
  }

  async function createAuthorization(chainMId: number) {
    const privateKey = getRequiredWalletPrivateKey();
    const walletAddress = (await deriveWalletAddress({ privateKey })).toLowerCase();
    const auth = await buildElementAuthorization(
      {
        getLoginNonce: graphql.getLoginNonce,
        loginAuth: graphql.loginAuth
      },
      {
        privateKey,
        walletAddress,
        chainMId
      }
    );
    return {
      authorization: auth.authorization,
      walletAddress,
      nonce: auth.nonce,
      loginMessage: auth.message,
      identity: auth.identity
    };
  }

  async function getWalletAddressFromEnv() {
    const privateKey = getRequiredWalletPrivateKey();
    return (await deriveWalletAddress({ privateKey })).toLowerCase();
  }

  async function buildCreateDropOnchainPreview(payload: {
    chainMId: number;
    name: string;
    symbol: string;
  }) {
    const auth = await createAuthorization(payload.chainMId);
    const encoded = await api.postCreateToken(
      auth.authorization,
      {
        chainMId: payload.chainMId,
        name: payload.name,
        symbol: payload.symbol
      },
      auth.walletAddress
    );

    return {
      walletAddress: auth.walletAddress,
      createToken: encoded.data
    };
  }

async function buildPublishDropOnchainPreview(payload: {
  authorization: string;
  walletAddress: string;
  chainMId: number;
  contractAddress: string;
  dropID: number;
  isPaused?: boolean;
  preRevealIPFSPollIntervalMs?: number;
  preRevealIPFSTimeoutMs?: number;
}) {
  const settingsResponse = await api.getDropSettings(
    {
      chainMId: payload.chainMId,
      contractAddress: payload.contractAddress
    },
    payload.walletAddress
  );
  const preRevealResolution = await resolvePublishPreRevealIPFS(
    {
      authorization: payload.authorization,
      chainMId: payload.chainMId,
      contractAddress: payload.contractAddress,
      dropID: payload.dropID,
      walletAddress: payload.walletAddress,
      pollIntervalMs: payload.preRevealIPFSPollIntervalMs,
      timeoutMs: payload.preRevealIPFSTimeoutMs
    },
    {
      getTempURL: api.getTempURL,
      getPreRevealIPFS: api.getPreRevealIPFS
    }
  );
  const postSettingsPayload = buildPostDropSettingsPayloadFromSettings({
    settings: settingsResponse.data,
    chainMId: payload.chainMId,
    contractAddress: payload.contractAddress
    });
  const setProjectConfigPayload = buildSetProjectConfigPayload({
    settings: settingsResponse.data,
    chainMId: payload.chainMId,
    contractAddress: payload.contractAddress,
    preRevealIPFS: preRevealResolution.preRevealIPFS.preRevealIPFS,
    isPaused: payload.isPaused
  });
  const encoded = await api.postSetProjectConfig(
    payload.authorization,
    setProjectConfigPayload,
      payload.walletAddress
    );

    return {
      walletAddress: payload.walletAddress,
      settings: settingsResponse.data,
      tempURL: preRevealResolution.tempURL,
      preRevealIPFS: preRevealResolution.preRevealIPFS,
      postSettingsPayload,
      setProjectConfigPayload,
      setProjectConfig: encoded.data
    };
}

  async function resolveContractAddressBySlug(input: {
    chainMId: number;
    slug?: string;
    contractAddress?: string;
  }) {
    if (!input.slug) {
      if (!input.contractAddress) {
        throw new Error("slug is required");
      }
      return {
        slug: undefined,
        contractAddress: input.contractAddress
      };
    }

    const collection = await graphql.getCollectionDetailFromEditors(input.slug);
    const expectedBlockChain = getElementIdentityByChainMId(input.chainMId, ZERO_ADDRESS).blockChain;
    const contract =
      collection.contracts.find(
        (item) =>
          item.blockChain.chain === expectedBlockChain.chain && item.blockChain.chainId === expectedBlockChain.chainId
      ) ?? null;

    if (!contract) {
      throw new Error(`No contract found for slug ${input.slug} on chain ${getElementChainNameByChainMId(input.chainMId)}`);
    }

    if (
      input.contractAddress &&
      input.contractAddress.toLowerCase() !== contract.address.toLowerCase()
    ) {
      throw new Error(
        `slug ${input.slug} resolved to contractAddress ${contract.address}, but payload provided ${input.contractAddress}`
      );
    }

    return {
      slug: collection.slug,
      contractAddress: contract.address
    };
  }

  async function resolveDropLocator<T extends Record<string, unknown>>(
    payload: T,
    input: {
      needDropID?: boolean;
      walletAddress?: string;
    } = {}
  ): Promise<T & { slug?: string; contractAddress: string; dropID?: number }> {
    const resolvedContract = await resolveContractAddressBySlug({
      chainMId: payload.chainMId as number,
      slug: typeof payload.slug === "string" ? payload.slug : undefined,
      contractAddress: typeof payload.contractAddress === "string" ? payload.contractAddress : undefined
    });

    let dropID =
      typeof payload.dropID === "number" && Number.isFinite(payload.dropID) ? payload.dropID : undefined;

    if (input.needDropID && dropID === undefined) {
      const walletAddress = input.walletAddress ?? (await getWalletAddressFromEnv());
      const settings = await api.getDropSettings(
        {
          chainMId: payload.chainMId as number,
          contractAddress: resolvedContract.contractAddress
        },
        walletAddress
      );
      dropID = settings.data.dropID;
      if (!(dropID > 0)) {
        throw new Error(`dropID is not available yet for slug ${resolvedContract.slug ?? payload.slug ?? ""}`.trim());
      }
    }

    return {
      ...payload,
      slug: resolvedContract.slug ?? (typeof payload.slug === "string" ? payload.slug : undefined),
      contractAddress: resolvedContract.contractAddress,
      ...(dropID !== undefined ? { dropID } : {})
    };
  }

  if (command === "preview") {
    const payload = await readJsonArg(filePath);
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  if (command === "list-chains") {
    const response = await api.getChainsWithGas();
    const chains = response.data.chains.map((chain) => ({
      chainName: (() => {
        try {
          return getElementChainNameByChainMId(chain.chainMId);
        } catch {
          return "unknown";
        }
      })(),
      currency: chain.currency,
      paymentTokens: chain.paymentTokens.map((token) => ({
        name: token.name,
        address: token.TokenAddress
      }))
    }));
    console.log(JSON.stringify({ chains }, null, 2));
    return;
  }

  if (command === "list-user-collections") {
    const payload = await resolvePayloadChain(await readJsonArg(filePath));
    const walletAddress = typeof payload.walletAddress === "string" && payload.walletAddress.length > 0
      ? payload.walletAddress.toLowerCase()
      : await getWalletAddressFromEnv();
    const identity = getElementIdentityByChainMId(payload.chainMId, walletAddress);
    const result = await graphql.getUserCollectionList({
      identity,
      first: typeof payload.first === "number" ? payload.first : undefined,
      after: typeof payload.after === "string" ? payload.after : undefined,
      before: typeof payload.before === "string" ? payload.before : undefined,
      last: typeof payload.last === "number" ? payload.last : undefined
    });
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            walletAddress,
            totalCollections: result.items.length
          },
          walletAddress,
          chainName: payload.chainName,
          collections: result.items.map((item) => ({
            slug: item.slug,
            name: item.name,
            isVerified: item.isVerified,
            imageUrl: item.imageUrl,
            assetCount: item.stats.assetCount
          })),
          pageInfo: result.pageInfo
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "list-user-drops") {
    const payload = await resolvePayloadChain(await readJsonArg(filePath));
    const walletAddress =
      typeof payload.walletAddress === "string" && payload.walletAddress.length > 0
        ? payload.walletAddress.toLowerCase()
        : await getWalletAddressFromEnv();
    const identity = getElementIdentityByChainMId(payload.chainMId, walletAddress);
    const result = await graphql.getUserCollectionList({
      identity,
      first: typeof payload.first === "number" ? payload.first : undefined,
      after: typeof payload.after === "string" ? payload.after : undefined,
      before: typeof payload.before === "string" ? payload.before : undefined,
      last: typeof payload.last === "number" ? payload.last : undefined
    });
    const drops = result.items
      .filter((item) => item.contracts.some((contract) => isElementDropCollection(contract.sourceType)))
      .map((item) => ({
        name: item.name,
        slug: item.slug,
        isVerified: item.isVerified,
        imageUrl: item.imageUrl,
        assetCount: item.stats.assetCount
      }));
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            walletAddress,
            totalDrops: drops.length
          },
          walletAddress,
          chainName: payload.chainName,
          drops,
          pageInfo: result.pageInfo
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "get-contract-by-slug") {
    const payload = await readJsonArg(filePath);
    const collection = await graphql.getCollectionDetailFromEditors(payload.slug);
    const contract = collection.contracts[0] ?? null;
    console.log(
      JSON.stringify(
        {
          summary: {
            slug: collection.slug,
            name: collection.name,
            contractAddress: contract?.address ?? null
          },
          slug: collection.slug,
          name: collection.name,
          contractAddress: contract?.address ?? null,
          blockChain: contract?.blockChain ?? null,
          sourceType: contract?.sourceType ?? null
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "create-token") {
    const payload = await resolvePayloadChain(await readJsonArg(filePath));
    setActiveOperationContext(command, payload);
    const result = await createTokenFlow(payload, {
      deriveAddress: deriveWalletAddress,
      resolveRpcUrl: getRpcUrlForChainMId,
      createAuthorization: (input) =>
        buildElementAuthorization(
          {
            getLoginNonce: graphql.getLoginNonce,
            loginAuth: graphql.loginAuth
          },
          input
        ),
      postCreateToken: api.postCreateToken,
      sendTransaction: sendEncodedTransaction
    });
    const output: Record<string, unknown> = { ...result };
    output.summary = {
      chainName: payload.chainName,
      symbol: payload.symbol,
      contractAddress: result.transaction.contractAddress ?? payload.contractAddress ?? null,
      transactionHash: result.transaction.hash
    };
    const contractAddress = result.transaction.contractAddress ?? payload.contractAddress;
    if (contractAddress) {
      output.postCreateCollection = await postCreateCollectionFlow(
        {
          chainMId: payload.chainMId,
          contractAddress,
          authorization: result.preflight.authorization,
          imageFilePath: payload.preReveal,
          pollIntervalMs: payload.pollIntervalMs,
          timeoutMs: payload.timeoutMs
        },
        {
          getCollectionContract: graphql.getCollectionContract,
          getMutateToken: graphql.getMutateToken,
          getCollectionDetailFromEditors: graphql.getCollectionDetailFromEditors,
          collectionEdit: graphql.collectionEdit
        }
      );
    }
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "create-drop") {
    const payload = await resolvePayloadChain(await readJsonArg(filePath));
    setActiveOperationContext(command, payload);
    if (dryRun) {
      const onchainPreview = await buildCreateDropOnchainPreview({
        chainMId: payload.chainMId,
        name: String(payload.name),
        symbol: String(payload.symbol)
      });
      console.log(JSON.stringify(buildCreateDropDryRunPreview(payload, { onchainPreview }), null, 2));
      return;
    }
    const result = await createDropFlow(payload, {
      createTokenFlow,
      postCreateCollectionFlow,
      uploadWithExistingAuthorization,
      getDropSettings: api.getDropSettings,
      postDropSettings: api.postDropSettings,
      getOssSignSingle: api.getOssSignSingle,
      postPreReveal: api.postPreReveal,
      postDesign: api.postDesign,
      uploadAsset: uploadSingleAsset,
      createAuthorization,
      deriveAddress: deriveWalletAddress,
      resolveRpcUrl: getRpcUrlForChainMId,
      createAuthorizationForToken: (input) =>
        buildElementAuthorization(
          {
            getLoginNonce: graphql.getLoginNonce,
            loginAuth: graphql.loginAuth
          },
          input
        ),
      postCreateToken: api.postCreateToken,
      sendTransaction: sendEncodedTransaction,
      getCollectionContract: graphql.getCollectionContract,
      getMutateToken: graphql.getMutateToken,
      getCollectionDetailFromEditors: graphql.getCollectionDetailFromEditors,
      collectionEdit: graphql.collectionEdit
    });
    console.log(
      JSON.stringify(
        {
          summary: result.summary,
          settings: summarizeSettingsSnapshot({
            maxSupply: result.initialSettingsPayload.maxSupply,
            dropBeginTime: result.initialSettingsPayload.dropBeginTime,
            dropType: result.initialSettingsPayload.dropType,
            mintingType: result.initialSettingsPayload.mintingType,
            stages: result.initialSettingsPayload.stagesUpdate,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
            currency: payload.currency
          }),
          design: summarizeDesignSnapshot(result.designUpload.payload),
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "configure-drop") {
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)));
    setActiveOperationContext(command, payload);
    if (dryRun) {
      const auth =
        payload.authorization && payload.walletAddress
          ? {
              authorization: payload.authorization,
              walletAddress: payload.walletAddress
            }
          : await createAuthorization(payload.chainMId);
      const preview = await previewConfigureDrop(
        {
          authorization: auth.authorization,
          walletAddress: auth.walletAddress,
          chainMId: payload.chainMId,
          contractAddress: payload.contractAddress,
          slug: payload.slug,
          patch: payload
        },
        {
          getDropSettings: api.getDropSettings,
          getDropDesign: api.getDropDesign,
          getMutateToken: graphql.getMutateToken,
          getCollectionDetailFromEditors: graphql.getCollectionDetailFromEditors
        }
      );
      console.log(JSON.stringify(preview, null, 2));
      return;
    }
    const auth =
      payload.authorization && payload.walletAddress
        ? {
            authorization: payload.authorization,
            walletAddress: payload.walletAddress
          }
        : await createAuthorization(payload.chainMId);
    const result = await configureDropFlow(
      {
        ...payload,
        authorization: auth.authorization,
        walletAddress: auth.walletAddress
      },
      {
        uploadWithExistingAuthorization,
        getDropSettings: api.getDropSettings,
        getDropDesign: api.getDropDesign,
        postDropSettings: api.postDropSettings,
        getOssSignSingle: api.getOssSignSingle,
        postPreReveal: api.postPreReveal,
        postDesign: api.postDesign,
        getMutateToken: graphql.getMutateToken,
        getCollectionDetailFromEditors: graphql.getCollectionDetailFromEditors,
        collectionEdit: graphql.collectionEdit,
        uploadAsset: uploadSingleAsset
      }
    );
    const displayDesignAfterConfigure = buildDisplayDesignAfterUpdate({
      current: result.currentDesignResponse?.data ?? null,
      designPayload: result.designPayload,
      collectionEditPayload: result.collectionEditPayload
    });
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: result.contractAddress,
            slug: result.slug,
            dropUrl: result.urls?.dropUrl ?? null,
            collectionUrl: result.urls?.collectionUrl ?? null,
            editUrl: result.urls?.editUrl ?? null,
            preRevealUrl: result.preRevealUpload?.publicUrls[0] ?? null,
            bannerUrl: result.designBannerUrl ?? null
          },
          settingsAfterUpdate: summarizeSettingsSnapshot({
            maxSupply: result.settingsAfterConfigure.data.maxSupply,
            totalMint: result.settingsAfterConfigure.data.totalMint,
            dropBeginTime: result.settingsAfterConfigure.data.dropBeginTime,
            dropType: result.settingsAfterConfigure.data.dropType,
            mintingType: result.settingsAfterConfigure.data.mintingType,
            stages: result.settingsAfterConfigure.data.stages,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : []
          }),
          ...(displayDesignAfterConfigure
            ? { designAfterUpdate: summarizeDesignSnapshot(displayDesignAfterConfigure) }
            : {}),
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "update-drop") {
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)));
    setActiveOperationContext(command, payload);
    if (dryRun) {
      const auth =
        payload.authorization && payload.walletAddress
          ? {
              authorization: payload.authorization,
              walletAddress: payload.walletAddress
            }
          : await createAuthorization(payload.chainMId);
      const preview = await previewConfigureDrop(
        {
          authorization: auth.authorization,
          walletAddress: auth.walletAddress,
          chainMId: payload.chainMId,
          contractAddress: payload.contractAddress,
          slug: payload.slug,
          patch: payload
        },
        {
          getDropSettings: api.getDropSettings,
          getDropDesign: api.getDropDesign,
          getMutateToken: graphql.getMutateToken,
          getCollectionDetailFromEditors: graphql.getCollectionDetailFromEditors
        }
      );
      const currentPaymentToken = summarizeResolvedPaymentToken({
        mintingType: preview.currentSettings.data?.mintingType,
        availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
        currency: payload.currency
      });
      const nextPaymentToken = summarizeResolvedPaymentToken({
        mintingType: preview.settingsPayload?.mintingType ?? preview.currentSettings.data?.mintingType,
        availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
        currency: payload.currency
      });
      const requiresRepublish = shouldRepublishUpdatedDrop({
        published: preview.currentSettings.data?.published,
        isPaused: preview.currentSettings.data?.isPaused,
        willUpdateSettings: preview.summary.willUpdateSettings,
        willUpdatePreReveal: preview.summary.willUpdatePreReveal
      });
      const republishPreview =
        requiresRepublish
          ? buildPublishDropDryRunPreview(payload, {
              onchainPreview: await buildPublishDropOnchainPreview({
                authorization: auth.authorization,
                walletAddress: auth.walletAddress,
                chainMId: payload.chainMId,
                contractAddress: payload.contractAddress,
                dropID: preview.summary.dropID,
                preRevealIPFSPollIntervalMs: payload.preRevealIPFSPollIntervalMs,
                preRevealIPFSTimeoutMs: payload.preRevealIPFSTimeoutMs
              })
            })
          : null;
      console.log(
        JSON.stringify(
          requiresRepublish
            ? {
                command: "update-drop",
                previewOnly: true,
                target: {
                  chainName: payload.chainName ?? null,
                  slug: payload.slug ?? null,
                  contractAddress: payload.contractAddress ?? null
                },
                current: {
                  publishState: summarizePublishState({
                    published: preview.currentSettings.data?.published,
                    isPaused: preview.currentSettings.data?.isPaused
                  }),
                  batch: preview.currentSettings.data?.batch ?? null,
                  settings: summarizeSettingsSnapshot({
                    maxSupply: preview.currentSettings.data?.maxSupply,
                    totalMint: preview.currentSettings.data?.totalMint,
                    dropBeginTime: preview.currentSettings.data?.dropBeginTime,
                    dropType: preview.currentSettings.data?.dropType,
                    mintingType: preview.currentSettings.data?.mintingType,
                    stages: preview.currentSettings.data?.stages,
                    availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
                    currency: payload.currency
                  }),
                  ...(preview.currentDesign?.data
                    ? { design: summarizeDesignSnapshot(preview.currentDesign.data) }
                    : {})
                },
                currentPaymentToken,
                nextPaymentToken,
                ...(preview.settingsPayload
                  ? { settingsPreview: summarizeSettingsSnapshot({
                      maxSupply: preview.settingsPayload.maxSupply,
                      dropBeginTime: preview.settingsPayload.dropBeginTime,
                      dropType: preview.settingsPayload.dropType,
                      mintingType: preview.settingsPayload.mintingType,
                      stages: preview.settingsPayload.stagesUpdate,
                      availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
                      currency: payload.currency
                    }) }
                  : {}),
                ...(preview.designPayload ? { designPreview: summarizeDesignSnapshot(preview.designPayload) } : {}),
                onchainRisk: {
                  hasBlockchainTransaction: true,
                  executionRequiresExplicitConfirmation: true,
                  note:
                    "This drop is already live, and the requested settings or prereveal update requires republish with an onchain transaction."
                },
                signingSafety: buildSigningSafetyNote(),
                republishReason:
                  "The current drop is live and this patch changes settings or prereveal, so update-drop will continue into publish flow.",
                ...(republishPreview ? { republishPreview } : {})
              }
            : {
                command: "update-drop",
                previewOnly: true,
                target: {
                  chainName: payload.chainName ?? null,
                  slug: payload.slug ?? null,
                  contractAddress: payload.contractAddress ?? null
                },
                current: {
                  publishState: summarizePublishState({
                    published: preview.currentSettings.data?.published,
                    isPaused: preview.currentSettings.data?.isPaused
                  }),
                  batch: preview.currentSettings.data?.batch ?? null,
                  settings: summarizeSettingsSnapshot({
                    maxSupply: preview.currentSettings.data?.maxSupply,
                    totalMint: preview.currentSettings.data?.totalMint,
                    dropBeginTime: preview.currentSettings.data?.dropBeginTime,
                    dropType: preview.currentSettings.data?.dropType,
                    mintingType: preview.currentSettings.data?.mintingType,
                    stages: preview.currentSettings.data?.stages,
                    availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
                    currency: payload.currency
                  }),
                  ...(preview.currentDesign?.data
                    ? { design: summarizeDesignSnapshot(preview.currentDesign.data) }
                    : {})
                },
                currentPaymentToken,
                nextPaymentToken,
                ...(preview.settingsPayload
                  ? { settingsPreview: summarizeSettingsSnapshot({
                      maxSupply: preview.settingsPayload.maxSupply,
                      dropBeginTime: preview.settingsPayload.dropBeginTime,
                      dropType: preview.settingsPayload.dropType,
                      mintingType: preview.settingsPayload.mintingType,
                      stages: preview.settingsPayload.stagesUpdate,
                      availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
                      currency: payload.currency
                    }) }
                  : {}),
                ...(preview.designPayload ? { designPreview: summarizeDesignSnapshot(preview.designPayload) } : {}),
                onchainRisk: {
                  hasBlockchainTransaction: false,
                  executionRequiresExplicitConfirmation: false,
                  note:
                    (preview.currentSettings.data?.published ?? 0) === 1
                      ? preview.currentSettings.data?.isPaused === true
                        ? "This drop is already paused, so update-drop applies the requested offchain changes without forcing republish."
                        : "This flow only changes design or collection profile fields, so it does not require republish or an onchain transaction."
                      : "This flow updates remote settings, prereveal, design, or collection profile fields and does not send an onchain transaction by itself."
                },
                signingSafety: buildSigningSafetyNote(),
                transactionPreview: []
              },
          null,
          2
        )
      );
      return;
    }
    const auth =
      payload.authorization && payload.walletAddress
        ? {
            authorization: payload.authorization,
            walletAddress: payload.walletAddress
          }
        : await createAuthorization(payload.chainMId);
    const result = await configureDropFlow(
      {
        ...payload,
        authorization: auth.authorization,
        walletAddress: auth.walletAddress
      },
      {
        uploadWithExistingAuthorization,
        getDropSettings: api.getDropSettings,
        getDropDesign: api.getDropDesign,
        postDropSettings: api.postDropSettings,
        getOssSignSingle: api.getOssSignSingle,
        postPreReveal: api.postPreReveal,
        postDesign: api.postDesign,
        getMutateToken: graphql.getMutateToken,
        getCollectionDetailFromEditors: graphql.getCollectionDetailFromEditors,
        collectionEdit: graphql.collectionEdit,
        uploadAsset: uploadSingleAsset
      }
    );
    const republishResult =
      shouldRepublishUpdatedDrop({
        published: result.currentSettings.published,
        isPaused: result.currentSettings.isPaused,
        willUpdateSettings: Boolean(result.settingsPayload),
        willUpdatePreReveal: Boolean(result.preRevealUpload)
      })
        ? await publishDropFlow(
            {
              authorization: auth.authorization,
              walletAddress: auth.walletAddress,
              rpcUrl: await getRpcUrlForChainMId(payload.chainMId),
              chainMId: payload.chainMId,
              contractAddress: result.contractAddress,
              dropID: result.dropID,
              getSettingsPollIntervalMs: payload.getSettingsPollIntervalMs,
              getSettingsTimeoutMs: payload.getSettingsTimeoutMs,
              preRevealIPFSPollIntervalMs: payload.preRevealIPFSPollIntervalMs,
              preRevealIPFSTimeoutMs: payload.preRevealIPFSTimeoutMs
            },
            {
              getDropSettings: api.getDropSettings,
              getPreRevealIPFS: api.getPreRevealIPFS,
              getTempURL: api.getTempURL,
              postDropSettings: api.postDropSettings,
              postSetProjectConfig: api.postSetProjectConfig,
              sendTransaction: sendEncodedTransaction,
              postCallbackUpdateProjectConfig: api.postCallbackUpdateProjectConfig
            }
          )
        : null;
    const displayDesignAfterUpdate = buildDisplayDesignAfterUpdate({
      current: result.currentDesignResponse?.data ?? null,
      designPayload: result.designPayload,
      collectionEditPayload: result.collectionEditPayload
    });
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: result.contractAddress,
            slug: result.slug,
            dropUrl: result.urls?.dropUrl ?? null,
            collectionUrl: result.urls?.collectionUrl ?? null,
            editUrl: result.urls?.editUrl ?? null,
            preRevealUrl: result.preRevealUpload?.publicUrls[0] ?? null,
            bannerUrl: result.designBannerUrl ?? null,
            republished: Boolean(republishResult),
            publishTransactionHash: republishResult?.setProjectConfigTransaction.hash ?? null
          },
          settingsAfterUpdate: summarizeSettingsSnapshot({
            maxSupply: result.settingsAfterConfigure.data.maxSupply,
            totalMint: result.settingsAfterConfigure.data.totalMint,
            dropBeginTime: result.settingsAfterConfigure.data.dropBeginTime,
            dropType: result.settingsAfterConfigure.data.dropType,
            mintingType: result.settingsAfterConfigure.data.mintingType,
            stages: result.settingsAfterConfigure.data.stages,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
            currency: payload.currency
          }),
          ...(displayDesignAfterUpdate ? { designAfterUpdate: summarizeDesignSnapshot(displayDesignAfterUpdate) } : {}),
          ...(republishResult
            ? { publishResult: {
                publishState: summarizePublishState({
                  published: republishResult.published.settings.published,
                  isPaused: republishResult.published.settings.isPaused
                }),
                publishTransactionHash: republishResult.setProjectConfigTransaction.hash,
                settings: summarizeSettingsSnapshot({
                  maxSupply: republishResult.published.settings.maxSupply,
                  totalMint: republishResult.published.settings.totalMint,
                  dropBeginTime: republishResult.published.settings.dropBeginTime,
                  dropType: republishResult.published.settings.dropType,
                  mintingType: republishResult.published.settings.mintingType,
                  stages: republishResult.published.settings.stages,
                  availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
                  currency: payload.currency
                })
              } }
            : {}),
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "preview-drop") {
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)));
    setActiveOperationContext(command, payload);
    const auth =
      payload.authorization && payload.walletAddress
        ? {
            authorization: payload.authorization,
            walletAddress: payload.walletAddress
          }
        : await createAuthorization(payload.chainMId);
    const result = await previewDropFlow(
      {
        authorization: auth.authorization,
        walletAddress: auth.walletAddress,
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        slug: payload.slug,
        page: payload.page,
        pageSize: payload.pageSize
      },
      {
        getDropSettings: api.getDropSettings,
        getDropDesign: api.getDropDesign,
        getTempURL: api.getTempURL
      }
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            ...result.summary,
            paymentToken: summarizeResolvedPaymentToken({
              mintingType: result.settings.data.mintingType,
              availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
              currency: payload.currency
            })
          },
          settings: summarizeSettingsSnapshot({
            maxSupply: result.settings.data.maxSupply,
            totalMint: result.settings.data.totalMint,
            dropBeginTime: result.settings.data.dropBeginTime,
            dropType: result.settings.data.dropType,
            mintingType: result.settings.data.mintingType,
            stages: result.settings.data.stages,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
            currency: payload.currency
          }),
          design: result.design ? summarizeDesignSnapshot(result.design.data) : null,
          preRevealMedia: result.tempURL
            ? {
                imageURL: extractPreRevealImageUrl(result.tempURL.data),
                animationURL: extractPreRevealAnimationUrl(result.tempURL.data)
              }
            : null
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "wait-collection-contract") {
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)));
    setActiveOperationContext(command, payload);
    const result = await waitForCollectionContract(
      {
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        pollIntervalMs: payload.pollIntervalMs,
        timeoutMs: payload.timeoutMs
      },
      {
        getCollectionContract: graphql.getCollectionContract
      }
    );
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === "post-create-collection") {
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)));
    setActiveOperationContext(command, payload);
    const authorization =
      payload.authorization ??
      (
        await createAuthorization(payload.chainMId)
      ).authorization;
    const result = await postCreateCollectionFlow(
      {
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        authorization,
        imageFilePath: payload.imageFilePath ?? payload.preReveal,
        pollIntervalMs: payload.pollIntervalMs,
        timeoutMs: payload.timeoutMs
      },
      {
        getCollectionContract: graphql.getCollectionContract,
        getMutateToken: graphql.getMutateToken,
        getCollectionDetailFromEditors: graphql.getCollectionDetailFromEditors,
        collectionEdit: graphql.collectionEdit
      }
    );
    console.log(JSON.stringify({ authorization, ...result }, null, 2));
    return;
  }

  if (command === "wait-prereveal-ipfs") {
    const walletAddress = await getWalletAddressFromEnv();
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)), {
      needDropID: true,
      walletAddress
    });
    setActiveOperationContext(command, payload);
    const result = await waitForPreRevealIPFS(
      {
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        dropID: payload.dropID,
        walletAddress,
        pollIntervalMs: payload.pollIntervalMs,
        timeoutMs: payload.timeoutMs
      },
      {
        getPreRevealIPFS: api.getPreRevealIPFS
      }
    );
    console.log(JSON.stringify({ walletAddress, ...result }, null, 2));
    return;
  }

  if (command === "wait-published-settings") {
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)), {
      needDropID: true
    });
    setActiveOperationContext(command, payload);
    const walletAddress = await getWalletAddressFromEnv();
    const result = await waitForPublishedSettings(
      {
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        dropID: payload.dropID,
        walletAddress,
        expectedPublished: typeof payload.expectedPublished === "number" ? payload.expectedPublished : undefined,
        pollIntervalMs: payload.pollIntervalMs,
        timeoutMs: payload.timeoutMs
      },
      {
        postCallbackUpdateProjectConfig: api.postCallbackUpdateProjectConfig,
        getDropSettings: api.getDropSettings
      }
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            walletAddress
          },
          walletAddress,
          publishState: summarizePublishState({
            published: result.settings.published,
            isPaused: result.settings.isPaused
          }),
          settings: summarizeSettingsSnapshot({
            maxSupply: result.settings.maxSupply,
            totalMint: result.settings.totalMint,
            dropBeginTime: result.settings.dropBeginTime,
            dropType: result.settings.dropType,
            mintingType: result.settings.mintingType,
            stages: result.settings.stages,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
            currency: payload.currency
          }),
          callbackResponse: result.callbackResponse,
          attempts: result.attempts,
          elapsedMs: result.elapsedMs
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "publish-drop") {
    const rawPayload = await readJsonArg(filePath);
    const resolvedChainPayload = await resolvePayloadChain(rawPayload);
    const auth = await createAuthorization(resolvedChainPayload.chainMId);
    const payload = await resolveDropLocator(resolvedChainPayload, {
      needDropID: true,
      walletAddress: auth.walletAddress
    });
    setActiveOperationContext(command, payload);
    if (dryRun) {
      const onchainPreview = await buildPublishDropOnchainPreview({
        authorization: auth.authorization,
        walletAddress: auth.walletAddress,
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        dropID: payload.dropID,
        isPaused: typeof payload.isPaused === "boolean" ? payload.isPaused : undefined,
        preRevealIPFSPollIntervalMs: payload.preRevealIPFSPollIntervalMs,
        preRevealIPFSTimeoutMs: payload.preRevealIPFSTimeoutMs
      });
      console.log(JSON.stringify(buildPublishDropDryRunPreview(payload, { onchainPreview }), null, 2));
      return;
    }
    const result = await publishDropFlow(
      {
        authorization: auth.authorization,
        walletAddress: auth.walletAddress,
        rpcUrl: await getRpcUrlForChainMId(payload.chainMId),
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        dropID: payload.dropID,
        isPaused: typeof payload.isPaused === "boolean" ? payload.isPaused : undefined,
        getSettingsPollIntervalMs: payload.getSettingsPollIntervalMs,
        getSettingsTimeoutMs: payload.getSettingsTimeoutMs,
        preRevealIPFSPollIntervalMs: payload.preRevealIPFSPollIntervalMs,
        preRevealIPFSTimeoutMs: payload.preRevealIPFSTimeoutMs
      },
      {
        getDropSettings: api.getDropSettings,
        getPreRevealIPFS: api.getPreRevealIPFS,
        getTempURL: api.getTempURL,
        postDropSettings: api.postDropSettings,
        postSetProjectConfig: api.postSetProjectConfig,
        sendTransaction: sendEncodedTransaction,
        postCallbackUpdateProjectConfig: api.postCallbackUpdateProjectConfig
      }
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            slug: payload.slug ?? null,
            dropUrl: payload.slug ? `https://element.market/collections/${payload.slug}` : null,
            collectionUrl: payload.slug ? `https://element.market/collections/${payload.slug}` : null,
            editUrl: payload.slug ? `https://element.market/collections/${payload.slug}/edit/drop` : null,
            publishState: summarizePublishState({
              published: result.published.settings.published,
              isPaused: result.published.settings.isPaused
            }),
            publishTransactionHash: result.setProjectConfigTransaction.hash,
            callbackSucceeded: result.published.callbackResponse.code === 0
          },
          settingsAfterPublish: summarizeSettingsSnapshot({
            maxSupply: result.published.settings.maxSupply,
            totalMint: result.published.settings.totalMint,
            dropBeginTime: result.published.settings.dropBeginTime,
            dropType: result.published.settings.dropType,
            mintingType: result.published.settings.mintingType,
            stages: result.published.settings.stages,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
            currency: payload.currency
          }),
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "get-settings") {
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)));
    setActiveOperationContext(command, payload);
    const walletAddress = await getWalletAddressFromEnv();
    const result = await api.getDropSettings(
      {
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress
      },
      walletAddress
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            walletAddress
          },
          settings: summarizeSettingsSnapshot({
            maxSupply: result.data.maxSupply,
            totalMint: result.data.totalMint,
            dropBeginTime: result.data.dropBeginTime,
            dropType: result.data.dropType,
            mintingType: result.data.mintingType,
            stages: result.data.stages,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
            currency: payload.currency
          })
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "post-settings") {
    const rawPayload = await readJsonArg(filePath);
    const resolvedChainPayload = await resolvePayloadChain(rawPayload);
    const auth = await createAuthorization(resolvedChainPayload.chainMId);
    const payload = await resolveDropLocator(resolvedChainPayload, {
      needDropID: true,
      walletAddress: auth.walletAddress
    });
    setActiveOperationContext(command, payload);
    const settingsPayload = {
      dropID: payload.dropID ?? 0,
      chainMId: payload.chainMId,
      contractAddress: payload.contractAddress,
      dropType: payload.dropType,
      maxSupply: payload.maxSupply,
      fee: payload.fee ?? 0,
      feeRecipient: payload.feeRecipient ?? "",
      mintingType: payload.mintingType ?? 0,
      dropBeginTime: payload.dropBeginTime,
      stagesUpdate: payload.stagesUpdate ?? []
    };
    const result = await api.postDropSettings(
      auth.authorization,
      settingsPayload,
      auth.walletAddress
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            walletAddress: auth.walletAddress,
            success: result.code === 0
          },
          requestedSettings: summarizeSettingsSnapshot({
            maxSupply: settingsPayload.maxSupply,
            dropBeginTime: settingsPayload.dropBeginTime,
            dropType: settingsPayload.dropType,
            mintingType: settingsPayload.mintingType,
            stages: settingsPayload.stagesUpdate,
            availablePaymentTokens: Array.isArray(payload.paymentTokens) ? payload.paymentTokens : [],
            currency: payload.currency
          }),
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "get-design") {
    const walletAddress = await getWalletAddressFromEnv();
    const payload = await resolveDropLocator(await resolvePayloadChain(await readJsonArg(filePath)), {
      needDropID: true,
      walletAddress
    });
    setActiveOperationContext(command, payload);
    const result = await api.getDropDesign(
      {
        dropID: payload.dropID,
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress
      },
      walletAddress
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            walletAddress,
            hasDesign: Boolean(result.data)
          },
          design: summarizeDesignSnapshot(result.data)
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "post-design") {
    const rawPayload = await readJsonArg(filePath);
    const resolvedChainPayload = await resolvePayloadChain(rawPayload);
    const auth = await createAuthorization(resolvedChainPayload.chainMId);
    const payload = await resolveDropLocator(resolvedChainPayload, {
      needDropID: true,
      walletAddress: auth.walletAddress
    });
    setActiveOperationContext(command, payload);
    const designPayload = {
      dropID: payload.dropID,
      chainMId: payload.chainMId,
      contractAddress: payload.contractAddress,
      dropName: payload.dropName ?? "",
      bannerURL: payload.bannerURL ?? "",
      previewMediaExt: payload.previewMediaExt ?? [],
      dropFeaturedImage: payload.dropFeaturedImage ?? "",
      description: payload.description ?? "",
      website: payload.website ?? "",
      twitter: payload.twitter ?? "",
      instagram: payload.instagram ?? "",
      discord: payload.discord ?? "",
      telegram: payload.telegram ?? "",
      medium: payload.medium ?? "",
      detailsUpdate: []
    };
    const result = await api.postDesign(
      auth.authorization,
      designPayload,
      auth.walletAddress
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            walletAddress: auth.walletAddress,
            success: result.code === 0
          },
          requestedDesign: summarizeDesignSnapshot(designPayload),
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "upload-prereveal") {
    const rawPayload = await readJsonArg(filePath);
    const resolvedChainPayload = await resolvePayloadChain(rawPayload);
    const auth = await createAuthorization(resolvedChainPayload.chainMId);
    const payload = await resolveDropLocator(resolvedChainPayload);
    setActiveOperationContext(command, payload);
    const result = await uploadWithExistingAuthorization(
      {
        authorization: auth.authorization,
        walletAddress: auth.walletAddress
      },
      {
        mode: "prereveal",
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        dropType: payload.dropType,
        filePath: payload.filePath
      },
      {
        getOssSignSingle: api.getOssSignSingle,
        postPreReveal: api.postPreReveal,
        uploadAsset: uploadSingleAsset
      }
    );
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            walletAddress: auth.walletAddress,
            uploaded: true,
            publicUrl: result.publicUrls[0] ?? null
          },
          upload: {
            sourcePath: result.uploads[0]?.sourcePath ?? null,
            fileName: result.uploads[0]?.fileName ?? null,
            objectKey: result.uploads[0]?.objectKey ?? null,
            publicUrls: result.publicUrls
          },
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "upload-design") {
    const rawPayload = await readJsonArg(filePath);
    const resolvedChainPayload = await resolvePayloadChain(rawPayload);
    const auth = await createAuthorization(resolvedChainPayload.chainMId);
    const payload = await resolveDropLocator(resolvedChainPayload, {
      needDropID: true,
      walletAddress: auth.walletAddress
    });
    setActiveOperationContext(command, payload);
    const result = await uploadWithExistingAuthorization(
      {
        authorization: auth.authorization,
        walletAddress: auth.walletAddress
      },
      {
        mode: "design",
        chainMId: payload.chainMId,
        contractAddress: payload.contractAddress,
        dropID: payload.dropID,
        dropName: payload.dropName,
        bannerFilePath: payload.bannerFilePath,
        previewFilePaths: payload.previewFilePaths
      },
      {
        getOssSignSingle: api.getOssSignSingle,
        postPreReveal: api.postPreReveal,
        uploadAsset: uploadSingleAsset
      }
    );
    if (result.mode !== "design") {
      throw new Error("upload-design expected design upload result");
    }
    const designResult = result;
    console.log(
      JSON.stringify(
        {
          summary: {
            chainName: payload.chainName,
            contractAddress: payload.contractAddress,
            walletAddress: auth.walletAddress,
            uploadedBanner: Boolean(designResult.payload.bannerURL),
            previewMediaCount: designResult.payload.previewMediaExt.length
          },
          designUpload: {
            bannerUrl: designResult.payload.bannerURL || null,
            previewUrls: designResult.payload.previewMediaExt
              .map((item) => item.image_url ?? "")
              .filter(Boolean),
            requestedDesign: summarizeDesignSnapshot(designResult.payload)
          },
          signingSafety: buildSigningSafetyNote()
        },
        null,
        2
      )
    );
    return;
  }

  if (command === "verify-ref-graphql") {
    const result = await verifyRefGraphqlExamples();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  throw new Error(`unknown command: ${command}`);
}

main().catch((error: unknown) => {
  const message = redactKnownSecrets(error instanceof Error ? error.message : String(error));
  console.error(
    JSON.stringify(
      {
        error: message,
        operationContext: activeOperationContext,
        chainName: activeOperationContext.chainName ?? null,
        symbol: activeOperationContext.symbol ?? null,
        note:
          "Verify chainName before retrying. A drop deployed on the wrong chain cannot be moved; create a new drop on the intended chain instead."
      },
      null,
      2
    )
  );
  process.exitCode = 1;
});
