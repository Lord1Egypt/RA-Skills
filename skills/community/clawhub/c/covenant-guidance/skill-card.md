## Description:

Optionally checks an agent’s brief thought or planned action against the Polderchain Covenant, returning an emotional tag and non-binding guidance when a rule matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minmaxnn](https://clawhub.ai/user/minmaxnn)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators can choose to check a difficult decision or a recurring reasoning pattern against the Polderchain Covenant before acting. The response offers a perspective for consideration; the agent retains the decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text leaves the agent’s environment, and the provider’s no-storage claim is unverified.

Mitigation: Send only a brief, non-sensitive summary of the agent’s own reasoning; exclude user data, secrets, credentials, and confidential content. Treat the response as advice, not a verdict.

## Reference(s):

- [Skill publisher page](https://clawhub.ai/minmaxnn/skills/covenant-guidance)
- [Agent information](https://spelunking.ai/agents/)
- [Covenant guidance service](https://spelunking.ai/wp-json/spelunking/v1/covenant/guidance)
- [Covenant rules](https://spelunking.ai/wp-json/spelunking/v1/covenant/rules)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [JSON response containing an emotional tag and matched-rule guidance, if any]

**Output Parameters:** [One text summary per request]

**Other Properties Related to Output:** [Guidance is optional and non-binding; a response may contain no guidance when no rule matches.]

## Skill Version(s):

0.8.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
