## Description:

Routes image editing and ecommerce SKU workflows through DesignKit to remove backgrounds, restore image quality, generate product listing image kits, and create Walmart or MercadoLibre preset SKU image sets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joywenxu100](https://clawhub.ai/user/joywenxu100)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to prepare product images for listing workflows, including background removal, quality restoration, listing image generation, and SKU-based Walmart or MercadoLibre image kits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or credentials may be exposed through request logging or broad environment loading.

Mitigation: Disable or fix request logging, scope the DesignKit API key and any database credentials, and avoid running the SKU workflow with unnecessary production secrets.

Risk: The SKU workflow can access database-backed product data and upload selected product images or metadata to DesignKit.

Mitigation: Run the SKU workflow only with explicitly approved, least-privilege database credentials and confirm that uploaded product data is appropriate for external processing.

Risk: Unpinned installation sources or endpoint override variables can make execution harder to audit.

Mitigation: Pin trusted installation sources and avoid endpoint overrides when using production credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joywenxu100/skills/designkit-sku-kit)
- [DesignKit](https://www.designkit.cn/)
- [DesignKit OpenClaw API Key](https://www.designkit.cn/openclaw)
- [SKU Pipeline Usage](artifact/scripts/SKU_PIPELINE_USAGE.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Files, Configuration]

**Output Format:** [Conversational Markdown with inline shell commands, image links, JSON result handling, and downloaded image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DESIGNKIT_OPENCLAW_AK; ecommerce workflows may upload selected images and product data to DesignKit and download generated images locally.]

## Skill Version(s):

1.1.0 (source: server release evidence and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
