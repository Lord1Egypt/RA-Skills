## Description:

Creates Instagram carousel content by researching viral references, selecting a Formula 100K format, drafting slide-by-slide copy and design guidance, generating a hook image when configured, and optionally helping build the carousel in Canva.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media teams, and agents use this skill to turn an idea, script, or reel into a complete Instagram carousel package with hook research, slide copy, design direction, production guidance, caption text, and a follow-on content calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Carousel prompts and brand context may be sent to Gemini or similar external services using configured API credentials.

Mitigation: Use only intended API keys, remove credentials that should not be available to the agent, and review provider costs before enabling image generation or research tools.

Risk: The skill can optionally edit a Canva design supplied by the user.

Mitigation: Provide only the intended editable Canva link and review the generated slides before accepting or publishing changes.

Risk: The saved brand profile is persistent local data.

Mitigation: Review the contents of the design profile before reuse and clear it when it should not persist across sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/carrusel-viral-formula100k)
- [ClawHub publisher profile](https://clawhub.ai/user/formula100k)
- [Design profile reference](artifact/references/design_profile.md)
- [Carousel format catalog index](artifact/references/formatos-carrusel-35.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with slide-by-slide carousel copy, Canva production instructions, image-generation prompts, captions, checklists, and content-calendar tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API command examples and may create a local hook image file when image generation is configured.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
