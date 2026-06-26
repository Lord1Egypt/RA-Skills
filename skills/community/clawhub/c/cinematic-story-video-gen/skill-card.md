## Description: <br>
Generates cinematic story video prompts and WeryAI video-generation commands for text-to-video or image-to-video workflows with explicit approval before paid submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn short cinematic story briefs or public image URLs into expanded production prompts, reviewed WeryAI parameters, and video generation commands. It is suited for emotional scenes, brand mood films, character moments, and cinematic image-to-video clips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid WeryAI submissions can consume credits when submit or wait commands are run. <br>
Mitigation: Require explicit user approval of the full expanded prompt and parameter table before any paid generation command. <br>
Risk: The skill requires WERYAI_API_KEY for runtime access. <br>
Mitigation: Treat the key as a secret, keep it out of committed files and chat output, and install only when WeryAI access is intended. <br>
Risk: Image-to-video workflows may upload local image files to WeryAI if local paths are used. <br>
Mitigation: Prefer public HTTPS image URLs and use local paths only after explicit consent to upload that file. <br>


## Reference(s): <br>
- [WeryAI Video API Reference](references/WERYAI_VIDEO_API.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/cinematic-story-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON parameters and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces expanded prompts, confirmation tables, WeryAI task commands, task IDs, status guidance, and Markdown video links when generation succeeds.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter: 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
