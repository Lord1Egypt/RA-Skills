## Description: <br>
Evaluates skill quality, runs a Pareto-protected self-improvement loop, and tracks score trends across six structural dimensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to score a skill across structural quality dimensions, run bounded self-improvement iterations, and review historical progress data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The self-improvement workflow can modify or restore files in target skill directories. <br>
Mitigation: Run it only against trusted, backed-up, version-controlled skills and review diffs before accepting changes. <br>
Risk: The workflow can run target tests and invoke the local Claude CLI. <br>
Mitigation: Disable or sandbox pytest and Claude execution when evaluating untrusted packages or sensitive skill content. <br>
Risk: The workflow can make git commits as part of accepting generated changes. <br>
Mitigation: Use a clean branch or disposable worktree and inspect any commits before merging or publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/auto-improvement-learner) <br>
- [Publisher Profile](https://clawhub.ai/user/lanyasheng) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON result artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces six-dimension quality scores, self-improvement iteration summaries, memory statistics, and trend data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
