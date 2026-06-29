## Description: <br>
Company profiles and recent SEC filings from EDGAR via Edgrapi.com. Resolve a US-listed ticker to its CIK, industry, fiscal-year end, and exchange, and list its recent 10-K / 10-Q / 8-K filings with document links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paperandbeyond23-gif](https://clawhub.ai/user/paperandbeyond23-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to look up US-listed company profile details and recent SEC 10-K, 10-Q, and 8-K filings when a user explicitly requests filer metadata or disclosure history for a specific company. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker lookups send the queried ticker to Edgrapi using the user's EDGRAPI_KEY and consume Edgrapi credits. <br>
Mitigation: Use only an Edgrapi key intended for this integration and activate the skill only for explicit company lookup or filing requests. <br>
Risk: Filing lookups depend on Edgrapi and SEC EDGAR availability. <br>
Mitigation: Check returned error fields such as edgar_unavailable, network, out_of_credits, or auth errors before relying on the result. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/paperandbeyond23-gif/edgrapi-skills/tree/main/skills/edgrapi-filings) <br>
- [Edgrapi homepage](https://edgrapi.com) <br>
- [Edgrapi app](https://edgrapi.com/app) <br>
- [Edgrapi pricing](https://edgrapi.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Structured lookup results with company metadata, filing dates, form types, and document links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EDGRAPI_KEY; each request consumes one Edgrapi credit; get_filings supports ticker, limit, and form filters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
