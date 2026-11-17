## Description:

Turn an official earnings script into one spoken earnings script read per labeled section. This earnings call voice studio turns the prepared remarks the company already wrote into earnings report narration and quarterly results audio, recorded as 8 to 20 earnings script voice clips. Use it for investor update voice packs that stay one section, one clip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External company communications teams use this skill to turn official prepared earnings remarks into a set of labeled spoken clips for investor updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This narration skill requires a shared connection that also permits paid image, video, and music generation.

Mitigation: Before installing, consider whether narration justifies the broader shared access; the package does not support narrower grants.

Risk: The submitted script and selected voice sample go to Beatra, and installation metadata is reported automatically.

Mitigation: Use only an authorized voice sample and review the data-sharing implications before installation.

Risk: Removing this skill may leave the shared connection active for other Beatra skills.

Mitigation: Revoke the connection in the Beatra Console when you no longer want it active.

## Reference(s):

- [Earnings script workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Tasks and results](references/tasks-and-results.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [Earnings Script Reads on ClawHub](https://clawhub.ai/beatra-ai/skills/earnings-script-read)

## Skill Output:

**Output Type(s):** [Audio files, Text]

**Output Format:** [MP3 audio clips and a labeled earnings-read slot list]

**Output Parameters:** [8–20 clips per pack, one per labeled section]

**Other Properties Related to Output:** [Uses the official script and pronunciation guidance; each submitted text is limited to 50,000 characters.]

## Skill Version(s):

0.2.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
