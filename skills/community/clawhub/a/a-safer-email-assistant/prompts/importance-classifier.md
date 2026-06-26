# Importance Classifier Template

Use this rubric only on unseen incoming messages.

## Inputs

- User importance criteria:
  - VIP senders/domains
  - urgency signals (deadlines, payment issues, legal/compliance, outages)
  - business goals (sales pipeline, hiring, customer escalations)
  - ignore patterns (newsletters, notifications, bulk mail)
- Message fields:
  - `from`, `to`, `cc`, `subject`, `internal_date`, `body_text`, `id`

## Required output per message

- `importance`: `high|medium|low`
- `why`: short rationale tied to user criteria
- `action`: `notify_now|batch_digest|ignore`
- `draft_recommended`: `true|false`

## Scoring guidance

- High:
  - VIP sender and clear request/deadline
  - blocked decision that needs user response
  - financially or operationally critical issue
- Medium:
  - relevant thread update without immediate urgency
  - useful context for current projects
- Low:
  - informational updates with no required action
  - automated/non-actionable messages matching ignore patterns
