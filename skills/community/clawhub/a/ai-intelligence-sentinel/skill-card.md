## Description:

AI前沿哨兵 tracks public AI, open-source, research, and big data industry signals and turns them into concise intelligence reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaopengs](https://clawhub.ai/user/xiaopengs)

### License/Terms of Use:

MIT-0

## Use Case:

Executives, product managers, developers, and data teams use this skill to gather public AI and data-platform signals, analyze their significance, and generate decision-ready Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Under-scoped network access can reach many public sources, including user-configured RSS feeds and web pages.

Mitigation: Review configured sources before use, narrow access to trusted public URLs, and keep the documented timeout and rate-limit controls enabled.

Risk: Twitter or custom API credentials may be entered through local configuration paths or the WebUI.

Mitigation: Avoid entering sensitive tokens in the WebUI, prefer environment variables or ignored secrets files, and rotate any token used during testing.

Risk: Broad USER.md or MEMORY.md loading can expose private context to generated reports or downstream analysis.

Mitigation: Use minimal purpose-specific configuration files and remove private, credential-like, or unrelated content before running the skill.

Risk: Mutable installer, dependency, or external-skill execution paths can change behavior between runs.

Mitigation: Pin ClawHub, dependency, and external skill versions; review external skill output before mixing it into reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaopengs/skills/ai-intelligence-sentinel)
- [README](README.md)
- [API setup guide](references/api_setup.md)
- [Source configuration guide](references/sources_guide.md)
- [Big Data Insight requirements](docs/BIGDATA_INSIGHT_REQUIREMENT.md)
- [Security configuration](SECURITY_CONFIG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional configuration snippets, code snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs summarize public sources and may save generated report files under configured report directories.]

## Skill Version(s):

2.1.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
