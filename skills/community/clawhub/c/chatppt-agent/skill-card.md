## Description:

Uses the ChatPPT CLI to generate PowerPoint presentations from a topic or from Word, PDF, Markdown, or text files, including login, generation, import, polling, download, and editor-link workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kahn520](https://clawhub.ai/user/kahn520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to drive ChatPPT CLI workflows that turn prompts or existing documents into PPT presentations and retrieve finished results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation and CLI execution can affect the local environment.

Mitigation: Install and run the CLI in a restricted or disposable environment and avoid elevated npm installs unless explicitly required.

Risk: Document-import workflows upload local content to the ChatPPT/Baidu BOS-backed service.

Mitigation: Do not upload confidential documents unless the user is comfortable sending their contents to that service.

Risk: Authentication and storage configuration can expose AK/SK values, passwords, tokens, or raw auth config if logged or pasted.

Mitigation: Avoid displaying or storing raw credential material in chat logs, command output, or shared artifacts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent guidance; generated PPT files and links are produced by the ChatPPT service.]

## Skill Version(s):

1.0.4 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
