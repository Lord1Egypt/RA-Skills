/**
 * 4payments.io API Client
 *
 * HTTP wrapper for all 4payments prepaid card API endpoints.
 * Base URL: https://business.4payments.io
 * Auth: Bearer token from Dashboard → Develop
 *
 * Docs: https://docs.4payments.io/
 */

interface FourPaymentsConfig {
  baseUrl: string;
  apiToken: string;
  cardTypeId: string;
  cardholderId?: string;
}

// ── Response types ────────────────────────────────────────

interface FPCardIssued {
  id: string;
  cardNumber: string;
  cardExpire: string;
  cardCVC: string;
  cardBalance: number;
  currency: string;
  maskedCardNumber: string;
  brand: string;
  label: string;
  status: string;
  externalCardId: string;
}

interface FPCardDetails {
  id: string;
  maskedCardNumber: string;
  currency: string;
  status: string;
  externalCardId: string;
  balance: {
    value: number;
    currency: string;
  };
}

interface FPSensitiveInfo {
  number: string;
  expire: string;
  cvc: string;
}

interface FPTopUpResult {
  transactionId: string;
}

interface FPCardType {
  id: string;
  price: number;
  currency: string;
  brand: string;
  minInitialAmount: number;
  bins: string[];
  country: string;
  tokenization: string[];
  canReissue: boolean;
  comissions: {
    topupFee: string;
    withdrawFee: string;
    fxFee: string;
    transactionFee: number;
    declineFee: number;
    refundFee: number;
  };
  actions: string[];
  isCustom: boolean;
  recommended: string;
}

interface FPAccountBalance {
  balance: number;
  currency: string;
}

// ── Error ──────────────────────────────────────────────────

export class FourPaymentsError extends Error {
  readonly statusCode: number;
  readonly responseBody: unknown;

  constructor(message: string, statusCode: number, responseBody: unknown) {
    super(message);
    this.name = "FourPaymentsError";
    this.statusCode = statusCode;
    this.responseBody = responseBody;
  }
}

// ── Client ─────────────────────────────────────────────────

class FourPaymentsClient {
  private readonly baseUrl: string;
  private readonly apiToken: string;
  readonly cardTypeId: string;
  readonly cardholderId?: string;

