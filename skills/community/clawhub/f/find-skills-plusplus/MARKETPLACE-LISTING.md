# find-skills++ — 市场同步上架描述

> 用途：将下列内容粘贴到 SkillHub / ClawHub 的技能发布/编辑页对应字段。
> 遵循本仓库「关键双语」策略——露出层（标题/简介）中英双语，实现细节仍见仓库文档。

## 1. 基础信息

- **技能名 / Name**：Find Skills++（安全策展·生态治理·智能发现）
- **Slug**：`find-skills-plusplus`
- **版本 / Version**：5.3.0
- **作者 / Author**：何巍
- **许可证 / License**：MIT-0（派生自 `guipi888/find-skills`，保留原 MIT 许可与署名，见 NOTICE；源头为 `vercel-labs/skills`）
- **分类 / Category**：developer-tools / 效率工具
- **标签 / Tags**：AI工具、技能发现、技能安全、WorkBuddy、CodeBuddy、生态治理

## 2. 一句话简介（Tagline）

- 中文：给 AI 智能体的技能生态做「安装前安全闸门 + 装后生态治理」的全能工具，智能发现作为顺带能力。
- EN: Vet before install, govern after — a security-first toolkit to curate and manage your AI agent's skill ecosystem (discovery included).

## 3. 详细描述（Description）

**中文：**
find-skills++ 是 `find-skills` 的社区超级增强版，补齐了原生技能生态里「没人真正帮你审查过要装的东西」这一环。它不只是帮你找技能，更帮你敢装、会管：
① 安装前 AST 级安全扫描（正则 + `ast`/`shlex` 语法树，四级风险 EXTREME/HIGH/MEDIUM/LOW + 文件·网络·命令权限清单，EXTREME 直接阻断，能识破动态拼接、`base64` 混淆执行、凭据目录窃取、Agent 身份文件读取）；
② `sync` 在线目录同步支撑的真·离线全能（断网照样搜）；
③ 环境感知引用完整性校验（专治「长得好看但引用了不存在工具」的假优技能）；
④ 技能质量评级 0–100（七维）；⑤ 跨源合并去重 + 来源信誉门槛；⑥ 全生命周期 `update`/`uninstall`（进回收站可还原）/`clean-dupes`；⑦ 冗余检测与瘦身建议；⑧ 自带零依赖 CLI `findskills.py`（20 子命令、140 项测试全绿 + 端到端冒烟自证）；⑨ 内置 `promote` 自我营销引擎与 `demo` 可录屏演示。
纯标准库、零依赖、全本地静态分析、不收集不上传任何本地数据。

**EN:**
Find Skills++ is a community supercharged fork of `find-skills`: an all-in-one skill discovery · security curation · ecosystem governance toolkit for AI agents. Differentiators the originals lack: ① AST-level pre-install security scan (regex + ast/shlex, 4-tier risk & file/network/command permission inventory, EXTREME blocks install); ② true offline catalog via `sync`; ③ reference-integrity check that flags skills referencing non-existent tools; ④ 0-100 quality rating (7 dimensions); ⑤ cross-source merge/dedup + source reputation gating; ⑥ full lifecycle update / uninstall-to-trash / clean-dupes; ⑦ redundancy detection & slim-down advice; ⑧ a zero-dependency CLI `findskills.py` (20 subcommands, 140 passing tests, end-to-end smoke self-proof); ⑨ built-in `promote` engine and recordable `demo`. Pure stdlib, zero dependencies, fully local static analysis, no data collection.

## 4. 核心差异化（卖点清单，可贴到详情页）

- 🛡️ AST 级安全闸门：正则抓不到的混淆调用，语法树级才抓得到
- 💾 真·离线全能：在线目录同步到本地，API 挂了照样搜
- 🔍 引用完整性校验：识破「假优」技能
- 🔄 全生命周期：装了也能管（更新 / 卸载可还原 / 去重）
- 🧠 中文结构化卡片 + 综合排序 + 语义匹配（离线、零依赖）
- 🚦 四级风险 + 权限清单 + 17 项红旗 + 5 级信任层级
- 🤝 多 agent 支持：自动识别 WorkBuddy/CodeBuddy/OpenClaw/Claude Code；治理命令也能管别的 agent 的技能，扩大可触达人群

## 5. 安装（Install）

```bash
git clone https://github.com/cdhewei/find-skills-plusplus.git
cp -r find-skills-plusplus ~/.workbuddy/skills/find-skills-plusplus
```

或在 SkillHub / ClawHub 搜索 `find-skills++` 一键安装。

## 6. 触发词（Keywords / Triggers）

skill, skills, find, discover, install, uninstall, update, security, audit, vetting, scan, ast, marketplace, skillhub, clawhub, agent, 技能, 找技能, 安装技能, 技能安全

## 7. 合规与署名（Compliance & Attribution）

- 上游：`guipi888/find-skills`（MIT, Copyright (c) 2026 Kyle，SkillHub 99.4 万下载）
- 源头：`vercel-labs/skills` 的 `find-skills`（Vercel 官方）
- 思路参考：`sandbaseai/workbuddy-skill`；红旗清单对标 `skill-vetter`
- 本仓库新增内容（`scripts/security_scan.py`、`findskills.py` 及全部 ++ 增强、文档）以 MIT 提供，均为独立自研、纯标准库、零依赖实现，保留上游 MIT 许可与署名，明确标注「基于 find-skills 修改」，非官方替代品。完整说明见仓库 README「许可证与署名」。
