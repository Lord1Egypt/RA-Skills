## Description: <br>
Long-term memory system for OpenClaw agents that manages entities, context summaries, and an Obsidian-backed knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexburrstudio](https://clawhub.ai/user/alexburrstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate a persistent memory agent that organizes people, companies, topics, session context, and knowledge-base summaries in a local Obsidian vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent local memory agent and scheduled cron processing by default. <br>
Mitigation: Review setup.sh before execution and run ./setup.sh --skip-cron unless scheduled processing is explicitly desired. <br>
Risk: The skill stores long-term local memory and session data with weak consent and retention boundaries. <br>
Mitigation: Use VAULT_DEST to choose an appropriate vault location, define retention expectations before use, and avoid storing sensitive data without user consent. <br>
Risk: Installation may write to an existing Obsidian vault or memory workspace. <br>
Mitigation: Back up existing vault and memory files before installation or before allowing the agent to write session summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexburrstudio/ab-agents-memory) <br>
- [Publisher profile](https://clawhub.ai/user/alexburrstudio) <br>
- [Homepage from ClawHub metadata](https://github.com/alexburrstudio/ab-agents-memory) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, local vault files, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local-file oriented and may update an Obsidian vault, OpenClaw agent workspace, and scheduled processing configuration.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter lists 1.0.1 and package/config list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
