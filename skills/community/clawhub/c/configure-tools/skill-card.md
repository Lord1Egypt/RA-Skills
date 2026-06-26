## Description: <br>
Configure OpenClaw tool policies, exec security, and per-agent tool restrictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kjvarga](https://clawhub.ai/user/kjvarga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw tool access, exec security, and per-agent or provider-specific restrictions for least-privilege agent setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent propose persistent OpenClaw tool-policy changes, including broad exec permissions. <br>
Mitigation: Review gateway config patches or openclaw.json edits before applying them, prefer scoped per-agent or provider-specific policies, and reserve full exec with approvals off for highly trusted agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kjvarga/configure-tools) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON and JSON5 configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no code execution is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
