# Changelog

本文件记录 person-profile 的所有显著变更。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

> `0.x` 阶段：SKILL.md 的章节结构与输出格式仍可能调整，升级前请阅读对应版本的**一句话概括**。

## [0.2.3](https://github.com/cgartlab/person-profile/compare/v0.2.2...v0.2.3) - 2026-10-30
> **一句话概括**：0.2.3 统一「主要参考来源」格式，全库只此一种写法，并新增 `check_sources.py` 机械校验。**修复 #10。**

### Added
- `scripts/check_sources.py`：参考来源段机械校验（行尾内联链接、无裸 URL、链接文本限 原文/快照/补充、无地址条目须注明原因、说明非空）。
- `tests/fixtures/sources-invalid/`：裸 URL 反例 fixture；CI 增加 check_sources 正例/反例两步。
- 硬规矩新增第 16 条：参考来源格式。

### Changed
- `templates/person-archive.md` 第 11 节：格式改为唯一写法 `- 说明（日期，可信度）｜[原文](url)`，补 6 条细则。
- `SKILL.md`：11 节结构说明、硬规矩（15→16）、验收清单、[6] 校验项同步。
- `benchmarks/`：3 份标杆从知识库重新拷贝（知识库已在 2026-10-30 统一格式）。

### 说明
- 无地址条目明确允许，但必须注明原因（需登录 / 403 / 快照缺失），不得编造地址。

## [0.2.2](https://github.com/cgartlab/person-profile/compare/v0.2.1...v0.2.2) - 2026-10-23
> **一句话概括**：0.2.2 把发布逻辑内联到本仓库，不再依赖 private reusable workflow，ClawHub / SkillHub 发布恢复。**升级后 Release 会自动发布到两个 registry。**

### Added
- `.github/actions/publish/action.yml`：内联发布 action（ClawHub + SkillHub，含 SkillHub 拒绝无扩展名文件的修复）。
- `publish.yml`：恢复 `release` 自动触发；新增 `publish_clawhub` / `publish_skillhub` 单侧补发开关。

### Changed
- 移除对 `cgartlab/cgartlab-skills` reusable workflow 的依赖（public 仓库无法调用 private workflow）。

### 说明
- 0.2.1 记的「发布暂缓」在 0.2.2 解除。

## [0.2.1](https://github.com/cgartlab/person-profile/compare/v0.2.0...v0.2.1) - 2026-10-22
> **一句话概括**：0.2.1 是 0.2.0 之后的 CI 修补，移除 release 自动发布触发（共享 workflow 在 private 仓库，public 仓库无法调用），并记录踩坑教训。**功能与 0.2.0 相同，升级无感知。**

### Fixed
- `publish.yml`：注释掉 `release` 自动触发，保留 `workflow_dispatch` 手动发布。原因：`cgartlab/cgartlab-skills` 是 private 仓库，GitHub 不允许 public 仓库调用 private reusable workflow，导致 publish 0s 失败。
- `LESSONS.md`：新增「CI 与发布」章节，记录 private reusable workflow 的排查信号（jobs 为空 + `referenced_workflows: []`）与 `git commit -- <path>` 的用法。

### 说明
- 发布到 ClawHub / SkillHub 暂不可用，待共享 workflow 迁到 public 仓库或改为内联后，按 `publish.yml` 注释恢复 release 触发。

## [0.2.0](https://github.com/cgartlab/person-profile/compare/v0.1.1...v0.2.0) - 2026-10-22
> **一句话概括**：0.2.0 让 skill 从「通用骨架」接入真实知识库——三份真实标杆档案入库、模板逐节注释、新增 Obsidian 集成章节。**升级后请读完模板注释，再按新模板落笔。**

### Added
- `benchmarks/dan-koe.md`、`benchmarks/ruanyifeng.md`、`benchmarks/esor-huang.md`：从 cgartlab-obsidian 知识库拷贝的三份真实标杆档案（278 / 294 / 289 行），替代原先只有评分标准、没有样本的状态。
- `templates/person-fragment.md`：单节片段模板，用于补双向链、补缺失章节、追加时间线单行。
- SKILL.md「知识库集成（Obsidian / PARA）」章节：明确档案目录、索引文件、frontmatter 规范、两套校验分工、读写方式。

