## Description: <br>
Design and audit command-line interfaces for agent usability, including non-interactive operation, progressive help, pipeline support, idempotency, actionable errors, and structured output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g9pedro](https://clawhub.ai/user/g9pedro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design new CLIs or audit existing CLIs for patterns that make them easier for AI agents to invoke, recover from errors, retry safely, and parse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automation-friendly flags such as --yes or --force can make destructive CLI actions easier to run unattended if a command is poorly designed. <br>
Mitigation: Keep safe defaults, require explicit bypass flags for destructive actions, provide --dry-run previews, and review proposed CLI behavior before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/g9pedro/agent-friendly-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external tools or credentials are required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
