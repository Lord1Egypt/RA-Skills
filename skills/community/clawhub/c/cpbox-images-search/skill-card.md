## Description: <br>
Searches for images through CPBox's paid x402 image-search API and returns image results with titles, source URLs, thumbnails, and SafeSearch controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve image-search results for visual content discovery, content enrichment, safe image retrieval, and batch image sourcing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid external x402 service and its payment helper can make payment automatic. <br>
Mitigation: Configure strict wallet spending limits and require explicit approval before each paid search. <br>
Risk: Image queries may reveal sensitive topics or intent to external services. <br>
Mitigation: Avoid sensitive image queries and route only approved search terms through the service. <br>
Risk: The external payment helper package is part of the execution path for paid requests. <br>
Mitigation: Verify the helper package and service URLs before enabling the skill in wallet-enabled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sprintmint/cpbox-images-search) <br>
- [CPBox API provider](https://www.cpbox.io) <br>
- [CPPay x402 facilitator](https://www.cppay.finance) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image result JSON may include titles, page URLs, source domains, thumbnails, original image URLs, dimensions, confidence, and offensive-content signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
