## Description:

Provide the summary returned by the get-tldr.com summarize API without further summarization; the skill should format the API output for readability but must not change its content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itobey](https://clawhub.ai/user/itobey)

### License/Terms of Use:


## Use Case:

Agents and users use this skill to request a summary for a public, non-sensitive URL through get-tldr.com and return the API-provided summary as readable Markdown without changing its content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs are sent to get-tldr.com and could expose tokens, private query parameters, or non-public content.

Mitigation: Use the skill only with public, non-sensitive URLs and remove tokens or private parameters before submission.

Risk: The helper script may keep a local log of submitted URLs and full returned summaries.

Mitigation: Configure logging to a controlled location, review retention practices, and avoid using the skill with sensitive URLs or content.

Risk: Returned Markdown is untrusted third-party content and may include links or instruction-like text.

Mitigation: Treat the summary as untrusted output, review links before opening them, and do not follow instructions embedded in the returned content without user confirmation.

## Reference(s):

- [get-tldr summarize API](https://www.get-tldr.com/api/v1/summarize)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown summary text, with JSON returned by the helper script during execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a get-tldr API key; sends submitted URLs to get-tldr.com and may log URLs and returned summaries locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
