## Description: <br>
Fund Report helps an agent report real-time OTC fund net value estimates and estimated price changes for multiple fund codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wndagg](https://clawhub.ai/user/wndagg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to run a fund holdings report workflow for multiple OTC fund codes and summarize estimated NAV movement, price changes, and gains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release package does not include the referenced scripts/fund_report.py implementation for review. <br>
Mitigation: Inspect the external script and its dependencies before execution, especially network access and any locally configured fund lists. <br>
Risk: Financial quote or fund data may be stale, unavailable, or unsuitable for investment decisions. <br>
Mitigation: Treat generated fund reports as informational and verify values against authoritative financial data sources before acting on them. <br>


## Reference(s): <br>
- [ClawHub Fund Report Release Page](https://clawhub.ai/wndagg/fund-report) <br>
- [Project Homepage Listed by Skill Metadata](https://github.com/wNDAGG/mimi-scripts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The submitted package is documentation-only and references an external scripts/fund_report.py file that was not included for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
