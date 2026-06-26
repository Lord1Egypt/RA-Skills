## Description: <br>
Use when the user wants to run a prepared AWS FIS experiment where the CloudFormation stack has already been deployed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panlm](https://clawhub.ai/user/panlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud reliability engineers use this skill to validate an existing AWS FIS experiment setup, run the experiment after explicit confirmation, monitor affected services, collect logs, and produce a results report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS FIS experiments can affect live cloud resources. <br>
Mitigation: Use only for approved chaos-engineering work, verify account, region, target resources, stop conditions, and maintenance window, and require explicit confirmation before starting. <br>
Risk: Default Kubernetes and application log collection may capture secrets, customer data, or regulated information. <br>
Mitigation: Review the app-service-log-analysis behavior before use and avoid default log collection where sensitive data may appear. <br>
Risk: Cleanup commands can remove experiment-related cloud resources. <br>
Mitigation: Run cleanup only after a separate explicit review using least-privilege AWS credentials. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [CLI Commands Reference](references/cli-commands.md) <br>
- [Experiment Results Report Template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and a local markdown results report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's conversation language and writes the final experiment report into the experiment directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
