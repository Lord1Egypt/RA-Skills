# 教育与培训运营预设

## domain_id

`education_training_ops`

## common_jobs

- 设计课程大纲、教案、讲义、练习和测验
- 把资料转成学习路径、知识卡片或课件
- 生成培训计划、作业反馈和学习报告
- 维护企业培训、社群课程或学校课程内容
- 分析学习进度、答题结果和知识薄弱点

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 学习对象是谁，当前水平和目标水平是什么
- 产物是课程大纲、教案、课件、练习、测验，还是学习报告
- 是否已有教材、知识库、视频、文档或题库
- 需要怎样的学习路径、课时、难度和评估方式
- 是否需要 PPT、图卡、讲义、表格或 LMS 导入格式
- 是否涉及未成年人、考试、证书或正式评估
- 成功标准是掌握度、完成率、互动质量，还是交付格式完整

## recommended_execution_planes

- `Skill-only`
  适合课程设计、练习题、反馈草稿和教学建议
- `Skill + CLI`
  适合批量生成讲义、题库、卡片、PPT 或数据报告
- `Skill + API/MCP`
  适合 LMS、知识库、表格、文档和学习数据系统联动
- `Skill + CLI + API/MCP`
  适合课程生成、资源导出、学习数据分析和平台写回

## risk_and_gates

- 教学内容必须匹配学习对象和难度
- 正式考试、证书和评分场景需要人工审核
- 未成年人相关内容需要额外安全和隐私 gate
- 知识来源和版权材料需要记录来源边界
- 视觉课件必须进入 `output_profile` 和 `design_md`

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.education_training_ops`
- 如果涉及课件视觉，必须补 `design_md` 和 `visual_storytelling`
