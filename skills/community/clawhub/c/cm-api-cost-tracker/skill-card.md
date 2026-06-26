## Description: <br>
Track, analyze, and optimize AI API costs across OpenAI, Anthropic, OpenRouter, Google, and other LLM providers using local billing exports, usage logs, or API response files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering teams, and operations users use this skill to inspect LLM provider usage, break down spend by model or time period, detect trends, and generate cost optimization reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Billing exports and usage logs may contain sensitive spending patterns, model choices, and operational metadata. <br>
Mitigation: Run the analyzer locally on explicit export files, keep those files out of shared folders, and review generated reports before sharing. <br>
Risk: The documented API-key auto mode may lead users to expect live provider access that is not implemented in the reviewed script. <br>
Mitigation: Use explicit local usage or billing export files and do not rely on API-key auto mode for collection. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/charlie-morrison/cm-api-cost-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Guidance] <br>
**Output Format:** [Terminal tables, Markdown reports, JSON objects, or CSV-style tabular output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include cost breakdowns, trend summaries, budget warnings, top-spender lists, and model substitution suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
