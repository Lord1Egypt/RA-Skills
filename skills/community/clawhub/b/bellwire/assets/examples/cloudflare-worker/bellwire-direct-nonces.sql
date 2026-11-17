-- SPDX-License-Identifier: MIT-0
create table if not exists bellwire_nonces (
  nonce text primary key,
  expires_at integer not null
);

create index if not exists bellwire_nonces_expiry_idx
  on bellwire_nonces(expires_at);
