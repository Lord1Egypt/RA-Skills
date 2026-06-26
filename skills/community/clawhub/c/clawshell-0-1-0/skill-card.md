## Description: <br>
Human-in-the-loop security layer. Intercepts high-risk commands and requires push notification approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lucky-2968](https://clawhub.ai/user/Lucky-2968) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use ClawShell to route shell command execution through a human approval workflow for commands classified as risky. The release evidence reports that the package does not include an implementation sufficient to verify or enforce the claimed behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Clawshell 0.1.0 on ClawHub](https://clawhub.ai/Lucky-2968/clawshell-0-1-0) <br>
- [Pushover application setup](https://pushover.net/apps/build) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration, Guidance] <br>
**Output Format:** [JSON command results, JSONL audit logs, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and notification credentials; security evidence says not to rely on it as a shell security layer until the implementation and dependency list are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
