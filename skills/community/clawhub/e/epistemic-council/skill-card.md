## Description: <br>
Manage and execute Epistemic Council pipeline operations including status checks, claim validation, boundary audits, gap finding, and adversarial re-challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[su-ariel](https://clawhub.ai/user/su-ariel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run a local epistemic reasoning pipeline, inspect its status, validate claims, audit boundaries, find evidence gaps, and re-challenge high-risk insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases can invoke local Python pipeline scripts and write persistent files. <br>
Mitigation: Use the skill in a dedicated workspace and prefer explicit invocations for pipeline actions. <br>
Risk: Prompts may be sent to a local Ollama-compatible model service. <br>
Mitigation: Do not provide secrets or private documents unless the local model service and filesystem are trusted. <br>
Risk: Reasoning, audit, status, and run-log files may persist after execution. <br>
Mitigation: Review generated files before relying on their contents and clean the workspace according to local retention requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/su-ariel/epistemic-council) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with command examples and generated local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent reasoning, audit, status, and run-log files in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
