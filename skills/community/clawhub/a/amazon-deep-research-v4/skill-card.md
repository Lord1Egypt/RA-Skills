## Description: <br>
Amazon Deep Research V4 guides agents through Amazon product research with multi-platform validation, 1688 image-based sourcing, live USD/CNY margin analysis, WIPO IP checks, and HTML report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachary2024](https://clawhub.ai/user/zachary2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace researchers and ecommerce operators use this skill to evaluate Amazon product opportunities, source matching 1688 suppliers from Amazon images, calculate gross margin, filter IP and high-risk products, and generate a sourced HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to extract and reuse live SellerSprite session cookies and tokens, which can expose account access. <br>
Mitigation: Prefer an official API key or OAuth flow, never paste or display cookies or tokens in chat, and clear copied session material after use. <br>
Risk: Generated marketplace and margin analysis can be misleading when live exchange rates, paid platform data, or IP checks are incomplete or stale. <br>
Mitigation: Treat reports as advisory and verify source data, current USD/CNY exchange rates, IP audit results, and margin assumptions before making commercial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zachary2024/amazon-deep-research-v4) <br>
- [1688 image search strategy](references/1688-image-search.md) <br>
- [Multi-platform data collection strategy](references/multi-platform.md) <br>
- [Gross margin calculation](references/margin.md) <br>
- [WIPO IP compliance audit](references/wipo-ip.md) <br>
- [HTML report template](references/html-template.md) <br>
- [SellerSprite API notes](references/sellersprite-api.md) <br>
- [WIPO Global Brand Database](https://branddb.wipo.int/) <br>
- [AMZScout Product Database](https://amzscout.net/product-database) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline Python, JavaScript, browser workflow steps, JSON data files, and an HTML report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sourced marketplace research artifacts such as multi-platform data, 1688 matches, qualified product lists, IP audit data, and an HTML report.] <br>

## Skill Version(s): <br>
1.0.0-beta.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