  constructor(config: FourPaymentsConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, "");
    this.apiToken = config.apiToken;
    this.cardTypeId = config.cardTypeId;
    this.cardholderId = config.cardholderId;
  }

  // ── Internal fetch ───────────────────────────────────────

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.apiToken}`,
      "Content-Type": "application/json",
    };

    const res = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    const responseBody = await res.json().catch(() => ({}));

    if (!res.ok) {
      throw new FourPaymentsError(
        `4payments API error: ${res.status} ${res.statusText} — ${JSON.stringify(responseBody)}`,
        res.status,
        responseBody
      );
    }

    return responseBody as T;
  }

  // ── Card Issuing ─────────────────────────────────────────

  /**
   * Issue a new prepaid card.
   * POST /external/api/prepaid-cards/issue
   */
  async issueCard(params: {
    externalId: string;
    firstName?: string;
    lastName?: string;
    email?: string;
    phone?: string;
    label?: string;
    initialBalance?: number;
  }): Promise<FPCardIssued> {
    const body: Record<string, unknown> = {
      typeId: this.cardTypeId,
      externalId: params.externalId,
    };

    if (this.cardholderId) {
      body.cardholderId = this.cardholderId;
    }

    if (params.firstName) body.firstName = params.firstName;
    if (params.lastName) body.lastName = params.lastName;
    if (params.email) body.email = params.email;
    if (params.phone) body.phone = params.phone;
    if (params.label) body.label = params.label;

    // Note: initialBalance may or may not be supported depending on the card type
    if (params.initialBalance !== undefined) {
      body.initialBalance = params.initialBalance;
    }

    const res = await this.request<{ status: string; data: { card: FPCardIssued } }>(
      "POST",
      "/external/api/prepaid-cards/issue",
      body
    );

    return res.data.card;
  }

  // ── Card Details ─────────────────────────────────────────

  /**
   * Get card metadata (balance, status, masked number).
   * GET /external/api/prepaid-cards/cards/{id}
   */
  async getCardDetails(
    fourPaymentsId: string,
    isExternal = false
  ): Promise<FPCardDetails> {
    const qs = isExternal ? "?is_external=1" : "";
    const res = await this.request<{ status: string; data: FPCardDetails }>(
      "GET",
      `/external/api/prepaid-cards/${fourPaymentsId}${qs}`
    );
    return res.data;
  }

  // ── Sensitive Info ───────────────────────────────────────

  /**
   * Get PCI-sensitive card details (full number, expiry, CVV).
   * GET /external/api/prepaid-cards/cards/{id}/sensetive
   * Note: "sensetive" is the actual path in the API (misspelled)
   */
  async getSensitiveInfo(
    fourPaymentsId: string,
    isExternal = false
  ): Promise<FPSensitiveInfo> {
    const qs = isExternal ? "?is_external=1" : "";
    const res = await this.request<{ status: string; data: FPSensitiveInfo }>(
      "GET",
      `/external/api/prepaid-cards/${fourPaymentsId}/sensetive${qs}`
    );
    return res.data;
  }

  // ── Top Up ───────────────────────────────────────────────

  /**
   * Add funds to a card.
   * POST /external/api/prepaid-cards/cards/{id}/topup
   */
  async topUpCard(
    fourPaymentsId: string,
    amount: number,
    externalId?: string
  ): Promise<FPTopUpResult> {
    const body: Record<string, unknown> = { amount };
    if (externalId) body.externalId = externalId;

    const res = await this.request<{ status: string; transactionId: string }>(
      "POST",
      `/external/api/prepaid-cards/${fourPaymentsId}/topup`,
      body
    );

    return { transactionId: res.transactionId };
  }

  // ── Freeze / Unfreeze ────────────────────────────────────

  /**
   * Freeze a card.
   * POST /external/api/prepaid-cards/cards/{id}/freeze
   */
  async freezeCard(fourPaymentsId: string): Promise<void> {
    await this.request(
      "POST",
      `/external/api/prepaid-cards/${fourPaymentsId}/freeze`
    );
  }

  /**
   * Unfreeze a card.
   * POST /external/api/prepaid-cards/cards/{id}/unfreeze
   */
  async unfreezeCard(fourPaymentsId: string): Promise<void> {
    await this.request(
      "POST",
      `/external/api/prepaid-cards/${fourPaymentsId}/unfreeze`
    );
  }

  // ── List types & cards ───────────────────────────────────

  /**
   * Get available card types.
   * GET /external/api/prepaid-cards/types
   */
  async listCardTypes(): Promise<FPCardType[]> {
    const res = await this.request<{ status: string; data: FPCardType[] }>(
      "GET",
      "/external/api/prepaid-cards/types"
    );
    return res.data;
  }

  /**
   * Get account balance.
   * GET /external/api/account/balance
   */
  async getAccountBalance(): Promise<FPAccountBalance> {
    const res = await this.request<{ status: string; data: FPAccountBalance }>(
      "GET",
      "/external/api/account/balance"
    );
    return res.data;
  }
}

// ── Singleton ──────────────────────────────────────────────

let _client: FourPaymentsClient | null = null;

export function getFourPaymentsClient(): FourPaymentsClient {
  if (_client) return _client;

  const apiToken = process.env.FOURPAYMENTS_API_TOKEN;
  if (!apiToken) {
    throw new Error("FOURPAYMENTS_API_TOKEN env var is required");
  }

  const cardTypeId = process.env.FOURPAYMENTS_CARD_TYPE_ID;
  if (!cardTypeId) {
    throw new Error("FOURPAYMENTS_CARD_TYPE_ID env var is required");
  }

  _client = new FourPaymentsClient({
    baseUrl: process.env.FOURPAYMENTS_BASE_URL || "https://business.4payments.io",
    apiToken,
    cardTypeId,
    cardholderId: process.env.FOURPAYMENTS_CARDHOLDER_ID,
  });

  return _client;
}

export type { FPCardIssued, FPCardDetails, FPSensitiveInfo, FPTopUpResult, FPCardType, FPAccountBalance };
