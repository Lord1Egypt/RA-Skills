import { definePlay, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { tierAnalyst } from "../agents/tier-analyst";
import { crm } from "../connectors/crm";
import { playsFolder } from "../folders";
import { tamCompanies } from "../models/tam-companies";
import { crmWriteback, rescoreAfter } from "../settings";

// The columns `aiArk.fetchCompanies` lands, confirmed against a live
// `tam_companies` on 2026-10-03. On a swapped source, check them with
// `cargo-ai storage column list` first: a renamed column leaves the prompt
// describing an undefined, and the agent tiers a company it was told nothing
// about.
const input = z.object({
  id: z.string(),
  name: z.string(),
  domain: z.string(),
  industry: z.string(),
  employee_count: z.number(),
  country: z.string(),
  description: z.string(),
});
const output = z.object({ tier: z.string(), rationale: z.string() });

// The CRM write-back settings, flattened into constants the CRM body inlines as
// literals. Unused when `crmWriteback.crm` is `none`. HubSpot's company object
// is `companies`; Salesforce's is `Account`.
const crmObjectType =
  crmWriteback.crm === "salesforce" ? "Account" : "companies";
const crmMatchOn =
  crmWriteback.crm === "none" ? "domain" : crmWriteback.matchOn;
const crmMatchProperty =
  crmWriteback.crm === "none" ? "" : crmWriteback.matchProperty;
const crmTierField =
  crmWriteback.crm === "none" ? "" : crmWriteback.fields.tier;
const crmReasonField =
  crmWriteback.crm === "none" ? "" : crmWriteback.fields.reason;
const crmScoredAtField =
  crmWriteback.crm === "none" ? "" : crmWriteback.fields.scoredAt;

// One agent call per company, written back onto the row that triggered it.
// The agent judges; this workflow is the only thing that persists, so a
// missing tier is always a failed run and never a silent skip.
//
// Two bodies, one chosen by `crmWriteback` in `settings.ts` when the project
// loads: the row write alone, or the row write followed by one CRM update. The
// body is parsed from source rather than executed, so a CRM call cannot sit
// behind a runtime `if` on a connector that `none` never declares. Everything
// above the CRM update is identical in both: change one, change the other.
const tierAccount =
  crm === undefined || crmWriteback.crm === "none"
    ? defineWorkflow(
        "tier_account",
        {
          input,
          output,
          uses: { tierAnalyst },
          // `imports` is not optional here. The body is parsed from source,
          // not executed, so a bare closure reference like `tamCompanies` is a
          // name the parser cannot resolve. Listing it hands the parser the
          // handle, whose `uuid` stays a deferred token the deploy resolves in
          // order.
          imports: { tamCompanies },
        },
        ({ input, uses, model }) => {
          // Agent calls resolve to `{ answer, evaluation? }`; the judgment is
          // on `.answer`. The JSON shape is declared once, on the agent's
          // `output`, so the schema and the write below cannot drift apart.
          const judgment = uses.tierAnalyst({
            prompt: `Tier ${input.name} (${input.domain}) against the ICP and the tiering rubric in the workspace context. Industry: ${input.industry}. Employees: ${input.employee_count}. Country: ${input.country}. About: ${input.description}`,
          });

          // Bare slugs, NOT the `custom__` names the read side exposes. The
          // write path nests the declared slug under `custom` itself, so
          // `custom__tier` here becomes `custom.custom__tier`: the node still
          // reports "Record upserted" and the value is dropped, which looks
          // like a play that ran perfectly over a book with no tiers in it.
          model.customColumn({
            modelUuid: tamCompanies.uuid,
            id: input.id,
            mappings: [
              { columnSlug: "tier", value: judgment.answer.tier },
              { columnSlug: "tier_reason", value: judgment.answer.rationale },
              {
                columnSlug: "tier_evidence_url",
                value: judgment.answer.evidence_url,
              },
              // The eligibility stamp the play filter reads, written on the
              // same node as the tier, so a row is never marked judged
              // without carrying the judgment.
              { columnSlug: "tiered_at", value: new Date() },
            ],
          });

          return {
            tier: judgment.answer.tier,
            rationale: judgment.answer.rationale,
          };
        },
      )
    : defineWorkflow(
        "tier_account",
        {
          input,
          output,
          uses: { tierAnalyst, crm },
          imports: {
            tamCompanies,
            crmObjectType,
            crmMatchOn,
            crmMatchProperty,
            crmTierField,
            crmReasonField,
            crmScoredAtField,
          },
        },
        ({ input, uses, model }) => {
          const judgment = uses.tierAnalyst({
            prompt: `Tier ${input.name} (${input.domain}) against the ICP and the tiering rubric in the workspace context. Industry: ${input.industry}. Employees: ${input.employee_count}. Country: ${input.country}. About: ${input.description}`,
          });

          model.customColumn({
            modelUuid: tamCompanies.uuid,
            id: input.id,
            mappings: [
              { columnSlug: "tier", value: judgment.answer.tier },
              { columnSlug: "tier_reason", value: judgment.answer.rationale },
              {
                columnSlug: "tier_evidence_url",
                value: judgment.answer.evidence_url,
              },
              { columnSlug: "tiered_at", value: new Date() },
            ],
          });

          // The CRM mirror, after the row is written, so the row stays the
          // record of the judgment whatever the CRM does. Guarded on a match
          // value: an empty domain would otherwise ask the CRM for every
          // company with an empty domain.
          //
          // `updateRecords`, never `upsertRecords`: a company the CRM does not
          // hold is not created from a TAM row. HubSpot answers a miss with
          // "No objects updated"; Salesforce throws "No records have been
          // updated". `continueOnFailure` lets that miss end the run as a
          // success, because most of a sourced TAM is not in the CRM yet. The
          // cost is that a CRM write that fails for another reason (a field
          // that does not exist, a lapsed connection) also ends green, so the
          // pilot reads one record back from the CRM (references/run.md).
          //
          // `isFailingOnMultipleMatches: true`: when the match value finds
          // several CRM companies (duplicates sharing a domain), the update
          // writes nothing and fails instead of tiering every one of them.
          // Without it, both duplicates get the tier. The failure is also
          // absorbed by `continueOnFailure`, so the row is still tiered in
          // Cargo and the CRM node's error names the match count.
          if (input[crmMatchOn]) {
            uses.crm.updateRecords(
              {
                objectType: crmObjectType,
                matchingPropertyName: crmMatchProperty,
                matchingValue: input[crmMatchOn],
                isFailingOnMultipleMatches: true,
                mappings: [
                  { propertyName: crmTierField, value: judgment.answer.tier },
                  {
                    propertyName: crmReasonField,
                    value: judgment.answer.rationale,
                  },
                  { propertyName: crmScoredAtField, value: new Date() },
                ],
              },
              { continueOnFailure: true },
            );
          }

          return {
            tier: judgment.answer.tier,
            rationale: judgment.answer.rationale,
          };
        },
      );

// Tiers every company never tiered, and re-tiers anything stamped longer ago
// than `rescoreAfter` (settings.ts, six months by default; "7 days" re-scores
// the book weekly). A stale row enters the filter again, which is what
// `changeKinds: ["added"]` enrols. The filter IS the eligibility: no separate segment restates it,
// and the workflow does not branch on it again.
//
// `changeKinds: ["added"]` is the cost control. Runs are created for rows
// entering the filter, not for the whole book on every tick, so steady state
// is: a sync lands N new companies, the next tick judges those N, and every
// tick after is a no-op. Drop it and the LLM bill scales with how often the
// cron fires instead of with how many companies arrived.
//
// Cron, not watch or realtime: `fetchCompanies` is a plain fetch extractor, so
// realtime needs an ingest-mode extractor and watch needs `isWatchable` (both
// fail at deploy with integrationNotCompatible). Hourly, because the model has
// no schedule of its own: rows land whenever someone syncs, and an untiered
// row sits outside the tier segments until the next tick.
//
// Ships disabled. Pilot a sample through the workflow first
// (references/run.md), then enable and execute once: `added` does not backfill
// the rows that were already there while the play was off.
export const tierAccounts = definePlay("tier_accounts", {
  description:
    "Per-company ICP tiering over the TAM: the agent judges against the context rubric and the play writes tier, rationale, evidence and stamp back onto the row.",
  folder: playsFolder,
  model: tamCompanies,
  workflow: tierAccount,
  filter: {
    conjonction: "and",
    groups: [
      {
        // Never tiered, or tiered before `rescoreAfter`. This reads the
        // STAMP, not the tier: a failed run leaves a null stamp and is retried,
        // while a row tiered `disqualified` stays put until it goes stale.
        conjonction: "or",
        conditions: [
          {
            kind: "date",
            columnSlug: tamCompanies.columns.custom__tiered_at,
            operator: "isNull",
          },
          {
            kind: "date",
            columnSlug: tamCompanies.columns.custom__tiered_at,
            operator: "lowerThan",
            value: rescoreAfter,
          },
        ],
      },
    ],
  },
  isEnabled: false,
  runCreationRule: "noConcurrency",
  changeKinds: ["added"],
  schedule: { type: "cron", cron: "15 * * * *" },
});
