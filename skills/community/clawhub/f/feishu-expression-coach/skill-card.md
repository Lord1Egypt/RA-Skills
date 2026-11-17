## Description:

表达教练 analyzes Chinese text or speech-to-text drafts, identifies issues such as verbosity, ambiguity, weak logic, or unsuitable tone, and provides focused suggestions plus a rewritten version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to get concise Chinese-language feedback on written messages, speech-to-text drafts, and message previews. It is intended to help users make communication clearer, shorter, better structured, and more appropriately toned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese trigger phrases may cause the skill to review text when the user intended a different kind of response.

Mitigation: Invoke the skill deliberately when asking for feedback or rewriting, and review the suggested rewrite before sending it.

Risk: Expression rewrites can change tone, emphasis, or intent in a way that does not fit the user's social or workplace context.

Mitigation: Compare the rewrite with the original message and keep the user's intended meaning and personal style before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/feishu-expression-coach)
- [ClawHub publisher profile](https://clawhub.ai/user/rfdiosuao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese expression analysis with score, diagnosis, suggestions, rewritten text, and a short change explanation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reviews user-provided text and does not execute code, persist data, request credentials, or access external services according to the server security evidence.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
