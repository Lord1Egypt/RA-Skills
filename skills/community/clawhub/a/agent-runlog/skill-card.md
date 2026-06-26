## Description: <br>
Wrap shell commands with the agent-runlog CLI to capture concise, redacted run logs for debugging, CI reproduction, long-running agent commands, repeated failures, test/lint/build evidence, and handoffs where stdout/stderr plus git state should be preserved without flooding chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run tests, builds, lint checks, and other shell commands through a logging wrapper so command output, summaries, and local repository state can be preserved for debugging, CI reproduction, and handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run an external npm CLI around user-chosen commands. <br>
Mitigation: Review commands before execution and do not wrap destructive commands without explicit user approval. <br>
Risk: Local run logs may contain command output or repository state. <br>
Mitigation: Keep redaction enabled, avoid --no-redact unless raw logs are explicitly required, and do not share .agent-runs/ when logs may include private data. <br>
Risk: Captured logs can become noisy or reveal more operational detail than intended. <br>
Mitigation: Summarize relevant report sections instead of posting full logs when handing work to another person or agent. <br>


## Reference(s): <br>
- [ClawHub skill page for agent-runlog](https://clawhub.ai/builtbyecho/agent-runlog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline bash command examples; the wrapped CLI can create Markdown reports and JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Run logs are written locally under .agent-runs/ and are redacted by default.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
