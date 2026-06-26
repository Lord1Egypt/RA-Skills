## Description: <br>
Manages multiple Fecify independent stores with per-session site URL and API token binding, persistent configuration, and support for product, order, and CSV bulk-import workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fancyecommerce](https://clawhub.ai/user/fancyecommerce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and developers use this skill to configure a Fecify site connection, inspect or change product and image data through Fecify APIs, and migrate Shopify product CSV exports after validation and confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Fecify API tokens on disk for persistent site configuration. <br>
Mitigation: Install only when the publisher is trusted, use scoped or revocable tokens where possible, and avoid shared machines for configured sessions. <br>
Risk: Authenticated API calls can create, update, delete, or bulk import store data. <br>
Mitigation: Require explicit user confirmation before write operations or bulk imports, and prefer dry-run or validation steps before importing. <br>
Risk: Temporary and failed-import files may contain sensitive product or request data. <br>
Mitigation: Review and clean temp or failed-import files after troubleshooting, especially on shared or long-lived environments. <br>
Risk: Misconfigured site URLs or insecure endpoints can expose tokens or send requests to the wrong store. <br>
Mitigation: Use HTTPS-only site URLs and verify the target site before saving configuration or running API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fancyecommerce/fecify-site-manager-v1) <br>
- [Architecture and core modules](docs/architecture.md) <br>
- [Product management API guide](docs/products.md) <br>
- [Base image API guide](docs/base-image.md) <br>
- [CSV import guide](docs/csv-import.md) <br>
- [Shopify CSV product import guide](docs/csv-import/shopify-csv-product-import.md) <br>
- [Extension guide](docs/extending.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, and generated configuration or import-result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write per-site configuration, session binding files, and failed-import diagnostics under the skill data and temp paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
