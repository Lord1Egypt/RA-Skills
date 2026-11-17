## Description:

Genai Toolkit helps agents use a local Bash CLI to log, view, search, and export generative AI workflow notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to track AI model configurations, benchmarks, prompts, evaluations, costs, usage, fine-tuning runs, and optimization notes in local logs. It is best treated as a plaintext logging utility rather than a database or MCP bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the manifest advertises a database/MCP bridge, while the artifact behaves as a local plaintext logging utility.

Mitigation: Review the skill before installation and rely on the local logging behavior shown by the artifact; do not assume database or MCP integration without separate verification.

Risk: Logged configurations, prompts, schemas, evaluations, exports, or cost records may contain sensitive information because data is stored in plaintext local files.

Mitigation: Do not record API keys, tokens, passwords, private keys, confidential datasets, private schemas, or production prompts; review exported JSON, CSV, or text files before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/genai-toolkit)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact can write local log and export files under ~/.local/share/genai-toolkit/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
