## Description: <br>
Analyzes Amazon category and keyword opportunities through the ClawEC API, including opportunity scores, search-rank trends, 30-day sales metrics, and radar scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers, operators, and agents use this skill to evaluate Amazon category or keyword opportunities and produce a Chinese market opportunity report with ranked keywords, trends, sales metrics, and radar-score interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon keyword, category, and market choices are sent to ClawEC with the user's API key. <br>
Mitigation: Avoid submitting confidential product plans or sensitive business research unless ClawEC's data handling and retention practices meet the user's requirements. <br>
Risk: The output depends on external ClawEC API availability, credentials, and returned market data. <br>
Mitigation: Check the API key, keyword, region code, and response status before relying on the generated opportunity analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-amazon-category-opportunity) <br>
- [Response schema](references/response-schema.md) <br>
- [ClawEC API base](https://www.clawec.com/api) <br>
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown report with ranked keyword tables, trend summaries, radar-score interpretation, and optional raw API JSON from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWEC_API_KEY and sends the requested keyword, Amazon marketplace region, and table flag to ClawEC.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
