## Description: <br>
BookStack provides a wiki and documentation API integration for creating, reading, updating, deleting, organizing, and searching books, chapters, pages, and shelves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenofex7](https://clawhub.ai/user/xenofex7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate BookStack documentation workflows, manage knowledge-base structure, and search wiki content from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete BookStack content using the configured API token. <br>
Mitigation: Use a least-privilege API token and review update or delete commands before running them against important documentation. <br>
Risk: BookStack API credentials are required for live operations. <br>
Mitigation: Keep BOOKSTACK_TOKEN_ID and BOOKSTACK_TOKEN_SECRET out of prompts, logs, screenshots, and repositories. <br>


## Reference(s): <br>
- [BookStack API documentation](https://demo.bookstackapp.com/api/docs) <br>
- [ClawHub BookStack skill page](https://clawhub.ai/xenofex7/bookstack) <br>
- [xenofex7 publisher profile](https://clawhub.ai/user/xenofex7) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOOKSTACK_URL, BOOKSTACK_TOKEN_ID, and BOOKSTACK_TOKEN_SECRET for live BookStack API operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
