## Description:

Manages IT hardware and software assets across their lifecycle, including registration, inventory, software license reminders, and cost analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

IT teams, asset managers, and operations staff use this skill to set up or reason about an asset-management system for hardware inventory, software license tracking, device lifecycle status, and asset cost reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill asks users to run mutable, unaudited remote code and dependencies from GitHub.

Mitigation: Review the referenced repository, pin a commit, lock dependency versions with hashes, and run in an isolated environment without sensitive credentials before execution.

Risk: The artifact describes an application that may store or process operational hardware, software license, inventory, and cost records.

Mitigation: Use least-privilege database credentials and avoid loading sensitive production asset data until the application and dependencies have been audited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-intelligent-asset-management)
- [Repository referenced by installation instructions](https://github.com/openclaw-skills/ai-intelligent-asset-management)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation steps for a Python, FastAPI, and PostgreSQL application plus guidance for asset registration, inventory, lifecycle tracking, license reminders, and reporting.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
