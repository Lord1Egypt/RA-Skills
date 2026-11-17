# IAM — Identity, Roles, and Why the 403 Is Lying

GCP IAM is additive-by-inheritance with three separate systems layered on top: deny policies, org policies, and VPC Service Controls. Most "IAM bugs" are one of those three, or an API that was never enabled.

**Contents:** [Diagnose a 403 in This Order](#diagnose-a-403-in-this-order) · [The Hierarchy Is Additive Downward](#the-hierarchy-is-additive-downward) · [Deny Policies](#deny-policies) · [Service Accounts Are Both Identity and Resource](#service-accounts-are-both-identity-and-resource) · [actAs vs TokenCreator](#actas-vs-tokencreator) · [Keys: The Credential With No Expiry](#keys-the-credential-with-no-expiry) · [Workload Identity Federation](#workload-identity-federation) · [Roles: Primitive, Predefined, Custom](#roles-primitive-predefined-custom) · [IAM Conditions](#iam-conditions) · [Groups Over People](#groups-over-people) · [Access Review Checklist](#access-review-checklist)

**Before granting anything or debugging a denial**, read `## Service Accounts` in `~/Clawic/data/gcp/memory.md` — or `service-accounts.md` if `## Boxes` points there. Half of "we need a new service account" is an existing one nobody documented.

## Diagnose a 403 in This Order

Never widen a role first. The order below is cheapest-first and catches the common cases before the expensive ones.

1. **Is the API enabled in this project?** A 403 whose message says the API "has not been used in project N before or it is disabled" is not a permissions problem at all. This is the most common false IAM alarm in GCP, and it costs teams hours because the status code says 403. Enabling the API takes seconds and can itself need a moment to propagate.
2. **Is the principal what you think it is?** A local `gcloud` command runs as your user; the deployed service runs as its attached service account; a client library runs as whatever Application Default Credentials resolved to, which may be a third identity (`commands.md`). Print the active identity from the same context that is failing, not from your terminal.
3. **Is the binding on the right resource?** A role granted on the project does not apply to a resource in a different project, and a role granted on a bucket does not appear in the project's policy. Check the policy of the exact resource named in the error.
4. **Policy Troubleshooter.** Give it the principal, the full resource name, and the exact permission from the error message. It returns which binding grants or fails to grant it, including inherited ones. This ends most arguments.
5. **Is a deny policy blocking it?** Deny is evaluated before allow and no amount of granting overrides it.
6. **Is an org policy blocking the operation?** Org policies constrain what can be *created or configured*, and their errors often read like permission failures — `constraints/compute.vmExternalIpAccess` denies an external IP no matter who you are (`organization.md`).
7. **Is VPC Service Controls blocking it?** A 403 that mentions VPC Service Controls, or that is unhelpfully vague and carries a unique request id, is a perimeter. The audit log entry names the perimeter and the blocked service; the API response deliberately does not (`security.md`).
8. **Propagation.** Policy changes are usually visible in seconds but can take a couple of minutes. Retry once before theorizing — and never grant a second, broader role during that window, because it will still be there next year.

## The Hierarchy Is Additive Downward

Organization → Folder → Project → Resource. A principal's effective permissions are the **union** of every allow binding at every level above the resource.

- There is no "allow at the project that overrides a grant at the org". You cannot revoke inherited access with an allow policy — only a deny policy or removing the higher binding does that.
- This is the practical reason to grant low: a role granted at the org node is a role on every project that will ever exist, including the one a contractor creates next year.
- `roles/resourcemanager.projectIamAdmin` at any level is effectively administrative over everything below it, because the holder can grant themselves anything there. Treat "can edit IAM" as "has all permissions" when you reason about blast radius.
- The Shared VPC host project is a second inheritance path people forget: `roles/compute.networkUser` on the host project's subnets is what lets a service project attach anything to the network (`networking.md`).

## Deny Policies

The only way to carve a hole out of inherited access.

- Attached at organization, folder or project. Evaluated **before** allow policies; a matching deny wins regardless of any grant.
- Deny rules name principals, permissions, and optionally exception principals — the standard pattern is "deny this permission to everyone except this break-glass group".
- The canonical uses: deny `iam.serviceAccountKeys.create` everywhere, deny production data-access permissions to everyone outside the on-call group, deny billing changes outside a finance group.
- They are not a substitute for removing over-grants. A deny policy layered over `roles/editor` leaves the editor role there for the next person to reason about incorrectly.

## Service Accounts Are Both Identity and Resource

This dual nature is the source of most GCP IAM confusion, and of most GCP privilege escalation.

- As an **identity**, a service account holds roles on other resources — that is what the workload can do.
- As a **resource**, a service account has its own IAM policy naming who may *use* it. Anyone with sufficient access to the service account inherits everything the service account can do.
- Consequence: granting a developer the ability to deploy a Cloud Run service as `prod-admin@…` grants them `prod-admin@…`'s permissions, whatever they are, permanently, without their own bindings changing. Reviews that only look at what a person is granted directly will never see it.
- **The default Compute Engine service account** (`<project-number>-compute@developer.gserviceaccount.com`) is granted Editor on the project at creation unless the org policy that suppresses it is enforced. Any VM, any GKE node without Workload Identity, and any Cloud Run service without an explicit service account runs as it. One compromised container is then a project takeover.
- One service account per workload, named after the workload, with the smallest role set that makes it work. Record it and its purpose in `## Service Accounts`.

## actAs vs TokenCreator

Two permissions that look interchangeable and are not. Getting this wrong is either a broken deploy or a silent escalation.

| Permission / role | What it allows | When you need it |
|---|---|---|
| `iam.serviceAccounts.actAs` (`roles/iam.serviceAccountUser`) | Attach the service account to a resource at creation time — a VM, a Cloud Run service, a Cloud Function, a Dataflow job | Deploy pipelines. This is GCP's equivalent of AWS `iam:PassRole` |
| `iam.serviceAccounts.getAccessToken` (`roles/iam.serviceAccountTokenCreator`) | Mint a short-lived token *as* that service account, right now, from anywhere | Local development by impersonation, and cross-service delegation |
| `iam.serviceAccounts.signBlob` / `signJwt` | Sign as the service account without holding its key | Signed URLs and custom JWTs without a downloaded key |

Rules that follow:

- Grant either one **on the specific service account resource**, never at project level. `roles/iam.serviceAccountUser` on the project means "may deploy as any service account in this project", which includes the one with Editor.
- The deploy error `caller does not have permission … iam.serviceAccounts.actAs` is asking for the first row, not the second. Granting TokenCreator will not fix it, and grants more than was asked for.
- TokenCreator is the reason a low-privileged account can become a high-privileged one with no audit-visible role change on the caller. Review the *service account's* IAM policy, not just the caller's roles.

## Keys: The Credential With No Expiry

A downloaded service account JSON key never expires, is valid from anywhere on the internet, and is indistinguishable from the workload it impersonates.

- Enforce `constraints/iam.disableServiceAccountKeyCreation` at the org node, with a documented exception process rather than a permanent carve-out.
- Replacements, in preference order: **attached service accounts** for anything running on GCP (no credential exists at all), **Workload Identity Federation** for CI and other clouds, **impersonation** for local development, and a key only for a legacy system that supports nothing else.
- Where a key genuinely must exist: set an expiry with `constraints/iam.serviceAccountKeyExpiryHours`, store it in Secret Manager or the platform's own secret store, and record only its *pointer* in this skill's boxes — never the key material (`memory-template.md`).
- Detection: enable the key-usage insights and check for keys authenticating from unexpected locations. A leaked key's first observable act is usually a spend anomaly, which is why the budget alert doubles as a security alert (`costs.md`).
- Record key count and age per service account in `## Service Accounts`. A row reading `Keys: none` is the entire value of the table.

## Workload Identity Federation

Exchanges an external identity provider's token for a short-lived GCP token. No key, nothing to leak, nothing to rotate.

- Structure: a **workload identity pool** contains **providers** (OIDC or SAML). An attribute mapping turns claims from the external token into GCP attributes; an attribute condition restricts which external identities are accepted.
- **The attribute condition is the security control.** A GitHub Actions provider that maps the repository claim but does not *condition* on it will accept a token from any repository on GitHub, including one an attacker creates. Condition on the full repository path, and on the ref or environment when the workflow is privileged.
- Two binding styles: grant roles directly to the pool principal (`principalSet://…`), or let the external identity impersonate a service account. Direct bindings are simpler and remove the service account as an escalation target; impersonation is needed when a product only accepts a service account email.
- **Workload Identity Federation for GKE** is the same idea inside a cluster: a Kubernetes service account is bound to a GCP identity, and pods get credentials from the metadata server without the node's service account being involved. Enabling it is also what lets you strip the node service account back to logging and monitoring only (`gke.md`).

## Roles: Primitive, Predefined, Custom

- **Primitive** — `roles/owner`, `roles/editor`, `roles/viewer`. Editor spans thousands of permissions across every API, including creating service accounts and granting them roles. Reserve Owner for break-glass, never grant Editor to a workload, and treat Viewer as "can read every secret name, every dataset schema, and every log" — which is more than most people mean by "read-only".
- **Predefined** — per-service, maintained by Google, and the right default. They change as services add permissions, which is a feature: your grant keeps working after a service adds an API.
- **Custom** — for the cases where a predefined role is genuinely too wide. Costs to own: custom roles do **not** auto-update, so a new permission a service starts requiring will silently break the workload. Define them at the org or folder level so they can be reused, version them in IaC, and record why each permission is present in `~/Clawic/data/gcp/artifacts/role-<name>.md`, with its `## Boxes` line added in the same turn.
- Build custom roles from **observed** usage, not from reading documentation: IAM's role recommendations derive a tighter role from 90 days of actual permission use. That is the same data the IAM Recommender uses for over-grant findings.

## IAM Conditions

CEL expressions attached to a binding. The three that earn their complexity:

- **Time-bound access** — `request.time < timestamp("…")`. The only reliable way to grant temporary elevated access, because "we'll remove it Friday" never happens.
- **Resource-name prefix** — restrict a bucket-level or dataset-level grant to objects or tables matching a prefix, so one role covers a team's slice rather than the whole store.
- **Request attributes** — restrict by resource type, so `roles/compute.admin` conditioned to disks does not also grant instances.

Limits worth knowing before designing around them: conditions apply to a binding, not to a role; not every service enforces every attribute; and a conditional binding is invisible to anyone reading the role list without expanding it. That invisibility is why every conditional grant goes to `~/Clawic/data/gcp/artifacts/iam-conditions.md` — the binding, its CEL expression, its expiry and who asked for it — with its `## Boxes` line added in the same turn.

## Groups Over People

- Bind roles to Google Groups, never to individual users, past the first two people. Offboarding then becomes one group removal instead of a search across every project's policy.
- Enforce `constraints/iam.allowedPolicyMemberDomains` (domain-restricted sharing) at the org node. Without it, any principal with IAM-edit rights can grant a role to a personal Gmail address, and that grant is valid forever, survives the employee, and appears in no offboarding checklist. This is the highest-value single org policy in GCP.
- `allUsers` and `allAuthenticatedUsers` are the two principals that make a resource public. `allAuthenticatedUsers` means anyone with a Google account, anywhere — it is not "our users" (`storage.md`).

## Access Review Checklist

| Check | How |
|---|---|
| No `roles/owner` or `roles/editor` on humans outside break-glass | Read the org, folder and project policies; check inherited bindings, not just direct ones |
| No `roles/editor` on any service account | Same, filtered to `serviceAccount:` principals |
| Default compute service account has no bindings | Look it up by project number; also check whether the auto-grant org policy is enforced |
| No service account keys, or all keys inside their expiry policy | Key list per service account, with creation dates |
| No project-level `serviceAccountUser` or `serviceAccountTokenCreator` | Grep policies for those roles with a project-level resource |
| Domain-restricted sharing enforced; no external principals | Org policy state, plus a scan for principals outside the domain |
| No public IAM on buckets or datasets | `allUsers` / `allAuthenticatedUsers` anywhere (`storage.md`) |
| Over-granted roles | IAM Recommender findings, which derive from 90 days of real use |
| Federation providers have attribute conditions | Read each provider's condition, not just its mapping |
| Service accounts unused for 90+ days | Service account usage insights; each one is a credential with no owner |

After a least-privilege role or binding set finally works, save it to `~/Clawic/data/gcp/artifacts/role-<name>.md` — the permission list, why each permission is there, what broke without it, the date, and what over-grant it replaced — and add its `## Boxes` line to `memory.md`. Deriving one costs a full deploy cycle; nobody should pay it twice. Conditional and time-bound grants go to `artifacts/iam-conditions.md` the same way, and a time-bound grant also gets its expiry date in the `## Due` table. New or changed service accounts get their row in `## Service Accounts` in the same turn.
