## Description: <br>
Uses the Chilltion API to create AI videos from text prompts and to check Chilltion sessions, credits, costs, balances, and API responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragondean](https://clawhub.ai/user/dragondean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create short AI videos from a single Chilltion prompt, monitor generation progress, and inspect session, credit, balance, and cost information through the Chilltion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Chilltion API key and may expose account, session, or credit information through API calls. <br>
Mitigation: Provide credentials only when you intend to use Chilltion, keep the key private, and review returned session or account data before sharing it. <br>
Risk: Creating video sessions or calling unlisted API endpoints may consume Chilltion credits. <br>
Mitigation: Confirm the user wants to start a session or endpoint call, and check balance or session cost when credit usage matters. <br>
Risk: Changing CHILLTION_BASE_URL can send credentials and prompts to a non-official service. <br>
Mitigation: Keep CHILLTION_BASE_URL set to https://chilltion.com unless the alternative endpoint is controlled and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dragondean/generate-free-ai-video-via-chilltion) <br>
- [Publisher profile](https://clawhub.ai/user/dragondean) <br>
- [Chilltion service](https://chilltion.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Chilltion session identifiers, video URLs, chat URLs, SSE event data, credit balances, and cost records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
