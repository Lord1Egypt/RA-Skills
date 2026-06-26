## Description: <br>
Retrieve public company information by stock ticker symbol or SEC CIK number using the apipick Company Facts API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and business users can ask an agent to look up public company facts by ticker or SEC CIK, including market capitalization, employee count, industry, exchange, website, and SEC filings links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an apipick API key and sends company lookup requests to apipick.com using that credential. <br>
Mitigation: Set APIPICK_API_KEY as an environment variable, avoid pasting the key into chat, and install only if this external API use is acceptable. <br>


## Reference(s): <br>
- [apipick-company-facts README](README.md) <br>
- [apipick Company Facts API Reference](references/api_reference.md) <br>
- [apipick](https://www.apipick.com) <br>
- [Company Facts](https://www.apipick.com/company-facts) <br>
- [Get API Key](https://www.apipick.com/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional API request examples and formatted company facts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the apipick Company Facts API and require APIPICK_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
