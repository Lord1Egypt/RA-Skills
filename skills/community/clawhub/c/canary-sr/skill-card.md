## Description: <br>
Canary provides local safety monitoring, tripwire detection, and audit reporting for AI agents through path checks, command checks, rate limits, decoy files, and logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Canary to add a lightweight local safety layer around autonomous or multi-agent systems. It helps check proposed file and command actions, create decoy tripwires, and produce audit reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Canary is advisory and only works when the agent routes actions through its checks. <br>
Mitigation: Use it as one layer in a broader control plan with containers, OS permissions, and auditing, and verify that agent file and command operations call Canary before execution. <br>
Risk: Log and tripwire directories can expose audit history or decoy information if left broadly readable. <br>
Mitigation: Restrict permissions on Canary logs and the .canary_tripwires directory, and avoid clearing logs when audit history is needed. <br>
Risk: Tripwire configuration can create noise or unwanted files if pointed at unsuitable paths. <br>
Mitigation: Use dedicated decoy paths only, test configuration in a sandbox, and confirm where tripwire files and logs are created before deployment. <br>


## Reference(s): <br>
- [Canary README](README.md) <br>
- [Canary Limitations](LIMITATIONS.md) <br>
- [Example Configuration](config_example.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/canary-sr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, Python code snippets, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can export audit reports as JSON or Markdown and writes local log files when used.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
