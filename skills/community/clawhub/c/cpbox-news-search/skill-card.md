## Description: <br>
Provides paid news search through CPBox with article metadata, freshness and date filters, SafeSearch, and custom Goggles ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search recent or historical news and receive structured article results for monitoring, research, multilingual queries, and data pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 payment can spend funds when requests are retried through a compatible payment helper. <br>
Mitigation: Review payment requirements and cost before use; use spending limits or a low-balance wallet when automatic payments are enabled. <br>
Risk: Queries and payment requests are sent to external CPBox and facilitator services. <br>
Mitigation: Avoid sending sensitive queries unless those services' terms and privacy practices are acceptable for the use case. <br>
Risk: News search results may be incomplete, stale, or affected by ranking, SafeSearch, and filtering settings. <br>
Mitigation: Verify important results against source URLs and tune freshness, SafeSearch, and Goggles filters for the task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sprintmint/cpbox-news-search) <br>
- [x402 payment setup prerequisites](https://github.com/springmint/cpbox-skills#prerequisites) <br>
- [CPBox API provider](https://www.cpbox.io) <br>
- [CP Pay facilitator](https://www.cppay.finance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown with HTTP, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 requests may automatically sign and settle payment when a compatible payment helper is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
