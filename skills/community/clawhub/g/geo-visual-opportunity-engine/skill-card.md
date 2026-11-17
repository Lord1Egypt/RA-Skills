## Description:

Turns a product and keyword opportunity into AI-generated visuals, structured product data, localized commerce copy, and export-ready commerce assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geo-seo](https://clawhub.ai/user/geo-seo)

### License/Terms of Use:

MIT-0

## Use Case:

Commerce, DTC, agency, and growth teams use this skill to analyze product opportunities, generate product image prompts and visuals, create localized listing copy, and prepare Shopify or WooCommerce export assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Store credentials may enable live Shopify or WooCommerce writes when direct export is enabled.

Mitigation: Use least-privilege test-store tokens first, avoid ambient store admin credentials unless publishing is intended, and require explicit direct-export flags before store writes.

Risk: Writable output paths can place generated images or workflow result files outside the intended workspace if not constrained.

Mitigation: Constrain output paths to a dedicated directory and review caller-provided paths before running workflows.

Risk: External API calls for image generation and commerce export can expose product data or credentials to third-party services.

Mitigation: Review inputs before execution, validate store URLs, and keep Google, Shopify, and WooCommerce credentials scoped to the minimum required action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geo-seo/skills/geo-visual-opportunity-engine)
- [Project homepage](https://github.com/GEO-SEO/geo-visual-opportunity-engine)
- [Dageno.ai](https://dageno.ai)

## Skill Output:

**Output Type(s):** [JSON, Text, Files, API Calls, Configuration]

**Output Format:** [Structured JSON with generated image paths, commerce copy, product data, schedules, and optional export results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated images and workflow result files to an output directory; direct Shopify or WooCommerce export occurs only when explicitly enabled with matching credentials.]

## Skill Version(s):

3.0.5 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
