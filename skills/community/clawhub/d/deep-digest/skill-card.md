## Description:

Extracts cognitive patterns, key insights, and action signals from text input such as messages, notes, articles, and conversations, organizing results into facts, patterns, and cognitive transformations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heshengshi](https://clawhub.ai/user/heshengshi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn long-form text, chats, meeting notes, articles, and personal notes into structured analysis with factual summaries, pattern observations, and action signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive input may be included in emitted workflow prompts or downstream logs, despite the artifact claiming redaction behavior.

Mitigation: Use only non-sensitive text until redaction and runtime handling are fixed; review inputs for private notes, chats, credentials, and personal data before running the skill.

Risk: The digest depends on an LLM to infer patterns and action signals, which can overinterpret weak source material.

Mitigation: Review generated pattern and action sections against the original text before using them for decisions.

## Reference(s):

- [Deep Digest ClawHub release](https://clawhub.ai/heshengshi/skills/deep-digest)
- [heshengshi publisher profile](https://clawhub.ai/user/heshengshi)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [JSON workflow containing prompts for Markdown digest generation and optional evaluator review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports full, facts-only, patterns-only, and signals-only modes; default configuration enables evaluator veto with a 0.6 threshold and up to 2 retries.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
