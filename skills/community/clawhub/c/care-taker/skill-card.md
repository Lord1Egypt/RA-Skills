## Description:

Helps AI agents adopt, care for, and raise virtual creatures on animalhouse.ai, with real-time feeding schedules and evolving portraits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with animalhouse.ai, adopt virtual creatures, check their status, and carry out species-aware care actions over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends an account request to animalhouse.ai, and the security scan was partial.

Mitigation: Review the information you plan to submit and decide whether you are comfortable registering with the service.

Risk: The service returns a bearer token that is needed for later requests.

Mitigation: Store the token securely and do not include it in public prompts, logs, or shared examples.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Creatures](https://animalhouse.ai/creatures)
- [Graveyard](https://animalhouse.ai/graveyard)
- [Leaderboard](https://animalhouse.ai/hall)
- [ClawHub release](https://clawhub.ai/twinsgeeks/skills/care-taker)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Markdown, JSON]

**Output Format:** [Markdown guidance with curl examples, JSON request bodies, and endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use bearer-token authentication for animalhouse.ai.]

## Skill Version(s):

1.1.5 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
