# Risk Model

This Skill uses a small operational rubric so a non-specialist can understand
what to do next. It is not a vulnerability score, legal opinion, compliance
attestation, or OWASP rating.

## Evidence and confidence

Use one evidence label for every material claim:

| Label | Use it when |
| --- | --- |
| Observed | A current read-only inspection saw the capability or event. |
| Available | The inspected configuration or permission makes it possible, but no current event proves use. |
| Not found | The named scope was inspected and the item was absent there. |
| Unknown | The relevant scope, provider behavior, or runtime control was not available to inspect. |

Confidence describes the audit as a whole:

- High: the relevant runtime, configuration, and data-flow boundaries were
  directly inspected.
- Medium: the main path was inspected but one provider, connector, or runtime
  behavior remains inferred.
- Low: the report relies mainly on declarations, screenshots, or a partial
  scope.

Never turn an Unknown claim into Not found. A missing observation can lower
confidence without proving safety.

## The three-part combination

| Element | Plain-language question | Common examples |
| --- | --- | --- |
| Secret Source | What private or valuable data could the agent read? | API keys, SSH keys, browser state, private repository files, customer records, local session data, confidential documents |
| External Sink | How could data leave the trusted boundary? | Model request, HTTP or webhook, browser upload, email or chat, Git push, connector, telemetry or log service, another agent |
| Untrusted Content | Who besides the trusted operator can influence the instructions? | Web pages, email, issue text, pull requests, downloaded files, mutable Skill docs, memory, retrieved chunks, tool output |

## External sink classes

Record the recipient and control boundary instead of treating every request as
the same:

| Class | Meaning |
| --- | --- |
| Trusted processing destination | An intended destination inside the declared trust boundary. |
| Third-party processing or retention destination | An outside provider or service named for the task, with handling or retention still needing evidence. |
| Agent-controlled external action | The agent can choose the recipient or payload. |
| Attacker-controlled or mutable destination | Untrusted content can choose, change, or redirect the recipient or payload. |

An agent Skill, README, or manifest declaration is a lead. Mark a capability
Available only when runtime permissions, executable implementation, or an
equivalent enforcement fact makes it reachable. A URL alone is not proof that
the agent can send data there.

Classify the combination as:

| Result | Decision rule |
| --- | --- |
| Confirmed | Evidence shows a reachable Secret Source, an external sink outside the intended boundary, and a plausible path from untrusted content to sending that sensitive data or choosing an unapproved recipient. |
| Likely | All three elements are available, but the influence path, runtime enforcement, or actual sink behavior is not fully verified. |
| Not demonstrated | The inspected scope lacks at least one element, or a control clearly separates the elements for the relevant workflow. |
| Unknown | A material element or boundary could not be inspected. |

Confirmed means the path is open, not that a leak occurred. Report actual
transmission separately. Use Observed for a confirmed event, Not found when the
inspected event sources contain no matching event, and Unknown when the event
boundary could not be checked. Available describes capability, not an event.

## Severity

Choose the highest level supported by evidence. When two findings differ, keep
both in the report and use the higher overall level.

| Level | What it means to a user | Typical evidence | First response |
| --- | --- | --- | --- |
| Low | The agent has a small, controlled reach and the reviewed path is unlikely to expose sensitive data. | Narrow read-only scope, no sensitive source or external sink in scope, clear separation of external content, and no material unknown. | Keep the boundary and review it when tools or Skills change. |
| Medium | There is a real gap or uncertainty, but the reviewed path is limited or not yet a high-impact route. | Unknown egress or retention, sensitive data in context or logs, mutable instructions, broad read-only access, or a missing audit trail. | Reduce the gap before using the agent with sensitive work. |
| High | A mistake or malicious input could plausibly cause serious harm. | Shell or write authority, broad filesystem access, external writes, no isolation or approval, or a Likely three-part combination. | Pause high-impact use, narrow access, and contain the risky sink. |
| Critical | The path can carry sensitive data outside the intended boundary with an unapproved payload or recipient, or through an attacker-controlled or mutable outside destination under attacker-influenced instructions, or a real incident is evidenced. | Confirmed three-part combination, observed exfiltration, credential use, account takeover, destructive administration, or active compromise. | Contain first, preserve evidence, revoke or rotate affected credentials through the owner process, and investigate. |

Use Medium for a material audit blind spot when the scope is too incomplete to
justify Low. Do not invent a Critical incident from an unknown provider policy.
Explain the exact uncertainty and the check that would resolve it.

## High-impact modifiers

Raise a finding when any of these are present:

- credentials, payment instruments, production administration, or personal data
  are reachable;
- shell, code execution, delete, publish, send, push, or account-management
  actions are available;
- network egress is unrestricted or the destination is mutable or unknown;
- external content or memory can change tool choice, parameters, or future
  behavior;
- the agent runs with the user's full host identity and no meaningful
  isolation;
- the user cannot preview, approve, interrupt, or audit the action.

These modifiers describe impact. They do not replace evidence for the
three-part combination.

## Evidence references in the report

Give material conclusions, worst-case consequences, and remediation reasons an
evidence row or an explicit Unknown reference. A remediation recommendation
does not prove that its triggering event happened.
