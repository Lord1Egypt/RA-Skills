## Description: <br>
Fetch LLM benchmarks and pricing from the Artificial Analysis API and sync them to a Feishu Bitable table for model catalog updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neymar011ren](https://clawhub.ai/user/neymar011ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, solution, and operations teams use this skill to build or refresh a Feishu Bitable catalog of LLM model benchmarks, pricing, speed, and provider metadata from Artificial Analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships with a prefilled Feishu Bitable target and can update records in that table. <br>
Mitigation: Clear or replace the bundled bitable-config.json values and confirm the target Base and table before running updates. <br>
Risk: The skill requires sensitive credentials for the Artificial Analysis API. <br>
Mitigation: Use an environment variable or managed secret store when policy requires it, and avoid committing real API keys to credential files. <br>


## Reference(s): <br>
- [Artificial Analysis API Reference](https://artificialanalysis.ai/api-reference) <br>
- [Artificial Analysis](https://artificialanalysis.ai/) <br>
- [LLM Models API Endpoint](https://artificialanalysis.ai/api/v2/data/llms/models) <br>
- [Feishu Bitable Setup](references/bitable-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/neymar011ren/artificial-analysis-models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON payloads for Feishu Bitable records and field definitions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Artificial Analysis API key and Feishu Bitable access; uses cached API responses to reduce repeated full pulls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
