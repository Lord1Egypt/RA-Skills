## Description:

AI.MD converts human-written CLAUDE.md or other LLM instruction files into AI-native structured-label Markdown intended to reduce token load and improve rule-following.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sstklen](https://clawhub.ai/user/sstklen)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use AI.MD to preview instruction-token overhead and rewrite CLAUDE.md-style guidance into structured labels, gates, rules, references, and examples for agent consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLAUDE.md and related instruction files can contain secrets, private URLs, tokens, or connection strings.

Mitigation: Remove sensitive values before using the skill and review the rewritten output before replacing any live configuration.

Risk: Multi-model validation can expose instruction content to external model providers without a clear separate opt-in.

Mitigation: Run validation only after explicitly approving the providers and after redacting content that should not leave the local environment.

Risk: A mutable main-branch curl install command can change over time.

Mitigation: Install from a pinned release or reviewed commit and verify checksums before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sstklen/skills/ai-md)
- [AI.MD Documentation Index](artifact/docs/index.md)
- [Before Conversion Example](artifact/examples/before.md)
- [After Conversion Example](artifact/examples/after.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with structured labels and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include before/after measurements, backup and restore commands, and model-validation score summaries.]

## Skill Version(s):

4.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
