## Description: <br>
Manage Apple Search Ads campaigns, ad groups, keywords, and reports via the asa-cli tool. Use when the user asks about Apple Search Ads management, campaign operations, keyword bidding, ASA reports, or ad performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TrebuhS](https://clawhub.ai/user/TrebuhS) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External advertisers, marketers, and developers use this skill to have an agent operate Apple Search Ads workflows through asa-cli, including campaign, ad group, keyword, negative keyword, reporting, and account-configuration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, update, delete, pause, or modify Apple Search Ads campaigns, ad groups, keywords, bids, and budgets. <br>
Mitigation: Require manual approval before any command that creates, updates, deletes, changes status, changes bids, or changes budgets. <br>
Risk: The skill depends on asa-cli credentials and local configuration files that may include sensitive Apple Search Ads access material. <br>
Mitigation: Use least-privileged credentials, protect ~/.asa-cli files, and install only when the asa-cli binary is trusted. <br>
Risk: Multi-org or multi-profile accounts can lead an agent to operate on the wrong Apple Search Ads organization. <br>
Mitigation: Run whoami, verify the selected profile and org ID, and pass --org-id explicitly for multi-org accounts before approving account-changing commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TrebuhS/apple-search-ads-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/TrebuhS) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline asa-cli commands, command reference sections, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require asa-cli credentials, an Apple Search Ads organization ID, and manual approval before account-changing operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
