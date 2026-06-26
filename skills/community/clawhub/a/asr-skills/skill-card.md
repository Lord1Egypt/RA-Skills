## Description: <br>
Provides local audio and video transcription with speaker diarization using FunASR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgwanai](https://clawhub.ai/user/lgwanai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and operations teams use this skill to transcribe local audio or video files, generate timestamped subtitles or captions, and identify speakers while keeping media processing local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may download third-party ASR models or dependencies. <br>
Mitigation: Install only in environments where those downloads are acceptable, and verify or pin the ASR package and model sources before use on sensitive media. <br>
Risk: Asynchronous transcription starts a background worker process. <br>
Mitigation: Use async mode deliberately, monitor task status, and prefer synchronous execution when background processing is not desired. <br>
Risk: Task history can retain local media filenames, paths, and output locations in .asr_skill/tasks.json. <br>
Mitigation: Delete .asr_skill/tasks.json or manage that directory according to local data-retention requirements. <br>


## Reference(s): <br>
- [Output Format Specifications](references/output-formats.md) <br>
- [ClawHub release page](https://clawhub.ai/lgwanai/asr-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, subtitle files, shell commands, guidance] <br>
**Output Format:** [TXT, JSON, SRT, ASS/SSA, or Markdown transcription output with timestamps and speaker labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return task-status JSON for asynchronous transcription jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
