import { facilitatorClient, FacilitatorError } from "./facilitatorClient";
import { emitMetric } from "./metrics";
import type { PaymentPayload, PaymentRequirements, SettleResponse } from "../types/x402";
import type { TierAmount } from "../types/domain";
import type { PaymentRepository } from "../repositories/types";
import { paymentRepository } from "../repositories/runtime";

// ── Payment verification result ────────────────────────────

export interface PaymentVerifyResult {
    valid: boolean;
    settleResponse?: SettleResponse;
    error?: string;
}

export interface VerifyPaymentInput {
    paymentPayload: PaymentPayload;
    paymentRequirements: PaymentRequirements;
    payer: string;
    tierAmount: TierAmount;
}

// ── PaymentService (x402 v2) ───────────────────────────────

export class PaymentService {
    private readonly paymentRepo: PaymentRepository;

    constructor(repo: PaymentRepository = paymentRepository) {
        this.paymentRepo = repo;
    }

    /**
     * x402 v2 flow:
     * 1. POST /verify — facilitator checks signed XDR
     * 2. If valid → POST /settle — facilitator submits tx to Stellar
     * 3. settle returns { transaction } — the on-chain tx hash (source of truth)
     * 4. Record in DB with txHash from settle response
     *
     * FAIL-CLOSED: if facilitator unreachable or rejects, deny the request.
     */
    async verifyAndSettle(input: VerifyPaymentInput): Promise<PaymentVerifyResult> {
        try {
            // ── Step 1: Verify ─────────────────────────────────
            const verifyResult = await facilitatorClient.verify(
                input.paymentPayload,
                input.paymentRequirements
            );

            if (!verifyResult.isValid) {
                emitMetric({ eventType: "verify_error", metadata: { reason: verifyResult.invalidReason?.substring(0, 100) } });
                return {
                    valid: false,
                    error: verifyResult.invalidReason ?? "Facilitator rejected payment"
                };
            }

            emitMetric({ eventType: "verify_ok" });

            // ── Step 2: Settle ─────────────────────────────────
            const settleResult = await facilitatorClient.settle(
                input.paymentPayload,
                input.paymentRequirements
            );

            if (!settleResult.success) {
                emitMetric({ eventType: "settle_failed", metadata: { reason: settleResult.errorReason?.substring(0, 100) } });
                return {
                    valid: false,
                    error: settleResult.errorReason ?? "Settlement failed"
                };
            }

            emitMetric({ eventType: "settle_ok" });

            // ── Step 3: Record in DB (atomic anti-replay) ──────
            const txHash = settleResult.transaction;   // on-chain tx hash = source of truth
            const payer = settleResult.payer ?? verifyResult.payer ?? input.payer;

            const { inserted } = await this.paymentRepo.recordPayment({
                txHash,
                payer,
                amount: input.paymentRequirements.amount,
                tierAmount: input.tierAmount,
                status: "settled",    // facilitator already submitted + confirmed
                settleId: txHash      // for settled payments, settleId = txHash
            });

            if (!inserted) {
                // Duplicate txHash — replay blocked
                emitMetric({ eventType: "replay_blocked" });
                return {
                    valid: false,
                    error: "Transaction hash already used (replay)"
                };
            }

            return {
                valid: true,
                settleResponse: settleResult
            };
        } catch (error) {
            if (error instanceof FacilitatorError) {
                return {
                    valid: false,
                    error: `Payment verification failed: ${error.message}`
                };
            }
            return {
                valid: false,
                error: "Payment verification failed: internal error"
            };
        }
    }
}

// ── Singleton ──────────────────────────────────────────────
export const paymentService = new PaymentService();
