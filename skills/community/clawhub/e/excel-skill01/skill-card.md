## Description: <br>
Create and manage Product Requirements Documents (PRDs) with structured user stories, acceptance criteria, and task prioritization for feature development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao202404](https://clawhub.ai/user/zhao202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and coding agents use this skill to create PRD task lists with user stories, verifiable acceptance criteria, dependency ordering, and completion tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced unattended agent loop can repeatedly change a project without permission prompts. <br>
Mitigation: Run one PRD story at a time, keep permission prompts enabled, and review each diff before committing. <br>
Risk: Generated PRD tasks or acceptance criteria may be incomplete, vague, or ordered in a way that causes implementation errors. <br>
Mitigation: Review story sizing, dependency order, and acceptance criteria before using the PRD to guide implementation. <br>
Risk: Publisher and package metadata are inconsistent across release evidence and artifact metadata. <br>
Mitigation: Verify the ClawHub publisher handle, package identity, and intended version before deployment. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/zhao202404/excel-skill01) <br>
- [Publisher profile](https://clawhub.ai/user/zhao202404) <br>
- [Agent Usage Patterns](references/agent-usage.md) <br>
- [Output Patterns and Templates](references/output-patterns.md) <br>
- [Workflow Patterns for PRD Skills](references/workflows.md) <br>
- [Ralph by snarktank](https://github.com/snarktank/ralph) <br>
- [Claude Code](https://github.com/anthropics/claude-code) <br>
- [Amp Code](https://ampcode.com) <br>
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PRD structures such as prd.json, user story checklists, acceptance criteria, progress notes, and agent prompt templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
