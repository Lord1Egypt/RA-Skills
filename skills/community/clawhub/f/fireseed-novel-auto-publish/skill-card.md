## Description:

Publishes novels to the fireseed.online platform by helping an agent authenticate, create a novel, generate chapters, publish chapters, and optionally upload a cover through HTTP APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanzhishuyuan](https://clawhub.ai/user/sanzhishuyuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to have an agent draft serialized fiction and publish it to FireSeed. It is intended for workflows that create or update public-facing novel content through the FireSeed API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish generated content externally to fireseed.online.

Mitigation: Require manual confirmation and content review before publication, deletion, or cover upload actions.

Risk: The skill can create or use a FireSeed account and store a reusable token.

Mitigation: Avoid saving credentials unless necessary, protect the token from logs or chat output, and rotate it when it is no longer needed.

## Reference(s):

- [FireSeed Platform](https://fireseed.online)
- [ClawHub Skill Page](https://clawhub.ai/sanzhishuyuan/skills/fireseed-novel-auto-publish)
- [FireSeed API Guide](references/api-guide.md)
- [Novel Template](resources/novel-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown narrative content, HTTP request guidance, configuration commands, and publication status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary Markdown files, store a reusable FireSeed token, and publish generated content to fireseed.online.]

## Skill Version(s):

3.5.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
