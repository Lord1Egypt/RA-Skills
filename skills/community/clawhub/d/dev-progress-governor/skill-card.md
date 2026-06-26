## Description: <br>
Governs software development execution hygiene by checking commit readiness, suggesting commit messages, updating progress logs, summarizing completed work, and tracking blockers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Majmunu](https://clawhub.ai/user/Majmunu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to keep implementation steps commit-ready, generate concise commit messages, append structured progress-log updates, and track blockers without expanding project scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Progress-log entries can include changed files, blockers, task status, commit details, and other project context. <br>
Mitigation: Review generated progress-log entries before committing or sharing them, and avoid recording secrets or private customer data. <br>
Risk: Commit-readiness guidance may be based on incomplete evidence when the user provides only a diff or summary. <br>
Mitigation: Treat readiness as evidence-limited in those cases and verify the changed files, tests, and blockers before committing. <br>


## Reference(s): <br>
- [Commit Guidelines](references/commit-guidelines.md) <br>
- [Progress Log Template](references/progress-log-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Majmunu/dev-progress-governor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with commit-readiness, rationale, changed areas, suggested commit message, progress-log entry, and next-step sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a ready/not-ready decision, blockers, affected files or areas, and a single recommended next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
