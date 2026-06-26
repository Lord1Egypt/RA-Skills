---
name: gcp-project-bootstrap
description: Create and bootstrap Google Cloud projects for new workloads. Use when the user wants to create a new Google Cloud project, choose a project ID and naming convention, decide billing and region setup, enable required Google APIs, prepare service accounts, or initialize a project for Cloud Run, Vertex AI, BigQuery, Cloud Storage, or Firebase. Also use when auditing whether a planned GCP project setup is complete before deployment.
---

# GCP Project Bootstrap

Create new Google Cloud projects in a deliberate, least-privilege way.

## Workflow

1. Clarify the workload first.
   - Cloud Run app
   - Vertex AI / Gemini / ML workload
   - BigQuery / analytics
   - Cloud Storage / file hosting
   - Firebase app
   - sandbox / experiment / tutorial

2. Collect required inputs before proposing commands.
   - project display name
   - desired `project_id`
   - org/folder placement if applicable
   - billing account availability
   - primary region or residency requirement
   - services that must work on day one
   - whether CI/CD or runtime service accounts are needed

3. Read `references/project-creation-checklist.md` and follow it as the default sequence.

4. If billing, API enablement, or service selection is part of the task, read `references/billing-and-apis.md`.

5. If command examples are needed, read `references/common-gcloud-commands.md`.

## Operating rules

- Do not assume billing is already linked.
- Do not recommend broad roles like `roles/owner` unless the user explicitly asks and understands the risk.
- Prefer least privilege and workload-specific service accounts.
- Call out when a step requires console-only actions, elevated org permissions, or a human with billing admin access.
- If the user has not chosen a region, explain the tradeoff briefly instead of picking randomly.
- If the project is for production, recommend enabling audit-friendly naming and separating runtime/service identities early.

## Output expectations

When helping the user, produce:
- a short summary of the intended project purpose
- the exact inputs still missing
- a safe creation sequence
- API list grouped by workload
- IAM/service-account recommendations only if relevant

## Common workload branches

### Cloud Run
Focus on:
- Artifact Registry
- Cloud Build
- Cloud Run Admin API
- runtime service account
- region choice close to users/data

### Vertex AI
Focus on:
- billing must be active
- Vertex AI API
- region support for the intended model/service
- storage buckets for datasets/artifacts if needed
- service account separation for notebooks/jobs/apps

### BigQuery
Focus on:
- dataset region planning
- billing confirmation
- BigQuery API
- least-privilege access for analysts vs pipelines

### Firebase
Focus on:
- whether this is primarily a Firebase project with GCP underneath
- required console setup beyond raw `gcloud`
- auth/hosting/firestore specific downstream decisions
