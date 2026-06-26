## Description: <br>
Unified AI Company skill consolidating 16 department skills into one for governance, finance, technology, security, legal, people, marketing, quality, intelligence, information, translation, and platform operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Developers, operators, and AI-company teams use this skill to coordinate cross-department enterprise workflows, generate implementation guidance, perform governance and risk checks, and produce structured operational reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags broad enterprise orchestration, high-impact capability tags, under-scoped automatic writes, auto-update behavior, and broad triggers. <br>
Mitigation: Install only after manual review; constrain triggers to explicit commands, disable or require approval for auto-updates, and require confirmation before file writes or external-system mutations. <br>
Risk: The evidence guidance warns against granting real OAuth tokens, financial authority, deployment authority, or sensitive business data before controls are in place. <br>
Mitigation: Use test credentials and limited workspaces first; keep persistence under the workspace and avoid sensitive data until approvals, audit logging, and permission boundaries are verified. <br>
Risk: Artifact behavior includes silent intelligence-library setup and workspace writes on first collection request. <br>
Mitigation: Require visible user confirmation for setup and persistence, and review generated files before relying on intelligence collection outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/ai-company-unified) <br>
- [Publisher profile](https://clawhub.ai/user/johnsmithfan) <br>
- [README](README.md) <br>
- [Skill manifest](SKILL.md) <br>
- [Method Patterns](references/method-patterns.md) <br>
- [Execution Reference](references/execution.md) <br>
- [Integrations Reference Guide](references/integrations.md) <br>
- [Data Integration Reference](references/data-integration.md) <br>
- [Memory System Technical Specification](references/memory.md) <br>
- [Visualization Reference Guide](references/visualization.md) <br>
- [Security & Compliance](references/departments/security-and-compliance.md) <br>
- [Information Services](references/departments/information.md) <br>
- [Intelligence](references/departments/intelligence.md) <br>
- [WorkBuddy platform](https://www.codebuddy.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured text, sometimes including code blocks, shell commands, configuration snippets, and JSON-like report data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce department-specific operational reports and implementation artifacts; file writes and external-system mutations should require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
