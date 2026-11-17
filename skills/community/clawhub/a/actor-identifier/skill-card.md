## Description: <br>
Generates Git repository collaboration analysis guidance, scripts, CI configuration, custom metric examples, and report templates for team-level workflow review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan repository collaboration analysis across one or more Git repositories, including aggregate metrics, CI report generation, and workflow improvement discussion prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security review is suspicious because the documentation understates steps that can write files, push reports, use credentials, send Slack notifications, or run privileged CI commands. <br>
Mitigation: Review the generated plan before installation or execution, and enable CI, git push, Slack, and token-based steps only when those side effects are intended. <br>
Risk: The skill can generate repository reports from private collaboration data. <br>
Mitigation: Use it only with repositories where automated report generation and sharing are acceptable, and keep reports local unless the team has approved external delivery. <br>
Risk: Custom metric queries or CI snippets can execute commands in the target repository. <br>
Mitigation: Restrict execution to reviewed, read-only git commands and run CI with least-privilege tokens. <br>


## Reference(s): <br>
- [Actor Identifier on ClawHub](https://clawhub.ai/thcjp/skills/actor-identifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, bash snippets, CI YAML, configuration examples, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file-writing, CI, git push, Slack notification, and token-based steps that require explicit user approval before use] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
