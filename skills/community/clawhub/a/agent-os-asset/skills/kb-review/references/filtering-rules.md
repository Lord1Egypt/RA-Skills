# Supplemental Filtering Rules / 筛选补充规则

This file contains details that do not belong in `SKILL.md`. / 本文件包含不适合放入 `SKILL.md` 的补充说明。

## Human Feedback / 人工反馈

Treat user-edited decisions as preference samples: a keep decision in `delete.md` is a false-delete sample; a delete decision in `review.md` or `keep.md` is a false-keep sample. Common keep signals include coherent historical learning archives, course sequences, technical growth paths, personal projects, and work context. Common delete signals include copied public material, stale environment configuration, obsolete commands or APIs, unannotated installation steps, old sensitive environment notes, and generated aggregate indexes. / 将用户改过的 decision 作为偏好样本：`delete.md` 中的 keep 是误删样本，`review.md` 或 `keep.md` 中的 delete 是误留样本。常见保留信号包括成体系的历史学习档案、连续课程、技术成长路径、个人项目和工作上下文；常见删除信号包括公开资料搬运、旧环境配置、过时命令或 API、无批注安装步骤、旧敏感环境记录和生成式汇总索引。

Learn only from the latest review directory explicitly selected by the user. Do not turn one directory into a universal allowlist or denylist; prefer reusable cross-directory rules. The only exception is an explicit article-ID allowlist matched exactly by `source_path`. / 每轮只从用户明确指定的最新审查目录学习。不要把单个目录固化成通用白名单或黑名单；优先提炼跨目录可复用规则。唯一例外是按 `source_path` 精确匹配的显式文章 ID 白名单。

When an edited `decision` conflicts with the old `reason`, reread safely accessible evidence and rewrite the reason. If full or sampled evidence still cannot distinguish `0` from `1`, output a confirmation item instead of learning a permanent rule. / 当人工 `decision` 与旧 `reason` 冲突时，重新读取可安全访问的证据并改写 reason。若全文或采样后仍无法区分 `0` 与 `1`，输出待确认项，不固化规则。

## Explicit Article IDs To Keep / 显式保留文章 ID

The following `source_path` values are explicitly retained and must never be recommended for deletion, even when public-blog, copyright, repost, or CSDN signals appear. / 以下 `source_path` 是显式保留项，即使命中公开博客、版权、转载或 CSDN 信号，也不得建议删除。

<!-- # bilingual-compat: exact Chinese article path retained for source_path matching -->
- `030 PKV/LibRec每周算法：FTRL原理与工程实践.md`
<!-- # bilingual-compat: exact Chinese article path retained for source_path matching -->
- `mweb/LibRec每周算法：Kaggle竞赛利器之xgBoost.md`
<!-- # bilingual-compat: exact Chinese article path retained for source_path matching -->
- `mweb/Linkedin协同过滤推荐平台Browsemap赏析.md`
<!-- # bilingual-compat: exact Chinese article path retained for source_path matching -->
- `mweb/推荐系统不相信眼泪，但此算法会给你些安慰.md`

Do not generalize these IDs into a rule that all user-authored or published articles are retained. Judge other public or reposted material by personal annotation, information density, long-term reuse, and LLM or search replaceability. / 不要把这些 ID 泛化成“用户写过或发布过的文章都保留”。其他公开或转载资料仍按个人批注、信息密度、长期复用价值，以及 LLM 或搜索可替代性判断。

## Summary And Timeline Notes / Summary 与 Timeline 笔记

Do not delete external video or podcast `summary` or `timeline` files merely because they were generated automatically. Delete only under either narrow condition. / 不要仅因外部视频或播客的 `summary` 或 `timeline` 是自动生成就删除；只有以下窄条件允许删除。

- The generated or published date is more than 183 days before the scan date, and the body has no user revision, added judgment, action conclusion, or secondary processing. / 生成或发布日期早于扫描日 183 天以上，且正文没有用户修订、补充判断、行动结论或二次加工。
- Multiple `summary` or `timeline` files have similar titles or content, a canonical copy is retained, and the remaining copies are near-duplicates. / 多篇 `summary` 或 `timeline` 标题或内容相近，已保留 canonical，其余为近重复。

