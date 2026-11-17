## Description:

Simulates Delonix executive decision perspectives, debates, and meeting participation using role cards, decision-chain heuristics, and confidence labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can ask an agent to generate simulated executive viewpoints, multi-person debate reports, meeting reactions, or new role-card drafts for Delonix strategy, operations, membership, AI investment, asset management, and cost-control questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use private or internal communications to create reusable executive profiles without clear authorization, minimization, or retention controls.

Mitigation: Use only in an approved internal environment with documented authorization from the organization or data owner, and restrict Feishu access to explicitly approved documents and channels.

Risk: Role simulations could be mistaken for real statements or used as colleague assessments.

Mitigation: Keep the required simulated-viewpoint label on outputs, prohibit private or one-to-one chats and colleague assessments by default, and require human review before sharing or archiving outputs.

Risk: Generated role profiles may retain sensitive source material longer than needed.

Mitigation: Apply review, redaction, retention, and deletion controls before archiving any role profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/skills/dalao)
- [Publisher profile](https://clawhub.ai/user/chaoliuzhu)
- [黎柱蒸馏角色卡](artifact/references/lizhu.md)
- [张琦 role source](https://www.feishu.cn/docx/P1mFd800MoyDGGxpiQ3c9rU2nCe)
- [毛新凯 role source](https://delonix.feishu.cn/docx/EQoedHHcyozLVhxCCmici2MDnPc)
- [李和聪 role source](https://www.feishu.cn/docx/SUUvdYKCho23qGxqN7BcBs78nWc)
- [郑南雁 role source](https://delonix.feishu.cn/docx/EqQ7d4akgoMqWpxSdyZcks6WnOe)
- [段纹瑾 role source](https://www.feishu.cn/docx/RetJdTk0IoAz7Px45ZBc00Dpngd)
- [孟令航 role source](https://delonix.feishu.cn/docx/VOMidRzFxoJZ0Nx5R6CcGebtnjh)
- [韩俏帆 role source](https://delonix.feishu.cn/docx/Ew9CdUrVAoBWoexLDUMcQSodnNg)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured simulated viewpoints, debate reports, meeting reactions, and YAML-style role-card drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to label simulated viewpoints, include confidence ratings, and cite decision-chain basis from the role cards.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
