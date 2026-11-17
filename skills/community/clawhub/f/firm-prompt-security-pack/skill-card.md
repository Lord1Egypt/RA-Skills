## Description:

Prompt injection and jailbreak detection pack with 16 compiled regex patterns across CRITICAL, HIGH, and MEDIUM severity levels for single-prompt and batch scanning modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to scan user prompts for prompt-injection and jailbreak patterns before the prompts are processed by an LLM-powered agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning all user messages can expose sensitive prompt content if the surrounding integration logs prompts or findings too broadly.

Mitigation: Review agent logging and retention behavior before deployment, and limit stored prompt content to what is necessary for security review.

Risk: Regex-based prompt scanning can miss novel or obfuscated attacks and can also flag benign text that matches attack examples.

Mitigation: Use findings as part of a layered input-safety workflow with human review or additional controls for high-impact actions.

## Reference(s):

- [Firm Prompt Security Pack on ClawHub](https://clawhub.ai/romainsantoli-web/skills/firm-prompt-security-pack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, shell-style tool calls, and Python integration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt-scanning guidance for single-prompt and batch workflows; runtime findings depend on mcp-openclaw-extensions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
