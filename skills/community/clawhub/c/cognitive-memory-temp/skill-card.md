## Description: <br>
Cognitive Memory Temp helps agents set up and operate a persistent multi-store memory system with episodic, semantic, procedural, core, and vault stores, plus reflection, decay scoring, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbei2007](https://clawhub.ai/user/linbei2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory, natural-language remember/forget/reflect workflows, knowledge graph records, and auditable memory updates to an agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a highly persistent memory system that may shape future agent behavior and retain sensitive behavior or memory records. <br>
Mitigation: Review the memory templates and resulting IDENTITY.md, SOUL.md, reward logs, reflection archives, and audit records before and after installation. <br>
Risk: Initialization and upgrade scripts modify workspace files and initialize or update git-backed audit history. <br>
Mitigation: Run scripts only in the intended workspace after reviewing them, and avoid running them where unrelated secrets or uncommitted work are present. <br>
Risk: Remote memory search can broaden access to stored memories and session-derived context. <br>
Mitigation: Consider disabling remote memorySearch or limiting its providers and sources unless the deployment requires that capability. <br>


## Reference(s): <br>
- [Architecture](artifact/references/architecture.md) <br>
- [Reflection Process](artifact/references/reflection-process.md) <br>
- [Routing Prompt](artifact/references/routing-prompt.md) <br>
- [ClawHub release page](https://clawhub.ai/linbei2007/cognitive-memory-temp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration snippets, and memory template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates persistent workspace memory files and git-backed audit records when its scripts or procedures are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
