# Data and authorization

Fires: when the project has a database, server API or storage bucket

Leading word: **user B**. You are signed in as B and hold user A's row ids. Then you are the database on the day a migration meets real rows.

Read the schema from its source of truth (migrations, ORM models, `schema.prisma`, `supabase/migrations`, Firestore rules) before the code that uses it.

Artifact: an access matrix (resource × verb → allowed for B? → evidence).

- **constraints** (when there is a schema): For each invariant the app relies on, is there a matching `NOT NULL`, `CHECK`, `FOREIGN KEY`, `UNIQUE`, enum or exclusion constraint? List each invariant with none, and each client enum stored as free text.
- **user-b** (when more than one user's data lives in the same store): For every table, view, RPC, REST or GraphQL route, and storage bucket: as B with A's id, what can you read, insert, update or delete? Check each verb separately: RLS disabled, `using (true)`, a policy for select but not update, `security definer` functions that never check the caller, routes that take the user id from the request body, storage paths not scoped to the owner, broad Firestore rules.
- **unbounded-growth**: What grows per user per day with no cap, TTL or retention job: events, logs, images, versions, notifications, soft-deleted rows? Estimate a heavy user's year against the plan's storage and row limits.
- **migration-on-real-data** (when there are migrations): For each pending or recent migration: which existing rows break the new constraint? Write the query that counts them. Check for locks on large tables, backfills in one transaction, and changes that are not expand-then-contract.
- **delete-account** (when users have accounts): The user deletes their account. What survives: rows in other tables, storage objects, backups, analytics, third-party processors, caches on other devices? Each survivor is a privacy finding.

Confirm against a local or branch database. A write against production to prove a finding is out of bounds; mark it `PLAUSIBLE` instead.

Done: the access matrix has a row for every resource, and every pending migration has a violator count or a reason it cannot have one.
