# Doubao GEO Audit Skill

豆包 GEO 效果评估 Skill 是一个极简、快速、标准化的内容评估工具。它帮助用户评估一段文字资料（官网介绍、公众号文章、产品说明等）在豆包大模型中是否容易被理解、总结、引用和推荐，并给出具体的 GEO（Generative Engine Optimization）改进建议。

## 项目结构

```
doubao-geo-audit-skill/
├── manifest.json                     # WorkBuddy / 自动化平台优先读取的 JSON 清单
├── SKILL.md                          # Skill 核心定义与调用说明
├── README.md                         # 项目介绍文件
├── prompts/                          # LLM 提示词
│   ├── audit.md                      # 内容评估核心 Prompt
│   └── scoring.md                    # 评分模型与标准 Prompt
├── templates/                        # 输出模板
│   └── doubao_geo_audit_report.md    # 标准评估报告模板
├── examples/                         # 输入输出样例
│   ├── example_input.md              # 示例用户输入
│   └── example_output.md             # 示例报告输出
└── CHANGELOG.md                      # 更新日志
```

## 核心特性
- **纯文本分析**: 无需复杂后端配置和数据爬取，极速反馈。
- **6 维评分模型**: 从品牌定义、目标用户、问题场景、内容结构化、可引用性、推荐触发度 6 个层面量化分析内容。
- **直观的报告输出**: 强制按预设模板输出报告，格式清晰直接，适合直接发给客户查看。
- **行动导向**: 不讲空话，给出具体的优化建议（如：提供可引用标准句、补充特定的 FAQ 等）。
- **自动化友好**: 提供 `manifest.json` 和默认 `compact` 输出模式，适合 WorkBuddy 等自动评测环境。

## 如何使用
该项目旨在作为一个标准的 Skill 注册到 OpenClaw 或其他基于大模型驱动的 Agent 平台。当用户输入关于某个品牌或产品的介绍文本时，Agent 可通过加载 `prompts` 和 `templates` 来生成对应的评估报告。请参考 `SKILL.md` 了解 Agent 视角的详细调用规范。

## WorkBuddy 兼容性建议
- 优先读取根目录 `manifest.json`，不要从示例代码片段推断参数结构。
- 程序化调用统一使用 UTF-8 编码的 JSON。
- 默认传入 `report_mode=compact`，可以显著减少自动评测中的超时风险。
- 传入 `content` 时，请正确转义 JSON 字符串中的换行和双引号。
