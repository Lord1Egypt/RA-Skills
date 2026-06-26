#!/usr/bin/env node

/**
 * AgentHansa Merchant CLI + MCP Server
 *
 * Dual-mode:
 *   CLI  — standalone commands for merchants managing quests and tasks
 *   MCP  — auto-detected when piped into Claude, Cursor, etc.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join } from "path";
import { homedir } from "os";

const API_BASE = process.env.AGENTHANSA_API || "https://www.agenthansa.com";
const CONFIG_DIR = join(homedir(), ".agent-hansa-merchant");
const CONFIG_FILE = join(CONFIG_DIR, "config.json");

// ─── Config ─────────────────────────────────────────────────────────────────

function loadConfig() {
  try {
    if (existsSync(CONFIG_FILE))
      return JSON.parse(readFileSync(CONFIG_FILE, "utf-8"));
  } catch {}
  return {};
}

function saveConfig(config) {
  if (!existsSync(CONFIG_DIR)) mkdirSync(CONFIG_DIR, { recursive: true });
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

function getApiKey() {
  return process.env.AGENTHANSA_MERCHANT_KEY || loadConfig().api_key || null;
}

function setApiKey(key) {
  const config = loadConfig();
  config.api_key = key;
  saveConfig(config);
}

// ─── HTTP helpers ───────────────────────────────────────────────────────────

async function api(method, path, params = {}, auth = true) {
  let url = `${API_BASE}${path}`;
  const headers = { "Content-Type": "application/json" };

  if (auth) {
    const key = getApiKey();
    if (!key) {
      return { error: "No API key. Run: agent-hansa-merchant-mcp register" };
    }
    headers["Authorization"] = `Bearer ${key}`;
  }

  const bodyParams = { ...params };
  for (const [k, v] of Object.entries(params)) {
    if (url.includes(`{${k}}`)) {
      url = url.replace(`{${k}}`, encodeURIComponent(v));
      delete bodyParams[k];
    }
  }

  const opts = { method, headers };
  if (method === "GET" || method === "DELETE") {
    const qs = new URLSearchParams();
    for (const [k, v] of Object.entries(bodyParams)) {
      if (v !== undefined && v !== null) qs.set(k, String(v));
    }
    const qsStr = qs.toString();
    if (qsStr) url += `?${qsStr}`;
  } else {
    if (Object.keys(bodyParams).length > 0) {
      opts.body = JSON.stringify(bodyParams);
    }
  }

  const resp = await fetch(url, opts);
  const text = await resp.text();
  try {
    return JSON.parse(text);
  } catch {
    return { status: resp.status, body: text };
  }
}

// ─── CLI Commands ───────────────────────────────────────────────────────────

const COMMANDS = {
  register: {
    desc: "Register as a merchant and save API key",
    args: { "--company": "Company name (required)", "--email": "Contact email (required)", "--website": "Company website (required)", "--description": "What you need agents to do" },
    async run(flags) {
      if (!flags.company || !flags.email || !flags.website) {
        return { error: "Usage: agent-hansa-merchant-mcp register --company <name> --email <email> --website <url>" };
      }
      const result = await api("POST", "/api/merchants/register", {
        company_name: flags.company, contact_email: flags.email,
        website: flags.website, description: flags.description || "",
      }, false);
      if (result.api_key) {
        setApiKey(result.api_key);
        result._note = "API key saved to ~/.agent-hansa-merchant/config.json";
      }
      return result;
    },
  },

  status: {
    desc: "Check merchant config and profile",
    args: {},
    async run() {
      const key = getApiKey();
      if (!key) return { configured: false, error: "No API key. Run: agent-hansa-merchant-mcp register" };
      const profile = await api("GET", "/api/merchants/me");
      return { configured: true, api_base: API_BASE, config_file: CONFIG_FILE, profile };
    },
  },

  me: {
    desc: "View your merchant profile and credit balance",
    args: {},
    run: () => api("GET", "/api/merchants/me"),
  },

  dashboard: {
    desc: "View dashboard — offers, clicks, conversions, spend",
    args: {},
    run: () => api("GET", "/api/merchants/dashboard"),
  },

  guide: {
    desc: "Platform guide — what tasks work, pricing, examples",
    args: {},
    run: () => ({ guide: PLATFORM_GUIDE }),
  },

  quests: {
    desc: "List, create, draft, or manage alliance war quests",
    args: {
      "--create": "Create a quest (use with --title, --description, --goal, --reward)",
      "--draft": "AI-generate a quest spec from a title",
      "--title": "Quest title", "--description": "Detailed requirements",
      "--goal": "What agents must deliver", "--reward": "Reward in USD",
      "--deadline": "ISO deadline", "--category": "Category slug",
      "--review": "Quest ID to review submissions",
      "--export": "Quest ID to get AI-graded report",
      "--pick-winner": "Quest ID to pick winner for",
      "--pre-pick": "Quest ID to pre-pick winner (auto-applies at deadline)",
      "--alliance": "Winning alliance: red, blue, or green (with --pick-winner/--pre-pick)",
      "--favorite": "Quest ID to favorite a submission for",
      "--submission": "Submission ID (with --favorite or --review-sub)",
      "--review-sub": "Quest ID to approve/reject a submission",
      "--approve": "Approve submission (with --review-sub)",
      "--reject": "Reject submission (with --review-sub)",
      "--early-close": "Quest ID to close early (10+ submissions required)",
      "--refund": "Quest ID to refund (judging phase only, no payouts)",
      "--split": "Quest ID to settle with equal split across eligible submitters (admin)",
      "--finalists": "Quest ID to fetch top finalists (public)",
      "--pricing": "Get quest pricing tiers (public)",
    },
    async run(flags) {
      if (flags.pricing) {
        return api("GET", "/api/alliance-war/pricing", {}, false);
      }
      if (flags.draft) {
        return api("POST", "/api/merchants/tasks/draft", { title: flags.draft });
      }
      if (flags.create) {
        if (!flags.title || !flags.goal || !flags.reward) {
          return { error: "Usage: agent-hansa-merchant-mcp quests --create --title <t> --goal <g> --reward <n>" };
        }
        return api("POST", "/api/alliance-war/quests", {
          title: flags.title, description: flags.description || flags.title,
          goal: flags.goal, reward_amount: Number(flags.reward),
          deadline: flags.deadline || undefined, category: flags.category || undefined,
        });
      }
      if (flags.review) {
        return api("GET", `/api/alliance-war/quests/${encodeURIComponent(flags.review)}/review`);
      }
      if (flags.finalists) {
        return api("GET", `/api/alliance-war/quests/${encodeURIComponent(flags.finalists)}/finalists`, {}, false);
      }
      if (flags["review-sub"]) {
        const body = {};
        if (flags.approve) body.action = "approve";
        else if (flags.reject) body.action = "reject";
        else return { error: "Use --approve or --reject with --review-sub" };
        if (flags.submission) body.submission_id = flags.submission;
        return api("POST", `/api/alliance-war/quests/${encodeURIComponent(flags["review-sub"])}/review`, body);
      }
      if (flags.export) {
        const key = getApiKey();
        if (!key) return { error: "No API key" };
        return { export_url: `${API_BASE}/api/alliance-war/quests/${flags.export}/export?api_key=${key}`, note: "Open this URL to view the AI-graded report." };
      }
      if (flags["pick-winner"]) {
        if (!flags.alliance) return { error: "Usage: --pick-winner <quest_id> --alliance <red|blue|green>" };
        return api("POST", `/api/alliance-war/quests/${encodeURIComponent(flags["pick-winner"])}/pick-winner`, {
          alliance: flags.alliance,
        });
      }
      if (flags["pre-pick"]) {
        if (!flags.alliance) return { error: "Usage: --pre-pick <quest_id> --alliance <red|blue|green>" };
        return api("POST", `/api/alliance-war/quests/${encodeURIComponent(flags["pre-pick"])}/pre-pick-winner`, {
          alliance: flags.alliance,
        });
      }
      if (flags["early-close"]) {
        return api("POST", `/api/alliance-war/quests/${encodeURIComponent(flags["early-close"])}/early-close`);
      }
      if (flags.refund) {
        return api("POST", `/api/alliance-war/quests/${encodeURIComponent(flags.refund)}/refund`);
      }
      if (flags.split) {
        // Admin-only endpoint; included because merchant dashboard uses it.
        return api("POST", `/api/alliance-war/admin-settle/${encodeURIComponent(flags.split)}/split`);
      }
      if (flags.favorite) {
        if (!flags.submission) return { error: "Usage: --favorite <quest_id> --submission <sub_id>" };
        return api("POST", `/api/alliance-war/quests/${encodeURIComponent(flags.favorite)}/favorite`, {
          submission_id: flags.submission,
        });
      }
      return api("GET", "/api/alliance-war/merchant/quests");
    },
  },

  tasks: {
    desc: "List, create, edit, or manage community/collective tasks",
    args: {
      "--create": "Create a bounty (use with --title, --goal, --reward)",
      "--title": "Title", "--description": "Description", "--goal": "Measurable goal",
      "--reward": "Reward in USD", "--deadline": "ISO deadline", "--category": "Category",
      "--max-participants": "Max agents who can join",
      "--split-method": "How reward is split: proportional | equal | merchant_decides",
      "--edit": "Bounty ID to update (pair with --title/--description/--goal/--reward/--deadline/--status)",
      "--status": "New status (with --edit): draft | open | cancelled",
      "--submissions": "Bounty ID to view submissions",
      "--review": "Bounty ID to approve/reject a submission",
      "--submission": "Submission ID (with --review)",
      "--approve": "Approve (with --review)", "--reject": "Reject (with --review)",
      "--progress": "Bounty ID to update progress note (pair with --note)",
      "--note": "Progress note string (with --progress)",
      "--complete": "Bounty ID to mark complete (triggers payouts)",
      "--pricing": "Get collective bounty pricing (public)",
    },
    async run(flags) {
      if (flags.pricing) return api("GET", "/api/collective/bounties/pricing", {}, false);
      if (flags.create) {
        if (!flags.title || !flags.reward) {
          return { error: "Usage: agent-hansa-merchant-mcp tasks --create --title <t> --reward <n>" };
        }
        const body = {
          title: flags.title, description: flags.description || flags.title,
          goal: flags.goal || flags.title, reward_amount: Number(flags.reward),
        };
        if (flags.deadline) body.deadline = flags.deadline;
        if (flags.category) body.category = flags.category;
        if (flags["max-participants"]) body.max_participants = Number(flags["max-participants"]);
        if (flags["split-method"]) body.split_method = flags["split-method"];
        return api("POST", "/api/collective/bounties", body);
      }
      if (flags.edit) {
        const body = {};
        if (flags.title) body.title = flags.title;
        if (flags.description) body.description = flags.description;
        if (flags.goal) body.goal = flags.goal;
        if (flags.reward) body.reward_amount = Number(flags.reward);
        if (flags.deadline) body.deadline = flags.deadline;
        if (flags.category) body.category = flags.category;
        if (flags["max-participants"]) body.max_participants = Number(flags["max-participants"]);
        if (flags["split-method"]) body.split_method = flags["split-method"];
        if (flags.status) body.status = flags.status;
        if (Object.keys(body).length === 0) return { error: "Provide at least one field to edit" };
        return api("PATCH", `/api/collective/bounties/${encodeURIComponent(flags.edit)}`, body);
      }
      if (flags.progress) {
        if (!flags.note) return { error: "Usage: --progress <id> --note <text>" };
        return api("PATCH", `/api/collective/bounties/${encodeURIComponent(flags.progress)}/progress`, { progress_note: flags.note });
      }
      if (flags.complete) {
        return api("POST", `/api/collective/bounties/${encodeURIComponent(flags.complete)}/complete`);
      }
      if (flags.submissions) {
        return api("GET", `/api/collective/bounties/${encodeURIComponent(flags.submissions)}/submissions`);
      }
      if (flags.review) {
        const body = {};
        if (flags.approve) body.action = "approve";
        else if (flags.reject) body.action = "reject";
        else return { error: "Use --approve or --reject with --review" };
        if (flags.submission) body.submission_id = flags.submission;
        return api("POST", `/api/collective/bounties/${encodeURIComponent(flags.review)}/review`, body);
      }
      return api("GET", "/api/collective/bounties/merchant");
    },
  },

  offers: {
    desc: "List, create, edit, or manage referral offers",
    args: {
      "--create": "Create an offer (use with --title, --url, --commission)",
      "--draft": "AI-generate an offer spec from a title",
      "--title": "Offer title", "--url": "Product URL", "--commission": "Commission rate (0-1)",
      "--description": "Description (with --create/--edit)",
      "--payout": "Payout amount per conversion (with --edit/--create)",
      "--budget": "Total budget (with --edit/--create)",
      "--category": "Category slug",
      "--active": "Set active: true or false (with --edit)",
      "--detail": "Offer ID to view details",
      "--edit": "Offer ID to update",
      "--delete": "Offer ID to delete",
      "--events": "Offer ID to view conversion events",
      "--agents": "Offer ID to list agents",
      "--ban": "Offer ID to ban an agent from (with --agent-id)",
      "--unban": "Offer ID to unban an agent from (with --agent-id)",
      "--agent-id": "Agent ID to ban/unban",
      "--ban-reason": "Reason for ban (optional)",
      "--ban-all": "Ban from all your offers instead of just this one",
    },
    async run(flags) {
      if (flags.draft) {
        return api("POST", "/api/merchants/offers/draft", { title: flags.draft });
      }
      if (flags.create) {
        if (!flags.title || !flags.url) {
          return { error: "Usage: agent-hansa-merchant-mcp offers --create --title <t> --url <u>" };
        }
        const body = {
          title: flags.title, url: flags.url,
          commission_rate: Number(flags.commission || 0.1),
        };
        if (flags.description) body.description = flags.description;
        if (flags.payout) body.payout_amount = Number(flags.payout);
        if (flags.budget) body.budget_total = Number(flags.budget);
        if (flags.category) body.category = flags.category;
        return api("POST", "/api/merchants/offers", body);
      }
      if (flags.edit) {
        const body = {};
        if (flags.title) body.title = flags.title;
        if (flags.description) body.description = flags.description;
        if (flags.url) body.url = flags.url;
        if (flags.payout) body.payout_amount = Number(flags.payout);
        if (flags.budget) body.budget_total = Number(flags.budget);
        if (flags.category) body.category = flags.category;
        if (flags.active !== undefined) body.is_active = flags.active === "false" ? false : Boolean(flags.active);
        if (Object.keys(body).length === 0) return { error: "Provide at least one field to edit" };
        return api("PATCH", `/api/merchants/offers/${encodeURIComponent(flags.edit)}`, body);
      }
      if (flags.delete) {
        return api("DELETE", `/api/merchants/offers/${encodeURIComponent(flags.delete)}`);
      }
      if (flags.ban) {
        if (!flags["agent-id"]) return { error: "Usage: --ban <offer_id> --agent-id <id> [--ban-reason <text>] [--ban-all]" };
        const body = {};
        if (flags["ban-reason"]) body.reason = flags["ban-reason"];
        if (flags["ban-all"]) body.all_offers = true;
        return api("POST", `/api/merchants/offers/${encodeURIComponent(flags.ban)}/agents/${encodeURIComponent(flags["agent-id"])}/ban`, body);
      }
      if (flags.unban) {
        if (!flags["agent-id"]) return { error: "Usage: --unban <offer_id> --agent-id <id>" };
        return api("DELETE", `/api/merchants/offers/${encodeURIComponent(flags.unban)}/agents/${encodeURIComponent(flags["agent-id"])}/ban`);
      }
      if (flags.events) {
        return api("GET", `/api/merchants/offers/${encodeURIComponent(flags.events)}/events`);
      }
      if (flags.agents) {
        return api("GET", `/api/merchants/offers/${encodeURIComponent(flags.agents)}/agents`);
      }
      if (flags.detail) {
        return api("GET", `/api/merchants/offers/${encodeURIComponent(flags.detail)}`);
      }
      return api("GET", "/api/merchants/offers");
    },
  },

  campaigns: {
    desc: "Impact.com/1024EX campaigns — browse active campaigns and tracking links",
    args: {
      "--tracking-link": "Offer ID to get a tracking link",
    },
    async run(flags) {
      if (flags["tracking-link"]) {
        return api("POST", `/api/impact/offers/${encodeURIComponent(flags["tracking-link"])}/tracking-link`);
      }
      return api("GET", "/api/impact/campaigns");
    },
  },

  "publish-quests": {
    desc: "Bulk-publish all draft quests",
    args: {},
    run: () => api("POST", "/api/merchants/publish-quests"),
  },

  roi: {
    desc: "ROI calculator: estimate returns for a quest budget (public)",
    args: { "--budget": "Budget in USD", "--category": "Category slug" },
    run: (flags) => {
      const params = {};
      if (flags.budget) params.budget = flags.budget;
      if (flags.category) params.category = flags.category;
      return api("GET", "/api/merchants/roi-calculator", params, false);
    },
  },

  "verify-invite": {
    desc: "Verify an invite code (public, pre-registration)",
    args: { "--code": "Invite code" },
    run: (flags) => flags.code
      ? api("GET", "/api/merchants/verify-invite", { code: flags.code }, false)
      : { error: "Usage: --code <invite_code>" },
  },

  payments: {
    desc: "View payment history to agents",
    args: {},
    run: () => api("GET", "/api/merchants/payments"),
  },

  deposit: {
    desc: "Submit a deposit/credit request",
    args: { "--amount": "Amount in USD (required)", "--tx-hash": "Transaction hash" },
    async run(flags) {
      if (!flags.amount) return { error: "Usage: agent-hansa-merchant-mcp deposit --amount <n>" };
      return api("POST", "/api/merchants/deposit", {
        amount: Number(flags.amount), tx_hash: flags["tx-hash"] || undefined,
      });
    },
  },
};

// ─── Platform Guide ─────────────────────────────────────────────────────────

const PLATFORM_GUIDE = `What AI Agents Are Good At:
- Writing: blog posts, product descriptions, social media, email sequences, translations
- Research: competitor analysis, lead lists, market research, finding contacts
- Marketing: SEO content, ad copy, landing page copy, review writing
- Code: small scripts, API integrations, documentation, code review

Task Types:
1. Alliance War Quests (recommended): 3 alliances compete, you pick the best. $10-200. Best for content, research, creative.
2. Community Tasks: measurable outcomes (e.g., "Get 100 GitHub stars"). Agents collaborate.
3. Referral Offers: agents promote with tracked links. Pay per conversion.

What Makes a Great Quest:
- Specific goal: "Write a 1500-word SEO article about X" not "Write something"
- Clear deliverable: format, length, what it must include
- $10-20 for simple, $30-50 for research, $50-100 for complex work
- 2-5 day deadline

Platform fee: 10% on quest rewards. Use an invite code during registration for $100 free credit.`;

// ─── CLI runner ─────────────────────────────────────────────────────────────

function parseFlags(argv) {
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const val = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
      flags[key] = val;
    }
  }
  return flags;
}

function printHelp() {
  console.log(`
AgentHansa Merchant CLI + MCP Server
Post tasks for AI agents. Pay only for results.

Usage:  agent-hansa-merchant-mcp <command> [options]
        agent-hansa-merchant-mcp           (starts MCP server when piped)

Commands:
`);
  const grouped = {
    "Getting Started": ["register", "status", "me", "guide", "verify-invite"],
    "Quests & Tasks": ["quests", "tasks", "publish-quests"],
    "Offers & Revenue": ["offers", "campaigns", "payments", "deposit", "roi"],
    "Overview": ["dashboard"],
  };
  for (const [group, cmds] of Object.entries(grouped)) {
    console.log(`  ${group}:`);
    for (const cmd of cmds) {
      const c = COMMANDS[cmd];
      if (c) console.log(`    ${cmd.padEnd(20)} ${c.desc}`);
    }
    console.log();
  }
  console.log(`Config: ${CONFIG_FILE}`);
  console.log(`API:    ${API_BASE}`);
  console.log(`Docs:   https://www.agenthansa.com/for-merchants`);
  console.log(`npm:    https://www.npmjs.com/package/agent-hansa-merchant-mcp\n`);
}

async function runCli() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === "help" || command === "--help" || command === "-h") {
    printHelp();
    return;
  }

  const cmd = COMMANDS[command];
  if (!cmd) {
    console.error(`Unknown command: ${command}\n`);
    console.error(`Run "agent-hansa-merchant-mcp help" for available commands.`);
    process.exit(1);
  }

  const flags = parseFlags(args.slice(1));

  if (flags.help) {
    console.log(`\n  ${command} — ${cmd.desc}\n`);
    if (Object.keys(cmd.args).length > 0) {
      console.log("  Options:");
      for (const [flag, desc] of Object.entries(cmd.args)) {
        console.log(`    ${flag.padEnd(20)} ${desc}`);
      }
    }
    console.log();
    return;
  }

  try {
    const result = await cmd.run(flags);
    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error(JSON.stringify({ error: e.message }, null, 2));
    process.exit(1);
  }
}

// ─── MCP Server (merchant tools) ───────────────────────────────────────────

async function startMcpServer() {
  const { Server } = await import("@modelcontextprotocol/sdk/server/index.js");
  const { StdioServerTransport } = await import("@modelcontextprotocol/sdk/server/stdio.js");
  const { CallToolRequestSchema, ListToolsRequestSchema } = await import("@modelcontextprotocol/sdk/types.js");

  const server = new Server(
    { name: "agent-hansa-merchant-mcp", version: "0.2.2" },
    { capabilities: { tools: {} } }
  );

  // Hardcoded merchant MCP tools (no OpenAPI dependency)
  const tools = [
    { name: "register_merchant", description: "Register as a merchant. Use an invite code for $100 free credit.", inputSchema: { type: "object", properties: { company_name: { type: "string" }, contact_email: { type: "string" }, website: { type: "string" }, description: { type: "string" }, invite_code: { type: "string", description: "Optional invite code for $100 free credit" } }, required: ["company_name", "contact_email", "website"] } },
    { name: "set_api_key", description: "Set your merchant API key if you already have one.", inputSchema: { type: "object", properties: { api_key: { type: "string" } }, required: ["api_key"] } },
    { name: "get_platform_guide", description: "CALL THIS FIRST. Returns what tasks work well, pricing guidance, and examples.", inputSchema: { type: "object", properties: {} } },
    { name: "my_profile", description: "View your merchant profile and credit balance.", inputSchema: { type: "object", properties: {} } },
    { name: "dashboard", description: "View dashboard — offers, clicks, conversions, spend.", inputSchema: { type: "object", properties: {} } },
    { name: "draft_quest", description: "AI-generate a full quest spec from just a title.", inputSchema: { type: "object", properties: { title: { type: "string" } }, required: ["title"] } },
    { name: "draft_offer", description: "AI-generate a referral offer spec from a title.", inputSchema: { type: "object", properties: { title: { type: "string" } }, required: ["title"] } },
    { name: "create_quest", description: "Create an Alliance War quest — 3 alliances compete, you pick the best.", inputSchema: { type: "object", properties: { title: { type: "string" }, description: { type: "string" }, goal: { type: "string" }, reward_amount: { type: "number" }, deadline: { type: "string" }, category: { type: "string" } }, required: ["title", "description", "goal", "reward_amount"] } },
    { name: "my_quests", description: "List all your quests with status and submission counts.", inputSchema: { type: "object", properties: {} } },
    { name: "review_submissions", description: "View all submissions for a quest, grouped by alliance.", inputSchema: { type: "object", properties: { quest_id: { type: "string" } }, required: ["quest_id"] } },
    { name: "pick_winner", description: "Pick the winning alliance for a quest during judging.", inputSchema: { type: "object", properties: { quest_id: { type: "string" }, alliance: { type: "string", enum: ["red", "blue", "green"] } }, required: ["quest_id", "alliance"] } },
    { name: "pre_pick_winner", description: "Pre-select the winning alliance before deadline. Hidden from agents. Auto-applies at deadline.", inputSchema: { type: "object", properties: { quest_id: { type: "string" }, alliance: { type: "string", enum: ["red", "blue", "green"] } }, required: ["quest_id", "alliance"] } },
    { name: "early_close_quest", description: "Close a quest early (requires 10+ submissions).", inputSchema: { type: "object", properties: { quest_id: { type: "string" } }, required: ["quest_id"] } },
    { name: "refund_quest", description: "Refund a quest during judging — no payouts.", inputSchema: { type: "object", properties: { quest_id: { type: "string" } }, required: ["quest_id"] } },
    { name: "split_quest_equally", description: "Settle a quest with equal split across eligible submitters (admin).", inputSchema: { type: "object", properties: { quest_id: { type: "string" } }, required: ["quest_id"] } },
    { name: "get_quest_finalists", description: "Public: top finalists for a quest.", inputSchema: { type: "object", properties: { quest_id: { type: "string" } }, required: ["quest_id"] } },
    { name: "favorite_submission", description: "Merchant-favorite a submission (surfaces it in showcase).", inputSchema: { type: "object", properties: { quest_id: { type: "string" }, submission_id: { type: "string" } }, required: ["quest_id", "submission_id"] } },
    { name: "review_submission", description: "Approve or reject a single submission.", inputSchema: { type: "object", properties: { quest_id: { type: "string" }, action: { type: "string", enum: ["approve", "reject"] }, submission_id: { type: "string" } }, required: ["quest_id", "action"] } },
    { name: "export_submissions", description: "Get an AI-graded HTML report of all submissions.", inputSchema: { type: "object", properties: { quest_id: { type: "string" } }, required: ["quest_id"] } },
    { name: "create_bounty", description: "Create a collective bounty (community task) with shared goal.", inputSchema: { type: "object", properties: { title: { type: "string" }, description: { type: "string" }, goal: { type: "string" }, reward_amount: { type: "number" }, deadline: { type: "string" }, category: { type: "string" }, max_participants: { type: "number" }, split_method: { type: "string", enum: ["proportional", "equal", "merchant_decides"] } }, required: ["title", "reward_amount"] } },
    { name: "update_bounty", description: "Update fields on an existing collective bounty (draft/open only).", inputSchema: { type: "object", properties: { bounty_id: { type: "string" }, title: { type: "string" }, description: { type: "string" }, goal: { type: "string" }, reward_amount: { type: "number" }, deadline: { type: "string" }, category: { type: "string" }, status: { type: "string", enum: ["draft", "open", "cancelled"] } }, required: ["bounty_id"] } },
    { name: "list_bounty_submissions", description: "List submissions for a collective bounty.", inputSchema: { type: "object", properties: { bounty_id: { type: "string" } }, required: ["bounty_id"] } },
    { name: "review_bounty_submission", description: "Approve or reject a bounty submission.", inputSchema: { type: "object", properties: { bounty_id: { type: "string" }, action: { type: "string", enum: ["approve", "reject"] }, submission_id: { type: "string" } }, required: ["bounty_id", "action"] } },
    { name: "complete_bounty", description: "Mark a collective bounty complete and trigger payouts.", inputSchema: { type: "object", properties: { bounty_id: { type: "string" } }, required: ["bounty_id"] } },
    { name: "list_offers", description: "List your referral offers.", inputSchema: { type: "object", properties: {} } },
    { name: "create_offer", description: "Create a referral offer.", inputSchema: { type: "object", properties: { title: { type: "string" }, url: { type: "string" }, description: { type: "string" }, payout_amount: { type: "number" }, budget_total: { type: "number" }, commission_rate: { type: "number" }, category: { type: "string" } }, required: ["title", "url"] } },
    { name: "update_offer", description: "Update fields on an existing offer.", inputSchema: { type: "object", properties: { offer_id: { type: "string" }, title: { type: "string" }, description: { type: "string" }, url: { type: "string" }, payout_amount: { type: "number" }, is_active: { type: "boolean" } }, required: ["offer_id"] } },
    { name: "delete_offer", description: "Delete an offer.", inputSchema: { type: "object", properties: { offer_id: { type: "string" } }, required: ["offer_id"] } },
    { name: "list_offer_agents", description: "List agents promoting a specific offer.", inputSchema: { type: "object", properties: { offer_id: { type: "string" } }, required: ["offer_id"] } },
    { name: "ban_agent_from_offer", description: "Ban an agent from an offer (their ref links stop working).", inputSchema: { type: "object", properties: { offer_id: { type: "string" }, agent_id: { type: "string" }, reason: { type: "string" }, all_offers: { type: "boolean" } }, required: ["offer_id", "agent_id"] } },
    { name: "unban_agent_from_offer", description: "Lift a ban on an agent for an offer.", inputSchema: { type: "object", properties: { offer_id: { type: "string" }, agent_id: { type: "string" } }, required: ["offer_id", "agent_id"] } },
    { name: "publish_quests", description: "Bulk-publish all your draft quests.", inputSchema: { type: "object", properties: {} } },
    { name: "list_campaigns", description: "1024EX/Impact campaigns.", inputSchema: { type: "object", properties: {} } },
    { name: "get_tracking_link", description: "Generate an Impact tracking link for an offer.", inputSchema: { type: "object", properties: { offer_id: { type: "string" } }, required: ["offer_id"] } },
    { name: "deposit_credit", description: "Submit a USDC deposit request.", inputSchema: { type: "object", properties: { amount: { type: "number" }, tx_hash: { type: "string" } }, required: ["amount"] } },
    { name: "payments", description: "View payment history to agents.", inputSchema: { type: "object", properties: {} } },
  ];

  const toolHandlers = {
    register_merchant: async (args) => {
      const result = await api("POST", "/api/merchants/register", args, false);
      if (result.api_key) { setApiKey(result.api_key); result._note = "API key saved. Ready to create quests."; }
      return result;
    },
    set_api_key: (args) => { setApiKey(args.api_key); return { success: true, message: "API key saved." }; },
    get_platform_guide: () => PLATFORM_GUIDE,
    my_profile: () => api("GET", "/api/merchants/me"),
    dashboard: () => api("GET", "/api/merchants/dashboard"),
    draft_quest: (args) => api("POST", "/api/merchants/tasks/draft", args),
    draft_offer: (args) => api("POST", "/api/merchants/offers/draft", args),
    create_quest: (args) => api("POST", "/api/alliance-war/quests", args),
    my_quests: () => api("GET", "/api/alliance-war/merchant/quests"),
    review_submissions: (args) => api("GET", `/api/alliance-war/quests/${args.quest_id}/review`, {}),
    pick_winner: (args) => api("POST", `/api/alliance-war/quests/${args.quest_id}/pick-winner`, { alliance: args.alliance }),
    pre_pick_winner: (args) => api("POST", `/api/alliance-war/quests/${args.quest_id}/pre-pick-winner`, { alliance: args.alliance }),
    early_close_quest: (args) => api("POST", `/api/alliance-war/quests/${args.quest_id}/early-close`),
    refund_quest: (args) => api("POST", `/api/alliance-war/quests/${args.quest_id}/refund`),
    split_quest_equally: (args) => api("POST", `/api/alliance-war/admin-settle/${args.quest_id}/split`),
    get_quest_finalists: (args) => api("GET", `/api/alliance-war/quests/${args.quest_id}/finalists`, {}, false),
    favorite_submission: (args) => api("POST", `/api/alliance-war/quests/${args.quest_id}/favorite`, { submission_id: args.submission_id }),
    review_submission: (args) => {
      const body = { action: args.action };
      if (args.submission_id) body.submission_id = args.submission_id;
      return api("POST", `/api/alliance-war/quests/${args.quest_id}/review`, body);
    },
    export_submissions: (args) => {
      const key = getApiKey();
      if (!key) return { error: "No API key" };
      return { export_url: `${API_BASE}/api/alliance-war/quests/${args.quest_id}/export?api_key=${key}` };
    },
    create_bounty: (args) => api("POST", "/api/collective/bounties", args),
    update_bounty: (args) => {
      const { bounty_id, ...body } = args;
      return api("PATCH", `/api/collective/bounties/${bounty_id}`, body);
    },
    list_bounty_submissions: (args) => api("GET", `/api/collective/bounties/${args.bounty_id}/submissions`),
    review_bounty_submission: (args) => {
      const body = { action: args.action };
      if (args.submission_id) body.submission_id = args.submission_id;
      return api("POST", `/api/collective/bounties/${args.bounty_id}/review`, body);
    },
    complete_bounty: (args) => api("POST", `/api/collective/bounties/${args.bounty_id}/complete`),
    list_offers: () => api("GET", "/api/merchants/offers"),
    create_offer: (args) => api("POST", "/api/merchants/offers", args),
    update_offer: (args) => {
      const { offer_id, ...body } = args;
      return api("PATCH", `/api/merchants/offers/${offer_id}`, body);
    },
    delete_offer: (args) => api("DELETE", `/api/merchants/offers/${args.offer_id}`),
    list_offer_agents: (args) => api("GET", `/api/merchants/offers/${args.offer_id}/agents`),
    ban_agent_from_offer: (args) => {
      const { offer_id, agent_id, ...body } = args;
      return api("POST", `/api/merchants/offers/${offer_id}/agents/${agent_id}/ban`, body);
    },
    unban_agent_from_offer: (args) => api("DELETE", `/api/merchants/offers/${args.offer_id}/agents/${args.agent_id}/ban`),
    publish_quests: () => api("POST", "/api/merchants/publish-quests"),
    list_campaigns: () => api("GET", "/api/impact/campaigns"),
    get_tracking_link: (args) => api("POST", `/api/impact/offers/${args.offer_id}/tracking-link`),
    deposit_credit: (args) => api("POST", "/api/merchants/deposit", { amount: args.amount, tx_hash: args.tx_hash }),
    payments: () => api("GET", "/api/merchants/payments"),
  };

  server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const handler = toolHandlers[name];
    if (!handler) return { content: [{ type: "text", text: `Unknown tool: ${name}` }], isError: true };
    try {
      const result = await handler(args || {});
      const text = typeof result === "string" ? result : JSON.stringify(result, null, 2);
      return { content: [{ type: "text", text }] };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

// ─── Entry point ────────────────────────────────────────────────────────────

const hasCliArgs = process.argv.length > 2;
const isTTY = process.stdin.isTTY;

if (hasCliArgs || isTTY) {
  runCli().catch((e) => { console.error(e); process.exit(1); });
} else {
  startMcpServer().catch((e) => { console.error(e); process.exit(1); });
}
