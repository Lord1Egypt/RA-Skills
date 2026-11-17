## Description:

Guides agents through creating mobile-compatible H5 mini games and uploading config.json, index.html, and preview.png through the Aigames custom API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianclan](https://clawhub.ai/user/brianclan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to package a simple browser game into the required configuration, HTML, and preview files and publish it to the Aigames/thenext.games flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploading game assets to the external service can disclose unintended secrets, private data, or local files.

Mitigation: Review config.json, index.html, and preview.png before upload and exclude credentials or private content.

Risk: Using overwrite=true through the general interface can destructively replace remote files.

Mitigation: Require explicit user approval before any overwrite-style update.

## Reference(s):

- [Aigames ClawHub Skill Page](https://clawhub.ai/brianclan/skills/aigames)
- [Aigames Upload API Base](https://www.idlab.top)
- [thenext.games Game URL Base](https://thenext.games)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces game asset requirements, upload commands, and final play URL guidance; does not bundle executable code.]

## Skill Version(s):

0.1.9 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
