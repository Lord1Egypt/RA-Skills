#!/usr/bin/env node

// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema
} from "@modelcontextprotocol/sdk/types.js";

// src/engines/deal.ts
import { z } from "zod";

// src/client.ts
var DEFAULT_BASE_URLS = {
  deal: "https://deal.works/api",
  fund: "https://fund.works/api",
  bourse: "https://bourse.works/api",
  cadre: "https://cadre.works/api",
  oath: "https://oath.works/api",
  parler: "https://parler.works/api",
  academy: "https://academy.works/api",
  hq: "https://hq.works/api",
  clause: "https://clause.works/api"
};
var RETRYABLE_STATUS_CODES = [429, 502, 503, 504];
var RETRY_DELAYS = [1e3, 2e3, 4e3];
var circuitState = {};
var CIRCUIT_FAILURE_THRESHOLD = 5;
var CIRCUIT_WINDOW_MS = 6e4;
var CIRCUIT_OPEN_DURATION_MS = 3e4;
function checkCircuit(engine) {
  const state = circuitState[engine];
  if (!state) return;
  const now = Date.now();
  if (state.openUntil > now) {
    throw new Error(`Circuit open for ${engine} engine. Retry after ${Math.ceil((state.openUntil - now) / 1e3)}s`);
  }
  if (now - state.lastFailure > CIRCUIT_WINDOW_MS) {
    state.failures = 0;
  }
}
function recordFailure(engine) {
  if (!circuitState[engine]) {
    circuitState[engine] = { failures: 0, lastFailure: 0, openUntil: 0 };
  }
  const state = circuitState[engine];
  const now = Date.now();
  state.failures++;
  state.lastFailure = now;
  if (state.failures >= CIRCUIT_FAILURE_THRESHOLD) {
    state.openUntil = now + CIRCUIT_OPEN_DURATION_MS;
    state.failures = 0;
  }
}
function recordSuccess(engine) {
  if (circuitState[engine]) {
    circuitState[engine].failures = 0;
  }
}
var EngineClient = class {
  apiKey;
  baseUrls;
  timeout;
  maxRetries;
  constructor(config = {}) {
    this.apiKey = config.apiKey ?? process.env.DEAL_WORKS_API_KEY;
    this.baseUrls = { ...DEFAULT_BASE_URLS, ...config.baseUrls };
    this.timeout = config.timeout ?? 3e4;
    this.maxRetries = config.maxRetries ?? 3;
  }
  async fetch(engine, path, options = {}) {
    const { method = "GET", body, idempotencyKey } = options;
    checkCircuit(engine);
    const baseUrl = this.baseUrls[engine];
    if (!baseUrl) {
      return {
        success: false,
        error: {
          code: "UNKNOWN_ENGINE",
          message: `Unknown engine: ${engine}`,
          retryable: false
        }
      };
    }
    const url = `${baseUrl}${path}`;
    const headers = {
      "Content-Type": "application/json",
      "User-Agent": "@goettelman/deal-works-mcp/0.1.0"
    };
    if (this.apiKey) {
      headers["Authorization"] = `Bearer ${this.apiKey}`;
    }
    if (idempotencyKey) {
      headers["X-Idempotency-Key"] = idempotencyKey;
    }
    let lastError = null;
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        const response = await fetch(url, {
          method,
          headers,
          body: body ? JSON.stringify(body) : void 0,
          signal: controller.signal
        });
        clearTimeout(timeoutId);
        if (response.ok) {
          recordSuccess(engine);
          const data = await response.json();
          return { success: true, data };
        }
        const isRetryable = RETRYABLE_STATUS_CODES.includes(response.status);
        if (!isRetryable || attempt === this.maxRetries) {
          recordFailure(engine);
          const errorBody = await response.text();
          return {
            success: false,
            error: {
              code: `HTTP_${response.status}`,
              message: errorBody || response.statusText,
              retryable: isRetryable
            }
          };
        }
        await sleep(RETRY_DELAYS[attempt] ?? 4e3);
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
        if (attempt === this.maxRetries) {
          recordFailure(engine);
          return {
            success: false,
            error: {
              code: "NETWORK_ERROR",
              message: lastError.message,
              retryable: true
            }
          };
        }
        await sleep(RETRY_DELAYS[attempt] ?? 4e3);
      }
    }
    return {
      success: false,
      error: {
        code: "MAX_RETRIES_EXCEEDED",
        message: lastError?.message ?? "Max retries exceeded",
        retryable: false
      }
    };
  }
};
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
var clientInstance = null;
function getEngineClient(config) {
  if (!clientInstance || config) {
    clientInstance = new EngineClient(config);
  }
  return clientInstance;
}

