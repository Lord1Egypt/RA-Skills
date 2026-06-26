## Description: <br>
Project management for AI agents using markdown files. Install and use the cairn CLI to create projects, manage tasks, track status, and coordinate human-AI collaboration through a shared workspace of markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gregoryehill](https://clawhub.ai/user/gregoryehill) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, AI agents, and teams use this skill to install and operate the Cairn CLI for markdown-based project and task management. It helps agents create projects, track task status, record progress notes, and manage deliverable artifacts in a shared workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the cairn-work npm package globally runs package code with global CLI permissions. <br>
Mitigation: Verify that the npm package and publisher are trusted before running npm install -g. <br>
Risk: The onboard workflow creates or updates agent context files in the user's home directory or selected workspace. <br>
Mitigation: Review the target workspace and generated files before relying on them for agent work. <br>
Risk: Execute autonomy can allow deploy, publish, send, or similar side effects when a workflow authorizes them. <br>
Mitigation: Use execute mode only for specific workflows that have been explicitly approved. <br>


## Reference(s): <br>
- [Cairn CLI Command Reference](artifact/COMMANDS.md) <br>
- [Cairn README](artifact/README.md) <br>
- [cairn-work npm package](https://www.npmjs.com/package/cairn-work) <br>
- [Cairn website](https://letcairn.work/) <br>
- [ClawHub release page](https://clawhub.ai/gregoryehill/cairn-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and markdown file conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local markdown project, task, artifact, and agent context files through the Cairn CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
