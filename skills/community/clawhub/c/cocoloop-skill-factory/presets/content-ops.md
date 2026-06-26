# 内容运营预设

## domain_id

`content_ops`

## common_jobs

- 公众号、小红书、博客、邮件和社媒内容生成
- SEO 审计、关键词规划、标题和摘要优化
- 从资料、长文或视频中提炼可发布内容
- 维护品牌语气、表达禁忌和发布规范
- 生成图文、信息图、短视频脚本或多渠道分发素材

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 目标发布渠道是什么，是否有主渠道和次渠道
- 目标读者是谁，读者已经知道什么
- 产物是选题、正文、图文脚本、SEO 页面，还是分发计划
- 是否有品牌语气、禁忌表达、参考来源和事实边界
- 是否需要视觉输出，例如信息图、封面、图卡或短视频分镜
- 是否需要真实发布、草稿填充，还是只生成可审核内容
- 成功标准是阅读、转化、排名、收藏，还是内部审核通过

## recommended_execution_planes

- `Skill-only`
  适合选题、文案、改写、风格约束和发布前审核
- `Skill + CLI`
  适合批量整理素材、生成多格式草稿或导出图文包
- `Skill + API/MCP`
  适合 CMS、Notion、SEO 工具、数据看板和发布系统接入
- `Skill + CLI + API/MCP`
  适合从素材抓取、内容生成、SEO 检查到外部系统写回的完整链路

## risk_and_gates

- 有参考来源时要明确引用边界和改写边界
- 涉及事实、数据、人物、价格和政策时要保留核实 gate
- 涉及账号发布、批量互动或平台抓取时要提示频率限制和平台规则
- 视觉输出必须进入 `output_profile` 和 `design_md`
- 最终面向读者的内容不得包含写作过程说明、来源改写提示或工程性注释

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 如果进入协议收口，必须补 `domain_supplements.content_ops`
- 如果涉及视觉输出，必须补 `design_md` 和 `visual_storytelling`
