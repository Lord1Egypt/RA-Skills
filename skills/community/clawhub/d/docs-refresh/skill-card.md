## Description: <br>
Refresh authoritative docs through a routed progressive-disclosure workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzg-lab](https://clawhub.ai/user/jzg-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to close out repository work by deciding whether durable documentation needs updates, routing to the right documentation maturity mode, and updating the smallest authoritative docs that own changed facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read repository state, diffs, untracked files, and generated artifacts, which can expose sensitive unreleased work to the active agent session. <br>
Mitigation: Install and run it only in repositories where the agent is allowed to inspect current workspace changes; review the bundled shell collector before use in sensitive repositories. <br>
Risk: Documentation edits can introduce incorrect or misleading durable guidance if the agent routes to the wrong authority or misreads the behavior change. <br>
Mitigation: Review proposed documentation changes against code, tests, schema, and generated artifacts before accepting them. <br>


## Reference(s): <br>
- [Docs Refresh Skill Page](https://clawhub.ai/jzg-lab/docs-refresh) <br>
- [Docs Refresh Skill Definition](artifact/SKILL.md) <br>
- [Bootstrap Mode](artifact/modes/bootstrap.md) <br>
- [Minimal Mode](artifact/modes/minimal.md) <br>
- [Structured Mode](artifact/modes/structured.md) <br>
- [Repair Mode](artifact/modes/repair.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown documentation edits, concise Markdown explanations, and plain-text collector output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run a local git-focused shell collector when available; does not stage or commit changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
