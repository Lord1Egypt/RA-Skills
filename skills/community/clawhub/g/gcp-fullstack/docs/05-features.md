> This is a sub-module of the `gcp-fullstack` skill. See the main [SKILL.md](../SKILL.md) for the Planning Protocol and overview.

## Part 14: Feature Generation

When the user describes a feature, implement the complete vertical slice autonomously. This replaces the need for a separate feature-forge skill.

### Feature Workflow

1. **Analyze** — Parse the description to identify: UI components needed, data model changes (Firestore collections or Cloud SQL tables), API endpoints, auth requirements.
2. **Schema first** — Create or update the data model. For Firestore: define the collection structure, security rules, indexes. For Cloud SQL: create a Prisma migration.
3. **Data access layer** — Create typed helpers in `src/lib/db/` that abstract Firestore or Prisma queries.
4. **API routes** — Create API routes or Server Actions (framework-dependent). Always validate input with Zod. Always check auth.
5. **UI components** — Build the UI using the project's component library (shadcn/ui, custom, etc.). Include loading states, error states, empty states.
6. **Toast notifications** — Add success/error toasts for every user action (create, update, delete). Use the project's toast library (sonner, react-hot-toast, shadcn toast).
7. **Tests** — Write at least: one unit test for the data access function, one integration test for the API route, one E2E test for the critical user flow.
8. **Verify** — Run `npx tsc --noEmit`, linter, and tests. Fix any issues before committing.

### Component Patterns (adapt per framework)

#### Server Action Pattern (Next.js App Router)

```typescript
// src/app/actions/entities.ts
"use server";

import { revalidatePath } from "next/cache";
import { z } from "zod";
import { db } from "@/lib/db/firestore"; // or prisma
import { getAuthUser } from "@/lib/firebase/admin";

const CreateEntitySchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().max(2000).optional(),
});

export async function createEntity(formData: FormData) {
  const user = await getAuthUser();
  if (!user) throw new Error("Unauthorized");

  const parsed = CreateEntitySchema.safeParse({
    name: formData.get("name"),
    description: formData.get("description"),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  // Firestore example
  const ref = await db.collection("entities").add({
    ...parsed.data,
    userId: user.uid,
    createdAt: new Date().toISOString(),
  });

  revalidatePath("/entities");
  return { data: { id: ref.id } };
}
```

#### Form Component with Toast

```tsx
// src/components/entity-form.tsx
"use client";

import { useTransition } from "react";
import { toast } from "sonner"; // or your toast lib
import { createEntity } from "@/app/actions/entities";

export function EntityForm() {
  const [isPending, startTransition] = useTransition();

  async function handleSubmit(formData: FormData) {
    startTransition(async () => {
      const result = await createEntity(formData);
      if (result?.error) {
        toast.error("Failed to create entity");
        return;
      }
      toast.success("Entity created successfully");
    });
  }

  return (
    <form action={handleSubmit}>
      <input name="name" placeholder="Name" required disabled={isPending} />
      <textarea name="description" placeholder="Description" disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create"}
      </button>
    </form>
  );
}
```

#### Page with Loading/Error/Empty States

```tsx
// src/app/entities/page.tsx
import { Suspense } from "react";

function EntitiesLoading() {
  return <div className="animate-pulse">Loading entities...</div>;
}

async function EntitiesList() {
  const entities = await getEntities(); // your data fetch

  if (entities.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-12">
        <p>No entities yet.</p>
        <a href="/entities/new">Create your first entity</a>
      </div>
    );
  }

  return (
    <ul>
      {entities.map((e) => (
        <li key={e.id}>{e.name}</li>
      ))}
    </ul>
  );
}

export default function EntitiesPage() {
  return (
    <Suspense fallback={<EntitiesLoading />}>
      <EntitiesList />
    </Suspense>
  );
}
```

### Checklist After Feature Generation

- [ ] Data model created (Firestore collection or Prisma migration)
- [ ] Security rules or RLS updated
- [ ] API route or Server Action with Zod validation
- [ ] Auth check on every write operation
- [ ] UI with loading, error, and empty states
- [ ] Toast notifications for success and failure
- [ ] At least one test per layer (unit, integration, E2E)
- [ ] `npx tsc --noEmit` passes
- [ ] Committed with `feat: <description>` message
