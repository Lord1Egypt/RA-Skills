## Description: <br>
AutoShorts helps an agent turn vertical long-form videos into reviewed short-form clip candidates and scheduled posts for TikTok, Instagram Reels, and YouTube Shorts using Whisper, Gemini, FFmpeg, and Upload-Post. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mutonby](https://clawhub.ai/user/mutonby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use AutoShorts to convert ready-to-post vertical long videos into daily short-form clip candidates, review the generated clips, and schedule approved posts through Upload-Post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow stores Gemini and Upload-Post credentials locally and may expose them if pasted into conversation logs. <br>
Mitigation: Keep required keys in the local .env file, avoid echoing secrets, and rotate any key that was shared in chat. <br>
Risk: Source videos and transcripts are sent to Gemini, and approved clips plus metadata are sent to Upload-Post. <br>
Mitigation: Install only when this cloud processing is acceptable for the source media, and verify the target Upload-Post profile before publishing. <br>
Risk: Publishing and scheduling can affect real social accounts. <br>
Mitigation: Keep dry-run and human approval steps enabled, review the exact payloads, and use TikTok draft mode unless direct posting is explicitly intended. <br>
Risk: Local clip history, candidate history, metrics, and learning files can retain operational and engagement data. <br>
Mitigation: Periodically clear local history and analytics files when retention requirements call for it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mutonby/autoshorts) <br>
- [Project homepage](https://github.com/mutonby/skill-autoshorts) <br>
- [Upload-Post](https://upload-post.com) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON status from CLI commands, and file paths for generated video clips.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces candidate clip tables, platform copy, scheduling commands, local output files, and learning-loop notes.] <br>

## Skill Version(s): <br>
2.0.3 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
