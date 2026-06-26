## Description: <br>
Analyzes LLM-generated brand mentions and sentiment within industry recommendations using DeepSeek's staged GEO performance pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External brand, marketing, and growth teams use this skill to test whether a target brand or product appears in DeepSeek-generated industry recommendations, then review mention status, sentiment, context, competitors, and optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a DeepSeek API key and can incur token usage costs. <br>
Mitigation: Use a dedicated DeepSeek API key with usage limits and monitor usage for the release. <br>
Risk: Brand name and category keyword inputs are sent to DeepSeek for analysis. <br>
Mitigation: Do not submit confidential or embargoed brand, product, or category information unless DeepSeek's data handling is acceptable. <br>
Risk: The artifact depends on unpinned Python package version ranges. <br>
Mitigation: Install in an isolated Python environment and pin reviewed dependency versions before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljseeking/geo-analyzer-deepseek) <br>
- [Skill homepage](https://github.com/LJseeking/lifesignal) <br>
- [DeepSeek API endpoint used by the skill](https://api.deepseek.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object containing a structured_result object and generated report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires brand_name and category_keyword inputs; the bundled script generates the report in Chinese.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
