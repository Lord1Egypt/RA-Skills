## Description: <br>
Creates a complete short video from a topic or prepared workflow by orchestrating Chanjing TTS, digital-human video composition, AI text-to-video scenes, and local ffmpeg packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binkes](https://clawhub.ai/user/binkes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, media operators, and developers use this skill to turn a topic, script, or workflow JSON into a publishable short video with narration, digital-human segments, AI-generated B-roll, and local MP4 assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends scripts, prompts, audio, and generated media through Chanjing API and CDN services. <br>
Mitigation: Use the skill only when the user trusts Chanjing's API/CDN and is comfortable sending that content through the service. <br>
Risk: The credential file can contain app_id, secret_key, access_token, and expiry data persisted on disk. <br>
Mitigation: Keep credentials.json out of source control, use restrictive file permissions, and place it in an explicit credentials directory. <br>
Risk: Rendering invokes ffmpeg and ffprobe and writes final media plus intermediate files to local storage. <br>
Mitigation: Install trusted ffmpeg/ffprobe binaries, choose an explicit output directory, and review or delete generated work files after each run. <br>
Risk: Prompt defaults include Chinese and East Asian visual assumptions that may be unsuitable for locale-neutral output. <br>
Mitigation: Review and adjust the prompt templates or workflow fields when locale-neutral or different regional outputs are required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/binkes/chanjing-one-click-video-creation) <br>
- [Publisher profile](https://clawhub.ai/user/binkes) <br>
- [Chanjing documentation](https://doc.chanjing.cc) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Runtime manifest](artifact/manifest.yaml) <br>
- [Render rules](artifact/templates/render_rules.md) <br>
- [Storyboard prompt rules](artifact/templates/storyboard_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance, JSON workflow and result files, shell commands, configuration values, and local media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the renderer writes final_one_click.mp4, workflow_result.json, and work/ intermediate files under the selected output directory.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
