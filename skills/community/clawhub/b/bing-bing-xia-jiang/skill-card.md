## Description:

蜂兵虾将 is a multi-agent workflow skill for monitoring cross-industry hotspots, drafting content strategies, analyzing trends and user state, and recording reusable workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT

## Use Case:

External creators, operators, and developers use this skill to coordinate multi-agent workflows that collect timely industry information, turn it into content plans, analyze trend or personal-state signals, and preserve reusable workflow memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores interaction history, preferences, goals, workflow records, and reports in local JSON and Markdown files.

Mitigation: Keep memory directories private and avoid storing secrets, regulated personal data, or other sensitive information in the skill memory.

Risk: Local memory reset or cleanup behavior can remove useful history.

Mitigation: Back up memory directories before using documented reset or cleanup commands.

Risk: Generated hotspot analysis, trend forecasts, content plans, and recommendations may be incomplete or misleading.

Mitigation: Review source evidence and generated reports before using them for business, publishing, or operational decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/e2e5g/skills/bing-bing-xia-jiang)
- [README](README.md)
- [Complete Workflow Design](references/workflow-design.md)
- [Module Data Flow](references/data-flow.md)
- [AI Collaboration Operating System Manual](docs/AI协作操作系统_完整使用说明书.md)
- [Complete User Manual](docs/完整使用手册.md)
- [Centralized Deployment Guide](docs/集中部署指南.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and guidance with JSON-like structures, TypeScript or JavaScript examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent prompts, reports, content plans, workflow templates, and local-memory records; no token cap is stated.]

## Skill Version(s):

1.4.1 (source: server release evidence; artifact package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
