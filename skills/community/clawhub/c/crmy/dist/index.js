// src/client.ts
import fs from "fs";
import os from "os";
import path from "path";
function resolveConfig(pluginConfig) {
  let fileConfig = {};
  try {
    const raw = fs.readFileSync(path.join(os.homedir(), ".crmy", "config.json"), "utf-8");
    fileConfig = JSON.parse(raw);
  } catch {
  }
  const serverUrl = pluginConfig?.serverUrl ?? process.env.CRMY_SERVER_URL ?? fileConfig.serverUrl ?? "http://localhost:3000";
  const apiKey = pluginConfig?.apiKey ?? process.env.CRMY_API_KEY ?? fileConfig.apiKey ?? "";
  return { serverUrl: serverUrl.replace(/\/$/, ""), apiKey };
}
var CrmyClient = class {
  base;
  headers;
  constructor(cfg) {
    this.base = `${cfg.serverUrl}/api/v1`;
    this.headers = {
      "Authorization": `Bearer ${cfg.apiKey}`,
      "Content-Type": "application/json"
    };
  }
  async get(endpoint, params) {
    const url = new URL(`${this.base}${endpoint}`);
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v !== void 0 && v !== null && v !== "") {
          url.searchParams.set(k, String(v));
        }
      }
    }
    const res = await fetch(url.toString(), { headers: this.headers });
    return this.parse(res);
  }
  async post(endpoint, body) {
    const res = await fetch(`${this.base}${endpoint}`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(body)
    });
    return this.parse(res);
  }
  async patch(endpoint, body) {
    const res = await fetch(`${this.base}${endpoint}`, {
      method: "PATCH",
      headers: this.headers,
      body: JSON.stringify(body)
    });
    return this.parse(res);
  }
  async parse(res) {
    const text = await res.text();
    if (!res.ok) {
      let msg = text;
      try {
        const j = JSON.parse(text);
        msg = j.error ?? j.message ?? text;
      } catch {
      }
      throw new Error(`CRMy API error ${res.status}: ${msg}`);
    }
    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  }
};

