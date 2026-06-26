## Description: <br>
Optimizes 1688 product titles by generating rule-based hot-keyword suggestions and LLM rewrite suggestions for comparison before a user applies a title. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 sellers and operators use this skill to review alternative product-title optimizations, compare keyword-based and LLM-generated suggestions, and confirm a selected title before any live listing update. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1688 access key and may store it in OpenClaw configuration or read it from environment variables. <br>
Mitigation: Use a scoped or rotatable key when available, keep local configuration protected, and rotate the key if it is exposed. <br>
Risk: The skill sends product IDs and title-related data to the 1688 skills gateway for optimization. <br>
Mitigation: Install only when that data flow is acceptable and verify the configured gateway is trusted before use. <br>
Risk: Generated title suggestions may be inaccurate, misleading, or unsuitable for a live listing. <br>
Mitigation: Review the original and proposed title carefully and require explicit user confirmation before applying any listing update. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/1688aiinfra/1688-item-title-optimizer) <br>
- [1688aiinfra publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [Interaction specifications](artifact/references/interaction-specs.md) <br>
- [Title optimizer Q&A](artifact/references/title_optimizer_qa.md) <br>
- [LLM title optimizer reference](artifact/references/title_llm_SKILL.md) <br>
- [Rule-based title optimizer reference](artifact/references/title_wo_llm_SKILL.md) <br>
- [Optimize title capability](artifact/capabilities/optimize_title.md) <br>
- [Optimize title LLM capability](artifact/capabilities/optimize_title_llm.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON command results and CLI invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured 1688 AK and product IDs; title suggestions should be reviewed and confirmed before applying to a live listing.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
