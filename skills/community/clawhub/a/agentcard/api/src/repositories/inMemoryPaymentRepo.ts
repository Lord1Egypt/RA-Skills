import crypto from "node:crypto";
import type { PaymentRecord, PaymentRepository } from "./types";

export class InMemoryPaymentRepository implements PaymentRepository {
    private payments = new Map<string, PaymentRecord>();

    async recordPayment(
        payment: Omit<PaymentRecord, "id" | "createdAt" | "updatedAt">
    ): Promise<{ record: PaymentRecord; inserted: boolean }> {
        // Match Postgres ON CONFLICT (tx_hash) DO NOTHING semantics
        const existing = this.payments.get(payment.txHash);
        if (existing) return { record: existing, inserted: false };

        const record: PaymentRecord = {
            ...payment,
            id: `pay_${crypto.randomUUID().slice(0, 8)}`,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        this.payments.set(record.txHash, record);
        return { record, inserted: true };
    }

    async findByTxHash(txHash: string): Promise<PaymentRecord | undefined> {
        return this.payments.get(txHash);
    }

    async markSettled(txHash: string, settleId: string): Promise<boolean> {
        const payment = this.payments.get(txHash);
        if (!payment) return false;
        payment.status = "settled";
        payment.settleId = settleId;
        payment.updatedAt = new Date().toISOString();
        return true;
    }

    async markFailed(
        txHash: string,
        status: "settle_failed" | "verify_failed"
    ): Promise<boolean> {
        const payment = this.payments.get(txHash);
        if (!payment) return false;
        payment.status = status;
        payment.updatedAt = new Date().toISOString();
        return true;
    }
}
