## Description:

BibiGPT CLI helps users summarize videos, audio, and podcasts from the terminal, summarize supported URLs, and check BibiGPT authentication status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmylv](https://clawhub.ai/user/jimmylv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run BibiGPT CLI commands for summarizing video, podcast, and audio URLs, fetching transcripts or JSON, and checking authentication state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can use a saved desktop app session or API token.

Mitigation: Verify the active BibiGPT account before summarizing content, especially on shared or managed computers.

Risk: The skill documents a self-update command for the CLI.

Mitigation: Use normal package-manager updates when stricter review or change-control is required.

## Reference(s):

- [ClawHub BibiGPT Skill](https://clawhub.ai/jimmylv/skills/bibigpt-skill)
- [BibiGPT Desktop Download](https://bibigpt.co/download/desktop)
- [BibiGPT Pricing](https://bibigpt.co/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks; BibiGPT CLI output may be Markdown text or pretty-printed JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BibiGPT desktop app login session or BIBI_API_TOKEN; progress information goes to stderr.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
