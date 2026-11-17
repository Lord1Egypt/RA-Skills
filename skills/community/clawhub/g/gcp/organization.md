# Organization — Projects, Folders, Billing, Org Policies, Quotas

Applies when `org_model` is `organization`, and describes what a single-project setup is choosing not to have. The decision matters early: **a project ID is permanent, quotas are per project, and reorganizing a live hierarchy means re-granting every binding.**

**Contents:** [The Project Is the Real Boundary](#the-project-is-the-real-boundary) · [When One Project Stops Being Enough](#when-one-project-stops-being-enough) · [The Hierarchy](#the-hierarchy) · [Org Policies Worth Setting on Day One](#org-policies-worth-setting-on-day-one) · [Billing Accounts](#billing-accounts) · [Quotas Are Per Project](#quotas-are-per-project) · [Project Lifecycle](#project-lifecycle) · [Landing Zone](#landing-zone) · [Client and Multi-Tenant Work](#client-and-multi-tenant-work)

**Before any billing, quota or cross-project question**, read `## Org Context` in `~/Clawic/data/gcp/memory.md` — or `projects.md` if `## Boxes` points there. Which project owns the network, which owns billing, and which client owns which project are all recorded there.

## The Project Is the Real Boundary

Four separate things are scoped to the project, which is why "just put it in the same project" compounds:

1. **Quota** — CPUs, IPs, accelerators, API rate limits. A runaway dev workload can exhaust production's quota when they share a project.
2. **IAM blast radius** — a project-level role applies to everything in it. Separation by label and good intentions is not separation.
3. **Cost attribution** — labels can be forgotten; nobody forgets which project they deployed to. Per-project cost is the only attribution that is correct by construction.
4. **Deletion and lifecycle** — a project can be deleted as a unit, which is what makes environments disposable.

The corollary: a single project holding prod, dev and a client's work is four problems in one, and none of them is visible until it is expensive.

## When One Project Stops Being Enough

Any one of these is sufficient reason to move to an organization with folders:

- More than one person can touch production, and prod and dev should be separated by a boundary rather than by naming discipline.
- A compliance regime (`compliance_regime` other than `none`) requiring demonstrable isolation of scope.
- Client work: each client's resources, costs and access must be separable, and one client must never be able to see another's existence.
- Quota contention between environments, or a need for different quota ceilings per environment.
- A need for org policies at all — folders and the organization node are the only places they can be inherited from.

An **organization node requires a verified domain** through Cloud Identity or Workspace. Projects created by an individual account have no organization, and moving them into one later is possible but is a migration with IAM consequences — which is the reason to set up the organization before the second project, not after the tenth.

## The Hierarchy

Organization → Folders → Projects → Resources. Three layouts, in increasing order of size:

| Layout | Shape | Right when |
|---|---|---|
| Environment folders | `prod`, `staging`, `dev`, each holding projects | One product, one team. The common correct answer |
| Team folders with environment subfolders | `team-a/prod`, `team-a/dev` | Several teams that own their own stacks |
| Client folders | `clients/acme`, `clients/beta` | Agency or multi-tenant delivery work |

Rules that hold across all three:

- **Grant roles at the folder, to groups.** Folder-level grants inherit to every project inside, including ones created next year, which is the point (`iam.md`).
- **Org policies inherit downward** and can be tightened, and in specific cases relaxed, at a lower node. Set the strict posture at the organization and grant narrow exceptions per folder or project, never the reverse.
- **A platform folder** holds the shared things: the Shared VPC host project, the logging sink destination, the artifact registry, the Terraform state bucket. These outlive every product project.
- Depth costs comprehensibility. Three levels of folders is almost always someone modeling the org chart rather than the blast radius.

## Org Policies Worth Setting on Day One

Free, inherited, and each one prevents a class of incident. This is the highest-value hour in a new organization.

| Constraint | Prevents |
|---|---|
| `iam.allowedPolicyMemberDomains` | A role granted to a personal account outside the domain — permanent, invisible in offboarding, and the highest-value single policy in GCP |
| `iam.disableServiceAccountKeyCreation` | Downloadable credentials with no expiry, which is how keys end up in repositories |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | The default Compute Engine service account receiving Editor at project creation |
| `storage.publicAccessPrevention` | A public bucket, in any project, ever |
| `sql.restrictPublicIp` | A database instance with a public address |
| `compute.vmExternalIpAccess` | VMs with public IPs outside an explicit allowlist |
| `compute.requireOsLogin` | SSH keys in instance metadata instead of IAM-controlled access |
| `compute.skipDefaultNetworkCreation` | The default VPC with its permissive firewall rules appearing in every new project |
| `gcp.resourceLocations` | Resources created outside the regions a regime or contract allows |
| `compute.disableSerialPortAccess` | An out-of-band console path that bypasses OS-level controls |

Two operational notes: set them in **dry-run mode** first on an existing estate to see what would break, because several of these will flag something already deployed. And record the enforced set, plus every exception granted and why, in `~/Clawic/data/gcp/artifacts/org-policies.md` with its `## Boxes` line — an exception with no recorded reason becomes permanent by default (`memory-template.md`).

## Billing Accounts

- A billing account is separate from the organization and can pay for projects across it. `roles/billing.admin` is the role that can attach and detach — treat it as production-critical, because detaching a billing account stops every resource in the project.
- **Detaching billing is destructive, not a pause.** VMs stop, and some resources are deleted rather than suspended. This is also why the "hard budget cap" pattern is a circuit breaker for sandboxes only (`costs.md`).
- One billing account per organization is the norm; separate accounts are for genuinely separate legal entities or for client work that must be invoiced separately.
- **Billing export to BigQuery is configured per billing account** and reports forward only. Enable it before the first project has anything in it (SKILL.md Rule 2).
- Cost attribution below the project level needs labels; above it, the folder hierarchy in the export is what gives per-team and per-environment reporting without any label discipline at all.
- Record the billing account and its scope in `## Org Context`, or in the `Billing account` column of `projects.md` once there is more than one project.

## Quotas Are Per Project

- Quota is granted per project, per region, and per quota type. Nothing is shared between projects, and an increase in one does not help another.
- **Several defaults are zero**, notably accelerators. Discover that during design, not during a launch (`vertex.md`).
- API **rate** quotas are separate from resource **allocation** quotas, and a busy service can exhaust a rate quota that a human clicking in the console never notices (`debug.md`).
- Increase requests carry a human review and take days. Anything with a launch date needs its quota request weeks before, with the observed peak attached.
- The per-project scope is a design tool: giving a noisy batch workload its own project is often the cheapest way to protect production's quota, and it costs nothing.
- Record every quota checked, requested and granted in `## Quotas` in `memory.md`, per project and region, with the observed peak (`memory-template.md`).

## Project Lifecycle

- **The ID is permanent and globally unique.** It cannot be renamed, and after deletion it can never be reused — by you or anyone else. Choose a scheme (`<org>-<product>-<env>`) and record it under `conventions.project_ids` in `config.yaml` once the user states one.
- The **project number** is the other identifier, and several systems use it rather than the ID: some IAM principals, Workload Identity Federation subjects, default service account names, and log filters. Record both in `projects.md` — looking the number up costs an API call the next session should not have to make.
- **Deletion has a recovery window** of about 30 days during which the project is suspended and restorable. Everything in it stops immediately.
- **Liens** prevent deletion outright. Put one on production and on the Shared VPC host project; the deletion of a host project takes every service project's networking with it.
- Deleting a project to clean up is usually the wrong move: the ID is burned forever and live dependencies stay hidden until they break. Delete the resources, keep the project — or, if the project must go, check what references it first (Shared VPC attachments, IAM bindings elsewhere, log sinks, billing export).
- Every project added, and its owner and billing account, goes in `## Org Context` in `~/Clawic/data/gcp/memory.md` while there is one, and in `~/Clawic/data/gcp/projects.md` from the second — recorded in the same turn, with the projects box getting its `## Boxes` line the moment it is created (`memory-template.md`).

## Landing Zone

What every new project should get automatically, whether by a factory or a checklist:

- Attached to the right folder and billing account, with the default VPC absent
- Inherited org policies verified as applying (dry-run findings resolved, not ignored)
- Logging sink to the central log destination, with the retention the regime requires
- The standard groups granted their roles at the folder, not at the project
- A budget with alerts routed somewhere a human reads
- Labels applied at creation: `env`, `team`, `service`
- Terraform state in the platform folder's bucket, never in the project it manages

**Terraform-based factories** are correct where IaC discipline exists and account creation should sit in the same review flow as everything else. Whatever creates projects must also apply the baseline — a project created without it is the one that appears in the next audit.

## Client and Multi-Tenant Work

- **One project per client, in a client folder.** It gives clean cost separation, clean access separation, and a clean handover: a project can be transferred to the client's organization, which a shared project cannot.
- Grant the client's people access at their folder, never at yours. Domain-restricted sharing may need a per-folder exception to allow their domain — grant it narrowly, and record the exception, its folder and its expiry alongside the rest in `~/Clawic/data/gcp/artifacts/org-policies.md`.
- Separate billing accounts when the client is invoiced directly, one billing account with per-project attribution when you invoice them.
- **The client is a contact, not a GCP object.** Write the named human to the shared `~/Clawic/data/contacts/contacts.md` (`Name | Role | Preferred channel | Context`), keyed by their **email, lowercased** — or their handle when there is no email. Read the file first: if the key is already there, update that row in place and extend `Context` instead of replacing it, because another skill wrote it; only its absence justifies a new row. Table until 15 people, then one file per person at `~/Clawic/data/contacts/<name-kebab>.md` with `contacts.md` left as the index. If the file already exists with other columns, match them and add anything missing as a trailing note — never rewrite its header. Reference them from `projects.md` by name only; duplicating a client record in two boxes is how two skills end up disagreeing about who the contact is (`memory-template.md`).
- Handover checklist: transfer or recreate the project under their organization, remove your groups' bindings, hand over the Terraform state and the artifacts folder, and delete the client's row from your inventory boxes with the date noted in `memory.md`. An inventory that only grows stops being an inventory.

Every project, folder decision, billing account, org-policy exception and quota grant produced here is written before the session ends: projects and their owners to `## Org Context` or `~/Clawic/data/gcp/projects.md`, quotas to `## Quotas`, clients to the shared `~/Clawic/data/contacts/contacts.md` as a pointer, the enforced org policies and every exception with its reason to `~/Clawic/data/gcp/artifacts/org-policies.md`, and the hierarchy design with its rejected alternative to `~/Clawic/data/gcp/artifacts/decision-hierarchy.md` — each artifact getting its `## Boxes` line in the same turn (`memory-template.md`).
