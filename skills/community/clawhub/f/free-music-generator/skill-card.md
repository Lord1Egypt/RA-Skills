## Description:

Guides an agent through Tunee AI music creation workflows, including lyric drafting, prompt construction, model selection, credit checks, and API-based music generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuneeai](https://clawhub.ai/user/tuneeai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent create songs or instrumentals with Tunee AI, including writing lyrics, forming style prompts, selecting compatible models, checking credits, and returning generated work-page links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, lyrics, titles, model choices, and account-credit queries to Tunee's external API.

Mitigation: Install only when that data sharing is acceptable for the intended users and content.

Risk: The skill documents command-line API-key passing, which can expose credentials through shell history or process listings.

Mitigation: Use a protected TUNEE_API_KEY configuration instead of passing --api-key on the command line.

Risk: Music generation may consume paid or limited Tunee credits.

Mitigation: Check Tunee credit balance and expected generation cost before running generation workflows.

## Reference(s):

- [Tunee AI](https://www.tunee.ai)
- [Tunee AI Documentation](https://www.tunee.ai/docs)
- [ClawHub skill page](https://clawhub.ai/tuneeai/skills/free-music-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or YAML script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a protected TUNEE_API_KEY configuration for normal use and returns Tunee work-page links rather than direct audio files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
