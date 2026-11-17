import { defineAgent } from "@cargo-ai/cdk";

import { anthropic } from "../connectors/anthropic";
import { agentsFolder } from "../folders";
import { gtmAccounts } from "../models/gtm-accounts";
import { gtmOpportunities } from "../models/gtm-opportunities";

// The analyst: one judgment per account whose won deal just entered its
// renewal window.
//
// The play hands it a won deal ten to twelve months old. The rest is SQL over
// the gtm_opportunities model: is this still the account's latest win (or did a newer one
// already renew it), what is the cadence across its wins, what did it pay
// last time. Then the question no column holds: is anything outside (a
// funding round, a hiring push, a new product, a new leader) giving the
// account manager a reason to call now.
//
// It reads, it never writes. Both models are read-only here, the
// playbook for what counts as an expansion moment is in the workspace context,
// and web search settles the outside signals. The play persists the judgment;
// an agent that could write would decide its own routing, and a missing
// signal could then be a failed run, a skip, or a choice.
export const expansionAnalyst = defineAgent("expansion_analyst", {
  name: "Expansion analyst",
  description:
    "Judges whether a customer in its renewal window is ready to expand, from its purchase history and outside signals, with evidence.",
  color: "green",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  systemPrompt: [
    "You have no clock of your own, so never assume the date. First read it with SQL: SELECT CURRENT_TIMESTAMP() AS now, CURRENT_DATE() AS today. Every 'now', 'this week' and date window below is measured from those values; write timestamps as ISO 8601 strings.",
    "You judge whether one existing customer of a B2B seller is at an expansion moment, for the account manager who owns it.",
    "Read the workspace context first: what we sell, our packaging and the plays our team runs on customers. It is the rubric for suggested_play; nothing in this prompt overrides it.",
    "Then query the gtm_opportunities model in SQL for this account_id: every deal with is_won true, with close_date and amount, newest first, and the account's row in the gtm_accounts model for its name and website. If a won deal closed after the trigger deal and more than 2 months after it, the account already renewed: answer 'none' and say so. A newer won deal within 2 months of the trigger is the same buying cycle (a second order, an add-on), not a renewal: judge the account on the purchase history as a whole. Otherwise state the cadence if there are two or more wins (for example 'renewed every 12 months, last at 18,000') and the last price paid.",
    "Then use web search, at most three times, for public events in the last 120 days: funding, a hiring push in the team that uses our product, a new product or market, a leadership change. Keep only events with a dated source.",
    "Signal is one of: 'renewal' (the contract anniversary is the moment and nothing more), 'expansion' (an outside event or usage pattern says they need more), 'repeat_purchase' (a cadence says the next order is due), 'at_risk' (an event says the renewal itself is in doubt, such as layoffs or a new leader who buys from a competitor), or 'none'.",
    "Never invent a deal, an amount, an event or a URL. An absent fact is absent; say so in the reason.",
    "Answer in the exact JSON shape requested: the signal, a reason of at most three sentences that names the purchase history and the deciding event with its date, the suggested play from the context, and every URL you relied on.",
  ].join(" "),
  output: {
    type: "jsonSchema",
    jsonSchema: {
      type: "object",
      properties: {
        signal: {
          type: "string",
          enum: ["renewal", "expansion", "repeat_purchase", "at_risk", "none"],
          description: "The kind of moment this account is at.",
        },
        reason: {
          type: "string",
          description:
            "At most three sentences: the purchase history, the deciding event and its date.",
        },
        suggested_play: {
          type: "string",
          description:
            "The play from the workspace context the account manager should run, or an empty string for 'none'.",
        },
        evidence_urls: {
          type: "array",
          items: { type: "string" },
          description:
            "Every page the judgment relied on. Empty when the deal history alone decided it.",
        },
      },
      required: ["signal", "reason", "suggested_play", "evidence_urls"],
      additionalProperties: false,
    },
  },
  // Per-company ceiling: a model read, up to three searches, and the answer.
  maxSteps: 10,
  capabilities: [
    "webSearch",
    { slug: "context", config: { isReadOnly: true } },
  ],
  uses: [
    { ref: gtmOpportunities, readOnly: true },
    { ref: gtmAccounts, readOnly: true },
  ],
  evaluator: {
    rubric:
      "Does the reason name the real purchase history from the gtm_opportunities model and, for any signal other than 'renewal' or 'none', a dated outside event with a URL in evidence_urls? Is suggested_play taken from the workspace context?",
    threshold: 0.8,
  },
  folder: agentsFolder,
});
