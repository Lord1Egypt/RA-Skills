import { definePlay, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { crm } from "../connectors/crm";
import { slack } from "../connectors/slack";
import { playsFolder } from "../folders";
import { crmAccounts } from "../models/crm-accounts";
import { deriveEvidence } from "../scripts/accounts/evidence";

// PLACEHOLDER — the Slack channel every review request is posted to. Resolve it
// against the live workspace and get it approved before deploying.
const reviewChannelId = "PLACEHOLDER_REVIEW_CHANNEL_ID";

// The automatic class is deliberately narrow: a cluster merges unattended only
// at this score AND under the exact-identity guard the evidence script sets.
// Either one alone is not enough — the score is evidence, the guard is policy.
const automaticMergeScore = 60;

// A reviewer has a working day to answer. After that the request declines
// itself, and a decline leaves the records separate — the safe outcome.
const reviewTimeoutMilliseconds = 24 * 60 * 60 * 1000;

// One CRM account row in, one terminal outcome out.
const deduplicateCrmAccount = defineWorkflow(
  "deduplicate_crm_account",
  {
    input: z.object({
      hs_object_id: z.string(),
      name: z.string().optional(),
      domain: z.string().optional(),
      linkedin_company_page: z.string().optional(),
      linkedin_company_id: z.string().optional(),
      // PLACEHOLDER — point these two at the protected-ID and parent-company
      // properties the live CRM audit approved.
      protected_business_id: z.string().optional(),
      parent_company_id: z.string().optional(),
      lifecyclestage: z.string().optional(),
      hs_num_open_deals: z.number().optional(),
      num_associated_contacts: z.number().optional(),
      hs_num_engagements: z.number().optional(),
      notes_last_updated: z.string().optional(),
      createdate: z.string().optional(),
    }),
    output: z.object({
      status: z.string(),
      score: z.number().optional(),
      survivorId: z.string().optional(),
      mergedIds: z.array(z.string()).optional(),
    }),
    uses: { crm },
  },
  ({ input, uses, js, scoring, humanReview }) => {
    // The queue can be hours old, so cluster membership is re-derived from the
    // CRM on every run rather than trusted from the extract that enrolled it.
    const records = uses.crm.findRecords({
      objectType: "companies",
      criterias: [
        {
          propertyName: "linkedin_company_id",
          value: input.linkedin_company_id,
        },
        {
          propertyName: "linkedin_company_page",
          value: input.linkedin_company_page,
        },
        { propertyName: "domain", value: input.domain },
      ],
    });

    // Everything the merge decision rests on, derived deterministically: no
    // model, no judgement. The same records always produce the same evidence.
    //
    // The body lives in `infra/scripts/accounts/`, one subject per module:
    // reading records into accounts, clustering, survivor ranking, and the
    // policy they read. It receives the search's records and this account's ID
    // as values, so it never names the slug either lives under, and `evidence`
    // is typed from what the script returns.
    const evidence = deriveEvidence({
      records,
      accountId: input.hs_object_id,
    });

    if (!evidence.accountFound) {
      return { status: "source_missing_or_changed" };
    }

    if (!evidence.hasDuplicates) {
      return { status: "no_duplicates" };
    }

    const score = scoring({
      criterias: [
        {
          name: "Exact LinkedIn company ID",
          value: evidence.exactLinkedinId,
          score: 60,
        },
        {
          name: "Exact LinkedIn company URL",
          value: evidence.exactLinkedinUrl,
          score: 25,
        },
        {
          name: "Exact non-generic domain",
          value: evidence.exactDomain,
          score: 15,
        },
      ],
    });

    if (score.score >= automaticMergeScore && evidence.autoEligible) {
      uses.crm.mergeRecords({
        objectType: "companies",
        primaryId: evidence.primaryId,
        idsToMerge: evidence.idsToMerge,
      });

      return {
        status: "merged_automatically",
        score: score.score,
        survivorId: evidence.primaryId,
        mergedIds: evidence.idsToMerge,
      };
    }

    // Everything else. The reviewer sees the score, every conflict that kept
    // the cluster out of the automatic class, and the evidence per record.
    const reviewed = humanReview(
      {
        connectorUuid: slack.uuid,
        channelId: reviewChannelId,
        title: `Review CRM account merge into ${evidence.primaryId}`,
        content: `Duplicate score: ${score.score}/100
Survivor: ${evidence.primaryId}
Records to merge: ${evidence.idsToMerge}
Identity conflict: ${evidence.identityConflict}
Protected ID conflict: ${evidence.protectedIdConflict}
Parent/subsidiary warning: ${evidence.parentOrSubsidiaryWarning}
Evidence:
${evidence.evidenceSummary}`,
        timeoutMilliseconds: reviewTimeoutMilliseconds,
        enableEditButton: false,
      },
      {
        approved: () => {
          uses.crm.mergeRecords({
            objectType: "companies",
            primaryId: evidence.primaryId,
            idsToMerge: evidence.idsToMerge,
          });
          return js(() => "merged_after_review");
        },
        // Decline and timeout share this path. It writes nothing.
        declined: () => js(() => "review_declined_or_timed_out"),
      },
    );

    return {
      status: reviewed,
      score: score.score,
      survivorId: evidence.primaryId,
      mergedIds: evidence.idsToMerge,
    };
  },
);

// A row is worth searching only when it carries the CRM record ID and at least
// one identity key. Company name is never one of them: two companies can share
// a name and never be the same record.
//
// Disabled, serial, and capped at 15 rows. This play merges CRM records, so the
// pilot stays small enough for a human to verify every survivor by hand, and
// only an approved pilot lifts any of the three.
export const deduplicateAccounts = definePlay("deduplicate_accounts", {
  folder: playsFolder,
  model: crmAccounts,
  workflow: deduplicateCrmAccount,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            columnSlug: crmAccounts.columns.hs_object_id,
            operator: "isNotEmpty",
          },
        ],
      },
      {
        conjonction: "or",
        conditions: [
          {
            kind: "string",
            columnSlug: crmAccounts.columns.linkedin_company_id,
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            columnSlug: crmAccounts.columns.linkedin_company_page,
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            columnSlug: crmAccounts.columns.domain,
            operator: "isNotEmpty",
          },
        ],
      },
    ],
  },
  limit: 15,
  isEnabled: false,
  runCreationRule: "noConcurrency",
  changeKinds: ["added", "updated"],
  schedule: { type: "cron", cron: "0 7 * * *" },
});
