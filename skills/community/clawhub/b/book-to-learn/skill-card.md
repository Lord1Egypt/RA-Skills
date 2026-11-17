## Description:

Turns books, documentation sites, and other source materials into structured learning cards for local use or optional publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT

## Use Case:

Learners, educators, and developers use this skill to break books, documentation sites, or reference material into learning cards, with optional daily delivery or batch image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad website and image fetching may access unintended resources, including services reachable on private networks.

Mitigation: Use trusted books and documentation sites; avoid website mode on untrusted or attacker-controlled sites, especially on networks with internal services.

Risk: Optional publishing or image hosting may send source material to external services.

Mitigation: Prefer local output; do not enable Feishu or IMA publishing for proprietary or sensitive material without appropriate safeguards and explicit approval.

## Reference(s):

- [ClawHub release](https://clawhub.ai/sedey999/skills/book-to-learn)
- [Configuration schema](references/config-schema.md)
- [Website mode guide](references/site-mode.md)
- [IMA integration](https://ima.qq.com/agent-interface)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local PDF or PNG learning cards and optionally publish through IMA or Feishu.]

## Skill Version(s):

1.6.1 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
