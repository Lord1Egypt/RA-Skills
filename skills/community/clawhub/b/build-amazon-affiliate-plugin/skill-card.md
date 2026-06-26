## Description: <br>
Create a production-ready WordPress plugin that displays Amazon product ads when users insert Amazon affiliate links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjohnathanblog-spec](https://clawhub.ai/user/imjohnathanblog-spec) <br>

### License/Terms of Use: <br>
GPL v2 or later <br>


## Use Case: <br>
Developers use this skill to generate a WordPress plugin for Amazon Associates workflows, including Amazon link detection, ASIN extraction, ad display, admin settings, caching, and Gutenberg block support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated WordPress plugin code could affect site content rendering, affiliate disclosures, or link behavior. <br>
Mitigation: Review the generated PHP before production use and test replace and append display modes on a staging site. <br>
Risk: Optional Amazon PA-API credentials include a secret key that must be protected. <br>
Mitigation: Store and handle PA-API credentials carefully in WordPress, and limit access to the settings page to administrators. <br>
Risk: Affiliate ad behavior must comply with Amazon Associates requirements and site disclosure practices. <br>
Mitigation: Confirm affiliate tags, nofollow links, and disclosure behavior before enabling the plugin broadly. <br>


## Reference(s): <br>
- [Plugin Specification](references/PLUGIN_SPEC.md) <br>
- [Amazon PA-API Integration Guide](references/AMAZON_API.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/imjohnathanblog-spec/build-amazon-affiliate-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [code, files, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated WordPress plugin files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PHP, CSS, JavaScript, installation instructions, and expansion documentation for the generated plugin.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact plugin readme, and plugin specification) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
