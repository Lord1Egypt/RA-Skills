## Description:

Configure and benchmark agent tools and integration patterns. Use when setting up agent workflows, comparing tools, or evaluating agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure, log, benchmark, compare, evaluate, and report on agent tools and integration patterns across local workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user-entered agent workflow notes in local plaintext logs and export files.

Mitigation: Avoid entering API keys, tokens, passwords, confidential prompts, regulated data, or security incident details; treat the data directory and exports as sensitive.

Risk: CSV exports can contain unescaped user-provided values that may be unsafe to open directly in spreadsheet software.

Mitigation: Review or sanitize CSV values before opening exports in spreadsheet tools, especially values that begin with formula characters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/agent-toolkit)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Plain text and Markdown-style terminal output; optional JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local plaintext logs and export files under ~/.local/share/agent-toolkit/.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter reports 2.0.1 and script output reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
