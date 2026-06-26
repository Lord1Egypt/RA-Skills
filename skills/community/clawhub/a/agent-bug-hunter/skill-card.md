## Description: <br>
Agent Bug Hunter helps agents proactively investigate, reproduce, fix, and verify software bugs using root cause analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nntrivi2001](https://clawhub.ai/user/nntrivi2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to have an agent inspect code, investigate reported or suspected bugs, classify severity, propose fixes, and verify fixes with builds, tests, or reproduction steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad debugging prompts may cause the agent to inspect or change more code than intended. <br>
Mitigation: Invoke it with a clear scope and review proposed shell commands and code changes before accepting them. <br>
Risk: Bug-fix guidance can be wrong if it is not verified against the exact reproduction. <br>
Mitigation: Require reproduction, root cause evidence, and passing tests or builds before treating fixes as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nntrivi2001/agent-bug-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with code changes, shell commands, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or apply code changes and commands when the host agent has tools available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
