## Description: <br>
Build multi-step AI content creation pipelines combining image, video, audio, and text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content teams use this skill to plan and run AI media workflows for short-form video, talking-head clips, product demos, and blog-to-video conversion using the inference.sh CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflows depend on the inference.sh CLI and third-party model providers. <br>
Mitigation: Install only if inference.sh and the selected providers are trusted; prefer the documented checksum-verification install path when extra assurance is needed. <br>
Risk: Prompts and media inputs may be sent to external AI or media-generation providers. <br>
Mitigation: Avoid confidential or regulated content unless provider policies and organizational approvals allow it. <br>
Risk: Generated media could be posted or distributed publicly as part of a content workflow. <br>
Mitigation: Require explicit confirmation before any workflow publishes or distributes generated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okaris/ai-content-pipeline) <br>
- [inference.sh](https://inference.sh) <br>
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline) <br>
- [Building Workflows](https://inference.sh/blog/guides/ai-workflows) <br>
- [Manual install checksum verification](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow plans and CLI command sequences for external media generation services.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
