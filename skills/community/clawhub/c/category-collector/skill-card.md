## Description:

Collects category links from Shopify storefront navigation menus, including Ajax-loaded hover menus, and exports the discovered hierarchy to CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qirongzhang](https://clawhub.ai/user/qirongzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce operators can use this skill to collect public storefront category URLs and menu hierarchy from Shopify sites into a structured CSV file for catalog analysis or migration planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad browser and network reach when pointed at a URL.

Mitigation: Use it only on public storefront pages you intentionally choose, preferably in an isolated environment; do not run it against authenticated dashboards, internal URLs, localhost services, cloud metadata addresses, or untrusted user-supplied sites.

Risk: The skill saves local CSV and screenshot files that may capture page content.

Mitigation: Check the output directory after each run and avoid running the scraper on pages that may expose sensitive or private information.

Risk: The skill depends on npm packages and Playwright browser automation.

Mitigation: Pin dependencies and use an approved npm registry before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qirongzhang/skills/category-collector)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands; runtime output is CSV plus page screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The main script accepts a storefront URL and optional output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
