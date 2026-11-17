## Description:

AWS Black Belt服务 helps agents search AWS Black Belt online seminars by keyword and retrieve Japanese video transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search AWS Black Belt seminar listings and retrieve transcript text for supported YouTube seminar videos. It is useful when an agent needs AWS seminar references, publication metadata, PDF links, video links, or Japanese transcript content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a third-party API key and sends requests through xiaobenyang.com.

Mitigation: Use the skill only when that service is trusted, prefer a disposable or least-privilege key, and avoid sending sensitive queries.

Risk: The API key may be saved in a local plaintext .env file.

Mitigation: Use environment-based secret injection where possible, restrict file access, and rotate or revoke keys after evaluation.

Risk: The package includes stale unrelated Gaokao references and broad XiaoBenYang wrapper code.

Mitigation: Review the bundled files before deployment and confirm the installed behavior is limited to the AWS Black Belt search and transcript tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/aws-blackbelt)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration guidance]

**Output Format:** [Markdown or structured text summarizing API-returned JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include seminar titles, dates, PDF links, YouTube links, and Japanese transcript text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
