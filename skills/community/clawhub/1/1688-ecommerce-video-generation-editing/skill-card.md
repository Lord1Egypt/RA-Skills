## Description:

为1688工厂与批发商生成和编辑产品演示、生产流程、OEM/ODM定制、质检包装和B2B询盘视频。Use this skill for 1688电商视频、阿里巴巴批发、源头工厂、OEM/ODM、生产线实拍、工艺流程、质检、包装物流、批发商品视频和采购询盘；支持 Seedance 与 AI Hive 自动交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 suppliers, wholesalers, and their agents use this skill to generate, edit, extend, and review product, factory process, OEM/ODM, inspection, packaging, and inquiry videos while keeping supplier evidence separate from illustrative generated scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and selected business media can be sent to a custom endpoint.

Mitigation: Review endpoint settings before use and keep the default trusted AI Hive base URL unless intentionally operating a custom deployment.

Risk: Supplier media, product images, and factory footage may be uploaded to AI Hive during generation, editing, or task submission.

Mitigation: Avoid passing sensitive business media unless upload is expected and approved for the workflow.

Risk: The skill stores an AI Hive API key in a local configuration file or reads it from the environment.

Mitigation: Protect the saved API key, use an isolated environment, and prefer pinned dependencies when installing.

Risk: Generated or edited ecommerce videos could imply unsupported supplier claims.

Mitigation: Require supplier review for capacity, lead time, certification, MOQ, customization, brand authorization, and customer-case claims before publication.

## Reference(s):

- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/1688-ecommerce-video-generation-editing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and downloaded media files from AI Hive tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload local image, video, or audio inputs to AI Hive, poll task status, and download generated video files to a configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
