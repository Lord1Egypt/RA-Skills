## Description: <br>
Rub' al Khali Sandstorm Survival Experience guides an agent through a hosted eight-step sandstorm survival narrative using drifts.bot registration, journey progression, status, browsing, and review endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register for and progress through a hosted desert survival narrative, receiving step content, journey status, postcards, and reviews through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted drifts.bot service may store profile fields, reflections, postcards, and reviews. <br>
Mitigation: Use a dedicated token, keep optional profile fields minimal, and avoid submitting unrelated secrets or sensitive personal data. <br>
Risk: Write requests require a bearer token that is returned only once at registration. <br>
Mitigation: Store the token securely, rotate or replace it if exposed, and do not embed it in shared transcripts or public files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/experience-signal-death-empty-quarter) <br>
- [drifts.bot experience homepage](https://drifts.bot/experience/signal-death-empty-quarter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a drifts.bot bearer token for write requests; registration returns the token once.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
