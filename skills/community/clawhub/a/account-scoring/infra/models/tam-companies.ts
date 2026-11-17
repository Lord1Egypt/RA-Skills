import { defineModel } from "@cargo-ai/cdk";

import { aiArk } from "../connectors/ai-ark";
import { modelsFolder } from "../folders";

// The account universe this skill tiers: tam-building's `tam_companies`, with
// four columns added for the tier, its reason, its evidence and its stamp.
//
// THIS IS A COPY. tam-building owns this model and its filter. A cookbook
// carries every resource it imports, so the copy is here for the case where
// account-scoring is installed alone, but the expected install is after
// tam-building: then move `additionalColumns` below onto tam-building's
// declaration (`infra/tam-building/models/tam-companies.ts`), point the play
// and the segments at that export, and delete this file. One slug declared
// twice collides at deploy.
//
// A sync of the model replaces its rows. Custom column values survive on the
// companies the sync returns again, so re-sourcing the same market keeps their
// tiers, and the play only judges the new rows.
export const tamCompanies = defineModel("tam_companies", {
  connector: aiArk,
  extractSlug: "fetchCompanies",
  description:
    "The account universe sourced from AI Ark, tiered A / B / C / disqualified in place by the account-scoring play.",
  folder: modelsFolder,

  // The tier lives on the row it judges, so a segment over this model is a
  // plain filter and the rows a re-sync keeps keep their tier. The play writes
  // these with their bare slugs; reads see them as `custom__<slug>`.
  additionalColumns: [
    {
      kind: "custom",
      slug: "tier",
      type: "string",
      label: "Tier",
      description:
        "A, B, C, or disqualified, from the tiering rubric in the workspace context. Written by the tiering play.",
    },
    {
      kind: "custom",
      slug: "tier_reason",
      type: "string",
      label: "Tier rationale",
      description:
        "Two sentences naming the rubric lines that decided the tier, and the evidence behind them.",
    },
    {
      kind: "custom",
      slug: "tier_evidence_url",
      type: "string",
      label: "Tier evidence",
      description:
        "The page the agent verified against when the sourced row was not enough. Empty when the sourced facts decided it.",
    },
    {
      kind: "custom",
      slug: "tiered_at",
      type: "date",
      label: "Tiered at",
      description:
        "When the tier was last written. The play's eligibility stamp: never tiered, or older than the refresh window.",
    },
  ],

  // PLACEHOLDER: tam-building's filter, kept so this copy deploys on its own.
  // Replace it with the approved one, or drop the file as described above.
  config: {
    industry: {
      industry_or: [
        "software development",
        "it services and it consulting",
        "technology, information and internet",
      ],
    },
    employeeSize: { min_employee_count: 20, max_employee_count: 500 },
    companyLocation: {
      location_or: ["United States", "United Kingdom"],
    },
    limit: 500,
  },
});
