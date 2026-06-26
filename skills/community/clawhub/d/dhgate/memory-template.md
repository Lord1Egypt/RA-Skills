# Memory Template - DHgate

Create `~/dhgate/memory.md` with this structure:

```markdown
# DHgate Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Buying Profile
primary_use:
destination_country:
typical_budget:
quantity_style:
lead_time_tolerance:

## Risk Boundaries
avoid_categories:
authenticity_tolerance:
quality_floor:
max_first_order_risk:

## Active Focus
current_need:
main_constraints:
decision_stage:

## Notes
- Confirmed seller preferences
- Proven shipping observations
- Open questions that still matter

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active support | Keep refining sourcing and dispute context |
| `complete` | Stable buying pattern | Maintain with lighter check-ins |
| `paused` | User paused sourcing work | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Skip setup questions unless requested |

## File Templates

Create `~/dhgate/shortlist.md`:

```markdown
# DHgate Shortlist

## Candidate Listings
### Option A
- link:
- seller:
- item:
- quantity:
- visible_price:
- key_green_flags:
- key_red_flags:
- next_check:
- status: watch | compare | reject | sample
```

Create `~/dhgate/sourcing.md`:

```markdown
# Sourcing Notes

## Seller Conversations
### Seller / Store
- item:
- questions_sent:
- answers_received:
- spec_gaps:
- packaging_or_moq_notes:
- confidence: low | medium | high
```

Create `~/dhgate/orders.md`:

```markdown
# Orders

## Active Orders
### Order
- item:
- order_date:
- promised_ship_window:
- tracking_status:
- current_issue:
- next_action:
```

Create `~/dhgate/disputes.md`:

```markdown
# Dispute Planner

## Case
- order:
- problem_type:
- evidence_ready:
- requested_remedy:
- seller_response_deadline:
- escalation_needed: yes | no
```

## Key Principles

- Save only what improves the next buying or dispute decision.
- Prefer facts from listings, seller replies, and completed orders over speculation.
- Ask before writes and update `last` when the buying context changes.
- Do not store payment credentials, identity documents, or unrelated personal data.
