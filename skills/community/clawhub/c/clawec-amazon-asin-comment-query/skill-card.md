## Description: <br>
Queries Amazon product reviews by ASIN or product URL through the ClawEC API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to fetch and summarize Amazon review data for ecommerce research, review analysis, negative-feedback investigation, and buyer-feedback insight workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Amazon product URLs or ASINs to ClawEC using the user's API key. <br>
Mitigation: Use the skill only when sharing those product research targets with ClawEC is acceptable. <br>
Risk: The skill requires the sensitive CLAWEC_API_KEY credential. <br>
Mitigation: Keep CLAWEC_API_KEY in environment or secret storage, and do not hardcode or paste it unnecessarily. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/clawec-amazon-asin-comment-query) <br>
- [ClawEC API Base](https://www.clawec.com/api) <br>
- [ClawEC API Key Page](https://www.clawec.com/api-key?source=q-clawhub) <br>
- [Response Schema](references/response-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summaries and tables based on JSON API responses, with optional shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWEC_API_KEY and sends Amazon product URLs or ASINs to ClawEC.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