### Changed
- `templates/person-archive.md` 重写为 11 节完整骨架，每节带 HTML 注释说明「写什么 / 写多少 / 证据要求 / 常见错误」，落盘前删除。
- `templates/person-archive-lite.md` 同步加注释，明确 6 节子集定位。
- 验收清单从 17 项扩到 19 项，新增 frontmatter 知识库规范与两套校验通过两项。
- 长度参考改为引用真实标杆行数（278 / 294 / 289），不再写记忆中的旧值。
- README 目录结构与实际文件对齐，移除不存在的 `assets/`，补充 `person-fragment.md` 与三份标杆。

### Removed
- 模板里的 `## Evidence Ledger` 章节与 frontmatter 的 `living_person` / `notability` 字段。真实知识库档案不用这些字段，保留会造成模板与成稿不一致、`validate_archive.py` 报「非模板章节」。

## [0.1.1](https://github.com/cgartlab/person-profile/compare/v0.1.0...v0.1.1) - 2026-09-30
> **一句话概括**：0.1.1 是一次可移植性修复——移除与 Hermes 平台的绑定、硬编码工具名和已失效的技能引用，使 skill 能在任意 harness 上运行。**你不需要做任何事，直接升级即可。**本次变更对应 [#2](https://github.com/cgartlab/person-profile/pull/2)。

### Fixed
- 对使用者：skill 不再绑定单一 Agent 平台，可在任意 harness 中使用。技术细节：移除 frontmatter（技能文件开头的元数据区）里的 `metadata.hermes` 平台耦合块（Hermes 是本 skill 原先绑定的一个 Agent 平台），只保留标准 name/description/version/author/license。
- 对使用者：在不同 harness（承载 agent 运行的宿主环境）之间切换时，不再因工具名不匹配而失败。技术细节：`delegate_task`（将任务委派给子 agent 的调用）不再硬编码工具名，改为用当前 harness 的 subagent / 委派工具的能力级描述，解决跨 harness 可移植性。
- 对使用者：档案里不再出现已不存在的技能，避免打开时看到失效的相关技能链接。技术细节：移除对 3 个不存在 skill（`person-profile-research` / `grounded-citations` / `concept-synthesis`）的引用，并同步更新「相关技能」与「不用于」章节。

## [0.1.0] - 2026-09-30

> **一句话概括**：首次发布 person-profile skill，一次性提供完整骨架：11 节档案模板、7 步工作流 + 17 项验收清单、证据分级、双向链与四份校验脚本。**你不需要做任何事——这是初始版本，后续升级前请阅读每版的“一句话概括”。**

### Added
- 项目骨架：README、DESIGN、CHANGELOG
- SKILL.md：完整工作流（7 步 + 17 项验收清单）
- templates/person-archive.md：11 节完整模板
- references/：证据分级、章节设计、双向链、反例审查、引用纪律、写作规范
- scripts/validate_archive.py：单份档案校验脚本
- scripts/validate_library.py：批量校验脚本
- scripts/check_bidirectional.py：双向链完整性检查
- scripts/check_prohibitions.py：禁词与格式违规扫描
- benchmarks/：标杆档案评分标准
- references/external-references.md：吸收的 GitHub 外部参考清单

### Design Decisions
- 11 节结构基于 27 份高质量档案实践提炼（[references/chapter-rationale.md](references/chapter-rationale.md)）
- 5 级证据分级独立于常见 3 级方案（[references/evidence-grading.md](references/evidence-grading.md)）
- 反例必须取自档案已有材料（禁止网上现找）（[references/counter-example-rules.md](references/counter-example-rules.md)）
- 抓不到就写「未取得」，绝不构造 URL（[references/citation-discipline.md](references/citation-discipline.md)）
- 章节标题必须 `##` 级别（[references/chapter-rationale.md](references/chapter-rationale.md)）
- 禁商业黑话 + 禁模型路标词 + 禁借喻清单 + 禁破折号（[references/writing-style.md](references/writing-style.md)）
