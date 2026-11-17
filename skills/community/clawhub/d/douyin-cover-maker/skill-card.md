## Description:

Create a Douyin cover or vertical short-video cover from a video topic, hook, script, portrait, product photo, or reference image. This AI cover maker builds a clear focal visual and headline-safe composition for Douyin short-video covers, creator series, product demos, tutorials, food, lifestyle, and knowledge content, then refines an accepted draft into a consistent account-cover direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and content teams use this skill to create a Douyin or vertical short-video cover from a topic, script, key frame, product or portrait photo, or visual reference. It can also refine an accepted cover draft into a consistent account style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad shared Beatra authorization beyond image creation, and revoking the shared credential disconnects every Beatra skill using it.

Mitigation: Review the authorization scope before connecting and proceed only if it is acceptable; check which Beatra skills share the credential before revoking it.

Risk: Image generation is paid, uploaded images may contain sensitive material, and installation analytics are documented.

Mitigation: Upload only images intended to be shared, review the complete request and approve each paid generation, and consult the installation and privacy disclosures.

Risk: The security evidence reports an uninstall flaw that could disconnect other Beatra skills when the skill inventory is malformed.

Mitigation: Before uninstalling, check for other installed Beatra skills and verify the connection outcome; use console revocation only when disconnecting all skills sharing the credential is intended.

## Reference(s):

- [Douyin Video Cover Maker on ClawHub](https://clawhub.ai/beatra-ai/skills/douyin-cover-maker)
- [Workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [Billing errors and recovery](references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Image artifacts, Text result details]

**Output Format:** [Generated cover image artifact link with a Markdown result summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One cover per request; canvas and style follow the confirmed brief, with vertical 9:16 as the default for Douyin.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
