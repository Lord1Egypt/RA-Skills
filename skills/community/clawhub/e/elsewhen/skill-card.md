## Description:

Guides agents through a persistent, turn-based historical text game in Traditional Chinese using a user-provided model key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenplus1000](https://clawhub.ai/user/tenplus1000)

### License/Terms of Use:

MIT-0

## Use Case:

Players and their command-capable agents use Elsewhen to explore a persistent historical setting, plan actions, and resume saved games in Traditional Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A billable model key is stored on a third-party game server.

Mitigation: Use a separate OpenRouter or Google AI Studio key with a low spending limit; never use a primary key.

Risk: An exposed Elsewhen token can grant access to saved games and the stored model key for this service.

Mitigation: Keep the account token private and do not paste it into conversations.

## Reference(s):

- [Elsewhen game and getting started](https://play.elsewhengame.com/about)
- [Elsewhen on ClawHub](https://clawhub.ai/tenplus1000/skills/elsewhen)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Traditional Chinese plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Turn-based narrative with persistent saved games; requires an account token and a dedicated model key.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
