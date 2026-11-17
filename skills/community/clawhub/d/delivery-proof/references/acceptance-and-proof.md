# Acceptance and proof protocol

Use this protocol before delivery work starts. It makes delivery acceptance,
economic proof, and public publication separate decisions.

Run Authorization permits private fulfillment, acceptance-check preparation,
evidence handling, and correction work without another approval. It never
authorizes buyer-facing delivery. Return the checklist and evidence state to
`moneyprinter` so Money Machine Run continues or waits honestly for an external
result.

## Acceptance checklist

Record each item before delivery. A criterion must be observable and tied to
the agreed deliverable; do not change it after seeing the result without
recording the change and obtaining the appropriate client agreement.

| Check | Record before delivery |
| --- | --- |
| Deliverable | Exact artifact, service, and exclusions |
| Acceptance criteria | Observable completion and quality conditions |
| Acceptance authority | Named role or client-approved decision maker, if provided |
| Delivery channel and timing | Authorized destination and due window |
| Revision, correction, and refund terms | Agreed path and responsible party |
| Evidence plan | Minimum records needed to support the result label |
| Privacy plan | Consent, redactions, retention location, and omissions |
| Human review | Required human reviewer, scope, and approval condition |

If scope, acceptance authority, criteria, delivery capacity, correction path,
or privacy authority is unknown, mark it `Unknown`; do not claim acceptance.

Stage the exact delivery payload or artifact, destination, channel/account,
timing, scope, expected cost, evidence label, prerequisite statuses, and
rollback/correction path. After an immediately preceding exact approval, the
current host may perform only that approved action, record a delivery `Action
receipt`, and return it to `moneyprinter`. Broad, batch, stale, or materially
changed permission is invalid.

## Evidence labels

Use exactly one current label for each reported result. Supporting records stay
private or redacted unless specific publication consent permits disclosure.

| Observed fact | Required label |
| --- | --- |
| A benchmark grader awarded $2,000 of simulated task value | `Simulation` |
| An invoice for $2,000 was sent but remains unpaid | `Revenue booked` |
| A $500 card payment settled and an inspected, privacy-safe settlement artifact supports it | `Cash collected` |
| An inspected, privacy-safe signed-obligation artifact exists but payment has not settled | `Revenue contracted` |
| Reply, meeting, proposal, waitlist, or stated intent | `Pipeline signal` |
| Modelled value with stated assumptions and sensitivity | `Estimated economic value` |
| Reported result without the artifact required for a stronger label | `Unverified anecdote` |

Never infer settlement, acceptance, a contract, or permission from a benchmark,
invoice, draft, dashboard, page view, or anecdote.

## Evidence handling and failure record

Record the source, date range, authorized custodian, and redaction decision for
each retained item. Do not retain credentials, unnecessary personal data, full
client files, payment tokens, or regulated data. A redaction must preserve the
meaning of the claimed fact without exposing protected details.

For every failed criterion, rejection, correction, refund, missing record, or
privacy constraint, record: what happened, when, the evidence available, the
economic effect if known, the owner of the next step, and whether it blocks
acceptance. Do not publish this material without the same specific permission
and immediate approval gate required for any other customer material.
Preserve the delivery Action receipt with the minimum privacy-safe supporting
proof, then return the observed acceptance and economic facts to `moneyprinter`.
