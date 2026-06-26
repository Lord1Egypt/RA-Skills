import { env } from "../config/env";
import type {
    PaymentPayload,
    PaymentRequirements,
    VerifyRequest,
    VerifyResponse,
    SettleRequest,
    SettleResponse,
} from "../types/x402";

// ── Errors ─────────────────────────────────────────────────

export class FacilitatorError extends Error {
    constructor(
        message: string,
        public readonly statusCode?: number,
        public readonly retryable: boolean = false
    ) {
        super(message);
        this.name = "FacilitatorError";
    }
}

// ── Retry helper ───────────────────────────────────────────

const sleep = (ms: number): Promise<void> =>
    new Promise((resolve) => setTimeout(resolve, ms));

const withRetry = async <T>(
    fn: () => Promise<T>,
    maxRetries: number,
    backoffMs: number[]
): Promise<T> => {
    let lastError: Error | undefined;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            return await fn();
        } catch (error) {
            lastError = error instanceof Error ? error : new Error(String(error));

            if (error instanceof FacilitatorError && !error.retryable) {
                throw error;
            }

            if (attempt < maxRetries) {
                const delay = backoffMs[attempt] ?? backoffMs[backoffMs.length - 1] ?? 1000;
                await sleep(delay);
            }
        }
    }

    throw lastError ?? new FacilitatorError("Max retries exceeded", undefined, false);
};

// ── FacilitatorClient (x402 v2 canonical) ──────────────────

export class FacilitatorClient {
    private baseUrl: string;
    private apiKey: string;
    private timeoutMs: number;
    private maxRetries: number;

    constructor(config?: {
        baseUrl?: string;
        apiKey?: string;
        timeoutMs?: number;
        maxRetries?: number;
    }) {
        this.baseUrl = config?.baseUrl ?? env.FACILITATOR_URL;
        this.apiKey = config?.apiKey ?? env.FACILITATOR_API_KEY;
        this.timeoutMs = config?.timeoutMs ?? env.FACILITATOR_TIMEOUT_MS;
        this.maxRetries = config?.maxRetries ?? env.FACILITATOR_MAX_RETRIES;
    }

    /**
     * POST /verify — x402 v2 canonical
     * Body: { paymentPayload, paymentRequirements }
     * Response: { isValid, invalidReason?, payer? }
     */
    async verify(
        paymentPayload: PaymentPayload,
        paymentRequirements: PaymentRequirements
    ): Promise<VerifyResponse> {
        const request: VerifyRequest = { paymentPayload, paymentRequirements };
        return withRetry(
            () => this.doPost<VerifyResponse>("/verify", request),
            this.maxRetries,
            [1000, 3000]
        );
    }

    /**
     * POST /settle — x402 v2 canonical
     * Body: { paymentPayload, paymentRequirements }
     * Response: { success, transaction, network, payer?, errorReason? }
     */
    async settle(
        paymentPayload: PaymentPayload,
        paymentRequirements: PaymentRequirements
    ): Promise<SettleResponse> {
        const request: SettleRequest = { paymentPayload, paymentRequirements };
        return withRetry(
            () => this.doPost<SettleResponse>("/settle", request),
            5,
            [2000, 4000, 8000, 16000, 30000]
        );
    }

    /**
     * GET /supported — check facilitator capabilities
     */
    async supported(): Promise<unknown> {
        return this.doGet("/supported");
    }

    private async doPost<T>(path: string, body: unknown): Promise<T> {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

        try {
            const response = await fetch(`${this.baseUrl}${path}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${this.apiKey}`,
                    "Bypass-Tunnel-Reminder": "true",
                    "User-Agent": "curl/8.x"
                },
                body: JSON.stringify(body),
                signal: controller.signal
            });

            if (!response.ok) {
                const text = await response.text().catch(() => "");
                throw new FacilitatorError(
                    `Facilitator ${path} failed: ${response.status} ${text}`,
                    response.status,
                    response.status >= 500
                );
            }

            return (await response.json()) as T;
        } catch (error) {
            if (error instanceof FacilitatorError) throw error;

            if (error instanceof Error && error.name === "AbortError") {
                throw new FacilitatorError(
                    `Facilitator ${path} timeout after ${this.timeoutMs}ms`,
                    undefined,
                    true
                );
            }

            throw new FacilitatorError(
                `Facilitator ${path} network error: ${error instanceof Error ? error.message : String(error)}`,
                undefined,
                true
            );
        } finally {
            clearTimeout(timeout);
        }
    }

    private async doGet<T>(path: string): Promise<T> {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

        try {
            const response = await fetch(`${this.baseUrl}${path}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${this.apiKey}`,
                },
                signal: controller.signal
            });

            if (!response.ok) {
                const text = await response.text().catch(() => "");
                throw new FacilitatorError(
                    `Facilitator ${path} failed: ${response.status} ${text}`,
                    response.status,
                    response.status >= 500
                );
            }

            return (await response.json()) as T;
        } catch (error) {
            if (error instanceof FacilitatorError) throw error;
            throw new FacilitatorError(
                `Facilitator ${path} error: ${error instanceof Error ? error.message : String(error)}`,
                undefined,
                true
            );
        } finally {
            clearTimeout(timeout);
        }
    }
}

// ── Singleton ──────────────────────────────────────────────
export const facilitatorClient = new FacilitatorClient();
