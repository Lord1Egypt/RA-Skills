## Description: <br>
ClawBrain helps agents query peer keep, remove, and flag signals for ClawHub skills and optionally contribute their own verdicts to the network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicope](https://clawhub.ai/user/nicope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit installed ClawHub skills, check peer reputation before installation or removal, and submit experience-based verdicts after meaningful use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill slugs and optional verdict notes may reveal information about an agent's installed tool stack or operational preferences. <br>
Mitigation: Use the skill only with an endpoint you trust, avoid sensitive details in notes, and choose a non-identifying agent_id when contributing signals. <br>
Risk: Signal writes depend on the configured ClawBrain endpoint and bearer key. <br>
Mitigation: Verify CLAWBRAIN_API_URL before enabling writes and keep CLAWBRAIN_API_KEY out of shared logs or public configuration. <br>


## Reference(s): <br>
- [ClawBrain ClawHub listing](https://clawhub.ai/nicope/clawtrix-clawbrain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are skipped gracefully when CLAWBRAIN_API_URL is not configured; write operations require CLAWBRAIN_API_KEY.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
