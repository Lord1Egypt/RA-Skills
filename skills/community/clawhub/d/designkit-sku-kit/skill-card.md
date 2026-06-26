## Description: <br>
AI 图片处理与电商商品图生成技能包（美图设计室 DesignKit），支持抠图去背景、透明底、AI 变清晰/画质修复、商品主图、Listing 套图和 SKU 套图生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joywenxu100](https://clawhub.ai/user/joywenxu100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route image-editing and ecommerce-image requests, collect required product inputs, call DesignKit workflows, and return edited images or ecommerce listing image sets. SKU workflows can query product data and generate Walmart or MercadoLibre-ready image sets from a SKU. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports review concerns around credential logging. <br>
Mitigation: Use the skill only in a controlled workspace, set OPENCLAW_REQUEST_LOG=0 before running, and rotate the DesignKit API key if it has already been used with default logging. <br>
Risk: Security evidence reports unsafe command input handling concerns. <br>
Mitigation: Avoid untrusted JSON, file paths, or URLs as inputs; review command arguments before execution. <br>
Risk: Security evidence reports under-scoped database access for SKU workflows. <br>
Mitigation: Verify DB_* configuration and the intended SKU table before using SKU generation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/joywenxu100/designkit-sku-kit) <br>
- [DesignKit OpenClaw API key setup](https://www.designkit.cn/openclaw) <br>
- [DesignKit website](https://www.designkit.cn/) <br>
- [SKU pipeline usage](scripts/SKU_PIPELINE_USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with image links, JSON status payloads, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESIGNKIT_OPENCLAW_AK; ecommerce workflows may return remote media URLs and local output paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
