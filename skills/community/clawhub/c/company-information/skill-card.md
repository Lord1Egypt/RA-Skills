## Description: <br>
CompanyInformation queries FEEDAX for listed-company news and public-opinion signals, including sentiment, heat, industry classifications, related companies, and risk indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longgggggg](https://clawhub.ai/user/longgggggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to query company news, monitor sentiment and reputation risk, and export FEEDAX results for further review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if pasted into chat, stored in agent memory, or passed directly on the command line. <br>
Mitigation: Use a scoped local secret or FEEDAX_API_KEY environment variable, restrict access to the secret, and avoid sharing credentials in chat. <br>
Risk: Company searches can create CSV and Markdown files containing sensitive research results by default. <br>
Mitigation: Use --no-output for sensitive searches or direct output to a protected directory with appropriate retention controls. <br>
Risk: Network calls require trust in the FEEDAX endpoint and credential handling. <br>
Mitigation: Verify the provider endpoint and HTTPS support before sending credentials or sensitive queries. <br>


## Reference(s): <br>
- [FEEDAX](https://www.feedax.cn) <br>
- [CompanyInformation ClawHub listing](https://clawhub.ai/longgggggg/company-information) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Files, Guidance] <br>
**Output Format:** [Conversation summary plus generated CSV and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a FEEDAX API key and can suppress file generation with --no-output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
