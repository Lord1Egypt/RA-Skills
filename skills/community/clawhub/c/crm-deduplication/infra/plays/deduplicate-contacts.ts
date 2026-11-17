import { definePlay, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { crm } from "../connectors/crm";
import { slack } from "../connectors/slack";
import { playsFolder } from "../folders";
import { crmContacts } from "../models/crm-contacts";
import { deriveContactEvidence } from "../scripts/contacts/evidence";
import { prepareContactSearch } from "../scripts/contacts/search";
import { prepareTransitiveContactSearch } from "../scripts/contacts/transitive-search";

// PLACEHOLDER: resolve the dedicated review channel before deployment.
const reviewChannelId = "PLACEHOLDER_REVIEW_CHANNEL_ID";
// PLACEHOLDER: set to false when the approved policy leaves low-confidence
// contacts untouched instead of sending them to Human Review.
const lowConfidenceContactReviewEnabled = true;
const automaticMergeScore = 60;
const reviewTimeoutMilliseconds = 24 * 60 * 60 * 1000;

const deduplicateCrmContact = defineWorkflow(
  "deduplicate_crm_contact",
  {
    input: z.object({
      hs_object_id: z.string(),
      email: z.string().optional(),
      phone: z.string().optional(),
      linkedin_url: z.string().optional(),
      linkedin_person_id: z.string().optional(),
      firstname: z.string().optional(),
      lastname: z.string().optional(),
      jobtitle: z.string().optional(),
      associatedcompanyid: z.string().optional(),
      num_associated_deals: z.number().optional(),
      num_contacted_notes: z.number().optional(),
      hs_sales_email_last_replied: z.number().optional(),
      createdate: z.string().optional(),
      lastmodifieddate: z.string().optional(),
    }),
    output: z.object({
      status: z.string(),
      score: z.number().optional(),
      survivorId: z.string().optional(),
      mergedIds: z.array(z.string()).optional(),
    }),
    uses: { crm },
    imports: { lowConfidenceContactReviewEnabled },
  },
  ({ input, uses, scoring, humanReview, js }) => {
    const search = prepareContactSearch({
      sourceId: input.hs_object_id,
      linkedinPersonId: input.linkedin_person_id,
      linkedinUrl: input.linkedin_url,
      email: input.email,
      phone: input.phone,
    });

    const directRecords = uses.crm.findRecords({
      objectType: "contacts",
      criterias: [
        {
          propertyName: "linkedin_person_id",
          value: search.linkedinPersonId,
        },
        { propertyName: "linkedin_url", value: search.linkedinUrlVariants[0] },
        { propertyName: "linkedin_url", value: search.linkedinUrlVariants[1] },
        { propertyName: "linkedin_url", value: search.linkedinUrlVariants[2] },
        { propertyName: "linkedin_url", value: search.linkedinUrlVariants[3] },
        { propertyName: "email", value: search.email },
        { propertyName: "phone", value: search.phone },
      ],
    });

    const transitiveSearch = prepareTransitiveContactSearch({
      records: directRecords,
    });
    const transitiveRecords = uses.crm.findRecords({
      objectType: "contacts",
      criterias: [
        {
          propertyName: "linkedin_person_id",
          value: transitiveSearch.linkedinPersonIds,
        },
        {
          propertyName: "linkedin_url",
          value: transitiveSearch.linkedinUrlVariants,
        },
        { propertyName: "email", value: transitiveSearch.emails },
        { propertyName: "phone", value: transitiveSearch.phones },
      ],
    });

    const evidence = deriveContactEvidence({
      directRecords,
      transitiveRecords,
      sourceId: input.hs_object_id,
    });

    if (!evidence.sourceFound) {
      return { status: "source_missing_or_changed" };
    }
    if (!evidence.hasDuplicates) {
      return { status: "no_duplicates" };
    }

    const score = scoring({
      criterias: [
        {
          name: "Exact LinkedIn person ID",
          value: evidence.exactLinkedinPersonId,
          score: 60,
        },
        {
          name: "Exact LinkedIn person URL without person-ID conflict",
          value: evidence.exactLinkedinUrl,
          score: 60,
        },
        {
          name: "Exact non-generic email without LinkedIn conflict",
          value: evidence.exactNonGenericEmail,
          score: 60,
        },
        {
          name: "Transitive high-confidence chain",
          value: evidence.transitiveHighConfidence,
          score: 60,
        },
      ],
    });

    if (score.score >= automaticMergeScore && evidence.autoEligible) {
      const merged = uses.crm.mergeRecords({
        objectType: "contacts",
        primaryId: evidence.primaryId,
        idsToMerge: evidence.idsToMerge,
      });
      return {
        status: "merged_automatically",
        score: score.score,
        survivorId: merged.id,
        mergedIds: evidence.idsToMerge,
      };
    }

    if (!lowConfidenceContactReviewEnabled) {
      return {
        status: "low_confidence_not_reviewed",
        score: score.score,
        survivorId: evidence.primaryId,
        mergedIds: evidence.idsToMerge,
      };
    }

    const reviewed = humanReview(
      {
        connectorUuid: slack.uuid,
        channelId: reviewChannelId,
        title: `Review CRM contact merge into ${evidence.primaryId}`,
        content: `Score: ${score.score}
Survivor before merge: ${evidence.primaryId}
Records to merge: ${evidence.idsToMerge}
Conflicting LinkedIn person IDs: ${evidence.conflictingLinkedinPersonIds}
Conflicting LinkedIn identity: ${evidence.conflictingLinkedinIdentity}
Generic or shared email: ${evidence.genericOrSharedEmail}
Records:
${evidence.reviewLines}`,
        timeoutMilliseconds: reviewTimeoutMilliseconds,
        enableEditButton: false,
      },
      {
        approved: () => {
          uses.crm.mergeRecords({
            objectType: "contacts",
            primaryId: evidence.primaryId,
            idsToMerge: evidence.idsToMerge,
          });
          return js(() => "merged_after_review");
        },
        declined: () => js(() => "review_declined_or_timed_out"),
      },
    );

    return {
      status: reviewed,
      score: score.score,
    };
  },
);

export const deduplicateContacts = definePlay("deduplicate_contacts", {
  folder: playsFolder,
  model: crmContacts,
  workflow: deduplicateCrmContact,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            columnSlug: crmContacts.columns.hs_object_id,
            operator: "isNotEmpty",
          },
        ],
      },
      {
        conjonction: "or",
        conditions: [
          {
            kind: "string",
            columnSlug: crmContacts.columns.linkedin_person_id,
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            columnSlug: crmContacts.columns.linkedin_url,
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            columnSlug: crmContacts.columns.email,
            operator: "isNotEmpty",
          },
          {
            kind: "string",
            columnSlug: crmContacts.columns.phone,
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
  schedule: { type: "cron", cron: "30 7 * * *" },
});
