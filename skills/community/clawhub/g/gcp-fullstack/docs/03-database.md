> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Service Selection: Database Decision Tree

| Condition | Recommended Service | Why |
|---|---|---|
| Document-oriented data, real-time listeners, mobile-first | **Firestore (Native mode)** | Real-time sync, offline support, Firebase SDK integration |
| Relational data, complex queries, joins, transactions | **Cloud SQL (PostgreSQL)** | Full SQL, strong consistency, mature ecosystem |
| Key-value lookups, session storage, caching | **Memorystore (Redis)** | Sub-millisecond latency, managed Redis |
| Global scale, financial-grade consistency | **Spanner** | Globally distributed SQL, 99.999% SLA (expensive) |
| Analytics, data warehouse | **BigQuery** | Serverless analytics, petabyte scale |

For most web apps, **Firestore** or **Cloud SQL (PostgreSQL)** covers 90% of use cases.

---

## Part 6: Database — Firestore

### Initialize Firestore

```bash
# Create Firestore database (Native mode)
gcloud firestore databases create --location=$GCP_REGION --type=firestore-native
```

### Firestore Client Helper

```typescript
// src/lib/db/firestore.ts
import { initializeApp, getApps, cert } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";

if (getApps().length === 0) {
  initializeApp({
    credential: cert({
      projectId: process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, "\n"),
    }),
  });
}

export const db = getFirestore();
```

### Firestore Security Rules

Create `firestore.rules`:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Users can only access their own profile
    match /users/{userId} {
      allow read, update, delete: if request.auth != null && request.auth.uid == userId;
      allow create: if request.auth != null;
    }

    // Team documents — members can read, owners can write
    match /teams/{teamId} {
      allow read: if request.auth != null &&
        request.auth.uid in resource.data.members;
      allow write: if request.auth != null &&
        request.auth.uid == resource.data.ownerId;
    }

    // Default deny
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

```bash
# Deploy rules
gcloud firestore deploy --rules=firestore.rules
# or via Firebase CLI
npx firebase deploy --only firestore:rules
```

### Firestore Indexes

Create `firestore.indexes.json`:

```json
{
  "indexes": [
    {
      "collectionGroup": "users",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "email", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

```bash
npx firebase deploy --only firestore:indexes
```

---

## Part 7: Database — Cloud SQL (PostgreSQL)

### Create Instance

```bash
# Create Cloud SQL instance
gcloud sql instances create <instance-name> \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$GCP_REGION \
  --storage-size=10GB \
  --storage-auto-increase

# Create database
gcloud sql databases create <db-name> --instance=<instance-name>

# Create user
gcloud sql users create <username> \
  --instance=<instance-name> \
  --password=<password>
```

### Connect from Cloud Run

Cloud Run connects to Cloud SQL via Unix socket (Cloud SQL Proxy is built in):

```bash
# Add Cloud SQL connection to Cloud Run service
gcloud run services update <service-name> \
  --region $GCP_REGION \
  --add-cloudsql-instances $GCP_PROJECT_ID:$GCP_REGION:<instance-name>
```

Connection string format for Cloud Run:

```
DATABASE_URL=postgresql://<user>:<password>@/<db-name>?host=/cloudsql/<project>:<region>:<instance>
```

### Prisma Setup (if using Prisma)

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  avatarUrl String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

```bash
# Generate client
npx prisma generate

# Push schema to database
npx prisma db push

# Create migration
npx prisma migrate dev --name init
```

### Cloud SQL Helper

```typescript
// src/lib/db/sql.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```
