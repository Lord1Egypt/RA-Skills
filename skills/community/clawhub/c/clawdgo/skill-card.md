## Description: <br>
ClawdGo is a Chinese cybersecurity-training companion that guides one lobster persona through 3 layers, 12 risk dimensions, and modes W plus A-H. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nrt2024](https://clawhub.ai/user/nrt2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security learners and operators use this skill for structured cybersecurity awareness training, scenario practice, self-assessment, teaching explanations, and local red-blue practice across phishing, social engineering, privacy, credential, supply-chain, and response topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep persistent local training memory, including runtime profile, state, generated scenario, and soul.md anchor data. <br>
Mitigation: Review the stored files before and after use, and install only where persistent local training records are acceptable. <br>
Risk: B-mode drills may configure a real scheduled training job after user interaction. <br>
Mitigation: Enable B-mode scheduling only with explicit intent, and inspect or disable local cron jobs if scheduled drills are not wanted. <br>
Risk: Broad trigger phrases can route normal conversation into the training experience. <br>
Mitigation: Review the trigger list before deployment and limit use to environments where the ClawdGo interaction model is expected. <br>


## Reference(s): <br>
- [ClawdGo ClawHub release](https://clawhub.ai/nrt2024/clawdgo) <br>
- [nrt2024 publisher profile](https://clawhub.ai/user/nrt2024) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Dimension prompts](artifact/references/dimension-prompts.md) <br>
- [Scenario schema](artifact/references/scenarios/_schema.md) <br>
- [A mode flow](artifact/references/a-mode-flow.md) <br>
- [B mode flow](artifact/references/b-mode-flow.md) <br>
- [C mode flow](artifact/references/c-mode-flow.md) <br>
- [D mode flow](artifact/references/d-mode-flow.md) <br>
- [F mode flow](artifact/references/f-mode-flow.md) <br>
- [W mode rules](artifact/references/w-mode-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown and structured text training cards, with occasional shell commands or configuration steps for explicitly requested local scheduling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only runtime; may write local runtime profile, state, scenario, and soul.md anchor files during training flows.] <br>

## Skill Version(s): <br>
1.3.2 (source: frontmatter, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
