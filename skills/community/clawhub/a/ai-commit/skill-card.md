## Description: <br>
Analyze staged changes and generate semantic commit messages automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afine907](https://clawhub.ai/user/afine907) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect staged Git changes, draft Conventional Commit messages, and optionally create or amend commits after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads staged diffs, which may contain secrets or sensitive implementation details. <br>
Mitigation: Review staged files for sensitive data before invoking the skill, and inspect the proposed message before committing. <br>
Risk: Commit and amend commands change repository history when executed. <br>
Mitigation: Use --dry-run to preview output and use --amend only when intentionally modifying the previous commit, especially on shared branches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afine907/ai-commit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with commit message text and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose git commit or amend commands; dry-run mode previews the message without committing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
