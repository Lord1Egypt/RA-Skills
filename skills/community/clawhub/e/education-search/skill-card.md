## Description:

Searches for Chinese academic and vocational exam resources, including exam papers, study aids, and preparation courses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kayy123](https://clawhub.ai/user/kayy123)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and exam-preparation users use this skill to find exam papers, study materials, and course resources for Chinese academic and professional certification exams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and host identifiers may be sent to Baidu over an unencrypted HTTP endpoint.

Mitigation: Use only non-sensitive queries and avoid environments where host or network identifiers are sensitive unless the endpoint is encrypted or otherwise controlled.

Risk: The skill asks users to provide an API key through chat for fallback search configuration.

Mitigation: Configure BAIDU_API_KEY through a managed secret or environment variable and do not paste credentials into chat.

Risk: The skill includes an automatic update path that can change installed behavior.

Mitigation: Disable automatic updates or require explicit review and approval before applying skill updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kayy123/skills/education-search)
- [Search API documentation](artifact/references/api.md)
- [Auto-update documentation](artifact/references/auto-update.md)
- [Baidu search configuration guide](artifact/references/baidu-search-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown tables with resource links and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches use up to three query variants; displayed results are filtered to resources with links and capped to keep responses readable.]

## Skill Version(s):

1.0.8 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
