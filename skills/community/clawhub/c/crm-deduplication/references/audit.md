# Audit CRM duplicates

Choose the account path, contact path, or both. Audit every selected path independently before
editing project resources, making a paid call, sending a review request, or writing to the CRM. Approval for one
path does not approve the other.

For every selected path, inspect the authenticated CRM connector, CRM-backed model, object schema,
record ID, identity fields, relevant conflict and protection fields, and existing compatible project
resources. Normalize identifiers exactly as the deployed scripts for that path do:
`infra/scripts/accounts/account.ts` for companies and `infra/scripts/contacts/identity.ts` for
people. Classify each cluster once, rank one deterministic survivor, and record the exact CRM IDs
proposed for merge.

Each selected path produces its own dated JSON artifact, matching Markdown report, and chat summary.
All three representations must agree on source totals, coverage, candidate counts, conflicts,
exclusions, survivor choices, and proposed merge IDs. Record policy approval, disabled deployment
approval, and merge-capable pilot approval separately for each path.

## Path 1: Account deduplication

### Account audit contract

Read current records from the CRM-backed `crm_accounts` model using the selected CRM record ID
(`hs_object_id` in the HubSpot example). Write `crm-account-dedup-audit-YYYY-MM-DD.json` and matching
Markdown with this minimum contract:

```json
{
  "generated_at": "ISO-8601 timestamp",
  "crm": "hubspot|salesforce|attio",
  "source_model_slug": "crm_accounts",
  "record_id_field": "hs_object_id",
  "total_accounts": 0,
  "identifier_coverage": {
    "linkedin_company_id": 0,
    "linkedin_url": 0,
    "domain": 0,
    "no_supported_identifier": 0
  },
  "candidate_clusters": 0,
  "candidate_records": 0,
  "clusters": {
    "exact_unique_linkedin": 0,
    "linkedin_url_review": 0,
    "domain_review": 0,
    "junk_domain_review": 0,
    "parent_or_subsidiary_review": 0,
    "conflict": 0
  },
  "conflicts": {
    "identity_conflict": 0,
    "protected_id_conflict": 0
  },
  "policy": {
    "status": "pending_operator_approval|approved",
    "protected_id_fields": [],
    "score": {
      "linkedin_company_id": 60,
      "linkedin_url": 25,
      "non_generic_domain": 15
    },
    "automatic_merge_class": "exact_unique_linkedin_without_conflict",
    "survivor_precedence": [
      "protected_id",
      "customer",
      "open_opportunities",
      "contacts",
      "activities",
      "populated_properties",
      "last_activity_at",
      "created_at",
      "record_id"
    ],
    "review_owner": "operator-approved owner",
    "review_channel": "operator-approved Slack channel"
  },
  "operator_approval": {
    "account_policy": false,
    "disabled_deployment": false,
    "merge_capable_pilot": false
  }
}
```

Account Markdown headings are `Summary`, `Identifier coverage`, `Match classes`, `Conflicts and
exclusions`, `Score and automatic gate`, `Survivor policy`, `Approvals`, and `Sample review queue`.
Every table reports count, percentage of audited accounts, and sampled CRM record IDs.

### Account candidate classes

Use only normalized LinkedIn company ID, LinkedIn URL or handle, and non-generic domain as candidate
keys. Company name alone is not a candidate key and never contributes to the score.

| Candidate                                                                                                                | Execution path                                                  |
| ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| Exact LinkedIn company ID on every record, with no conflicting identity, protected ID, or parent-subsidiary relationship | Automatic merge after score and fresh CRM search                |
| LinkedIn URL or handle only                                                                                              | Human Review                                                    |
| Domain only                                                                                                              | Human Review                                                    |
| Junk or shared domain                                                                                                    | Ignore as a key; another supported key determines the route     |
| Parent, subsidiary, brand, division, or regional entity                                                                  | Human Review                                                    |
| Conflicting identity or protected ID                                                                                     | Human Review or decline                                         |
| AI-assisted judgement                                                                                                    | Evidence for Human Review only                                  |

Count `identity_conflict` and `protected_id_conflict` separately. Present detected billing,
customer, and external-system identifiers before asking the operator to approve protected fields
and account survivor precedence.

### Account audit complete when

- identifier coverage and candidate counts agree across account JSON, Markdown, and chat
- every account candidate cluster contains at least two distinct CRM record IDs
- company name never creates or scores a candidate
- every account cluster has one mutually exclusive class and one deterministic survivor
- protected-ID, parent-subsidiary, and non-null identity conflicts are visible
- weak matching-key coverage produces a recommendation to run `crm-enrichment`, not name matching
- account policy, disabled deployment, and merge-capable pilot approvals are recorded independently

## Path 2: Contact deduplication

### Contact audit contract

Read current records from the CRM-backed `crm_contacts` model using the selected CRM record ID
(`hs_object_id` in the HubSpot example). Write `crm-contact-dedup-audit-YYYY-MM-DD.json` and matching
Markdown with this minimum contract:

