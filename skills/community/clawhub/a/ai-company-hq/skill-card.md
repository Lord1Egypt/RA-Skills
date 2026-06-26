## Description: <br>
HQ skill: Cross-agent coordination, conflict resolution, knowledge base management, audit logging, strategic scheduling, task orchestration, IMA sync hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this agent skill as a central coordination hub for AI-company workflows, including cross-agent routing, conflict resolution, knowledge-base management, audit logging, scheduling, and task orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad cross-agent, state, logging, and knowledge-capture authority may exceed the user's intended scope. <br>
Mitigation: Restrict allowed file paths, API destinations, MCP recipients, and subagent use before installing or invoking the skill. <br>
Risk: Broadcasts, shared-state changes, and knowledge-base publication can affect multiple agents or workflows. <br>
Mitigation: Require explicit confirmation for broadcasts, shared-state changes, and KB publication. <br>
Risk: Audit logging and knowledge capture can retain sensitive or unnecessary information. <br>
Mitigation: Define privacy, redaction, retention, and deletion rules before use. <br>


## Reference(s): <br>
- [AI Company HQ ClawHub release](https://clawhub.ai/johnsmithfan/ai-company-hq) <br>
- [AI Company HQ homepage](https://clawhub.com/skills/ai-company-hq) <br>
- [Method Patterns & Detailed Specifications](references/method-patterns.md) <br>
- [Department Integration Process](references/department-integration-process.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with optional code, shell command, configuration, and report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce implementation plans, robustness findings, test cases, documentation, workflow results, audit-trail summaries, and quality metrics.] <br>

## Skill Version(s): <br>
3.0.1-en2 (source: ClawHub release metadata; artifact frontmatter lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
