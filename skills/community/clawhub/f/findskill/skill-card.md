## Description:

Find Skill helps agents search and discover OpenClaw skills across ClawHub, GitHub, and a Volces mirror with bilingual query support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to locate skills by keyword, tag, author, popularity, or source, then review skill details and suggested install commands before deciding what to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to ClawHub, GitHub, and an undeclared Volces mirror.

Mitigation: Avoid confidential project names, private technologies, credentials, and internal identifiers in search terms.

Risk: Remote results can be displayed with a trusted-looking verified status even when the result source does not provide verification.

Mitigation: Treat verification labels as informational only and inspect the source, publisher, repository, and install command before using a result.

Risk: The skill can display install commands for remote skills.

Mitigation: Review each install command and target package before execution, especially for results from non-ClawHub sources or mirrors.

## Reference(s):

- [Find Skill on ClawHub](https://clawhub.ai/hgta23/skills/findskill)
- [Publisher profile](https://clawhub.ai/user/hgta23)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text with skill listings, skill details, recommendations, source status, and optional install commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include source names, verification status, quality scores, repository or source links, and cached remote search results.]

## Skill Version(s):

1.0.4 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
