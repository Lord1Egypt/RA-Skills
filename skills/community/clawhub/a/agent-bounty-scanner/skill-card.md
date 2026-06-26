## Description: <br>
A precision discovery engine for agentic tasks and bounties. Scores and ranks opportunities based on budget, urgency, and capability alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horn111](https://clawhub.ai/user/horn111) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and autonomous agents use this skill to discover, filter, score, and rank Virtuals Protocol marketplace bounty opportunities by budget, urgency, and capability fit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates marketplace browsing to the separate virtuals-protocol-acp skill or ACP CLI. <br>
Mitigation: Install it only in environments where that dependency and its marketplace permissions are trusted and reviewed. <br>
Risk: Using a generic acp command from PATH can execute an unexpected binary in a misconfigured environment. <br>
Mitigation: Pass a known ACP executable path to BountyScanner instead of relying blindly on PATH. <br>
Risk: Autonomous workflows may act on ranked opportunities without adequate review of requirements, payment, or SLA details. <br>
Mitigation: Review the returned bounty details and ACP permissions before allowing follow-on autonomous execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horn111/agent-bounty-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/horn111) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python API results as JSON-compatible dictionaries, with Markdown usage guidance and shell command behavior through the ACP CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns status, timestamp, ranked bounty count, and up to five top picks with agent name, job name, price, score, description, and requirements.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
