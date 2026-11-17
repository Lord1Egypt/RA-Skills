## Description:

Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Twitter/X activity, monitor competitors or watchlists, and run user-approved OAuth posting workflows through AIsa.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the AISA API key in command output.

Mitigation: Avoid running it where stdout is logged, do not paste logs publicly, and rotate the key if it may have been printed.

Risk: Posting and media uploads can publish user content publicly through the AIsa Twitter/X relay.

Mitigation: Require explicit user approval before posting, upload only files the user intentionally provided, and confirm API success before claiming publication.

## Reference(s):

- [AIsa Twitter OAuth](references/post_twitter.md)
- [AIsa Homepage](https://aisa.one)
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/aisa-twitter-api-command-center-slot1)
- [baofeng-tech Publisher Profile](https://clawhub.ai/user/baofeng-tech)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AISA_API_KEY and can send approved media files to the AIsa Twitter/X relay.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
