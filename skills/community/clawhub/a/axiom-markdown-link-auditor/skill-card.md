## Description:

Extracts links from Markdown content and can optionally run HTTP HEAD checks to report unreachable external links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to extract Markdown links, review link counts and line locations, and optionally check external HTTP(S) targets before publishing documentation or running CI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact claims internal link validation, orphan-page reporting, and directory auditing capabilities that are not supported by the implementation.

Mitigation: Use the skill only for simple Markdown link extraction and optional external status checks until those capabilities are implemented and tested.

Risk: Optional remote checks issue HTTP HEAD requests for links found in Markdown, which can contact untrusted or sensitive network destinations.

Mitigation: Run remote checks only on trusted documents and networks where outbound requests to discovered URLs are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-markdown-link-auditor)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON audit report with link counts, link types, URLs, line numbers, and optional remote status results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses deterministic local parsing; optional remote checks issue HTTP HEAD requests with a timeout.]

## Skill Version(s):

0.1.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
