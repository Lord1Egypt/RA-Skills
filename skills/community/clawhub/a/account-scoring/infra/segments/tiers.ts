import { defineSegment } from "@cargo-ai/cdk";

import { tamCompanies } from "../models/tam-companies";

// Views onto what the play produced, which is the only kind of segment worth
// deploying: one per tier the agent can emit, so no tier lands nowhere. They
// read `custom__tier` because the read side exposes custom columns under that
// alias; the play writes the bare slug.

// Work it now. The handle contact-sourcing and engagement take.
export const tierA = defineSegment("tier_a_accounts", {
  model: tamCompanies,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            columnSlug: tamCompanies.columns.custom__tier,
            operator: "is",
            values: ["A"],
          },
        ],
      },
    ],
  },
});

// Worth a sequence, not a rep.
export const tierB = defineSegment("tier_b_accounts", {
  model: tamCompanies,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            columnSlug: tamCompanies.columns.custom__tier,
            operator: "is",
            values: ["B"],
          },
        ],
      },
    ],
  },
});

// In the market, not in the motion. Nurture, or leave until it changes.
export const tierC = defineSegment("tier_c_accounts", {
  model: tamCompanies,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            columnSlug: tamCompanies.columns.custom__tier,
            operator: "is",
            values: ["C"],
          },
        ],
      },
    ],
  },
});

// The one that pays for the skill. Everything here was sourced, judged and
// ruled out with a written reason, so it is the segment you suppress rather
// than the one you work. A large disqualified share is a tam-building filter
// that is too wide, not an agent that is too harsh: narrow the filter, where
// narrowing is free, not the rubric.
export const disqualified = defineSegment("disqualified_accounts", {
  model: tamCompanies,
  filter: {
    conjonction: "and",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            kind: "string",
            columnSlug: tamCompanies.columns.custom__tier,
            operator: "is",
            values: ["disqualified"],
          },
        ],
      },
    ],
  },
});
