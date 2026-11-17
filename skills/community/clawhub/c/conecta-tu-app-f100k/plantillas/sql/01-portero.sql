-- ============================================================
-- EL PORTERO — lista de acceso de tu app
-- Pégalo en Supabase → SQL Editor → Run. Se puede correr dos veces sin romper nada.
-- ============================================================

-- 1) Historial: cada subida de CSV, alta por webhook o cambio manual deja un "lote".
--    Sirve para responder "¿por qué María no entra?" con evidencia.
create table if not exists public.lotes_miembros (
  id            uuid primary key default gen_random_uuid(),
  hecho_por     text not null,                 -- correo del admin, 'webhook' o 'cron'
  hecho_en      timestamptz not null default now(),
  archivo       text,                          -- nombre del CSV (null si no hubo archivo)
  origen        text not null check (origen in ('csv','manual','webhook','pasarela','cron')),
  total         int not null default 0,
  agregados     int not null default 0,
  quitados      int not null default 0,
  nota          text
);

-- 2) LA LISTA. Si un correo no está aquí, no entra. Punto.
create table if not exists public.miembros_activos (
  email       text primary key,                -- siempre en minúsculas y sin espacios
  nombre      text,
  lote_id     uuid not null references public.lotes_miembros(id),
  agregado_en timestamptz not null default now(),
  origen      text not null default 'csv' check (origen in ('csv','manual','webhook','pasarela','cron'))
);
create index if not exists idx_miembros_lote on public.miembros_activos(lote_id);

-- 3) Rebotes: quién intentó entrar y el portero no lo dejó.
--    Sin esto el muro pierde gente en silencio (alguien pagó con otro correo y nadie se entera).
create table if not exists public.rebotes (
  id         bigint generated always as identity primary key,
  email      text not null,
  intento_en timestamptz not null default now()
);
create index if not exists idx_rebotes_email on public.rebotes(email, intento_en desc);

-- 4) Candado: RLS encendido y SIN políticas = nadie lee ni escribe desde el navegador.
--    Solo tu servidor, con la llave service_role. Es a propósito.
--    OJO: por eso, si consultas estas tablas desde el navegador te devuelven lista VACÍA
--    sin ningún error. Léelas siempre desde el servidor.
alter table public.lotes_miembros   enable row level security;
alter table public.miembros_activos enable row level security;
alter table public.rebotes          enable row level security;

-- 5) Reemplazo de la lista en UNA sola operación (todo o nada).
--    Si algo falla a la mitad, la lista vieja queda intacta: nadie se queda afuera por un corte.
create or replace function public.reemplazar_miembros(
  p_filas     jsonb,   -- [{"email":"a@b.com","nombre":"Ana"}, ...]
  p_hecho_por text,
  p_archivo   text,
  p_agregados int,
  p_quitados  int,
  p_origen    text default 'csv'   -- 'csv' si lo subiste tú, 'cron' si lo trajo el refresco diario
) returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  v_lote uuid;
  v_total int;
begin
  select count(distinct lower(trim(f->>'email'))) into v_total
  from jsonb_array_elements(p_filas) f
  where coalesce(trim(f->>'email'), '') <> '';

  if v_total = 0 then
    raise exception 'La lista nueva viene vacía: no reemplazo nada (dejaría a todos afuera).';
  end if;

  insert into lotes_miembros (hecho_por, archivo, origen, total, agregados, quitados)
  values (p_hecho_por, p_archivo, p_origen, v_total, p_agregados, p_quitados)
  returning id into v_lote;

  -- Los que diste de alta A MANO se quedan: son tus excepciones (pagó con otro correo, beca, socia).
  -- Salen solo cuando tú los quitas desde el centro de control.
  delete from miembros_activos where origen <> 'manual';

  insert into miembros_activos (email, nombre, lote_id, origen)
  select distinct on (lower(trim(f->>'email')))
         lower(trim(f->>'email')), nullif(trim(f->>'nombre'), ''), v_lote, p_origen
  from jsonb_array_elements(p_filas) f
  where coalesce(trim(f->>'email'), '') <> ''
  on conflict (email) do nothing;

  return v_lote;
end;
$$;

-- La función solo la puede llamar tu servidor.
revoke all on function public.reemplazar_miembros(jsonb, text, text, int, int, text) from public, anon, authenticated;
grant execute on function public.reemplazar_miembros(jsonb, text, text, int, int, text) to service_role;
