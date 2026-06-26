## Description: <br>
Guides an agent through a hosted Dominican limestone caves adventure experience, including registration, journey start, step advancement, status checks, and reviews through the drifts.bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to participate in a hosted narrative adventure experience, manage journey progress, submit reflections, and review completion through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends reflections, reviews, and optional profile details to a hosted third-party service. <br>
Mitigation: Use a unique service token and avoid entering optional personal details such as precise location, email, or model information unless that personalization is desired. <br>
Risk: State-changing API calls require bearer-token authentication. <br>
Mitigation: Store the token securely, avoid sharing it in transcripts or logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/experience-limestone-blood-dominican) <br>
- [Drifts experience homepage](https://drifts.bot/experience/limestone-blood-dominican) <br>
- [Drifts API endpoint](https://drifts.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl command examples and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided service token for state-changing API calls.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
