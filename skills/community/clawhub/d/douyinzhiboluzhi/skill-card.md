## Description:

从本地直播录屏中自动识别高光时刻并切割为短视频片段，可按音频能量、场景变化、音画组合或 ASR 关键词分析，并可生成合并版视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juzanxie-dev](https://clawhub.ai/user/juzanxie-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, livestream operators, and developers use this skill to turn local livestream recordings into reusable highlight clips for review or secondary distribution. It is suited to extracting emotional peaks, scene-change-heavy moments, and e-commerce keyword moments from replay content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local video files and optional ASR file paths supplied by the user.

Mitigation: Run it only on media and transcripts you are comfortable processing in the local environment.

Risk: The selected output directory may receive or overwrite clips, segments.json, concat_list.txt, or merged_highlights.mp4.

Mitigation: Use a fresh output directory for each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juzanxie-dev/skills/douyinzhiboluzhi)
- [Publisher profile](https://clawhub.ai/user/juzanxie-dev)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; generated runtime artifacts are MP4 files and JSON metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local absolute video paths, ffmpeg/ffprobe, and Python dependencies; can optionally consume an ASR JSON or text file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
