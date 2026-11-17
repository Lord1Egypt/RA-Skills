# Error Codes

> Full error code table for the micro (XS) tier. 34 codes in 3 prefixes: `CEO_` (12), `CTO_` (12), `SCL_` (10).
> `CEO_` codes belong to function blocks of `governance-and-delivery`; `CTO_` codes belong to function blocks of `engineering-and-safety`; `SCL_` is the infrastructure prefix for self-scaling and is not owned by any department.
> Numbering is continuous with no gaps; new codes are appended at the end, never inserted.

## CEO_ Prefix (governance-and-delivery)

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CEO_001 | Strategic decision made without quantified options | A decision brief carries fewer than 2 options with numeric cost and risk estimates | 1. Freeze the decision 2. Return the brief for rework 3. Re-review within 1 business day |
| CEO_002 | Crisis acknowledgment SLA breached | A P0 crisis report is not acknowledged within 15 minutes | 1. Acknowledge and assign a named owner 2. Activate the crisis protocol 3. File a post-mortem within 24 hours |
| CEO_003 | Cross-department SLA breach | A dependency handoff misses its SLA by more than 10% | 1. Notify the COO function block 2. Reschedule capacity within 4 hours 3. Record the breach in the PDCA log |
| CEO_004 | Resource scheduling conflict | Two or more units reserve the same agent capacity for overlapping windows | 1. Detect the conflict on the operations calendar 2. Apply authorization-matrix priority rules 3. Confirm reassignment within 2 hours |
| CEO_005 | Authorization matrix violation | A decision is executed above or outside its defined approval level | 1. Halt the decision 2. Route it to the correct escalation level 3. Log the violation for quarterly board review |
| CEO_006 | Quarterly budget overrun | Spend exceeds the quarterly budget by more than 10% | 1. Freeze non-essential spend 2. Generate a variance analysis within 24 hours 3. Escalate to FB-1 for approval |
| CEO_007 | Cash-flow threshold breach | DSO exceeds 45 days or projected runway falls below 6 months | 1. Halt new capital expenditure 2. Produce a 13-week cash forecast 3. Escalate to FB-3 |
| CEO_008 | Risk threshold breach without circuit breaker | FAIR-assessed exposure exceeds the risk threshold with no breaker tripped | 1. Trip the circuit breaker 2. Re-run the FAIR assessment within 4 hours 3. Report to FB-1 |
| CEO_009 | Vendor cost deviation | A final vendor invoice exceeds the contracted amount by more than 5% | 1. Suspend payments to the vendor 2. Request a written reconciliation 3. Enforce the penalty clause within 5 business days |
| CEO_010 | Quality gate bypassed | An artifact ships without passing all quality gates or with coverage below 85% | 1. Roll back the delivery 2. Re-run the full gate suite 3. Record the bypass in the audit trail |
| CEO_011 | Document completeness failure | A deliverable is missing one or more mandatory documentation sections | 1. Block the release 2. Return it to the authoring unit 3. Re-verify within 1 business day |
| CEO_012 | Information fusion inconsistency | Multi-source lookups disagree on more than 15% of fields, or localization coverage is below 100% | 1. Flag the conflicting fields 2. Re-query the authoritative source 3. Correct the fusion rule within 4 hours |

