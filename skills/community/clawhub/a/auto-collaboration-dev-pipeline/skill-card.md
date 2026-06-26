## Description: <br>
Fully automated collaborative code development pipeline for complex code development tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate complex coding work to a staged pipeline covering requirements, architecture, implementation, testing, review, documentation, and delivery. It is intended for larger or quality-sensitive tasks where automated handoffs and final artifact delivery are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run hands-off and create or modify multiple project files. <br>
Mitigation: Use it in a clean or dedicated workspace, avoid placing secrets in prompts or source files, and request explicit checkpoints or overwrite confirmation when automatic execution is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/auto-collaboration-dev-pipeline) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Requirements analyst role prompt](artifact/references/requirements-analyst.md) <br>
- [Architect role prompt](artifact/references/architect.md) <br>
- [Backend developer role prompt](artifact/references/backend-developer.md) <br>
- [Frontend developer role prompt](artifact/references/frontend-developer.md) <br>
- [QA engineer role prompt](artifact/references/qa-engineer.md) <br>
- [Code reviewer role prompt](artifact/references/code-reviewer.md) <br>
- [Documentation engineer role prompt](artifact/references/documentation-engineer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with generated project files, code blocks, reports, and delivery summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create multiple files under a project workspace and pass context between sub-agent roles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
