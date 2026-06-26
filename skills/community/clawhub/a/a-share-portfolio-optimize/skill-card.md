## Description: <br>
A-share portfolio optimization skill that helps agents analyze a user-provided stock pool, estimate return and risk statistics, and produce optimized allocation weights using mean-variance, minimum-variance, risk-parity, equal-weight, and optional Black-Litterman methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzswk](https://clawhub.ai/user/yzswk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent builders use this skill to produce informational A-share portfolio analysis, optimized asset weights, risk contribution summaries, efficient-frontier context, and concise or report-style allocation outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat optimized allocation output as personalized investment advice. <br>
Mitigation: Present results as informational portfolio analysis and include a clear investment-risk disclaimer in both brief and formal outputs. <br>
Risk: Historical return and covariance estimates can be unstable and may produce misleading optimized weights. <br>
Mitigation: State that past performance does not predict future returns, prefer minimum-variance or risk-parity methods when return estimates are weak, and use at least a one-year data window when available. <br>
Risk: Black-Litterman outputs can be unreliable without explicit user views and confidence assumptions. <br>
Mitigation: Use Black-Litterman only when the agent captures the required view and confidence inputs; otherwise choose another supported optimization method. <br>
Risk: The workflow depends on a separate cn-stock-data helper and Python data-science dependencies. <br>
Mitigation: Verify the helper and dependencies before execution and review generated shell commands before running them locally. <br>


## Reference(s): <br>
- [A-share portfolio optimization reference guide](references/portfolio-optimize-guide.md) <br>
- [ClawHub skill release page](https://clawhub.ai/yzswk/a-share-portfolio-optimize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown narrative with tables and optional JSON optimization results from the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include portfolio weights, risk contributions, asset statistics, correlation matrices, efficient-frontier summaries, disclaimers, and command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