```json
{
  "generated_at": "ISO-8601 timestamp",
  "crm": "hubspot|salesforce|attio",
  "source_model_slug": "crm_contacts",
  "record_id_field": "hs_object_id",
  "total_contacts": 0,
  "identifier_coverage": {
    "linkedin_person_id": 0,
    "linkedin_url": 0,
    "email": 0,
    "phone": 0,
    "no_supported_identifier": 0
  },
  "candidate_clusters": 0,
  "candidate_records": 0,
  "matched_classes": {
    "exact_linkedin_person_id": 0,
    "exact_linkedin_url": 0,
    "exact_non_generic_email": 0,
    "transitive_high_confidence": 0
  },
  "low_confidence_groups": {
    "phone_only": 0,
    "generic_or_shared_email": 0,
    "linkedin_conflict": 0,
    "other_ambiguous": 0
  },
  "excluded_records": {
    "stale_or_invalid": 0
  },
  "conflicts": {
    "linkedin_identity_conflict": 0,
    "generic_or_shared_email": 0
  },
  "policy": {
    "status": "pending_operator_approval|approved",
    "score": {
      "linkedin_person_id": 60,
      "linkedin_url_without_person_id_conflict": 60,
      "non_generic_email_without_linkedin_conflict": 60,
      "conflict_free_transitive_chain": 60
    },
    "automatic_merge_classes": [
      "exact_linkedin_person_id",
      "exact_linkedin_url_without_person_id_conflict",
      "exact_non_generic_email_without_linkedin_conflict",
      "conflict_free_transitive_chain"
    ],
    "global_automatic_guards": [
      "no_linkedin_identity_conflict",
      "no_generic_or_shared_email"
    ],
    "low_confidence_disposition": "human_review|leave_untouched",
    "survivor_precedence": [
      "associated_deals",
      "activity",
      "created_at",
      "populated_properties",
      "record_id"
    ],
    "review_owner": "required when disposition is human_review",
    "review_channel": "required when disposition is human_review"
  },
  "operator_approval": {
    "contact_policy": false,
    "disabled_deployment": false,
    "merge_capable_pilot": false
  }
}
```

`matched_classes` counts may overlap because one cluster can share several approved identity keys.
Count every candidate cluster once in `candidate_clusters`, and list every true class on that
cluster's evidence row.

Contact Markdown headings are `Summary`, `Identifier coverage`, `Matched classes`, `Conflicts and
exclusions`, `Direct and transitive clusters`, `Score and automatic gate`, `Survivor policy`,
`Approvals`, and `Sample review queue`. Every table reports count, percentage of audited contacts,
and sampled CRM record IDs.

### Contact normalization and candidate classes

Normalize email by trimming and lowercasing. Normalize LinkedIn URLs to the `/in/<handle>` handle and
audit all four runtime URL forms with and without `www` and a trailing slash. The direct CRM search
starts with the source phone exactly as stored. The transitive search uses normalized
phone values derived from direct results. Within records already retrieved, phone comparison covers
explicit international numbers, `00` prefixes, NANP numbers, and the approved French and UK local
forms. Phone-only matches stay low confidence after normalization.

Person name, job title, company association, and fuzzy similarity are evidence for a reviewer only.
They never create or score a contact candidate.

| Candidate                                                                                     | Execution path                                   |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Exact LinkedIn person ID with no global automatic guard failure                               | Automatic merge after score and fresh CRM search |
| Exact LinkedIn URL with no person-ID conflict or global automatic guard failure               | Automatic merge after score and fresh CRM search |
| Exact non-generic email with no LinkedIn conflict or global automatic guard failure           | Automatic merge after score and fresh CRM search |
| Transitive chain of supported high-confidence keys with no global automatic guard failure     | Automatic merge after score and fresh CRM search |
| Phone-only cluster                                                                            | Human Review or leave untouched, per policy      |
| Any cluster with a LinkedIn identity conflict or generic/shared email                         | Human Review or leave untouched, per policy      |
| AI-assisted judgement                                                                         | Evidence for Human Review only                   |

Apply LinkedIn identity conflict and generic/shared-email guards to the whole automatic decision,
including clusters that also share a person ID. Rank one survivor by associated deals, activity,
oldest creation time, populated properties, then CRM record ID.

### Contact audit complete when

- identifier coverage and candidate counts agree across contact JSON, Markdown, and chat
- every contact candidate cluster contains at least two distinct CRM record IDs
- every direct or transitive group has distinct CRM IDs and a complete list of matched classes
- every contact cluster has one deterministic survivor and exact child IDs proposed for merge
- LinkedIn identity conflicts and generic/shared-email risks are visible as global guards
- person name, job title, company association, and fuzzy similarity never create or score a candidate
- phone-only groups remain outside the automatic path
- the approved low-confidence disposition and any required review owner and channel are recorded
- contact policy, disabled deployment, and merge-capable pilot approvals are recorded independently
