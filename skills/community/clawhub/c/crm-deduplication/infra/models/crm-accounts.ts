import { defineModel } from "@cargo-ai/cdk";

import { crm } from "../connectors/crm";
import { modelsFolder } from "../folders";

// The authoritative account universe, extracted from the CRM itself. The play
// runs on this model so every row it enrolls carries the CRM's own record ID —
// the identifier `mergeRecords` expects. A native or staging model would
// introduce a second identity system, and a merge targeting the wrong one looks
// successful while nothing lands.
//
// `columnSelectionMode: "all"` keeps the properties the duplicate policy reads
// (identity keys, protected IDs, parent company, lifecycle, engagement counts)
// available without naming each one here.
export const crmAccounts = defineModel("crm_accounts", {
  folder: modelsFolder,
  connector: crm,
  extractSlug: "fetchRecords",
  config: { objectType: "companies", columnSelectionMode: "all" },
  schedule: { type: "cron", cron: "0 * * * *" },
});
