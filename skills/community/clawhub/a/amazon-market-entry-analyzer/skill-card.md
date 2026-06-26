## Description: <br>
Assesses Amazon market viability from a keyword or category by using APIClaw data to analyze demand, competition, pricing, brand concentration, reviews, and trends, then returns a GO, CAUTION, or AVOID recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, product researchers, and commerce analysts use this skill to evaluate whether a product category or niche is worth entering and to compare sub-markets with data-backed scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product keywords, category paths, ASINs, and related market research inputs are sent to APIClaw. <br>
Mitigation: Use the skill only for inputs that are acceptable to share with APIClaw, and avoid including confidential product plans unless that data sharing is approved. <br>
Risk: Broad analyses can make many API calls and consume API credits. <br>
Mitigation: Use explicit prompts that narrow the category or requested deep dives, and review the API usage section in generated reports. <br>
Risk: API credential handling has disclosure gaps around fallback behavior. <br>
Mitigation: Set APICLAW_API_KEY in the environment and avoid storing API keys in shared local configuration files. <br>
Risk: Market-entry recommendations can be misleading if treated as the sole basis for a business decision. <br>
Mitigation: Use the generated disclaimer, confidence labels, and data provenance, and validate decisions with additional sources before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/apiclaw/amazon-market-entry-analyzer) <br>
- [Market Entry Analyzer API Field Reference](references/reference.md) <br>
- [APIClaw API Documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw](https://apiclaw.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown market-entry report with scoring tables, data provenance, API usage, and optional shell commands for APIClaw CLI execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's language and includes confidence labels for data-backed, inferred, and directional conclusions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
