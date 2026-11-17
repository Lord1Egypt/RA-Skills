## Description:

Prompt-injection and data-exfiltration screening for untrusted text before summarizing, replying, or writing to memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deegerwalker](https://clawhub.ai/user/deegerwalker)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to screen untrusted web, email, or social content for prompt-injection, data-exfiltration, and tool-abuse patterns before an agent summarizes, replies, or writes to memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lightly sanitized untrusted text may still be written into persistent agent memory.

Mitigation: Require explicit user approval for memory writes and quarantine medium-or-higher severity content or text with lint findings.

Risk: The safe memory append script depends on an unpinned local aegis-shield module outside the released package.

Mitigation: Use only in environments where the external library path is trusted, locked down, and verified before installation.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON, markdown]

**Output Format:** [Markdown instructions with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled safe memory append workflow may write sourced memory entries or quarantine records when run in a configured OpenClaw environment.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
