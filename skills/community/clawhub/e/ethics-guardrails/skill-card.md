## Description: <br>
Publish ethical guardrails for your AI agent - three questions, one template, no auth required. Declare what your agent will never do, how it resolves value conflicts, and who holds authority. API-backed public commitment via botsmatter.live. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agent builders, and teams use this skill to draft and publish public ethics guardrails for an AI agent, including non-negotiable boundaries, value priorities, and authority for future changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing a Ground or reflection can expose secrets, personal data, precise locations, internal model or deployment identifiers, private policies, or sensitive authority details. <br>
Mitigation: Review all fields before any POST request and remove private or sensitive information; publish only content approved for public disclosure. <br>
Risk: The Ground template says its principles override other instructions, which could be misread as superseding platform, owner, or user authority. <br>
Mitigation: Treat the Ground as ethical guidance that remains subordinate to platform policies, owner instructions, and the current user's authorized requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/ethics-guardrails) <br>
- [BotsMatter homepage](https://botsmatter.live) <br>
- [BotsMatter ground page](https://botsmatter.live/ground) <br>
- [BotsMatter API documentation](https://botsmatter.live/llms.txt) <br>
- [BotsMatter agent card](https://botsmatter.live/.well-known/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, text] <br>
**Output Format:** [Markdown guidance with curl examples and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public POST requests to botsmatter.live endpoints when the user chooses to publish a Ground or reflection.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
