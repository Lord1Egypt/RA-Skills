## Description:

伴奏提取器从 YouTube 或本地音频中分离人声和伴奏，帮助用户生成卡拉 OK 伴奏、纯伴奏音频和可选人声轨道。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gycdsj](https://clawhub.ai/user/gycdsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill through OpenClaw to provide a song name, YouTube link, or local audio file and receive separated accompaniment and optional vocal tracks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default YouTube download path gives yt-dlp access to the user's Chrome login cookies without a separate opt-in.

Mitigation: Prefer local-file mode when possible; for YouTube downloads, use an isolated browser profile, a reviewed cookies file, or a modified script that requests explicit consent before using browser cookies.

Risk: Dependency installation and optional Deno setup can affect the user's local Python and shell environment.

Mitigation: Install dependencies in a dedicated virtual environment and avoid curl-to-shell installation patterns unless the installer has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gycdsj/skills/accompaniment-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/gycdsj)
- [Spleeter source separation project](https://github.com/deezer/spleeter)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Guidance]

**Output Format:** [Audio files with optional JSON status output and human-readable command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs accompaniment and optional vocal tracks to the configured local output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
