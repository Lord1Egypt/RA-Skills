import type { CreationTier, FundingTier, TierAmount } from "../types/domain";

export const SUPPORTED_TIERS: TierAmount[] = [10, 25, 50, 100, 200, 500];

export const CREATION_TIERS: CreationTier[] = [
  {
    loadAmount: 10,
    issuanceFee: 3.0,
    topUpFee: 2.2,
    serviceFee: 2.0,
    totalCost: 17.2,
    endpoint: "/cards/create/tier/10"
  },
  {
    loadAmount: 25,
    issuanceFee: 3.0,
    topUpFee: 2.5,
    serviceFee: 2.0,
    totalCost: 32.5,
    endpoint: "/cards/create/tier/25"
  },
  {
    loadAmount: 50,
    issuanceFee: 3.0,
    topUpFee: 3.0,
    serviceFee: 2.0,
    totalCost: 58.0,
    endpoint: "/cards/create/tier/50"
  },
  {
    loadAmount: 100,
    issuanceFee: 3.0,
    topUpFee: 4.0,
    serviceFee: 3.0,
    totalCost: 110.0,
    endpoint: "/cards/create/tier/100"
  },
  {
    loadAmount: 200,
    issuanceFee: 3.0,
    topUpFee: 6.0,
    serviceFee: 5.0,
    totalCost: 214.0,
    endpoint: "/cards/create/tier/200"
  },
  {
    loadAmount: 500,
    issuanceFee: 3.0,
    topUpFee: 12.0,
    serviceFee: 7.0,
    totalCost: 522.0,
    endpoint: "/cards/create/tier/500"
  }
];

export const FUNDING_TIERS: FundingTier[] = [
  {
    fundAmount: 10,
    topUpFee: 2.2,
    serviceFee: 2.0,
    totalCost: 14.2,
    endpoint: "/cards/fund/tier/10"
  },
  {
    fundAmount: 25,
    topUpFee: 2.5,
    serviceFee: 2.0,
    totalCost: 29.5,
    endpoint: "/cards/fund/tier/25"
  },
  {
    fundAmount: 50,
    topUpFee: 3.0,
    serviceFee: 2.0,
    totalCost: 55.0,
    endpoint: "/cards/fund/tier/50"
  },
  {
    fundAmount: 100,
    topUpFee: 4.0,
    serviceFee: 3.0,
    totalCost: 107.0,
    endpoint: "/cards/fund/tier/100"
  },
  {
    fundAmount: 200,
    topUpFee: 6.0,
    serviceFee: 5.0,
    totalCost: 211.0,
    endpoint: "/cards/fund/tier/200"
  },
  {
    fundAmount: 500,
    topUpFee: 12.0,
    serviceFee: 7.0,
    totalCost: 519.0,
    endpoint: "/cards/fund/tier/500"
  }
];

/**
 * Convert USD to Stellar USDC atomic units (7 decimal places).
 * Stellar uses 7 decimals for all assets (including USDC).
 * $1.00 = 10_000_000 atomic | $17.20 = 172_000_000 atomic
 */
export const toAtomicUsdc = (usd: number): string =>
  Math.round(usd * 10_000_000).toString();

export const findCreationTier = (amount: number): CreationTier | undefined =>
  CREATION_TIERS.find((tier) => tier.loadAmount === amount);

export const findFundingTier = (amount: number): FundingTier | undefined =>
  FUNDING_TIERS.find((tier) => tier.fundAmount === amount);
