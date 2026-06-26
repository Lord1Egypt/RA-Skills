## Description: <br>
Fetch financing event lists from the iYiou skill API and generate daily or recent-N-days financing reports in Markdown to stdout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-byte](https://clawhub.ai/user/ai-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to fetch public iYiou financing-event data and produce Chinese daily or recent-window investment digest reports. It is intended for report generation, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implicit invocation may cause the agent to use the skill automatically for finance-report tasks and make bounded requests to the disclosed iYiou API. <br>
Mitigation: Review automatic skill selection for finance-report prompts and confirm outbound requests to the disclosed endpoint are acceptable. <br>
Risk: Reports depend on third-party API availability and page-level fetches, so network failures or empty API responses can produce incomplete or empty digests. <br>
Mitigation: Review the generated report metadata, page errors, and source links before relying on the digest. <br>


## Reference(s): <br>
- [Field Mapping](references/field_mapping.md) <br>
- [iYiou financing event API](https://api.iyiou.com/skill/info) <br>
- [ClawHub skill page](https://clawhub.ai/ai-byte/daily-investment-digest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report text to stdout, with normalized JSON available as an intermediate stdout stream] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to yesterday for single-day reports, supports recent 2-7 day windows, and does not write report files to disk.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
