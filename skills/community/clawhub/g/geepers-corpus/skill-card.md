## Description:

Query the COCA (Corpus of Contemporary American English) linguistics API for word frequency, collocations, concordances, and historical usage trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukeslp](https://clawhub.ai/user/lukeslp)

### License/Terms of Use:


## Use Case:

Writers, linguists, and developers use this skill to query the COCA corpus API for American English concordance examples, collocations, word frequency, genre filters, and historical usage trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searched words, query parameters, and the configured API key are sent to the documented external corpus API.

Mitigation: Avoid using the skill for sensitive private text unless the user trusts that service's handling of requests.

Risk: The skill depends on a DREAMER_API_KEY for authenticated API access.

Mitigation: Store the API key in the environment and avoid placing it in prompts, transcripts, or checked-in files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukeslp/skills/geepers-corpus)
- [Dreamer Corpus API](https://api.dr.eamer.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DREAMER_API_KEY and sends query terms and parameters to https://api.dr.eamer.dev.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
