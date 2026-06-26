## Description: <br>
Autonomous skill optimizer inspired by Karpathy's autoresearch that evaluates SKILL.md files with an 8-dimension rubric, runs hill-climbing with git version control, and validates improvements through test prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alchaincyf](https://clawhub.ai/user/alchaincyf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to evaluate and improve Claude Code Skills by combining static structure scoring, test-prompt validation, git-backed changes, and human checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose and apply edits to local skill files and use git operations during optimization. <br>
Mitigation: Run it on an explicit target skill, keep the branch and human checkpoints enabled, and inspect diffs before accepting changes. <br>
Risk: Skill text used during evaluation may be exposed to subagents or the configured model provider. <br>
Mitigation: Avoid placing secrets or sensitive operational details in SKILL.md files before evaluation. <br>


## Reference(s): <br>
- [ClawHub listing for 达尔文.skill](https://clawhub.ai/alchaincyf/darwin-skill) <br>
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch) <br>
- [Claude Code](https://claude.ai/code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus JSON and TSV file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May edit SKILL.md, create test-prompts.json, update .claude/skills/auto-optimize-results.tsv, and propose git commits or reverts for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
