## Description: <br>
Schedule recurring AI agent prompts using fixed intervals or cron expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femto](https://clawhub.ai/user/femto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to schedule recurring agent prompts for periodic checks, reports, monitoring, and other repeated workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled prompts can continue running if users do not set limits. <br>
Mitigation: Use --max, --timeout, or --until for nontrivial jobs, and stop the loop manually when it is no longer needed. <br>
Risk: Unattended recurring prompts may repeat actions that delete data, deploy changes, spend money, or post publicly. <br>
Mitigation: Only schedule prompts that are safe to run repeatedly and require human review for consequential actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/femto/acp-loop) <br>
- [npm package](https://www.npmjs.com/package/acp-loop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
