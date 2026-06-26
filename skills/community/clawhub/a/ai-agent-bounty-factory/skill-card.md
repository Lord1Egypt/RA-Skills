## Description: <br>
AI Agent Bounty Factory discovers, scores, previews, and locally records proposal submissions for freelance AI task bounties across listed marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to evaluate freelance AI task bounties, generate proposal drafts, and track proposal and earnings status. It is most appropriate for reviewed proposal workflows rather than unsupervised live marketplace submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises autonomous marketplace submissions and staking-like workflows, while the included script simulates submissions locally. <br>
Mitigation: Use discovery and proposal preview by default, and add explicit live or dry-run separation before connecting marketplace APIs. <br>
Risk: Auto-submission or instant workflows could submit unreviewed proposals or create financial exposure if adapted to live services. <br>
Mitigation: Require manual approval, truthful proposal review, platform compliance checks, and spending or staking limits before submit-all or instant workflows are enabled. <br>
Risk: Broad marketplace credentials could expand the impact of misuse or configuration mistakes. <br>
Mitigation: Use least-privilege API keys, avoid broad credentials, and keep credentials out of tracker and proposal output files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/ai-agent-bounty-factory) <br>
- [AI Agent Bounty Factory README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files] <br>
**Output Format:** [CLI text output, Markdown proposal drafts, and JSON tracker files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local tracker and earnings files configured with BOUNTY_TRACKER and BOUNTY_EARNINGS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
