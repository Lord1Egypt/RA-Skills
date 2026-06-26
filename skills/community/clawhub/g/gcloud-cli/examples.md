# Google Cloud CLI Examples

All examples below follow this policy: show the full command and wait for explicit user approval before execution, including read-only operations.

## Example 1: Creating a Cloud Storage Bucket

**User prompt:** "Create a new storage bucket called my-app-data in us-central1"

**Expected agent behavior:**
1. Run `gcloud config list --format='text(core.account,core.project)'` and show the active context.
2. Identify the relevant group: `storage`.
3. Run `gcloud storage --help`, then `gcloud storage buckets --help`, then `gcloud storage buckets create --help`.
4. Present command:
   ```bash
   gcloud storage buckets create gs://my-app-data --location=us-central1
   ```
5. Wait for explicit user approval before executing.

## Example 2: Deploying a Cloud Run Service

**User prompt:** "Deploy my Docker image gcr.io/my-project/api:latest to Cloud Run in us-east1"

**Expected agent behavior:**
1. Show active context with `gcloud config list --format='text(core.account,core.project)'`.
2. Identify group: `run`.
3. Run `gcloud run --help` and `gcloud run deploy --help`.
4. Present command:
   ```bash
   gcloud run deploy api --image=gcr.io/my-project/api:latest --region=us-east1
   ```
5. Wait for explicit user approval before executing.

## Example 3: Listing Kubernetes Clusters

**User prompt:** "Show me all GKE clusters in my project"

**Expected agent behavior:**
1. Show active context with `gcloud config list --format='text(core.account,core.project)'`.
2. Identify group: `container`.
3. Run `gcloud container --help`, `gcloud container clusters --help`, and `gcloud container clusters list --help`.
4. Present command:
   ```bash
   gcloud container clusters list --format=json
   ```
5. Wait for explicit user approval before executing (read operation).

## Example 4: Managing IAM Permissions

**User prompt:** "Grant the Storage Admin role to user alice@example.com on project my-project"

**Expected agent behavior:**
1. Show active context with `gcloud config list --format='text(core.account,core.project)'`.
2. Identify group: `projects`.
3. Run `gcloud projects --help` and `gcloud projects add-iam-policy-binding --help`.
4. Present command:
   ```bash
   gcloud projects add-iam-policy-binding my-project --member=user:alice@example.com --role=roles/storage.admin
   ```
5. Wait for explicit user approval before executing.

## Example 5: Creating a Cloud SQL Instance

**User prompt:** "Create a PostgreSQL 15 instance named prod-db with 4 vCPUs and 16GB RAM"

**Expected agent behavior:**
1. Show active context with `gcloud config list --format='text(core.account,core.project)'`.
2. Identify group: `sql`.
3. Run `gcloud sql --help`, `gcloud sql instances --help`, and `gcloud sql instances create --help`.
4. Present full command with discovered flags.
5. Wait for explicit user approval before executing.