<!-- # bilingual-compat: legacy Chinese date-field literals retained for metadata matching -->
Prefer frontmatter or metadata dates such as `生成时间`, `发布日期`, `saved_at`, and `date created`. Without a date field, do not apply the age rule based only on file type. / 日期优先读取这些 frontmatter 或 metadata 字段；没有日期字段时，不得仅凭文件类型应用年龄规则。

## Judgment Frameworks / 判断框架

Keep personal experience that helps reuse decision logic, weigh trade-offs, or avoid repeated mistakes. / 保留能帮助复用判断逻辑、权衡取舍或避免重复踩坑的个人经验。

## Durable Foundations / 经典基础

Keep foundational knowledge that remains explanatory across tool cycles, especially when it includes personal annotations or repeated-use value. Older non-foundational material without personal annotation usually belongs in delete or review. / 保留跨工具周期仍有解释力的基础知识，尤其是带个人批注或反复使用价值的内容。非经典且无个人批注的旧资料通常应删除或复核。

## Historical Learning And Dense Public Material / 历史学习档案与高密度公开资料

Online availability alone is not enough to delete material. Keep or review public material when it is well structured, dense, consistently high quality, expensive to summarize, repeatedly useful, or part of a coherent historical learning path. / “网上能搜到”本身不足以支持删除。如果公开资料结构清晰、信息密度高、质量稳定、总结成本高、会反复使用，或属于成体系历史学习轨迹，应保留或复核。

If long-term value remains uncertain, place the item in `review.md` and explain the trade-off between retention value and replaceability in a bilingual reason. / 如果仍不确定长期价值，将其放入 `review.md`，并用双语 reason 说明保留价值与可替代性的权衡。

## Forbidden Reading / 禁止读取

Files matching `forbidden_paths` or `forbidden_tags` require no body processing. / 命中 `forbidden_paths` 或 `forbidden_tags` 的文件不处理正文。

- `forbidden_paths` matches file or directory paths. / `forbidden_paths` 按文件或目录路径匹配。
- `forbidden_tags` matches Markdown frontmatter `tags` exactly and includes `PII` by default. / `forbidden_tags` 精确匹配 Markdown frontmatter `tags`，默认包含 `PII`。
- A path match forbids even frontmatter reads; otherwise read only frontmatter metadata first to evaluate tags. / 路径命中时连 frontmatter 也不读取；路径未命中时，只先读取 frontmatter 元数据判断 tag。

## Default Scan Exclusions / 默认扫描排除

Exclude these path components by default. / 默认排除以下路径组件。

- `KB-Review-*`: current review output. / 当前审查输出。
- `KB-Refactor-*`: legacy review output retained for migration compatibility. / 为迁移兼容保留的历史审查输出。
- `AI-Era-*`: backup directories. / 备份目录。
- `Archived`: archived source directories. / 已归档原文目录。
- `.obsidian`, `.trash`, `.Trash`, `.smart-env`: tool configuration, cache, or Trash directories. / 工具配置、缓存或回收站目录。
<!-- # bilingual-compat: exact Chinese attachment path literals retained for legacy matching -->
- `Attachment`, `Attachments`, `attachment`, `attachments`, `附件`, `附件文件`, and matching `*.ext` basenames: attachment resources. / 这些名称及对应 `*.ext` basename 代表附件资源。
- Markdown whose frontmatter `tags` contains exact `archived`: archived and excluded without reading the body. / frontmatter `tags` 精确含 `archived` 的 Markdown 已归档，不进入候选且不读取正文。

These exclusions apply only to candidate body scanning; attachment resources are not independent review documents. / 这些排除只用于候选正文扫描；附件资源不作为独立审查文档。

## Large-File Sampling / 大文件采样

Read full bodies at or below 4096 tokens. Above 4096 tokens, use only the first and last 1000 tokens. / 正文不超过 4096 token 时全文读取；超过时只使用首尾各 1000 token。

