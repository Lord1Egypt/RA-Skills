## Description: <br>
This is a simple skill for article recording, collect URLs as article, and provide users with query, delete, and other capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect article URLs, fetch page-title summaries for supported article pages, list saved records, and delete selected saved entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opening user-provided URLs can expose private, internal, or sensitive links through browser access. <br>
Mitigation: Only provide URLs that are acceptable to open in the agent environment, and avoid private or sensitive URLs. <br>
Risk: Saved article URLs create local browsing-history records. <br>
Mitigation: Review stored article records periodically and delete entries that should not be retained. <br>
Risk: Deleting by list number can remove the wrong saved article if the target item is unclear. <br>
Mitigation: List articles first and confirm the intended item number before deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bondli/article-collect) <br>
- [Publisher profile](https://clawhub.ai/user/bondli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-formatted article records when listing saved articles.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
