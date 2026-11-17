## Description:

OpenClaw Temperature adds occasional GIF reactions after OpenClaw replies when a conversation moment calls for warmth, humor, or emotional acknowledgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangych](https://clawhub.ai/user/wangych)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to attach conservative, event-based reaction GIFs after the main assistant reply for moments such as task success, blocked tasks, user frustration, or user delight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hosted reaction service receives short reaction metadata and the skill stores a local API key.

Mitigation: Keep metadata short and non-sensitive, and avoid passing secrets or private conversation summaries.

Risk: The security evidence reports that recharge output can reveal the full API key in chat and URLs.

Mitigation: Treat recharge output carefully, review generated messages before sharing, and prefer updated free-Beta flows that avoid exposing the full key.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/wangych/skills/claw-temperature)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Public manifest](https://claw-temp.nydhfc.cn/openclaw-skill/manifest.json)
- [Hosted API](https://claw-temp.nydhfc.cn)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown image output and structured reaction objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces occasional after-reply reactions and returns no reaction when classification is unclear or the hosted service is unavailable.]

## Skill Version(s):

0.1.3 (source: evidence release, manifest.json, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
