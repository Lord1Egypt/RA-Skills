## Description:

Web search using curl + multiple search engines (Baidu, Google, Bing, DuckDuckGo). Activates when user asks to search, look up, or query something online. Includes security enhancements: input sanitization, command injection protection, and URL encoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluejoy34](https://clawhub.ai/user/bluejoy34)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform public web searches through curl when a dedicated search API is unavailable. It supports Baidu, Google, Bing, and DuckDuckGo with configurable engine and result-count options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to public search engines, and the default Baidu search path uses plaintext HTTP.

Mitigation: Avoid private or proprietary queries, and set SEARCH_ENGINE to an HTTPS-backed engine when appropriate.

Risk: Broad activation for search or lookup requests can unintentionally send sensitive text outside the local environment.

Mitigation: Add explicit confirmation or narrower privacy guidance before external searches involving credentials, internal URLs, incident details, or proprietary text.

## Reference(s):

- [ClawHub curl-search skill page](https://clawhub.ai/bluejoy34/skills/curlsearch)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text search output with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; result count is bounded from 1 to 50 by CLI option or MAX_RESULTS.]

## Skill Version(s):

2.0.0 (source: release evidence, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
