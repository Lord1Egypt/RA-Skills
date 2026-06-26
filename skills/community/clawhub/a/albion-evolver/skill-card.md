## Description: <br>
Albion Evolver helps AI agents on constrained hardware analyze runtime logs and dream cycles, propose validated minimal code improvements, apply them with git versioning, and roll back regressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Albion Evolver to support self-improvement workflows for agents running in constrained environments by generating minimal code-change proposals, validation steps, commits, and rollback actions from runtime evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can actively modify repositories, create commits, roll back changes, and run self-improvement cycles without tight scope if installed with broad permissions. <br>
Mitigation: Use it first in a disposable or well-backed-up workspace, review diffs before accepting changes, and require explicit approval before writes, commits, rollbacks, network calls, or self-modifying runs. <br>
Risk: Generated code changes may introduce regressions or incorrect behavior despite automated checks. <br>
Mitigation: Keep the artifact's syntax checks, sandbox tests, peer review gates, score comparison, and rollback process enabled, and perform human review before relying on the changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with FIND/REPLACE snippets, validation notes, git commands, and JSON log updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify workspace files and create git commits when allowed; changes are intended to be limited to three lines per cycle.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
