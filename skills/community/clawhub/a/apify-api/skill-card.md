## Description: <br>
Apify API integration with managed authentication for running web scrapers and managing actors, datasets, key-value stores, schedules, and related Apify resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to interact with Apify through Maton-managed authentication, run or monitor actors, and manage datasets, storage, request queues, schedules, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Maton API key grants access to the connected Apify account. <br>
Mitigation: Keep MATON_API_KEY secret and do not place it in client-side code, shared logs, or public repositories. <br>
Risk: Actor runs can spend Apify credits and destructive API calls can modify or delete account resources. <br>
Mitigation: Confirm actor runs, deletions, and other write operations with the user before execution. <br>
Risk: Schedules and webhooks can continue operating after the conversation ends. <br>
Mitigation: Review existing schedules and webhooks before changes, and confirm creation or modification of persistent resources. <br>
Risk: Multiple Apify connections can cause actions to target the wrong account. <br>
Mitigation: Specify the intended Maton-Connection header whenever more than one connection exists. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/apify-api) <br>
- [Maton](https://maton.ai) <br>
- [Apify API Reference](https://docs.apify.com/api/v2) <br>
- [Apify Actors Documentation](https://docs.apify.com/actors) <br>
- [Apify Storage Documentation](https://docs.apify.com/storage) <br>
- [Apify Schedules Documentation](https://docs.apify.com/schedules) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, HTTP examples, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access; outputs may include Apify resource identifiers, connection headers, and account-specific API responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
