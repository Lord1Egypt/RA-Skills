## Description: <br>
Creates short highlight clips from YouTube links or local videos by extracting subtitles, selecting highlight timestamps with MiniMax, generating an AI cover image, and cutting captioned clips with ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freak30](https://clawhub.ai/user/freak30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to turn long-form YouTube or local video inputs into a requested number of short highlight clips with burned-in subtitles and an AI-generated cover image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary reports an exposed provider credential. <br>
Mitigation: Review before installing, remove shared credentials, and require users to provide their own secrets through a protected configuration path. <br>
Risk: The security guidance reports that transcript and title data may be sent to external AI services without clear user consent or scoping. <br>
Mitigation: Use only videos whose titles and subtitles are appropriate to share with MiniMax, document third-party data flows, and make LLM and cover-generation calls optional where possible. <br>
Risk: The security guidance says Tencent COS is mentioned but its actual use is unclear. <br>
Mitigation: Clarify whether Tencent COS is used before deployment and document any storage destinations or disable unused storage behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freak30/clipping-video-highlights) <br>
- [Publisher profile](https://clawhub.ai/user/freak30) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Video files, image files, and command-line progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cover.jpg and clip_01.mp4, clip_02.mp4, and subsequent numbered MP4 highlight clips in the requested output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
