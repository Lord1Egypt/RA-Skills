## Description:

Helps locate local files by searching common directories for a specified file name or partial name on Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fidods](https://clawhub.ai/user/fidods)

### License/Terms of Use:


## Use Case:

Users ask an agent to find local documents or other files by exact or partial name. The agent searches common local directories, reports matching paths, and offers follow-up actions such as opening the file, narrowing the search, or broadening the search scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-name searches may reveal private local file paths in the chat.

Mitigation: Search only locations needed for the request and avoid displaying paths the user would not want visible in the session.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with local file paths and brief follow-up options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May display local file names and paths; does not modify, delete, upload, or share files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
