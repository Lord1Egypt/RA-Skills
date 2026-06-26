## Description: <br>
Generates a Chinese rebirth-revenge short-video pipeline from a theme by creating a story, converting it to TTS audio, and composing a vertical MP4 with FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h1456942763](https://clawhub.ai/user/h1456942763) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to automate Chinese web-novel short-video generation from a supplied or random theme. It can run the novel, audio, and video steps independently or as one local command-line pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local shell command construction is unsafe when processing generated media-list and FFmpeg inputs. <br>
Mitigation: Review before installation, run only in a dedicated throwaway working directory, and avoid media files from untrusted sources or with unusual filenames until the command construction is fixed. <br>
Risk: Story text is sent to an under-disclosed third-party TTS service. <br>
Mitigation: Do not use sensitive, private, or proprietary story text, and review the TTS service before using it for production content. <br>
Risk: The pipeline requires an OpenAI-compatible API key. <br>
Mitigation: Use a revocable API key scoped for this workflow and rotate or revoke it after testing or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h1456942763/ai-novel-chongshengfuchou) <br>
- [Publisher profile](https://clawhub.ai/user/h1456942763) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Pexels Videos](https://www.pexels.com/videos/) <br>
- [Pixabay Videos](https://pixabay.com/videos/) <br>
- [Free Music Archive](https://freemusicarchive.org/) <br>
- [YouTube Audio Library](https://www.youtube.com/audiolibrary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Audio, Video] <br>
**Output Format:** [Plain text story file, MP3 audio segments, vertical MP4 video, and command-line logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces output.txt, audio/*.mp3, and output.mp4; final video is documented as 1080x1920 vertical output and requires user-provided video/ assets plus bgm.mp3.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
