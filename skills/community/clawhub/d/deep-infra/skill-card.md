## Description: <br>
Configure DeepInfra model routing with provider auth, model selection, fallback chains, and cost-aware defaults for stable open-source and frontier model workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ats3v](https://clawhub.ai/user/ats3v) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenAI-compatible workflows to DeepInfra, choose models by workload, define fallback chains, and control cost drift over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text and selected model metadata are sent to DeepInfra when inference is requested. <br>
Mitigation: Use the skill only for data you are comfortable sending to DeepInfra, and do not include API keys, passwords, personal records, or regulated data in prompts. <br>
Risk: Local routing notes can accumulate operational preferences and incident history under ~/deep-infra/. <br>
Mitigation: Periodically review the local memory file and keep notes limited to routing decisions, outcomes, and non-secret configuration preferences. <br>
Risk: Model routing mistakes, excessive retries, or broad premium-model use can increase cost. <br>
Mitigation: Set budget ceilings by workload, keep fallback chains short, and verify routing changes with a small prompt set before broader use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ats3v/deep-infra) <br>
- [DeepInfra OpenAI-compatible API](https://api.deepinfra.com/v1/openai/) <br>
- [DeepInfra model catalog endpoint](https://api.deepinfra.com/v1/openai/models) <br>
- [DeepInfra chat completions endpoint](https://api.deepinfra.com/v1/openai/chat/completions) <br>
- [DeepInfra dashboard](https://deepinfra.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and DEEPINFRA_API_KEY for verification examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
