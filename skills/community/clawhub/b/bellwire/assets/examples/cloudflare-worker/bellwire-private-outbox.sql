-- SPDX-License-Identifier: MIT-0
create table if not exists bellwire_private_outbox (
  reference text primary key check (
    length(reference) between 22 and 200
    and reference not glob '*[^A-Za-z0-9_-]*'
  ),
  event_type text not null,
  title text not null,
  body text not null,
  subtitle text,
  occurred_at text not null,
  data_json text not null default '{}',
  deep_link text,
  logo_url text,
  expires_at integer not null
);

create index if not exists bellwire_private_outbox_occurred_at
  on bellwire_private_outbox (occurred_at desc);
