## Description: <br>
Run Apify Actors, manage tasks, inspect datasets and key-value stores, and review usage via the Apify API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation users use this skill to connect an Apify account through ClawLink, discover available Apify tools, run Actors or tasks, inspect datasets and stores, and manage scraping workflow resources from chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on ClawLink storing and using the user's Apify API key for authenticated requests. <br>
Mitigation: Install only if the user trusts ClawLink with Apify credentials, and revoke the credential in Apify or ClawLink when access is no longer needed. <br>
Risk: Actor runs, writes, and deletes can change Apify resources or incur compute costs. <br>
Mitigation: Use the described preview and confirmation flow before launches, writes, or destructive actions, and verify the target resource and intended effect before execution. <br>
Risk: Large or long-running Actor jobs can exceed synchronous run limits. <br>
Mitigation: Prefer asynchronous runs for large datasets or long scraping jobs, then inspect run status, logs, and dataset output after launch. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/apify-actors) <br>
- [Apify API Documentation](https://docs.apify.com/api/v2) <br>
- [Apify Platform](https://apify.com/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Apify resource data, run logs, dataset items, usage information, and confirmation prompts through ClawLink tool calls.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
