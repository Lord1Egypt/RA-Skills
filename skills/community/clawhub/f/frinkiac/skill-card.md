## Description:

Search TV show screenshots and generate memes from The Simpsons, Futurama, Rick and Morty, and 30 Rock.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryantenney](https://clawhub.ai/user/ryantenney)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search dialogue, browse frames, retrieve episode context, fetch screenshots, and generate meme images from supported TV shows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs an npm package through npx, and the package is not pinned in the artifact configuration.

Mitigation: Pin @ryantenney/frinkiac-mcp to a reviewed version and run it with least privilege before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryantenney/skills/frinkiac)
- [Publisher profile](https://clawhub.ai/user/ryantenney)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Text, Markdown]

**Output Format:** [Markdown with MCP tool calls, JSON configuration, scene metadata, image URLs, and generated meme or screenshot results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npx; uses the @ryantenney/frinkiac-mcp package through an MCP server.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
