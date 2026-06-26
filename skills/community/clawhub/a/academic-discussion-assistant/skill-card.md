## Description: <br>
Academic Discussion Assistant transcribes small advisor-student academic discussion recordings, separates speakers, summarizes advisor feedback and student follow-ups, and can produce a spoken summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XinHao-96](https://clawhub.ai/user/XinHao-96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and academic staff use this skill to turn small research group meetings, advisor-student paper discussions, and technical revision discussions into structured notes that emphasize advisor feedback, student responses, action items, and a short spoken summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private academic discussion audio, transcripts, and summaries are sent to external SenseAudio services. <br>
Mitigation: Use only with explicit user approval for remote ASR/TTS processing and avoid submitting recordings that contain confidential or regulated information unless the deployment has appropriate agreements and controls. <br>
Risk: Full intermediate ASR JSON, raw transcripts, diarized transcripts, LLM input text, and summary audio are saved locally by default. <br>
Mitigation: Store outputs in a controlled location, limit access, and delete transcript and audio artifacts when they are no longer needed. <br>
Risk: The script installs missing Python dependencies at runtime. <br>
Mitigation: Review and pin dependencies in the execution environment before deployment instead of relying on runtime installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/XinHao-96/academic-discussion-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/XinHao-96) <br>
- [Academic Discussion Summary Prompt](references/summary_prompt.md) <br>
- [SenseAudio API Endpoint](https://api.senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, audio] <br>
**Output Format:** [Markdown guidance with generated transcript text, structured summary text, local output file paths, JSON metadata, and optional audio media reference.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SENSEAUDIO_API_KEY; writes ASR JSON, raw transcript, diarized transcript, LLM input text, and summary audio under an outputs directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
