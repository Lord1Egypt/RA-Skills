## Description: <br>
使用豆包（火山引擎 Ark）生成图片或视频，将结果保存到本地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showtimewalker](https://clawhub.ai/user/showtimewalker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to call Doubao Seedream and Seedance through Volcengine Ark for text-to-image, image-to-image, text-to-video, and frame-guided video generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image inputs, and image URLs may be sent to Volcengine Ark for generation or editing. <br>
Mitigation: Use the skill only with content that is appropriate to share with Volcengine Ark, and avoid sensitive prompts or media unless that transfer is acceptable. <br>
Risk: Generated outputs and logs are written under OUTPUT_ROOT and may contain sensitive prompts, media paths, or generated assets. <br>
Mitigation: Set OUTPUT_ROOT to a controlled directory and review or clean generated outputs and logs when working with sensitive material. <br>
Risk: The optional webhook server accepts asynchronous callbacks for video tasks. <br>
Mitigation: Run the webhook server only when async callbacks are needed and expose it only in an environment where the callback endpoint is intended to receive Ark task updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/showtimewalker/doubao-all-in-one) <br>
- [Publisher profile](https://clawhub.ai/user/showtimewalker) <br>
- [Usage guide](references/usage.md) <br>
- [Seedream prompt guide](references/seedream_prompt_guide.md) <br>
- [Seedance 1.5 Pro prompt guide](references/seedance_1_5_pro_prompt_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON status records plus local image or video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets are saved under OUTPUT_ROOT in outputs/doubao paths; video workflows may return task IDs, source URLs, and downloaded MP4 paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
