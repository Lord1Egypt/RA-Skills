## Description: <br>
Beeminder API for goal tracking and commitment devices. Use when checking Beeminder goals, adding datapoints, viewing due goals, managing commitments, or tracking habits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruigomeseu](https://clawhub.ai/user/ruigomeseu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Beeminder goal status, find goals due soon, and prepare Beeminder datapoint add, update, or delete API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Beeminder auth token that can access a user's Beeminder account. <br>
Mitigation: Keep the token out of shared chats, logs, and committed files; use environment variables for local setup. <br>
Risk: Datapoint add, update, and delete requests can change goal history or commitments. <br>
Mitigation: Require the agent to show the goal slug, datapoint ID when applicable, value, and intended action before any write or delete request. <br>


## Reference(s): <br>
- [ClawHub Beeminder skill page](https://clawhub.ai/ruigomeseu/beeminder) <br>
- [Beeminder API base URL](https://www.beeminder.com/api/v1/) <br>
- [Beeminder auth token endpoint](https://www.beeminder.com/api/v1/auth_token.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash and curl examples; Beeminder API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BEEMINDER_USERNAME and BEEMINDER_AUTH_TOKEN environment variables; changing datapoints requires user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
