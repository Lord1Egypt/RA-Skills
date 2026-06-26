## Description: <br>
ClawBrain Pro configures OpenClaw with memory, data fidelity checks, automatic error recovery, and output validation for more reliable agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelfeng](https://clawhub.ai/user/michaelfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to configure ClawBrain models, manage persistent memory and recall, diagnose configuration health, and benchmark agent behavior across realistic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw prompts, images, and diagnostic requests may be sent to the ClawBrain/FactorHub service. <br>
Mitigation: Install only when third-party processing is acceptable, use a dedicated API key, and avoid sending secrets or regulated data. <br>
Risk: Conversation-derived facts may be remembered across sessions through the long-term memory features. <br>
Mitigation: Review memory management and deletion options before use, and avoid storing sensitive personal, customer, or regulated information. <br>
Risk: Benchmark and doctor workflows may involve commands, file changes, package installs, network calls, or messages without clearly documented limits. <br>
Mitigation: Run these workflows in a test workspace and require explicit approval before executing commands, changing files, installing packages, making network calls, or sending messages. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/michaelfeng/clawbrain-pro) <br>
- [ClawBrain homepage from ClawHub metadata](https://github.com/michaelfeng/clawbrain) <br>
- [ClawBrain dashboard](https://clawbrain.dev/dashboard) <br>
- [OpenClaw model comparison report](https://clawbrain.dev/blog/openclaw-model-comparison) <br>
- [ClawBrain product site](https://clawbrain.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell/API command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw model configuration, API-key setup guidance, benchmark instructions, and diagnostic command examples.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
