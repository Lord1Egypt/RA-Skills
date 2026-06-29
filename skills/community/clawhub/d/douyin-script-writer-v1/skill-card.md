## Description: <br>
Turn a topic into a Douyin-ready short video script with hook, storyboard, captions, and BGM suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, e-commerce sellers, and video editing assistants use this skill to draft Douyin/TikTok-style short video scripts for 15, 30, or 60 second videos. It produces structured hooks, timed scenes, voiceover lines, camera direction, subtitle guidance, BGM suggestions, publish windows, and cover copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local CLI helper may save prompts locally. <br>
Mitigation: Avoid entering sensitive campaign, customer, or product details unless local prompt retention is acceptable. <br>
Risk: Generated scripts may include inaccurate, unsuitable, or platform-risky claims for a specific campaign. <br>
Mitigation: Review scripts, claims, CTAs, and music suggestions before filming or publishing. <br>
Risk: Helper scripts are executable local files. <br>
Mitigation: Review included helper scripts before running them directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/douyin-script-writer-v1) <br>
- [BGM examples](artifact/references/bgm-examples.json) <br>
- [15-second script template](artifact/references/templates/15s-template.json) <br>
- [30-second script template](artifact/references/templates/30s-template.json) <br>
- [60-second e-commerce script template](artifact/references/templates/60s-ecommerce-template.json) <br>
- [Input schema](artifact/schemas/input.schema.json) <br>
- [Output schema](artifact/schemas/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown and JSON-compatible script objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized around supported durations of 15, 30, and 60 seconds and include timed storyboard scenes, captions, BGM, publishing windows, and cover copy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
