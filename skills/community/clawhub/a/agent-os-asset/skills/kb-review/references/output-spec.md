# Output Specification / 输出规范

By default, produce only four Markdown review files and no CSV. / 默认只输出四个 Markdown 审查文件，不输出 CSV。

In Agent OS historical modernization, `.cleanup-extracted/asset-manifest.jsonl` comes from [`agent-readable-doc`](../../agent-readable-doc/SKILL.md) or a project adapter; it is not a default output of this Skill. `kb-review` produces editable value judgments, and [`second-brain`](../../second-brain/SKILL.md) indexes retained independent assets only after decisions are complete. / 在 Agent OS 历史资料改造中，`.cleanup-extracted/asset-manifest.jsonl` 由 [`agent-readable-doc`](../../agent-readable-doc/SKILL.md) 或项目 adapter 生成，不是本 Skill 的默认输出。`kb-review` 输出可编辑的价值判断；决策完成后，[`second-brain`](../../second-brain/SKILL.md) 才索引保留的独立资产。

## Default Directory / 默认目录

Use an independent review workspace under the source knowledge-base root. / 在原始知识库根目录下使用独立审查工作目录。

`KB-Review-YYYY-MM-DD/`

Recommended structure / 建议结构:

```text
KB-Review-YYYY-MM-DD/
  keep.md
  delete.md
  review.md
  duplicates.md
  trash-execution-log.md
  trash-rollback-log.md
```

Generate `trash-execution-log.md` after delete preview or execution, and `trash-rollback-log.md` after rollback preview or execution. Generate `second-brain-coverage.md` only after explicit `--second-brain-coverage`; do not create it by default. / delete 预演或执行后生成 `trash-execution-log.md`，rollback 预演或执行后生成 `trash-rollback-log.md`。只有显式使用 `--second-brain-coverage` 才生成 `second-brain-coverage.md`，默认不生成。

## Default Scan Exclusions / 默认扫描排除

Exclude obvious non-review paths or basenames. / 排除明显不应进入审查的路径或 basename。

- `KB-Review-*`: current review output. / 当前审查输出。
- `KB-Refactor-*`: legacy review output retained for migration compatibility. / 为迁移兼容保留的历史审查输出。
- `AI-Era-*`: backup directories. / 备份目录。
- `Archived`: archived source directories. / 已归档原文目录。
- `.obsidian`, `.trash`, `.Trash`, `.smart-env`: tool configuration, cache, or Trash directories. / 工具配置、缓存或回收站目录。
<!-- # bilingual-compat: exact Chinese attachment path literals retained for legacy matching -->
- `Attachment`, `Attachments`, `attachment`, `attachments`, `附件`, `附件文件`, and matching `*.ext` basenames: attachment resources. / 这些名称及对应 `*.ext` basename 代表附件资源。
- Markdown whose frontmatter `tags` contains `archived`: archived and excluded. / frontmatter `tags` 含 `archived` 的 Markdown 已归档并排除。

## Files / 文件

- `keep.md`: files recommended for retention. / 建议保留的文件。
- `delete.md`: files recommended for deletion. / 建议删除的文件。
- `review.md`: files requiring human review. / 建议人工复核的文件。
- `duplicates.md`: groups with identical body content. / 正文内容相同的文件组。

The filenames describe only the initial grouping. Users may edit row-level `decision` values directly. Delete execution follows `decision=0/delete`; across all review files, `1` means keep and `0` means delete. / 文件名只表示初始建议分组。用户可以直接修改行内 `decision`；delete 执行以 `decision=0/delete` 为准。所有审查文件中，`1` 表示保留，`0` 表示删除。

## Agent-Readable Boundary / Agent-readable 边界

`kb-review` may read existing `.agent.md` frontmatter, summary, Insight, and Source Map, and may generate a read-only SecondBrain coverage report. It does not generate, modify, reorder, re-summarize, validate, or archive `.agent.md`; those rules belong to [`agent-readable-doc`](../../agent-readable-doc/SKILL.md) and `agent-os-asset`. / `kb-review` 可只读使用已有 `.agent.md` 的 frontmatter、summary、Insight 和 Source Map，也可生成只读 SecondBrain coverage 报告。它不生成、修改、重排、重新摘要、验证或归档 `.agent.md`；这些规则属于 [`agent-readable-doc`](../../agent-readable-doc/SKILL.md) 和 `agent-os-asset`。

## Table Fields / 表格字段

`keep.md`, `delete.md`, and `review.md` share this table. / `keep.md`、`delete.md` 和 `review.md` 共用此表。

| index | decision | confidence | title | reason | source_path |
| --- | --- | --- | --- | --- | --- |

`duplicates.md` adds a group field. / `duplicates.md` 增加 group 字段。

| duplicate_group | index | decision | confidence | title | reason | source_path |
| --- | --- | --- | --- | --- | --- | --- |

Field meanings / 字段含义:

