## Description: <br>
Exact-match bug bounty triage workflow for Code4rena, Sherlock, HackenProof, Cantina-style security reviews, Solidity/EVM targets, and vulnerability report prep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n8gendegen](https://clawhub.ai/user/n8gendegen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External security researchers, bounty hunters, smart contract auditors, DeFi teams, and agent operators use this skill to prioritize bounty targets, triage candidate findings, prepare submission checklists, and draft credible finding reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security findings may be submitted or shared before impact, severity, and exploitability are manually verified. <br>
Mitigation: Require runnable proof-of-concept evidence, responsible disclosure approval, and manual severity review before any submission. <br>
Risk: Sensitive exploit details, secrets, or private keys could be exposed in public examples or reports. <br>
Mitigation: Exclude secrets, private keys, undisclosed live exploit details, and any non-public target information from generated materials. <br>
Risk: Commands or operational actions referenced by the skill may be run in sensitive repositories when not intended. <br>
Mitigation: Review proposed commands before allowing moderation actions, production deployments, migrations, GitHub publishing, or broad autoreview runs. <br>


## Reference(s): <br>
- [AtlasAgentSuite Skill Page](https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=bug-bounty-triage) <br>
- [ClawHub Skill Listing](https://clawhub.ai/n8gendegen/bug-bounty-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown triage notes, checklists, scoring rubrics, priority queues, and report skeletons] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewed triage guidance rather than executable exploit actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