// src/engines/deal.ts
var DealListInputSchema = z.object({
  status: z.enum(["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED"]).optional(),
  limit: z.number().min(1).max(100).default(20),
  offset: z.number().min(0).default(0)
});
var DealCreateInputSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().max(5e3).optional(),
  counterpartyEmail: z.string().email().optional(),
  templateId: z.string().optional(),
  amount: z.number().positive().optional(),
  currency: z.string().default("USD"),
  dueDate: z.string().datetime().optional()
});
var DealGetInputSchema = z.object({
  dealId: z.string().min(1)
});
var DealActionInputSchema = z.object({
  dealId: z.string().min(1),
  action: z.enum(["SIGN", "APPROVE", "REJECT", "CANCEL", "COMPLETE", "ARCHIVE"]),
  comment: z.string().max(1e3).optional()
});
var DealSearchInputSchema = z.object({
  query: z.string().min(1).max(200),
  status: z.enum(["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED"]).optional(),
  fromDate: z.string().datetime().optional(),
  toDate: z.string().datetime().optional(),
  limit: z.number().min(1).max(100).default(20)
});
var DealTimelineInputSchema = z.object({
  dealId: z.string().min(1),
  limit: z.number().min(1).max(100).default(50)
});
var DealAttachmentsInputSchema = z.object({
  dealId: z.string().min(1)
});
var dealTools = [
  {
    name: "deal_list",
    description: "List deals with optional status filter. Returns paginated list of deals for the authenticated user.",
    inputSchema: {
      type: "object",
      properties: {
        status: {
          type: "string",
          enum: ["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED"],
          description: "Filter by deal status"
        },
        limit: {
          type: "number",
          description: "Number of deals to return (max 100)",
          default: 20
        },
        offset: {
          type: "number",
          description: "Pagination offset",
          default: 0
        }
      }
    }
  },
  {
    name: "deal_create",
    description: "Create a new deal. Can optionally use a template and specify counterparty.",
    inputSchema: {
      type: "object",
      properties: {
        title: {
          type: "string",
          description: "Deal title (required)"
        },
        description: {
          type: "string",
          description: "Deal description"
        },
        counterpartyEmail: {
          type: "string",
          description: "Email of the counterparty to invite"
        },
        templateId: {
          type: "string",
          description: "Template ID to base the deal on"
        },
        amount: {
          type: "number",
          description: "Deal amount"
        },
        currency: {
          type: "string",
          description: "Currency code (default: USD)"
        },
        dueDate: {
          type: "string",
          description: "Due date in ISO 8601 format"
        }
      },
      required: ["title"]
    }
  },
  {
    name: "deal_get",
    description: "Get detailed information about a specific deal including parties, terms, and current status.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID"
        }
      },
      required: ["dealId"]
    }
  },
  {
    name: "deal_action",
    description: "Perform an action on a deal: sign, approve, reject, cancel, complete, or archive.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID"
        },
        action: {
          type: "string",
          enum: ["SIGN", "APPROVE", "REJECT", "CANCEL", "COMPLETE", "ARCHIVE"],
          description: "Action to perform"
        },
        comment: {
          type: "string",
          description: "Optional comment for the action"
        }
      },
      required: ["dealId", "action"]
    }
  },
  {
    name: "deal_search",
    description: "Search deals by text query across titles, descriptions, and party names.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Search query"
        },
        status: {
          type: "string",
          enum: ["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED"],
          description: "Filter by status"
        },
        fromDate: {
          type: "string",
          description: "Start date filter (ISO 8601)"
        },
        toDate: {
          type: "string",
          description: "End date filter (ISO 8601)"
        },
        limit: {
          type: "number",
          description: "Max results",
          default: 20
        }
      },
      required: ["query"]
    }
  },
  {
    name: "deal_timeline",
    description: "Get the activity timeline for a deal showing all events and state changes.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID"
        },
        limit: {
          type: "number",
          description: "Max events to return",
          default: 50
        }
      },
      required: ["dealId"]
    }
  },
  {
    name: "deal_attachments",
    description: "List all attachments (documents, files) associated with a deal.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID"
        }
      },
      required: ["dealId"]
    }
  }
];
async function handleDealTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "deal_list": {
      const input = DealListInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.status) params.set("status", input.status);
      params.set("limit", String(input.limit));
      params.set("offset", String(input.offset));
      return client.fetch("deal", `/deals?${params.toString()}`);
    }
    case "deal_create": {
      const input = DealCreateInputSchema.parse(args);
      return client.fetch("deal", "/deals", {
        method: "POST",
        body: input,
        idempotencyKey: `create-${Date.now()}`
      });
    }
    case "deal_get": {
      const input = DealGetInputSchema.parse(args);
      return client.fetch("deal", `/deals/${input.dealId}`);
    }
    case "deal_action": {
      const input = DealActionInputSchema.parse(args);
      return client.fetch("deal", `/deals/${input.dealId}/actions`, {
        method: "POST",
        body: { action: input.action, comment: input.comment },
        idempotencyKey: `action-${input.dealId}-${input.action}-${Date.now()}`
      });
    }
    case "deal_search": {
      const input = DealSearchInputSchema.parse(args);
      return client.fetch("deal", "/deals/search", {
        method: "POST",
        body: input
      });
    }
    case "deal_timeline": {
      const input = DealTimelineInputSchema.parse(args);
      const params = new URLSearchParams({ limit: String(input.limit) });
      return client.fetch("deal", `/deals/${input.dealId}/timeline?${params.toString()}`);
    }
    case "deal_attachments": {
      const input = DealAttachmentsInputSchema.parse(args);
      return client.fetch("deal", `/deals/${input.dealId}/attachments`);
    }
    default:
      throw new Error(`Unknown deal tool: ${name}`);
  }
}

