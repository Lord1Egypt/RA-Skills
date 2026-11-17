## Description:

Guides users through Beijing points-settlement eligibility, scoring, field validation, and planning using a bundled local HTML simulator or bounded text guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent51-commits](https://clawhub.ai/user/vincent51-commits)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to collect and validate Beijing points-settlement facts, interpret page-derived score results, and discuss unofficial planning scenarios. The skill supports a visual simulator workflow when the bundled HTML page is available and a narrower text-guidance workflow when it is not.

### Deployment Geography for Use:

Global; content is specific to Beijing, China.

## Known Risks and Mitigations:

Risk: Personal settlement-related details may remain in local browser storage after use.

Mitigation: Use a trusted device or browser profile and clear saved records when finished.

Risk: Users may mistake simulator or guidance output for an official Beijing points-settlement result.

Mitigation: Label outputs as unofficial simulation only and direct users to official or professional sources for final decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vincent51-commits/skills/beijing-jifen-consult)
- [Beijing Points-Settlement Local Simulator](artifact/assets/beijing-jifen-wizard.html)
- [北京积分落户 · 口径与查询](artifact/references/口径与查询.md)
- [北京积分落户 · 填写校验清单](artifact/references/填写校验清单.md)
- [北京人社公共服务](https://fuwu.rsj.beijing.gov.cn/bjdkhy/ggfw/)
- [北京市积分落户连续7年口径参考](https://www.bjmtg.gov.cn/bjmtg/wxts/202407/1fb1ac9b17a343a6a41c385952c27e50.shtml)
- [北京市规划和自然资源委员会](https://ghzrzyw.beijing.gov.cn/)
- [学信网](https://www.chsi.com.cn/)
- [教育部留学服务中心](https://www.cscse.edu.cn/)
- [自然人电子税务局](https://etax.chinatax.gov.cn/)
- [12366纳税服务](https://12366.chinatax.gov.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain-text consultation guidance with checklist-style status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify the selected mode, source of any score result, confirmed and pending fields, unofficial assumptions, and the required simulation disclaimer.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
