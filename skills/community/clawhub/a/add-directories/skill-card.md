## Description:

Adds new AI/startup directories to directories.json from a URL, pasted text, or GitHub awesome-list by parsing, deduplicating, appending entries, and running analysis, cleanup, and browser verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[man0l](https://clawhub.ai/user/man0l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and growth teams use this skill to add AI or startup directory records from URLs, pasted text, or GitHub awesome-lists, then deduplicate, append, classify, and verify those records in a local directory dataset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes submission workflows even though its summary says submission is out of scope.

Mitigation: Limit use to parsing, deduplication, appending, classification, and verification unless the submission sections are removed or split into an explicitly authorized submission skill.

Risk: Submission workflows may upload files, use OAuth sessions, create GitHub pull requests, or store credentials in project JSON.

Mitigation: Require per-site review and explicit approval before any submission action; do not store real passwords, OAuth session data, or personal credentials in project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/man0l/skills/add-directories)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local JSON files and run local analysis, cleanup, browser verification, form discovery, and submission scripts when present in the target project.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
