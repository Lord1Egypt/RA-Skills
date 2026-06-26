-- ============================================================
-- Hotfix template: lock down role / email columns on a "profiles"-style table.
--
-- Apply this when `audit.js` reports:
--   🚨 policy:<table>.<name> — UPDATE policy lacks WITH CHECK on role/email
--
-- HOW TO USE:
--   1. Replace `public.profiles` below with the affected table name if
--      different (typically it really is `profiles` / `users` / `members`).
--   2. Confirm the column name is `role` (the rest of the policy assumes it).
--   3. Run via: node ~/.openclaw/workspace/projects/oganim/deploy/run-migration.cjs <this-file>
--      ...or the equivalent migration tool for the project.
--
-- The migration is idempotent. Safe to re-run.
-- ============================================================

reset role;

-- 1. Replace the existing self-update policy with one that locks role + email.
drop policy if exists profiles_self_update on public.profiles;

create policy profiles_self_update
  on public.profiles
  for update
  using (auth.uid() = id)
  with check (
    auth.uid() = id
    and role  is not distinct from (select role  from public.profiles where id = auth.uid())
    and email is not distinct from (select email from public.profiles where id = auth.uid())
  );

-- 2. Belt-and-suspenders DB trigger: even if the policy is later changed by
--    mistake, this trigger rejects role mutations from any non-staff caller.
create or replace function public.tg_profile_role_lock()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  caller_is_staff boolean;
begin
  -- service_role / postgres bypass: auth.uid() is null for those.
  if auth.uid() is null then
    return NEW;
  end if;

  if NEW.role is distinct from OLD.role then
    select coalesce(
             (select role in ('admin','agent') from public.profiles where id = auth.uid()),
             false)
      into caller_is_staff;
    if not caller_is_staff then
      raise exception 'profile.role can only be changed by staff (caller=%)', auth.uid()
        using errcode = '42501';
    end if;
  end if;
  return NEW;
end;
$$;

drop trigger if exists trg_profile_role_lock on public.profiles;
create trigger trg_profile_role_lock
  before update of role on public.profiles
  for each row execute function public.tg_profile_role_lock();
