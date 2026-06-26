export type TierAmount = 10 | 25 | 50 | 100 | 200 | 500;

export interface CreationTier {
  loadAmount: TierAmount;
  issuanceFee: number;
  topUpFee: number;
  serviceFee: number;
  totalCost: number;
  endpoint: string;
}

export interface FundingTier {
  fundAmount: TierAmount;
  topUpFee: number;
  serviceFee: number;
  totalCost: number;
  endpoint: string;
}

export interface CardBillingAddress {
  street: string;
  city: string;
  state: string;
  zip: string;
  country: string;
}

export interface CardDetails {
  cardNumber: string;
  expiryMonth: number;
  expiryYear: number;
  cvv: string;
  maskedCardNumber?: string;
  billingAddress: CardBillingAddress;
}

export interface StoredCard {
  cardId: string;
  walletAddress: string;
  nameOnCard: string;
  email: string;
  balance: number;
  initialAmountUsd: number;
  status: "active" | "frozen";
  createdAt: string;
  updatedAt: string;
  details: CardDetails;
  fourPaymentsId?: string;
}
