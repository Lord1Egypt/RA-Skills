# Security — Exposure, Encryption, Detection, and the Leak Runbook

Identity is the perimeter, and the permissions half of the subject — hierarchy, deny policies, service accounts, keys, federation — is a separate route from the Quick Reference (`iam.md`). This file covers exposure, encryption, perimeters, detection, and what to do when a credential leaks.

**Contents:** [Threat Model in Three Lines](#threat-model-in-three-lines) · [The Exposure Sweep](#the-exposure-sweep) · [Encryption](#encryption) · [Secret Manager](#secret-manager) · [VPC Service Controls](#vpc-service-controls) · [Detection Stack, in Cost Order](#detection-stack-in-cost-order) · [Audit Logs](#audit-logs) · [Leaked Credential Runbook](#leaked-credential-runbook) · [Compliance Regimes](#compliance-regimes) · [Audit Checklist](#audit-checklist)

## Threat Model in Three Lines

1. **A credential leaks** — a service account key in a repository, an over-permissive federation condition, a key in a container image. This is the overwhelming majority of real GCP incidents, and the service account key is the specific artifact involved.
2. **Something is public that should not be** — a bucket, a dataset, a VM with an external IP and an open port, a Cloud Run service with unauthenticated invocation, an IAM binding to `allUsers` or to a personal Gmail address.
3. **Cost is the payload** — a stolen credential's first act is usually to launch expensive compute for mining, which is why the budget anomaly alert doubles as a security alert (`costs.md`).

Everything below is ordered against those three, cheapest control first.

## The Exposure Sweep

Run on any inherited project, and quarterly thereafter. Each row is a question with a definite answer.

| Surface | What to look for |
|---|---|
| IAM principals | Anyone outside the organization's domain; `allUsers` and `allAuthenticatedUsers` anywhere; `roles/owner` and `roles/editor` on humans or service accounts |
| Service account keys | Any key at all; keys older than the expiry policy; keys authenticating from unexpected locations |
| Buckets | Public access prevention off; uniform bucket-level access off; any public object ACL surviving from before |
| BigQuery | Datasets or views shared with `allAuthenticatedUsers`; authorized views that expose more than intended |
| Cloud SQL | Any instance with a public IP; any authorized network wider than a single host |
| Firewall | Ingress from `0.0.0.0/0` on 22, 3389, or any database port; broad allow rules with no target |
| VMs | External IPs; OS Login off; serial port access enabled; Shielded VM off |
| Cloud Run / Functions | Unauthenticated invocation on services that are not meant to be public; ingress not restricted to internal or the load balancer |
| Artifact Registry | Repositories readable by `allUsers`; images with embedded credentials |
| Org policies | The day-one list not enforced, or enforced with undocumented exceptions (`organization.md`) |
| Secrets in code | Keys, tokens and connection strings in repositories, container images, environment variables, and Terraform state |

Terraform state deserves its own line: it stores resource attributes in plain text, including generated passwords and some secret values. The state bucket needs the same protection as a secret store — private, versioned, encrypted, and access-restricted to the automation identity (`iac.md`).

## Encryption

- **At rest, always on.** Every GCP storage service encrypts by default with Google-managed keys. The question is never whether, only who holds the key.
- **CMEK** puts a Cloud KMS key you control in the path. It gives you the ability to revoke access by disabling the key, an audit trail of key use, and the answer most compliance questionnaires want.
- **CMEK is largely a creation-time decision.** A bucket, a dataset, a disk or a Cloud SQL instance created without it usually needs to be recreated and the data copied. Decide it with the compliance regime, before the first resource.
- **Key rings and keys cannot be deleted, ever.** Only key versions are destroyed, after a scheduled delay. Naming is permanent — plan it, because the mistake is visible forever.
- Key location must match, or be compatible with, the resource's location. A global key ring and a regional bucket is a common first-attempt failure.
- **The service agent needs a grant.** Each product uses a per-project service agent identity to call KMS; without `roles/cloudkms.cryptoKeyEncrypterDecrypter` for that agent, resource creation fails with an error naming a principal nobody remembers creating. This is also the detail that breaks a restore into a new project (`databases.md`).
- In transit: Google-to-Google traffic is encrypted; your own service-to-service traffic inside the VPC is not encrypted by default at the application layer. Where a regime requires it, that is mTLS or a mesh, and it is your work.

## Secret Manager

- Per-secret-version storage cost plus per-access cost — materially cheaper than the equivalent on other clouds, so "we'll use environment variables to save money" is not an argument here.
- **Versions are immutable.** Rotation adds a version and disables the old one; nothing is overwritten. Reference `latest` for convenience or a pinned version for reproducibility, and know which you chose — `latest` means a rotation changes behaviour without a deploy.
- Grant `roles/secretmanager.secretAccessor` **on the individual secret**, never at project level. Project-level access to secrets is access to all of them.
- Mount secrets into Cloud Run and GKE rather than baking them into environment variables in a revision or a manifest: an environment variable is visible in the resource's configuration to anyone who can read it, and it persists in every revision's history (`run.md`).
- Enable rotation notifications where the secret has a rotating counterpart. A rotation schedule with no consumer is a reminder, not a mechanism.
- **Secret names are not secrets.** Record the name and the pointer in this skill's boxes, never the value: `gcp-sm:projects/<project>/secrets/<name>` (`memory-template.md`).

## VPC Service Controls

A perimeter around Google APIs for a set of projects. It is the control that addresses exfiltration by an authorized identity — the case IAM cannot cover, because the credential is legitimate.

- Inside a perimeter, calls to protected services from outside are denied even with valid credentials and correct IAM. That is the entire value, and the entire operational cost.
- **Denials are deliberately opaque**: a vague 403 with a unique request identifier. The audit log entry names the perimeter and the service; the API response does not. Anyone debugging without knowing a perimeter exists will spend hours in IAM (`debug.md`).
- **Dry-run mode first, for weeks.** A perimeter dropped onto a live estate breaks CI, the console, third-party integrations and half the data pipelines simultaneously. Dry-run logs what would have been blocked without blocking it.
- Access levels (by IP range, device posture, or identity) are how humans and CI reach in. Ingress and egress rules are how specific cross-perimeter flows are allowed.
- Perimeter-protected access to Google APIs requires the restricted VIP and matching private DNS entries, which is a networking change, not a security setting (`networking.md`).
- Justified by: regulated data, a genuine insider-exfiltration threat model, or a contract that names it. Not justified by a general wish to be more secure — the operational cost is high and it is paid by everyone, daily.

## Detection Stack, in Cost Order

Add in this order, and stop where the value stops.

1. **Free and immediate**: org policies (`organization.md`), Admin Activity audit logs (always on), budget and anomaly alerting as a security signal, Recommender's IAM findings for over-grants.
2. **Cheap and high value**: log-based alerts on the events that matter — service account key created, org policy changed, IAM policy changed at the org or folder, firewall rule opened to `0.0.0.0/0`, billing account detached. Each is one log filter and one alert policy, and each catches a real incident class.
3. **Security Command Center Standard**: built-in vulnerability and misconfiguration findings across the organization at no additional charge for the basic tier. Turn it on and triage the findings — most organizations have several days of work waiting there.
4. **Paid tiers and add-ons**: threat detection over audit logs and container behaviour, sensitive-data discovery, attack path simulation. Real value at real cost; adopt when there is a team to act on the findings, because unread findings are worse than none.
5. **Sensitive data discovery** over buckets and BigQuery: scans cost per amount inspected. Scope it to the datasets that might contain personal data rather than running it over everything.

## Audit Logs

| Category | Default | Cost | Note |
|---|---|---|---|
| Admin Activity | Always on, cannot be disabled | Free | Every write operation, with principal and parameters. The evidence always exists |
| Data Access | Off by default, except BigQuery data access which is on and free | Billable ingestion | Enabling org-wide is a classic Logging bill; enable per service, per project, where the data is |
| System Event | On | Free | Google-initiated actions such as live migration |
| Policy Denied | On | Billable | Where org policy and VPC-SC denials appear — the log to read when a 403 makes no sense |

- Route logs to a central sink in a dedicated project, with the retention the regime requires. The `_Required` bucket keeps admin activity for a long fixed period at no cost; anything longer or broader is a bucket you configure and pay for.
- Sinks to Cloud Storage are cheap archival; sinks to BigQuery make logs queryable and then they are a BigQuery cost (`bigquery.md`).
- **Exclusion filters are the cost control.** Health checks, readiness probes and debug-level application logs are the usual top talkers, and excluding them at the sink saves more than any retention change (`costs.md`).
- Log bucket retention and log-based metrics are independent: a metric derived from logs survives the logs being excluded from storage, which is the cheap way to keep the signal without the volume.

## Leaked Credential Runbook

When a service account key, an API key, or an OAuth secret is exposed. Order matters — containment first, forensics second.

1. **Disable the key immediately**, before deleting it. Disabling is reversible and stops use instantly; deleting destroys evidence and can be harder to explain later.
2. **Check what the identity could do.** Read the service account's roles and every binding naming it, including at folder and org level. Assume everything it could do, it did.
3. **Look for the payload.** Newly created VMs, especially large or accelerator-backed ones, in regions you do not use. New service accounts and new keys. Changed IAM bindings. New firewall rules. Buckets read or copied. Query the audit log filtered to that principal for the full exposure window.
4. **Check the bill.** Cost anomaly detection often shows the incident before anything else does, and the spend curve gives the start time precisely.
5. **Rotate everything the identity could reach**: database passwords, downstream API keys, anything in the secrets it could access. A key that could read Secret Manager compromises every secret it could read.
6. **Close the path.** Where did the key come from and why did it exist? The fix is almost always removing the need for a key at all — Workload Identity Federation, impersonation, or an attached service account (`iam.md`).
7. **Then delete the key**, and enforce `constraints/iam.disableServiceAccountKeyCreation` so the next one cannot be created.
8. **Write the runbook.** Save the timeline, the queries used, what was found and what was rotated to `~/Clawic/data/gcp/artifacts/runbook-credential-leak.md` — with every secret replaced by its pointer — and add its `## Boxes` line. The second incident should be an hour, not a day.

## Compliance Regimes

`compliance_regime` changes defaults rather than adding a step at the end.

| Regime | What it forces |
|---|---|
| `hipaa` | Only covered services, a signed agreement in place, CMEK, Data Access logging with long retention, and no data in services outside the covered list |
| `pci` | Network segmentation, restricted access with documented justification, long log retention, and evidence of quarterly review |
| `soc2` | Access review evidence, change management through IaC, alerting and incident records, and the audit trail to prove all three |
| `gdpr-eu` | Resource locations constrained to EU regions (`constraints/gcp.resourceLocations`), a data-processing agreement, retention limits, and deletion that is actually executed |

Common to all: CMEK decided at creation, Data Access logging enabled where the regulated data lives, resource locations constrained, and access reviewed on a cadence recorded in `## Due`. The service eligibility list is the part to check first — designing on a service the regime does not cover wastes the whole design.

## Audit Checklist

| Check | How |
|---|---|
| Domain-restricted sharing enforced; no external principals | Org policy state, then a scan of every policy for principals outside the domain |
| No service account keys, or all within expiry policy | Key list per service account, with dates |
| Default compute service account stripped of bindings | Per project, by project number |
| Public access prevention and uniform bucket access on every bucket | Bucket configuration, org policy state |
| No public IP on Cloud SQL; no `0.0.0.0/0` on 22, 3389, or database ports | Instance list, firewall rules |
| No unauthenticated Cloud Run services that are not deliberately public | Service IAM policies |
| OS Login required; serial port access disabled; Shielded VM on | Org policy state, instance configuration |
| Admin Activity logs routed to a central sink with required retention | Sink configuration in the log project |
| Data Access logging on for the services holding regulated data | Audit config per service |
| CMEK where the regime requires it | Resource configuration; remember it cannot be retrofitted |
| Security Command Center findings triaged | Findings list, filtered to active and high severity |
| Budget and anomaly alerts exist and route to a human | Budget configuration (`costs.md`) |
| Alerts exist for key creation, IAM change at org/folder, and firewall opened to the world | Log-based alert policies |

Write the sweep result into `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md`, any service account it turned up into `## Service Accounts`, and any host into the shared `~/Clawic/data/servers/servers.md`. Put the next quarterly sweep in `## Due`. The next session should start from the gaps, not from a fresh inventory (`memory-template.md`).
