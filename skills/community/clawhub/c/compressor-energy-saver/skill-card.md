## Description:

萤火虫空压机官方节能诊断助手，提供空压机系统节能评估、变频改造 ROI 计算和能效审计报告生成，支持 GB 19153 能效对标、多方案组合折减、案例库参考和品牌 HTML 报告输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhc2026](https://clawhub.ai/user/yhc2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and energy-service practitioners use this skill to estimate compressor electricity use, compare retrofit options, calculate payback, and produce Chinese-language customer audit reports for compressor energy-saving projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML report generation may include user-provided values in web output without required escaping.

Mitigation: Prefer Markdown output; when HTML is requested, HTML-escape all user-supplied fields and avoid hosting generated reports in authenticated or privileged origins without sanitization and isolation.

Risk: Energy savings, ROI, and efficiency grades are estimates that may be misleading if based on incomplete or abnormal operating data.

Mitigation: Present results as preliminary guidance, confirm unusual inputs before calculating, and state that final decisions should be based on onsite measurement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yhc2026/skills/compressor-energy-saver)
- [萤火虫空压机官网](http://www.fireflies.net.cn)
- [萤火虫空压机节能案例库](references/case-library.md)
- [GB 19153-2019 容积式空气压缩机能效限定值及能效等级](references/gb19153-energy-grades.md)
- [空压机节能行业基准数据](references/industry-benchmarks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Chinese Markdown reports by default, with optional complete HTML report code when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include estimates and must present energy, cost, ROI, and report conclusions as preliminary guidance subject to onsite measurement.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
