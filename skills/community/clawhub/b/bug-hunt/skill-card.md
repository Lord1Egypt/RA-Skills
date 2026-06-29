## Description: <br>
Use when asked to find bugs, hunt for correctness issues, sweep a codebase for defects, or verify a repo behaves as intended. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to perform read-only correctness sweeps over codebases, verify potential defects, and produce a structured markdown bug-hunt report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may inspect broad areas of a repository during a bug hunt. <br>
Mitigation: Install and run only where broad read-only code inspection is appropriate. <br>
Risk: Bug reports can include incorrect or unverified findings if candidate issues are not checked skeptically. <br>
Mitigation: Require the skill's mandatory verification pass and mark any unverifiable finding as unverified or downgrade it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/solomonneas/bug-hunt) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with findings, scorecard, backlog, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only; may suggest safe test runs or reproduction sketches but does not ask the agent to modify files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
