import { z } from "zod";
import type { CreateDropInput, CreateStageInput, DropInput, StageInput } from "./types";
import { DEFAULT_MAX_SUPPLY, resolveDropMode } from "./drop-mode";
const DEFAULT_STAGE_DURATION_SECONDS = 3 * 24 * 60 * 60;
const DEFAULT_STAGE_NAME = "Public";
const DEFAULT_STAGE_PRICE = "0";
const DEFAULT_STAGE_INTERVAL = 0;
const DEFAULT_STAGE_MAX_MINTED_PER_WALLET = 1;
const DEFAULT_STAGE_ID = 256;

const stageSchema = z.object({
  stageID: z.number().int().nonnegative(),
  stageName: z.string().min(1),
  price: z.string().min(1),
  duration: z.number().int().positive(),
  maxSupplyAtThisStage: z.number().int().positive(),
  maxMintedPerWallet: z.number().int().positive(),
  interval: z.number().int().nonnegative(),
  stageMode: z.union([z.literal(0), z.literal(1)])
});

const createStageSchema = z.object({
  stageID: z.number().int().nonnegative().optional(),
  stageName: z.string().min(1),
  price: z.string().min(1),
  duration: z.number().int().positive(),
  maxSupplyAtThisStage: z.number().int().positive(),
  maxMintedPerWallet: z.number().int().positive(),
  interval: z.number().int().nonnegative(),
  stageMode: z.union([z.literal(0), z.literal(1)])
});

const createDropInputSchema = z.object({
  chainMId: z.number().int().positive(),
  name: z.string().min(1),
  symbol: z.string().min(1),
  paymentToken: z.string().min(1).optional(),
  preReveal: z.string().min(1).optional(),
  previewMedia: z.array(z.string().min(1)).optional(),
  description: z.string().optional(),
  desc: z.string().optional(),
  website: z.string().optional(),
  twitter: z.string().optional(),
  instagram: z.string().optional(),
  discord: z.string().optional(),
  telegram: z.string().optional(),
  medium: z.string().optional(),
  dropFeaturedImage: z.string().optional(),
  edition: z.union([z.literal("limited"), z.literal("open")]).optional(),
  dropType: z.union([z.literal(0), z.literal(1)]).optional(),
  maxSupply: z.number().int().positive().optional(),
  dropBeginTime: z.number().int().positive().optional(),
  stages: z.array(createStageSchema).min(1).optional()
}).superRefine((input, ctx) => {
  if (!input.preReveal) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "preReveal is required",
      path: ["preReveal"]
    });
  }
});

export const dropInputSchema = z
  .object({
    chainMId: z.number().int().positive(),
    name: z.string().min(1),
    symbol: z.string().min(1),
    paymentToken: z.string().min(1).optional(),
    preReveal: z.string().min(1),
    description: z.string(),
    dropType: z.union([z.literal(0), z.literal(1)]),
    maxSupply: z.number().int().positive(),
    dropBeginTime: z.number().int().positive(),
    stages: z.array(stageSchema).min(1)
  })
  .superRefine((input, ctx) => {
    const stageSupply = input.stages.reduce((sum, stage) => sum + stage.maxSupplyAtThisStage, 0);
    if (stageSupply > input.maxSupply) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "stages total maxSupply exceeds drop maxSupply"
      });
    }
  });

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

export function normalizeCreateDropInput(input: CreateDropInput): DropInput {
  const parsed = createDropInputSchema.parse(input);
  const { dropType, maxSupply } = resolveDropMode({
    requestedEdition: parsed.edition,
    requestedDropType: parsed.dropType,
    requestedMaxSupply: parsed.maxSupply,
    fallbackMaxSupply: DEFAULT_MAX_SUPPLY
  });

  const normalized: DropInput = {
    chainMId: parsed.chainMId,
    name: parsed.name,
    symbol: parsed.symbol,
    paymentToken: parsed.paymentToken,
    preReveal: parsed.preReveal ?? "",
    description: parsed.description ?? parsed.desc ?? "",
    dropType,
    maxSupply,
    dropBeginTime: parsed.dropBeginTime ?? defaultDropBeginTime(),
    stages: parsed.stages ? assignStageIds(parsed.stages) : [buildDefaultStage(maxSupply)]
  };

  return dropInputSchema.parse(normalized);
}

export type DropInputSchema = z.infer<typeof dropInputSchema>;
