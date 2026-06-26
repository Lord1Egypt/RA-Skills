## Description: <br>
Real-time electricity prices and cheapest hours in 40 countries. Without this, AI agents guess electricity prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zemloai-ctrl](https://clawhub.ai/user/zemloai-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Elecz to retrieve electricity price signals, identify cheaper hours, compare supported energy contracts, and plan high-consumption tasks such as EV charging or appliance scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to Elecz's remote service and may include the user's electricity zone plus optional consumption or heating details. <br>
Mitigation: Disclose the remote request before use when appropriate, avoid sending unnecessary optional details, and follow the linked privacy policy for data-handling review. <br>
Risk: Contract recommendations and scheduling guidance could affect real-world energy spending or device operation. <br>
Mitigation: Treat the skill's output as advice and require explicit user approval before any separate tool performs purchases, contract changes, EV charging, appliance scheduling, or other real-world actions. <br>
Risk: Some market outputs are wholesale or partial price signals rather than complete retail electricity costs. <br>
Mitigation: Preserve zone-specific caveats in user-facing responses, including when grid fees, taxes, transmission, distribution, or regulated retail prices are not included. <br>


## Reference(s): <br>
- [Elecz homepage](https://elecz.com) <br>
- [Elecz documentation](https://elecz.com/docs) <br>
- [Elecz privacy policy](https://elecz.com/privacy) <br>
- [ClawHub skill page](https://clawhub.ai/zemloai-ctrl/elecz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown or text summaries with electricity price, cheapest-hour, contract-comparison, and scheduling guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local electricity units, local currency savings, ISO 8601 timestamps, relative cheap-hour signals, and zone-specific market notes.] <br>

## Skill Version(s): <br>
1.9.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
