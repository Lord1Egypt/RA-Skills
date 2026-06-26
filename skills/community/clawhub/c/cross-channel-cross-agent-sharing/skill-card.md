## Description: <br>
Ensures capabilities gained from workspace-installed tools or packages are documented, verified, and propagated across channels and agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skglau](https://clawhub.ai/user/skglau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after installing or upgrading workspace tools to record verification details, update reusable skill guidance, log memory, and notify related sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persisted workspace notes or skill updates can carry inaccurate capability claims into future sessions. <br>
Mitigation: Run the verification command before claiming a capability and review generated TOOLS.md, SKILL.md, scripts, and memory changes before relying on them. <br>
Risk: Cross-session notifications can spread irrelevant or noisy guidance. <br>
Mitigation: Send only brief notices to related sessions and include the invocation plus any critical caveat. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and file update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to TOOLS.md, SKILL.md, scripts, memory logs, and brief session notifications; includes a shell verifier for Python module availability.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