## Agent-Readable Boundary / Agent-readable 边界

`kb-review` may read existing `.agent.md` frontmatter, summary, Insight, and Source Map as evidence. Generation, summarization, conversion, validation, and rebuilding rules belong to [`agent-readable-doc`](../../agent-readable-doc/SKILL.md); cross-asset architecture belongs to `agent-os-asset`. / `kb-review` 可只读使用已有 `.agent.md` 的 frontmatter、summary、Insight 和 Source Map。生成、摘要、转换、验证和重建规则属于 [`agent-readable-doc`](../../agent-readable-doc/SKILL.md)；跨资产架构属于 `agent-os-asset`。

## Project And Data-Bundle Judgment / 项目与数据包判断

Judge `asset_type=code_project` at project level, not by `.py`, `.java`, `.ipynb`, or other member files. Prefer safe README, AGENTS/CLAUDE, and docs/wiki evidence; use root package, build, manifest, run, control, main, app, or CLI evidence only when documentation is absent. Project documentation showing purpose, reuse, or workflow can support keep; root-entry-only evidence normally supports medium-confidence review; dependency or vendor bundles without independent context can be `archive_only`. Never recommend keep from code count, language, or directory name alone. / `asset_type=code_project` 按项目级判断，不按成员文件判断。优先使用安全的 README、AGENTS/CLAUDE 和 docs/wiki 证据；缺少文档时才使用根目录 package、build、manifest、run、control、main、app 或 CLI 线索。能说明目的、复用价值或工作流的项目文档可支持 keep；只有根入口证据通常支持中置信度 review；缺少独立上下文的依赖或 vendor bundle 可为 `archive_only`。不得仅凭代码数量、语言或目录名建议 keep。

Judge `asset_type=data_bundle` from metadata only: member count, formats, sample paths, parent context, and safely readable documentation. Do not create member-level body judgments or decisions. On delete, the adapter may trash only files in the member ledger and never the parent project or course directory. PII rules remain unchanged. / `asset_type=data_bundle` 只根据成员数量、格式、样例路径、父级上下文和可安全读取的文档判断。不要生成成员级正文判断或 decision。删除时 adapter 只能处理 member ledger 中的文件，不能删除父项目或课程目录；PII 规则不变。

## Confidence Scores / 置信度评分

| Score / 分值 | Meaning / 含义 | Typical signals / 典型信号 |
| --- | --- | --- |
| 3 | High confidence / 高置信度 | **keep-3**: personal dotfiles, custom aliases, project runbooks, annotated cheatsheets. **delete-3**: verbatim official tutorials, generic AI-generated docs, default shortcut lists. / **keep-3**：个人 dotfile、自定义 alias、项目 runbook、有批注 cheatsheet。**delete-3**：逐字官方教程、通用 AI 生成文档、默认快捷键列表。 |
| 2 | Medium confidence / 中置信度 | **keep-2**: learning notes with personal context on an LLM-coverable topic. **delete-2**: mostly public material with one or two personal comments. / **keep-2**：有个人上下文但 LLM 可覆盖的学习笔记。**delete-2**：主要是公开内容，仅有一两行个人注释。 |
| 1 | Low confidence / 低置信度 | **keep-1**: somewhat personal but mostly generic. **delete-1**: uncertain authorship, old, or niche. / **keep-1**：略有个人化但内容通用。**delete-1**：原创性不明、较旧或主题冷门。 |

`confidence=1` means high human-review priority but does not block deletion; confirmed deletion still requires `decision=0/delete`. / `confidence=1` 表示人工复核优先级高，但不阻止删除；确认删除仍必须设置 `decision=0/delete`。

`review.md` defaults to `decision=1`, `confidence=1`. After review, raise confidence to `2` or `3` when keeping, or change decision to `0` when deleting. / `review.md` 默认 `decision=1`、`confidence=1`。人工确认后，保留时将 confidence 调到 `2` 或 `3`；删除时将 decision 改为 `0`。
