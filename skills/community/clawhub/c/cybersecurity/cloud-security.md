# Cloud And SaaS Security

The control plane is the perimeter: one API call with the right credential does what used to require physical access. Identity first, logging second, network third — in that order, because that is the order intrusions actually take.

**Before reviewing a tenant**, read `## Environment` in `~/Clawic/data/cybersecurity/memory.md` for the accounts, subscriptions and SaaS tenants already mapped, and `## Scope & Authorization` — a client's tenant, a personal account, or an acquired company's estate each needs its own written authorization. `primary_cloud` in `config.yaml` selects the column below; `multi` means running the review per provider rather than averaging them.

**Contents:** [The Universal Control Set](#the-universal-control-set) · [Provider Specifics That Change The Answer](#provider-specifics-that-change-the-answer) · [Logging You Cannot Obtain Retroactively](#logging-you-cannot-obtain-retroactively) · [The Exposure Sweep](#the-exposure-sweep) · [Keys, Roles And The Leak Runbook](#keys-roles-and-the-leak-runbook) · [SaaS Tenants Are Cloud Too](#saas-tenants-are-cloud-too) · [Shared Responsibility, Concretely](#shared-responsibility-concretely) · [Kubernetes: The Five That Matter](#kubernetes-the-five-that-matter) · [Cloud Incident Response Differences](#cloud-incident-response-differences) · [Guardrails Over Findings](#guardrails-over-findings)

## The Universal Control Set

Provider-independent, ordered by attack path removed:

1. **No long-lived credentials anywhere.** Workload identity for machines (instance roles, managed identities, workload identity federation, IRSA), federated SSO for humans. Every static key is a credential waiting to appear in a repository, a log, or a laptop backup.
2. **MFA on every human identity, phishing-resistant for administrators**, and the root or global-administrator account locked away with MFA, no keys, and an alarm on any use.
3. **Break-glass account tested and alarmed** — one per tenant, credentials split and stored physically, excluded from conditional access by design and monitored precisely because of that exclusion.
4. **Audit logging on, exported out of the account, retained beyond your dwell time**, and the export protected from the account's own administrators.
5. **Block public access at the account level**, not per resource — a per-resource setting is a decision somebody will get wrong at 6pm on a Friday.
6. **Guardrails as policy**: organization-level policies that make the dangerous configuration impossible rather than detectable. Region restriction, deny disabling audit logging, deny deleting the log destination, deny creating static credentials.
7. **Separate accounts or subscriptions per environment.** The account boundary is the only hard blast-radius boundary a cloud provider offers; tags and good intentions are not a boundary.
8. **Cost anomaly alerting**, which doubles as a security control: a stolen credential's first act is typically expensive compute.

## Provider Specifics That Change The Answer

| Concern | AWS | Azure / Entra | Google Cloud |
|---|---|---|---|
| Hard boundary | Account, inside an Organization with SCPs | Subscription, with management groups and Azure Policy | Project, with folders and organization policies |
| Human access | Identity Center / federation, not IAM users | Entra ID with conditional access and PIM | Cloud Identity with context-aware access |
| Workload identity | Instance profiles, IRSA/Pod Identity, OIDC federation from CI | Managed identities, workload identity federation | Service accounts with workload identity, keyless where possible |
| The escalation everyone misses | `iam:PassRole` combined with a compute-launch permission is effectively administrator | Owner on a subscription, plus consent to an application with directory write | `iam.serviceAccountUser` / `actAs` plus deploy permission, and project-level `editor` |
| Metadata service | IMDSv2 with hop limit — the SSRF control | Requires a header; still SSRF-reachable if the app forwards headers | Requires a metadata header |
| Audit log | CloudTrail management events; data events cost extra and are off | Entra sign-in and audit; Activity log; diagnostic settings for the rest | Admin Activity free; **Data Access logs are opt-in and are the ones you need** |
| The public-exposure trap | S3 bucket and object ACLs, snapshots, AMIs, RDS public accessibility | Storage account public blob access, NSG any-any, public SQL endpoint | Bucket IAM with `allUsers`, firewall rules with `0.0.0.0/0`, public Cloud SQL |
| Free high-value detection | GuardDuty | Defender for Cloud, Entra ID Protection | Security Command Center, Event Threat Detection |

Cross-provider constant: **the identity model is where the account is lost**, and the specific escalation path in row four is the one that appears in real incidents rather than in checklists.

## Logging You Cannot Obtain Retroactively

The defining cloud forensics constraint — the evidence is a setting somebody made months ago, and there is no way to reconstruct it after the fact.

- **Data-plane access logging is off by default in every provider.** Without it, "did they read the bucket?" is permanently *unknown*, and *unknown* is what has to be told to a regulator. Turn it on for the buckets and databases that hold regulated data at minimum; the cost of full data-event logging is real, and this is a deliberate scoping decision, not an oversight to leave for later.
- Export audit logs to a separate account or project with a different administrative boundary. An intrusion with administrative rights deletes the logs in the account it owns, and that deletion is the last thing you see.
- Retention beyond your realistic dwell time. Provider default consoles keep management events for a matter of months and data events for nothing.
- SaaS audit depth is frequently a licence tier rather than a setting — the mailbox per-item access log being the canonical example. Discovering this during an incident is how "what did they read" becomes unanswerable.
- Enabling logging is cheap; the storage is what costs. Tier it — hot for 30 days, cheap archive for a year — rather than choosing between full and none.

## The Exposure Sweep

Run this per account, per environment, and record the result rather than the process:

| Check | What it catches |
|---|---|
| Account-level public-access block enabled on storage | The bucket somebody makes public next month |
| Public storage objects, snapshots, machine images, and database endpoints | The classic data-exposure headline |
| Security groups / NSGs / firewall rules open to 0.0.0.0/0 on management or database ports | Internet-reachable databases and RDP/SSH |
| Metadata service hardening enforced, including in launch templates and node pools | SSRF to credentials — the discontinuous-impact bug |
| Static keys: count, age, last use | Every key over 90 days old, and every key never used, is pure liability |
| Root / global admin: MFA on, no keys, no recent use | The one finding an auditor always writes up |
| Identity policies with wildcard actions on wildcard resources, and the `PassRole`-class escalations | Effective administrator hiding behind a modest-looking role |
| Audit logging enabled, exported, and undeletable by the account | Whether an incident here would be investigable at all |
| Unused regions restricted by policy | Cryptomining in the region nobody watches |
| External-access analysis: resources shared outside the organization | Cross-account trust nobody remembers granting |
| Cost anomaly and budget alerts configured | The cheapest compromise detector in the account |

The output is a `## Findings` row per gap and an updated `## Environment` — not a screenshot of a dashboard.

## Keys, Roles And The Leak Runbook

When a credential leaks — in a repository, a log, a support ticket, a public bucket, a Slack message:

1. **Deactivate rather than delete** first, so the audit trail of what used it stays intact and you can still attribute activity.
2. **Determine what it could do**, not what it was for. The blast radius is the permission set, and the answer is almost always broader than the developer believed.
3. **Search the audit log for its use** across the whole retention window, filtered to sources outside your normal ranges. Public leak to exploitation is measured in minutes — automated scrapers monitor public repositories continuously.
4. **Look for what the credential created**: new users, new keys, new roles, new instances (especially in unused regions), new trust relationships, modified logging.
5. **Rotate properly**: create the replacement, migrate consumers, verify the new one in the logs, then delete the old. The delete step is the one that gets skipped, which means the rotation never happened.
6. **Fix the cause**: the key existed because a workload used a static credential. Replace it with workload identity, or the same incident is scheduled.
7. Record the incident and the pointer — `env:AWS_ACCESS_KEY_ID`, `ssm:/prod/db/password` — never the value.

Public-repository leaks additionally need history rewriting *and* rotation; rotation alone is the fix, and history rewriting alone is cosmetic.

## SaaS Tenants Are Cloud Too

Often more data than the cloud account and reviewed a fraction as often. Per tenant:

- SSO enforced for all users, with a check that local password login is actually disabled rather than merely unused — the local login path surviving SSO adoption is the standard finding.
- Admin roles enumerated with an owner each; SaaS admin sprawl is invisible until an audit.
- **OAuth applications connected to the tenant**: which third parties hold a token, with what scopes, granted by whom, and used when. Users self-granting file and mail scopes to random productivity apps is the shadow-IT surface with an actual credential attached.
- Public sharing settings: file links set to "anyone with the link", public workspace pages, guest accounts with no expiry, and a periodic sweep of what is externally shared.
- API tokens and webhooks created by users, which survive offboarding.
- Audit log availability and retention, plus whether the export can be automated on the current tier.
- Offboarding covers SaaS, not just the identity provider. An app not behind SSO keeps working after the account is disabled.

## Shared Responsibility, Concretely

The phrase is used to avoid decisions; the useful version is a table naming who does what for your architecture:

| Model | Provider handles | You always handle |
|---|---|---|
| IaaS | Hypervisor, physical, network fabric | OS patching, configuration, identity, data, network rules, logging, backup |
| Containers as a service | Host and runtime | Image contents, workload identity, network policy, secrets, registry |
| Serverless | Runtime and scaling | Code, dependencies, function permissions, event-source configuration, secrets |
| SaaS | Everything technical | **Identity, access, configuration, data classification, sharing, and offboarding** |

The SaaS row is the one people get wrong: the provider secures the platform, and every breach you will actually experience there is an identity or configuration failure on your side.

## Kubernetes: The Five That Matter

1. **The API server must not be publicly reachable** without authentication and network restriction. An exposed unauthenticated API is cluster takeover in one request.
2. **RBAC**: `cluster-admin` bound to a service account, wildcard verbs on wildcard resources, and the ability to create pods in a namespace with privileged service accounts — all of which are administrator by another name. Pod-create is the escalation primitive, because a pod can mount any service account in that namespace.
3. **Workload identity, not mounted static cloud credentials.** A pod with a node's cloud role inherits everything the node can do.
4. **Secrets are base64-encoded, not encrypted**, unless encryption at rest and an external secrets store are configured. Anyone with read on secrets in a namespace has the credentials.
5. **Network policy default-deny**, because the default is that every pod can reach every pod and the flat network problem reappears inside the cluster.

Plus the boring one that carries most of the risk: node and control-plane patching, and the images you run (`supply-chain.md`).

## Cloud Incident Response Differences

- **Containment is an API call**: detach the policy, deactivate the key, apply a deny policy to the principal, isolate the instance's security group. Faster and more reversible than anything on-premises.
- **Preserve before terminating.** Snapshot volumes, capture memory where the platform allows, and export the relevant audit slice before anything is deleted — auto-scaling will otherwise destroy the evidence while you are typing.
- Evidence lives in the control plane rather than on the host: the audit log is the timeline, and the instance is often secondary.
- **Assume the credential reached everything the credential could reach.** Enumerate by permission, not by observed activity, and treat unlogged data-plane access as unknown.
- The provider holds logs you cannot get retroactively; open a support case on day one, in writing.
- Cross-account trust and organization-level roles extend the blast radius past the compromised account. Enumerate the trust relationships early, before declaring scope.

## Guardrails Over Findings

A finding is fixed once; a guardrail is fixed forever. Convert every recurring finding into a preventive control:

- Organization-level policy denying the configuration outright — region restriction, denying static-key creation, denying audit-log deletion, denying public storage. This is the strongest available control and it is free.
- Infrastructure-as-code policy checks in CI, so the misconfiguration never merges (`supply-chain.md` covers the pipeline itself).
- Secure-by-default modules and templates that the platform team owns; developers get the paved path and the exception requires a conversation.
- Automated remediation for the small set where the fix is unambiguous — public bucket closed, unused key deactivated — with an alert so it is visible rather than silent.
- **Test the guardrail** by trying to do the thing. An untested policy is a belief, and organization-level policies fail in surprising ways: they do not apply to the management account, they do not apply retroactively, and a misconfigured one at the root is an outage with a slow rollback.

Write it (`memory-template.md`): accounts, subscriptions, SaaS tenants, their owners, the logging state and retention, and which crown-jewel data each holds, in `## Environment`; instances and appliances in `~/Clawic/data/servers/servers.md`; each gap as a `## Findings` row with owner, due date and the attack path it removes; each SaaS provider with a token or your data as a row in `## Vendors` with tier and review date, plus its security contact in `~/Clawic/data/contacts/contacts.md`; the key-rotation, access-review and exposure-sweep cadences as `## Due` rows; the tenant baseline and the guardrail policy set — once derived — in `~/Clawic/data/cybersecurity/artifacts/` with its `## Boxes` line in the same turn. Account ids, ARNs, resource names and profile names are identifiers and belong in the record; keys, tokens and connection strings never do — the pointer only.
