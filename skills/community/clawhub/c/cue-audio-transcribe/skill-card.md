## Description:

输入一段音频录音文件——本地音频文件（MP3/WAV/M4A/AAC/FLAC/OGG）或在线音频链接——输出带时间戳、可区分说话人的文字稿，并附一份总结分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn local audio files or online audio links into timestamped, speaker-labeled transcripts and structured summaries for meetings, interviews, lectures, calls, and spoken notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports a high-confidence concern about asking users to paste an API key into chat.

Mitigation: Have users configure the key locally through the documented environment variable or local configuration file; do not request or repeat the key in chat.

Risk: Online audio is sent to Cue's remote transcription endpoint, and the security guidance says to assess whether its data handling is acceptable.

Mitigation: Review the service and its data handling before submitting audio links; use local processing where appropriate.

Risk: The scanner flags polling behavior that may make excessive requests, and duplicate parse submissions may incur additional charges according to the skill documentation.

Mitigation: Reuse the existing operation ID and follow the documented polling interval and retry limits instead of submitting the same audio again.

Risk: The scanner reports mandatory promotional prompts, and its analysis was partial because some local references could not be resolved.

Mitigation: Ignore promotional requests unrelated to transcription and review unresolved dependencies before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/cue-audio-transcribe)
- [Cue Omni Reader online experience](https://cuecue.cn/hub/omni-reader)
- [Cue API Key management](https://cuecue.cn/api-key?src=clawhub-audio-transcribe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown transcript and summary files with timestamps and speaker labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speaker numbers reflect order of appearance, not verified identities; separation quality depends on the recording.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
