## Description: <br>
BookStack API lets agents manage a BookStack wiki through REST API commands for searching, reading, creating, updating, and deleting books, chapters, pages, and shelves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f-liva](https://clawhub.ai/user/f-liva) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and documentation agents use this skill to search, read, publish, update, organize, and delete content in a configured BookStack knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update or delete live BookStack content. <br>
Mitigation: Use a dedicated least-privilege API token and require explicit confirmation before updates or deletions. <br>
Risk: Broad activation wording can cause an agent to act on vague requests about docs or a wiki. <br>
Mitigation: Confirm the target BookStack instance, resource type, and resource ID before making changes. <br>
Risk: Delete commands do not include built-in confirmation prompts. <br>
Mitigation: Restrict delete permissions unless they are needed and review proposed delete commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/f-liva/bookstack-api) <br>
- [Publisher profile](https://clawhub.ai/user/f-liva) <br>
- [BookStack API commands reference](artifact/references/api-commands.md) <br>
- [BookStack project site](https://www.bookstackapp.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with shell commands, BookStack resource summaries, API results, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOOKSTACK_URL, BOOKSTACK_TOKEN_ID, and BOOKSTACK_TOKEN_SECRET for API access; page content may be read or written as HTML or Markdown.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
