## Description: <br>
Check coding-model API quality, capability fit, and drift with LT-lite and B3IT-lite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chekhovin](https://clawhub.ai/user/chekhovin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to verify whether OpenAI, OpenAI-compatible, or Anthropic-style coding-model endpoints support smoke checks, first-token detection, logprob-based LT-lite checks, and baseline-vs-current drift monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials and generated reports may expose provider keys or sensitive endpoint details. <br>
Mitigation: Use scoped test keys, keep provider configuration and output directories out of source control and shared hosting, and rotate any key that may have been printed to logs or published. <br>
Risk: Batch and daily output files may be shared before their contents are reviewed. <br>
Mitigation: Review generated batch, daily, JSON, and HTML files before publishing or attaching them to issues, reports, or support requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chekhovin/api-quality-check) <br>
- [Config Schema](references/config-schema.md) <br>
- [Endpoint Types Playbook](references/endpoint-types-playbook.md) <br>
- [Kimi Anthropic Quickstart](references/kimi-anthropic-quickstart.md) <br>
- [Kimi Coding Quickstart](references/kimi-coding-quickstart.md) <br>
- [Workflow Notes](references/workflows.md) <br>
- [Example Provider List](references/providers.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with command examples and file-based JSON/HTML report outputs from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include provider configuration files, smoke-test reports, LT-lite and B3IT-lite baselines, drift reports, and HTML summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
