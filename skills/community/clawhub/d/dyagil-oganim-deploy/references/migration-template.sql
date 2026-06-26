-- ============================================================
-- Stage <N> — <one-line description>
--
-- Background:
--   <Why this migration exists. Be specific about the bug or feature being
--    addressed. Future-you will thank present-you.>
--
-- Idempotent. Safe to re-run.
-- ============================================================

-- IMPORTANT: the Supabase pooler may leave us in `authenticated` from a
-- previous transaction, which breaks ownership checks (e.g. on profiles).
-- Always reset the role at the top.
reset role;

-- =====================================================================
-- 1. SCHEMA CHANGES (add columns, tables, indexes — all idempotent)
-- =====================================================================

-- Example: add columns to an existing table
-- alter table public.deals
--   add column if not exists customer_facing_notes text,
--   add column if not exists won_at timestamptz;

-- Example: create a new table
-- create table if not exists public.<name> (
--   id uuid primary key default gen_random_uuid(),
--   ...
--   created_at timestamptz default now()
-- );

-- =====================================================================
-- 2. RLS POLICIES
-- =====================================================================

-- ALWAYS enable RLS on new tables.
-- alter table public.<name> enable row level security;

-- Customer-facing read access — restrict to the row's owner.
-- drop policy if exists <name>_self_select on public.<name>;
-- create policy <name>_self_select
--   on public.<name> for select
--   using (auth.uid() = user_id);

-- Staff override — every privileged table needs is_staff() ALL.
-- drop policy if exists <name>_staff_all on public.<name>;
-- create policy <name>_staff_all
--   on public.<name> for all
--   using (public.is_staff()) with check (public.is_staff());

-- CRITICAL: any UPDATE policy on a table with `role`/`email` columns MUST
-- include a WITH CHECK that forbids changing those fields. Otherwise a
-- customer can self-promote to admin. See supabase-security-audit skill.

-- =====================================================================
-- 3. TRIGGERS / FUNCTIONS
-- =====================================================================

-- Functions used by RLS should be SECURITY DEFINER with an explicit
-- search_path so they aren't fooled by callers manipulating the path.
-- create or replace function public.<name>()
-- returns trigger
-- language plpgsql
-- security definer
-- set search_path = public
-- as $$
-- begin
--   ...
--   return NEW;
-- end;
-- $$;
--
-- drop trigger if exists trg_<name> on public.<table>;
-- create trigger trg_<name>
--   before insert on public.<table>
--   for each row execute function public.<name>();

-- =====================================================================
-- 4. SEED / BACKFILL
-- =====================================================================

-- Seed data should be conditional so re-runs don't duplicate.
-- insert into public.<name> (...) values (...)
--   on conflict (...) do nothing;

-- Backfill is also idempotent: only update rows that haven't been set yet.
-- update public.<table> set <col> = <value> where <col> is null;


-- ============================================================
-- handle_new_user() reference implementation
-- ============================================================
-- Drop-in template that MERGES an existing profile by email instead of
-- creating a duplicate. Use whenever your project has a "staff creates a
-- profile in the CRM before the customer signs up via Supabase auth" flow.
-- ============================================================
--
-- create or replace function public.handle_new_user()
-- returns trigger
-- language plpgsql
-- security definer
-- set search_path = public
-- as $$
-- declare
--   existing_id uuid;
-- begin
--   select id into existing_id
--     from public.profiles
--    where lower(email) = lower(NEW.email)
--      and id <> NEW.id
--    limit 1;
--
--   if existing_id is not null then
--     -- Clear unique columns on the old row so the move doesn't trip
--     -- unique constraints, then create the new auth-side row.
--     update public.profiles
--        set national_id = null, email = null
--      where id = existing_id;
--
--     insert into public.profiles (id, email, role, created_at)
--     values (NEW.id, NEW.email, 'customer', now())
--     on conflict (id) do nothing;
--
--     -- Copy meaningful fields from the existing profile to the new id.
--     update public.profiles dst
--        set first_name = coalesce(nullif(dst.first_name, ''), src.first_name),
--            last_name  = coalesce(nullif(dst.last_name,  ''), src.last_name),
--            phone      = coalesce(nullif(dst.phone,      ''), src.phone),
--            national_id = coalesce(dst.national_id, src.national_id),
--            birth_date  = coalesce(dst.birth_date, src.birth_date)
--            -- ...add every column you actually use
--       from public.profiles src
--      where dst.id = NEW.id and src.id = existing_id;
--
--     -- Repoint every FK that referenced the orphan profile.
--     update public.deals              set customer_id = NEW.id where customer_id = existing_id;
--     update public.tasks              set customer_id = NEW.id where customer_id = existing_id;
--     update public.documents          set user_id     = NEW.id where user_id     = existing_id;
--     update public.invoices           set user_id     = NEW.id where user_id     = existing_id;
--     update public.notifications      set user_id     = NEW.id where user_id     = existing_id;
--     update public.inquiries          set user_id     = NEW.id where user_id     = existing_id;
--     update public.customer_events    set customer_id = NEW.id where customer_id = existing_id;
--     update public.tax_engagements    set customer_id = NEW.id where customer_id = existing_id;
--     update public.chat_conversations set customer_id = NEW.id where customer_id = existing_id;
--     update public.children           set parent_id   = NEW.id where parent_id   = existing_id;
--
--     -- Finally delete the orphan.
--     delete from public.profiles where id = existing_id;
--   else
--     insert into public.profiles (id, email, role, created_at)
--     values (NEW.id, NEW.email, 'customer', now())
--     on conflict (id) do nothing;
--   end if;
--   return NEW;
-- end;
-- $$;
--
-- drop trigger if exists on_auth_user_created on auth.users;
-- create trigger on_auth_user_created
--   after insert on auth.users
--   for each row execute function public.handle_new_user();
