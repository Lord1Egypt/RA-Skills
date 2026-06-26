> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Service Selection: Compute Decision Tree

| Condition | Recommended Service | Why |
|---|---|---|
| SSR framework (Next.js, Nuxt, SvelteKit, Remix) | **Cloud Run** | Container-based, supports long-running requests, auto-scaling to zero, custom Dockerfile |
| Static site / Jamstack (Astro static, plain HTML) | **Cloud Storage + Cloud CDN** | Cheapest option, global CDN, no server needed |
| Lightweight API or webhooks (no frontend) | **Cloud Functions (2nd gen)** | Per-invocation billing, event-driven, minimal config |
| Legacy or monolith app needing managed runtime | **App Engine (Flexible)** | Managed VMs, supports custom runtimes, built-in versioning |
| Microservices with high concurrency | **Cloud Run** | Multi-container, gRPC support, concurrency control |

When in doubt, default to **Cloud Run** — it is the most versatile.

---

## Part 3: Compute — Cloud Run

Cloud Run is the default compute platform for SSR frameworks.

### Dockerfile (Next.js example — adapt per framework)

```dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 appuser

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

USER appuser
EXPOSE 8080
ENV PORT=8080
CMD ["node", "server.js"]
```

For Next.js, enable standalone output in `next.config.ts`:

```typescript
const nextConfig = {
  output: "standalone",
};
export default nextConfig;
```

### Build and Deploy to Cloud Run

```bash
# Build container image using Cloud Build
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/<service-name>

# Deploy to Cloud Run
gcloud run deploy <service-name> \
  --image gcr.io/$GCP_PROJECT_ID/<service-name> \
  --platform managed \
  --region $GCP_REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars "NODE_ENV=production"
```

### Setting Environment Variables on Cloud Run

```bash
# Set env vars (repeat for each var)
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --set-env-vars "KEY1=value1,KEY2=value2"

# For secrets, use Secret Manager
gcloud secrets create <secret-name> --data-file=- <<< "secret-value"
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --set-secrets "ENV_VAR=<secret-name>:latest"
```

### Revision Management and Rollback

```bash
# List revisions
gcloud run revisions list --service <service-name> --region $GCP_REGION

# Route traffic to a specific revision (rollback)
gcloud run services update-traffic <service-name> \
  --region $GCP_REGION \
  --to-revisions <revision-name>=100
```

### Health Check

Cloud Run uses the container's HTTP health endpoint. Create a `/api/health` or `/health` route:

```typescript
// Example for Next.js: src/app/api/health/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ status: "ok", timestamp: new Date().toISOString() });
}
```

---

## Part 4: Compute — Cloud Functions (2nd gen)

Use for lightweight APIs, webhooks, or event-driven workloads.

```bash
# Deploy an HTTP function
gcloud functions deploy <function-name> \
  --gen2 \
  --runtime nodejs20 \
  --region $GCP_REGION \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point handler \
  --source .

# Deploy an event-triggered function (e.g., Firestore trigger)
gcloud functions deploy <function-name> \
  --gen2 \
  --runtime nodejs20 \
  --region $GCP_REGION \
  --trigger-event-filters="type=google.cloud.firestore.document.v1.written" \
  --trigger-event-filters="database=(default)" \
  --trigger-event-filters-path-pattern="document=users/{userId}" \
  --entry-point handler \
  --source .
```

---

## Part 5: Compute — App Engine

Use for legacy or monolith apps needing a fully managed runtime.

### `app.yaml`

```yaml
runtime: nodejs20
env: standard

instance_class: F2

automatic_scaling:
  min_instances: 0
  max_instances: 5
  target_cpu_utilization: 0.65

env_variables:
  NODE_ENV: "production"
```

```bash
# Deploy
gcloud app deploy --quiet

# View logs
gcloud app logs tail -s default

# Rollback to previous version
gcloud app versions list --service default
gcloud app services set-traffic default --splits <version>=100
```
