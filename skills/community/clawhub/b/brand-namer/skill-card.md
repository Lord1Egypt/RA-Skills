## Description:

Generate brand names with domain checks and analysis. Use when naming a startup, checking domain availability, or brainstorming product names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, product teams, and developers use this skill to brainstorm brand-name candidates, check basic domain signals, analyze readability and language fit, and manage a shortlist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or untrusted generate count argument could run local commands before the script validates it as a bounded integer.

Mitigation: Review before installing and do not pass untrusted or generated text as the count argument until integer bounds validation is added.

Risk: Domain checks are public network lookups and may disclose candidate names.

Mitigation: Avoid checking confidential pre-launch names unless that disclosure is acceptable.

## Reference(s):

- [Brand Namer skill page](https://clawhub.ai/ckchzh/skills/brand-namer)
- [BytesAgain homepage](https://bytesagain.com)
- [Brand naming tips](artifact/tips.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text, with optional txt, csv, or json shortlist exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local shell scripts, optional DNS lookups, and a configurable local data directory.]

## Skill Version(s):

3.0.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
