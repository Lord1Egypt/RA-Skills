## Description: <br>
auto-remotion guides agents through turning existing screen recordings or product demo videos into Remotion promotional videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[16miku](https://clawhub.ai/user/16miku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-producing agents use this skill to plan and implement promotional videos from existing recordings, including constraint gathering, storyboard and edit-spec creation, Remotion implementation, subtitles, voiceover, background music, and rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions may install npm or pip packages, including optional global or forced installs. <br>
Mitigation: Run the workflow in a dedicated project directory, review packages before installation, and avoid global or --force installs unless they are required. <br>
Risk: The workflow may process confidential recordings, audio, screenshots, transcripts, or filmstrip images with external transcription or AI services. <br>
Mitigation: Obtain permission before uploading sensitive media, redact private content where possible, and use approved services for confidential material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/16miku/auto-remotion) <br>
- [Remotion documentation](https://www.remotion.dev/) <br>
- [Remotion Skills documentation](https://www.remotion.dev/docs/ai/skills) <br>
- [Remotion with Claude Code](https://www.remotion.dev/docs/ai/claude-code) <br>
- [video-use project](https://github.com/browser-use/video-use) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON, TypeScript, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning artifacts such as edit scripts, storyboard JSON, edit-spec JSON, subtitle cues, voiceover scripts, and Remotion implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
