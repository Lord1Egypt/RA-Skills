## Description:

Use when the user wants to extract spoken text from a Douyin video link and produce a corrected, readable Chinese transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao2769433](https://clawhub.ai/user/xiao2769433)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn public Douyin video links into Chinese transcript documents. It extracts raw speech, has the agent correct recognition errors, segments the text for readability, and summarizes the main ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to run a local Python extractor from a hard-coded path.

Mitigation: Review the local extractor before installation or execution, and only run it from a trusted skill directory.

Risk: Browser-cookie options may expose logged-in session access.

Mitigation: Avoid browser-cookie options unless the user understands the access being granted; prefer no-cookie or dedicated cookie-file flows when possible.

Risk: Generated transcripts and video metadata are saved locally.

Mitigation: Store outputs in an appropriate local directory and remove transcript files that contain sensitive or unwanted content.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/xiao2769433/douyin-text)
- [ClawHub skill page](https://clawhub.ai/xiao2769433/skills/douyin-text)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown document plus concise text response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated document preserves the raw transcript, adds a corrected and segmented transcript, and includes 3-5 key takeaways.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
