## Description: <br>
Gives an OpenClaw agent persistent memory across sessions through a local markdown file that stores user context, projects, decisions, preferences, lessons, and blockers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[contrario](https://clawhub.ai/user/contrario) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use MEMORIA to let an agent load, maintain, and summarize long-lived local context about the user and their work across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent long-lived ability to save and resurface personal and work details with limited confirmation controls. <br>
Mitigation: Review the local memory file and backups regularly, prefer explicit memory requests, and remove entries that should not persist. <br>
Risk: Persistent memory can capture secrets, sensitive infrastructure details, private URLs, or other data that should not be stored. <br>
Mitigation: Do not store credentials, tokens, IP addresses, private URLs, access codes, or sensitive infrastructure details in memory. <br>
Risk: Local memory files or backups may be accidentally committed or synchronized to cloud storage. <br>
Mitigation: Keep memory files in a restricted local directory, use owner-only file permissions, and add memory paths to git and cloud-sync ignore lists. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/contrario/agent-memoria) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides the agent to read, create, back up, and patch a local markdown memory file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
