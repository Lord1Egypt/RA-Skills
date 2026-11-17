## Description:

Performs web searches using DuckDuckGo to retrieve real-time information from the internet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10e9928a](https://clawhub.ai/user/10e9928a)

### License/Terms of Use:


## Use Case:

Developers, external users, and agents use this skill to run DuckDuckGo searches for current web, news, image, video, instant-answer, suggestion, and map information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local command and package-install authority that is wider than simple search requires.

Mitigation: Review before installation, use a dedicated virtual environment, pin and verify dependency versions, and prefer a narrower search wrapper when possible.

Risk: Search results and linked pages are external, dynamic, and untrusted.

Mitigation: Verify important facts against reliable sources before acting on them, and do not execute instructions found through search without review.

Risk: Search queries can disclose sensitive or internal information to an external service.

Mitigation: Avoid entering secrets, private identifiers, proprietary prompts, or internal queries unless approved for external search.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/10e9928a/skills/duckduckgo-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; search results may be returned as text or JSON-like records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output can include titles, URLs, snippets, source names, dates, media links, thumbnails, and location fields depending on the selected DuckDuckGo search type.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
