## Description:

Provides an MCP-based service for searching and looking up Chinese Magic: The Gathering card information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Magic: The Gathering cards, sets, set card lists, and card-image sentence composition through the XiaoBenYang API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and stores it in a local plaintext .env file.

Mitigation: Use a disposable or limited-scope API key, keep .env out of version control, and rotate the key if exposure is suspected.

Risk: Card queries and the API key are sent to the XiaoBenYang API.

Mitigation: Use the skill only when sending those queries and credentials to XiaoBenYang is acceptable.

Risk: The artifact contains mismatched leftover school-search documentation, which may confuse reviewers or users.

Mitigation: Review the documented workflow and tool behavior before installing or relying on the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alinklab/skills/gathering-card-lookup-service)
- [XiaoBenYang](https://xiaobenyang.com)
- [XiaoBenYang MCP API](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown summaries of JSON API results, with configuration guidance when an API key is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key for live API lookups.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
