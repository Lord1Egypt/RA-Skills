## Description: <br>
Create and manage Product Requirements Documents (PRDs) with user stories, acceptance criteria, and prioritized task tracking for feature implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao202404](https://clawhub.ai/user/zhao202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and agent operators use this skill to draft PRDs, break features into independently verifiable user stories, and track implementation progress through structured acceptance criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an unattended coding-agent loop with permission checks disabled. <br>
Mitigation: Use the skill for PRD drafting and task planning by default; if using agents to implement stories, run them in a branch or worktree, keep permission prompts enabled, and review changes between stories. <br>
Risk: Progress logs may capture sensitive implementation details or secrets if agents write unchecked notes. <br>
Mitigation: Review `progress.txt` entries before sharing or committing them, and avoid storing secrets or credentials in progress notes. <br>
Risk: The security guidance reports that embedded package metadata does not match the registry metadata. <br>
Mitigation: Verify the package identity, publisher handle, slug, and release version against the server-resolved ClawHub metadata before deployment. <br>


## Reference(s): <br>
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
**Other Properties Related to Output:** [Produces PRD structures, acceptance criteria, progress-tracking templates, and agent execution guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
