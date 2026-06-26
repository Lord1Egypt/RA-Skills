# Billing and APIs

This file covers the practical realities that usually block new Google Cloud projects.

## Billing realities

Billing is not just an accounting detail. It determines whether many services are usable at all.

### Common failure mode
A user creates a project successfully, but service setup fails later because billing was never linked.

### Services that commonly require billing immediately
- Cloud Run
- Vertex AI
- BigQuery
- many managed networking and storage features
- most real deployments beyond free-tier experiments

### Questions to ask
- Does the user already know their billing account ID?
- Do they actually have permission to link projects to billing?
- Is this under a company org where billing is centrally controlled?

### Practical guidance
- If billing ownership is unclear, call that out early
- If the user is creating a proof-of-concept, still warn them that “project created” does not mean “services usable”
- If the workload is production-facing, treat billing linkage as part of the bootstrap, not an optional later step

## API enablement strategy

Enable only what the workload needs. Avoid cargo-cult enabling a huge list.

### Minimal platform baseline
Useful in many projects:
- `cloudresourcemanager.googleapis.com`
- `serviceusage.googleapis.com`
- `iam.googleapis.com`

### Cloud Run / container app baseline
- `run.googleapis.com`
- `artifactregistry.googleapis.com`
- `cloudbuild.googleapis.com`
- `logging.googleapis.com` (often useful operationally)
- `monitoring.googleapis.com` (often useful operationally)

### Vertex AI baseline
- `aiplatform.googleapis.com`
- `storage.googleapis.com`
- `iam.googleapis.com`

### BigQuery baseline
- `bigquery.googleapis.com`
- `storage.googleapis.com` when import/export is part of the flow
- `iam.googleapis.com`

### Firebase-oriented setup
Some Firebase setup is console-driven or product-specific. Do not overpromise a pure `gcloud` flow if the user expects a polished Firebase bootstrap.

## Region caveats

APIs being enabled is not enough. Region support still matters.

Examples:
- Vertex AI features differ by region
- Cloud Run is region-specific
- BigQuery dataset region decisions can constrain downstream design

## IAM guidance during bootstrap

### Good defaults
- Human admin access stays with humans
- Runtime gets its own service account
- CI/CD gets its own deployment identity when applicable

### Avoid by default
- Granting Owner to application service accounts
- Reusing one powerful service account for runtime and deployment
- Enabling a large set of APIs “just in case”

## What to report back to the user

When advising, summarize:
- which APIs are truly required
- whether billing is a blocker
- whether any step needs console access or elevated org permissions
- what identities should exist from day one
