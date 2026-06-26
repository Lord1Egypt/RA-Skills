## Description: <br>
Upgrades OpenClaw toward a Claude-Code-style agent architecture with concurrent subagents, self-reflection, vector memory search, and context compression guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw with Claude-Code-style agent workflows, including an N0 loop, parallel subagents, vector memory search, periodic self-reflection, health checks, and context compression. It provides installation-oriented scripts and configuration examples for adapting OpenClaw to longer-running autonomous work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cron jobs and background health checks can keep automation running after setup. <br>
Mitigation: Review each command before installation, enable scheduled jobs only when persistent automation is intended, and keep clear cleanup steps for removing cron entries and generated scripts. <br>
Risk: The subagent executor can run broad shell or skill commands against local files and accounts. <br>
Mitigation: Run it in a sandbox or non-root account, restrict allowed commands and working directories, and avoid using it around important credentials or production data. <br>
Risk: Dependency installation and vector memory indexing can add supply-chain and data exposure risk. <br>
Mitigation: Pin and review dependencies before installation, store vector memory with controlled permissions, and avoid indexing secrets or sensitive operational data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/claude-code-engine) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/smseow001) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash, Python, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language OpenClaw upgrade guidance with scripts for cron-based reflection, vector search, subagent execution, health checks, and context compression] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
