## Description:

Places calls to businesses on a user's behalf and reports answers, including when calling several businesses for comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakemarsh](https://clawhub.ai/user/jakemarsh)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to contact businesses on their behalf about reservations, appointments, quotes, availability, or other requested inquiries. It can also call several businesses and summarize their responses.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Call details are sent to an external service, and the security review did not establish which data the transmission carries.

Mitigation: Review the request details before each call and share only information needed for the user's request; keep passwords and payment credentials out of call details.

Risk: The security review is incomplete because a referenced local path was not found.

Mitigation: Resolve and review the missing reference before relying on the skill.

## Reference(s):

- [CallForMe website](https://callforme.tel)
- [CallForMe MCP connection](https://callforme.tel/mcp)
- [CallForMe agent documentation](https://callforme.tel/llms.txt)
- [CallForMe pricing](https://callforme.tel/docs/pricing)
- [ClawHub skill release](https://clawhub.ai/jakemarsh/skills/callforme)

## Skill Output:

**Output Type(s):** [Text, Structured call results, Call transcripts]

**Output Format:** [Plain-language summaries and structured call outcomes, answers, and transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking details, quoted prices, unanswered questions, and call status.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
