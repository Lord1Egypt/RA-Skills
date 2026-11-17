## Description:

Query and operate on Tencent Coding DevOps platform data for iterations, issues, defects, requirements, tasks, and team members, including creating requirements and defects with a CODING_TOKEN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyin717](https://clawhub.ai/user/wangyin717)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project operators use this skill to inspect Tencent Coding project iterations, issue lists, issue details, defect types, custom fields, and team members. The skill can also help create requirements or defects after validating the token, team, project identifier, and required project fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Tencent Coding personal access token and its instructions may lead users to expose that token in chat.

Mitigation: Provide CODING_TOKEN through a secret or environment mechanism, avoid pasting tokens into chat, use a narrowly scoped token, and rotate any token that may have been exposed.

Risk: The skill can create remote Tencent Coding requirements or defects.

Mitigation: Review create-issue details with the user before sending the request and confirm project identifiers, assignees, iteration codes, dates, labels, working hours, defect type, and custom fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyin717/skills/coding-net)
- [Publisher profile](https://clawhub.ai/user/wangyin717)
- [Tencent Coding Open API endpoint](https://e.coding.net/open-api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell code blocks, plus structured API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote Tencent Coding API calls that read project data or create issues when supplied with a valid token.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
