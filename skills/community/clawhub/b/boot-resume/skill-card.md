## Description: <br>
Boot Resume detects interrupted OpenClaw sessions after gateway restart or system wake and schedules automatic continuation events without checkpoint logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Belugary](https://clawhub.ai/user/Belugary) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to resume OpenClaw agent sessions that were interrupted by gateway restarts, crashes, or system wake events. It is intended for environments where automatic continuation after interruption is desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent automation that can automatically resume agent work without fresh user approval. <br>
Mitigation: Use it only when automatic resume is explicitly desired, and narrow the agent or session scope or add confirmation for agents that can perform high-risk actions. <br>
Risk: The release evidence advises review before installing and notes missing systemd template files. <br>
Mitigation: Inspect or supply the expected systemd template files before enabling the skill. <br>


## Reference(s): <br>
- [Boot Resume ClawHub Listing](https://clawhub.ai/Belugary/boot-resume) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report which sessions were resumed or that no interrupted sessions were found.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
