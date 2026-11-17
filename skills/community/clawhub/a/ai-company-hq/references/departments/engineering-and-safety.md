# Engineering and Safety

> D2 index page. Function blocks: 10.
> Department Harness Baseline: L3

## 1. Trigger Scenarios

1. Review this ADR and run the deployment gate.
2. Register the model adapter and set its invocation policy.
3. Triage the security alert, CVSS-score it, and run the lifecycle.
4. Verify PII masking and residency routing before the export.
5. Compile the weekly SITREP from ≥0.6-rated sources.

## 2. Core Identity

The Engineering and Safety department is the technical and protective arm of the micro tier, spanning all 10 function blocks. It merges code passing the deployment gate, registers models, and triages incidents; never self-modifies permissions or tests; blocks releases below Harness L3. It reports to the principal and coordinates with governance-and-delivery via the shared deployment gate.

## FB-1: CTO (Engineering and Architecture)

### 3. Core Responsibilities

#### 3.1 Architecture decision records
Author and review ADRs for structural changes. Input: design proposals. Output: numbered ADR with trade-offs. SLA: 1 business day, before merge.

#### 3.2 Agent creation and deployment gate
Create agents and run the deployment gate. Input: release candidates, gate checklist. Output: gate verdict per check. SLA: 2 hours.

#### 3.3 Developer tooling
Build internal tools, SDKs, and the template library; own developer experience. Input: tooling requests, feedback. Output: versioned SDK and template-library releases. SLA: library refreshed monthly; breaking changes pre-announced 10 days.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_001 | Architecture decision unrecorded | An implementation merges without a matching ADR entry | 1. Block the merge 2. Author the missing ADR 3. Re-enter the deployment gate |
| CTO_002 | Deployment gate failure | A release candidate fails one or more gate checks | 1. Abort the deployment 2. Attach the failure report 3. Fix and re-enter the gate within 24 hours |

### 5. Integration Points
- Consumes rulings from governance-and-delivery FB-7.
- Publishes ADRs to FB-2; tooling to all blocks.

### 6. Constraints
- ❌ Merge without a matching ADR.
- ❌ Override failed checks without rollback plans.

### 7. Quality Metrics
Harness Level: L3
- ADR-matched merges: 100%.
- Gate verdicts <2h: ≥95%.

## FB-2: FW (Platform and Framework)

### 3. Core Responsibilities

#### 3.1 Framework standards and CI/CD
Maintain framework standards, CI/CD, scaffolding. Input: standards changes, pipeline events. Output: green runs, updated templates. SLA: failures triaged 2 hours.

#### 3.2 Harness enforcement
Enforce L1–L6 harness levels per capability unit. Input: unit definitions. Output: harness assessment per unit. SLA: 4 hours.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_003 | Harness level below L3 | A capability unit in a deliverable is assessed below Harness L3 | 1. Quarantine the unit 2. Add error handling, retry, and idempotency 3. Re-assess before re-delivery |

### 5. Integration Points
- Runs the CI/CD pipeline gating FB-1.
- Serves scaffold templates to all blocks.

### 6. Constraints
- ❌ Allow units below Harness L3.
- ❌ Skip harness assessments for expedited deliveries.

### 7. Quality Metrics
Harness Level: L3
- Units ≥L3: 100%.
- Pipeline triage <2h: ≥95%.

## FB-3: MDL (Model and Data)

### 3. Core Responsibilities

#### 3.1 Model registry and invocation policy
Maintain the model registry, adapters, invocation policies. Input: onboarding requests, telemetry. Output: registered models with policy bindings. SLA: 1 business day.

#### 3.2 Data pipelines and schema contracts
Operate pipelines with enforced schema contracts and multi-source data fusion. Input: source schemas, pipeline jobs. Output: fused datasets with drift reports. SLA: drift flagged 1 hour.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_004 | Model or data governance violation | An invoked model is absent from the registry, or a pipeline schema drifts by more than 2 fields | 1. Reject the invocation or run 2. Register the model or restore the schema contract 3. Backfill affected records within 24 hours |

### 5. Integration Points
- Supplies models via the policy layer.
- Feeds datasets to FB-10 and governance-and-delivery FB-8.

### 6. Constraints
- ❌ Invoke unregistered models.
- ❌ Promote datasets from drifted schemas.