// src/engines/fund.ts
import { z as z2 } from "zod";
var FundBalanceInputSchema = z2.object({
  walletId: z2.string().optional()
});
var FundTransferInputSchema = z2.object({
  toWalletId: z2.string().min(1),
  amount: z2.number().positive(),
  currency: z2.string().default("TALER"),
  memo: z2.string().max(500).optional(),
  idempotencyKey: z2.string().optional()
});
var FundTransactionsInputSchema = z2.object({
  walletId: z2.string().optional(),
  type: z2.enum(["CREDIT", "DEBIT", "ESCROW_LOCK", "ESCROW_RELEASE"]).optional(),
  limit: z2.number().min(1).max(100).default(50),
  offset: z2.number().min(0).default(0)
});
var FundEscrowInputSchema = z2.object({
  dealId: z2.string().min(1),
  amount: z2.number().positive(),
  currency: z2.string().default("TALER"),
  releaseConditions: z2.array(z2.string()).optional()
});
var FundCashoutInputSchema = z2.object({
  amount: z2.number().positive(),
  destinationAddress: z2.string().min(1),
  network: z2.enum(["BASE", "BASE_SEPOLIA"]).default("BASE_SEPOLIA")
});
var FundAgentFundInputSchema = z2.object({
  agentId: z2.string().min(1),
  amount: z2.number().positive(),
  purpose: z2.string().max(200).optional()
});
var fundTools = [
  {
    name: "fund_balance",
    description: "Get wallet balance including available, locked (in escrow), and pending amounts.",
    inputSchema: {
      type: "object",
      properties: {
        walletId: {
          type: "string",
          description: "Wallet ID (optional, defaults to user's primary wallet)"
        }
      }
    }
  },
  {
    name: "fund_transfer",
    description: "Transfer funds between wallets. Supports Taler tokens on Base.",
    inputSchema: {
      type: "object",
      properties: {
        toWalletId: {
          type: "string",
          description: "Destination wallet ID"
        },
        amount: {
          type: "number",
          description: "Amount to transfer"
        },
        currency: {
          type: "string",
          description: "Currency (default: TALER)"
        },
        memo: {
          type: "string",
          description: "Transfer memo/note"
        },
        idempotencyKey: {
          type: "string",
          description: "Idempotency key to prevent duplicate transfers"
        }
      },
      required: ["toWalletId", "amount"]
    }
  },
  {
    name: "fund_transactions",
    description: "List transaction history with optional type filter.",
    inputSchema: {
      type: "object",
      properties: {
        walletId: {
          type: "string",
          description: "Wallet ID (optional)"
        },
        type: {
          type: "string",
          enum: ["CREDIT", "DEBIT", "ESCROW_LOCK", "ESCROW_RELEASE"],
          description: "Filter by transaction type"
        },
        limit: {
          type: "number",
          description: "Max transactions to return",
          default: 50
        },
        offset: {
          type: "number",
          description: "Pagination offset",
          default: 0
        }
      }
    }
  },
  {
    name: "fund_escrow",
    description: "Lock funds in escrow for a deal. Funds are released when deal conditions are met.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID to escrow funds for"
        },
        amount: {
          type: "number",
          description: "Amount to lock"
        },
        currency: {
          type: "string",
          description: "Currency (default: TALER)"
        },
        releaseConditions: {
          type: "array",
          items: { type: "string" },
          description: "Conditions that must be met to release funds"
        }
      },
      required: ["dealId", "amount"]
    }
  },
  {
    name: "fund_cashout",
    description: "Cash out Taler tokens to external wallet address on Base network.",
    inputSchema: {
      type: "object",
      properties: {
        amount: {
          type: "number",
          description: "Amount to cash out"
        },
        destinationAddress: {
          type: "string",
          description: "Destination wallet address (0x...)"
        },
        network: {
          type: "string",
          enum: ["BASE", "BASE_SEPOLIA"],
          description: "Network (default: BASE_SEPOLIA for testnet)"
        }
      },
      required: ["amount", "destinationAddress"]
    }
  },
  {
    name: "fund_agent_fund",
    description: "Fund an agent's operational wallet for autonomous transactions.",
    inputSchema: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Agent ID to fund"
        },
        amount: {
          type: "number",
          description: "Amount to allocate"
        },
        purpose: {
          type: "string",
          description: "Purpose/reason for funding"
        }
      },
      required: ["agentId", "amount"]
    }
  }
];
async function handleFundTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "fund_balance": {
      const input = FundBalanceInputSchema.parse(args);
      const path = input.walletId ? `/wallets/${input.walletId}/balance` : "/wallets/me/balance";
      return client.fetch("fund", path);
    }
    case "fund_transfer": {
      const input = FundTransferInputSchema.parse(args);
      return client.fetch("fund", "/transfers", {
        method: "POST",
        body: input,
        idempotencyKey: input.idempotencyKey ?? `transfer-${Date.now()}`
      });
    }
    case "fund_transactions": {
      const input = FundTransactionsInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.walletId) params.set("walletId", input.walletId);
      if (input.type) params.set("type", input.type);
      params.set("limit", String(input.limit));
      params.set("offset", String(input.offset));
      return client.fetch("fund", `/transactions?${params.toString()}`);
    }
    case "fund_escrow": {
      const input = FundEscrowInputSchema.parse(args);
      return client.fetch("fund", "/escrow", {
        method: "POST",
        body: input,
        idempotencyKey: `escrow-${input.dealId}-${Date.now()}`
      });
    }
    case "fund_cashout": {
      const input = FundCashoutInputSchema.parse(args);
      return client.fetch("fund", "/cashout", {
        method: "POST",
        body: input,
        idempotencyKey: `cashout-${Date.now()}`
      });
    }
    case "fund_agent_fund": {
      const input = FundAgentFundInputSchema.parse(args);
      return client.fetch("fund", `/agents/${input.agentId}/fund`, {
        method: "POST",
        body: { amount: input.amount, purpose: input.purpose },
        idempotencyKey: `agent-fund-${input.agentId}-${Date.now()}`
      });
    }
    default:
      throw new Error(`Unknown fund tool: ${name}`);
  }
}

// src/engines/bourse.ts
import { z as z3 } from "zod";
var BourseSearchInputSchema = z3.object({
  query: z3.string().min(1).max(200),
  category: z3.enum(["TEMPLATE", "SKILL", "INTEGRATION", "CONNECTOR"]).optional(),
  minQuality: z3.number().min(0).max(100).optional(),
  source: z3.enum(["OFFICIAL", "COMMUNITY", "ACTIVEPIECES"]).optional(),
  limit: z3.number().min(1).max(100).default(20)
});
var BourseGetInputSchema = z3.object({
  listingId: z3.string().min(1)
});
var BourseForkInputSchema = z3.object({
  listingId: z3.string().min(1),
  newName: z3.string().min(1).max(100).optional()
});
var BoursePublishInputSchema = z3.object({
  type: z3.enum(["TEMPLATE", "SKILL", "INTEGRATION"]),
  name: z3.string().min(1).max(100),
  description: z3.string().max(2e3),
  content: z3.record(z3.unknown()),
  price: z3.number().min(0).default(0),
  tags: z3.array(z3.string()).default([])
});
var BourseEarningsInputSchema = z3.object({
  period: z3.enum(["DAY", "WEEK", "MONTH", "ALL"]).default("MONTH")
});
var bourseTools = [
  {
    name: "bourse_search",
    description: "Search the Bourse marketplace for templates, skills, and integrations.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Search query"
        },
        category: {
          type: "string",
          enum: ["TEMPLATE", "SKILL", "INTEGRATION", "CONNECTOR"],
          description: "Filter by category"
        },
        minQuality: {
          type: "number",
          description: "Minimum quality score (0-100)"
        },
        source: {
          type: "string",
          enum: ["OFFICIAL", "COMMUNITY", "ACTIVEPIECES"],
          description: "Filter by source"
        },
        limit: {
          type: "number",
          description: "Max results",
          default: 20
        }
      },
      required: ["query"]
    }
  },
  {
    name: "bourse_get",
    description: "Get detailed information about a Bourse listing including reviews and usage stats.",
    inputSchema: {
      type: "object",
      properties: {
        listingId: {
          type: "string",
          description: "Listing ID"
        }
      },
      required: ["listingId"]
    }
  },
  {
    name: "bourse_fork",
    description: "Fork a Bourse listing to create your own customized version.",
    inputSchema: {
      type: "object",
      properties: {
        listingId: {
          type: "string",
          description: "Listing ID to fork"
        },
        newName: {
          type: "string",
          description: "Name for your forked version"
        }
      },
      required: ["listingId"]
    }
  },
  {
    name: "bourse_publish",
    description: "Publish a new template, skill, or integration to the Bourse marketplace.",
    inputSchema: {
      type: "object",
      properties: {
        type: {
          type: "string",
          enum: ["TEMPLATE", "SKILL", "INTEGRATION"],
          description: "Listing type"
        },
        name: {
          type: "string",
          description: "Listing name"
        },
        description: {
          type: "string",
          description: "Description"
        },
        content: {
          type: "object",
          description: "Listing content/definition"
        },
        price: {
          type: "number",
          description: "Price in Talers (0 for free)",
          default: 0
        },
        tags: {
          type: "array",
          items: { type: "string" },
          description: "Tags for discoverability"
        }
      },
      required: ["type", "name", "description", "content"]
    }
  },
  {
    name: "bourse_earnings",
    description: "View your Bourse earnings from published listings.",
    inputSchema: {
      type: "object",
      properties: {
        period: {
          type: "string",
          enum: ["DAY", "WEEK", "MONTH", "ALL"],
          description: "Time period",
          default: "MONTH"
        }
      }
    }
  }
];
async function handleBourseTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "bourse_search": {
      const input = BourseSearchInputSchema.parse(args);
      return client.fetch("bourse", "/listings/search", {
        method: "POST",
        body: input
      });
    }
    case "bourse_get": {
      const input = BourseGetInputSchema.parse(args);
      return client.fetch("bourse", `/listings/${input.listingId}`);
    }
    case "bourse_fork": {
      const input = BourseForkInputSchema.parse(args);
      return client.fetch("bourse", `/listings/${input.listingId}/fork`, {
        method: "POST",
        body: { newName: input.newName },
        idempotencyKey: `fork-${input.listingId}-${Date.now()}`
      });
    }
    case "bourse_publish": {
      const input = BoursePublishInputSchema.parse(args);
      return client.fetch("bourse", "/listings", {
        method: "POST",
        body: input,
        idempotencyKey: `publish-${Date.now()}`
      });
    }
    case "bourse_earnings": {
      const input = BourseEarningsInputSchema.parse(args);
      return client.fetch("bourse", `/earnings?period=${input.period}`);
    }
    default:
      throw new Error(`Unknown bourse tool: ${name}`);
  }
}

