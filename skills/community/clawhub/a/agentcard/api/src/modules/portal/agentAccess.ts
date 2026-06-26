import { Router } from "express";
import { requireWalletAuth } from "../../middleware/walletAuth";
import { cardService, HttpError } from "../../services/cardService";

/**
 * REALIGN-005: Owner can revoke/restore agent access to card details.
 * Owner remains secondary control plane — doesn't block card creation
 * or basic agent flow, but can cut off details access.
 */
export const agentAccessRouter = Router();

agentAccessRouter.use(requireWalletAuth);

// POST /portal/cards/:cardId/revoke-details
agentAccessRouter.post("/cards/:cardId/revoke-details", async (req, res) => {
    if (!req.walletContext) {
        res.status(401).json({ error: "Wallet auth required" });
        return;
    }

    try {
        const result = await cardService.setDetailsRevoked(
            req.walletContext.address,
            req.params.cardId,
            true
        );
        res.json(result);
    } catch (error) {
        if (error instanceof HttpError) {
            res.status(error.status).json({ error: error.message });
            return;
        }
        res.status(500).json({ error: "Internal server error" });
    }
});

// POST /portal/cards/:cardId/restore-details
agentAccessRouter.post("/cards/:cardId/restore-details", async (req, res) => {
    if (!req.walletContext) {
        res.status(401).json({ error: "Wallet auth required" });
        return;
    }

    try {
        const result = await cardService.setDetailsRevoked(
            req.walletContext.address,
            req.params.cardId,
            false
        );
        res.json(result);
    } catch (error) {
        if (error instanceof HttpError) {
            res.status(error.status).json({ error: error.message });
            return;
        }
        res.status(500).json({ error: "Internal server error" });
    }
});
