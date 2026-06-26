## Description: <br>
Set up Blossom Hire, create local work opportunities, and help employers and jobseekers move through Blossom work flows in plain language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbiwu](https://clawhub.ai/user/robbiwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External employers and jobseekers use this skill to set up a Blossom Hire account, create local work opportunities, search for work, apply to roles, and manage Blossom marketplace records through the assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles personal details and a permanent Blossom API key that grants full account access. <br>
Mitigation: Collect only the data needed for the current Blossom action, keep the API key in runtime memory only, and treat the key as a secret until Blossom rotates or revokes it. <br>
Risk: The skill can create, update, delete, post, or apply to marketplace records. <br>
Mitigation: Summarize each mutating action and require clear user confirmation before sending the request. <br>
Risk: Forwarding unrelated conversation content could expose private or irrelevant data to the Blossom API. <br>
Mitigation: Send only the minimal job-related instruction or payload needed for the current action, and do not forward unrelated conversation history, prompts, documents, tokens, cookies, or keys. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/robbiwu/blossom-hire) <br>
- [Blossom website](https://blossomai.org) <br>
- [Blossom API endpoint](https://hello.blossomai.org/api/v1/blossom/protocol) <br>
- [Blossom privacy policy](https://blossomai.org/privacypolicy.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls, configuration] <br>
**Output Format:** [Plain-language responses with structured API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles personal details and a Blossom API key; requires user confirmation before mutating marketplace records.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
