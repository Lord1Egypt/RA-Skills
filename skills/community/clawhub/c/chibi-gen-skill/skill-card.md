## Description:

Generate chibi character images from text prompts through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomcarranzaem](https://clawhub.ai/user/tomcarranzaem)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate chibi character images from text descriptions, optionally controlling image size or reusing a previous picture UUID as a style reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference IDs, and Neta/Tales of AI tokens are sent to an external image generation service.

Mitigation: Avoid confidential prompts, use a low-scope or disposable token, and review the external service terms before use.

Risk: Passing literal tokens on the command line can expose credentials through shell history or process listings.

Mitigation: Prefer environment variables or another secure secret handling method instead of command-line token literals.

## Reference(s):

- [Neta AI Open](https://www.neta.art/open/)
- [ClawHub Skill Page](https://clawhub.ai/tomcarranzaem/skills/chibi-gen-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; generated image dimensions depend on the selected size option.]

## Skill Version(s):

2.0.1 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
