## Description:

AnyLink to Note converts shared links from WeChat articles, Get note links, RSS or podcast feeds, and public webpages into structured notes with title, content, summary, tags, source name, and URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanxlab](https://clawhub.ai/user/fanxlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to save, parse, summarize, or collect a shared URL as a structured note. It is intended for public web, WeChat, Get note, and RSS or podcast links that the user is comfortable processing through the documented extraction services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, internal, or tokenized links may be exposed to third-party extraction services during link processing.

Mitigation: Use the skill only with links approved for third-party processing, and avoid private, internal, authenticated, or token-bearing URLs.

Risk: Raw user-provided URLs in documented shell commands could lead to unintended local command execution if handled unsafely.

Mitigation: Validate URLs before use and pass them with argument-safe execution instead of shell interpolation.

Risk: Broad network fetching may retrieve unexpected or blocked content from public webpages.

Mitigation: Review extracted content before relying on it, and restrict accepted URL schemes and domains where the deployment context requires tighter control.

## Reference(s):

- [Supported URL Types](references/url-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured note fields with Markdown guidance, JSON examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces title, content, summary, tags, sourceName, and url fields for extracted links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
