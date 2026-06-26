## Description: <br>
Use when you need to turn a local source video and one product image into a single-product placement video with the DPP pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kotot](https://clawhub.ai/user/kotot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video workflow operators use this skill to run a staged local pipeline that creates storyboard analysis, product material configuration, placement selection, generated best-segment composition, and a final cut for one source video and one product image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends source video, product image, prompts, and media references to Ark and may upload reference media to TOS. <br>
Mitigation: Run the skill only with media you are permitted to process through those services, and provide TOS upload credentials only when automatic reference-media upload is intended. <br>
Risk: The skill requires sensitive Ark and optional TOS credentials. <br>
Mitigation: Use narrowly scoped credentials in a dedicated workspace .env and avoid sharing or committing generated environment files. <br>
Risk: Persistent Ark response logging may retain prompts, media metadata, or response details. <br>
Mitigation: Review or delete log/ark_responses.log after use according to the workspace retention policy. <br>
Risk: Bundled TOS list/upload demo modules can perform storage operations beyond the main staged workflow. <br>
Mitigation: Do not invoke the demo modules unless those storage operations are explicitly needed and credentials have been scoped for that purpose. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kotot/dpp-pipeline) <br>
- [DPP Commands](references/commands.md) <br>
- [DPP Pipeline Runtime](references/runtime-readme.md) <br>
- [Environment example](references/env-example.txt) <br>
- [Ark API base URL](https://ark.cn-beijing.volces.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and file paths for staged pipeline outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime can create JSON files, logs, thumbnails, reference clips, and final video files in the caller workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
