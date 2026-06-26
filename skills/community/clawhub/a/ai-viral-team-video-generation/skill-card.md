## Description: <br>
Generates and edits AI videos by guiding Vidu model selection, additive prompt optimization, video stitching, and quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junhongzhang77-ui](https://clawhub.ai/user/junhongzhang77-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams and video-generation agents use this skill to turn storyboard prompts into platform-adapted AI video clips, tune prompts without removing original details, stitch clips with FFmpeg, and route outputs through quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vidu API use may send generation prompts, storyboards, and media references to an external service. <br>
Mitigation: Use a scoped Vidu token where possible, review prompts and media before submission, and monitor paid usage. <br>
Risk: FFmpeg stitching could process files outside the intended project area if paths are chosen carelessly. <br>
Mitigation: Keep generated clips and FFmpeg processing inside intended project folders. <br>
Risk: The workflow depends on script-writing and quality-check companion skills. <br>
Mitigation: Review the referenced companion skills before relying on the full video-production workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/junhongzhang77-ui/ai-viral-team-video-generation) <br>
- [Vidu service endpoint](https://service.vidu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown instructions with prompt templates, checklists, configuration notes, and FFmpeg workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a VIDU_TOKEN environment variable for Vidu API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
