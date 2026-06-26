## Description: <br>
Turns a user-provided short-drama script or story outline into a staged AI video-production workflow covering script analysis, asset prompts, storyboard design, first-frame generation, clip generation, and final compositing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to guide short-drama video production from a script through character and scene assets, storyboard planning, generated clips, subtitles or music, and final composition. It is intended for agent-assisted creative production with user confirmation between stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can write or overwrite local files under output/ during video production. <br>
Mitigation: Review output paths before generation and run the workflow in a clean project directory or container when prior outputs must be preserved. <br>
Risk: The workflow suggests installing ffmpeg with apt-get if ffmpeg is missing, which can make persistent system changes. <br>
Mitigation: Install dependencies manually in a controlled environment and do not allow automatic package installation during skill execution. <br>
Risk: The workflow uses ffmpeg and generated media files in a local video pipeline. <br>
Mitigation: Review ffmpeg commands and input file paths before execution, especially when adding subtitles, music, or transitions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/ai-short-drama-director) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Code, Shell commands, Media files] <br>
**Output Format:** [Markdown reports, JSON manifests, inline shell and Python snippets, tool request payloads, and generated media file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates an output/ workspace containing analysis, asset lists, storyboards, frame and clip references, subtitles, optional music, final video, and a production report.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
