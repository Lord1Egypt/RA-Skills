## Description: <br>
Manages agent memory backup, restoration, rollback, and cloning using Fulcra's versioned file storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve, restore, roll back, or clone an agent's memory and identity state through Fulcra's versioned file storage. It is intended for agents that need durable progress reports, backup archives, and controlled recovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory archives and progress reports can persist sensitive personal data, credentials, or private internal reasoning. <br>
Mitigation: Review backup contents before upload, minimize progress report detail, and obtain explicit user consent before storing sensitive context. <br>
Risk: Restore and clone operations can overwrite current memory and identity files. <br>
Mitigation: Create a fresh backup before restore or clone, inspect the downloaded archive, warn the user about replacement, and proceed only after explicit confirmation. <br>
Risk: Multiple active agents using the same Fulcra memory path can interleave or confuse backup history. <br>
Mitigation: Confirm the intended agent namespace and check that no other active agent is backing up to the same path before continuing. <br>


## Reference(s): <br>
- [Fulcra Memory on ClawHub](https://clawhub.ai/fulcra/fulcra-memory) <br>
- [Fulcra Memory CLI Reference](references/fulcra-memory-cli.md) <br>
- [Fulcra CLI Documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-onboarding/references/fulcra-cli.md) <br>
- [Open Knowledge Format Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and Fulcra file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create progress reports, OKF index and log files, compressed memory archives, and Fulcra file storage updates.] <br>

## Skill Version(s): <br>
0.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
