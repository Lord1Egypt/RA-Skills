import type { CardDetails, TierAmount } from "../types/domain";
import type { CardRepository } from "../repositories/types";
import { cardRepository } from "../repositories/runtime";
import { getFourPaymentsClient, FourPaymentsError } from "./fourPaymentsClient";
import type { FPCardIssued, FPSensitiveInfo } from "./fourPaymentsClient";
import { AdminBot } from "../modules/admin/adminBot";

/** Default billing address for ASG virtual cards */
const ASG_DEFAULT_BILLING_ADDRESS = {
  street: "1 Market Street",
  city: "San Francisco",
  state: "CA",
  zip: "94105",
  country: "US",
} as const;

class HttpError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

class CardService {
  private readonly repo: CardRepository;

  constructor(repo: CardRepository = cardRepository) {
    this.repo = repo;
  }

  /**
   * Create a new prepaid card via 4payments API.
   * 1. Issue card via 4payments (returns real card number, CVV, expiry)
   * 2. Top up with initial balance
   * 3. Store in our DB with 4payments ID
   */
  async createCard(input: {
    walletAddress: string;
    nameOnCard: string;
    email: string;
    initialAmountUsd: number;
    tierAmount: TierAmount;
    chargedUsd: number;
    txHash: string;
  }) {
    const fp = getFourPaymentsClient();

    // Generate our own external ID for tracking
    const externalId = `asg_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

    // Parse name into first/last for 4payments
    const nameParts = input.nameOnCard.trim().split(/\s+/);
    const firstName = nameParts[0] || "Card";
    const lastName = nameParts.slice(1).join(" ") || "Holder";

    // Sync: look up profile email/phone from owner_telegram_links
    let profileEmail = input.email;
    let profilePhone = "+17073164477"; // default for new clients

    try {
      const { query: dbQuery } = await import("../db/db");
      const rows = await dbQuery<{ email: string | null; phone: string | null }>(
        `SELECT email, phone FROM owner_telegram_links
         WHERE owner_wallet = $1 AND status = 'active' LIMIT 1`,
        [input.walletAddress]
      );
      if (rows.length > 0) {
        if (rows[0].email) profileEmail = rows[0].email;
        if (rows[0].phone) profilePhone = rows[0].phone;
      }
    } catch (err) {
      console.error("[cardService] Profile lookup failed, using request values:", err);
    }

    // Step 1: Issue card via 4payments
    let fpCard: FPCardIssued;
    try {
      fpCard = await fp.issueCard({
        externalId,
        firstName,
        lastName,
        email: profileEmail,
        phone: profilePhone,
        label: `ASG ${input.nameOnCard}`.slice(0, 50),
        initialBalance: input.initialAmountUsd,
      });
    } catch (error) {
      if (error instanceof FourPaymentsError) {
        console.error("[4payments] issueCard failed:", error.statusCode, error.responseBody);
        throw new HttpError(502, `Card issuance failed: ${error.message}`);
      }
      throw error;
    }

    // Step 2: Top up with initial amount (if card was issued without initialBalance)
    if (fpCard.cardBalance < input.initialAmountUsd) {
      try {
        await fp.topUpCard(fpCard.id, input.initialAmountUsd, externalId);
      } catch (error) {
        if (error instanceof FourPaymentsError) {
          console.error("[4payments] topUpCard failed:", error.statusCode, error.responseBody);
          // Card was issued but top-up failed — still return card but note the issue
          console.error("[4payments] Card issued but top-up failed. Card ID:", fpCard.id);
        }
      }
    }

    // Step 3: Parse card details from 4payments response
    let cardDetails = this.parseCardDetails(fpCard);

    // Fallback: if issueCard response has empty sensitive fields,
    // fetch them separately via getSensitiveInfo (P2 fix)
    if (!cardDetails.cardNumber || cardDetails.expiryMonth === 0) {
      try {
        const sensitive = await fp.getSensitiveInfo(fpCard.id);
        cardDetails = this.parseSensitiveInfo(sensitive);
      } catch (err) {
        console.error("[4payments] getSensitiveInfo fallback failed:", err);
        // Continue with whatever we have from issueCard
      }
    }

    // Step 4: Store in our DB
    const card = await this.repo.create({
      walletAddress: input.walletAddress,
      nameOnCard: input.nameOnCard,
      email: input.email,
      initialAmountUsd: input.initialAmountUsd,
      tierAmount: input.tierAmount,
      txHash: input.txHash,
      details: cardDetails,
      fourPaymentsId: fpCard.id,
    });

    const result = {
      success: true as const,
      card: {
        cardId: card.cardId,
        nameOnCard: card.nameOnCard,
        balance: input.initialAmountUsd,
        status: card.status,
        createdAt: card.createdAt,
      },
      payment: {
        amountCharged: input.chargedUsd,
        txHash: input.txHash,
        network: "stellar" as const,
      },
      details: cardDetails,
    };

    // Notify admin bot
    AdminBot.cardCreated({
      cardId: card.cardId,
      wallet: input.walletAddress,
      tier: input.tierAmount,
      balance: input.initialAmountUsd,
      last4: cardDetails.cardNumber?.slice(-4) ?? "????",
    }).catch(() => {});

    return result;
  }

  /**
   * Fund an existing card via 4payments API.
   */
  async fundCard(input: {
    walletAddress: string;
    cardId: string;
    fundAmountUsd: number;
    chargedUsd: number;
    txHash: string;
  }) {
    const card = await this.repo.findById(input.cardId);
    if (!card || card.walletAddress !== input.walletAddress) {
      throw new HttpError(404, "Card not found");
    }

    if (!card.fourPaymentsId) {
      throw new HttpError(400, "Card missing 4payments ID — cannot top up");
    }

    const fp = getFourPaymentsClient();

    // Top up via 4payments
    try {
      await fp.topUpCard(card.fourPaymentsId, input.fundAmountUsd);
    } catch (error) {
      if (error instanceof FourPaymentsError) {
        console.error("[4payments] topUpCard failed:", error.statusCode, error.responseBody);
        throw new HttpError(502, `Card top-up failed: ${error.message}`);
      }
      throw error;
    }

    // Update local balance
    const updated = await this.repo.addBalance(card.cardId, input.fundAmountUsd);
    if (!updated) {
      throw new HttpError(500, "Unable to update card balance");
    }

    const refreshed = await this.repo.findById(card.cardId);
    if (!refreshed) {
      throw new HttpError(500, "Card not found after balance update");
    }

    const result = {
      success: true,
      cardId: card.cardId,
      fundedAmount: input.fundAmountUsd,
      newBalance: refreshed.balance,
      payment: {
        amountCharged: input.chargedUsd,
        txHash: input.txHash,
        network: "stellar",
      },
    };

    // Notify admin bot
    AdminBot.cardFunded({
      cardId: card.cardId,
      amount: input.fundAmountUsd,
      newBalance: refreshed.balance,
      last4: card.details?.cardNumber?.slice(-4) ?? "????",
      txHash: input.txHash,
    }).catch(() => {});

    return result;
  }

  async listCards(walletAddress: string) {
    const cards = await this.repo.findByWallet(walletAddress);
    return cards.map((card) => ({
      cardId: card.cardId,
      nameOnCard: card.nameOnCard,
      lastFour: (card as any).lastFour || card.details?.cardNumber?.slice(-4) || "????",
      balance: card.balance,
      status: card.status,
      createdAt: card.createdAt,
    }));
  }

  async getCard(walletAddress: string, cardId: string) {
    const card = await this.repo.findById(cardId);
    if (!card || card.walletAddress !== walletAddress) {
      throw new HttpError(404, "Card not found");
    }

    return {
      card: {
        cardId: card.cardId,
        nameOnCard: card.nameOnCard,
        email: card.email,
        balance: card.balance,
        initialAmountUsd: card.initialAmountUsd,
        status: card.status,
        lastFour: (card as any).lastFour || card.details?.cardNumber?.slice(-4) || "????",
        createdAt: card.createdAt,
        updatedAt: card.updatedAt,
        fourPaymentsId: card.fourPaymentsId,
      },
    };
  }

  /**
   * Get card sensitive details.
   * If 4payments ID exists, fetches fresh data from 4payments API.
   * Otherwise falls back to locally stored details.
   */
  async getCardDetails(walletAddress: string, cardId: string) {
    const card = await this.repo.findById(cardId);
    if (!card || card.walletAddress !== walletAddress) {
      throw new HttpError(404, "Card not found");
    }

    // REALIGN-005: Owner can revoke agent access to details
    if ((card as any).detailsRevoked) {
      throw new HttpError(403, "Card details access revoked by owner");
    }

    // If we have a 4payments ID, fetch fresh sensitive info
    if (card.fourPaymentsId) {
      try {
        const fp = getFourPaymentsClient();
        const sensitive = await fp.getSensitiveInfo(card.fourPaymentsId);
        return {
          details: this.parseSensitiveInfo(sensitive),
        };
      } catch (error) {
        console.error("[4payments] getSensitiveInfo failed, falling back to local:", error);
        // Fall through to local details
      }
    }

    return {
      details: card.details,
    };
  }

  async setCardStatus(walletAddress: string, cardId: string, status: "active" | "frozen") {
    const card = await this.repo.findById(cardId);
    if (!card || card.walletAddress !== walletAddress) {
      throw new HttpError(404, "Card not found");
    }

    // Sync with 4payments if we have an ID
    if (card.fourPaymentsId) {
      const fp = getFourPaymentsClient();
      try {
        if (status === "frozen") {
          await fp.freezeCard(card.fourPaymentsId);
        } else {
          await fp.unfreezeCard(card.fourPaymentsId);
        }
      } catch (error) {
        if (error instanceof FourPaymentsError) {
          console.error("[4payments] freeze/unfreeze failed:", error.statusCode, error.responseBody);
          throw new HttpError(502, `Card status update failed: ${error.message}`);
        }
        throw error;
      }
    }

    const updated = await this.repo.updateStatus(cardId, status);
    if (!updated) {
      throw new HttpError(500, "Unable to update card status");
    }

    return {
      success: true,
      cardId: card.cardId,
      status,
    };
  }

  // REALIGN-005: Owner revoke/restore agent access to card details
  async setDetailsRevoked(walletAddress: string, cardId: string, revoked: boolean) {
    const card = await this.repo.findById(cardId);
    if (!card || card.walletAddress !== walletAddress) {
      throw new HttpError(404, "Card not found");
    }

    const updated = await this.repo.setDetailsRevoked(cardId, revoked);
    if (!updated) {
      throw new HttpError(500, "Unable to update card details access");
    }

    return {
      success: true,
      cardId: card.cardId,
      detailsRevoked: revoked,
    };
  }

  // ── Helpers ──────────────────────────────────────────────

  private parseCardDetails(fpCard: FPCardIssued): CardDetails {
    // Parse expiry "MM/YY" or "MM/YYYY"
    const parts = fpCard.cardExpire.split("/");
    let expiryMonth = parseInt(parts[0], 10) || 0;
    let expiryYear = parseInt(parts[1], 10) || 0;
    if (expiryYear < 100) expiryYear += 2000;

    return {
      cardNumber: fpCard.cardNumber,
      expiryMonth,
      expiryYear,
      cvv: fpCard.cardCVC,
      maskedCardNumber: fpCard.maskedCardNumber,
      billingAddress: ASG_DEFAULT_BILLING_ADDRESS,
    };
  }


  private parseSensitiveInfo(sensitive: FPSensitiveInfo): CardDetails {
    const parts = sensitive.expire.split("/");
    let expiryMonth = parseInt(parts[0], 10) || 0;
    let expiryYear = parseInt(parts[1], 10) || 0;
    if (expiryYear < 100) expiryYear += 2000;

    return {
      cardNumber: sensitive.number,
      expiryMonth,
      expiryYear,
      cvv: sensitive.cvc,
      billingAddress: ASG_DEFAULT_BILLING_ADDRESS,
    };
  }
}

export const cardService = new CardService();
export { HttpError };
