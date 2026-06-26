# Persistent Memory

Follow-up memory turns recent triage into an operating system.

Track a follow-up when:
- someone is waiting on the user
- the user is waiting on someone else and should re-nudge later
- a decision was deferred and should be revisited
- silence itself now matters

Suggested follow-up fields:
- id
- source
- person or entity
- program
- waiting_on
- priority
- last_signal
- next_nudge
- summary
- status

Decision memory keeps unresolved choices alive over time.

Track a decision when:
- the user must choose between options
- the user must approve or reject something
- a thread is blocked on the user's answer
- a setup step needs the user's consent

Suggested decision fields:
- id
- source
- decision_owner
- program
- priority
- deadline
- blocking
- options
- recommended
- summary
- status

Keep both ledgers concise and current instead of historical.
