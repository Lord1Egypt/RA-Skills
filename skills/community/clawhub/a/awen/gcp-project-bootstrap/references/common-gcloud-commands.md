# Common gcloud Commands

These are practical examples for project bootstrap tasks. Replace placeholders before use.

## Variables to collect first
- `PROJECT_NAME`
- `PROJECT_ID`
- `BILLING_ACCOUNT_ID`
- `REGION`

## Create a project

```bash
gcloud projects create PROJECT_ID --name="PROJECT_NAME"
```

## Set default project locally

```bash
gcloud config set project PROJECT_ID
```

## Link billing to the project

```bash
gcloud beta billing projects link PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

## Check whether billing is linked

```bash
gcloud beta billing projects describe PROJECT_ID
```

## Enable baseline APIs

```bash
gcloud services enable \
  cloudresourcemanager.googleapis.com \
  serviceusage.googleapis.com \
  iam.googleapis.com \
  --project=PROJECT_ID
```

## Enable Cloud Run app APIs

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  --project=PROJECT_ID
```

## Enable Vertex AI APIs

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  --project=PROJECT_ID
```

## Enable BigQuery APIs

```bash
gcloud services enable \
  bigquery.googleapis.com \
  storage.googleapis.com \
  --project=PROJECT_ID
```

## Create a service account

```bash
gcloud iam service-accounts create deploy-bot \
  --display-name="Deploy Bot" \
  --project=PROJECT_ID
```

## List service accounts

```bash
gcloud iam service-accounts list --project=PROJECT_ID
```

## Example: grant a narrower role to a service account

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:deploy-bot@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```

## Example: allow the runtime service account to pull from Artifact Registry

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:RUNTIME_SA@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

## Check enabled APIs

```bash
gcloud services list --enabled --project=PROJECT_ID
```

## Notes
- Some steps require permissions the current user may not have.
- Billing linkage often fails because of account permissions, not command syntax.
- Prefer workload-specific roles over broad project-wide admin roles.
