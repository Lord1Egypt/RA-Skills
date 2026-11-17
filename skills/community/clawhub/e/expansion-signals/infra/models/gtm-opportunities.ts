import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// Every deal, native: `defineDeal` gives id, name, account_id, amount,
// stage_name, close_date, is_closed, is_won, owner_id. The play runs on it
// (a won deal entering its renewal window is the trigger) and the analyst
// reads it in SQL for the account's purchase history: cadence across won
// deals, the last price paid, and whether a newer win already renewed it.
//
// Nothing in this pipeline writes a deal.
//
// `gtm_opportunities` is a shared native model (scripts/native-models.json): every
// pipeline that needs opportunities declares it under this slug, so a project that
// installs several keeps one, with each pipeline's added columns merged.
export const gtmOpportunities = defineModel("gtm_opportunities", {
  name: "GTM opportunities",
  kind: "native",
  extractSlug: "defineDeal",
  description:
    "Every deal. Won deals are the purchase history expansion signals judge from.",
  folder: modelsFolder,
});
