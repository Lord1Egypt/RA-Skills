---
name: daily-insight-brief
description: Daily morning brief（8:30 Beijing time）自动收集、交叉验证并提炼来自广域来源的商业、科技、金融等领域信息，产出10-15条要点性简报。每条包含：标题/要点、来源（名称+链接）、关键数据点、分析评论（1-2句）、核心观点、验证状态（已验证 / 待核实）。
---

# daily-insight-brief

## Trigger and Use
- When to use: 每日晨间（北京时间 08:30）自动输出 Brief；也支持通过对话触发预览版本。
- Trigger name: daily_insight_brief（也可变体如 daily-insight-brief_v1，具体在实现层统一映射）。
- Input: 无外部输入；系统自动抓取与聚合。
- Output: 结构化清单，包含以下字段的若干条目（总数10-15条）。

## Source and Verification Strategy
- Sources: 广域来源优先，从咨询/金融机构、主流媒体、科技巨头、智库、大学、知名博客、媒体头条等获取信息；初版包含但不限于以下清单（后续可扩展）：
- 顾问与金融机构：McKinsey & Co、Bain & Co、BCG、Deloitte、PwC、KPMG、Goldman Sachs、Morgan Stanley、BlackRock、Bridgewater
- 主要媒体：Wall Street Journal、Financial Times、Reuters、Bloomberg、CNBC、Nikkei
- 科技与学术：MIT Technology Review、Stanford News、Harvard Business Review、主流学术期刊与高校新闻
- 科技巨头/行业观察：Google、Amazon、NVIDIA、Meta、Apple、OpenAI、Anthropic
- 知名博客/智库：Naval Ravikant、Karpathy、RAND 等
- 证券市场与高校：NYSE/NASDAQ 要闻；MIT、斯坦福、哈佛、耶鲁、清华等
- 交叉验证：同一主题将来自至少2个以上独立来源进行对照核实；对无法证实的信息标注为待核实并附上线索/证据需求。
- 验证标记：每条信息包含验证状态字段：已验证 / 待核实。
- 证据等级：对关键事实给出等级标识（如 1=高可信、2=中等、3=待证据）。

## Output Format (10-15 条 Brief)
每条 Brief 包含以下字段，单位为中文描述，必要时附英文要点以便拓展：
- 序号 + 标题（要点摘要）
- 来源名称与链接
- 关键数据点（如时间、对比、趋势、数值等，列出2-4点）
- 分析评论（1-2句，简明判断或趋势解读）
- 核心观点（1句话摘要，便于传播）
- 验证状态（已验证 / 待核实）
- 备注/证据（简述为何可信或需要后续核实）

示例：
- 1) 标题：某科技公司宣布重要里程碑
- 来源：SourceName (https://source.url)
- 关键数据点：数据点A、数据点B
- 分析评论：简短评述1-2句
- 核心观点：一句话摘要
- 验证：已验证
- 备注：若与其他来源冲突则标待核实

- 2) 标题：宏观市场/政策趋势
- 来源：SourceName (https://source.url)
- 关键数据点：数据点A、数据点B
- 分析评论：简短评述
- 核心观点：一句话摘要
- 验证：待核实
- 备注：需要更多数据支持

- 3) 标题：行业对比/对照分析
- 来源：SourceName (https://source.url)
- 关键数据点：数据点A、数据点B
- 分析评论：简短评述
- 核心观点：一句话摘要
- 验证：已验证

（注：此处给出格式示例，实际输出请按上述字段灵活排布。）

## Resources
- Bundled Resources (Optional)
- scripts/: 负责抓取、聚合、去重、初步分析的自动化脚本
- references/: 存放用于上下文加载的参考文档、数据字典、来源模板等
- assets/: 模板、图标、输出模板等可选资源

## Workflow and Design Notes
- Progressive Disclosure: SKILL.md body 保持简洁（核心工作流在前，详细策略/来源细节在 references/ 中）
- 流程分解：如果后续需要多来源扩展，可以将来源分类到 references 下的独立文档，并在 SKILL.md 中引用链接
- 错误处理：无法验证的条目标注为待核实，附上可核对的线索
- 测试与验收：初版在开发环境输出3-5条样例 Brief，与你对格式与风格后逐步扩展

## How to Use / Operational Guidance
- 启动与调度：每日 08:30 Beijng time (UTC+8) 自动触发 Brief；也支持手动触发预览
- 输出渠道：初期直接输出到当前会话；后续可扩展写入 Feishu 文档、邮件或指定频道
- 语言与风格：中文为主，必要时包含英文要点；分析评论由系统生成，后续可由你或我对口味进行微调

## Testing Plan
- 版本初始阶段：生成3-5条示例 Brief，与你对格式、风格、来源覆盖范围逐条确认
- 迭代阶段：根据反馈逐步扩展来源、优化数据点与评论深度

---

如果你愿意，我可以直接把这份草案落在 /Users/alex/.openclaw/workspace/skills/daily-insight-brief/SKILL.md，并继续为你生成第一版3-5条样例 Brief，以及初步的来源候选扩展清单。请确认是否直接使用以上草案文本，或你希望对描述、字段或格式做进一步定制。