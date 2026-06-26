## Description: <br>
Searches Amazon products across supported marketplace regions through the ClawEC API and returns product prices, sales, ratings, review counts, and links for sourcing and competitor research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce operators use this skill to search Amazon products by keyword and marketplace region, compare product metrics, and support sourcing or competitor research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive ClawEC API key. <br>
Mitigation: Store CLAWEC_API_KEY in an environment variable or secret store and never hard-code it in skill files or prompts. <br>
Risk: Product-search keywords and selected marketplace regions are sent to a third-party ClawEC API. <br>
Mitigation: Use the skill only when the user accepts sending those queries to clawec.com, and avoid private or sensitive keywords. <br>


## Reference(s): <br>
- [Amazon product search response schema](references/response-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-amazon-product-search) <br>
- [ClawEC API base URL](https://www.clawec.com/api) <br>
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and tables, with JSON responses from the ClawEC API when called directly.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWEC_API_KEY and sends product-search keywords and marketplace region codes to the ClawEC API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
