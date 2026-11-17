## Description:

Remove hardcoded video subtitles, watermarks from short-video share links, and image watermarks or unwanted text with the 550W Open API; check processing tasks and credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinehu](https://clawhub.ai/user/sunshinehu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to remove subtitles or watermarks from selected videos, public share links, and images, and to check processing tasks and account credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media files or public links are sent to the 550W Open API for processing.

Mitigation: Use only media or links explicitly selected by the user and disclose the remote processing step before the first media operation.

Risk: Credentials may be stored locally for authenticated API requests.

Mitigation: Use connector or environment secret storage when available and avoid repeating complete API keys in chat or logs.

Risk: Deleting a subtitle task can clean up related remote media and does not refund credits.

Mitigation: Allow deletion only through a host workflow that asks for explicit confirmation immediately before the destructive action.

## Reference(s):

- [API contract](references/api-contract.md)
- [Agent compatibility](references/agent-compatibility.md)
- [550W Open API credential page](https://eraser.550wai.com/api/)
- [ClawHub skill page](https://clawhub.ai/sunshinehu/skills/550w-ai-subtitle-remover)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration]

**Output Format:** [Markdown and JSON-like tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task IDs, status messages, credit balances, result URLs, and actionable errors.]

## Skill Version(s):

2.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
