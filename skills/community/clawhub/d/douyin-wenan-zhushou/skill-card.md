## Description:

Retrieves public Douyin videos, creator profiles, comments, post details, and trending topics as structured JSON for content research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, brands, and creators use the skill to research public Douyin content, find creators and trends, compare competitor content, and inspect audience comments. It returns structured data for follow-up analysis such as topic planning and sentiment or demand research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or identifiers are sent to a third-party API, creating a possible privacy disclosure risk.

Mitigation: Use public content only, and avoid submitting private or sensitive identifiers or queries.

Risk: The required GUAIKEI_API_TOKEN grants access to the API and could be misused if exposed.

Mitigation: Keep the token in a protected environment variable and do not include it in prompts, logs, or shared output.

Risk: The security scan was benign but had medium confidence and incomplete component inspection, so it provides limited assurance.

Mitigation: Review the skill's documented behavior and decide whether its third-party API data sharing is acceptable before installation.

## Reference(s):

- [Search and output options](references/options.md)
- [Output data contract](references/contract.md)
- [Errors and retry guidance](references/errors.md)
- [Demand research guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)
- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/douyin-wenan-zhushou)
- [GuaiKei API service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results, with concise text or Markdown summaries when analysis is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin search, creator, post, comment, and trending data; some results can be saved as JSON for later analysis.]

## Skill Version(s):

1.4.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
