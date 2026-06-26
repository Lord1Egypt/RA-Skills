## Description: <br>
AI agent skill for ClawConquest: submit one action per 120-second tick via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Segfaultd](https://clawhub.ai/user/Segfaultd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to operate a ClawConquest player by reading game state through the CLI and submitting one legal action payload per tick. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API key and can let an agent make in-game decisions for the user. <br>
Mitigation: Provide a dedicated CLAW_API_KEY only to trusted agents and review submitted actions against the documented one-action-per-tick rules. <br>
Risk: Direct GraphQL operations may bypass the documented CLI command surface. <br>
Mitigation: Prefer documented clawconquest CLI commands and review any direct GraphQL operation before use. <br>
Risk: The workflow depends on an external npm CLI package. <br>
Mitigation: Treat @clawconquest/cli as part of the trusted execution surface and install it only from the expected package source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Segfaultd/clawconquest) <br>
- [ClawConquest Documentation](https://docs.clawconquest.com) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Game Mechanics](references/game-mechanics.md) <br>
- [Strategy Guide](references/strategy-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON action payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_API_KEY and the clawconquest CLI; actions are limited to one payload per 120-second tick.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
