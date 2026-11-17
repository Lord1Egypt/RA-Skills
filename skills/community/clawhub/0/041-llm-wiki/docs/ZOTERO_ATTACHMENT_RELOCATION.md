# Zotero 附件受控搬迁设计（方案六）

> 状态：设计完成、受限实现阶段。本文档定义目标、边界、状态机和验收门槛；当前代码已实现 dry-run 和受限 apply 流程，但在 Phase 0 的 Zotero 附件写回能力验证通过、用户显式启用配置并完成本地授权前，不对用户库执行搬迁写操作。
>
> 本方案的目标不是把 ZotMoov 的插件内部实现机械搬到 llm-wiki，而是在 llm-wiki 的外部进程、MCP 和能力契约边界内，提供一个可审计、可恢复、默认不破坏数据的附件搬迁流程。

## 1. 目标与非目标

### 1.1 目标

llm-wiki 增加一个显式授权的附件搬迁能力，负责把当前机器上可解析的 Zotero 附件放入用户配置的受管根目录，并保持以下三层定位一致：

1. Zotero 附件条目的真实 `path` / `linkMode`；
2. `sources/zotero/metadata.yaml` 中的 `local_path` 快照；
3. `sources/zotero/` 下供 Agent 使用的 alias 或 symlink。

搬迁流程应支持：

- 以 Zotero Collection 层级、作者、年份、标题、引用键和条目类型等字段生成目录与文件名；
- 跨平台文件名清洗、UTF-8 字节级截断和扩展名保护；
- 目标路径 containment 校验、冲突避让、重复执行幂等；
- dry-run、逐附件结果、失败恢复和 post-write verify；
- 尽量保留原附件 item key、父条目、子项、批注和关系；
- 只在用户明确允许时清理旧文件，不覆盖既有文件。

### 1.2 非目标

以下内容不属于第一版搬迁能力：

- 迁移 Zotero 数据目录、`zotero.sqlite` 或任何 live database；
- 通过普通文件扫描猜测 Zotero 附件，绕过 MCP 的权威路径解析；
- 修改笔记正文或重写笔记中的附件引用；
- 通过新建条目、删除旧条目的方式模拟插件内部行为，除非未来具备经过验证的、能保留全部子项与引用的 API 能力；
- group library 的跨机器附件搬迁；
- 修改 wiki 页面名或把附件路径模板用于 wiki 页面命名；
- 在没有用户审查的情况下删除 Zotero storage 中的旧文件；
- 把 Web API 的“写入成功”当作本机 Zotero Desktop 已经更新的证据。

## 2. 已确认的事实与关键约束

### 2.1 ZotMoov 的本体语义

对照 ZotMoov 源码，附件移动不是简单的 `rename()`：

- 它先生成不覆盖既有文件的目标路径并复制文件；
- 在 Zotero 内部创建或更新 linked-file 附件；
- 转移子项、批注、关系和 full-text 索引；
- 重写笔记中的旧附件 key 引用；
- 确认新附件可用后删除旧项和旧文件。

因此，ZotMoov 的“保留用户体验”依赖 Zotero 插件内部 API，而不是单个文件系统操作。llm-wiki 运行在 Zotero 外部，不能假设拥有同等的 clone、子项迁移或笔记 re-key 能力。

### 2.2 llm-wiki 的现有边界

- Zotero 负责元数据、附件、批注、Collections、标签、引用键及其他库状态；llm-wiki 负责知识页面、来源蒸馏和索引。
- Zotero MCP 是发现、元数据、附件 key 和路径解析的首选入口。
- 当前 zotero-mcp 的写入能力不能自动推断为 Zotero 10 Local API 写入；需要确认真实后端并执行写后重读。
- `sources/zotero/metadata.yaml` 是路径快照，不是附件位置的权威来源。
- `scripts/zotero_sources.py` 已经对 `source_alias` 做 project-root 下的 containment 校验，并支持 metadata-only、copy、hardlink 三种 symlink 降级模式。
- 当前已有能力契约没有给普通命令开放任意 `sources/`、Zotero storage 或用户文件系统的写权限。

### 2.3 核心设计判断

**第一版不做无条件的 clone-and-repoint fallback。** 如果外部 API 无法以可验证的方式保留 item key、父子关系和批注，命令必须拒绝该附件，而不是创建一个看似成功但可能丢失笔记引用或批注的替代条目。

这意味着“llm-wiki 自己承担搬迁职责”与“完全复刻 ZotMoov 的所有内部细节”是两个不同目标：前者是本方案的目标，后者受 Zotero 外部 API 能力约束，不能通过猜测实现。