// src/index.ts
var index_default = (api) => {
  const cfg = resolveConfig(api.config);
  const client = new CrmyClient(cfg);
  api.registerTool({
    id: "crmy_search",
    name: "CRMy: Search",
    description: "Search across all CRMy records \u2014 contacts, accounts, opportunities, activities, and more. Use this as a first step when you are not sure which record type the user is referring to.",
    input: {
      type: "object",
      properties: {
        q: { type: "string", description: "Search query" },
        limit: { type: "number", description: "Max results (default 10)" }
      },
      required: ["q"]
    },
    handler: async (input) => client.get("/search", { q: input.q, limit: input.limit ?? 10 })
  });
  api.registerTool({
    id: "crmy_contact_search",
    name: "CRMy: Search Contacts",
    description: "Search for contacts by name, email, company, or any keyword. Supports optional lifecycle stage filter.",
    input: {
      type: "object",
      properties: {
        q: { type: "string", description: "Search query (name, email, company, etc.)" },
        stage: { type: "string", description: "Filter by lifecycle stage (e.g. prospect, customer, churned)" },
        limit: { type: "number", description: "Max results (default 20)" }
      },
      required: ["q"]
    },
    handler: async (input) => client.get("/contacts", { q: input.q, stage: input.stage, limit: input.limit ?? 20 })
  });
  api.registerTool({
    id: "crmy_contact_create",
    name: "CRMy: Create Contact",
    description: "Create a new contact in CRMy. At minimum provide a name. Email, phone, title, and account_id are optional.",
    input: {
      type: "object",
      properties: {
        name: { type: "string", description: "Full name (required)" },
        email: { type: "string", description: "Email address" },
        phone: { type: "string", description: "Phone number" },
        title: { type: "string", description: "Job title" },
        account_id: { type: "string", description: "UUID of the associated account/company" },
        lifecycle_stage: { type: "string", description: "Initial lifecycle stage (e.g. prospect, lead, customer)" },
        notes: { type: "string", description: "Any initial notes about this contact" }
      },
      required: ["name"]
    },
    handler: async (input) => client.post("/contacts", input)
  });
  api.registerTool({
    id: "crmy_contact_update",
    name: "CRMy: Update Contact",
    description: "Update fields on an existing contact. Provide the contact id and any fields to change.",
    input: {
      type: "object",
      properties: {
        id: { type: "string", description: "Contact UUID (required)" },
        name: { type: "string", description: "Updated name" },
        email: { type: "string", description: "Updated email" },
        phone: { type: "string", description: "Updated phone" },
        title: { type: "string", description: "Updated job title" },
        account_id: { type: "string", description: "Move to a different account UUID" }
      },
      required: ["id"]
    },
    handler: async ({ id, ...rest }) => client.patch(`/contacts/${id}`, rest)
  });
  api.registerTool({
    id: "crmy_contact_log_activity",
    name: "CRMy: Log Activity",
    description: "Log a call, email, meeting, or other activity against a contact, account, or opportunity. Provide subject_type + subject_id to attach it to the right record.",
    input: {
      type: "object",
      properties: {
        activity_type: {
          type: "string",
          description: "Type of activity \u2014 e.g. call, email, meeting, demo, proposal, note"
        },
        subject_type: {
          type: "string",
          description: "Record type the activity is attached to: contact, account, or opportunity",
          enum: ["contact", "account", "opportunity"]
        },
        subject_id: { type: "string", description: "UUID of the contact, account, or opportunity" },
        summary: { type: "string", description: "Short summary of what happened" },
        outcome: { type: "string", description: "Outcome of the activity (e.g. positive, neutral, negative)" },
        performed_at: { type: "string", description: "ISO 8601 timestamp (defaults to now)" },
        duration_minutes: { type: "number", description: "Duration in minutes (for calls and meetings)" },
        notes: { type: "string", description: "Detailed notes" }
      },
      required: ["activity_type", "subject_type", "subject_id", "summary"]
    },
    handler: async (input) => client.post("/activities", input)
  });
  api.registerTool({
    id: "crmy_contact_set_lifecycle",
    name: "CRMy: Set Contact Lifecycle Stage",
    description: "Change the lifecycle stage of a contact (e.g. lead \u2192 prospect \u2192 customer \u2192 churned).",
    input: {
      type: "object",
      properties: {
        id: { type: "string", description: "Contact UUID" },
        stage: { type: "string", description: "New lifecycle stage (e.g. lead, prospect, customer, churned)" },
        note: { type: "string", description: "Optional note explaining the stage change" }
      },
      required: ["id", "stage"]
    },
    handler: async ({ id, ...rest }) => client.patch(`/contacts/${id}`, rest)
  });
  api.registerTool({
    id: "crmy_account_search",
    name: "CRMy: Search Accounts",
    description: "Search for companies/accounts by name, industry, or keyword.",
    input: {
      type: "object",
      properties: {
        q: { type: "string", description: "Search query (company name, domain, etc.)" },
        industry: { type: "string", description: "Filter by industry" },
        limit: { type: "number", description: "Max results (default 20)" }
      },
      required: ["q"]
    },
    handler: async (input) => client.get("/accounts", { q: input.q, industry: input.industry, limit: input.limit ?? 20 })
  });
  api.registerTool({
    id: "crmy_account_create",
    name: "CRMy: Create Account",
    description: "Create a new company/account record in CRMy.",
    input: {
      type: "object",
      properties: {
        name: { type: "string", description: "Company name (required)" },
        domain: { type: "string", description: "Company website domain (e.g. acme.com)" },
        industry: { type: "string", description: "Industry sector" },
        size: { type: "string", description: "Company size (e.g. 1-10, 11-50, 51-200, 201-1000, 1000+)" },
        notes: { type: "string", description: "Any initial notes about this company" }
      },
      required: ["name"]
    },
    handler: async (input) => client.post("/accounts", input)
  });
  api.registerTool({
    id: "crmy_opportunity_search",
    name: "CRMy: Search Opportunities",
    description: "Search for deals/opportunities by name, account, or stage.",
    input: {
      type: "object",
      properties: {
        q: { type: "string", description: "Search query (deal name, account, etc.)" },
        stage: { type: "string", description: "Filter by deal stage (e.g. prospecting, proposal, closed_won)" },
        account_id: { type: "string", description: "Filter by account UUID" },
        limit: { type: "number", description: "Max results (default 20)" }
      },
      required: ["q"]
    },
    handler: async (input) => client.get("/opportunities", {
      q: input.q,
      stage: input.stage,
      account_id: input.account_id,
      limit: input.limit ?? 20
    })
  });
  api.registerTool({
    id: "crmy_opportunity_create",
    name: "CRMy: Create Opportunity",
    description: "Create a new deal/opportunity in CRMy. Provide a name and optionally an account, value, and stage.",
    input: {
      type: "object",
      properties: {
        name: { type: "string", description: "Deal name (required)" },
        account_id: { type: "string", description: "Associated account UUID" },
        value: { type: "number", description: "Deal value in your base currency" },
        stage: { type: "string", description: "Initial deal stage (defaults to prospecting)" },
        close_date: { type: "string", description: "Expected close date (ISO 8601, e.g. 2026-06-30)" },
        notes: { type: "string", description: "Any notes about this deal" }
      },
      required: ["name"]
    },
    handler: async (input) => client.post("/opportunities", input)
  });
  api.registerTool({
    id: "crmy_opportunity_advance_stage",
    name: "CRMy: Advance Opportunity Stage",
    description: "Move a deal to a new stage (e.g. proposal \u2192 negotiation \u2192 closed_won). Optionally add a note.",
    input: {
      type: "object",
      properties: {
        id: { type: "string", description: "Opportunity UUID (required)" },
        stage: { type: "string", description: "New stage name (required)" },
        note: { type: "string", description: "Note explaining the stage transition" },
        lost_reason: { type: "string", description: "If closing as lost, the reason" }
      },
      required: ["id", "stage"]
    },
    handler: async ({ id, ...rest }) => client.patch(`/opportunities/${id}`, rest)
  });
  api.registerTool({
    id: "crmy_pipeline_summary",
    name: "CRMy: Pipeline Summary",
    description: 'Get a summary of the sales pipeline \u2014 total deal count and value by stage. Useful for answering questions like "how many deals do we have?" or "what is our pipeline worth?"',
    input: {
      type: "object",
      properties: {
        group_by: {
          type: "string",
          description: "Group results by: stage (default), owner, or forecast_cat",
          enum: ["stage", "owner", "forecast_cat"]
        }
      }
    },
    handler: async (input) => client.get("/analytics/pipeline", { group_by: input.group_by ?? "stage" })
  });
};
export {
  index_default as default
};
