## Description: <br>
Fund Signal Monitor documents passive monitoring for fund reports, manager changes, size changes, performance volatility, and style drift, with alerts that hand off to fund-analyzer-pro for deeper analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to configure and describe passive fund-signal monitoring for watchlisted funds, including reports, manager changes, size changes, volatility, and style drift. It is intended to produce concise alert guidance and route users to fund-analyzer-pro for deeper analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fund alerts may be stale, incomplete, or inaccurate if fund events are not checked against official disclosures. <br>
Mitigation: Verify fund reports, manager changes, size changes, and other events against official fund-company disclosures before acting on an alert. <br>
Risk: The operational monitor is documented as a separate fund-analyzer-pro implementation that may use credentials, push destinations, watchlists, and scheduled monitoring. <br>
Mitigation: Review fund-analyzer-pro signal_checker.py separately, confirm credential and push-destination handling, verify watchlist storage and encryption, and confirm how scheduled monitoring can be disabled or removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/fund-signal-monitor) <br>
- [Repository URL listed in clawhub.yaml](https://github.com/lj22503/one-person-ceo-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown alerts, YAML configuration examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only release; operational monitoring depends on the separately referenced fund-analyzer-pro signal_checker.py implementation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence, SKILL.md frontmatter, clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
