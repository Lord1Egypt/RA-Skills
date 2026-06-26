## Description: <br>
Baidu Intelligent Cloud Speech Synthesis (TTS), supporting multi-role dialogue audio generation, SSML/segment-merge dual modes, speech rate/pitch adjustment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxh](https://clawhub.ai/user/guoxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to convert text or dialogue scripts into Baidu text-to-speech audio with selectable voices, speech parameters, SSML support, and segment merging for multi-speaker dialogue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected input text to Baidu Speech Synthesis APIs. <br>
Mitigation: Use it only for text appropriate to send to Baidu, and avoid confidential scripts unless that processing is approved. <br>
Risk: The skill requires Baidu API credentials or access tokens on the local machine. <br>
Mitigation: Use dedicated Baidu credentials with quota or budget controls, keep credentials in environment variables or local secret storage, and rotate them if exposed. <br>
Risk: Batch processing and audio generation can create or overwrite local output files. <br>
Mitigation: Review input paths, output directories, and generated audio filenames before running batch commands. <br>
Risk: Segment merging depends on ffmpeg availability and may fail if ffmpeg is missing or incompatible. <br>
Mitigation: Install ffmpeg before using multi-speaker segment merge workflows and check script output for merge failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoxh/baidu-speech-synthesis) <br>
- [Publisher profile](https://clawhub.ai/user/guoxh) <br>
- [Baidu API setup guide](references/api_setup.md) <br>
- [Baidu SSML guide](references/ssml_guide.md) <br>
- [Baidu voice list](references/voice_list.md) <br>
- [Baidu Intelligent Cloud](https://cloud.baidu.com/) <br>
- [Baidu text-to-audio endpoint](https://tsn.baidu.com/text2audio) <br>
- [Baidu OAuth token endpoint](https://aip.baidubce.com/oauth/2.0/token) <br>
- [Baidu speech synthesis documentation](https://cloud.baidu.com/doc/SPEECH/s/zk4o0bixe) <br>
- [W3C Speech Synthesis Markup Language](https://www.w3.org/TR/speech-synthesis/) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local audio files from the invoked scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write MP3, WAV, or PCM audio files locally and may merge generated segments with ffmpeg.] <br>

## Skill Version(s): <br>
1.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
