## Description:

Chanjing Video Compose helps agents use Chanjing video synthesis APIs to list digital human figures, create text- or audio-driven videos, poll task status, and download completed videos when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzn1018](https://clawhub.ai/user/iamzn1018)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compose Chanjing digital-human videos from scripts or uploaded audio, select public or customized figures, monitor generation tasks, and save completed results on request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Chanjing app credentials and access tokens in ~/.chanjing/credentials.json or a CHANJING_CONFIG_DIR override.

Mitigation: Use a private configuration directory, avoid shared machines, restrict file permissions, and never commit credentials.json.

Risk: CHANJING_API_BASE can redirect API calls to a non-default endpoint.

Mitigation: Set CHANJING_API_BASE only to endpoints you fully trust.

Risk: Callback URLs and media URLs cross a trust boundary and may receive or provide task-result payloads.

Mitigation: Use only trusted callback endpoints and verify media URLs before requesting or downloading content.

Risk: Custom download output paths can overwrite local files.

Mitigation: Choose output paths deliberately and review existing files before saving generated videos.

## Reference(s):

- [Chanjing API documentation](https://doc.chanjing.cc)
- [ClawHub skill page](https://clawhub.ai/iamzn1018/skills/chanjing-video-compose)
- [reference.md](artifact/reference.md)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text task IDs, file IDs, URLs, or local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Chanjing task IDs, uploaded file IDs, video URLs, or a saved video path.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
