## Description:

Respond to user requests for AIOZ Stream API. Use provided scripts to upload videos, fetch analytics, manage media, and create livestreams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[namle-aioz](https://clawhub.ai/user/namle-aioz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage AIOZ Stream media workflows, including video uploads, media search, livestream-key creation, account balance checks, and analytics reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires AIOZ Stream API keys that can read account and media data and create or upload resources.

Mitigation: Use narrowly scoped or temporary keys where available, inject them through protected environment variables, and avoid running the scripts on shared machines.

Risk: User-provided video titles, stream names, and search strings are passed into API requests.

Mitigation: Review untrusted inputs before execution and avoid using sensitive or attacker-controlled values until JSON construction and credential handling are hardened.

Risk: Script output can include account details, media identifiers, analytics data, and playback URLs.

Mitigation: Treat command output as sensitive, avoid sharing logs publicly, and return only the fields needed for the user's task.

## Reference(s):

- [AIOZ Stream API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/namle-aioz/skills/aioz-stream-toolkit)
- [Publisher Profile](https://clawhub.ai/user/namle-aioz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return media IDs, upload status, playback URLs, account data, analytics totals, and structured JSON from AIOZ Stream API calls.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
