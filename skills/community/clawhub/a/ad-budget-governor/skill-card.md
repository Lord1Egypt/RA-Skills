## Description: <br>
Cross-platform rolling ad-spend cap that blocks overspend across multiple ad platforms combined, not just per-platform daily limits. Fails closed on unreadable spend data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roberthill0475-lang](https://clawhub.ai/user/roberthill0475-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to gate agent-driven ad spend across multiple advertising platforms against one rolling budget cap before spend actions execute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roberthill0475-lang/skills/ad-budget-governor) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Python module with Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. Configure LEDGER_PATHS narrowly to intended ad-spend ledger files and restrict set_cap access to trusted operators or workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
