import { defineConnector } from "@cargo-ai/cdk";

// The CRM slot. The checked example is HubSpot: `fetchRecords` extracts the
// account model, `findRecords` searches for live duplicates, and `mergeRecords`
// performs the merge. Salesforce or Attio replaces the integration, the
// extractor, the record-ID field, and both action slugs — one CRM shape per
// project, never parallel branches.
//
// Binds the workspace's DEFAULT HubSpot connector rather than creating one:
// authorize it once (`cargo-ai project add connector/hubspot`) and this
// declaration resolves to it.
export const crm = defineConnector("crm", {
  integration: "hubspot",
  default: true,
});
