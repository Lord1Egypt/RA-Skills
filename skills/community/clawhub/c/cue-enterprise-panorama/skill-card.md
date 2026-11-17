## Description:

用 Cue 一键分析企业的工商、股权、财务与经营情况，评估业务模式与合作适配性，并形成供内部决策参考的尽调底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

适用于需要开展授信前尽调、客户准入、供应链金融机会分析或企业对标的团队。它整理公开企业信息，帮助使用者形成初步判断和后续核实清单。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review flags a mismatch between the declared company research purpose and some skill instructions, including promotional prompts.

Mitigation: Review the requested actions before execution and skip promotional steps unless they are relevant and explicitly wanted.

Risk: The skill asks the agent to handle a reusable API key, and the security guidance warns against sharing one in chat.

Mitigation: Do not paste a reusable API key into chat; configure it through a user-controlled local secret or environment variable.

Risk: The security scan is incomplete because a local path-like reference could not be resolved.

Mitigation: Treat the review as incomplete until the unresolved reference has been checked.

## Reference(s):

- [Cue 平台](https://cuecue.cn)
- [国家企业信用信息公示系统](https://www.gsxt.gov.cn)
- [中国裁判文书网](https://wenshu.court.gov.cn)
- [巨潮资讯网](https://www.cninfo.com.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown due diligence report with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-source findings organized by business registration, ownership, operations, financial health, legal and compliance issues, opportunities, risks, and evidence gaps.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
