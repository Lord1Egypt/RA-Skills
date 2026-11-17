## Description:

Helps ecommerce, product photography, brand, and livestream commerce teams use AI-HIVE to generate or edit Douyin ecommerce images from prompts and optional reference images, then submit, track, and download remote generation results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand teams, product photographers, marketers, and developers use this skill to create commercial product images, campaign visuals, social commerce assets, and reference-guided image edits through AI-HIVE. The skill also provides shell commands and configuration guidance for API key setup, task submission, status checks, and result downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys and selected files to configurable remote endpoints.

Mitigation: Use only the trusted AI-HIVE endpoint unless testing with a separate key, keep API keys scoped and revocable, and avoid sharing sensitive reference files.

Risk: The skill can automatically create remote generation tasks that may incur charges.

Mitigation: Confirm routing, batch size, pricing snapshot, and budget before submitting tasks, especially for batch or high-cost runs.

Risk: Implicit use for broad image or ecommerce prompts could upload unintended files or create unwanted tasks.

Mitigation: Invoke the skill only for explicit AI-HIVE image generation or editing tasks and use a dedicated output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-douyin-ecommerce-image-gen-edit)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image files are downloaded by the bundled script when remote AI-HIVE tasks complete.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
