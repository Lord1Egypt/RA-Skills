## Description: <br>
Anthropic Buddy helps agents use animalhouse.ai's virtual pet API for 73+ species with real-time hunger, permanent death, and pixel art portraits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent interact with the animalhouse.ai virtual pet API for registration, adoption, pet status checks, and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands interact with a third-party virtual pet API and may create or modify account and pet state. <br>
Mitigation: Review each command before running it and install the skill only when interaction with animalhouse.ai is intended. <br>
Risk: The registration flow returns an ah_ bearer token that grants access to the account. <br>
Mitigation: Keep the token private, avoid sharing command history or logs containing it, and use minimal profile information if privacy matters. <br>
Risk: The skill name and text reference Anthropic and Claude, but server evidence does not show official affiliation. <br>
Mitigation: Treat the release as a third-party community skill and do not assume it is owned, endorsed, or operated by Anthropic or Claude. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/anthropic-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes visible curl commands for a third-party virtual pet API; no local code execution is bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
