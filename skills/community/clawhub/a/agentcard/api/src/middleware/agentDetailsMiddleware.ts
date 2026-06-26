import { appLogger } from "../utils/logger";
import type { Request, Response, NextFunction } from "express";
import crypto from "node:crypto";
import { cardRepository } from "../repositories/runtime";
import { env } from "../config/env";

/**
 * REALIGN-003: Nonce + anti-replay + rate-limit middleware
 * for agent card details access.
 *
 * - Requires X-AGENT-NONCE header (UUID v4 format)
 * - Rejects if nonce was already used (anti-replay)
 * - Rate limit: controlled by DETAILS_READ_LIMIT_PER_HOUR
 */

const UUID_V4_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export const requireAgentNonce = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const nonce = req.header("X-AGENT-NONCE");

    if (!nonce) {
        res.status(400).json({
            error: "Missing X-AGENT-NONCE header",
            hint: "Generate a UUID v4 nonce for each details request"
        });
        return;
    }

    // Validate UUID v4 format
    if (!UUID_V4_REGEX.test(nonce)) {
        res.status(400).json({ error: "X-AGENT-NONCE must be UUID v4 format" });
        return;
    }

    const cardId = req.params.cardId;
    const walletAddress = (req as any).walletContext?.address;

    if (!cardId || !walletAddress) {
        // Fallback if applied improperly, though wallet auth ensures context
        res.status(500).json({ error: "Context missing for nonce tracking" });
        return;
    }

    try {
        const result = await cardRepository.recordNonceAndCheckRateLimit(
            walletAddress,
            cardId,
            nonce,
            env.DETAILS_READ_LIMIT_PER_HOUR
        );

        if (!result.allowed) {
            if (result.reason === 'replay') {
                res.status(409).json({
                    error: "Nonce already used (replay detected)",
                    code: "REPLAY_REJECTED"
                });
                return;
            }
            if (result.reason === 'rate_limit') {
                res.status(429).json({
                    error: `Card details rate limit exceeded (${env.DETAILS_READ_LIMIT_PER_HOUR} requests/hour)`,
                    retryAfterSeconds: result.retryAfterSeconds
                });
                return;
            }
        }
        next();
    } catch (e) {
        appLogger.error({ err: e }, "Nonce Tracking Error:");
        res.status(500).json({ error: "Internal server error" });
    }
};

/**
 * Hash a nonce for audit logging (don't store raw nonces in logs)
 */
export const hashNonce = (nonce: string): string =>
    crypto.createHash("sha256").update(nonce).digest("hex").slice(0, 16);
