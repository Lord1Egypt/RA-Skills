## Description:

Creates a picture book from a theme by drafting a paged story, generating consistent illustrations and background music, and assembling them into an interactive HTML book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to turn a theme into a read-aloud children's story with consistent illustrations, music, and a browsable HTML book.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's tool scope and runtime permissions are not fully characterized, and scan coverage was partial because some local path references could not be resolved.

Mitigation: Review the included files and CLI behavior before installation, and grant only the permissions needed for the requested book-generation steps.

Risk: Prompts and local reference images are sent to dLazy hosted services during illustration and music generation.

Mitigation: Avoid submitting sensitive text or images, and confirm the data-sharing implications before using those services.

## Reference(s):

- [CLI source link listed in the skill documentation (not server-verified provenance)](https://github.com/dlazy-ai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML, Images, Audio]

**Output Format:** [Paged story data in book.json, an interactive HTML book, and associated illustration and music files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually 10 pages; theme, audience, art style, and page count can be tailored to the user's brief.]

## Skill Version(s):

1.3.40 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
