## Description:

Scans user-supplied text and files for prompt injection, hidden characters, encoded payloads, and AI configuration backdoors, then returns a verdict, redacted evidence, and handling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a9320](https://clawhub.ai/user/a9320)

### License/Terms of Use:

MIT

## Use Case:

Developers and users use the skill to check untrusted messages, documents, scripts, and AI configuration files before acting on them. It provides scan findings for human review and does not execute scanned content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags concerns about report redaction when scanned content may be sensitive.

Mitigation: Avoid scanning sensitive material until the redaction behavior is reviewed, and inspect reports before sharing them.

Risk: The security assessment reports incomplete coverage because a reference was missing and some static checks were degraded.

Mitigation: Review scan coverage and supplement the result with a manual security review when completeness matters.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/a9320/skills/ai-content-guard)
- [PITAX rule reference](references/rules.md)
- [Privacy statement](references/privacy.md)
- [Security notes](references/security-notes.md)
- [Arcanum Prompt Injection Taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [JSON scan results with optional Markdown and JSONL reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Four-way verdicts with redacted findings and handling guidance; read-only scanning.]

## Skill Version(s):

1.3.3 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