## 3. 建议架构

### 3.1 独立命令与适配层

新增一个独立的 `zotero-relocate` 能力，建议实现为以下边界清晰的层：

```text
命令入口
  ├─ 读取配置、选择条目、生成 dry-run 计划
  ├─ 调用 ZoteroAttachmentAdapter 获取权威路径和执行受限写回
  ├─ 调用 RelocationPlanner 生成目标路径、校验冲突和安全边界
  ├─ 调用 FileTransaction 执行 copy / verify / cleanup
  ├─ 更新 metadata.yaml 并调用现有 materialize 流程
  └─ 输出审计结果与可恢复状态
```

建议代码位置为：

- `src/llm_wiki/zotero_relocate.py`：计划、状态机、路径与结果模型；
- `src/llm_wiki/zotero_attachment_adapter.py`：Zotero 附件读取、写回和 post-write verify；
- `scripts/zotero_sources.py`：复用或小范围扩展 metadata 更新后的 alias materialization；
- `src/llm_wiki/capabilities.py`：声明动态受管根目录和 metadata 文件的写入边界；
- `tests/`：纯文件系统测试、fake adapter 测试和显式隔离的本地 API smoke test。

命令不应把 Zotero HTTP 细节、文件搬迁、YAML 文本替换和日志输出全部堆在一个函数中。这样可以让不具备 Zotero 的测试覆盖路径安全和事务恢复，也可以让未来替换 MCP / Local API adapter 时不改变文件系统状态机。

### 3.2 两阶段运行模式

#### `plan` / `--dry-run`

只读读取以下信息：

- 目标 Collection 或显式附件 key；
- Zotero 权威解析出的当前附件路径、`linkMode`、文件名和父项关系；
- Collection 层级和命名模板字段；
- 当前 `metadata.yaml` 绑定和 alias 状态；
- 目标路径、冲突、路径 containment 和能力契约结果。

输出每个附件的计划状态，例如 `ready`、`same-target`、`collision`、`missing-local-path`、`unsupported-backend` 或 `blocked-by-policy`。dry-run 不创建目录、不复制文件、不修改 Zotero、不写 metadata。

报告中的普通日志不打印完整的用户私有路径；详细路径只允许出现在 gitignored 的本地审计产物中，并且不能包含凭证或环境变量内容。

#### `apply`

apply 必须重新读取关键前置条件，而不是盲目执行旧计划：

1. 重新解析附件当前路径和 item version；
2. 确认源文件仍与计划中的文件指纹一致；
3. 确认目标路径仍未被其他文件占用；
4. 确认能力契约仍允许所有待写路径；
5. 按第 5 节状态机逐项执行；
6. 每个外部写回后立即 post-write verify；
7. 任何一项不满足都停止当前附件，其他附件逐条报告，不把单条失败升级为整个批次崩溃。

## 4. 配置草案

配置键名在实现前仍需与项目配置加载方式对齐；下面的结构用于固定语义，不代表已经承诺的最终 schema：

```yaml
zotero_relocation:
  enabled: false
  # 推荐在 config.yaml 配置一次，而不是每次用 --root 传入；跨设备同步时指向网盘同步目录，
  # 并用环境变量保持可移植，例如 "${OneDrive}/zotero-attachments"。
  root: "/absolute/path/to/managed-attachments"
  storage_root: "/absolute/path/to/zotero/storage"
  path_template: "%c/%y-%a-%t"
  max_component_bytes: 120
  collision_policy: "suffix"
  delete_source: false
  allowed_source_roots: []
  update_metadata: true
  materialize_aliases: true
  # true:写回 Zotero 的 path 为 "attachments:<相对路径>"(相对于 root),由每台设备的
  # Linked Attachment Base Directory 各自解析,跨操作系统(Windows/Linux)可移植。
  base_dir_relative: false
```

约束如下：

