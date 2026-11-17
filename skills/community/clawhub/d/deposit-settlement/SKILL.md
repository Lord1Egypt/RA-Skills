---
name: deposit-settlement
description: Settle a US rental security deposit after move-out with the Tektolo deposit settlement engine - the return deadline, which deductions are allowed and how much after depreciation, interest owed, the refund, penalty exposure and a draft itemized statement, every rule cited. Use when a landlord or property manager is closing a move-out, when a tenant asks whether a deposit came back on time or a deduction is allowed, or for a state's deposit rules.
metadata:
  openclaw:
    requires:
      bins:
      - curl
    homepage: https://tektolo.com/capabilities/deposit-settlement?ref=clawhub
---

# Security deposit settlement

Tektolo runs a deterministic, source-cited engine over each state's deposit statute (all 50
states and DC) and a covered city's ordinance (Chicago, San Francisco, Berkeley, Los Angeles,
Seattle, Portland, Minneapolis, Saint Paul). You give it the state, dates, deposit and the deductions the manager
intends to take. It returns the deadline, an assessment of each deduction, interest, the refund,
penalty exposure if the return is late or wrongful, and a draft itemized statement. The same
input always gives the same result (`result_hash`). It computes and cites the rule, and the manager
signs the statement.

## When to use

- Closing a move-out: "when must I return the deposit", "can I charge for the carpet",
  "how much interest do I owe", "what goes in the itemized statement", "what if I'm late".
- A tenant asking about their own deposit: "my landlord didn't return my deposit", "is my
  landlord late", "can they charge for the carpet or paint". Same operation: send `returned`
  (what came back and when) and the deductions the landlord listed; relay `timeliness`.
- A state's (or a covered city's) deposit rules without a specific move-out:
  `deposit_settlement_rules`.

## When not to use

- Pricing the repairs (use the property turnover tools), evictions, rent increases, notice
  periods, tenant demand letters, where to hold the deposit, pet deposits, non-US rentals.
- Kentucky and Tennessee set no statutory deadline (`deadline.status: none_in_statute`): say
  so; never invent a date. Other cities get the state rule plus a warning about local
  ordinances.

## How to call it

- **MCP** (preferred in assistants): add the remote server
  `https://tektolo.com/mcp/rental-property` (the rental-property tools only; `https://tektolo.com/mcp`
  serves every Tektolo tool and keeps working). Call `deposit_settlement_settle` with the
  request below; `deposit_settlement_rules` with `{"state": "IL", "city": "Chicago"}`.
- **REST**: `POST https://tektolo.com/v1/deposit-settlement/settle` (and `/rules`).
- Catalog and schemas: `https://tektolo.com/catalog.json`,
  `https://tektolo.com/capabilities/deposit-settlement`.
- **Web** (for the user to fill in themselves): the free form at
  `https://tektolo.com/tools/rental-property/deposit-settlement` (landlords); for tenants, the
  Security deposit check at `https://tektolo.com/tools/rental-property/deposit-check` (add
  `?state=TX` to prefill the state); the rule for each state is at
  `https://tektolo.com/deposit-settlement/<state>` (for example `/deposit-settlement/illinois`).
- **Before this step**: if the user has move-out findings but no costs yet, the property turnover estimate
  (`property_turnover_quick_estimate`, web tool `/tools/rental-property/property-turnover`) is
  step 1 of the same move-out workflow.

## Building the request

1. `state` (2 letters), `city` if any (adds a city overlay where covered), `deposit_usd`, and
   `vacated_on` (the day the tenant moved out and returned possession). Never invent dates;
   ask for the move-out date if it is missing.