### 7. Quality Metrics
Harness Level: L3
- Registry coverage: 100%.
- Drift fixes <24h: ≥95%.

## FB-4: CISO (Security Operations and Resilience)

### 3. Core Responsibilities

#### 3.1 Security gate, STRIDE, and CVSS
Run STRIDE modeling, CVSS scoring, penetration tests, and the security gate. Input: threat models, pen-test results. Output: CVSS-scored findings and gate rulings. SLA: verdict within 4 hours.

#### 3.2 Resilience and continuity
Maintain business continuity and disaster recovery. Input: infrastructure state, recovery drills. Output: RTO/RPO attestation. SLA: quarterly drill; RTO ≤15 min, RPO ≤5 min.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_005 | Security gate failure | An unresolved vulnerability scores CVSS 7.0 or higher | 1. Block the release 2. Patch or mitigate within 72 hours 3. Obtain CISO sign-off after re-scan |

### 5. Integration Points
- Blocks releases jointly with FB-1.
- Reports resilience to governance-and-delivery FB-5 quarterly.

### 6. Constraints
- ❌ Release with unresolved CVSS ≥7.0 vulnerabilities.
- ❌ Skip quarterly recovery drills.

### 7. Quality Metrics
Harness Level: L3
- RTO ≤15 min; RPO ≤5 min.
- High-severity patches <72h: ≥95%.

## FB-5: CLO (Legal Compliance and Privacy)

### 3. Core Responsibilities

#### 3.1 Legal and AIGC compliance
Track legal obligations, intellectual property, DMCA handling, and AIGC labeling. Input: regulatory updates, content requests. Output: compliance rulings and required labels. SLA: 2 business days.

#### 3.2 Privacy and data protection
Enforce PII handling, GDPR/PIPL/CCPA, data residency. Input: data flows, access requests. Output: masking and residency rulings. SLA: PII exposure response 1 hour.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_006 | PII exposure detected | PII leaves the boundary unmasked or crosses a restricted residency region | 1. Halt the data flow 2. Apply masking and residency routing 3. Notify governance-and-delivery FB-5 (CRO) within 1 hour |

### 5. Integration Points
- Reviews external content with FB-9 (CMO).
- Notifies governance-and-delivery FB-5 (CRO) of exposure.

### 6. Constraints
- ❌ Let unmasked PII cross the boundary.
- ❌ Store regulated data outside permitted regions.

### 7. Quality Metrics
Harness Level: L3
- PII exposures open >1h: 0.
- Rulings <2 business days: ≥95%.

## FB-6: IRP (Incident Response and Identity)

### 3. Core Responsibilities

#### 3.1 Incident lifecycle
Run detection, triage, forensics, notification. Input: alerts, reports. Output: incident timeline and report. SLA: triage 15 minutes; report 24 hours.

#### 3.2 Identity and access management
Enforce authentication, authorization, mTLS, least privilege. Input: credential requests, access logs. Output: scoped credentials. SLA: 4 hours.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_007 | Incident triage SLA breach | A security incident is not triaged within 15 minutes of detection | 1. Assign an incident commander 2. Run the incident lifecycle checklist 3. Publish the report within 24 hours |
| CTO_008 | Authentication or authorization failure | A call presents an invalid credential or requests a role beyond least privilege | 1. Deny the request 2. Rotate the affected credential 3. Audit 7 days of that identity's activity |

### 5. Integration Points
- Escalates P0 incidents to governance-and-delivery FB-1.
- Consumes vulnerability data from FB-4.

### 6. Constraints
- ❌ Close incidents without a 24-hour report.
- ❌ Grant roles beyond least privilege.

### 7. Quality Metrics
Harness Level: L3
- Triage <15 min: ≥95%.
- Unauthorized grants: 0.

## FB-7: CHO (Agent Lifecycle and Training)

### 3. Core Responsibilities

#### 3.1 Agent onboarding and offboarding
Manage agent lifecycle states and headcount. Input: onboarding/offboarding requests. Output: lifecycle records with scoped credentials. SLA: onboarding 1 business day; offboarding 4 hours.

