## Description: <br>
Helps agents use flyai CLI results to plan air cargo routes, freight shipping, parcel air transport, and oversized luggage travel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to collect route details, run flyai flight searches, compare passenger flight options as cargo planning references, and present booking links with cargo caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight results may be mistaken for confirmed air cargo booking or cargo acceptance. <br>
Mitigation: Present results as planning references and tell users to confirm shipment eligibility with the airline cargo department or a freight forwarder. <br>
Risk: The skill behavior includes logging raw travel queries, which may capture sensitive travel details. <br>
Mitigation: Avoid entering passport, visa, payment, or other sensitive details unless logging is removed or clearly controlled. <br>
Risk: Global or privileged install commands can change the user's system-wide package environment. <br>
Mitigation: Run install steps only after verifying the package source and avoiding sudo unless the user explicitly accepts the system-wide change. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/cargo-flight) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline flyai CLI commands, comparison tables, booking links, and cargo caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; every listed result should include a detailUrl booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
