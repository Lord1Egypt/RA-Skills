## Description:

Pre-send verification for outbound agents: a separate control placed before send() that gives outbound messages an independent verdict across deterministic gates and an optional LLM semantic check, with a per-message audit log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workloftai](https://clawhub.ai/user/workloftai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams operating outbound text agents use this skill to check email, social, helpdesk, and notification drafts before sending. It is aimed at agent stacks that need independent pre-send controls and readable audit records, especially in regulated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive outbound drafts may be sent to an unapproved hosted or third-party LLM review path.

Mitigation: Use a trusted local or approved LLM callable for sensitive drafts, or complete data-handling review before using the hosted endpoint.

Risk: The verifier can incorrectly approve sensitive or manipulated outbound messages.

Mitigation: Treat PASS as a control signal rather than a guarantee, keep human review for high-risk sends, and monitor audit logs for verifier misses.

Risk: Recipient-based redlist exceptions can allow a redlisted term when the recipient address contains that term.

Mitigation: Harden or disable recipient exceptions for confidential workflows and test redlist behavior against expected leakage cases.

Risk: LLM semantic checks depend on valid JSON responses and provider behavior.

Mitigation: Use stricter response validation and fail closed for regulated or confidential use cases where WARN is not sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workloftai/skills/agent-verifier)
- [Workloft Research Note 05: Pre-send verification](https://workloft.ai/labs/notes/pre-send-verifier-2026-05-09.html)
- [Workloft Labs API](https://workloft.ai/labs/api.html)
- [Redlist example](redlist.example.txt)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, JSON]

**Output Format:** [Markdown guidance with Python snippets; runtime verifier results are JSON-serializable data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python 3.10+ standard library only; optional LLM callable; verifier truncates message body sent to the LLM to 3000 characters by default]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package version is 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
