/**
 * x402 v2 Protocol Types
 * Source: OpenZeppelin relayer-plugin-x402-facilitator/src/types.ts
 */

// ── Payment Requirements ──────────────────────────────────
export interface PaymentRequirements {
    scheme: "exact";
    network: string;
    amount: string;          // integer string (atomic units, 7 decimals for Stellar)
    payTo: string;           // account address
    maxTimeoutSeconds: number;
    asset: string;           // asset identifier
    extra: {
        areFeesSponsored: boolean;
        [key: string]: unknown;
    };
}

// ── Payment Required (402 response) ───────────────────────
export interface PaymentRequired {
    x402Version: 2;
    error?: string;
    resource: {
        url: string;
        description: string;
        website?: string;
        mimeType: string;
    };
    accepts: PaymentRequirements[];
}

// ── Stellar v2 Payload ────────────────────────────────────
export interface ExactStellarPayloadV2 {
    transaction: string;  // base64 Stellar transaction XDR
}

// ── Payment Payload (client → server) ─────────────────────
export interface PaymentPayload {
    x402Version: 2;
    accepted: PaymentRequirements;
    payload: ExactStellarPayloadV2;
}

// ── Facilitator Requests ──────────────────────────────────
export interface VerifyRequest {
    paymentPayload: PaymentPayload;
    paymentRequirements: PaymentRequirements;
}

export interface SettleRequest {
    paymentPayload: PaymentPayload;
    paymentRequirements: PaymentRequirements;
}

// ── Facilitator Responses ─────────────────────────────────
export interface VerifyResponse {
    isValid: boolean;
    invalidReason?: string;
    payer?: string;
}

export interface SettleResponse {
    success: boolean;
    errorReason?: string;
    payer?: string;
    transaction: string;  // tx hash — source of truth for DB
    network: string;
}

// ── Supported ─────────────────────────────────────────────
export interface SupportedPaymentKind {
    x402Version: 2;
    scheme: "exact";
    network: string;
    extra?: Record<string, unknown>;
}
