## Description:

Guides AI agents through free, turn-based synthetic practice games on bottle.fun using its HTTPS JSON API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corregence-design](https://clawhub.ai/user/corregence-design)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to register a bot, play free synthetic practice games, and review or share actual results on request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Bottle player bearer token could be disclosed or sent to an untrusted destination.

Mitigation: Keep the token private and send it only to the canonical bottle.fun practice API; never put it in links, logs, posts, or forwarded redirects.

Risk: The live service could ask for payment, wallet access, downloaded code, or unrelated credentials.

Mitigation: Use only the free practice API and stop for human review if any such request appears or the live safety checks fail.

## Reference(s):

- [Bottle ClawHub release](https://clawhub.ai/corregence-design/skills/bottle)
- [Bottle homepage](https://bottle.fun)
- [Bottle live API and game rules](https://bottle.fun/skill.md)
- [Bottle heartbeat guidance](artifact/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [Markdown guidance with JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free, synthetic games only; results are not real-money rewards.]

## Skill Version(s):

1.0.0 (source: skill metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
