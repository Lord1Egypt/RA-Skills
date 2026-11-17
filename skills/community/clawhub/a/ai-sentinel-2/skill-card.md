## Description:

AI前沿哨兵 automatically collects, analyzes, scores, and reports AI news, papers, open-source projects, discussions, and social updates from multiple configured sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaopengs](https://clawhub.ai/user/xiaopengs)

### License/Terms of Use:

MIT-0

## Use Case:

External AI researchers, developers, product managers, investors, and content creators use this skill to monitor AI-field developments, rank collected items by relevance and quality, and generate structured Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WebUI credential handling may expose Twitter/X bearer tokens.

Mitigation: Avoid entering Twitter/X bearer tokens in the WebUI until token storage and DOM injection issues are fixed; prefer environment variables or a backend secret store.

Risk: Custom feed fetching can retrieve content from untrusted or unexpected URLs.

Mitigation: Run the skill in a limited workspace with pinned dependencies and use only trusted feed URLs.

Risk: Scheduled collection can create unintended background network activity.

Mitigation: Enable cron or scheduled runs only when recurring collection is intentional and review the configured schedule first.

## Reference(s):

- [API Configuration Guide](artifact/references/api_setup.md)
- [Source Addition Guide](artifact/references/sources_guide.md)
- [ClawHub Release Page](https://clawhub.ai/xiaopengs/skills/ai-sentinel-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, shell commands, and YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates morning, evening, and Xiaohongshu-style reports from configured information sources.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
