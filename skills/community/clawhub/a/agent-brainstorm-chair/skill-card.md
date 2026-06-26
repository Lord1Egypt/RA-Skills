## Description: <br>
Agent Brainstorm Chair facilitates structured multi-agent brainstorming with role assignment, round control, baton handoffs, and fallback modes for Hermes, OpenClaw, or manual facilitation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[usewild2026](https://clawhub.ai/user/usewild2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and teams use this skill to run structured brainstorming sessions across multiple agents or simulated roles before turning decisions into execution steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw bridge use can require broader local agent privileges than a casual meeting trigger suggests. <br>
Mitigation: Use an explicit trigger phrase, review bridge scripts before use, and limit ACP capabilities to read-only when consultation is sufficient. <br>
Risk: Command-line prompts and bridge calls can expose sensitive credentials if tokens or passwords are included. <br>
Mitigation: Keep tokens and passwords out of command-line arguments and meeting prompts; pass only the minimum discussion context needed. <br>
Risk: Fallback simulation mode can make one agent's role-play look like independent multi-agent consensus. <br>
Mitigation: Label simulation mode clearly and keep strategist, executor, and facilitator outputs separated by role. <br>


## Reference(s): <br>
- [Adapter Guide](ADAPTERS.md) <br>
- [Setup Guide](SETUP_GUIDE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/usewild2026/agent-brainstorm-chair) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Facilitation guidance] <br>
**Output Format:** [Markdown with structured role labels and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate baton messages, meeting summaries, execution checklists, and OpenClaw consultation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
