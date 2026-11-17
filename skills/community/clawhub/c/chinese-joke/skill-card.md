## Description:

提供多类型中文笑话，包括谐音梗、程序员笑话、生活趣事和脑筋急转弯，无需外部接口。

This skill is ready for commercial/non-commercial use.

## Publisher:

[djttt](https://clawhub.ai/user/djttt)

### License/Terms of Use:

MIT-0

## Use Case:

Agents can use this skill to retrieve Chinese-language jokes by type or at random for conversational, entertainment, or content drafting tasks without calling an external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid joke types can fail noisily instead of returning a clean user-facing error.

Mitigation: Use the listed joke types from the artifact documentation or add input validation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djttt/skills/chinese-joke)
- [Publisher profile](https://clawhub.ai/user/djttt)
- [Artifact skill instructions](artifact/SKILL.md)
- [Local joke database](artifact/jokes.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text jokes with category labels; Markdown command guidance when explaining use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local JSON-backed content with optional type and count filters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
