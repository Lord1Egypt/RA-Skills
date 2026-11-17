## Description:

Dandan Multi Search helps agents compose multi-engine search workflows across 17 domestic and international search engines, including privacy-oriented, academic, code, medical, and WolframAlpha knowledge queries, without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realorange1994](https://clawhub.ai/user/realorange1994)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent in selecting suitable search engines, constructing advanced search queries, and summarizing results with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command examples can unsafe-handle search text.

Mitigation: URL-encode queries and revise command examples so untrusted query text is not interpolated into shell commands.

Risk: Broad user queries may be sent to external services without enough control.

Mitigation: Avoid using secrets, credentials, personal data, or sensitive business information in search queries, and confirm before searching when a request is ambiguous or sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realorange1994/skills/dandan-multi-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown search-result summaries with source links and inline shell or PowerShell commands when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include engine coverage, main findings, deeper sources, WolframAlpha notes, and original search links.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
