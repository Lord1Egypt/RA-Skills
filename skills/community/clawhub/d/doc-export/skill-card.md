## Description: <br>
Exports solution documents from conversations as Markdown and publishes them to a configured web server for download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binyuli](https://clawhub.ai/user/binyuli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask the agent to turn an in-progress troubleshooting or setup conversation into a downloadable Markdown solution document with background, steps, examples, and common issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived documents may become publicly reachable when published to the configured website. <br>
Mitigation: Show the document, filename, and URL before publishing, and remove secrets or private details from the content. <br>
Risk: Published and archived documents may remain available after the user downloads them. <br>
Mitigation: Ask the agent to delete the public copy and any archived local copy when the document is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown document, public download link, and cleanup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes generated documents to a configured HTTPS web directory and retains a local archive unless cleanup is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
