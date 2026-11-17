## Description:

Encodes and decodes Cashu tokens hidden in emojis using Unicode variation selectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced users can use this skill to encode Cashu token content into emoji text and decode emoji-hidden token content for automation or utility workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad execution, file, and API authority for an emoji Cashu-token utility.

Mitigation: Run it only in a sandboxed agent workspace with the minimum required tool permissions, and review requested commands or file writes before execution.

Risk: Cashu tokens can represent bearer value, and hiding them in emoji text does not make them private or safe to share.

Mitigation: Use only test or low-value tokens unless the publisher adds explicit bearer-token warnings and stronger handling guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/text result examples and shell configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include emoji-encoded token text, decoded token content, execution logs, and status metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
