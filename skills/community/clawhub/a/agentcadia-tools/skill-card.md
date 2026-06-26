## Description: <br>
Upload or download Agentcadia agent workspaces with metadata writeback and detailed reporting using explicit upload and download commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ideaforceai-sys](https://clawhub.ai/user/ideaforceai-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to move Agentcadia agent drafts between a local OpenClaw-style workspace and Agentcadia while preserving required metadata and delivery reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles bearer tokens and workspace files. <br>
Mitigation: Install only when the Agentcadia origin is trusted, use HTTPS origins, and avoid running uploads from workspaces that contain secrets or private notes. <br>
Risk: Downloaded packages may place files into a local workspace and destination handling requires review. <br>
Mitigation: Download only from trusted origins and review reported placed files and conflicts before approving overwrites or using the downloaded workspace. <br>


## Reference(s): <br>
- [OpenClaw Runtime Integration](references/openclaw-runtime.md) <br>
- [Agentcadia](https://agentcadia.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/ideaforceai-sys/agentcadia-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or place local workspace files, package skill directories, call Agentcadia APIs, and report upload or download results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