// src/engines/cadre.ts
import { z as z4 } from "zod";
var CadreListInputSchema = z4.object({
  status: z4.enum(["RUNNING", "STOPPED", "FAILED", "PENDING"]).optional(),
  limit: z4.number().min(1).max(100).default(20),
  offset: z4.number().min(0).default(0)
});
var CadreDeployInputSchema = z4.object({
  name: z4.string().min(1).max(100),
  skillId: z4.string().min(1),
  config: z4.record(z4.unknown()).optional(),
  fundingAmount: z4.number().positive().optional(),
  slaConfig: z4.object({
    maxLatencyMs: z4.number().positive().optional(),
    minUptime: z4.number().min(0).max(100).optional()
  }).optional()
});
var CadreCommandInputSchema = z4.object({
  agentId: z4.string().min(1),
  command: z4.enum(["START", "STOP", "RESTART", "SCALE_UP", "SCALE_DOWN"]),
  params: z4.record(z4.unknown()).optional()
});
var CadreHealthInputSchema = z4.object({
  agentId: z4.string().min(1)
});
var CadreDelegationsInputSchema = z4.object({
  agentId: z4.string().optional(),
  status: z4.enum(["ACTIVE", "REVOKED", "EXPIRED"]).optional()
});
var CadreSlaViolationsInputSchema = z4.object({
  agentId: z4.string().optional(),
  severity: z4.enum(["LOW", "MEDIUM", "HIGH", "CRITICAL"]).optional(),
  fromDate: z4.string().datetime().optional(),
  limit: z4.number().min(1).max(100).default(50)
});
var cadreTools = [
  {
    name: "cadre_list",
    description: "List deployed agents with optional status filter.",
    inputSchema: {
      type: "object",
      properties: {
        status: {
          type: "string",
          enum: ["RUNNING", "STOPPED", "FAILED", "PENDING"],
          description: "Filter by agent status"
        },
        limit: {
          type: "number",
          description: "Max agents to return",
          default: 20
        },
        offset: {
          type: "number",
          description: "Pagination offset",
          default: 0
        }
      }
    }
  },
  {
    name: "cadre_deploy",
    description: "Deploy a new agent from a skill definition. Optionally fund and configure SLA.",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: "Agent name"
        },
        skillId: {
          type: "string",
          description: "Skill ID from Bourse to deploy"
        },
        config: {
          type: "object",
          description: "Agent configuration overrides"
        },
        fundingAmount: {
          type: "number",
          description: "Initial funding amount in Talers"
        },
        slaConfig: {
          type: "object",
          properties: {
            maxLatencyMs: { type: "number" },
            minUptime: { type: "number" }
          },
          description: "SLA configuration"
        }
      },
      required: ["name", "skillId"]
    }
  },
  {
    name: "cadre_command",
    description: "Send a command to an agent: start, stop, restart, or scale.",
    inputSchema: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Agent ID"
        },
        command: {
          type: "string",
          enum: ["START", "STOP", "RESTART", "SCALE_UP", "SCALE_DOWN"],
          description: "Command to execute"
        },
        params: {
          type: "object",
          description: "Command parameters (e.g., scale factor)"
        }
      },
      required: ["agentId", "command"]
    }
  },
  {
    name: "cadre_health",
    description: "Get health status and metrics for a specific agent.",
    inputSchema: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Agent ID"
        }
      },
      required: ["agentId"]
    }
  },
  {
    name: "cadre_delegations",
    description: "List permission delegations granted to agents.",
    inputSchema: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Filter by agent ID"
        },
        status: {
          type: "string",
          enum: ["ACTIVE", "REVOKED", "EXPIRED"],
          description: "Filter by delegation status"
        }
      }
    }
  },
  {
    name: "cadre_sla_violations",
    description: "List SLA violations for agents. Used for monitoring and alerting.",
    inputSchema: {
      type: "object",
      properties: {
        agentId: {
          type: "string",
          description: "Filter by agent ID"
        },
        severity: {
          type: "string",
          enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
          description: "Filter by severity"
        },
        fromDate: {
          type: "string",
          description: "Start date filter (ISO 8601)"
        },
        limit: {
          type: "number",
          description: "Max violations to return",
          default: 50
        }
      }
    }
  }
];
async function handleCadreTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "cadre_list": {
      const input = CadreListInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.status) params.set("status", input.status);
      params.set("limit", String(input.limit));
      params.set("offset", String(input.offset));
      return client.fetch("cadre", `/agents?${params.toString()}`);
    }
    case "cadre_deploy": {
      const input = CadreDeployInputSchema.parse(args);
      return client.fetch("cadre", "/agents", {
        method: "POST",
        body: input,
        idempotencyKey: `deploy-${input.skillId}-${Date.now()}`
      });
    }
    case "cadre_command": {
      const input = CadreCommandInputSchema.parse(args);
      return client.fetch("cadre", `/agents/${input.agentId}/command`, {
        method: "POST",
        body: { command: input.command, params: input.params },
        idempotencyKey: `command-${input.agentId}-${input.command}-${Date.now()}`
      });
    }
    case "cadre_health": {
      const input = CadreHealthInputSchema.parse(args);
      return client.fetch("cadre", `/agents/${input.agentId}/health`);
    }
    case "cadre_delegations": {
      const input = CadreDelegationsInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.agentId) params.set("agentId", input.agentId);
      if (input.status) params.set("status", input.status);
      return client.fetch("cadre", `/delegations?${params.toString()}`);
    }
    case "cadre_sla_violations": {
      const input = CadreSlaViolationsInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.agentId) params.set("agentId", input.agentId);
      if (input.severity) params.set("severity", input.severity);
      if (input.fromDate) params.set("fromDate", input.fromDate);
      params.set("limit", String(input.limit));
      return client.fetch("cadre", `/sla-violations?${params.toString()}`);
    }
    default:
      throw new Error(`Unknown cadre tool: ${name}`);
  }
}

