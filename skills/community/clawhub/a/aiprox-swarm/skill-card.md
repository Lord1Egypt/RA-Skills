## Description: <br>
40-persona prediction engine for binary market questions. Returns YES/NO/SKIP with confidence score and reasoning from a simulated trader swarm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit binary market questions and receive a structured YES, NO, or SKIP prediction with confidence, reasoning, voter summary, detected domain, and groupthink warning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts and context are sent to a third-party market-analysis service. <br>
Mitigation: Do not include confidential, regulated, or sensitive personal data in market questions or context. <br>
Risk: The skill requires an AIPROX_SPEND_TOKEN for authenticated or billable access. <br>
Mitigation: Store the token in the environment, avoid committing it to files, and confirm the spend-token model before relying on it for billing or access control. <br>
Risk: Prediction outputs may be incorrect or misleading for financial, political, sports, or macro decisions. <br>
Mitigation: Treat outputs as decision-support analysis, verify against independent sources, and avoid using the prediction as the sole basis for high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unixlamadev-spec/aiprox-swarm) <br>
- [Publisher profile](https://clawhub.ai/user/unixlamadev-spec) <br>
- [AIProx homepage](https://aiprox.dev) <br>
- [AIProx orchestration endpoint](https://aiprox.dev/api/orchestrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with curl examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The service response includes prediction, confidence, reasoning, voter_summary, domain, persona_count, and groupthink_warning fields.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
