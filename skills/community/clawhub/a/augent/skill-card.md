## Description: <br>
The audio & video layer for agents. 22 local MCP tools. No cloud, no API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[augentdevs](https://clawhub.ai/user/augentdevs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Augent to download, transcribe, search, summarize, clip, and organize audio and video content through local MCP tools. It is suited for workflows such as podcast review, meeting transcription, speaker labeling, semantic media search, note generation, clip export, visual frame extraction, Spaces recording, and text-to-speech output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Augent can download media, save notes and clips, and store transcription memory on the local machine. <br>
Mitigation: Configure the download, notes, and memory directories deliberately, and avoid processing sensitive recordings unless local transcript storage is acceptable. <br>
Risk: Twitter/X Spaces recording uses an optional local authentication token file. <br>
Mitigation: Create and configure the auth token only when Spaces recording is intended, and protect the token file as a credential. <br>
Risk: First use may download local ML models and media-processing dependencies. <br>
Mitigation: Install from trusted package sources and confirm required binaries such as ffmpeg, yt-dlp, and aria2c are expected in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Augent listing](https://clawhub.ai/augentdevs/augent) <br>
- [Augent documentation](https://docs.augent.app) <br>
- [Augent website](https://augent.app) <br>
- [Augent GitHub repository](https://github.com/AugentDevs/Augent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [MCP tool responses with text, JSON-like structured results, Markdown notes, saved media clips, audio files, and extracted visual frames] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be cached or saved locally under user-configured download, notes, clips, TTS, and transcription memory directories.] <br>

## Skill Version(s): <br>
1.5.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
