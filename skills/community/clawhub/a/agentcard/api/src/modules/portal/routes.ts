import { appLogger } from "../../utils/logger";
/**
 * Portal Routes — Owner Cabinet API endpoints.
 *
 * All endpoints require wallet authentication (reuses existing walletAuth).
 *
 * @module modules/portal/routes
 */

import { Router } from "express";
import { requireWalletAuth } from "../../middleware/walletAuth";
import { LinkService } from "./linkService";
import { agentAccessRouter } from "./agentAccess";

export const portalRouter = Router();

// All portal routes require wallet auth
portalRouter.use(requireWalletAuth);

// Mount REALIGN agent access management
portalRouter.use(agentAccessRouter);

/**
 * POST /portal/telegram/link-token
 * Generate a one-time deep-link token for Telegram binding.
 */
portalRouter.post("/telegram/link-token", async (req, res) => {
    if (!req.walletContext) {
        res.status(401).json({ error: "Wallet auth required" });
        return;
    }

    try {
        const result = await LinkService.issueToken(
            req.walletContext.address,
            req.ip
        );

        res.json({
            deepLink: result.deepLink,
            expiresAt: result.expiresAt,
            message: "Open this link in Telegram to connect your account.",
        });
    } catch (error) {
        appLogger.error({ err: error }, "[PORTAL] link-token error");
        res.status(500).json({ error: "Failed to generate link token" });
    }
});

/**
 * POST /portal/telegram/revoke
 * Disconnect Telegram from wallet. Immediately invalidates bot access.
 */
portalRouter.post("/telegram/revoke", async (req, res) => {
    if (!req.walletContext) {
        res.status(401).json({ error: "Wallet auth required" });
        return;
    }

    try {
        const revoked = await LinkService.revokeBinding(
            req.walletContext.address,
            req.ip
        );

        res.json({
            revoked,
            message: revoked
                ? "Telegram account disconnected. Bot access revoked immediately."
                : "No active Telegram connection found.",
        });
    } catch (error) {
        appLogger.error({ err: error }, "[PORTAL] revoke error");
        res.status(500).json({ error: "Failed to revoke binding" });
    }
});

/**
 * GET /portal/telegram/status
 * Get current Telegram link status for the wallet.
 */
portalRouter.get("/telegram/status", async (req, res) => {
    if (!req.walletContext) {
        res.status(401).json({ error: "Wallet auth required" });
        return;
    }

    try {
        const status = await LinkService.getStatus(req.walletContext.address);
        res.json(status);
    } catch (error) {
        appLogger.error({ err: error }, "[PORTAL] status error");
        res.status(500).json({ error: "Failed to get link status" });
    }
});
