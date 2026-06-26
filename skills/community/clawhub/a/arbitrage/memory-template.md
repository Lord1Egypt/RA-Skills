# Memory Template — Arbitrage

Create `~/arbitrage/memory.md` with this structure:

```markdown
# Arbitrage Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Activation
- Trigger phrases:
- Proactive or on-request:
- Markets to ignore:

## Focus Arenas
- Primary arena:
- Secondary arena:
- Current goal:

## Constraints
- Minimum spread worth checking:
- Fees to always model:
- Transfer or settlement limits:
- Max capital at risk:
- Geography or KYC limits:

## Venue Preferences
- Preferred venues:
- Blocked venues:
- Reliability notes:

## Working Notes
- Repeated failure modes:
- User-stated priorities:
- Open questions:

---
*Updated: YYYY-MM-DD*
```

## Initial Directory Structure

Create on first activation:

```bash
mkdir -p ~/arbitrage/archive
touch ~/arbitrage/{memory.md,opportunities.md,venue-notes.md}
```

## Opportunities Template

For `~/arbitrage/opportunities.md`:

```markdown
# Arbitrage Opportunities

## Active

### Opportunity name
- Type:
- Venues:
- Timestamp:
- Gross edge:
- Net edge:
- Max realistic size:
- Status: screening | needs-one-check | ready | rejected
- Blocker:

## Rejected or Archived

### Opportunity name
- Why rejected:
- Lesson:
```

## Venue Notes Template

For `~/arbitrage/venue-notes.md`:

```markdown
# Venue Notes

## Venue name
- Products covered:
- Fees:
- Withdrawal or transfer speed:
- Fill or size limits:
- Rule quirks:
- Reliability notes:
```

## Principles

- Save only explicit user-stated preferences and constraints
- Update `last` on each meaningful use
- Confirm important risk limits and blocked venues before relying on them