// src/engines/oath.ts
import { z as z5 } from "zod";
var OathAttestInputSchema = z5.object({
  dealId: z5.string().min(1),
  type: z5.enum(["COMPLETION", "QUALITY", "DELIVERY", "PAYMENT", "CUSTOM"]),
  evidence: z5.record(z5.unknown()).optional(),
  comment: z5.string().max(1e3).optional()
});
var OathVerifyInputSchema = z5.object({
  attestationId: z5.string().min(1)
});
var OathVaultUploadInputSchema = z5.object({
  dealId: z5.string().min(1),
  documents: z5.array(z5.object({
    name: z5.string(),
    contentHash: z5.string(),
    mimeType: z5.string().optional()
  }))
});
var OathVaultSealInputSchema = z5.object({
  dealId: z5.string().min(1),
  sealType: z5.enum(["PARTIAL", "FINAL"]).default("FINAL")
});
var OathTrustTierInputSchema = z5.object({
  userId: z5.string().optional(),
  orgId: z5.string().optional()
});
var oathTools = [
  {
    name: "oath_attest",
    description: "Create an attestation for a deal milestone or outcome. Attestations are cryptographically signed.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID to attest"
        },
        type: {
          type: "string",
          enum: ["COMPLETION", "QUALITY", "DELIVERY", "PAYMENT", "CUSTOM"],
          description: "Attestation type"
        },
        evidence: {
          type: "object",
          description: "Evidence supporting the attestation"
        },
        comment: {
          type: "string",
          description: "Optional comment"
        }
      },
      required: ["dealId", "type"]
    }
  },
  {
    name: "oath_verify",
    description: "Verify an attestation's authenticity and check its on-chain status.",
    inputSchema: {
      type: "object",
      properties: {
        attestationId: {
          type: "string",
          description: "Attestation ID to verify"
        }
      },
      required: ["attestationId"]
    }
  },
  {
    name: "oath_vault_upload",
    description: "Upload document hashes to the secure vault for a deal. Documents are stored off-chain with on-chain anchoring.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID"
        },
        documents: {
          type: "array",
          items: {
            type: "object",
            properties: {
              name: { type: "string" },
              contentHash: { type: "string" },
              mimeType: { type: "string" }
            },
            required: ["name", "contentHash"]
          },
          description: "Documents to upload (hashes only)"
        }
      },
      required: ["dealId", "documents"]
    }
  },
  {
    name: "oath_vault_seal",
    description: "Seal a deal's vault, creating a Merkle root that anchors all documents on-chain.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID"
        },
        sealType: {
          type: "string",
          enum: ["PARTIAL", "FINAL"],
          description: "Seal type (FINAL is irreversible)",
          default: "FINAL"
        }
      },
      required: ["dealId"]
    }
  },
  {
    name: "oath_trust_tier",
    description: "Get the trust tier for a user or organization based on their attestation history.",
    inputSchema: {
      type: "object",
      properties: {
        userId: {
          type: "string",
          description: "User ID to check"
        },
        orgId: {
          type: "string",
          description: "Organization ID to check"
        }
      }
    }
  }
];
async function handleOathTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "oath_attest": {
      const input = OathAttestInputSchema.parse(args);
      return client.fetch("oath", "/attestations", {
        method: "POST",
        body: input,
        idempotencyKey: `attest-${input.dealId}-${input.type}-${Date.now()}`
      });
    }
    case "oath_verify": {
      const input = OathVerifyInputSchema.parse(args);
      return client.fetch("oath", `/attestations/${input.attestationId}/verify`);
    }
    case "oath_vault_upload": {
      const input = OathVaultUploadInputSchema.parse(args);
      return client.fetch("oath", `/deals/${input.dealId}/vault/upload`, {
        method: "POST",
        body: { documents: input.documents },
        idempotencyKey: `vault-upload-${input.dealId}-${Date.now()}`
      });
    }
    case "oath_vault_seal": {
      const input = OathVaultSealInputSchema.parse(args);
      return client.fetch("oath", `/deals/${input.dealId}/vault/seal`, {
        method: "POST",
        body: { sealType: input.sealType },
        idempotencyKey: `vault-seal-${input.dealId}-${Date.now()}`
      });
    }
    case "oath_trust_tier": {
      const input = OathTrustTierInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.userId) params.set("userId", input.userId);
      if (input.orgId) params.set("orgId", input.orgId);
      return client.fetch("oath", `/trust-tier?${params.toString()}`);
    }
    default:
      throw new Error(`Unknown oath tool: ${name}`);
  }
}

