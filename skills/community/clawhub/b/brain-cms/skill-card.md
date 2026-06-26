## Description: <br>
Continuum Memory System for OpenClaw agents that replaces flat memory loading with a brain-inspired architecture using semantic schemas, a topic router, a LanceDB vector store, and NREM/REM consolidation scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrey401](https://clawhub.ai/user/harrey401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate a persistent local memory layer that routes topics to semantic schemas, supports vector search over memory files, and runs consolidation scripts to reduce routine context loading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes local agent instructions and memory files, which can affect future agent behavior. <br>
Mitigation: Back up AGENTS.md and the memory folder before installation, then review all generated memory instructions before relying on them. <br>
Risk: Daily logs, semantic schemas, and anchors may store private or sensitive user information. <br>
Mitigation: Avoid storing secrets or sensitive data in memory files, and periodically audit the memory directory before indexing or consolidation. <br>
Risk: NREM and REM scripts mutate memory files and can consolidate incorrect or unwanted information. <br>
Mitigation: Run sleep-cycle scripts manually until trusted, inspect their changes, and revert or edit memory updates before using them in later sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrey401/brain-cms) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local memory/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs local Python scripts, memory index files, and vector-store configuration for an OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