- `duplicate_group`: used only in `duplicates.md`, such as `dup-001`; identical bodies share one group. / 仅用于 `duplicates.md`，例如 `dup-001`；正文相同的文件使用同一组。
- `index`: starts at `1` in each file and exists only for human navigation. / 每个文件内从 `1` 开始，只用于人工定位。
- `decision`: `1` keeps and `0` deletes; legacy `keep/delete/review` values remain compatible, and `review` is non-actionable. / `1` 保留，`0` 删除；兼容旧值 `keep/delete/review`，其中 `review` 不触发动作。
- `confidence`: `1` through `3`, used for review priority and never as a deletion gate. / 取值 `1` 到 `3`，用于复核优先级，不作为删除门槛。
- `title`: source title or a short title derived from safe evidence; preserve its original language. / 源标题或根据安全证据提炼的短标题；保持原语言。
- `reason`: a complete rule-based explanation written as `English / 中文`, with English first. / 按规则给出的完整说明，使用 `English / 中文`，英文在前。
- `source_path`: original path. Inside an Obsidian vault, prefer a wikilink such as `[[Flomo/AI/Agent.agent\|AI/Agent.agent.md]]`, escaping the alias separator as `\|`. The script also accepts plain paths, `[label](path)`, `[label](<path with spaces>)`, and wikilinks. Relative paths resolve from the review file directory; wikilink targets resolve from the nearest `.obsidian` vault root. / 原始路径。在 Obsidian vault 内优先使用 wikilink，并将 alias 分隔符转义为 `\|`。脚本也兼容纯路径、Markdown link 和 wikilink；普通相对路径从审查文件目录解析，wikilink target 从最近的 `.obsidian` vault root 解析。

## Duplicate Rules / 重复项规则

Define identical content by an exact hash of the readable body. Files matching `forbidden_paths` are not read or hashed. Files matching `forbidden_tags` are not read for classification or summarization, but may use a byte-level exact hash without exposing content to the model; write them to `duplicates.md` only when at least two files match exactly, otherwise default them to `keep.md`. / “内容相同”按可读正文的精确 hash 定义。命中 `forbidden_paths` 的文件不读取也不参与 hash。命中 `forbidden_tags` 的文件不读取正文用于分类或摘要，但可在不把正文交给模型的前提下计算 byte-level 精确 hash；只有至少两个文件完全一致时才写入 `duplicates.md`，否则默认写入 `keep.md`。

If an entire duplicate group should be deleted, set every row to `decision=0`. If it should be retained, set the first canonical row to `decision=1` and copies to `decision=0`. / 若整组重复内容都应删除，所有行设为 `decision=0`；若应保留，首个 canonical 行设为 `1`，其余副本设为 `0`。

Choose the canonical file by richer path, filename, or frontmatter and better structural location; otherwise choose the shorter path, then lexical `source_path` order. / canonical 文件优先选择路径、文件名或 frontmatter 信息更丰富且结构位置更合理的版本；否则选择较短路径，再按 `source_path` 字典序。

## Human Feedback / 人工反馈

Before applying learned preferences, inspect user edits: keep decisions in `delete.md` are false-delete samples; delete decisions in `review.md` or `keep.md` are false-keep samples. Use path, title, reason, and safely readable content, but never turn one directory into a universal allowlist. / 学习偏好前先检查用户改判：`delete.md` 中的 keep 是误删样本，`review.md` 或 `keep.md` 中的 delete 是误留样本。结合 path、title、reason 和可安全读取内容判断，但不要把单个目录固化成通用白名单。

Retention signals include historical learning archives, course sequences, early learning routes, personal projects, drafts, verifiable original articles, work context, retrospectives, templates, judgment frameworks, and technical-route evolution. Deletion signals include isolated stale configuration, copied public tutorials, obsolete command or API excerpts, unannotated install steps, old sensitive environment notes, generated aggregate indexes, and public material with weak personal traces. Do not treat “possibly authored by the user” as a default keep rule; require an explicit article-ID allowlist match or direct evidence of original judgment. / 保留信号包括历史学习档案、连续课程、早期学习路线、个人项目、草稿、可证实原创文章、工作上下文、复盘、模板、判断框架和技术路线演化。删除信号包括孤立旧配置、公开教程搬运、过时命令或 API 摘录、无批注安装步骤、旧敏感环境记录、生成式汇总索引，以及个人痕迹弱的公共资料。不要把“可能由用户创作”作为默认保留规则；必须命中显式文章 ID 白名单或有直接原创判断证据。

<!-- # bilingual-compat: exact Chinese article path literals retained for source_path matching -->
The explicit keep allowlist is `030 PKV/LibRec每周算法：FTRL原理与工程实践.md`, `mweb/LibRec每周算法：Kaggle竞赛利器之xgBoost.md`, `mweb/Linkedin协同过滤推荐平台Browsemap赏析.md`, and `mweb/推荐系统不相信眼泪，但此算法会给你些安慰.md`. A matching reason must say that the user explicitly retained the item rather than citing public-blog or repost signals. / 显式保留白名单为上述四个 `source_path`；命中时 reason 必须说明用户显式保留，而不是把公开博客或转载信号当作删除依据。

