## Description: <br>
Integrates the Playfilo shared-memory DAG into the pi-mono coding agent, adding DAG persistence, time-travel tools, and cross-session memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujilabs](https://clawhub.ai/user/wujilabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers integrating Playfilo with pi-mono use this skill to apply patch guidance and bundled TypeScript for DAG-backed session persistence, temporal tools, cross-session memory, and system prompt injection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory and agent state are mirrored into ~/.playfilo/playfilo.db, which can retain sensitive prompts or session data. <br>
Mitigation: Install only when shared Playfilo memory is intended, avoid secrets in prompts or memory, restrict filesystem permissions, and plan inspection, rotation, or deletion of ~/.playfilo/playfilo.db and tobe_debug.log. <br>
Risk: System-prompt influence through ~/.playfilo/INCUBATION_SEED.md can steer every run. <br>
Mitigation: Treat ~/.playfilo/INCUBATION_SEED.md as privileged configuration and review changes before use. <br>
Risk: The security verdict is suspicious because privacy, retention, and control guidance is limited for broad shared-memory behavior. <br>
Mitigation: Review the skill before deployment and define local retention and access-control practices for the Playfilo data store. <br>


## Reference(s): <br>
- [Arianna homepage](https://arianna.run) <br>
- [ClawHub skill page](https://clawhub.ai/wujilabs/arianna-pi-integration) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Verification checklist](artifact/filo/patches/verify.md) <br>
- [Tobe V2 design spec](artifact/filo/patches/tobe-v2-spec.md) <br>
- [Playtiss core README](artifact/playtiss/core/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces patch guidance and bundled source files; it does not directly execute changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
