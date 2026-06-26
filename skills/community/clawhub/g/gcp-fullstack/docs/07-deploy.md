> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Part 9: Deployment Pipeline

### Pre-Deploy Checklist

Run these before every deployment. Adapt commands per framework:

```bash
# 1. Type checking
npx tsc --noEmit

# 2. Linting
npx eslint . --ext .ts,.tsx

# 3. Tests
npx vitest run

# 4. Build
npm run build
```

### Cloud Run Deploy (production flow)

```bash
# 1. Ensure on main branch and up to date
git checkout main && git pull origin main

# 2. Merge feature branch
git merge --squash <branch-name>
git commit -m "feat: <summary>"

# 3. Build and push container
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/<service-name>

# 4. Deploy new revision
gcloud run deploy <service-name> \
  --image gcr.io/$GCP_PROJECT_ID/<service-name> \
  --platform managed \
  --region $GCP_REGION

# 5. Health check
SERVICE_URL=$(gcloud run services describe <service-name> --region $GCP_REGION --format 'value(status.url)')
curl -sf "$SERVICE_URL/api/health" | jq .

# 6. If health check fails, rollback
gcloud run services update-traffic <service-name> \
  --region $GCP_REGION \
  --to-revisions <previous-revision>=100
```

### GitHub Integration

```bash
# Create PR
gh pr create --title "feat: <title>" --body "<description>" --base main

# Check CI status
gh pr checks <pr-number>

# Merge (squash)
gh pr merge <pr-number> --squash --delete-branch
```

### CI/CD with Cloud Build (optional)

Create `cloudbuild.yaml` in the project root:

```yaml
steps:
  # Install dependencies
  - name: 'node:20'
    entrypoint: npm
    args: ['ci']

  # Run tests
  - name: 'node:20'
    entrypoint: npm
    args: ['test']

  # Build container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}', '.']

  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}']

  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE_NAME}'
      - '--image=gcr.io/$PROJECT_ID/${_SERVICE_NAME}'
      - '--region=${_REGION}'
      - '--platform=managed'

substitutions:
  _SERVICE_NAME: my-app
  _REGION: us-central1

images:
  - 'gcr.io/$PROJECT_ID/${_SERVICE_NAME}'
```

```bash
# Set up Cloud Build trigger from GitHub
gcloud builds triggers create github \
  --repo-name=<repo> \
  --repo-owner=<owner> \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

---

## Part 11: Cloud Storage (Static Assets and Uploads)

### Create Bucket

```bash
gcloud storage buckets create gs://$GCP_PROJECT_ID-assets \
  --location=$GCP_REGION \
  --uniform-bucket-level-access

# Make public (for static assets served via CDN)
gcloud storage buckets add-iam-policy-binding gs://$GCP_PROJECT_ID-assets \
  --member=allUsers \
  --role=roles/storage.objectViewer
```

### Upload Helper (server-side)

```typescript
// src/lib/storage.ts
import { Storage } from "@google-cloud/storage";

const storage = new Storage({ projectId: process.env.GCP_PROJECT_ID });
const bucket = storage.bucket(`${process.env.GCP_PROJECT_ID}-assets`);

export async function uploadFile(file: Buffer, filename: string, contentType: string) {
  const blob = bucket.file(filename);
  const stream = blob.createWriteStream({
    metadata: { contentType },
    resumable: false,
  });

  return new Promise<string>((resolve, reject) => {
    stream.on("error", reject);
    stream.on("finish", () => {
      resolve(`https://storage.googleapis.com/${bucket.name}/${filename}`);
    });
    stream.end(file);
  });
}
```

---

## Part 12: Secret Manager

Never hardcode secrets. Use Secret Manager for all sensitive values.

```bash
# Create a secret
echo -n "my-secret-value" | gcloud secrets create <secret-name> --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding <secret-name> \
  --member="serviceAccount:<service-account>@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Mount in Cloud Run
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --set-secrets "ENV_VAR=<secret-name>:latest"
```

---

## Part 13: Monitoring and Logging

### View Logs

```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=<service-name>" \
  --limit 50 --format json | jq '.[].textPayload'

# Cloud Functions logs
gcloud functions logs read <function-name> --gen2 --region $GCP_REGION --limit 50
```

### Error Reporting

```bash
# Enable Error Reporting
gcloud services enable clouderrorreporting.googleapis.com
```

---

## Commit Message Convention

All commits must follow Conventional Commits:

- `feat:` — new feature
- `fix:` — bug fix
- `refactor:` — code change that neither fixes a bug nor adds a feature
- `test:` — adding or fixing tests
- `chore:` — tooling, config, deps
- `docs:` — documentation only
- `db:` — database migrations or schema changes
- `infra:` — infrastructure changes (Cloud Run config, Cloudflare rules, IAM)

## Branch Strategy

- `main` = production. Every push triggers production deployment.
- Feature branches (`feat/`, `fix/`, `refactor/`) = preview/staging deploys.
- Never force-push to `main`.

## Safety Rules

- NEVER deploy to production without running the pre-deploy checklist.
- NEVER store credentials in code or commit `.env` files.
- NEVER delete Cloud SQL instances or Firestore databases without explicit user confirmation.
- NEVER modify IAM roles without user approval.
- ALWAYS verify `.gitignore` includes credential files before the first commit.
- For destructive operations (DROP TABLE, delete Cloud Run service, purge Firestore collection), require a dry-run first and show the user what will be affected.
