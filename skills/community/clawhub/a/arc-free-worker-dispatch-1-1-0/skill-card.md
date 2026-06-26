## Description: <br>
Routes agent tasks to free OpenRouter models for content writing, research, code generation, and other delegated work to help reduce primary model costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate writing, research, code generation, analysis, and batch tasks to OpenRouter-hosted free models while reserving higher-cost primary models for strategy and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch mode can bypass the skill's free-model promise. <br>
Mitigation: Manually review batch JSON and keep batch model values to known free model IDs until batch model validation is fixed. <br>
Risk: Batch output writes use weaker file-safety controls. <br>
Mitigation: Use disposable output paths and review output destinations before running batch jobs. <br>
Risk: Prompts and task content are sent to OpenRouter-hosted models. <br>
Mitigation: Use a limited OpenRouter key and do not send secrets, credentials, or confidential code. <br>
Risk: Free model output can be incorrect or misleading. <br>
Mitigation: Review generated text, code, and research before publishing, executing, or relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/arc-free-worker-dispatch-1-1-0) <br>
- [Publisher profile](https://clawhub.ai/user/Sieyer) <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files] <br>
**Output Format:** [Plain text or JSON on stdout, with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and OPENROUTER_API_KEY; task output may include model, token, and timing metadata when JSON mode is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
