## Description:

Transcribes audio and video files with Whisper and can produce plain text, SRT/VTT subtitles, or JSON output for meetings, videos, interviews, and podcasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan830826](https://clawhub.ai/user/ivan830826)

### License/Terms of Use:


## Use Case:

Developers, content teams, and other external users can use this skill to convert local audio or video recordings into transcripts, subtitles, or structured JSON for editing, review, accessibility, and downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings and generated transcripts may contain confidential or personal information.

Mitigation: Process only authorized media and handle transcript, subtitle, JSON, and temporary audio files according to applicable data-handling requirements.

Risk: Video audio extraction uses a predictable /tmp/audio_extract.wav path, which can expose or overwrite temporary audio on shared machines, especially when --keep-audio is used.

Mitigation: Run the skill in an isolated workspace or change the extraction workflow to use a unique temporary file path before processing video on shared systems.

Risk: Dependency installation can affect the host environment if run globally or as root.

Mitigation: Install Python dependencies in a virtual environment and avoid root-level package installation unless it is operationally required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivan830826/skills/audio-video-to-text)
- [OpenAI Whisper documentation](https://github.com/openai/whisper)
- [FFmpeg documentation](https://ffmpeg.org/documentation.html)
- [ISO 639-1 language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, SRT, VTT, or JSON files, with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports selectable Whisper model size, optional language code, CPU or CUDA execution, and optional retention of extracted audio.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
