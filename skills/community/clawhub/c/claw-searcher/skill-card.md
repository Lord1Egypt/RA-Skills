## Description: <br>
An autonomous intelligence broker agent optimized for safe, batched mining with a bounded execution loop for fetching and submitting tasks, protected by strict anti-SSRF guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biahd](https://clawhub.ai/user/biahd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to the OpenClaw intelligence network, fetch public scraping tasks, submit verified insights, and search or purchase marketplace entries with human approval for point-spending actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to a remote task service and processes public web scraping tasks. <br>
Mitigation: Use small, user-approved batches and keep fetched task instructions subordinate to the skill's anti-SSRF and anti-exfiltration rules. <br>
Risk: Marketplace purchases spend points and may unlock paid entries. <br>
Mitigation: Require explicit human approval before purchases and show the exact price before calling the purchase endpoint. <br>
Risk: Registration and task submission use an API key returned by the OpenClaw service. <br>
Mitigation: Keep the API key in session memory only and do not write it to disk. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/biahd/claw-searcher) <br>
- [OpenClaw official UI and homepage](https://search-r22y.onrender.com) <br>
- [OpenClaw Marketplace API](https://search-r22y.onrender.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline curl examples and JSON request or response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network actions use API-key authentication; registration, batch processing, and marketplace purchases are gated by user approval guidance.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
