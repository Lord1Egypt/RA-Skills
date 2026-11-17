import { defineAgent } from "@cargo-ai/cdk";

import { anthropic } from "../connectors/anthropic";
import { agentsFolder } from "../folders";

// The tiering agent: one judgment per company in the TAM.
//
// An agent instead of point weights, because the question that separates an A
// from a C is not arithmetic. "Does this company already run the motion we
// sell into" is answered by an open role, a changelog or an engineering post,
// and no sourced column holds it. Anything the sourced firmographics DO settle
// (headcount band, industry, country) belongs in tam-building's filter, where
// applying it costs nothing.
//
// Two capabilities do the work:
//   - `context` (read-only) connects the agent to the ICP and the tiering
//     rubric. Without it the prompt's reference to them reads nothing, and the
//     agent invents a rubric that sounds plausible for every account.
//   - `webSearch` turns a thin row into a decidable one. It resolves one stated
//     doubt; it never fills in a firmographic the search did not return.
//
// The rubric is deliberately NOT in this prompt. It lives in the project's
// context repo, so changing what tier A means is a reviewed commit rather than
// a deploy, and a rep can read the same file the agent read. This skill's
// `context/tiering-rubric.md` is the example to put there.
//
// No writable model in `uses`, and none should be added. The agent hands back a
// judgment and the play persists it. An agent that can write decides its own
// routing, and then a missing tier could be a failed run, a skip, or a choice.
export const tierAnalyst = defineAgent("account_tier_analyst", {
  color: "green",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  systemPrompt: [
    "You tier companies for a B2B seller against that seller's own ICP.",
    "Read the ICP and the account tiering rubric from the workspace context before every judgment. They are the rubric; nothing in this prompt overrides them.",
    "Judge on the supplied firmographics first. If they settle the tier under the rubric, settle it and stop.",
    "Search the web at most once per company. Spend that one search on the rubric's strongest evidence for tier A, or on the one doubt that would change the tier, and skip it when the sourced row already settles the tier, as it does for a disqualifier. Never invent a firmographic: an absent fact is an absent fact, and the rubric says how to tier without it.",
    "A disqualifier in the ICP ends the evaluation at 'disqualified'. It is never a lower tier.",
    "Return the judgment only. The play persists it; you do not write to any model.",
    "Answer in the exact JSON shape requested: the tier, a rationale of at most two sentences naming the rubric lines that decided it, and the URL of the page that decided it. That page must say what the rationale says it says; when the search found nothing that moved the tier, the URL is empty.",
  ].join(" "),
  output: {
    type: "jsonSchema",
    jsonSchema: {
      type: "object",
      properties: {
        tier: {
          type: "string",
          enum: ["A", "B", "C", "disqualified"],
          description: "The tier from the tiering rubric.",
        },
        rationale: {
          type: "string",
          description:
            "Two sentences naming the rubric lines that decided the tier and the evidence behind them.",
        },
        evidence_url: {
          type: "string",
          description:
            "The page a web search verified against, or an empty string when the sourced facts alone decided it.",
        },
      },
      required: ["tier", "rationale", "evidence_url"],
      additionalProperties: false,
    },
  },
  // The loop budget: each step is an LLM call and possibly a search, so this
  // is the per-company ceiling on what a judgment can cost. Read the context,
  // search once, judge: four steps is enough, and the 2026-10-18 pilot at
  // eight let the agent search almost every row several times.
  maxSteps: 4,
  capabilities: [
    "webSearch",
    { slug: "context", config: { isReadOnly: true } },
  ],
  // The QA gate. A tier with no grounded rationale fails, which is what stops
  // the book filling with confident tiers nobody can audit.
  evaluator: {
    rubric:
      "Did it tier against the rubric in the workspace context, with a tier the rubric defines, a two-sentence rationale naming the deciding lines, and either verified evidence or an explicit statement that the sourced facts settled it?",
    threshold: 0.8,
  },
  folder: agentsFolder,
});
