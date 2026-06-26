## Description: <br>
ANCC helps agents discover, validate, audit, and integrate ANCC-compliant CLI tools for local agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppiankov](https://clawhub.ai/user/ppiankov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and run the ANCC CLI for validating agent-native tools, auditing local agent environments, checking token budgets, and scaffolding compliant tool definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit workflow may inspect sensitive local credential and shell history locations. <br>
Mitigation: Run ANCC only in the intended local workspace, review audit output before sharing it, and avoid exposing local credential paths or configuration details. <br>
Risk: Install commands may fetch the latest external CLI release. <br>
Mitigation: Prefer pinned or otherwise verified ANCC releases before using the skill in production workflows. <br>


## Reference(s): <br>
- [ANCC documentation](https://ancc.dev) <br>
- [ANCC GitHub repository](https://github.com/ppiankov/ancc) <br>
- [ANCC ClawHub listing](https://clawhub.ai/ppiankov/ancc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of JSON-formatted ANCC CLI output for machine parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
