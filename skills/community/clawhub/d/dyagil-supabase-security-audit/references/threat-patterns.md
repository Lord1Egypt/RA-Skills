# Threat patterns to look for in Supabase projects

This is a checklist of real, exploitable mistakes that have shown up in projects
in this workspace. Each section describes the pattern, the impact, the detection
query, and the fix.

## 1. UPDATE policy without WITH CHECK on `role`

**Pattern**

```sql
create policy profiles_self_update
  on public.profiles
  for update
  using (auth.uid() = id);   -- no WITH CHECK
```

**Impact**

Any authenticated customer can run
`update profiles set role='admin' where id=auth.uid()`,
because `is_staff()` (typically `role in ('admin','agent')`) then returns true
and unlocks every `*_staff_all` policy in the schema.

**Detection**

```sql
select c.table_name, p.policyname, p.with_check
  from information_schema.columns c
  join pg_policies p
    on p.schemaname = c.table_schema and p.tablename = c.table_name
 where c.table_schema = 'public'
   and c.column_name in ('role', 'email')
   and p.cmd = 'UPDATE'
   and (p.with_check is null
        or (p.with_check not like '%role%' and p.with_check not like '%is_staff%'));
```

**Fix**

Use `scripts/hotfix-role-lock.sql` as a starting point.

## 2. RLS disabled on a public-schema table

**Pattern**

A migration creates a new table and forgets `alter table ... enable row level security`.

**Impact**

Anonymous (anon key) clients can read or even write everything in that table.

**Detection**

```sql
select tablename
  from pg_tables
 where schemaname='public' and not rowsecurity;
```

**Fix**

```sql
alter table public.<name> enable row level security;
-- then add at minimum a staff-only or owner-only policy.
```

## 3. Permissive client-facing policy without `auth.uid()` scoping

**Pattern**

```sql
create policy foo_read on public.deals for select using (true);
```

**Impact**

Any logged-in user reads every row.

**Detection**

```sql
select tablename, policyname, qual
  from pg_policies
 where schemaname='public'
   and cmd='SELECT'
   and qual !~ 'auth\\.uid|is_staff';
```

(Allow-listed reference tables such as `pipelines` or `pipeline_products` are
legitimate exceptions — confirm the table is intended to be public.)

## 4. Storage bucket without folder-isolated RLS

**Pattern**

```sql
create policy "any_user_read" on storage.objects
  for select using (auth.role() = 'authenticated');
```

**Impact**

Authenticated user A can fetch user B's files by guessing their `storage_path`.

**Fix**

```sql
create policy "user_owned_read" on storage.objects
  for select using (
    bucket_id = 'documents'
    and (storage.foldername(name))[1] = auth.uid()::text
  );
```

## 5. Service-role key in client bundle

**Pattern**

Vite/Webpack accidentally bundles a server env var into client JS, or a
developer copy-pastes the wrong key into `createClient`.

**Detection**

```bash
# Scan deployed JS for the JWT shape that service_role keys use.
curl -s https://<site>/portal/portal.js | grep -E 'eyJ[A-Za-z0-9_-]+\\.eyJ[A-Za-z0-9_-]+'

# Each match: decode the payload (2nd dot-section, base64url) and look for
#   "role":"service_role"
```

**Fix**

Rotate the key in Supabase Studio → API Settings → Reset service key
**and** replace the value in Vercel env / wherever it lives. Any client that
held a service-role key must be treated as compromised: rotate, then audit the
project for unexpected writes.

## 6. CORS `*` on admin-only endpoints

**Pattern**

A serverless function for `/api/manage-staff` sets
`Access-Control-Allow-Origin: *`.

**Impact**

Combined with a stolen Bearer token this allows attacks from any origin. Not as
severe as a missing auth check, but it weakens defense-in-depth.

**Fix**

Restrict CORS to the project's own origin(s):

```js
const ALLOWED = ['https://oganimy.co.il', 'https://oganim.vercel.app'];
const origin = request.headers.origin || '';
response.setHeader('Access-Control-Allow-Origin',
  ALLOWED.includes(origin) ? origin : ALLOWED[0]);
response.setHeader('Vary', 'Origin');
```

## 7. Magic-link redirect not whitelisted → tokens land in URL hash on the
   wrong page

**Pattern**

Code calls `auth.admin.generate_link({ redirect_to: 'https://site/portal/' })`
but `https://site/portal/` is not in the Supabase Redirect URL allow-list. The
auth server silently rewrites the redirect to the Site URL (e.g.
`https://site/`), and the `access_token=...` hash arrives on the marketing
homepage instead of the portal.

**Impact**

UX bug, not a security bug — but it _looks_ like one (tokens visible in the
URL on the wrong page).

**Fix**

Generate the link manually as
`https://<site>/portal/?token_hash=<hashed_token>&type=magiclink`
and let the portal call `auth.verifyOtp({ token_hash, type })` itself. Bypasses
the redirect-whitelist altogether.

## 8. Profile auto-create trigger creates duplicates instead of merging

**Pattern**

```sql
create function handle_new_user() ...
  insert into profiles(id, email) values (NEW.id, NEW.email);
```

When a staff member created a customer profile **before** the customer signed
up via Supabase auth, the auth-side insert creates a SECOND profile row.
`auth.uid()` now points at the empty new row; all of the customer's data
(deals, events, documents) stays on the orphan profile.

**Impact**

Customer sees an empty portal even though their data exists in the database.

**Fix**

Update the trigger to merge instead of duplicate. See the
`migration-stage15-profile-dedupe.sql` template in the oganim project for
reference (FK repoint + delete orphan).