2. When known: `move_in_on` (interest and item ages), `tenancy_ended_on` (if the lease ended on
   another day), `forwarding_address_received_on` (starts or holds the clock in Texas,
   Connecticut, Iowa, Minnesota, Rhode Island, South Dakota, Wyoming), `demand_received_on`
   (the tenant's written demand: Arizona, Kansas, Oklahoma, South Carolina, Mississippi),
   `new_tenant_moved_in_on` (re-rented: West Virginia, Wisconsin), `claim_notice_sent_on`
   (Florida: the day you sent the notice of intent to impose a claim; the balance is due 30
   days after it), `lease_return_days` (a
   period the lease sets: Colorado, Idaho, Maine), `tenant_gave_proper_notice` (Alaska),
   `contractor_needed` (Virginia, West Virginia), `monthly_rent_usd` (deposit cap; Ohio
   interest; Iowa and Nebraska penalties), `building_units` (NY 6+, IL 25+ interest rules),
   `statement_sent_on` (the day the itemized statement went out: on time or late),
   `tenant_gave_forwarding_address: false` (never given: IL, PA, OH, DE, SC, NH safe harbors),
   `deposit_collected_on` / `lease_signed_or_renewed_on` / `lease_term_months` / `furnished`
   (caps: CA AB 12, GA, MD, DE, NM, KS), `rent_ordinance_covered` (Los Angeles RSO, Berkeley
   interest), `interest_rate_percent` (the account rate where interest is the bank's),
   `owner_is_natural_person` (Georgia's small-landlord exemption), `deposit_in_separate_account`
   (Tennessee 66-28-301(c)), `county` (Tennessee: the act covers counties over 75,000 by the
   2010 census), `renter_notice_served_on` (Utah: the owner then has five business days),
   `landlord_filed_action_on` (Michigan: a suit for the damages within 45 days; not given, none
   is assumed).
   For Colorado, send `deposit_required_on` (the actual day submission was required) and
   `colorado_post_closing_occupancy`: true only when the buyer-landlord bought this residence
   from the seller-tenant and both executed a post-closing occupancy agreement under that
   purchase contract before the requirement. Ordinary leases are false; unknown facts stay
   null. C.R.S. 38-12-102.5(2) exempts only qualifying requirements from 2027-01-01; later
   collection or move-out alone does not establish it. Check the linked act in the result.
3. `deductions`: one per charge, with `category` (`unpaid_rent`, `unpaid_utilities`,
   `cleaning`, `carpet`, `flooring`, `paint`, `blinds_window_coverings`, `appliance`,
   `fixture_or_hardware`, `wall_or_door_repair`, `key_or_lock`, `late_fees`,
   `lease_break_fee`, `moving_and_storage`, `reletting_costs`, `trash_and_abandoned_items`, `other_damage`, `other`) and `amount_usd`. For wearing items give
   `item_installed_on` or `item_age_years` (one, not both), and `useful_life_years` when known;
   set `caused_by_tenant: false` for normal wear (damage and cleaning lines only). Cleaning:
   `cleaning_kind` (`beyond_wear`, `routine`, `unknown`). Late fees: `late_payments`. Carpet cleaning is `cleaning` (or `work_kind: cleaning`); `work_kind: repair` is never depreciated. Rent after a re-rental: `rent_through` on the rent line, and `new_tenant_moved_in_on` / `new_tenant_rent_usd` (rent for the new tenant's days is not recoverable twice).
   `description`: what was damaged or owed and the repair or charge. It prints under the
   line on the itemized statement download (HTML or PDF) and is never stored, logged or
   hashed, or put in the result. TX, WI, GA, WA, NH and MA require each deducted item to
   be described, so pass one per deduction there.
4. `documentation`: what the manager has (`itemized_statement`, `receipts`,
   `photos_move_in`, `photos_move_out`, `photos_after_repair`, `cleaning_notice`: Montana);
   leave out what is unknown. Unknown or misspelled fields are rejected, not ignored.
5. `as_of`: today's date, for a repeatable answer.
6. For a tenant: `returned` = `{"what": "nothing" | "full_refund" | "partial_refund" |
   "itemized_statement", "on": "YYYY-MM-DD", "amount_usd": "..."}` (`on` required unless
   nothing came back), the landlord's deductions as listed, and `caused_by_tenant: null` when
   it is disputed whether a charge is damage or normal wear (the line comes back `depends`
   with the amount the rule allows if it is damage). The forwarding address date is the day
   the landlord received it.

## Example

```json
{
  "state": "CA",
  "deposit_usd": "2000",
  "monthly_rent_usd": "2000",
  "move_in_on": "2023-06-01",
  "vacated_on": "2026-09-30",
  "deductions": [
    {"category": "cleaning", "amount_usd": "150"},
    {"category": "carpet", "amount_usd": "1200", "item_age_years": 5},
    {"category": "blinds_window_coverings", "amount_usd": "80", "caused_by_tenant": false}
  ],
  "as_of": "2026-10-09"
}
```

## Relaying the result

- Lead with `deadline.return_by` and its `status` (`upcoming`, `due_today`, `overdue`,
  `not_started` with the missing event, `none_in_statute`), then `totals.refund_due_usd`. In
  Florida with deductions, `itemization_by` is the deadline for the notice of claim and
  `return_by` runs from `claim_notice_sent_on`; relay both. If
  `deadline.extended_to` is set, the statute moves a weekend or holiday last day there; still
  advise acting by `return_by`. Mention `itemization_by` when it differs (Chicago earlier,
  Louisiana later).
- For each deduction marked `no` or `depends`, say why (`notes`): normal wear, not a listed
  deduction, or missing item age.
- Give `penalty_exposure` as exposure under the statute, not a verdict, including any city
  penalty in `penalty_exposure.additional` (Portland, Berkeley).
- Offer `statement.text` as the draft itemized statement (no names or addresses in it).
- Relay `warnings`, `assumptions` (for example assumed useful lives) and `unknowns` (for example
  a missing forwarding address).
- Give each citation with its link (`citations[].url`) and the rules' date
  (`provenance.rules_as_of`), and relay the result's `disclaimer` word for word:
  "This is not legal advice. Check the linked sources before you rely on it. You decide, sign and send."
- If the user needs an audit trail, keep the `result_hash` and `run.ruleset_version`. Over MCP
  they come back only when you call with `audit: true` (REST always returns them).
- If a call says the daily free limit is reached, tell the user when it resets and do not
  retry; `deposit_settlement_rules` still works. The message names the page for a free
  connector URL with its own allowance when the user shares a hosted assistant's limit.
- `outcome` is the one answer the summary is worded from: `owed_now_usd` (what is still owed
  to the tenant, net of what came back), `next_due` and `stages` (each step's date and status:
  met, late, short, overdue, due today, upcoming), and `uncertain` (what the answer still turns
  on). `deadline.status` is `met` or `late` once `returned` shows the refund went out. Never say
  "interest $0.00" when `outcome.interest_unknown` is true.
- With `returned`, also relay `timeliness`: `late` (true, false, or null when the clock has not
  started or the statute sets no deadline), `days_late`, and each check's `due_by`. With
  nothing returned, `late` is true only once every way of meeting the rule has passed (in
  Florida, the refund at 15 days or the notice of claim at 30). Give the refund as the range
  `totals.refund_min_usd` to `totals.refund_due_usd` when lines depend. State the rule and
  the numbers; do not take a side or predict a court.
