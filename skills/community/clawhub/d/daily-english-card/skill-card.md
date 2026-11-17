## Description:

Generates a daily English speaking practice card image with scenario dialogue, review scheduling, and style rotation, then sends it to WeChat and archives it to an IMA knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryaction](https://clawhub.ai/user/jerryaction)

### License/Terms of Use:

MIT-0

## Use Case:

English learners and personal automation users use this skill to receive a scheduled daily oral-English study card in WeChat. The skill is also useful for maintaining spaced-review progress and archiving generated cards in an IMA knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends generated learning-card images and uploads them to external services automatically.

Mitigation: Configure and verify the intended WeChat recipient, bot account, cron schedule, and IMA knowledge base before enabling automatic delivery.

Risk: The release depends on local scripts and credential helpers that are not included in the artifact.

Mitigation: Review or package the referenced scripts and credential helpers, pin dependencies, and test card generation and upload manually before scheduled use.

Risk: A fixed Python path or missing Pillow installation can prevent card generation.

Mitigation: Install Pillow in the configured Python 3.9 environment or update the cron payload to a verified Python interpreter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryaction/skills/daily-english-card)
- [README.md](artifact/README.md)
- [Card example image](https://r2.image-upload.app/ptImg/4OOX6Lbi.jpeg)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG learning card, JSON script output, and concise Markdown/text status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one daily card image and a short delivery confirmation; depends on local Python, Pillow, WeChat messaging, cron, and IMA credentials.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