// src/engines/parler.ts
import { z as z6 } from "zod";
var ParlerDisputeFileInputSchema = z6.object({
  dealId: z6.string().min(1),
  reason: z6.enum([
    "NON_DELIVERY",
    "QUALITY_ISSUE",
    "LATE_DELIVERY",
    "PAYMENT_DISPUTE",
    "BREACH_OF_TERMS",
    "OTHER"
  ]),
  description: z6.string().min(10).max(5e3),
  evidence: z6.array(z6.object({
    type: z6.string(),
    url: z6.string().url().optional(),
    hash: z6.string().optional(),
    description: z6.string()
  })).optional(),
  requestedResolution: z6.enum(["REFUND", "PARTIAL_REFUND", "COMPLETION", "ARBITRATION"]).optional()
});
var ParlerDisputeListInputSchema = z6.object({
  status: z6.enum(["OPEN", "IN_REVIEW", "RESOLVED", "ESCALATED"]).optional(),
  role: z6.enum(["CLAIMANT", "RESPONDENT", "ARBITRATOR"]).optional(),
  limit: z6.number().min(1).max(100).default(20)
});
var ParlerProposalsInputSchema = z6.object({
  disputeId: z6.string().min(1)
});
var ParlerVoteInputSchema = z6.object({
  proposalId: z6.string().min(1),
  vote: z6.enum(["APPROVE", "REJECT", "ABSTAIN"]),
  comment: z6.string().max(1e3).optional()
});
var parlerTools = [
  {
    name: "parler_dispute_file",
    description: "File a dispute against a deal. Initiates the resolution process.",
    inputSchema: {
      type: "object",
      properties: {
        dealId: {
          type: "string",
          description: "Deal ID to dispute"
        },
        reason: {
          type: "string",
          enum: [
            "NON_DELIVERY",
            "QUALITY_ISSUE",
            "LATE_DELIVERY",
            "PAYMENT_DISPUTE",
            "BREACH_OF_TERMS",
            "OTHER"
          ],
          description: "Dispute reason"
        },
        description: {
          type: "string",
          description: "Detailed description of the dispute"
        },
        evidence: {
          type: "array",
          items: {
            type: "object",
            properties: {
              type: { type: "string" },
              url: { type: "string" },
              hash: { type: "string" },
              description: { type: "string" }
            }
          },
          description: "Supporting evidence"
        },
        requestedResolution: {
          type: "string",
          enum: ["REFUND", "PARTIAL_REFUND", "COMPLETION", "ARBITRATION"],
          description: "Requested resolution outcome"
        }
      },
      required: ["dealId", "reason", "description"]
    }
  },
  {
    name: "parler_dispute_list",
    description: "List disputes you're involved in as claimant, respondent, or arbitrator.",
    inputSchema: {
      type: "object",
      properties: {
        status: {
          type: "string",
          enum: ["OPEN", "IN_REVIEW", "RESOLVED", "ESCALATED"],
          description: "Filter by status"
        },
        role: {
          type: "string",
          enum: ["CLAIMANT", "RESPONDENT", "ARBITRATOR"],
          description: "Filter by your role"
        },
        limit: {
          type: "number",
          description: "Max disputes to return",
          default: 20
        }
      }
    }
  },
  {
    name: "parler_proposals",
    description: "List resolution proposals for a dispute.",
    inputSchema: {
      type: "object",
      properties: {
        disputeId: {
          type: "string",
          description: "Dispute ID"
        }
      },
      required: ["disputeId"]
    }
  },
  {
    name: "parler_vote",
    description: "Vote on a resolution proposal. Requires arbitrator role for binding votes.",
    inputSchema: {
      type: "object",
      properties: {
        proposalId: {
          type: "string",
          description: "Proposal ID to vote on"
        },
        vote: {
          type: "string",
          enum: ["APPROVE", "REJECT", "ABSTAIN"],
          description: "Your vote"
        },
        comment: {
          type: "string",
          description: "Optional comment explaining your vote"
        }
      },
      required: ["proposalId", "vote"]
    }
  }
];
async function handleParlerTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "parler_dispute_file": {
      const input = ParlerDisputeFileInputSchema.parse(args);
      return client.fetch("parler", "/disputes", {
        method: "POST",
        body: input,
        idempotencyKey: `dispute-${input.dealId}-${Date.now()}`
      });
    }
    case "parler_dispute_list": {
      const input = ParlerDisputeListInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.status) params.set("status", input.status);
      if (input.role) params.set("role", input.role);
      params.set("limit", String(input.limit));
      return client.fetch("parler", `/disputes?${params.toString()}`);
    }
    case "parler_proposals": {
      const input = ParlerProposalsInputSchema.parse(args);
      return client.fetch("parler", `/disputes/${input.disputeId}/proposals`);
    }
    case "parler_vote": {
      const input = ParlerVoteInputSchema.parse(args);
      return client.fetch("parler", `/proposals/${input.proposalId}/vote`, {
        method: "POST",
        body: { vote: input.vote, comment: input.comment },
        idempotencyKey: `vote-${input.proposalId}-${Date.now()}`
      });
    }
    default:
      throw new Error(`Unknown parler tool: ${name}`);
  }
}

// src/engines/academy.ts
import { z as z7 } from "zod";
var AcademyCoursesInputSchema = z7.object({
  category: z7.enum(["DEALS", "FINANCE", "LEGAL", "AGENTS", "BLOCKCHAIN"]).optional(),
  level: z7.enum(["BEGINNER", "INTERMEDIATE", "ADVANCED"]).optional(),
  limit: z7.number().min(1).max(100).default(20)
});
var AcademyEnrollInputSchema = z7.object({
  courseId: z7.string().min(1)
});
var AcademyTipInputSchema = z7.object({
  courseId: z7.string().min(1),
  amount: z7.number().positive(),
  message: z7.string().max(500).optional()
});
var academyTools = [
  {
    name: "academy_courses",
    description: "Browse available courses on the Academy platform.",
    inputSchema: {
      type: "object",
      properties: {
        category: {
          type: "string",
          enum: ["DEALS", "FINANCE", "LEGAL", "AGENTS", "BLOCKCHAIN"],
          description: "Filter by category"
        },
        level: {
          type: "string",
          enum: ["BEGINNER", "INTERMEDIATE", "ADVANCED"],
          description: "Filter by difficulty level"
        },
        limit: {
          type: "number",
          description: "Max courses to return",
          default: 20
        }
      }
    }
  },
  {
    name: "academy_enroll",
    description: "Enroll in a course. Some courses may require payment.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: {
          type: "string",
          description: "Course ID to enroll in"
        }
      },
      required: ["courseId"]
    }
  },
  {
    name: "academy_tip",
    description: "Tip a course creator to show appreciation.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: {
          type: "string",
          description: "Course ID"
        },
        amount: {
          type: "number",
          description: "Tip amount in Talers"
        },
        message: {
          type: "string",
          description: "Optional thank-you message"
        }
      },
      required: ["courseId", "amount"]
    }
  }
];
async function handleAcademyTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "academy_courses": {
      const input = AcademyCoursesInputSchema.parse(args);
      const params = new URLSearchParams();
      if (input.category) params.set("category", input.category);
      if (input.level) params.set("level", input.level);
      params.set("limit", String(input.limit));
      return client.fetch("academy", `/courses?${params.toString()}`);
    }
    case "academy_enroll": {
      const input = AcademyEnrollInputSchema.parse(args);
      return client.fetch("academy", `/courses/${input.courseId}/enroll`, {
        method: "POST",
        idempotencyKey: `enroll-${input.courseId}-${Date.now()}`
      });
    }
    case "academy_tip": {
      const input = AcademyTipInputSchema.parse(args);
      return client.fetch("academy", `/courses/${input.courseId}/tip`, {
        method: "POST",
        body: { amount: input.amount, message: input.message },
        idempotencyKey: `tip-${input.courseId}-${Date.now()}`
      });
    }
    default:
      throw new Error(`Unknown academy tool: ${name}`);
  }
}

