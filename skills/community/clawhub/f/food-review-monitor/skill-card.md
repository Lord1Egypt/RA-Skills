## Description:

餐饮外卖评价智能监控可导入或拉取美团外卖、饿了么/淘宝闪购、京东外卖评价数据，检测口味、评分、配送、服务和差评突增异常，并生成可视化HTML报告和告警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

餐饮商家、门店运营人员和支持他们的代理可用此技能分析外卖平台评价导出文件、检查历史趋势、发现服务异常，并生成本地HTML报告用于运营复盘和告警处理。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional platform API keys may be stored in plaintext local configuration.

Mitigation: Prefer CSV import where possible; avoid API mode and real platform API keys until secret storage is improved.

Risk: Generated HTML reports may expose sensitive customer review exports or unsafe review text when opened locally.

Mitigation: Treat review exports and reports as sensitive local files, and open generated reports only from trusted data or in an isolated browser context until HTML escaping is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/food-review-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/bettermen)
- [Configured Python package index](https://pypi.tuna.tsinghua.edu.cn/simple/)
- [ECharts CDN used by generated reports](https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Text guidance with shell commands, configuration details, analysis summaries, and generated local HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and history are written to local user-configured directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
