## Description: <br>
Brain-inspired memory for AI agents that keeps recent context vivid, lets older context fade unless reinforced, and uses spreading activation on a semantic graph to recall related memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dario-github](https://clawhub.ai/user/dario-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add semantic graph memory, contextually relevant recall, natural memory decay, and learned memory prioritization to AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can delete and recreate a user-configurable local installation directory if an update fails. <br>
Mitigation: Review the installer before running it, avoid setting BIOMORPHIC_INSTALL_DIR to a directory containing unrelated files, and prefer a pinned manual clone when installing in sensitive environments. <br>
Risk: The memory workflow may store user-provided context and send text to an embedding provider. <br>
Mitigation: Confirm where memories are stored, how they can be deleted, and what text is sent to the embedding provider before using the skill with sensitive context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dario-github/biomorphic-memory) <br>
- [Project Homepage](https://github.com/dario-github/biomorphic-memory) <br>
- [Companion Project: nous-safety](https://github.com/dario-github/nous) <br>
- [Companion Project: agent-self-evolution](https://github.com/dario-github/agent-self-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.11 or later and an embedding API.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
