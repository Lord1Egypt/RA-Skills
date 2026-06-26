## Description: <br>
Use when a task adds, upgrades, removes, or reviews software dependencies and the agent should apply a Socket-based supply-chain guardrail before changing manifests or lockfiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuthan](https://clawhub.ai/user/tuthan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to review proposed dependency additions, upgrades, removals, or transient install commands before manifest or lockfile changes are made. It guides the agent to prefer existing project capabilities, run Socket-based checks, and block or escalate risky dependency changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Socket credentials or GitHub integration keys could be exposed if pasted into prompts or committed in workflow configuration. <br>
Mitigation: Use Socket login or environment variables for local CLI authentication, use GitHub secrets for CI keys, and avoid placing private tokens in prompts. <br>
Risk: Dependency changes may be made without a reliable Socket result when tooling is unavailable or reports are incomplete. <br>
Mitigation: Require human review before changing manifests or lockfiles when Socket tooling, category scores, or dependency reports are unavailable. <br>
Risk: CI scanning can request pull request and issue write permissions when comments or GitHub integration behavior are enabled. <br>
Mitigation: Review GitHub Actions permissions and enable write scopes only when CI comments or issue/PR updates are required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tuthan/dependency-guard) <br>
- [Publisher Profile](https://clawhub.ai/user/tuthan) <br>
- [Canonical Policy](references/policy.md) <br>
- [Decision Matrix](references/decision-matrix.md) <br>
- [Example Review Format](references/examples.md) <br>
- [GitHub Actions Example](examples/github/dependency-guard.yml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown review summaries with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Socket CLI or host-provided MCP dependency scoring for automated review; otherwise the skill directs the agent to request human review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
