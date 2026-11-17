## Description:

This is a simple skill for article recording, collect URLs as article, and provide users with query, delete, and other capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to save article URLs, list saved article records, and delete saved entries. It is especially oriented toward collecting WeChat article URLs with fetched page-title summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a browser to navigate to arbitrary URLs from the agent environment.

Mitigation: Avoid internal, localhost, private-network, authenticated, or sensitive URLs unless an allowlist and review process are in place.

Risk: Saved article records persist under the user's home directory.

Mitigation: Treat saved URLs and summaries as local user data and review or delete sensitive records before sharing the environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [CLI text with JSON article records and agent-formatted Markdown links for lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists article records in a local JSON file under the user's home directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
