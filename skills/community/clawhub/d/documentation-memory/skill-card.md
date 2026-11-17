## Description:

Gives agents a way to store, recall, and search documentation context using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to help an agent remember documentation facts, recall previously stored context, and reuse that context while maintaining docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation summaries may be sent to an external persistent memory service and later reused without clear approval or data limits.

Mitigation: Use only a scoped BlueColumn key, store only explicit documentation facts, and have the agent show and sanitize summaries before sending them to memory.

Risk: Stored documentation context could include confidential plans, customer data, credentials, or internal URLs.

Mitigation: Review content before storage and avoid sending sensitive or credential-like material to persistent memory.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/documentation-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples for storing notes, recalling documentation context, and adding quick notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
