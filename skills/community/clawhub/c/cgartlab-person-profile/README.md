# person-profile / 人物档案

一个独立的、通用的、可脱离特定知识库使用的**人物档案 skill**。

为 AI agent 提供结构化的人物档案创建、维护与验证工作流。基于 30 份高质量人物档案（cgartlab-obsidian 知识库实践）的经验沉淀，融合 GitHub 上同类 skill 的成熟做法。

## 项目定位

**是什么**：AI agent 的 skill 项目，指导 agent 如何从零创建一个高质量、可核验、有反例的人物档案。

**不是什么**：
- 不是模板库（模板只是本 skill 的一个 artifact）
- 不是特定知识库的插件（默认适配 Obsidian，可替换 frontmatter 规范用于其他环境）
- 不是人物百科生成器（不做"一键生成 100 个人"的批量任务）

**核心承诺**：
- 每条事实必须可点开核验，附实际访问到的 URL
- 抓不到就写「未取得」，绝不凭记忆构造 URL
- 每条判断必须有反例审查，反例只能取自档案已有材料
- 章节结构固定，写作纪律严格，验收标准可自动化

## 目录结构

```
person-profile/
├── SKILL.md              # 主入口，agent 加载此文件即可获得完整工作流
├── README.md             # 本文件，项目介绍与快速开始
├── DESIGN.md             # 设计哲学与决策记录（Why not What）
├── CHANGELOG.md          # 版本历史与破坏性变更
├── LESSONS.md            # 教训→规则清单（会话开始先读）
├── AGENTS.md             # 仓库协作约定
│
├── references/           # 深度方法论（agent 需要时才加载）
│   ├── evidence-grading.md     # 5 级证据分级详解
│   ├── chapter-rationale.md    # 11 节结构的设计逻辑
│   ├── bidirectional-links.md  # 关系网络双向链规范
│   ├── counter-example-rules.md # 反例审查与边界承认
│   ├── citation-discipline.md  # 引用纪律与 URL 校验
│   ├── length-and-density.md   # 长度密度参考
│   ├── writing-style.md        # 标点、禁词、句式规范
│   └── external-references.md  # 吸收的 GitHub 外部参考清单
│
├── templates/            # 可复制的档案模板
│   ├── person-archive.md       # 11 节完整模板（每节带 HTML 注释说明）
│   ├── person-archive-lite.md  # 6 节精简版（快速建档用）
│   └── person-fragment.md      # 单节片段模板（补链 / 补章节用）
│
├── scripts/              # 校验与工具脚本（Python）
│   ├── validate_archive.py     # 单份档案校验
│   ├── validate_library.py     # 批量校验整个档案库
│   ├── check_bidirectional.py  # 双向链完整性检查
│   ├── check_prohibitions.py   # 禁词与格式违规扫描
│   ├── check_sources.py        # 参考来源格式校验（内联链接、无裸 URL）
│   └── migrate_heading_level.py # 标题级别批量迁移
│
├── benchmarks/           # 高质量标杆档案样本（取自真实知识库）
│   ├── dan-koe.md            # 英文创作者经济标杆（278 行）
│   ├── ruanyifeng.md         # 中文技术博客标杆（295 行）
│   ├── esor-huang.md         # 中文独立作者标杆（289 行）
│   └── benchmark-rubric.md   # 评分标准
│
└── tests/                # CI 校验用 fixtures（正例 / 反例）
    └── fixtures/
```

## 快速开始

### 1. 作为 Hermes Agent skill 使用

复制整个目录到 `~/.hermes/skills/person-profile/`（或你的 agent 框架的 skills 目录）。加载 SKILL.md 即可。

### 2. 作为独立方法论引用

`DESIGN.md` 讲为什么这么做；`references/` 里有每节的详细方法论。适合阅读后内化，不依赖任何 agent 框架。

### 3. 直接跑校验脚本

```bash
# 校验单份档案
python scripts/validate_archive.py path/to/archive.md

# 批量校验整个库
python scripts/validate_library.py path/to/library/

# 检查双向链完整性
python scripts/check_bidirectional.py path/to/library/
```

## 在 Obsidian 知识库中使用

本 skill 默认适配 `cgartlab-obsidian` 的 PARA 结构：

- **档案目录**：`03-资源/人物/`
- **索引文件**：`03-资源/人物/人物-README.md`
- **frontmatter 规范**：`type: reference`、`tags: [资源/人物]`、`created`、`updated`
- **知识库自带校验**：`node scripts/check-frontmatter.mjs`（管 type/tags/日期）
- **skill 校验**：`python scripts/validate_archive.py`（管 11 节结构 + 写作纪律）
- **读写方式**：Obsidian CLI（`obsidian read/create/append file=...`）或直接文件操作

两套校验互补：知识库校验器管元数据合规，skill 校验器管内容结构与写作纪律。详见 `SKILL.md` 的「知识库集成」章节。

## 版本

- **v0.1.0** — 首版：核心工作流、11 节模板、5 级证据分级、17 项验收清单
- **v0.1.1** — 可移植性修复：移除平台耦合与死引用
- **v0.2.0** — 接入真实知识库：标杆档案入库、模板逐节注释、Obsidian 集成章节
- **v0.2.1** — CI 修补：移除 release 自动发布触发，记录 private reusable workflow 教训
- **v0.2.2** — 发布逻辑内联到本仓库 action，ClawHub / SkillHub 发布恢复
- **v0.2.3** — 统一「主要参考来源」格式，新增 check_sources.py 机械校验（修复 #10）

## 许可

MIT. See LICENSE.

## 致谢

- CGArtLab Obsidian 知识库 30 份人物档案的实践
- GitHub 上开源 skill 与提示词库的方法论（见 `references/external-references.md`）
- 相关 skill：`quill`（长文写作）、`obsidian-cli`（知识库读写）
