## Description:

为1688工厂与批发商生成和编辑产品主图、规格图、工厂能力图、定制说明、包装运输和批量SKU图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 factories, wholesalers, and ecommerce operators use this skill to generate or edit B2B product images, specification visuals, factory-process visuals, OEM/ODM explanation images, packaging images, and batch SKU assets from supplied product and factory references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or compromised API endpoint could cause downloaded files to be written outside the selected output folder.

Mitigation: Use only the default trusted AI Hive endpoint, avoid untrusted --base-url values, and choose a low-risk output directory until output containment is verified.

Risk: Reference images and API keys are handled by the AI Hive service and local configuration.

Mitigation: Upload only content suitable for that service and store the API key through the documented local config or environment variable with restricted access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/1688-ecommerce-image-generation-editing)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown instructions with bash command examples; the helper script can print JSON task data and download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the AI Hive image-generation API with optional reference images, batch generation, routing mode, model parameters, output directory, and no-download mode.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
