## Description: <br>
Browser tool health check and auto-repair. Automatically checks browser status before each use and diagnoses/fixes issues. Use when preparing to use browser automation, a browser snapshot or start times out, CDP connection fails, or browser timeout/disconnection symptoms appear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to check browser tool readiness, diagnose browser timeouts or CDP failures, and apply guided repairs before running browser screenshots or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic repair can forcibly stop local browser processes without enough safeguards. <br>
Mitigation: Use diagnostic mode first, and only allow --fix or taskkill after confirming the PID belongs to the intended OpenClaw browser process. <br>


## Reference(s): <br>
- [Browser Healthcheck release page](https://clawhub.ai/systiger/browser-healthcheck) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline command, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic status checks and optional local repair commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
