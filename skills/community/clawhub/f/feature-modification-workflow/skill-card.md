## Description: <br>
Structured workflow to analyze, plan, and execute feature modifications by scenario complexity, ensuring controlled, incremental, and risk-aware changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liancheng-zcy](https://clawhub.ai/user/liancheng-zcy) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and coding agents use this skill to classify feature-change requests, choose an appropriate workflow, analyze existing code, plan complex changes, and apply modifications incrementally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate for broad code-modification requests and may influence agent behavior across a repository. <br>
Mitigation: Install it only where agent-assisted code modification is desired, narrow activation if needed, and review diffs before committing. <br>
Risk: Feature-change proposals or code edits can introduce incorrect guidance or unintended behavior. <br>
Mitigation: Use the skill's scenario analysis and confirmation steps for complex changes, then validate changes with tests or review before release. <br>


## Reference(s): <br>
- [Feature Modification Workflow on ClawHub](https://clawhub.ai/liancheng-zcy/feature-modification-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with code edits and shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project analysis, implementation plans, confirmation questions, progress updates, and completed code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
