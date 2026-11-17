## Description:

This skill helps an agent search, retrieve, and manage locally indexed files through the Gety CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujfsd](https://clawhub.ai/user/lujfsd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need to locate local documents by file name, content, file type, date range, or connector scope, then optionally retrieve full document content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and document retrieval can expose private local content that has been indexed by Gety.

Mitigation: Confirm the user's intent and indexed scope before searching, and present only the file details or excerpts needed for the request.

Risk: Adding or removing connectors changes what local folders Gety indexes for future searches.

Mitigation: Before connector changes, ask the user to confirm the exact folder path or connector ID and explain that the indexed content scope will change.

Risk: Gety CLI failures can lead to incomplete or misleading search guidance.

Mitigation: Check command exit codes and handle not-running, quota, invalid-argument, and general-error cases using the skill's documented responses.

## Reference(s):

- [Gety CLI Reference](references/gety_cli.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON-producing CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results should include file names, locations, and brief matched-content descriptions when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
