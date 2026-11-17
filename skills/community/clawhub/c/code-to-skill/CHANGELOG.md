# CHANGELOG — code-to-skill

## v1.0.6 (2026-08-22) — 版本号升版以适配重新发布
- **版本号统一升 1.0.6**：SKILL.md / `_meta.json` / `skill-card.md` / 文件名 四处统一为 1.0.6，避免与已发布/预发布的 1.0.5 冲突（ClawHub 不允许重复发布同一版本号）
- 内容与 v1.0.5 一致（自包含引擎 + CLAWhub 三级检测合规化），仅版本号递进

## v1.0.5 (2026-08-22) — 自包含 + CLAWhub 发布检测合规化

- **自包含引擎**：`scripts/extract.py` + `book_to_skill/` 随包提供，不再依赖外部 `book-to-skill` 安装
- **frontmatter 强化**：补齐 `version`(1.0.5) / `slug`(code-to-skill) / `author`(51comic) / `license`(MIT-0) / `compatibility`，修复此前缺 `version` 导致 Level 1 硬失败
- **版本统一**：SKILL.md frontmatter / `_meta.json` / `skill-card.md` / 文件名 四处版本号统一为 1.0.5（此前 _meta 与 skill-card 写 1.0.4，与文件名 1.0.5 不一致）
- **新增章节**：`When to Activate`（触发条件）、`Anti-Triggers`（不适用场景）、`References`（参考文件表）
- **新增 `references/` 目录**（`references/REFERENCES.md`），满足发布检测的 references 目录要求
- **新增 `README.md` 与 `CHANGELOG.md`**，补齐文档与变更记录

## v1.0.4 (2026-08-11) — 此前发布版本

- 建筑规范→Skill 转换器基础能力：条文索引、强制力标注、表格 JSON 提取、跨规范引用图
- 内置 `tools/scan_generated_skill.py` 安全扫描与强制力审计
