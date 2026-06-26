## Description: <br>
Fathom API integration with managed OAuth for accessing meeting recordings, transcripts, summaries, action items, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Fathom meeting content, search recordings, and manage webhook notifications through Maton-managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Fathom meeting recordings, transcripts, summaries, and related account data through Maton-managed OAuth. <br>
Mitigation: Install only for intended Fathom accounts, keep MATON_API_KEY private, and review retrieved meeting content before sharing or storing it. <br>
Risk: Webhook creation or destination_url callbacks can send meeting fields to an external URL. <br>
Mitigation: Before approving webhook or callback operations, confirm the exact URL, the included meeting fields, and how the webhook can be deleted. <br>


## Reference(s): <br>
- [Maton](https://maton.ai) <br>
- [Fathom API Documentation](https://developers.fathom.ai) <br>
- [Fathom LLM Reference](https://developers.fathom.ai/llms.txt) <br>
- [ClawHub Fathom Skill](https://clawhub.ai/byungkyu/fathom-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline Python, JavaScript, HTTP, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access; API responses are JSON from Maton and Fathom.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
