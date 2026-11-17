## Description:

Run AI-simulated user interviews and focus group discussions using atypica.ai's library of human-like personas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owenrao](https://clawhub.ai/user/owenrao)

### License/Terms of Use:

MIT-0

## Use Case:

External product, UX, and research teams use this skill to run AI-simulated one-on-one interviews or focus groups, monitor the session workflow, and retrieve synthesized research reports without recruiting participants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts, interview outputs, persona queries, and generated reports may be sent to atypica.ai.

Mitigation: Avoid confidential or regulated data unless the service's retention and sharing model has been reviewed.

Risk: Generated report share links may expose sensitive research content.

Mitigation: Do not use public share links for sensitive reports.

Risk: Verbose mode can expose private inputs during direct Bash usage.

Mitigation: Disable verbose output when prompts, tokens, or research data are sensitive.

Risk: An untrusted ATYPICA_ENDPOINT value can redirect direct Bash wrapper calls.

Mitigation: Run the wrapper only in trusted environments or explicitly set the intended endpoint.

## Reference(s):

- [atypica Universal Agent API Reference](references/api-reference.md)
- [atypica MCP documentation](https://atypica.ai/docs/mcp)
- [atypica Universal MCP endpoint](https://atypica.ai/mcp/universal)
- [ClawHub skill page](https://clawhub.ai/owenrao/skills/atypica-user-interview)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing workflow instructions for creating sessions, sending messages, handling interactions, polling status, and retrieving reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
