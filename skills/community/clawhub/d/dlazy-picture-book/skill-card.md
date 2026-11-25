## Description:

Creates a complete picture book from a theme, including a paged story, consistent illustrations, background music, and a standalone HTML reader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to create illustrated storybooks for readers, including children's and bedtime books. It guides story planning, page-by-page media generation, and assembly of a browsable HTML book.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis is partial and leaves some file-access and media-download scope questions unresolved.

Mitigation: Review the skill’s access disclosures and tool permissions before installation, and inspect downloaded media before opening the finished book.

Risk: The workflow sends prompts to dLazy services and uploads local reference images for illustration generation.

Mitigation: Avoid sending sensitive prompts or images, and confirm that users are comfortable with those materials being processed by the service.

## Reference(s):

- [CLI project link listed in skill metadata (release provenance unavailable)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML, Image and audio files]

**Output Format:** [Paged story content in book.json and a standalone HTML book with linked illustration and music assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to 10 pages; the book folder includes the HTML reader and generated media assets.]

## Skill Version(s):

1.3.43 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
