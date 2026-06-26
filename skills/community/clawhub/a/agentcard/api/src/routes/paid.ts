import { Router } from "express";
import { z } from "zod";
import { requireX402Payment } from "../middleware/x402";
import { cardService, HttpError } from "../services/cardService";

const createCardSchema = z.object({
  nameOnCard: z.string().min(1),
  email: z.string().email()
});

const fundCardSchema = z.object({
  cardId: z.string().min(1)
});

export const paidRouter = Router();

paidRouter.post("/create/tier/:amount", requireX402Payment("create"), async (req, res) => {
  if (!req.paymentContext) {
    res.status(500).json({ error: "Payment context unavailable" });
    return;
  }

  const parsed = createCardSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid request body" });
    return;
  }

  try {
    const result = await cardService.createCard({
      walletAddress: req.paymentContext.payer,
      nameOnCard: parsed.data.nameOnCard,
      email: parsed.data.email,
      initialAmountUsd: req.paymentContext.tierAmount,
      tierAmount: req.paymentContext.tierAmount,
      chargedUsd: req.paymentContext.totalCostUsd,
      txHash: req.paymentContext.txHash
    });

    // REALIGN-001/002: Agent-first — unified contract (detailsEnvelope only, no flat details leak)
    const response: Record<string, unknown> = {
      success: result.success,
      card: result.card,
      payment: result.payment,
    };
    if (result.details) {
      response.detailsEnvelope = {
        cardNumber: result.details.cardNumber,
        cvv: result.details.cvv,
        expiryMonth: result.details.expiryMonth,
        expiryYear: result.details.expiryYear,
        billingAddress: result.details.billingAddress,
        oneTimeAccess: true,
        expiresInSeconds: 300,
        note: "Store securely. Use GET /cards/:id/details with X-AGENT-NONCE for subsequent access."
      };
    }

    res.status(201).json(response);
  } catch (error) {
    if (error instanceof HttpError) {
      res.status(error.status).json({ error: error.message });
      return;
    }

    res.status(500).json({ error: "Internal server error" });
  }
});

paidRouter.post("/fund/tier/:amount", requireX402Payment("fund"), async (req, res) => {
  if (!req.paymentContext) {
    res.status(500).json({ error: "Payment context unavailable" });
    return;
  }

  const parsed = fundCardSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid request body" });
    return;
  }

  try {
    const result = await cardService.fundCard({
      walletAddress: req.paymentContext.payer,
      cardId: parsed.data.cardId,
      fundAmountUsd: req.paymentContext.tierAmount,
      chargedUsd: req.paymentContext.totalCostUsd,
      txHash: req.paymentContext.txHash
    });

    res.status(200).json(result);
  } catch (error) {
    if (error instanceof HttpError) {
      res.status(error.status).json({ error: error.message });
      return;
    }

    res.status(500).json({ error: "Internal server error" });
  }
});
