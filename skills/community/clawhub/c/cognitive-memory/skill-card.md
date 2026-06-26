## Description: <br>
Cognitive Memory helps agents maintain multi-store long-lived memory with recall, decay, reflection, knowledge graphs, gated multi-agent writes, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Icemilo414](https://clawhub.ai/user/Icemilo414) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize and configure a local cognitive memory workspace for persistent preferences, episodic logs, semantic graphs, procedural memory, reflection cycles, and auditable updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a long-lived local memory system that can store user preferences, agent behavior notes, and reflective self-image content. <br>
Mitigation: Install only when persistent memory is intended, avoid storing secrets, and review the generated memory files regularly. <br>
Risk: The initialization and upgrade scripts can create or modify workspace files and may initialize or commit to git for audit tracking. <br>
Mitigation: Review scripts before running them, start in a clean workspace, and confirm backup and git behavior are acceptable. <br>
Risk: Broad triggers, shared read access, gated write proposals, and token-reward/persona sections can shape future agent behavior. <br>
Mitigation: Keep write approval gates enabled and edit or disable broad triggers, vault sharing, and token-reward/persona sections that do not match the deployment policy. <br>


## Reference(s): <br>
- [Cognitive Memory Skill Page](https://clawhub.ai/Icemilo414/cognitive-memory) <br>
- [Architecture](references/architecture.md) <br>
- [Reflection Process](references/reflection-process.md) <br>
- [Routing Prompt](references/routing-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and memory file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory structures and agent instructions; reflection output is gated by user approval.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
