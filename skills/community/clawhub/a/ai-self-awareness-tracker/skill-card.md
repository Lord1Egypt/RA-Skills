## Description: <br>
小Z的元认知置信度检测模块会评估回答置信度，并在低置信度回答前添加不确定标记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freak30](https://clawhub.ai/user/freak30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders can use this skill to add a lightweight confidence check that flags low-confidence answers before they are sent. It is intended for uncertainty signaling around generated responses, not for proving answer correctness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions and generated answers can be sent to MiniMax through the local `mmx` CLI using the user's API key. <br>
Mitigation: Use only with conversations that are acceptable to send to MiniMax, and disable or review the checker for confidential chats. <br>
Risk: The artifact privacy section under-discloses the question data sent during consistency checks. <br>
Mitigation: Document the CLI, credential, and data-sharing behavior clearly before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/freak30/ai-self-awareness-tracker) <br>
- [UQLM PTrueScorer project](https://github.com/cvs-health/uqlm) <br>
- [arXiv:2602.17431](https://arxiv.org/abs/2602.17431) <br>
- [arXiv:2604.13068](https://arxiv.org/abs/2604.13068) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [JSON and text guidance from a Python confidence-checking helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May add an uncertainty marker when confidence is below the configured threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
