## Description: <br>
Implementation of the Dynamic Ethical Entity Personality (D.E.E.P.) v2 Framework. The cognitive architecture for agentic sovereignty and partnership. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daCptn](https://clawhub.ai/user/daCptn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to structure local agent personality files, check whether required personality pillars exist, and synchronize selected Markdown values into a local JSON vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local personality and memory data that may contain sensitive personal information. <br>
Mitigation: Avoid storing secrets or sensitive personal information in personality files, and review or delete memory/personality/soul_vault.json as needed. <br>
Risk: The advertised triple-check safety filter always returns a proceed verdict in the provided artifact behavior. <br>
Mitigation: Do not rely on deep_triple_check as a real safety approval mechanism unless it is changed to perform actual checks and reject unsafe actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daCptn/deep-framework) <br>
- [personality_template.md](artifact/personality_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python >=3.8 and reads or writes local files under memory/personality/.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