// src/engines/hq.ts
import { z as z8 } from "zod";
var HqDashboardInputSchema = z8.object({
  period: z8.enum(["DAY", "WEEK", "MONTH", "QUARTER"]).default("WEEK")
});
var HqHealthInputSchema = z8.object({
  detailed: z8.boolean().default(false)
});
var hqTools = [
  {
    name: "hq_dashboard",
    description: "Get dashboard metrics including deal volume, transaction totals, and agent activity.",
    inputSchema: {
      type: "object",
      properties: {
        period: {
          type: "string",
          enum: ["DAY", "WEEK", "MONTH", "QUARTER"],
          description: "Time period for metrics",
          default: "WEEK"
        }
      }
    }
  },
  {
    name: "hq_health",
    description: "Check system health status across all engines.",
    inputSchema: {
      type: "object",
      properties: {
        detailed: {
          type: "boolean",
          description: "Include detailed per-service metrics",
          default: false
        }
      }
    }
  }
];
async function handleHqTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "hq_dashboard": {
      const input = HqDashboardInputSchema.parse(args);
      return client.fetch("hq", `/dashboard?period=${input.period}`);
    }
    case "hq_health": {
      const input = HqHealthInputSchema.parse(args);
      const params = input.detailed ? "?detailed=true" : "";
      return client.fetch("hq", `/health${params}`);
    }
    default:
      throw new Error(`Unknown hq tool: ${name}`);
  }
}

// src/engines/clause.ts
import { z as z9 } from "zod";
var ClauseRenderInputSchema = z9.object({
  templateId: z9.string().min(1),
  variables: z9.record(z9.union([z9.string(), z9.number(), z9.boolean()])),
  format: z9.enum(["HTML", "MARKDOWN", "PLAIN"]).default("MARKDOWN")
});
var clauseTools = [
  {
    name: "clause_render",
    description: "Render a contract clause template with provided variables. Returns formatted text.",
    inputSchema: {
      type: "object",
      properties: {
        templateId: {
          type: "string",
          description: "Clause template ID"
        },
        variables: {
          type: "object",
          description: "Variables to substitute in the template",
          additionalProperties: {
            oneOf: [
              { type: "string" },
              { type: "number" },
              { type: "boolean" }
            ]
          }
        },
        format: {
          type: "string",
          enum: ["HTML", "MARKDOWN", "PLAIN"],
          description: "Output format",
          default: "MARKDOWN"
        }
      },
      required: ["templateId", "variables"]
    }
  }
];
async function handleClauseTool(name, args) {
  const client = getEngineClient();
  switch (name) {
    case "clause_render": {
      const input = ClauseRenderInputSchema.parse(args);
      return client.fetch("clause", "/render", {
        method: "POST",
        body: input
      });
    }
    default:
      throw new Error(`Unknown clause tool: ${name}`);
  }
}

// src/resources.ts
var resources = [
  {
    uri: "dealworks://profile",
    name: "User Profile",
    description: "Current user's profile including trust tier, verification status, and preferences",
    mimeType: "application/json"
  },
  {
    uri: "dealworks://wallet",
    name: "Wallet Summary",
    description: "Wallet balances across all currencies including locked/available breakdown",
    mimeType: "application/json"
  },
  {
    uri: "dealworks://deals",
    name: "Active Deals",
    description: "List of active deals with summary status",
    mimeType: "application/json"
  },
  {
    uri: "dealworks://agents",
    name: "Deployed Agents",
    description: "List of deployed agents with health status",
    mimeType: "application/json"
  },
  {
    uri: "dealworks://templates",
    name: "Deal Templates",
    description: "Available deal templates from Bourse",
    mimeType: "application/json"
  },
  {
    uri: "dealworks://disputes",
    name: "Open Disputes",
    description: "Active disputes requiring attention",
    mimeType: "application/json"
  },
  {
    uri: "dealworks://dashboard",
    name: "Dashboard Metrics",
    description: "Key metrics and KPIs from HQ dashboard",
    mimeType: "application/json"
  }
];
async function readResource(uri) {
  const client = getEngineClient();
  switch (uri) {
    case "dealworks://profile": {
      const result = await client.fetch("hq", "/users/me/profile");
      return JSON.stringify(result.data ?? result, null, 2);
    }
    case "dealworks://wallet": {
      const result = await client.fetch("fund", "/wallets/me/summary");
      return JSON.stringify(result.data ?? result, null, 2);
    }
    case "dealworks://deals": {
      const result = await client.fetch("deal", "/deals?status=ACTIVE&limit=50");
      return JSON.stringify(result.data ?? result, null, 2);
    }
    case "dealworks://agents": {
      const result = await client.fetch("cadre", "/agents?status=RUNNING&limit=50");
      return JSON.stringify(result.data ?? result, null, 2);
    }
    case "dealworks://templates": {
      const result = await client.fetch("bourse", "/listings?category=TEMPLATE&limit=50");
      return JSON.stringify(result.data ?? result, null, 2);
    }
    case "dealworks://disputes": {
      const result = await client.fetch("parler", "/disputes?status=OPEN&limit=20");
      return JSON.stringify(result.data ?? result, null, 2);
    }
    case "dealworks://dashboard": {
      const result = await client.fetch("hq", "/dashboard?period=WEEK");
      return JSON.stringify(result.data ?? result, null, 2);
    }
    default:
      throw new Error(`Unknown resource: ${uri}`);
  }
}

