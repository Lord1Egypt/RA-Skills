## Description: <br>
Generate serialized comic-drama / 漫剧 episodes through a fixed multi-skill pipeline that creates scripts, character turnarounds, keyframes, 15-second video shots, and final edited episodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and production teams use this skill to turn a story idea into a repeatable short-form comic-drama workflow with consistent recurring characters. It guides script development, storyboard and keyframe generation, video creation through prerequisite skills, and local final assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public media URLs used for image and video handoff may expose sensitive source or generated assets. <br>
Mitigation: Use only authorized, non-sensitive media and avoid private images in public URLs. <br>
Risk: External generation services and prerequisite skills can fail or incur cost when credentials, quota, or credits are not ready. <br>
Mitigation: Configure API keys through secure environment variables and confirm quota, credits, and cost expectations before production. <br>
Risk: Downloaded clips and ffmpeg exports can create confusing or unintended local files. <br>
Mitigation: Keep all generated files in a dedicated project folder and review outputs before publishing or sharing. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Install Checklist](references/install-checklist.md) <br>
- [Asset Consistency Rules](references/asset-rules.md) <br>
- [NanoPhoto Service Homepage](https://nanophoto.ai) <br>
- [NanoPhoto API Key Settings](https://nanophoto.ai/settings/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown project documents with shell commands, asset URLs, and local media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires prerequisite skills, their configured API credentials, public URL handoffs, and local ffmpeg for final assembly.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
