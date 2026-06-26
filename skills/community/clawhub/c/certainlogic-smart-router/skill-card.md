## Description: <br>
Deprecated keyword-based router that recommends cheap, default, or powerful LLM model tiers for prompts and points users to replacement skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can classify prompts into model tiers with deterministic keyword and regex heuristics. This release is deprecated in favor of smart-router-coding and smart-router-intents for maintained routing behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is deprecated and may not receive maintained routing updates. <br>
Mitigation: Use smart-router-coding or smart-router-intents when maintained routing behavior is required. <br>
Risk: Untrusted custom config files can change routing profiles. <br>
Mitigation: Only pass custom config files from trusted sources and review profile rules before use. <br>
Risk: Static keyword and regex heuristics can misclassify edge cases or non-English prompts. <br>
Mitigation: Review the recommended tier for important prompts and use explicit overrides when the recommendation is unsuitable. <br>


## Reference(s): <br>
- [CertainLogic](https://certainlogic.ai) <br>
- [ClawHub package page](https://clawhub.ai/certainlogicai/certainlogic-smart-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration guidance] <br>
**Output Format:** [JSON object printed by a local CLI, with supporting shell commands and configuration examples in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends a model tier only; it does not call an LLM or route requests directly.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
