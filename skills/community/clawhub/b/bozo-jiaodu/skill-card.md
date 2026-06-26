## Description: <br>
Converts Chinese camera-angle requests into standardized <sks> image camera-position prompts and can provide BizyAir task commands for image angle adjustment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and image-generation workflow developers use this skill to turn Chinese direction, height, and shot-distance descriptions into one of 96 standardized <sks> camera-position prompts, or to identify non-angle image-editing requests. When intentionally configured with a BizyAir API key, users can run the packaged scripts to create and poll image angle-adjustment tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packaged local permission settings can pre-approve shell and API actions. <br>
Mitigation: Review or remove .claude/settings.local.json before installing and require explicit approval for script execution. <br>
Risk: BizyAir API use sends image URLs, prompts, task IDs, output URLs, and account quota context to a third-party service. <br>
Mitigation: Set BIZYAIR_API_KEY and run the scripts only when remote BizyAir processing is intended; avoid submitting sensitive images or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/bozo-jiaodu) <br>
- [BizyAir task creation API](https://api.bizyair.cn/w/v1/webapp/task/openapi/create) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text prompts, Markdown tables, and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Camera-angle conversions must use one of 96 <sks> prompt strings; BizyAir scripts require BIZYAIR_API_KEY and submit image URLs and prompts to BizyAir.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
