## Description: <br>
Discover new ideas, sources, opportunities, and angles with durable watchlists, novelty rules, and heartbeat-backed finding logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain durable discovery topics, apply novelty filters, and log only new findings that may change a decision, risk assessment, opportunity search, or next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent discovery memory may retain sensitive interests, plans, or personal context in ~/discover/. <br>
Mitigation: Store only durable discovery preferences and findings; avoid secrets and sensitive personal details in local discovery files. <br>
Risk: Broad activation language could make discovery behavior appear in more conversations than intended. <br>
Mitigation: Keep AGENTS.md routing narrow, review any proposed routing changes, and activate durable discovery only for topics with a clear decision, risk, or opportunity. <br>
Risk: Heartbeat checks can create recurring monitoring noise or scope drift if enabled too broadly. <br>
Mitigation: Enable heartbeat only for specific approved topics with a clear novelty bar and use HEARTBEAT_OK when nothing materially changed. <br>
Risk: External lookups may send topic keywords or query variants to public search and source services. <br>
Mitigation: Keep lookup scope narrow, tied to active watchlist topics, and ask before using paid tools, contacting third parties, or taking actions beyond research and logging. <br>


## Reference(s): <br>
- [ClawHub Discover listing](https://clawhub.ai/ivangdavila/discover) <br>
- [Discover homepage](https://clawic.com/skills/discover) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update local discovery memory, watchlists, heartbeat state, and findings when approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
