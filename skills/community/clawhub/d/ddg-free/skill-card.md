## Description:

Provides free Bing-backed web search results without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ipdoctor961051-cyber](https://clawhub.ai/user/ipdoctor961051-cyber)

### License/Terms of Use:


## Use Case:

Agents and users use this skill to search the web for current information, documents, and general research material, then consume structured result summaries for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Bing.

Mitigation: Avoid submitting secrets, private documents, sensitive personal details, or confidential business information as search queries.

Risk: The documented command path is author-local and may not match the installed path.

Mitigation: Adjust the command path to the installed artifact location before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ipdoctor961051-cyber/skills/ddg-free)
- [Bing Search](https://www.bing.com)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON object containing the original query and an array of result titles, URLs, and snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count is controlled by the max-results argument; network access to Bing is required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
