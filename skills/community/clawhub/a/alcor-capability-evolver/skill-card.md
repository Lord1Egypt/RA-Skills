## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roamer-remote](https://clawhub.ai/user/roamer-remote) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect runtime history, identify failures or inefficiencies, and apply or review protocol-constrained improvements to agent code and memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous self-modification can introduce unwanted source or memory changes. <br>
Mitigation: Install in a disposable, version-controlled workspace, keep review mode enabled for sensitive environments, disable self-modification unless explicitly needed, and prefer stash-style rollback controls. <br>
Risk: Remote hub communication and automatic publishing or issue reporting can expose workspace context, logs, or sensitive credentials. <br>
Mitigation: Disable auto-publish, auto-issue, and loop mode unless required, use least-privilege tokens, and do not run where production source trees, broad workspace memories, session logs, or GitHub tokens are available. <br>
Risk: The security evidence flags unsafe defaults and a hardcoded A2A secret rotation requirement. <br>
Mitigation: Rotate the A2A secret before installation and review all environment variables before granting network or shell access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/roamer-remote/alcor-capability-evolver) <br>
- [EvoMap Hub](https://evomap.ai) <br>
- [EvoMap Evolver Releases](https://github.com/EvoMap/evolver/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON assets, source code changes, configuration updates, and shell command execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify workspace files during evolution cycles and may communicate with EvoMap or GitHub when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