- `enabled` 默认为 `false`；未显式启用时命令 fail closed。
- `root` 必须是绝对路径，启动时解析并固定；不能是项目根、`sources/`、Zotero 数据库目录或未解析的相对路径。`root` 应在 `config.yaml` 中配置（`--root` 仅为一次性覆盖）；跨设备同步时应指向网盘同步目录，且每台设备都必须能访问同一根目录，可用 `${OneDrive}` 等环境变量保持路径可移植。跨操作系统（如 Windows + Linux）时绝对路径不可能一致，必须设 `base_dir_relative: true`，使写回 Zotero 的路径为 `attachments:<相对路径>` 便携形式，并在每台设备上把 Zotero 的 Linked Attachment Base Directory 指向本机的 `root` 等价路径；重跑时 `attachments:` 源路径也会相对 `root` 解析，保证幂等。
- `path_template` 只生成附件布局，不参与 wiki 页面命名。模板字段必须是白名单字段，字段值先按路径组件清洗，禁止把原始 `/`、`\\`、`.` 或 `..` 当作组件直接拼接。
- `max_component_bytes` 应小于目标文件系统上限，并为扩展名和冲突序号预留空间；默认值应由实现和跨平台测试最终确定。
- `collision_policy: suffix` 表示永不覆盖，按有限次数尝试 `name 2.ext`、`name 3.ext` 等候选名；达到上限则报告冲突并跳过。
- `delete_source` 默认为 `false`。即使设为 `true`，源文件也必须位于 `allowed_source_roots`，并通过逐项 containment、身份和引用检查。
- `update_metadata` 与 `materialize_aliases` 控制 llm-wiki 本地层是否同步；二者不能改变 Zotero 本身的写回结果。

## 5. 搬迁状态机与顺序

外部文件系统、Zotero 和 YAML 文件无法组成一个真正的跨系统原子事务，因此实现目标是**有序、可审计、可恢复**，而不是假称原子完成。

### 5.1 单附件状态

```text
planned
  → source-verified
  → target-prepared
  → target-copied
  → target-verified
  → zotero-repointed
  → zotero-verified
  → metadata-updated
  → alias-materialized
  → source-cleaned
  → complete
```

每个状态都应记录 item key、attachment key、当前 item version、源/目标文件指纹、目标路径的受管根、完成时间和下一步。状态记录不保存认证信息。

### 5.2 推荐顺序

1. **解析权威源**：不使用旧 `metadata.yaml.local_path` 作为事实来源；通过 MCP / 允许的本地能力重新解析当前附件路径。
2. **验证源文件**：确认路径存在、是普通文件、可读，并取得流式 hash、大小和修改时间。
3. **生成目标**：根据 Collection 路径和白名单字段生成目标相对路径，执行组件清洗、字节截断和扩展名保护。
4. **检查目标**：在创建目录前做 lexical 和 resolved containment 校验；拒绝穿越、危险 symlink 父目录和不受管目标。
5. **复制并校验**：以临时文件写入目标目录，完成后执行大小和 hash 校验，再原子 rename 到最终目标；不覆盖既有文件。
6. **Zotero 写回**：优先尝试保留原 item key 的 `linkMode` / `path` 更新；写回范围只允许当前附件及其路径字段。
7. **Zotero 重读验证**：确认 item key、父条目、attachment key、`linkMode`、目标路径和 item version 符合预期；无法确认时停止，不更新 metadata。
8. **更新 metadata**：只替换对应 attachment 的 `local_path`，保留 `zotero_item_key`、`zotero_attachment_key`、`source_alias` 及其他字段；使用临时文件 + 原子替换，并保留操作前快照用于恢复。
9. **修复 alias**：调用现有 materialize 逻辑，让 alias 指向新路径；只允许替换受管的 symlink，不覆盖用户创建的普通文件。
10. **清理旧源**：仅在 `delete_source: true`、路径位于 `allowed_source_roots`、旧路径仍指向本次源文件且没有其他附件引用时执行；否则留下旧文件并标记 `cleanup-pending`。
11. **完成审计**：重读 Zotero、metadata 和 alias，确认三层路径一致后才标记 `complete`。

### 5.3 失败与恢复

- `source-verified` 之前失败：不创建、不写回。
- 复制或目标校验失败：只删除本次操作创建且指纹一致的临时/目标文件。
- Zotero 写回失败：metadata 保持不变；若目标是本次新建且未被其他记录引用，可安全清理，否则保留并标记孤儿候选。
- Zotero 写回成功但 metadata 更新失败：不得盲目反向写回；保留目标，生成 `metadata-repair-needed`，通过 verify/reconcile 继续完成本次操作。
- alias 更新失败：Zotero 和 metadata 保持新路径，记录 `alias-repair-needed`；不得删除仍被旧 alias 使用的源文件。
- 清理失败：不回滚已验证的新路径，只报告 `cleanup-pending`，供下一次显式 reconcile 处理。
- 清理成功后：不自动尝试反向搬回。因为跨系统状态可能已被用户或 Zotero 同步改变，恢复必须基于新的权威读取和用户确认。

## 6. Zotero 写回策略与 Phase 0 门槛

### 6.1 优先路径：保留 item key 的原地更新

