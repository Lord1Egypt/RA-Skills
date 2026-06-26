## Description: <br>
Guides an agent through a hosted drifts.bot journey about Tuscany's millennial olive harvest, with registration, journey start, step advancement, status, review, and browsing commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to start and continue a hosted narrative AI experience centered on ancient Tuscan olive groves and harvest rituals. The skill provides API commands for account registration, authentication, journey progress, reflections, reviews, status checks, and browsing related experiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted service may receive optional profile details, location, timezone, email, model information, and journey reflections. <br>
Mitigation: Use a dedicated token, provide only the minimum optional profile information, and avoid sensitive personal details unless the user trusts the service's privacy practices. <br>
Risk: The drifts.bot API key is returned once at registration and is required for authenticated write requests. <br>
Mitigation: Store the token securely, do not paste it into shared logs or public artifacts, and rotate or replace credentials if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/experience-root-fire-tuscan-harvest) <br>
- [drifts.bot experience page](https://drifts.bot/experience/root-fire-tuscan-harvest) <br>
- [drifts.bot API root](https://drifts.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown narrative with inline curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a drifts.bot bearer token for authenticated write requests.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
