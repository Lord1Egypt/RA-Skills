# 数据分析与报告预设

## domain_id

`data_analysis_reporting`

## common_jobs

- 清洗 CSV、Excel、JSON、日志和业务导出数据
- 生成指标表、图表、周报、月报和经营分析
- 对比不同时间、渠道、项目或用户分组
- 发现异常、趋势、漏斗和贡献项
- 导出 Markdown、HTML、PPT、Excel 或仪表盘型结果

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 数据来源是什么，文件路径、表名或 API 在哪里
- 需要回答的业务问题是什么
- 关键指标、维度、时间范围和对比口径是什么
- 是否需要清洗、合并、去重、脱敏或口径校验
- 输出是临时分析、固定报告、图表，还是可复用脚本
- 是否需要可编辑 Excel、PPT、HTML 仪表盘或 Markdown 报告
- 结果是否要写回外部系统或定期执行

## recommended_execution_planes

- `Skill + CLI`
  适合本地文件清洗、图表生成、报表导出和可复用脚本
- `Skill + API/MCP`
  适合 BI、数据库、Notion、Sheets 或远端数据源
- `Skill + CLI + API/MCP`
  适合远端取数、本地处理、报告生成和系统写回
- `Skill-only`
  只适合解释已有结果和轻量分析口径讨论

## risk_and_gates

- 必须确认指标口径和时间范围，避免误读
- 涉及个人信息、财务数据或客户数据时需要脱敏和权限 gate
- 自动结论要区分数据事实、推断和建议
- 图表和报告要保留数据来源与生成时间
- 需要复用时，脚本必须支持参数、结构化输出和错误提示

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.data_analysis_reporting`
- 如果涉及可视化报告，必须补 `output_profile` 和 `design_md`
