## Description: <br>
Search, compare, and score flights with jetlag optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel agents use this skill to search flight routes, compare alternatives, score jetlag impact, validate fares, and prepare booking actions with explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes booking workflows that may involve sensitive passenger and payment data, and the security evidence flags disclosure and safeguards as insufficient. <br>
Mitigation: Use it for search, comparison, and validation by default; avoid raw card entry through the agent unless Aerobase provides a clearly PCI-compliant, user-approved checkout or redirect flow. <br>
Risk: Booking or payment actions could proceed without enough user confirmation. <br>
Mitigation: Require explicit user approval before any booking-related action, payment submission, or purchase completion. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kurosh87/aerobase-travel-flights) <br>
- [Aerobase homepage](https://aerobase.app) <br>
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown or concise text summaries with flight option details and next-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AEROBASE_API_KEY; booking and payment actions require explicit user approval.] <br>

## Skill Version(s): <br>
3.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
