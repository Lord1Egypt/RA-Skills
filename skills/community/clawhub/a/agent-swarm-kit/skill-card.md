## Description: <br>
Multi-agent swarming for OpenClaw - two or more AI agents collaborating in real time on shared Discord channels, with config patterns, loop prevention, channel setup, and handoff protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vswarm-ai](https://clawhub.ai/user/vswarm-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure two or more OpenClaw agents to collaborate in a shared Discord channel for complex debugging, architecture decisions, research synthesis, and code review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bot tokens or other channel credentials could be exposed during setup. <br>
Mitigation: Keep bot tokens out of chat and source control, and configure separate bot accounts through private operational channels. <br>
Risk: Agents could respond in unintended Discord channels or with broader permissions than needed. <br>
Mitigation: Use a private swarming channel and restrict bot roles to only the permissions needed for that channel. <br>
Risk: Multi-agent conversations can loop or continue after they stop adding new information. <br>
Mitigation: Apply the included SOUL.md swarming rules, including mention discipline, exchange limits, summaries, and clear action ownership. <br>


## Reference(s): <br>
- [Agent Swarm Kit](SKILL.md) <br>
- [Swarming Channel Config - OpenClaw Examples](templates/CHANNEL_CONFIG.md) <br>
- [Swarming Rules - Add to SOUL.md](templates/SWARMING_RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown] <br>
**Output Format:** [Markdown with JSON configuration examples and copy-paste rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; produces setup guidance and reusable configuration snippets for OpenClaw Discord swarming workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
