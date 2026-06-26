# Project Creation Checklist

Use this checklist when planning or creating a new Google Cloud project.

## 1. Confirm purpose

Decide what the project is for before creating it.

Common categories:
- production application
- staging / testing
- personal experiment
- data / analytics
- AI / Vertex AI
- Firebase-backed app
- storage / file distribution

Questions to ask:
- What will run in this project?
- Is this temporary or long-lived?
- Is it isolated from existing environments on purpose?
- Does it need to meet naming, audit, or residency requirements?

## 2. Confirm naming

Capture both forms of identity:
- **Project display name**: human-friendly
- **Project ID**: immutable technical identifier used across CLI/API/infrastructure

Project ID guidance:
- keep it short and readable
- use environment suffixes where needed, for example `myapp-prod`, `myapp-staging`
- avoid random IDs unless this is disposable
- prefer a naming rule that scales across future projects

## 3. Confirm placement

If the user belongs to a Google Cloud organization, ask whether the project belongs under:
- a specific organization
- a folder
- a standalone personal account context

This affects:
- inherited IAM
- org policies
- billing permissions
- security constraints

## 4. Confirm billing

Billing is often the real blocker.

Check:
- whether a billing account already exists
- whether the user has permission to link projects to billing
- whether billing must be linked immediately for the intended services

Important:
- Cloud Run, Vertex AI, BigQuery, and many managed products require active billing
- some users can create projects but cannot link billing
- billing constraints may come from org policy or a central finance/admin owner

## 5. Confirm region and residency

Do not choose a region blindly.

Discuss:
- where users are located
- where data should live
- whether low latency matters
- whether the chosen Google service is supported in that region

Examples:
- Cloud Run should usually be near end users or dependent services
- BigQuery dataset region should be chosen carefully because cross-region assumptions get painful later
- Vertex AI availability varies by feature and region

## 6. Confirm required services on day one

List only what is actually needed.

Examples by workload:

### Cloud Run app
- Cloud Run Admin API
- Artifact Registry API
- Cloud Build API
- IAM API
- Service Usage API

### Vertex AI workload
- Vertex AI API
- Cloud Storage API
- IAM API
- Service Usage API

### BigQuery workload
- BigQuery API
- Cloud Storage API if loading/exporting data
- IAM API

### Firebase app
- Firebase-related console setup
- likely Firestore / Hosting / Auth downstream choices

## 7. Confirm identity model

Ask whether the project needs dedicated identities for:
- runtime execution
- CI/CD deployment
- local developer access
- automation scripts

Prefer separate service accounts when:
- production deployment is involved
- CI/CD should be auditable
- app runtime should not inherit broad deploy rights

## 8. Confirm security expectations

For anything beyond a toy project, note:
- least privilege is preferred
- avoid `roles/owner` for workloads
- separate human admin access from machine execution access
- think early about secrets, artifact storage, and auditability

## 9. Final pre-create review

Before running commands, confirm:
- display name
- project ID
- billing account state
- org/folder target
- region assumptions
- API list
- service account plan

If any of these are fuzzy, stop and clarify instead of improvising.