第一版的首选路径是对现有附件条目执行受限更新，使其继续使用原 attachment item key，只改变 `linkMode` 和 `path`（具体字段名与后端行为必须通过 spike 确认）。如果该更新由 Zotero 接受并能被同一权威后端重读，子项、批注、关系和笔记引用可以由 Zotero 自身继续关联，llm-wiki 无需触碰笔记。

必须验证：

- imported-file → linked-file 是否被支持；
- linked-file → linked-file 路径变更是否被支持；
- `path` 的绝对路径、相对 storage 路径和平台分隔符如何解释；
- 写回后旧 stored 文件由谁负责清理；
- Web API、Zotero 10 Local API 和 zotero-mcp 实际使用的后端是否一致；
- 写回后的 item version、attachment key、父条目、子项和批注是否保持不变。

### 6.2 不能接受的 fallback

以下行为不能作为“先实现再说”的替代方案：

- 直接创建一个新的附件条目，再删除旧条目，但不迁移子项、批注、关系和笔记引用；
- 只修改 `metadata.yaml` 或 symlink，却不更新 Zotero 的真实附件路径；
- 只修改 Zotero 路径，却不执行写后重读和本地层校验；
- 使用 Web API 成功响应推断 Local API 已经更新；
- 通过 glob、标题或文件名猜测附件归属；
- 在根目录 containment 未验证时删除任何旧文件。

### 6.3 Phase 0 验证场景

Phase 0 使用隔离的测试库和临时目录，不接触用户主库。至少覆盖：

1. 一个 imported PDF，包含父条目、子项和可读取批注；
2. 一个已有 linked PDF；
3. 同名目标和目标目录中的冲突文件；
4. 非 ASCII 标题、非法字符、超长标题和多重 Collection；
5. API 写回中途失败、版本冲突和写后读不到目标路径；
6. 现有 alias、copy fallback 和 metadata-only 模式；
7. Web-only / local / hybrid 能力不完整的情况。

只有在 item key 保持、关系完整、写后路径可重读且失败状态可恢复时，才允许进入 Phase 1。

## 7. 安全与能力契约

### 7.1 动态写范围

`zotero-relocate` 必须拥有独立能力声明，不能借用 `zotero-writeback` 的标签或关系写范围。有效写范围至少包含：

- 配置解析后的受管附件根目录；
- 项目内 `sources/zotero/metadata.yaml`；
- 受管 alias 的父目录（仅允许现有 materialize 语义）；
- 经过显式配置并逐项校验的 `allowed_source_roots`，仅用于旧源清理。

能力检查必须在 plan 和 apply 两次执行；配置变更、root 解析结果变化或计划外路径出现时，整个附件操作 fail closed。

### 7.2 路径安全不变量

- 所有用户可控模板字段先变成单一安全路径组件，再拼接相对路径。
- 目标路径必须同时通过字符串规范化和实际文件系统解析后的 containment 检查。
- 目标目录中已有 symlink、junction 或 reparse point 导致路径逃逸时拒绝操作。
- 不跟随来源文件的 symlink 去执行未经授权的删除；旧源清理必须验证最终目标仍在允许根目录内。
- 不覆盖既有普通文件、alias 或未知内容；同一操作创建的临时文件除外。
- 路径、标题、Collection 名称和 Zotero 返回字段都视为不可信输入，禁止进入 shell 命令或未参数化查询。

### 7.3 同步边界

stored attachment 转为 linked attachment 可能改变 Zotero File Sync 的行为：文件字节可能不再由 Zotero File Sync 管理，其他设备也未必能访问配置的外部根目录。每次 apply 前必须在报告中明确提示这一点，并要求用户选择本机布局是否适合作为权威附件位置。

本方案不自动暂停、重置或修复 Zotero 同步；如果本地库与 Web 库已经分叉，必须先停止搬迁，让用户在 Zotero 中选择权威方向，完成同步后重新审计。

## 8. 与 `sources/zotero/` 的集成

### 8.1 metadata 更新原则

`metadata.yaml` 只保存可复现的绑定信息，不承担 Zotero 权威状态：

- `zotero_item_key` 和 `zotero_attachment_key` 不变；
- `local_path` 在 Zotero 写回验证成功后更新；
- `source_alias` 默认不改名，因为它是 wiki frontmatter `sources[]` 的锚点；
- 使用结构化 YAML 更新或最小范围文本替换，不能重排无关条目；
- 更新失败必须留下可重试的 repair 状态，而不是写入半截文件。

### 8.2 alias materialization

metadata 更新完成后，复用 `scripts/zotero_sources.py` 的幂等 materialize 行为：

- symlink 指向新 `local_path` 时跳过；
- 旧 symlink 指向其他路径时只在 `--force` 且目标确实为受管 symlink 时替换；
- copy fallback 不得被当作 symlink 成功；
- 受管 alias 与目标内容不一致时报告错误，不覆盖普通文件。

