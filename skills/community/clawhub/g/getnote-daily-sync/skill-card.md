## Description: <br>
Syncs the user's daily Get笔记 notes, recordings, meetings, and to-dos into a structured Notion daily report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phoenixyy](https://clawhub.ai/user/phoenixyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to pull their daily Get笔记 content, organize meeting notes, recordings, inspirations, and follow-up tasks, and write the result to a configured Notion database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill copies sensitive daily Get笔记 content into the configured Notion database. <br>
Mitigation: Use a Notion integration limited to the intended database, verify the database ID before running, protect API tokens, and enable scheduled syncing only when daily automatic transfer is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phoenixyy/getnote-daily-sync) <br>
- [Notion integration setup](https://developers.notion.com/docs/create-a-notion-integration) <br>
- [Get笔记 Open API resource endpoint](https://openapi.biji.com/open/api/v1/resource) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with environment-variable configuration and script execution output; generated daily report content is written to Notion.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Get笔记 and Notion credentials, a target Notion database ID, and optional MY_NAME filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
