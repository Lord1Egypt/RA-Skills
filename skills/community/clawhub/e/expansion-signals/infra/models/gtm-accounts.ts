import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The customer book: a native account model, so the worked example deploys
// with no CRM connector and no key. `defineAccount` gives the standard schema
// (id, name, website, industry, number_of_employees, owner_id, …); fill it
// with `cargo-ai storage record create-bulk`, a sourcing pipeline, or swap it
// for a CRM-backed model (the `crm-backed` variation in SKILL.md).
//
// Nothing here says who is a customer. That is computed from won deals, in
// SQL, by the analyst; a "customer" flag kept by hand is a second answer to
// the same question that drifts from the deals.
//
// The three columns below are the pipeline's only writes. Read side:
// `gtmAccounts.columns.custom__<slug>`. Write side (the play): the bare slug.
//
// `gtm_accounts` is a shared native model (scripts/native-models.json): every
// pipeline that needs accounts declares it under this slug, so a project that
// installs several keeps one, with each pipeline's added columns merged.
export const gtmAccounts = defineModel("gtm_accounts", {
  name: "GTM accounts",
  kind: "native",
  extractSlug: "defineAccount",
  description:
    "The customer book. Expansion signals write the signal, its reason and a stamp onto each judged account.",
  folder: modelsFolder,
  additionalColumns: [
    {
      kind: "custom",
      slug: "expansion_signal",
      type: "string",
      label: "Expansion signal",
      description:
        "renewal, expansion, repeat_purchase, at_risk or none. Written by the expansion play.",
    },
    {
      kind: "custom",
      slug: "expansion_reason",
      type: "string",
      label: "Expansion reason",
      description:
        "At most three sentences: purchase history, the deciding event and its date, the play to run, the sources.",
    },
    {
      kind: "custom",
      slug: "expansion_signal_at",
      type: "date",
      label: "Expansion judged at",
      description:
        "When the signal was last written. The digest reads the week's stamps.",
    },
  ],
});
