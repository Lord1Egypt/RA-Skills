# References — code-to-skill (1.0.5, self-contained)

本目录汇总 code-to-skill 的参考与设计说明，供发布检测 / 维护时查阅。

## 文档索引

| 文件 | 说明 |
|------|------|
| `../SKILL.md` | 技能主说明（frontmatter + Step 0–10 全流程指令） |
| `../README.md` | 快速上手、安装与使用说明 |
| `../CHANGELOG.md` | 版本与变更记录 |
| `../skill-card.md` | 技能卡片：发布者、许可证、风险评估、输出规范 |
| `../_meta.json` | 发布元数据（owner / slug / version） |
| `../scripts/extract.py` | 自包含 PDF 文本提取入口 |
| `../book_to_skill/` | 内置提取引擎（parsers / cli / config / sanitize / dependencies / utils / exceptions） |
| `../tools/scan_generated_skill.py` | 生成技能的安全扫描 + 强制力审计工具 |
| `../examples/` | （可选）示例输入 / 输出（如提供） |

## 设计要点

- **索引而非概括**：规范是编号条文构成的决策规则系统，本技能对每条条文按触发条件建立可检索索引，绝不改写强制性措辞（应 / 宜 / 可 / 不应 / 不得）。
- **表格即数据**：耐火等级、防火间距、疏散宽度等数据表提取为结构化 JSON（程序可查询）+ Markdown（阅读）。
- **自包含引擎**：`scripts/extract.py` + `book_to_skill/` 随包提供，无需外部安装 `book-to-skill`；缺 poppler 时自动回退 pypdf / pdfminer。
- **安全闭环**：生成的规范 Skill 可用自带 `tools/scan_generated_skill.py` 做安全扫描与强制力审计（路径可信、条文原文未被改写、强制等级一致）。
- **版本一致**：SKILL.md frontmatter / `_meta.json` / `skill-card.md` / 文件名四处的版本号必须一致（当前 1.0.5）。
