import { defineConnector } from "@cargo-ai/cdk";

import { crmWriteback } from "../settings";

// The CRM the tier is written back to, declared only when `crmWriteback.crm`
// in `settings.ts` names one. With `none` nothing is declared, so a workspace
// with no CRM connection plans and deploys exactly as before.
//
// Bound, not created: `default: true` links the workspace's existing HubSpot or
// Salesforce connector (`cargo-ai project add connector/hubspot`), the same way
// crm-enrichment binds its `crm`. A workspace without that connection fails at
// deploy, not at plan, because binding declares no `config` to typecheck. When
// crm-enrichment is installed too, both files declare the slug `crm`: delete
// this one and import theirs, since one slug declared twice collides at deploy.
export const crm =
  crmWriteback.crm === "none"
    ? undefined
    : defineConnector("crm", {
        integration: crmWriteback.crm,
        default: true,
      });
