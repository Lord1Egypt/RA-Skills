## Description: <br>
Lightweight command monitoring tool that periodically executes local commands/scripts in batches, detects output changes, and triggers alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengyun8](https://clawhub.ai/user/mengyun8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use Cmdnotify to monitor recurring local commands or scripts, detect output or exit-code changes, and trigger alerts for system health, configuration drift, logs, and service checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured commands may repeatedly execute local programs or scripts. <br>
Mitigation: Review every command, use trusted configuration files, set appropriate intervals and timeouts, and avoid running with elevated privileges unless required. <br>
Risk: Notification commands can send alert content or host details to external services. <br>
Mitigation: Review each notify_cmd endpoint and payload, avoid sending secrets or sensitive host details, and use only trusted webhook destinations. <br>
Risk: The packaged artifact describes Go build steps but does not include the referenced Go source files. <br>
Mitigation: Review any external source before building or running the tool. <br>


## Reference(s): <br>
- [Cmdnotify ClawHub release](https://clawhub.ai/mengyun8/cmdnotify) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command-monitoring configuration examples, build and run commands, and notification setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