Do not delete external video or podcast `summary` or `timeline` merely because it is generated. Delete only when it is older than 183 days with no user revision, added judgment, action conclusion, or secondary processing, or when a canonical near-duplicate is retained. / 不要仅因外部视频或播客的 `summary` 或 `timeline` 是自动生成就删除。只有超过 183 天且没有用户修订、补充判断、行动结论或二次加工，或已有保留的 canonical 近重复时，才允许删除。

<!-- # bilingual-compat: legacy Chinese date-field literals retained for metadata matching -->
Prefer date fields such as `生成时间`, `发布日期`, `saved_at`, and `date created`; without a date field, do not apply the age rule from file type alone. / 日期优先读取这些字段；没有日期字段时，不得仅凭文件类型应用年龄规则。

For sensitive samples, use only path, title, frontmatter, and existing review reason; do not read or repeat sensitive body content. `forbidden_tags` items default to keep and enter `duplicates.md` only after a byte-level exact duplicate match. / 对敏感样本，只使用路径、标题、frontmatter 和已有 review reason，不读取或复述敏感正文。命中 `forbidden_tags` 的条目默认保留，仅在 byte-level 精确重复时进入 `duplicates.md`。

## Reason Requirements / Reason 要求

Every generated `reason` must be specific and bilingual as `English / 中文`. Include these elements when applicable. / 每个生成的 `reason` 必须具体，并按 `English / 中文` 双语书写；适用时包含以下内容。

1. Body evidence, including an explicit sampling statement for large files; read all text at `<=4096` tokens and only the first and last `1000` tokens above that threshold. / 正文证据；大文件必须明确说明采样。`<=4096` token 全文读取，超过时只读首尾各 `1000` token。
2. The concrete keep, delete, or review rule that matched. / 命中的具体保留、删除或复核规则。
3. Whether current LLMs or search can reconstruct the information easily. / 当前 LLM 或搜索是否能轻松重建该信息。
4. Risks or exceptions such as personal annotation, privacy, durable foundations, duplicates, missing files, forbidden paths, or forbidden tags. / 风险或例外，例如个人批注、隐私、经典基础、重复项、缺失文件、禁止路径或禁止标签。

Do not delete mechanically because material is searchable online. High-quality, dense, structured public material may be kept or reviewed when it captures a historical learning trail or has strong reuse value. Conversely, public material with only weak personal traces and no judgment, project context, or retrospective may be deleted when the reason explains why false-deletion risk is controlled. / 不要因为资料可在线搜索就机械删除。高质量、高密度、结构化的公开资料，如果体现历史学习轨迹或有较强复用价值，可以保留或复核。反之，只有弱个人痕迹且没有判断、项目上下文或复盘的公共资料，可以在 reason 说明误删风险可控后删除。

## Optional Outputs / 可选输出

Create these files only after the matching preview or execution is explicitly requested. / 只有明确请求对应预演或执行时才生成这些文件。

- `trash-execution-log.md`: records `source_path`, `trash_path`, `status`, force-delete reason, root-boundary skips, and `pruned_dirs`. Default status is `planned-trash`; only `--execute` produces `moved-to-trash`. Prune parents only after a successful move and never above `review_root`. / 记录删除预演或执行信息。默认状态为 `planned-trash`；只有 `--execute` 产生 `moved-to-trash`。仅在成功移动后清理父目录，且不得越过 `review_root`。
- `trash-rollback-log.md`: records rollback status, `source_path`, `trash_path`, `restored_path`, and a bilingual note. Only `--execute` moves files. / 记录 rollback 状态、路径和双语 note；只有 `--execute` 实际移动文件。
- `second-brain-coverage.md`: read-only coverage for active raw rows and indexed `.agent.md` counterparts. Generate it only on explicit request; mark `Archived/` and `archived`-tagged rows as `skipped-archived`. / 记录 active raw 行与 indexed `.agent.md` 对应关系的只读 coverage。仅在明确请求时生成；`Archived/` 与带 `archived` tag 的行标记为 `skipped-archived`。

Do not create other intermediate files by default. The deterministic script reads all four review files, acts only on `decision=0/delete`, ignores `decision=1/keep` and legacy `decision=review`, preserves `duplicate_group` in reports, accepts only safe literal relative force-delete components, and constrains delete and rollback paths to explicit roots. Coverage never changes decisions. / 默认不生成其他中间文件。确定性脚本读取四个审查文件，只处理 `decision=0/delete`，忽略 `decision=1/keep` 与旧版 `decision=review`，在报告中保留 `duplicate_group`，只接受安全的字面量相对 force-delete 组件，并以显式根目录约束 delete 与 rollback 路径。coverage 不修改决策。

Use the model only for classification, judgment, and generation of bilingual review files. After human review, `--delete` and `--rollback` are deterministic and require no model. / 模型只用于分类、判断和生成双语审查文件。人工复核后，`--delete` 与 `--rollback` 是确定性操作，不再需要模型。
