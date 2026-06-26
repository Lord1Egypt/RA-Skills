import { Router } from "express";
import { requireWalletAuth } from "../middleware/walletAuth";
import { requireAgentNonce } from "../middleware/agentDetailsMiddleware";
import { cardService, HttpError } from "../services/cardService";

export const walletRouter = Router();

walletRouter.use(requireWalletAuth);

walletRouter.get("/", async (req, res) => {
  if (!req.walletContext) {
    res.status(401).json({ error: "Wallet auth required" });
    return;
  }

  const cards = await cardService.listCards(req.walletContext.address);
  res.json({ cards });
});

walletRouter.get("/:cardId", async (req, res) => {
  if (!req.walletContext) {
    res.status(401).json({ error: "Wallet auth required" });
    return;
  }

  try {
    const result = await cardService.getCard(req.walletContext.address, req.params.cardId);
    res.json(result);
  } catch (error) {
    if (error instanceof HttpError) {
      res.status(error.status).json({ error: error.message });
      return;
    }

    res.status(500).json({ error: "Internal server error" });
  }
});

// REALIGN-003: Nonce + anti-replay always enabled for details access
walletRouter.get("/:cardId/details", requireAgentNonce, async (req, res) => {
  if (!req.walletContext) {
    res.status(401).json({ error: "Wallet auth required" });
    return;
  }

  try {
    const result = await cardService.getCardDetails(req.walletContext.address, req.params.cardId);
    res.json(result);
  } catch (error) {
    if (error instanceof HttpError) {
      res.status(error.status).json({ error: error.message });
      return;
    }

    res.status(500).json({ error: "Internal server error" });
  }
});

walletRouter.post("/:cardId/freeze", async (req, res) => {
  if (!req.walletContext) {
    res.status(401).json({ error: "Wallet auth required" });
    return;
  }

  try {
    const result = await cardService.setCardStatus(
      req.walletContext.address,
      req.params.cardId,
      "frozen"
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

walletRouter.post("/:cardId/unfreeze", async (req, res) => {
  if (!req.walletContext) {
    res.status(401).json({ error: "Wallet auth required" });
    return;
  }

  try {
    const result = await cardService.setCardStatus(
      req.walletContext.address,
      req.params.cardId,
      "active"
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
