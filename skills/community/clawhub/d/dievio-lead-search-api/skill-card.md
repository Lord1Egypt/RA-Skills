## Description: <br>
Runs Dievio lead search and LinkedIn lookup workflows through the public API with authentication, filters, pagination, and credit-aware handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Growth teams, SDR workflows, agencies, and builders use this skill to run authorized B2B lead discovery and LinkedIn enrichment through Dievio with structured filters, pagination, and credit-aware result handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead search and LinkedIn enrichment can expose personal contact data. <br>
Mitigation: Use the skill only for authorized B2B workflows, keep summary output unless full records are needed, and follow applicable privacy, platform, anti-spam, retention, and internal data-handling rules. <br>
Risk: API credentials and large paginated pulls can increase security, privacy, or billing exposure. <br>
Mitigation: Use a dedicated Dievio API key, avoid printing secrets, set explicit page and result limits, and pass only intended JSON files to body-file inputs. <br>
Risk: Credit limits or transient API failures can return fewer results than requested or interrupt pagination. <br>
Mitigation: Trust the returned count and paging fields, do not retry credential or credit failures until fixed, and use bounded backoff for transient server errors. <br>


## Reference(s): <br>
- [Dievio Homepage](https://dievio.com) <br>
- [Dievio API Overview](https://docs.dievio.com/api-reference/overview) <br>
- [Dievio API Reference (Condensed)](references/api-reference.md) <br>
- [Dievio Filters Cheatsheet](references/filters-cheatsheet.md) <br>
- [Dievio Pagination](references/pagination.md) <br>
- [Dievio API Errors](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is summary-only; raw output can include emails or phone numbers and should be requested only when full records are needed.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
