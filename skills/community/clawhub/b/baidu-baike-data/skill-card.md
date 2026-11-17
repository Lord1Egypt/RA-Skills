## Description:

The Baidu Baike Component queries Baidu Baike for standardized encyclopedia explanations of user-provided nouns such as objects, people, places, concepts, and events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ide-rea](https://clawhub.ai/user/ide-rea)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve Baidu Baike entries by title or entry ID, including homonym lists when a term has multiple matching entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Baidu API key.

Mitigation: Use a scoped key, store it through the agent's normal secret handling, and rotate it if it may have been exposed.

Risk: Search terms are sent to Baidu's AppBuilder Baike service.

Mitigation: Avoid submitting private, confidential, or sensitive terms unless that disclosure is acceptable for the deployment.

## Reference(s):

- [Baidu Baike](https://baike.baidu.com/)
- [Baidu AppBuilder Baike endpoint](https://appbuilder.baidu.com/v2/baike)
- [ClawHub skill page](https://clawhub.ai/ide-rea/skills/baidu-baike-data)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [JSON returned by the query script, typically summarized for the user as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; searched terms are sent to Baidu's AppBuilder Baike service.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
