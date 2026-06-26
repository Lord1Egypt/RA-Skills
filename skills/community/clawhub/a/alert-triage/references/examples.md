# Worked examples for alert-triage

## Example 1: customer-facing outage

### Input
"Checkout API error rate exceeded 20% for 6 minutes across production."

### Triage
- severity: critical
- outcome: send-now
- audience: operator
- timing: immediate
- reason: active customer impact with clear need for rapid intervention

## Example 2: repetitive background job failures

### Input
"Nightly export job failed again. Same error signature as previous 4 alerts in the last 30 minutes."

### Triage
- severity: medium
- outcome: suppress-as-duplicate
- audience: system
- timing: current window
- reason: same underlying issue, no new information beyond repetition count

## Example 3: billing sync lag

### Input
"Billing sync is delayed by 18 minutes but recovering. No failed invoices yet."

### Triage
- severity: medium
- outcome: batch-later
- audience: owner
- timing: next-digest
- reason: useful and actionable, but not urgent while recovery is in progress and no downstream damage is present

## Example 4: vanity metric movement

### Input
"Homepage traffic is down 4% compared with the same hour last week."

### Triage
- severity: info
- outcome: ignore
- audience: system
- timing: none
- reason: low-signal fluctuation with no clear immediate action

## Example 5: escalation trigger

### Input
"Primary responder did not acknowledge the production database failover alert within 10 minutes."

### Triage
- severity: critical
- outcome: escalate
- audience: operator
- timing: immediate
- reason: response policy breached on a critical service issue

## Example 6: digest-worthy alert cluster

### Input
"Five low-priority content publishing warnings occurred across different jobs between 01:00 and 05:00. All retries succeeded."

### Triage
- severity: low
- outcome: batch-later
- audience: owner
- timing: morning-digest
- reason: useful pattern signal, but interruptions are unnecessary because recovery succeeded
