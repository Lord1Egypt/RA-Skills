import { definePlay, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { expansionAnalyst } from "../agents/analyst";
import { playsFolder } from "../folders";
import { gtmAccounts } from "../models/gtm-accounts";
import { gtmOpportunities } from "../models/gtm-opportunities";

// One won deal entering its renewal window in, one judgment written onto its
// account out. The analyst decides what moment the account is at; this
// workflow is the only thing that persists, so a missing signal is always a
// failed run and never a silent skip.
const flagAccount = defineWorkflow(
  "flag_expansion_account",
  {
    input: z.object({
      id: z.string(),
      account_id: z.string(),
      name: z.string().optional(),
      amount: z.any(),
      close_date: z.any(),
    }),
    output: z.object({ signal: z.string() }),
    uses: { expansionAnalyst },
    // The body is parsed from source, not executed: `gtm_accounts` has to be
    // handed to the parser here, or its uuid is a name nothing resolves.
    imports: { gtmAccounts },
  },
  ({ input, uses, model }) => {
    const judgment = uses.expansionAnalyst({
      prompt: `Judge the expansion moment for account ${input.account_id}. The trigger is won deal ${input.id} (${input.name}), closed on ${input.close_date} for ${input.amount}, now in its renewal window.`,
    });

    // The only write in the pipeline: three custom columns on the account
    // record, by its id. No deal, contact or owner is touched. Bare slugs, not
    // the `custom__` read alias: a prefixed slug is silently dropped while the
    // node still reports success.
    model.customColumn({
      modelUuid: gtmAccounts.uuid,
      id: input.account_id,
      mappings: [
        { columnSlug: "expansion_signal", value: judgment.answer.signal },
        {
          columnSlug: "expansion_reason",
          value: `${judgment.answer.reason} Play: ${judgment.answer.suggested_play} Sources: ${judgment.answer.evidence_urls}`,
        },
        { columnSlug: "expansion_signal_at", value: new Date() },
      ],
    });

    return { signal: judgment.answer.signal };
  },
);

// Who is judged, asked here and nowhere else: a won deal whose close date is
// ten to twelve months old, which for an annual contract is the sixty days
// before the renewal.
//
// `changeKinds: ["added"]` is the idempotency. A deal enters this window once
// per renewal, so each renewal is judged once, not once a week for two
// months. Whether the account is still a customer, and whether a newer win
// already renewed it, is the analyst's SQL over `gtm_opportunities`, not a hand-kept flag
// on the account.
//
// The window is the number most teams change: monthly or two-year contracts
// move both dates. Ships disabled; enable, then execute once, since `added`
// does not backfill deals that entered while the play was off.
export const flagExpansion = definePlay("flag_expansion", {
  description:
    "Per won deal entering its renewal window: the analyst judges the account and the play writes signal, reason and stamp onto it.",
  folder: playsFolder,
  model: gtmOpportunities,
  workflow: flagAccount,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "boolean",
            columnSlug: gtmOpportunities.columns.is_won,
            operator: "isTrue",
          },
          {
            kind: "string",
            columnSlug: gtmOpportunities.columns.account_id,
            operator: "isNotEmpty",
          },
          {
            kind: "date",
            columnSlug: gtmOpportunities.columns.close_date,
            operator: "lowerThan",
            value: "10 months",
          },
          {
            kind: "date",
            columnSlug: gtmOpportunities.columns.close_date,
            operator: "greaterThan",
            value: "12 months",
          },
        ],
      },
    ],
  },
  isEnabled: false,
  runCreationRule: "noConcurrency",
  changeKinds: ["added"],
  // Monday 06:00 UTC. The digest runs at 15:00 the same day.
  schedule: { type: "cron", cron: "0 6 * * 1" },
});
