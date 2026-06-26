## Description: <br>
Neuroplastic self-modifying runtime for AI agents. Creates a file-based 'brain' that learns from interactions: reflexes (fast-path responses), habits (learned patterns), weighted pathways (reinforcement), and a cortex (self-review loop). Use when: setting up adaptive agent behavior, creating learning loops, building persistent behavioral memory, or making an agent that improves over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p0lish](https://clawhub.ai/user/p0lish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use brainmd to add persistent behavioral reinforcement to an AI agent through file-based pathway weights, outcome recording, review cycles, and mutation logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic learning loops can reshape future agent behavior without strong boundaries or rollback guidance. <br>
Mitigation: Use it only where an adaptive behavior layer is intentional, inspect the brain directory and mutation logs, disable heartbeat automation for sensitive workflows, and keep a reset or rollback process available. <br>
Risk: The skill writes persistent local state and mutation logs that can influence later decisions. <br>
Mitigation: Review generated pathway files before relying on them and avoid deploying the state directory into production or sensitive contexts without approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/p0lish/brainmd) <br>
- [ClawHub brainmd listing](https://clawhub.ai/skills/brainmd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operating guidance for local files, scripts, pathway state, and mutation logs.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
