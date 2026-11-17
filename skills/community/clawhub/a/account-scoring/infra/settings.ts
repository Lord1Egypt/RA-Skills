// The two settings an operator changes without touching the graph. Everything
// else in this skill is wired from them, so edit here, run `cargo-ai project plan`,
// and read what moved.

// How long a tier stands before the play judges the company again. The play
// filter enrols a row whose `tiered_at` is older than this, so it is the
// re-score cadence, and every account is re-billed once per window.
//
// The value is a segment filter's relative date: "<n> days", "<n> months" or
// "<n> years", compared by calendar day. "7 days" is weekly, "30 days" monthly.
// Write weeks as days: "1 week" is not a date unit the filter accepts.
export const rescoreAfter = "6 months";

// Where the tier goes besides the row. `none` writes only onto the Cargo model,
// which is what this skill did before the setting existed, and declares no CRM
// connector at all.
//
// `hubspot` or `salesforce` adds one update after the row write: it finds the
// CRM company matching this row and sets the three fields named below. It
// never creates a record, and it never writes a field you did not name here.
// When the match value finds more than one CRM company, it writes to none of
// them (`isFailingOnMultipleMatches` on the update, in the play).
// The fields must exist in the CRM before the first run (see SKILL.md,
// `crm-writeback`).
export type CrmWriteback =
  | { crm: "none" }
  | {
      crm: "hubspot" | "salesforce";
      // Which value of the row finds the CRM company.
      //   "domain": the row's `domain`. HubSpot matches it on `domain`.
      //     Salesforce has no standard domain field, so name the Account field
      //     that holds a bare domain (often a custom `Domain__c`); `Website`
      //     holds URLs and will not match.
      //   "id": the row's `id`, only when the play runs on a CRM companies
      //     model, whose row id is the CRM record id. On `tam_companies` the
      //     id is Cargo's own and matches nothing.
      matchOn: "domain" | "id";
      // The CRM property compared to that value: `domain` or `hs_object_id`
      // on HubSpot, your domain field or `Id` on Salesforce.
      matchProperty: string;
      // The CRM properties written. Create them first: HubSpot company
      // properties, or Salesforce Account fields. Text for tier and reason,
      // date or datetime for the stamp.
      fields: { tier: string; reason: string; scoredAt: string };
    };

export const crmWriteback: CrmWriteback = { crm: "none" };

// A HubSpot example, by domain, for a play running on `tam_companies`:
//
// export const crmWriteback: CrmWriteback = {
//   crm: "hubspot",
//   matchOn: "domain",
//   matchProperty: "domain",
//   fields: {
//     tier: "cargo_tier",
//     reason: "cargo_tier_reason",
//     scoredAt: "cargo_tiered_at",
//   },
// };
