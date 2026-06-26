# 活动与社群运营预设

## domain_id

`event_community_ops`

## common_jobs

- 策划线上活动、线下活动、直播、研讨会和社群运营
- 生成活动方案、议程、邀约文案、主持稿和复盘报告
- 整理报名、签到、反馈、问答和社群互动记录
- 维护社群内容日历、活动 SOP 和成员分层
- 把活动线索、任务和素材写回 CRM、表格或知识库

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 活动或社群类型是什么，线上还是线下
- 目标人群、规模、时间、预算和目标是什么
- 产物是活动方案、传播素材、议程、主持稿，还是复盘报告
- 是否已有报名表、嘉宾资料、历史活动或社群记录
- 是否需要海报、图卡、PPT、表格或短视频脚本
- 是否需要写回 CRM、表格、日历、任务系统或社群工具
- 成功标准是报名、到场、互动、转化，还是复盘沉淀

## recommended_execution_planes

- `Skill-only`
  适合活动方案、话术、议程、主持稿和复盘框架
- `Skill + CLI`
  适合批量整理报名表、反馈表、素材包和报告
- `Skill + API/MCP`
  适合日历、表格、CRM、社群工具、邮件和任务系统联动
- `Skill + CLI + API/MCP`
  适合活动数据整理、内容生成、任务分发和系统写回

## risk_and_gates

- 自动群发、邀约、提醒和社群互动必须单独确认
- 报名信息、联系方式和反馈内容需要脱敏或权限 gate
- 对外宣传素材需要品牌、嘉宾和事实核实
- 活动预算、价格、权益和承诺需要人工确认
- 视觉产物必须进入 `output_profile` 和 `design_md`

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.event_community_ops`
- 如果涉及群发或系统写回，必须在 `build-plan.md` 中写清写回 gate
