## Description:

Byted Kickart Subtitle Extractor helps an agent upload a local MP4 or MOV video, extract existing subtitles from it, and return subtitle results as JSON with optional SRT generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract subtitles from supported video files and receive structured subtitle data. It is suited for workflows that need video subtitle recognition, subtitle export, or conversion of extracted subtitle timing into SRT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may be exposed if long-lived AK/SK values are pasted into chat or captured in local logs.

Mitigation: Use least-privilege, short-lived credentials through environment or secret management, avoid pasting long-lived secrets into chat, and rotate any credential that may have been exposed.

Risk: Local logs under /tmp/openclaw may contain authorization headers, request data, response data, or media metadata.

Mitigation: Restrict access to the log directory, avoid sharing logs without redaction, and remove logs after the task when retention is not required.

Risk: The self-update path can run a server-provided install command.

Mitigation: Avoid automatic self-update execution; review and scan any new release before installing it.

Risk: Video processing uploads user-provided media to external Volcengine services.

Mitigation: Use only media approved for upload to that service and avoid sensitive or personal content unless the deployment's data-handling requirements permit it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-kickart-subtitle-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands; subtitle results are saved as JSON and may be converted to SRT text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow validates credentials and package access, uploads a supported video, polls for extraction completion, and writes the subtitle result to a local JSON file.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
