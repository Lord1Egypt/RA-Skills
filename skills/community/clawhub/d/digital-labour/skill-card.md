## Description: <br>
24 AI agents for business automation - sales outreach, lead gen, content creation, SEO, ad copy, bookkeeping, proposals, market research, business plans, tech docs, data entry, web scraping, CRM ops, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ResonanceEnergy](https://clawhub.ai/user/ResonanceEnergy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, sales teams, marketers, and support teams use this skill to run specialized remote AI agents for sales outreach, lead generation, content creation, SEO, bookkeeping, proposals, research, support replies, and related back-office workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs sent through the helper scripts are submitted to an external Digital Labour API endpoint. <br>
Mitigation: Only send data that the user is authorized to process externally, and avoid secrets, regulated personal data, financial records, resumes, or customer data unless policy allows it. <br>
Risk: The API endpoint and optional API key are controlled through environment variables. <br>
Mitigation: Set DIGITAL_LABOUR_API_URL and DIGITAL_LABOUR_API_KEY deliberately, and verify the endpoint before running single-agent, batch, or pipeline commands. <br>
Risk: Batch and pipeline workflows can submit multiple business tasks sequentially. <br>
Mitigation: Review batch files and pipeline inputs before execution so unintended or sensitive records are not submitted. <br>


## Reference(s): <br>
- [Digital Labour API homepage](https://bitrage-labour-api-production.up.railway.app) <br>
- [Digital Labour ClawHub listing](https://clawhub.ai/ResonanceEnergy/digital-labour) <br>
- [ResonanceEnergy publisher profile](https://clawhub.ai/user/ResonanceEnergy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote API responses are structured JSON and may include QA status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