## CTO_ Prefix (engineering-and-safety)

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_001 | Architecture decision unrecorded | An implementation merges without a matching ADR entry | 1. Block the merge 2. Author the missing ADR 3. Re-enter the deployment gate |
| CTO_002 | Deployment gate failure | A release candidate fails one or more gate checks | 1. Abort the deployment 2. Attach the failure report 3. Fix and re-enter the gate within 24 hours |
| CTO_003 | Harness level below L3 | A capability unit in a deliverable is assessed below Harness L3 | 1. Quarantine the unit 2. Add error handling, retry, and idempotency 3. Re-assess before re-delivery |
| CTO_004 | Model or data governance violation | An invoked model is absent from the registry, or a pipeline schema drifts by more than 2 fields | 1. Reject the invocation or run 2. Register the model or restore the schema contract 3. Backfill affected records within 24 hours |
| CTO_005 | Security gate failure | An unresolved vulnerability scores CVSS 7.0 or higher | 1. Block the release 2. Patch or mitigate within 72 hours 3. Obtain CISO sign-off after re-scan |
| CTO_006 | PII exposure detected | PII leaves the boundary unmasked or crosses a restricted residency region | 1. Halt the data flow 2. Apply masking and residency routing 3. Notify governance-and-delivery FB-5 (CRO) within 1 hour |
| CTO_007 | Incident triage SLA breach | A security incident is not triaged within 15 minutes of detection | 1. Assign an incident commander 2. Run the incident lifecycle checklist 3. Publish the report within 24 hours |
| CTO_008 | Authentication or authorization failure | A call presents an invalid credential or requests a role beyond least privilege | 1. Deny the request 2. Rotate the affected credential 3. Audit 7 days of that identity's activity |
| CTO_009 | Agent activated without certification | An agent enters production routing with a capability matrix score below 80% | 1. Deactivate the agent 2. Assign targeted training 3. Re-certify before reactivation |
| CTO_010 | Knowledge base staleness | A knowledge or memory artifact passes 90 days unreviewed, or an ethics review is overdue by more than 14 days | 1. Mark the artifact stale 2. Schedule review or ethics audit 3. Update or archive within 10 business days |
| CTO_011 | External content released without approval | Content leaves the organization without L5 harness or CMO sign-off, or NPS falls below 30 | 1. Withdraw the content 2. Route it through the approval chain 3. Add the case to brand review within 5 business days |
| CTO_012 | Intelligence source reliability below threshold | A SITREP cites sources averaging below 0.6 reliability, or is more than 7 days overdue | 1. Reclassify the report as unverified 2. Re-acquire from sources rated 0.6 or higher 3. Republish within 48 hours |

## SCL_ Prefix (infrastructure, all tiers fixed)

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| SCL_001 | Upgrade threshold not met | Scaling evaluation metrics fall below the tier thresholds defined in the scaling specification | 1. Keep the current tier 2. Log the evaluation result in the scaling state file 3. Re-evaluate at the next cycle |
| SCL_002 | Upgrade path undefined in merge tree | The current tier has no defined merge path to the requested target tier | 1. Halt the upgrade 2. Report the missing path 3. Request a specification update before retry |
| SCL_003 | Alias collision detected | A proposed department slug matches any historical alias (gate G5) | 1. Reject the upgrade package 2. Rename the colliding slug 3. Re-run the alias integrity gate |
| SCL_004 | Permission self-modification attempted | The upgrade package diff changes the permissions block or the deny and gating scripts (gates G1/G3) | 1. Reject and delete the proposal package 2. Regenerate without permission changes 3. Record the attempt in the audit trail |
| SCL_005 | Test self-modification attempted | The upgrade package contains any path under tests/ (gate G2) | 1. Reject and delete the proposal package 2. Regenerate without test changes 3. Record the attempt in the audit trail |
| SCL_006 | Upgrade package validation failed | The package fails one or more checks of the full acceptance suite (gate G6) | 1. Reject the package 2. Attach the failure item list 3. Fix and re-validate before resubmission |
| SCL_007 | Scaling state file corrupted | The scaling state file is unreadable or fails schema validation | 1. Stop the scaling sequence 2. Restore the state file from backup 3. Re-run the first step of the upgrade sequence |
| SCL_008 | Downgrade requires manual approval | A downgrade request arrives without explicit written approval | 1. Block automatic downgrade 2. Request written justification recorded in tier history 3. Produce a deleted-content mapping table before any file removal |
| SCL_009 | Tier already at maximum (group) | An upgrade is requested while the current tier is group | 1. Reject the upgrade request 2. Report that group is the maximum tier 3. Suggest a horizontal capacity review instead |
| SCL_010 | Function block conservation violated | The function block count after an upgrade differs from the target tier expectation of 18 or 36 (gate G4) | 1. Reject the upgrade 2. Emit the list of missing or extra function blocks 3. Rebuild the package from the merge tree |