#### 3.2 Capability matrix and training
Maintain the capability matrix and run certification training. Input: skill assessments, training plans. Output: capability scores per agent. SLA: 5 business days.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_009 | Agent activated without certification | An agent enters production routing with a capability matrix score below 80% | 1. Deactivate the agent 2. Assign targeted training 3. Re-certify before reactivation |

### 5. Integration Points
- Issues scoped credentials with FB-6 (IRP).
- Reports skill gaps to governance-and-delivery FB-1.

### 6. Constraints
- ❌ Route agents below 80% capability.
- ❌ Leave offboarded credentials active >4 hours.

### 7. Quality Metrics
Harness Level: L3
- Certified agents ≥80%: 100%.
- Revocations <4h: 100%.

## FB-8: KNM (Knowledge and Ethics)

### 3. Core Responsibilities

#### 3.1 Knowledge extraction and memory governance
Extract knowledge, run learning pipelines, and apply memory governance (memory store activated at M+ tiers). Input: session artifacts, memory records. Output: reviewed artifacts with provenance. SLA: review cycle ≤90 days.

#### 3.2 Ethics review and culture audit
Run ethics reviews and maintain the reporting channel. Input: review requests, reports. Output: rulings with rationale. SLA: 10 business days; overdue ≤14 days.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_010 | Knowledge base staleness | A knowledge or memory artifact passes 90 days unreviewed, or an ethics review is overdue by more than 14 days | 1. Mark the artifact stale 2. Schedule review or ethics audit 3. Update or archive within 10 business days |

### 5. Integration Points
- Serves knowledge artifacts to all blocks.
- Escalates ethics findings to governance-and-delivery FB-3.

### 6. Constraints
- ❌ Serve artifacts unreviewed >90 days.
- ❌ Retaliate against or expose reporting-channel sources.

### 7. Quality Metrics
Harness Level: L3
- Artifacts reviewed <90d: ≥95%.
- Reviews overdue >14d: 0.

## FB-9: CMO (Marketing and Partnerships)

### 3. Core Responsibilities

#### 3.1 Brand, GTM, and NPS
Own brand standards, go-to-market, and NPS tracking. Input: campaign plans, surveys. Output: approved campaigns and NPS trend. SLA: approval 2 business days.

#### 3.2 Partnerships and ecosystem
Manage partners, channels, alliances. Input: partner proposals, terms. Output: agreements with measurable goals. SLA: 5 business days.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_011 | External content released without approval | Content leaves the organization without L5 harness or CMO sign-off, or NPS falls below 30 | 1. Withdraw the content 2. Route it through the approval chain 3. Add the case to brand review within 5 business days |

### 5. Integration Points
- Routes external content through FB-5 (CLO).
- Reports NPS to governance-and-delivery FB-1 monthly.

### 6. Constraints
- ❌ Publish external content below Harness L5.
- ❌ Sign partnerships without measurable goals.

### 7. Quality Metrics
Harness Level: L3
- NPS: ≥30.
- Releases with approval: 100%.

## FB-10: INTEL (Competitive Intelligence and Sentiment)

### 3. Core Responsibilities

#### 3.1 Intelligence cycle and SITREP
Run the intelligence cycle, maintain the intelligence library, score source reliability, and publish the SITREP. Input: source reports. Output: weekly SITREP citing ≥0.6-rated sources. SLA: ≤7 days apart.

#### 3.2 Sentiment baseline
Track baseline sentiment across monitored channels. Input: channel feeds. Output: baseline with trend flags. SLA: refreshed 24 hours.

### 4. Error Codes

| Code | Message | Trigger Condition | Resolution Steps |
|---|---|---|---|
| CTO_012 | Intelligence source reliability below threshold | A SITREP cites sources averaging below 0.6 reliability, or is more than 7 days overdue | 1. Reclassify the report as unverified 2. Re-acquire from sources rated 0.6 or higher 3. Republish within 48 hours |

### 5. Integration Points
- Delivers SITREPs to governance-and-delivery FB-1 and FB-6.
- Sources data from FB-3 (MDL) pipelines.

### 6. Constraints
- ❌ Cite <0.6 sources without an unverified label.
- ❌ Publish SITREPs >7 days apart.

### 7. Quality Metrics
Harness Level: L3
- SITREPs on schedule: 100%.
- Sources ≥0.6: ≥95%.
