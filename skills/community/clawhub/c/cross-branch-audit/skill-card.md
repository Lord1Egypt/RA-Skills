## Description: <br>
Audits planned cross-branch code migrations by analyzing git history, dependency links, conflict risk, and migration readiness before cherry-picking or porting work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xianjingnb](https://clawhub.ai/user/xianjingnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to assess whether a module or feature can be migrated between branches, identify dependent commits and files, and plan safer cherry-pick or manual merge steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes git commands and migration actions that can affect branch history or working tree state if applied without review. <br>
Mitigation: Review the proposed command list and run audits from a clean working tree or disposable branch before applying cherry-picks or manual merge changes. <br>
Risk: The audit may miss scattered feature work when keyword, author, or time-range inputs are incomplete. <br>
Mitigation: Have the user confirm the discovered commit list and supply known issue IDs, commit SHAs, module paths, or watch paths before relying on the migration plan. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xianjingnb/cross-branch-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, audit tables, migration plans, and generated HTML report code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an interactive HTML audit report under docs/ and printable migration checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
