# Changelog

版本号：vMAJOR.MINOR.PATCH。MINOR 功能新增、PATCH 修订、MAJOR 架构级变更。

## v1.6.0 - 2026-11-18

### Changed

- work 场景归集放宽：`docs/ data/ references/` 三桶降为缺省建议（coding 场景不变），agent 可按 work 类型自定顶层子文件夹（如报告库用 `reports/`、`minutes/`），优先沿用目录既有结构与命名惯例；成果／底稿／参考三分法降为建议维度之一
- 自定分类方案连同完整目录树进入既有审批流程（清单待批、批准后移动、修复断链均不变）；批准后把归档约定写入 AGENTS.md，后续会话沿用不再重定
- 场景适配表 work 列归集行同步改写，表后新增「work 场景归集放宽」说明段
- frontmatter `description` 归集措辞同步（fixed buckets for coding / work-type-fitted taxonomy for work，触发短语不动）；README 特性表、七件事⑦、交付物、FAQ 与 zh-CN 双语译文同步

## v1.5.2 - 2026-11-09

### Changed

- 英文化：SKILL.md 正文、`references/`、`assets/`、README 全部切换为英文默认（国际 Skills Hub 索引与审核友好）；中文参考译文收进 `docs/zh-CN/`（SKILL.md 与 README，仅供人阅读，不随技能包发布），双语 README 顶部互链
- frontmatter `description` 改为双语：英文主句供 Hub 索引，保留中文触发短语，触发判据兼容中文会话

## v1.5.1 - 2026-11-09

### Added

- README 特性列表升格「记忆与进度同步」为卖点：借宿主 agent 自身的记忆机制沉淀项目记忆——按宿主格式、先查重、批准后写入，不另起炉灶；无记忆机制则静默跳过（表格末行与七件事⑥同步改写）
- FAQ 新增「Hermes / OpenClaw 这类 personal agent 能用吗？」条目：纯 Markdown 无依赖不绑定 CLI，有记忆机制就按其格式沉淀记忆
- README「仓库结构」加注：仓库另含协作用文件，不属于 skill 安装内容
- SKILL.md 文末新增「关于」：GitHub 仓库与作者站点 [kelegele.com](https://kelegele.com) 引流位
- frontmatter 新增 `metadata.openclaw.homepage`（ClawHub 卡片主页链接指向 GitHub 仓库）
- README 徽章区新增 skills.sh 安装徽章；「安装」新增技能市场入口（ClawHub、LobeHub Skills Marketplace）；「反馈」补作者站点
- 首次发布至 ClawHub 与 LobeHub Skills Marketplace（ClawHub 平台条款下按 MIT-0 分发）；skills.sh 此前已自动收录

## v1.5.0 - 2026-11-05

### Added

- 场景适配：Step 3 先判定 coding / work（非代码协作目录）场景，工作流一致、仅三处适配——首版扫描与核验（coding 核命令 / work 核引用路径）、章节语义（work 偏向数据口径、命名归档、交付复核）、归集方向；不新增模板文件，复用既有"不适用章节整段删除"规则

### Changed

- Step 7「文档归集」扩为「文档与数据归集」：供人阅读的文档归 `docs/<主题>/`，CSV/XLSX/JSON 等机器可读数据归 `data/<主题>/`，数据表格不再被当文档塞进 docs/；用途不明的单独标出询问用户，并保留"保持不动"选项
- 归集方案前先 grep 全项目（代码、脚本、构建/CI 配置）排查引用，被引用的文件一律不动；批准后的断链验证同样覆盖代码引用点
- 留根目录的例外清单明确加入 README、LICENSE
- frontmatter `description` 同步分流归集与 work 场景触发措辞（"整理项目文档与数据"、"沉淀项目协作规范"）

## v1.3.0 - 2026-09-16

### Added

- 瘦身迁移机制：削减 AGENTS.md 时，仍有长期参考价值但不满足根文件准入门槛的内容（背景说明、操作细节、低频特例）迁往 `docs/<主题>.md`，在原位置留一行按需引用；过时、重复内容仍直接删，不迁移
- Step 4 新增引用行约束：宁缺毋滥，每章至多 1–2 条，防 docs/ 变相撑大根文件
- Step 5 改动方案新增迁移清单项（目标文件与引用行；docs/ 写入同样先经用户批准）

## v1.2.0 - 2026-09-16

### Added

- 成稿示例 `assets/AGENTS-example.md`（agents.md 官方 pnpm/Turborepo monorepo 实例），供把握合格成稿的颗粒度与密度
- 模板与章节约定扩展可选章节：`Build & Deployment`、`Security Notes`、`Debugging & Troubleshooting`，仅当项目确有对应固定流程时追加
- Step 3 命令可执行验证：首版写入的每条命令须实跑确认，或与 package.json scripts / Makefile / CI 配置逐一核对，跑不通不写入
- 章节约定新增嵌套指引：仅适用特定子目录的教训不进根文件，下沉为该子目录的局部 AGENTS.md
- 模板顶部补充裁剪与语言约定说明（章节名保留英文，条目语言随项目主流语言）

### Changed

- 自建章节门槛修正为"标准与可选章节均无法覆盖时才自建，全文章节总数 ≤ 9"（原"≤ 6"与 6 个标准章节自相矛盾）

## v1.1.0 - 2026-09-16

### Added

- 文档归集步骤（Step 7，收尾可选）：扫描散落的产出文档，给出 `docs/<主题>/` 归类方案；经用户批准才移动文件，并自动修复引用断链
- agent 记忆与进度同步（Step 6，条件执行）：agent 有记忆机制则沉淀为项目记忆条目；项目有 TODO/CHANGELOG/PROGRESS/STATUS 等进度/状态文件则一并更新
- 铁律 4「先确认后落盘」：所有文件改动（AGENTS.md 写入、记忆、进度文件、文档移动）先出方案、经用户批准后执行

### Changed

- 安装方式不再局限 WorkBuddy：npx skills 一键安装（推荐）、Claude Code、手动复制（各 agent 技能目录对照表）、WorkBuddy URL 导入
- SKILL.md frontmatter 新增 `version` 字段

## v1.0.0 - 2026-09-04

- 初版：经验教训蒸馏固化为 AGENTS.md（5 步工作流：收集 → 蒸馏 → 读取现状 → 有机合并 → 写入），120 行硬上限与合并决策表，遵循 agents.md 开源规范
