# 文档与办公产物预设

## domain_id

`document_artifacts`

## common_jobs

- 处理 PDF、Word、PPT、Excel
- 合并、拆分、抽取、重排文件
- 生成正式文档
- 从原始材料生产可交付办公产物
- 生成或修改 `.pptx` 演示文稿
- 生成视觉叙事型办公产物，如答辩稿、汇报 deck、报告页

## default_question_pack

下面是候选问题池，不是整包必问清单。
先排最小问题集，整轮默认不超过 10 个问题；预算接近上限时，把剩余缺口写入 `open_gaps`。

- 当前交付物是什么文件类型
- 是处理已有文件，还是新生成文件
- 更看重读取抽取、格式重排，还是最终排版
- 是否需要批量处理
- 是否需要脚本化文件转换
- 如果是 PPT，是否必须保留可编辑性和源文件
- 如果是视觉优先的 PPT，风格来源是什么
  - 用户指定风格
  - 用户提供 `DESIGN.md`
  - 用户详细描述
  - 用户从本地 `ref/design-md/` 中选择
- 是否需要更强的文字层级来增强版式节奏
  - kicker / 章节标签
  - 大标题与一句话结论
  - 数字块 / 短句强调
  - 注释层
- 信息图元素要强调到什么程度
  - 少量点缀
  - 每个章节至少一页
  - 每个内容页都要有

## recommended_execution_planes

- `Skill + slides + PptxGenJS`
  适合稳定生成和修改 `.pptx`
- `Skill + structured-visual-storytelling + slides`
  适合把答辩稿、汇报 deck、报告页先走统一视觉叙事主线，再落到 `.pptx`
- `Skill + 文件脚本`
  适合稳定、可重复的文件处理
- `Skill-only`
  只适合规划文档结构或写作约束，不适合最终文件生成

## risk_and_gates

- 先确认真实交付文件类型
- 如果是 PPT，先确认页数范围、比例和是否必须可编辑
- 如果是视觉优先的 PPT，在风格来源未明确前，不进入具体排版
- 如果是正式汇报或答辩型 PPT，需要明确是否强制加入图表、流程图、对比卡和指标卡
- 大文件或多文件流程要控制输出体积
- 如果文件损坏风险高，要优先规划可回滚和副本策略
- 需要明确哪些结果是提取，哪些结果是改写

## default_outputs

- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`
- 文件处理场景建议保留脚本化比例说明
