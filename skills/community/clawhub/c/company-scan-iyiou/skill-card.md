## Description: <br>
Company Scan helps agents filter companies by industry, region, funding round, investment amount, and recent financing, then return structured Markdown results from IYIOU data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-byte](https://clawhub.ai/user/ai-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn company-screening requests into structured search parameters and retrieve matching companies from the IYIOU company data service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search criteria are sent to an external IYIOU API. <br>
Mitigation: Avoid including secrets, highly sensitive business plans, or confidential strategy details in search terms. <br>
Risk: Results are temporarily written to a local file before display. <br>
Mitigation: Review local temporary-file handling and delete generated result files when the output contains sensitive screening criteria. <br>
Risk: Company search results may be incomplete, stale, or affected by narrow filters. <br>
Mitigation: Validate important company data against authoritative sources and broaden filters when the result set is unexpectedly small. <br>


## Reference(s): <br>
- [Company Scan on ClawHub](https://clawhub.ai/ai-byte/company-scan-iyiou) <br>
- [IYIOU Company Data](https://data.iyiou.com/company/comlist) <br>
- [IYIOU Company Search API](https://api-open-data.iyiou.com/llm/company/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables with a query summary, company fields, and source links; JSON is available from the helper script when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may be written to a temporary Markdown file before being read back and presented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
