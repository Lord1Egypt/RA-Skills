## Description: <br>
Searches videos through a paid x402 API and returns video result metadata including titles, URLs, thumbnails, durations, view counts, creators, freshness filters, SafeSearch, and pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search video content, monitor fresh video results, target specific platforms with search operators, and retrieve structured video metadata for research, curation, analytics, or recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 payment tooling can make paid calls using a wallet private key without clear spending limits or confirmation steps. <br>
Mitigation: Use a dedicated wallet with minimal funds, configure explicit spending limits outside the skill where possible, and require manual approval before any paid or direct x402 call. <br>
Risk: A primary wallet private key could expose broader funds if used for this paid API flow. <br>
Mitigation: Avoid storing or using a primary wallet private key with this skill; use a separate key scoped to low-value payment activity. <br>
Risk: Video search results may include offensive or adult content depending on query and SafeSearch settings. <br>
Mitigation: Keep SafeSearch set to moderate or strict for general use and review result metadata before downstream publication or automation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sprintmint/cpbox-videos-search) <br>
- [x402 payment setup prerequisites](https://github.com/springmint/cpbox-skills#prerequisites) <br>
- [CPBox API provider](https://www.cpbox.io) <br>
- [CPPay facilitator](https://www.cppay.finance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with HTTP and cURL examples plus JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 requests may sign and retry automatically when compatible payment tooling is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
