## Description: <br>
Review agentic software-development plans and release readiness for Codex, GitHub, and ClawHub work. Use when a user asks for scoped delivery planning, implementation review, public-surface checks, or release evidence review without running remote-changing commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release reviewers use this skill to review agentic development plans, diffs, repository notes, or release checklists for scope, public-surface risks, verification evidence, and readiness before shipping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat review guidance as authorization to publish, modify repositories, or take account actions. <br>
Mitigation: Use the skill as an advisory review aid only; require separate human-approved release actions and normal verification gates. <br>
Risk: Review prompts may accidentally include secrets, credentials, private paths, or internal notes. <br>
Mitigation: Avoid pasting secrets or credentials into prompts and keep public-surface review focused on wording, scope, tests, and release evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/agentic-codex-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sections with a readiness verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Scope, Findings, Public surface, Verification, and one of ready, ready_with_notes, blocked, or do_not_ship.] <br>

## Skill Version(s): <br>
0.3.6 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
