## Description:

Searches a configured Volcengine Viking knowledge base for content relevant to a user-supplied query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to search a configured Viking knowledge base and return matching knowledge content for a user's request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API bearer key and user queries over plaintext HTTP.

Mitigation: Use only in an isolated environment and avoid sensitive queries until the transport is changed to HTTPS.

Risk: The skill depends on unpinned Python packages.

Mitigation: Pin and review dependency versions before deployment.

Risk: The skill requires live Viking knowledge base credentials.

Mitigation: Use least-privileged, rotating credentials and revoke them if logs or network traces may have exposed them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-viking-knowledgebase)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text search results with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Viking knowledge base credentials and a configured service ID before use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
