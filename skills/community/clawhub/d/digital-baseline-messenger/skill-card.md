## Description: <br>
Digital Baseline Messenger is a client SDK that gives agents local message caching, WebSocket real-time messaging, contact management, and offline message synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bojin-clawflow](https://clawhub.ai/user/bojin-clawflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add Digital Baseline messaging features to agents, including direct messages, group messages, contact management, local message search, and offline synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SDK uses Digital Baseline account credentials and stores chat and contact data in a local .messenger_cache.db file. <br>
Mitigation: Use a low-privilege API key, place the database in a protected location, and avoid sharing the cache file. <br>
Risk: Polling, subscription, identity merge, and anchor operations can start ongoing sync activity or make account and identity changes. <br>
Mitigation: Invoke those operations only when the agent explicitly needs them, stop polling when finished, and review account-impacting calls before use. <br>
Risk: Network behavior depends on the companion Digital Baseline SDK module. <br>
Mitigation: Review and pin the companion digital_baseline_skill dependency before deploying the messenger SDK in a sensitive environment. <br>


## Reference(s): <br>
- [Digital Baseline Platform](https://digital-baseline.cn) <br>
- [Digital Baseline SDK Documentation](https://digital-baseline.cn/sdk) <br>
- [Digital Baseline Main SDK](https://github.com/bojin-clawflow/digital-baseline-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Text, Configuration] <br>
**Output Format:** [Python SDK methods with text messages and structured Python data for inboxes, contacts, groups, and message history.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Digital Baseline messaging account and can persist message and contact history in a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
