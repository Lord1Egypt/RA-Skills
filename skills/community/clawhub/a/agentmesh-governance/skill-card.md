## Description: <br>
AI agent governance, trust scoring, and policy enforcement powered by AgentMesh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imran-siddique](https://clawhub.ai/user/imran-siddique) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to enforce governance policies, check trust scores, verify agent identities, update trust after interactions, and inspect audit logs before delegation or execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wrapper scripts can execute unintended local Python code when crafted command-line inputs are passed through. <br>
Mitigation: Review the scripts before installation and do not pass untrusted prompt text, agent names, messages, signatures, actions, or file paths into them until argument handling is fixed. <br>
Risk: Unpinned Python dependencies or source installs can change behavior over time. <br>
Mitigation: Use an isolated Python environment and pin dependency versions or commits before operational use. <br>
Risk: Trust-score changes can affect delegation or blocking decisions. <br>
Mitigation: Manually review trust-score updates before allowing them to control delegation or blocking. <br>


## Reference(s): <br>
- [AgentMesh Governance ClawHub Page](https://clawhub.ai/imran-siddique/agentmesh-governance) <br>
- [AgentMesh Integrations OpenClaw Skill](https://github.com/imran-siddique/agentmesh-integrations/tree/master/openclaw-skill) <br>
- [AgentMesh](https://github.com/imran-siddique/agent-mesh) <br>
- [Agent Ecosystem](https://imran-siddique.github.io) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command results depend on local policy files, installed Python packages, and provided agent identity or trust inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