// src/prompts.ts
var prompts = [
  {
    name: "escrow-deal",
    description: "Create a deal with escrow protection. Guides through deal creation, escrow funding, and attestation.",
    arguments: [
      {
        name: "counterparty",
        description: "Email or user ID of the counterparty",
        required: true
      },
      {
        name: "amount",
        description: "Deal amount to escrow",
        required: true
      },
      {
        name: "description",
        description: "Brief description of the deal",
        required: true
      }
    ]
  },
  {
    name: "deploy-agent",
    description: "Deploy an autonomous agent from a skill. Includes funding and SLA configuration.",
    arguments: [
      {
        name: "skill",
        description: "Skill name or ID to deploy",
        required: true
      },
      {
        name: "budget",
        description: "Maximum budget in Talers",
        required: true
      }
    ]
  },
  {
    name: "file-dispute",
    description: "File a dispute against a deal with evidence collection.",
    arguments: [
      {
        name: "dealId",
        description: "Deal ID to dispute",
        required: true
      },
      {
        name: "reason",
        description: "Brief reason for the dispute",
        required: true
      }
    ]
  },
  {
    name: "publish-template",
    description: "Publish a deal template to the Bourse marketplace.",
    arguments: [
      {
        name: "name",
        description: "Template name",
        required: true
      },
      {
        name: "category",
        description: "Template category (e.g., 'freelance', 'real-estate', 'consulting')",
        required: true
      }
    ]
  },
  {
    name: "portfolio-review",
    description: "Review your deal portfolio including active deals, pending escrows, and agent performance.",
    arguments: []
  }
];
function getPromptMessages(name, args) {
  switch (name) {
    case "escrow-deal":
      return [
        {
          role: "user",
          content: `I want to create an escrow-protected deal with ${args.counterparty} for ${args.amount} Talers.

Description: ${args.description}

Please help me:
1. Create the deal with appropriate terms
2. Set up escrow for the full amount
3. Create an attestation template for completion verification

Use the deal_create, fund_escrow, and oath_attest tools to complete this workflow.`
        }
      ];
    case "deploy-agent":
      return [
        {
          role: "user",
          content: `I want to deploy an agent using the "${args.skill}" skill with a budget of ${args.budget} Talers.

Please help me:
1. Search for the skill in Bourse
2. Deploy the agent with appropriate configuration
3. Fund the agent's wallet
4. Set up SLA monitoring

Use bourse_search, cadre_deploy, and fund_agent_fund tools to complete this workflow.`
        }
      ];
    case "file-dispute":
      return [
        {
          role: "user",
          content: `I need to file a dispute for deal ${args.dealId}.

Reason: ${args.reason}

Please help me:
1. Get the deal details first
2. File the dispute with proper categorization
3. List any relevant attestations as evidence
4. Explain the next steps in the resolution process

Use deal_get, oath_verify (for any attestations), and parler_dispute_file tools.`
        }
      ];
    case "publish-template":
      return [
        {
          role: "user",
          content: `I want to publish a deal template called "${args.name}" in the ${args.category} category.

Please help me:
1. Check if similar templates exist in Bourse
2. Create the template structure
3. Publish to the marketplace
4. Explain how others can use it

Use bourse_search and bourse_publish tools.`
        }
      ];
    case "portfolio-review":
      return [
        {
          role: "user",
          content: `Please review my current deal.works portfolio:

1. Show my active deals and their status
2. List any pending escrows with locked amounts
3. Show deployed agents and their health
4. Summarize my wallet balances
5. Flag any items needing attention (SLA violations, expiring deals, etc.)

Use deal_list, fund_balance, cadre_list, cadre_sla_violations, and hq_dashboard tools to compile this review.`
        }
      ];
    default:
      throw new Error(`Unknown prompt: ${name}`);
  }
}

// src/index.ts
var allTools = [
  ...dealTools,
  ...fundTools,
  ...bourseTools,
  ...cadreTools,
  ...oathTools,
  ...parlerTools,
  ...academyTools,
  ...hqTools,
  ...clauseTools
];
var toolHandlers = {
  // Deal tools
  deal_list: handleDealTool,
  deal_create: handleDealTool,
  deal_get: handleDealTool,
  deal_action: handleDealTool,
  deal_search: handleDealTool,
  deal_timeline: handleDealTool,
  deal_attachments: handleDealTool,
  // Fund tools
  fund_balance: handleFundTool,
  fund_transfer: handleFundTool,
  fund_transactions: handleFundTool,
  fund_escrow: handleFundTool,
  fund_cashout: handleFundTool,
  fund_agent_fund: handleFundTool,
  // Bourse tools
  bourse_search: handleBourseTool,
  bourse_get: handleBourseTool,
  bourse_fork: handleBourseTool,
  bourse_publish: handleBourseTool,
  bourse_earnings: handleBourseTool,
  // Cadre tools
  cadre_list: handleCadreTool,
  cadre_deploy: handleCadreTool,
  cadre_command: handleCadreTool,
  cadre_health: handleCadreTool,
  cadre_delegations: handleCadreTool,
  cadre_sla_violations: handleCadreTool,
  // Oath tools
  oath_attest: handleOathTool,
  oath_verify: handleOathTool,
  oath_vault_upload: handleOathTool,
  oath_vault_seal: handleOathTool,
  oath_trust_tier: handleOathTool,
  // Parler tools
  parler_dispute_file: handleParlerTool,
  parler_dispute_list: handleParlerTool,
  parler_proposals: handleParlerTool,
  parler_vote: handleParlerTool,
  // Academy tools
  academy_courses: handleAcademyTool,
  academy_enroll: handleAcademyTool,
  academy_tip: handleAcademyTool,
  // HQ tools
  hq_dashboard: handleHqTool,
  hq_health: handleHqTool,
  // Clause tools
  clause_render: handleClauseTool
};
async function createServer() {
  const server = new Server(
    {
      name: "deal-works-mcp",
      version: "0.1.0"
    },
    {
      capabilities: {
        tools: {},
        resources: {},
        prompts: {}
      }
    }
  );
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: allTools
  }));
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const handler = toolHandlers[name];
    if (!handler) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: `Unknown tool: ${name}` })
          }
        ],
        isError: true
      };
    }
    try {
      const result = await handler(name, args ?? {});
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: errorMessage })
          }
        ],
        isError: true
      };
    }
  });
  server.setRequestHandler(ListResourcesRequestSchema, async () => ({
    resources
  }));
  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const { uri } = request.params;
    try {
      const content = await readResource(uri);
      return {
        contents: [
          {
            uri,
            mimeType: "application/json",
            text: content
          }
        ]
      };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      throw new Error(`Failed to read resource ${uri}: ${errorMessage}`);
    }
  });
  server.setRequestHandler(ListPromptsRequestSchema, async () => ({
    prompts
  }));
  server.setRequestHandler(GetPromptRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const prompt = prompts.find((p) => p.name === name);
    if (!prompt) {
      throw new Error(`Unknown prompt: ${name}`);
    }
    const messages = getPromptMessages(name, args ?? {});
    return {
      description: prompt.description,
      messages: messages.map((m) => ({
        role: m.role,
        content: {
          type: "text",
          text: m.content
        }
      }))
    };
  });
  return server;
}
async function main() {
  if (!process.env.DEAL_WORKS_API_KEY) {
    console.error("Warning: DEAL_WORKS_API_KEY not set. API calls will fail.");
    console.error("Set it via: export DEAL_WORKS_API_KEY=your_key");
  }
  const server = await createServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("deal.works MCP Server running");
  console.error(`Tools: ${allTools.length}`);
  console.error(`Resources: ${resources.length}`);
  console.error(`Prompts: ${prompts.length}`);
}
main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
//# sourceMappingURL=index.js.map