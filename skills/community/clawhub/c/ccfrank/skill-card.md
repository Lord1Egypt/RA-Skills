## Description:

查询会议/期刊的 CCF 等级。当用户提到 CCF 等级、论文评级、会议排名、期刊等级，或需要查询某个会议/期刊是 CCF-A/B/C 时使用此技能。支持通过会议简称（如 PLDI、ICSE）、全称、或 DBLP URL 查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[m2kar](https://clawhub.ai/user/m2kar)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research support agents use this skill to look up CCF conference or journal rankings by abbreviation, full venue name, or DBLP path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global npm install can run a package version other than the reviewed ccfrank package.

Mitigation: Install `ccfrank@4.5.5` explicitly or use a lockfile-controlled local install before configuring the skill.

Risk: Installing or running the package with elevated privileges increases the impact of any package-level issue.

Mitigation: Install and run with normal user privileges unless the npm package has been separately reviewed for privileged execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m2kar/skills/ccfrank)
- [Publisher profile](https://clawhub.ai/user/m2kar)
- [Project homepage](https://github.com/m2kar/CCFrank4dblp)
- [CCF official directory](https://www.ccf.org.cn/Academic_Evaluation/By_category/)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Text]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill's lookup tool returns matched status, rank, canonical venue name, venue type, match method, and normalized source key.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
