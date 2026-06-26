## Description: <br>
Summarize recent emails, generate a thematic image, and send a formatted HTML email report with the summary and image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxfz3](https://clawhub.ai/user/matthewxfz3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn recent Gmail messages matching a query into a concise email digest with a generated image and formatted HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow reads Gmail content and sends email automatically, which can expose confidential messages or send a digest to unintended recipients. <br>
Mitigation: Use only trusted Gmail accounts and recipient lists, keep Gmail queries narrow, and add a dry-run or confirmation step before sending confidential digests. <br>
Risk: The current summarizer uses a canned placeholder summary that may not reflect the retrieved email content. <br>
Mitigation: Treat generated summaries as unreliable until content-based summarization is implemented and review the digest before sending. <br>


## Reference(s): <br>
- [Email Filters Reference](references/email-filters.md) <br>
- [HTML Email Template](references/html-template.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/matthewxfz3/email-news-digest) <br>
- [Publisher Profile](https://clawhub.ai/user/matthewxfz3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated artifacts include JSON summary data, HTML email content, and an attached image.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The digest workflow accepts a recipient list, Gmail search query, and image prompt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
