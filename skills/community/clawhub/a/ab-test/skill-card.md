## Description: <br>
Manage A/B tests for marketing and product experiments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, product, and experimentation teams use this skill to manage A/B testing workflows, configure required API access, and run test-related command-line tasks that return JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys could be exposed if pasted into chat, committed to files, or stored in unprotected environments. <br>
Mitigation: Store AB_API_KEY in a protected environment variable or secret manager and avoid including secrets in prompts, logs, or source files. <br>
Risk: Proposed experiment changes could affect marketing or product decisions if applied without review. <br>
Mitigation: Review test setup, targeting, and result interpretation before applying changes or acting on exported results. <br>
Risk: The artifact describes running scripts/ab_test.py, but that script is not included in the submitted artifact. <br>
Mitigation: Confirm the required runtime files are available in the deployment environment before depending on command execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/ab-test) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with bash examples and JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API key configuration through a protected environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
