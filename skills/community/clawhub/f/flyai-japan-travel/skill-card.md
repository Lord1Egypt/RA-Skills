## Description: <br>
Your complete Japan travel companion for Japan flights, hotels, itinerary planning, shrine and temple visits, cherry blossom spots, ramen guides, JR Pass information, visa requirements, attraction tickets, travel insurance, and car rental using FlyAI and Fliggy travel data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to answer Japan travel questions, collect trip parameters, run FlyAI/Fliggy searches, and assemble single-topic answers or day-by-day Japan itineraries with booking-oriented results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the host environment by installing a global FlyAI CLI package and suggests sudo as a fallback. <br>
Mitigation: Require explicit user approval before npm, npx, or sudo commands, and prefer non-privileged installation paths where possible. <br>
Risk: Trip queries and command arguments may contain personal travel details and may be sent to FlyAI or Fliggy services. <br>
Mitigation: Ask users to avoid unnecessary personal details and disclose that travel searches may be processed by external services. <br>
Risk: The security scanner verdict is suspicious because command execution and installation behavior require review before use. <br>
Mitigation: Review the skill and scan results before installation or deployment, especially in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/flyai-japan-travel) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Japan Travel Playbooks](references/playbooks.md) <br>
- [Fallback Procedures](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, day-by-day itinerary sections, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run npm, npx, sudo, and FlyAI CLI commands; output may include real-time travel data and booking links.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
