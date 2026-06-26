## Description: <br>
AI Agent team skill that provides persona-driven specialist agents and an orchestrator for engineering, marketing, project management, testing, support, product, design, and specialized workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyzx](https://clawhub.ai/user/gyzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users can use this skill to request specialist agent guidance, generated implementation artifacts, project plans, marketing strategy, QA review, and orchestrated multi-agent task breakdowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may overstate the number or completeness of included agents. <br>
Mitigation: Treat the package as a prompt and persona bundle until the installed files are reviewed against the claimed agent inventory. <br>
Risk: Orchestrated workflows may suggest file changes, deployment steps, public posts, or business decisions without enough built-in controls. <br>
Mitigation: Require explicit human approval before applying changes, deploying outputs, publishing content, or relying on business recommendations. <br>
Risk: The artifact includes placeholder manual-install source references. <br>
Mitigation: Install from the ClawHub release page or another verified source rather than placeholder repository URLs. <br>
Risk: Outputs may be saved locally or contain sensitive task context. <br>
Mitigation: Do not provide secrets, regulated data, or confidential business data unless local retention and downstream handling are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gyzx/agency-agents-1-0-2) <br>
- [Quickstart guide](docs/QUICKSTART.md) <br>
- [README](README.md) <br>
- [Package metadata](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, task plans, implementation snippets, reports, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by selected agent or orchestrated workflow and may include project status, deliverable lists, QA findings, and follow-up recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
