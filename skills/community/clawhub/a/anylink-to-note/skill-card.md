## Description: <br>
Turns public links into structured notes for WeChat articles, Get note shares, RSS podcasts, and general web pages, returning a title, content, short summary, tags, source name, and original URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanxlab](https://clawhub.ai/user/fanxlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert user-supplied public links into structured notes for saving, summarizing, and tagging source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided URLs through third-party or local tooling, so private, internal, localhost, metadata-service, or token-bearing URLs could expose sensitive content. <br>
Mitigation: Use only public links that are acceptable to fetch externally or locally; avoid private documents, internal network URLs, localhost links, cloud metadata endpoints, and URLs containing access tokens. <br>
Risk: Some pages may require login, heavy JavaScript rendering, or block Jina Reader, which can produce incomplete or failed extraction. <br>
Mitigation: Check extracted content before relying on the note; use the documented Playwright fallback for supported Get note links when Jina Reader is insufficient. <br>


## Reference(s): <br>
- [Supported URL Types](references/url-types.md) <br>
- [AnyLink to Note on ClawHub](https://clawhub.ai/fanxlab/anylink-to-note) <br>
- [Jina Reader Endpoint](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON object with title, content, summary, tags, sourceName, and url; may include Markdown summaries and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public URLs with Jina Reader, Playwright, or RSS parsing depending on URL type.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
