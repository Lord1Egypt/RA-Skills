import { defineModel } from "@cargo-ai/cdk";

import { crm } from "../connectors/crm";
import { modelsFolder } from "../folders";

// The authoritative contact universe. The play runs on CRM record IDs and
// refreshes every candidate from the CRM immediately before any merge.
export const crmContacts = defineModel("crm_contacts", {
  folder: modelsFolder,
  connector: crm,
  extractSlug: "fetchRecords",
  config: { objectType: "contacts", columnSelectionMode: "all" },
  schedule: { type: "cron", cron: "0 * * * *" },
});
