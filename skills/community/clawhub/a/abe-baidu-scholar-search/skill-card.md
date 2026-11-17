## Description:

Academic Literature Search Tool enables the retrieval of both Chinese and English literature, covering various types of literature such as academic journals, conference papers, and dissertations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to search Chinese and English academic literature by keyword through a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic search queries are sent to api.heybossai.com under the user's SkillBoss API key.

Mitigation: Avoid sending secrets or sensitive internal research topics as search queries.

Risk: The shell script interpolates the query into a JSON request body.

Mitigation: Prefer a fixed version that JSON-escapes the query before sending it.

## Reference(s):

- [Baidu Scholar](https://xueshu.baidu.com/)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)
- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-baidu-scholar-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SKILLBOSS_API_KEY; sends keyword queries to an external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
