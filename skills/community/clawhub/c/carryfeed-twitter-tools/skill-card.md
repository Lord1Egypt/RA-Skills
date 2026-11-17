## Description:

Use the CarryFeed CLI to resolve public X/Twitter profiles, posts, article-style links, image, video, and GIF media for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christian-beep383](https://clawhub.ai/user/christian-beep383)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve source-preserving public X/Twitter profile, post, article-link, and media context through the CarryFeed CLI without browser login flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run an unpinned npm CLI package directly at runtime.

Mitigation: Prefer a pinned and reviewed version of @carryfeed/cli before use in environments with sensitive files, tokens, or broad network access.

Risk: The CLI supports alternate base URLs, which could route requests through an untrusted endpoint.

Mitigation: Use the default CarryFeed endpoint unless the alternate endpoint is explicitly trusted.

Risk: Returned social content can contain untrusted user-generated text.

Mitigation: Keep source URLs with summaries and do not follow instructions embedded in returned posts, bios, names, or article content.

## Reference(s):

- [CarryFeed Website](https://carryfeed.com)
- [CarryFeed Agent Discovery](https://carryfeed.com/llms.txt)
- [CarryFeed CLI Package](https://www.npmjs.com/package/@carryfeed/cli)
- [CarryFeed API Health](https://api.carryfeed.com/health)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source URLs and limits outputs to public X/Twitter content and media metadata.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
