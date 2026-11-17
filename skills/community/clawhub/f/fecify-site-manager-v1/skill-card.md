## Description:

Manages multiple Fecify independent stores with per-session site binding, persisted URL and API token configuration, product and image API operations, and Shopify CSV product import workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fancyecommerce](https://clawhub.ai/user/fancyecommerce)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to configure Fecify store access, inspect or change product and image data through Fecify APIs, and migrate Shopify product CSV files into a Fecify store after detection and validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Fecify API tokens locally and uses them for live store API calls.

Mitigation: Use a dedicated least-privilege token, bind only intended HTTPS sites, and rotate or delete stored tokens when the workflow is complete.

Risk: Product creation, product updates, image uploads, and CSV imports can make broad live changes to a store.

Mitigation: Start with a test store or a small dry run, review generated product JSON and CSV detection results, and require explicit confirmation before bulk import.

Risk: Network image import can fetch or reuse external image URLs from uploaded CSV content.

Mitigation: Inspect CSV image URLs before import and prefer uploading vetted images to the Fecify store unless direct network images are required.

Risk: Skipping execution-layer validation can bypass safeguards for malformed product rows.

Mitigation: Do not use --skip-validation in production; fix CSV data issues reported by the detector before importing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fancyecommerce/skills/fecify-site-manager-v1)
- [Architecture and core modules](docs/architecture.md)
- [Product management API](docs/products.md)
- [Image management API](docs/base-image.md)
- [Shopify CSV product import](docs/csv-import/shopify-csv-product-import.md)
- [CSV import guide](docs/csv-import.md)
- [Extension guide](docs/extending.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API request or response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, dry-run JSON, import summaries, and failed-item archives under the skill data or temp directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
