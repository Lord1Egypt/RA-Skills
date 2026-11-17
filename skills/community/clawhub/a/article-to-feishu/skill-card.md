## Description:

Converts public web articles into Feishu cloud documents by fetching article content, downloading images, and guiding the agent to append text and insert images in order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mywaystay](https://clawhub.ai/user/mywaystay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to import public web articles into Feishu documents while preserving text and image order. It is intended for workflows such as saving article links, importing webpages, or converting supported Chinese content sites into editable Feishu documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches arbitrary article URLs and remote image URLs.

Mitigation: Use it only with public, non-sensitive URLs and apply URL allowlists or network restrictions before execution.

Risk: Downloaded remote files may be written into local temporary directories with weak scoping.

Mitigation: Use a unique private temporary directory, enforce download limits, and delete downloaded files after Feishu document creation is confirmed.

Risk: Article import may expose private or signed links to external fetchers or Feishu documents.

Mitigation: Avoid private, internal, or signed URLs and review the destination Feishu document before sharing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mywaystay/skills/article-to-feishu)
- [Publisher Profile](https://clawhub.ai/user/mywaystay)
- [Jina Reader Endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, API Calls, Files]

**Output Format:** [Markdown instructions with shell commands and Feishu tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces downloaded image files in a caller-provided temporary directory and guides the agent to create or update a Feishu document.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