如果 alias 修复失败，Zotero 和 metadata 的新定位仍然是事实来源，下一次 reconcile 应根据 attachment key 修复 alias，而不是根据旧 alias 反推源文件。

## 9. 分阶段实施路线

### Phase 0：能力验证与协议定稿（P0）

- 为 Zotero attachment adapter 建立隔离测试库 spike；
- 确认保留 item key 的路径写回是否可用；
- 明确 MCP、Local API 和 Web API 的真实后端差异；
- 将附件写回加入独立能力契约和 canonical Zotero operating protocol；
- 在没有满足验收条件前，命令只提供 dry-run / audit。

### Phase 1：安全搬迁核心（P1）

- 实现模板字段白名单、路径组件清洗、字节截断和冲突避让；
- 实现 copy-verify-repoint-verify 的单附件状态机；
- 实现能力契约、dry-run、逐条错误和审计状态；
- 默认禁止旧源删除。

### Phase 2：本地层一致性（P1）

- 原子更新 `metadata.yaml`；
- 联动 `zotero_sources.py` materialize；
- 增加 alias repair 和 `cleanup-pending` reconcile；
- 覆盖 metadata-only、copy、hardlink 和跨平台行为。

### Phase 3：受控清理与恢复增强（P2）

- 在显式 `allowed_source_roots` 下实现旧源清理；
- 增加引用去重检查、操作前快照和恢复报告；
- 研究 Zotero 同步协调，但不自动调用破坏性同步操作；
- 只有在外部 API 能安全支持时，才评估 clone-and-repoint 的扩展。

## 10. 验收清单

实现完成前必须同时满足：

- 默认配置不会产生任何写操作；
- dry-run 不创建目录、不写 Zotero、不改 metadata；
- 每个文件系统写路径均经过能力契约和 containment 校验；
- 目标文件永不被覆盖，重复执行是幂等的；
- 写回后原 attachment item key、父项和子项关系保持不变；
- 批注可继续访问，命令从不修改笔记正文；
- Zotero、metadata 和 alias 三层重读结果一致；
- 单个附件失败不会掩盖其他附件结果，也不会让批次留下未记录的半成品；
- 清理旧源需要显式配置、允许根目录和逐项引用检查；
- Web/local/hybrid 后端差异和 stored→linked 的同步影响在 apply 前可见；
- 测试覆盖路径穿越、symlink 逃逸、冲突、权限失败、版本冲突、半完成状态和恢复；
- canonical Zotero protocol、能力契约和用户文档在实现前同步更新。

## 11. 待 Phase 0 决定的问题

1. ~~Zotero 10 Local API 是否允许在不新建附件条目的情况下更新现有 attachment item 的 `linkMode` 与 `path`？~~ **已由实证回答（2026-08-29）：不允许 imported→linked 转换。** 对 `{linkMode: "linked_file", path: "attachments:..."}` 的 PATCH 返回 HTTP 500 但部分生效：7 个条目被置为 `linkMode: linked_file`、`path` 保留旧的 `storage:` 伪路径、`filename` 清空、`version` 归零，处于不一致状态；文件本身无损。反向的简单字段回退（`linkMode: imported_file` + `filename`）可正常 PATCH 并恢复。因此 imported→linked 转换必须走 Zotero 原生 "Convert Stored Files to Linked Files" 或 ZotMoov 等内部 API。同一日补充实证：**linked→linked 的纯路径变更 PATCH 可用**，且接受 `attachments:` 便携相对路径（3 个旧机器死链附件已用此形式修复并写后验证）。`zotero-relocate` 的写回范围据此限定为 linked_file 附件的路径更新。
2. imported-file → linked-file 转换后，原 storage 文件由 Zotero 自动清理，还是必须由调用方处理？
3. 通过当前 zotero-mcp 版本是否能获得附件路径写回能力；如果不能，临时 direct Local API 例外的精确授权边界是什么？
4. `metadata.yaml` 的受管写范围是否应继续由 `sources/zotero/` 这一单文件收窄，而不是开放整个 `sources/`？
5. group library 是否永远排除，还是允许用户为每个库配置独立的外部根目录？
6. 目标路径模板中 Collection 层级的展示名称如何处理同名 Collection、空层级和改名后的历史路径？
7. 清理旧源时，如何以稳定 attachment key 而不是文件名判断“没有其他引用”？

在这些问题有实证答案之前，文档中的实现路径均视为设计约束和验证计划，不视为已经存在的 API 能力。
