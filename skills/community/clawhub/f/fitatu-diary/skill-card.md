## Description:

Keep the user's Fitatu food diary through fitatu-mcp tools by reading and updating meals, nutrition goals, body metrics, workouts, and weekly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jezue](https://clawhub.ai/user/jezue)

### License/Terms of Use:

MIT-0

## Use Case:

People who use Fitatu can connect an agent to review their nutrition intake and goals, log meals and health metrics, update diary entries, and request reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fitatu access can expose sensitive health information and allow diary changes; remote access also uses a session and token.

Mitigation: Use --read-only for reporting-only access, protect the saved session and remote-access token, and confirm changes inferred beyond the user's request.

## Reference(s):

- [fitatu_library project](https://github.com/Jezue/fitatu_library)
- [fitatu_library agent documentation](https://github.com/Jezue/fitatu_library/blob/main/docs/AGENTS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Natural-language responses and structured Fitatu MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update the user's Fitatu diary and health metrics, depending on the request and server permissions.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
