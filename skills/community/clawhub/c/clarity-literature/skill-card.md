## Description: <br>
Search research papers and get publication details from Clarity Protocol for literature, PubMed references, and citation details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and researchers use this skill to search Clarity Protocol literature records, retrieve paper metadata by PMID, check full-text availability, and gather citation details for literature reviews or bibliographies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send literature lookup requests to Clarity Protocol and may include an API key when CLARITY_API_KEY is set. <br>
Mitigation: Install it only when Clarity Protocol network access is acceptable, and store CLARITY_API_KEY as a service credential rather than embedding it in prompts or files. <br>
Risk: Anonymous use is limited to 10 requests per minute, while authenticated use is limited to 100 requests per minute. <br>
Mitigation: Plan automated literature lookups around the documented rate limits and retry after the API-provided delay when rate limited. <br>


## Reference(s): <br>
- [Clarity Literature on ClawHub](https://clawhub.ai/clarityprotocol/clarity-literature) <br>
- [clarityprotocol Publisher Profile](https://clawhub.ai/user/clarityprotocol) <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [Clarity Protocol API](https://clarityprotocol.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or summary command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Clarity Protocol over the network and may use the optional CLARITY_API_KEY environment variable for higher rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
