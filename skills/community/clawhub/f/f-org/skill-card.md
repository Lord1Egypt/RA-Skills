## Description: <br>
Automatically organizes newly created, downloaded, copied, or loose workspace files into a user/ directory by file type while leaving OpenClaw native files and structured project directories unchanged. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyh-longying](https://clawhub.ai/user/xyh-longying) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to keep an OpenClaw workspace tidy by routing new documents, scripts, media, archives, downloads, and temporary files into predictable user/ subdirectories. It is intended for loose workspace files, not established project structures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may move loose workspace files, which can disrupt workflows if existing paths are important. <br>
Mitigation: Ask the agent to show planned moves before cleanup and avoid using it in active project directories where path stability matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xyh-longying/f-org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with file paths and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform file moves into user/ subdirectories when the agent has file-system access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
