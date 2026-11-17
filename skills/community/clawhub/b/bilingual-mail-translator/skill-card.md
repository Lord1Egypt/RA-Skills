## Description:

Build or improve a bilingual email translation and notification workflow that converts raw emails into Chinese-friendly bilingual output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huacius](https://clawhub.ai/user/huacius)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to define or maintain prompt-layer contracts for bilingual email translation, notification formatting, recipient truncation, quoted-history summarization, duplicate suppression, and signature handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw email content can contain confidential or personal information.

Mitigation: Use approved LLM runtimes, avoid unnecessary retention or logging, and redact sensitive mail when possible.

Risk: Prompt or contract changes could produce misleading translations or omit important context from quoted history.

Mitigation: Review prompt changes, update regression tests for contract assertions, and run representative sample mails through the translation entrypoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huacius/skills/bilingual-mail-translator)
- [Mail Translation Contracts](artifact/references/contracts.md)
- [Commands](artifact/references/commands.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples and prompt-contract guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces human-facing guidance for agent behavior; it does not install code or run commands by itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
