# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- `node --import tsx evals/contract.mjs` passes against the adapted graph: no HubSpot connector;
  native `gtm_accounts` (defineAccount) and `gtm_opportunities` (defineDeal); the play is disabled, calls the
  analyst once, calls no connector, and owns one `modelCustomColumn` on `gtm_accounts`, by the deal's
  `account_id`, with exactly the three expansion columns; the analyst has no action and only
  read-only models; the digest has one locked `postMessage`, a writable ledger and `gtm_accounts`
  read-only.
- `cargo-ai connection connector list` shows authorized Slack and Anthropic connectors.
- `context/expansion-plays.md` exists in the project and names what you sell to customers.
- `channelId` was read out loud from the connector's channel autocomplete, and the channel is
  internal.

## Seed

After the deploy, read the two model uuids (`cargo-ai storage model list`) and load fictional
records on the `.example` TLD. Cargo generates every record id (passing an `id` is rejected), so
create the companies first and put each returned `id` into its deals' `account_id`:

```bash
cargo-ai storage record create-bulk --model-uuid <gtm_accounts uuid> --records '[
  {"data":{"name":"Fabrikam","website":"fabrikam.example","owner_id":"4402"}},
  {"data":{"name":"Contoso","website":"contoso.example","owner_id":"4419"}},
  {"data":{"name":"Litware","website":"litware.example","owner_id":"4411"}}
]'
cargo-ai storage record create-bulk --model-uuid <gtm_opportunities uuid> --records '[
  {"data":{"name":"Fabrikam annual","account_id":"<fabrikam id>","amount":38000,"stage_name":"Closed won","close_date":"<11 months ago>","is_closed":true,"is_won":true}},
  {"data":{"name":"Contoso H1","account_id":"<contoso id>","amount":9500,"stage_name":"Closed won","close_date":"<17 months ago>","is_closed":true,"is_won":true}},
  {"data":{"name":"Contoso H2","account_id":"<contoso id>","amount":9500,"stage_name":"Closed won","close_date":"<11 months ago>","is_closed":true,"is_won":true}},
  {"data":{"name":"Litware annual","account_id":"<litware id>","amount":12000,"stage_name":"Closed won","close_date":"<11 months ago>","is_closed":true,"is_won":true}},
  {"data":{"name":"Litware renewal","account_id":"<litware id>","amount":13000,"stage_name":"Closed won","close_date":"<1 month ago>","is_closed":true,"is_won":true}}
]'
```

Replace each `<… ago>` with an ISO date. Three won deals sit inside the window; Litware already
renewed early.

## Pilot

Keep the account records and the Slack permalink as evidence.

- **Judged.** Executing the play once runs the analyst for the three in-window deals and writes a
  signal, a reason and a stamp onto Fabrikam, Contoso and Litware. Contoso's reason names a
  six-month cadence at 9,500. Every outside event a reason names has a dated source in it.
- **Already renewed.** Litware is written `none`, and its reason names the newer win.
- **Same buying cycle.** An account with two won deals inside the window a few days apart is judged
  on its purchase history, not written `none` because one of them is newer than the other.
- **Re-run.** A second execution the same week judges none of the three deals again.
- **Nothing else written.** No deal record changed (`cargo-ai storage query` over `gtm_opportunities` before and
  after).
- **Digest.** The digest posts once, lists the accounts stamped that week with a signal other than
  `none`, at-risk first, with each reason as written on the account. Once the digest's
  `expansion_digests` row reads back through SQL, a re-run that week posts nothing. A native write
  takes minutes to become readable, through SQL and `search_records` alike, so run the digest after
  the play's stamps read back, and re-run it only after its own row does.

## Isolation

- This is one root skill. Its supporting Markdown lives under `references/`, and no nested
  `SKILL.md` exists.
- No import leaves the folder.
