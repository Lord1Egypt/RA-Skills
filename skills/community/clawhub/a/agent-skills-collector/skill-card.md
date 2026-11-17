## Description:

Collects AI Skills related to a specified agent business type from SkillHub and exports the results as an Excel inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shmiss](https://clawhub.ai/user/shmiss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to find, classify, and export candidate AI Skills for business agent types such as HR, sales, customer service, data analysis, finance, IT, marketing, legal, and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted remote skill metadata may be written into Excel cells without formula neutralization.

Mitigation: Open generated workbooks with external content and automatic link updates disabled, and review workbook contents before sharing or operational use.

Risk: The skill contacts SkillHub, cn.clawhub-mirror.com, and a third-party translation service.

Mitigation: Use only in environments where these outbound data flows are acceptable, especially when collecting sensitive or internal skill search terms.

Risk: Mutable dependency installs and external CLI behavior can change over time.

Mitigation: Prefer a project-local install with pinned dependency versions and review the installed SkillHub CLI before use in sensitive environments.

## Reference(s):

- [Agent Skills Collector release page](https://clawhub.ai/shmiss/skills/agent-skills-collector)
- [Publisher profile](https://clawhub.ai/user/shmiss)
- [SkillHub skill pages](https://skillhub.tencent.com/skill/{slug})
- [ClawHub mirror API](https://cn.clawhub-mirror.com/api/v1)
- [ClawHub mirror skill pages](https://cn.clawhub-mirror.com/skill/{slug})

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Excel workbook (.xlsx) with terminal status messages and install or URL guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workbook rows include skill name, relevance, category, description, install guidance or URL, tags, stars, downloads, and version.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
