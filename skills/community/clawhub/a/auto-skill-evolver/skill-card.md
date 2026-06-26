## Description: <br>
Auto Skill Evolver helps agents propose, review, and apply improvements to local skill files from execution traces and feedback, with status and approval flows for chat-driven use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YSSHI-FPGA](https://clawhub.ai/user/YSSHI-FPGA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to iteratively improve local agent skills from execution traces and feedback while keeping proposed edits reviewable before application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run user-chosen local training commands and modify skill files after approval. <br>
Mitigation: Use it in a development workspace, review the full diff before applying changes, and require explicit approval before edits are applied. <br>
Risk: Trace and feedback files may contain credentials or sensitive private data. <br>
Mitigation: Avoid placing secrets in traces or feedback, and keep optimization artifacts in restricted local workspaces. <br>
Risk: A broad writable scope could allow proposals to target unintended skill files. <br>
Mitigation: Restrict writable targets with --allowed-skill-roots and keep self-targeting disabled unless performing controlled maintenance. <br>


## Reference(s): <br>
- [Auto Skill Evolver on ClawHub](https://clawhub.ai/YSSHI-FPGA/auto-skill-evolver) <br>
- [YSSHI-FPGA publisher profile](https://clawhub.ai/user/YSSHI-FPGA) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown and JSON with command-line output and proposed file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Proposal artifacts, diffs, status payloads, approval hashes, and update reports may be generated during skill evolution workflows.] <br>

## Skill Version(s): <br>
1.5.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
