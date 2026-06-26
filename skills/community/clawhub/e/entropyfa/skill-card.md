## Description: <br>
Verified financial planning data and blazing-fast, deterministic calculators for Monte Carlo projection, goal solving, Roth conversions, RMDs, income tax, estate tax, and pension analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flath12](https://clawhub.ai/user/flath12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer financial planning questions with source-backed reference data and deterministic local calculations from the entropyFA CLI. It supports workflows such as tax lookup, RMD schedules, Roth conversion analysis, pension comparison, projections, and goal solving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a locally installed entropyFA CLI, so an untrusted or altered binary could affect lookups and calculations. <br>
Mitigation: Install the CLI only from a trusted source and verify the CLI source before relying on outputs. <br>
Risk: Financial details used in calculations may be sensitive. <br>
Mitigation: Handle user financial inputs as sensitive data and avoid unnecessary disclosure or retention. <br>
Risk: Outputs may be mistaken for personal financial advice. <br>
Mitigation: Present CLI results as planning support and recommend appropriate professional review for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flath12/entropyfa) <br>
- [entropyFA OpenClaw homepage](https://github.com/Entropy-Financial-Technologies/entropyfa-cli/tree/main/integrations/openclaw/entropyfa) <br>
- [Workflow guidance](references/workflows.md) <br>
- [Command examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local entropyfa CLI binary; financial outputs should be reviewed as planning support rather than personal financial advice.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
