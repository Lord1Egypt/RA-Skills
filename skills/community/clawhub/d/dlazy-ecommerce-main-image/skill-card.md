## Description:

生成与编辑电商商品主图候选，涵盖白底基线、可视差异、场景图、配色 SKU 和单变量 A/B 测试，并强调商品事实准确。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

电商卖家和营销团队可使用已批准的商品实拍图，制作适用于商品列表和内容渠道的主图候选，并按单变量原则设计可比较的测试组。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a medium-confidence benign verdict but flags an unexplained login command that does not match the stated image-generation purpose; its evidence is incomplete.

Mitigation: Before authenticating, review the login flow and confirm it matches the expected dLazy CLI behavior.

Risk: The documented workflow sends prompts to dLazy and uploads local image files to its media service.

Mitigation: Use only approved product photos and avoid sending images containing sensitive or customer information.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-ecommerce-main-image)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Generated image candidates returned as hosted image URLs, with Markdown guidance and Bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image candidates are generated from approved product photos; the skill recommends checking product details and channel rules before publishing.]

## Skill Version(s):

1.0.32 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
