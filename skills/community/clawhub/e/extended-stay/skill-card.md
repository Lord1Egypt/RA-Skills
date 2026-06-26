## Description: <br>
Find serviced apartments and hotels for extended stays, including weekly or monthly rates, kitchenettes, laundry, and home-like amenities for long-term travelers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for long-stay hotels and serviced apartments with real-time pricing and booking links through the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a global flyai CLI dependency before use. <br>
Mitigation: Require explicit approval before npm global installation and prefer an isolated or pinned CLI installation. <br>
Risk: Travel-search details may be sent to the flyai provider and retained locally in an execution log. <br>
Mitigation: Use the skill only when the provider is trusted, avoid sensitive itinerary details, and disable or delete .flyai-execution-log.json if local retention is not desired. <br>
Risk: Results may be misleading if the agent answers from prior knowledge instead of fresh CLI output. <br>
Mitigation: Verify that every travel result includes a booking link from CLI output and rerun the CLI workflow when links or real-time data are missing. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a working flyai CLI and should include booking links sourced from CLI output.] <br>

## Skill Version(s): <br>
v3.2.4 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
