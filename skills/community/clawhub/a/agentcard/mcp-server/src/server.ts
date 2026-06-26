/**
 * @asgcard/mcp-server — Core MCP Server
 *
 * Exposes 8 tools for AI agents to manage ASGCard virtual cards:
 *   - create_card:       Create a virtual card (x402 autonomous payment)
 *   - fund_card:         Fund an existing card (x402 autonomous payment)
 *   - list_cards:        List all cards for the wallet
 *   - get_card:          Get card summary by ID
 *   - get_card_details:  Get sensitive card details (PAN, CVV, expiry)
 *   - freeze_card:       Freeze a card temporarily
 *   - unfreeze_card:     Unfreeze a frozen card
 *   - get_pricing:       Get available tier pricing
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { ASGCardClient } from "@asgcard/sdk";
import { WalletClient } from "./wallet-client.js";

export interface ServerConfig {
  /** Stellar secret key (S...) */
  privateKey: string;
  /** ASGCard API base URL */
  apiUrl?: string;
  /** Soroban RPC URL */
  rpcUrl?: string;
}

const VALID_AMOUNTS = [10, 25, 50, 100, 200, 500] as const;

export function createASGCardServer(config: ServerConfig): McpServer {
  const apiUrl = config.apiUrl ?? "https://api.asgcard.dev";

  // SDK client for x402-paid operations (create, fund, tiers, health)
  const sdkClient = new ASGCardClient({
    privateKey: config.privateKey,
    baseUrl: apiUrl,
    rpcUrl: config.rpcUrl,
  });

  // Wallet client for wallet-auth operations (list, get, details, freeze, unfreeze)
  const walletClient = new WalletClient({
    privateKey: config.privateKey,
    baseUrl: apiUrl,
  });

  const server = new McpServer({
    name: "asgcard",
    version: "0.1.0",
  });

  // ── Tool 1: create_card ───────────────────────────────────

  // @ts-expect-error — TS2589: MCP SDK server.tool() generic depth exceeds TS limit; runtime is correct
  server.tool(
    "create_card",
    "Create a new virtual debit card. Pays on-chain with USDC via x402 protocol — fully autonomous, no human intervention needed. Returns card details (PAN, CVV, expiry) in the response.",
    {
      amount: z
        .enum(["10", "25", "50", "100", "200", "500"])
        .describe("Card tier amount in USD. Available tiers: 10, 25, 50, 100, 200, 500"),
      nameOnCard: z.string().min(1).describe("Name to print on the virtual card"),
      email: z.string().email().describe("Email address for card notifications"),
    },
    async ({ amount, nameOnCard, email }) => {
      try {
        const numericAmount = Number(amount) as (typeof VALID_AMOUNTS)[number];
        const result = await sdkClient.createCard({
          amount: numericAmount,
          nameOnCard,
          email,
        });

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error creating card: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 2: fund_card ─────────────────────────────────────

  server.tool(
    "fund_card",
    "Fund an existing card with additional USDC. Pays on-chain via x402 protocol — fully autonomous.",
    {
      amount: z
        .enum(["10", "25", "50", "100", "200", "500"])
        .describe("Fund tier amount in USD. Available tiers: 10, 25, 50, 100, 200, 500"),
      cardId: z.string().min(1).describe("The card ID to fund"),
    },
    async ({ amount, cardId }) => {
      try {
        const numericAmount = Number(amount) as (typeof VALID_AMOUNTS)[number];
        const result = await sdkClient.fundCard({
          amount: numericAmount,
          cardId,
        });

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error funding card: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 3: list_cards ────────────────────────────────────

  server.tool(
    "list_cards",
    "List all virtual cards associated with the configured wallet. Returns card IDs, names, balances, and statuses.",
    {},
    async () => {
      try {
        const result = await walletClient.listCards();

        if (!result.cards || result.cards.length === 0) {
          return {
            content: [
              {
                type: "text" as const,
                text: "No cards found. Use create_card to issue a new virtual card.",
              },
            ],
          };
        }

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error listing cards: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 4: get_card ──────────────────────────────────────

  server.tool(
    "get_card",
    "Get summary information for a specific card (balance, status, name). Does NOT return sensitive details like card number or CVV — use get_card_details for that.",
    {
      cardId: z.string().min(1).describe("The card ID to look up"),
    },
    async ({ cardId }) => {
      try {
        const result = await walletClient.getCard(cardId);

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error getting card: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 5: get_card_details ──────────────────────────────

  server.tool(
    "get_card_details",
    "Get sensitive card details: full card number (PAN), CVV, expiry date, and billing address. Use ONLY when you need to fill in a payment form. Prefer get_card or list_cards for balance checks.",
    {
      cardId: z.string().min(1).describe("The card ID to get details for"),
    },
    async ({ cardId }) => {
      try {
        const result = await walletClient.getCardDetails(cardId);

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error getting card details: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 6: freeze_card ───────────────────────────────────

  server.tool(
    "freeze_card",
    "Temporarily freeze a card. The card cannot be used for purchases while frozen. Use unfreeze_card to re-enable it. This is reversible (unlike closing a card).",
    {
      cardId: z.string().min(1).describe("The card ID to freeze"),
    },
    async ({ cardId }) => {
      try {
        const result = await walletClient.freezeCard(cardId);

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error freezing card: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 7: unfreeze_card ─────────────────────────────────

  server.tool(
    "unfreeze_card",
    "Unfreeze a previously frozen card, re-enabling it for purchases.",
    {
      cardId: z.string().min(1).describe("The card ID to unfreeze"),
    },
    async ({ cardId }) => {
      try {
        const result = await walletClient.unfreezeCard(cardId);

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error unfreezing card: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 8: get_pricing ───────────────────────────────────

  server.tool(
    "get_pricing",
    "Get current pricing tiers for card creation and funding. Shows available amounts, total costs (including fees), and API endpoints for each tier.",
    {},
    async () => {
      try {
        const result = await sdkClient.getTiers();

        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text" as const,
              text: `Error getting pricing: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  return server;
}
