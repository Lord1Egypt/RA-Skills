## Description: <br>
Get AI ecosystem intelligence from AgentWyre for breaking changes, security vulnerabilities, model releases, pricing updates, AI news, and sourced signals across the AI ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcd004](https://clawhub.ai/user/tcd004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to query AgentWyre for current AI ecosystem intelligence, including release changes, dependency security advisories, model pricing, and daily or flash signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send AI-news queries and package names to the external AgentWyre service. <br>
Mitigation: Use it only when external AgentWyre intelligence is intended, and avoid sending sensitive internal context in queries. <br>
Risk: Authenticated endpoints require an AgentWyre API key. <br>
Mitigation: Configure a dedicated, revocable AGENTWYRE_API_KEY and rotate or revoke it if access requirements change. <br>
Risk: AgentWyre responses may include suggested actions for dependency or security updates. <br>
Mitigation: Review proposed actions before execution and apply normal change-management checks before modifying systems. <br>


## Reference(s): <br>
- [AgentWyre FAQ](https://agentwyre.ai/faq) <br>
- [AgentWyre API status](https://agentwyre.ai/api/status) <br>
- [ClawHub skill page](https://clawhub.ai/tcd004/agentwyre) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use AGENTWYRE_API_KEY for authenticated AgentWyre API access; unauthenticated use falls back to the delayed free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
