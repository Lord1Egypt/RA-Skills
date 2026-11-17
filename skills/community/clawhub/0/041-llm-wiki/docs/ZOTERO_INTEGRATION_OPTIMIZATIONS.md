# Zotero 集成与附件管理优化方案

> 基于 Zotero 原生扩展 **ZotMoov** 的工程实践，为 `llm-wiki` 的文献层（Literature Layer）交互体系提供架构升级与健壮性优化指南。

---

## 1. 方案背景与定位

在 `llm-wiki` 架构中：
- **Zotero** 是文献底座（Literature Layer），负责文献元数据、原始附件、PDF 批注、分类目录（Collections）与引用键（Citation Keys）；
- **llm-wiki** 是蒸馏知识库（Distilled Markdown Knowledge Layer），负责概念提炼、跨源综合、双向链接与索引构建。

原生 Zotero 插件 **ZotMoov** 在长期的 Zotero 7/8 环境运行中，积累了处理底层文件系统兼容性、附件多模态、跨端同步竞态及引用链接自愈等方面的成熟设计模式。本文档梳理并提取这些优秀设计，作为 `llm-wiki` 后续在 Zotero 附件抽取、本地 API 写回与元数据维护等模块的优化依据。

---

## 2. 核心优化方案

### 方案一：跨平台文件名清洗与超长路径安全截断 (Sanitization & Path Guard)

#### 现有痛点
- 学术论文标题常包含特殊字符（如冒号 `:`、斜杠 `/`、反斜杠 `\`、问号 `?`、重音/变音符等），且长度常超过 150~200 字符。
- 在 Windows 环境下存在 **260 字符最大路径限制**（`MAX_PATH`），Linux/macOS 文件名存在 **255 字节限制**。
- `llm-wiki` 在生成 `wiki/<stem>.md` 页面名或 `sources/zotero/` 别名时，极易因超长路径或非法字符在跨平台同步时遭遇 IO 异常。

#### ZotMoov 的设计借鉴
- **智能标点与分词截断**（`src/00-zotmoov-wildcard.js` `_truncateTitle`）：
  - 遇到首个 `: . ? !` 标点时优先截断为副标题前的内容（默认最大长度 200 字符）；
  - 达到最大长度时，向前回溯至最近的单词边界（空格），避免截断单个单词。
- **跨平台非法字符清洗**（`lib/02-sanitize-filename.js`，派生自 node-sanitize-filename）：
  - 清洗斜杠、问号、尖括号、反斜杠、冒号、星号、引号等非法字符与控制字符，处理全点号名称、Windows 保留名（`CON/PRN/AUX/NUL/COM0-9/LPT0-9`）及尾部点号/空格；
  - 按 UTF-8 **字节**截断至 255 字节上限，截断处剥离 `�` 残片以保证多字节字符不被切半。
- **字节级安全截断与后缀保护**（`lib/01-zotlib.js` `createShortened`）：
  - 以 `Zotero.Utilities.Internal.byteLength` 精确计算 UTF-8 字节长度，保留文件扩展名，并预留 3 字节缓冲给唯一性冲突序号（如 ` 1.pdf`）；
  - 针对 eCryptfs（143 字节）等特殊文件系统自动收紧上限——**路径长度与文件名长度是两类不同约束**（Windows 260 字符路径 vs ext4/HFS+ 255 字节文件名）。
- **音标/变音符号清理**（`src/02-zotmoov.js`，由 `strip_diacritics` 偏好开关控制）：
  - 调用 Zotero 内置 `Zotero.Utilities.removeDiacritics` 去除变音符，确保 ASCII 兼容性。

#### `llm-wiki` 落地设计
在 `src/llm_wiki/` 中增加文件路径规范化工具（`sanitizer.py`）：
```python
def sanitize_title_stem(title: str, max_bytes: int = 120) -> str:
    """清理非法字符、去除音标、并在词边界安全截断以适配跨平台文件名"""
    ...
```

现状接入点（已核对）：wiki 页面命名在 `src/llm_wiki/core.py` `create_page()`，目前仅 `title.replace(' ','-').replace('/','-')`，无长度截断与非法字符清洗，长 CJK 标题会在写盘时触发 `OSError: File name too long`；`sources/zotero/` 别名由 `scripts/zotero_sources.py` 从 `metadata.yaml` 原样消费，仅做路径 confinement 校验。新工具应同时覆盖这两处，Python 侧可用 `unicodedata.normalize('NFKD')` 复刻去音标、以 `encode()[:n].decode('utf-8', 'ignore')` 复刻多字节安全的字节截断。

> **兼容性原则**：清洗规则只约束**新增**页面与别名；既有 wiki 页面名与别名是 `[[链接]]`、frontmatter `sources[]`、`metadata.yaml.source_alias` 的共同锚点，不随本方案重命名（详见文末"兼容性与迁移原则"）。

---

### 方案二：附件双模态解析与 Symlink 降级容错机制 (Attachment Dual-Mode & Fallback)

#### 现有痛点
- `scripts/zotero_sources.py` 强依赖于操作系统级符号链接（Symlink）创建 `sources/zotero/` 别名。
- **Windows 权限限制**：普通权限的 Windows 用户（未开开发者模式）无法创建 Symlink，导致脚本直接报错中断。
- **外部链接文件（Linked File）**：当用户使用了 ZotMoov 或 ZotFile 将附件存放在外部网盘（非 Zotero 内部 `storage/` 目录）时，单纯依赖默认 storage 路径无法正确解析文件。

#### ZotMoov 的设计借鉴
- **显式区分 Stored vs. Linked 模态**（`src/02-zotmoov.js`）：
  - 通过 `attachmentLinkMode` 区分存储附件与链接附件，使用 Zotero 官方 API `item.getFilePath()` 解析真实的绝对路径，不假设附件必然存在于 `storage/`。
- **降级容错机制**：如果无法建立软映射，提供只读复制或纯元数据映射。

#### `llm-wiki` 落地设计
修改 `scripts/zotero_sources.py`：
1. **真实物理路径检测**：支持通过 MCP 或 local API 提取 `item.getFilePath()` 等价信息，无论附件是 Stored 还是 Linked 均能定位真实物理文件。前置验证：zotero-mcp 是否暴露 Linked 附件真实路径需先实测确认；若 MCP 不暴露，可经由 Zotero local API（loopback）获取。
2. **Symlink 异常降级策略**（按优先级排序）：
   - 尝试创建 Symlink；
   - 若捕获 `OSError`（如 Windows 权限不足），按以下顺序降级：
     - **选项 C（首选）**：仅在 `metadata.yaml` 记录绝对路径映射，Agent 读取时直接路由到源路径，不强求本地实体别名文件——与现有 `local_path` 字段天然兼容，不引入数据漂移；
     - **选项 B**：降级为 Read-only Copy（只读副本）——副本会与源文件产生双份漂移，仅在下游工具必须见到实体文件时使用；
     - **选项 A**：降级为 Hardlink（硬链接）——同一分区下无需管理员权限，但跨设备（如网盘场景）必然失败，适用面最窄。
   - 现状（已核对）：`zotero_sources.py` 对 `symlink_to` 无任何异常捕获，单次失败会中断整个批次并丢失已完成计数；降级实现应同时补上逐条容错。

---

### 方案三：Zotero 条目死链自愈与关联重映射 (Link Healing & Reconciliation)

#### 现有痛点
- `llm-wiki` 在 Wiki 页面 Frontmatter 中记录了 `zotero_item_key`。
- 科研工作流中，用户常在 Zotero 中执行“条目合并（Merge Items）”、“重新从 DOI 导入条目并删除旧项”或“转换附件”。此时 Wiki 页面中记录的旧 `item_key` 将悬空失效，导致后续 `zotero-refresh` 或写回操作失败。

#### ZotMoov 的设计借鉴
- **笔记引用自愈**（`src/02-zotmoov-menu-helper.js` `fixNoteLinks`，**手动菜单命令**）：
  - 遍历 Zotero 笔记中的引用 URI，通过 `Zotero.Items.getIDFromLibraryAndKey` 检测引用的旧条目是否已从数据库删除；
  - 若已删除，以当前有效附件条目（`item.getBestAttachment()`）作为替换目标，调用 `Zotero.Notes.replaceItemKey` 修复；
  - 附件移动（move）过程中的自动修复发生在 `src/02-zotmoov.js` 的事务块内部，与手动自愈是两条独立路径。
- **对 llm-wiki 的启示是"探测失效 → 二次寻址 → 原地修复"的三段式结构**；下文的多维寻址链（DOI → citation_key → 标题）是 llm-wiki 基于自身 frontmatter 元数据的设计，ZotMoov 并未提供等价实现。

#### `llm-wiki` 落地设计
前置修复（独立于自愈管道的健壮性缺口，已核对）：`src/llm_wiki/zotero_mcp_client.py` 的 `get_items` 使用无 `return_exceptions` 的 `asyncio.gather`，**单个失效 key 会使整个 refresh 批次崩溃**；应先改为逐条容错，将失效条目降级为"待修复"记录。

在此基础上，于 `src/llm_wiki/zotero_ingest_verify.py` 和 `zotero_refresh.py` 中引入**条目自愈管道**：
1. **失效 Key 探测**：当 `zotero_get_item_metadata` 返回 404/not found 时，标记为待修复悬空条目。
2. **多维二次寻址**：
   - 优先通过 Wiki Frontmatter 中的 `doi` 查询 Zotero 库匹配有效条目；
   - 次优通过 `citation_key` 或标准化标题（Title matching）匹配有效条目（`zotero_plan.py` 已读取 `citation_key` 与规范化标题，数据基础现成）；
3. **自动迁移修复**：在用户确认或 `--apply-safe` 模式下，自动更新受影响 Wiki 文件的 `zotero_item_key`，并在 `log.md` 记录自愈日志。该修复为 frontmatter 字段原地更新，不涉及文件重命名，无迁移面。

---

### 方案四：双向关系原子性与同步状态隔离防护 (Transactional Relations & Sync Guard)

#### 现有痛点
- `llm-wiki` 在 `src/llm_wiki/zotero_local.py` 中支持互关写入（`dc:relation`）。
- 若在执行双向关联时，Source 条目写入成功而 Target 条目写入失败（或遇网络/版本冲突），会在 Zotero 中留下单向不对称的残缺关联。
- 大规模写回时若恰逢 Zotero 后台云端同步，容易产生版本冲突（HTTP 412）。

#### ZotMoov 的设计借鉴
- **同步挂起协调**（`src/01-zotmoov-notify-callback.js`）：
  - 在大批量写入期间，通知同步器推迟后台同步（`Zotero.Sync.Runner.delayIndefinite()`），并在同步进行中时跳过执行，全部原子写入完成后再恢复同步。
- **事务与失败清理**（`src/02-zotmoov.js` `move()`）：
  - 核心写操作置于 `Zotero.DB.executeTransaction` 内，异常时数据库自动回滚，并由外层 catch 清理已复制的临时文件，不留孤儿文件。

#### `llm-wiki` 落地设计
前提说明（已核对）：`delayIndefinite()` 是 Zotero **插件进程内 API**，llm-wiki 作为外部客户端无等价物；`docs/ZOTERO_MCP_INTEGRATION.md` 中定义的 `metadata_sync_state` 是"权威端与写入端一致性"的状态分类（`disabled/pending/caught_up/divergent/unknown`），并非"同步进行中"的实时探针，目前也没有任何代码填充或消费它。因此本方案的落地重心放在客户端可达成的机制上：

1. **两阶段关系写入与补偿机制**：
   - 在 `zotero_local.py` 中写入 `RelationWriteResult` 时，如果第二阶段失败，自动向第一阶段的 Source 条目触发补偿回滚，移除刚刚新增的关联 URI，确保双向关联的原子一致性。
   - 现状（已核对）：`zotero_local.py` 已有版本守卫（`If-Unmodified-Since-Version`）、单次 HTTP 412 重试与 GET-after-PATCH 验证；`ensure_relation_pair` 本身幂等（已存在的关联会跳过），单向残留可靠重跑自愈。补偿回滚属整洁性增强，优先级见路线图。
2. **冲突退避强化（替代同步探针）**：
   - 在现有单次 412 重试基础上加强为有界指数退避重试；`metadata_sync_state` 仅作为计划/审计输出中的只读状态呈现，不作为写入门禁。

---

### 方案五：基于通配符与层级目录的元数据模板引擎 (Wildcard Template Engine)

#### 现有痛点
- 目前从 Zotero 导入条目到 `llm-wiki` 时，文件命名与目录结构规则较为单一，缺乏对 Zotero 分类树（Collection Hierarchy）和自定义命名格式的灵活支持。

#### ZotMoov 的设计借鉴
- **多层级分类路径解析**（`src/00-zotmoov-wildcard.js`）：
  - 递归遍历父 Collection，生成标准层级路径（如 `Machine Learning/LLM/Reasoning`）。
- **统一通配符体系**：
  - `%a` (主作者)、`%y` (年份)、`%t` (截断标题)、`%c` (分类路径)、`%b` (CiteKey)、`%T` (条目类型)。

#### `llm-wiki` 落地设计
在 `config.yaml` 中允许用户自定义 Zotero 导入及 Wiki 页面命名的模板规则：
```yaml
zotero_import:
  page_template_pattern: "%c/%y-%a-%t"
  alias_pattern: "%b"
```

> **范围警示**：`%c/%y-%a-%t` 是文献管理式命名，而 wiki 页面名是 `[[链接]]` 体系的知识锚点，两者约束不同。建议本方案缩小为仅覆盖 `sources/zotero/` 别名与导入目录结构（`alias_pattern`），wiki 页面命名模板待真实需求出现后再做；任何模板输出都必须先经方案一的 `sanitize_title_stem` 清洗。

---

### 方案六：附件受控搬迁与定位一致性 (Controlled Attachment Relocation)

#### 现有痛点
- `sources/zotero/metadata.yaml` 的 `local_path` 是**收录时点的路径快照**，不是 Zotero 附件位置的权威来源。
- 用户随后用 ZotMoov 重组附件目录，或在 Zotero 中转换附件后，`local_path` 与其 alias/symlink 可能悬空：`zotero_sources.py` 报 missing source，Agent 读源失败，且目前没有机制在保持 provenance 的同时完成修复。
- 仅修复 metadata 或 symlink 不能解决 Zotero 侧定位不一致；仅修改 Zotero 路径又会让 llm-wiki 本地来源层继续指向旧位置。

#### 设计纠正：llm-wiki 负责搬迁编排
ZotMoov 的附件重组是其本体功能，而不是 llm-wiki 只能借用的外围模式。llm-wiki 将通过独立、显式授权的 `zotero-relocate` 能力承担受控搬迁：

- 以配置的附件根目录和 Collection/作者/年份/标题等白名单字段生成目标布局；
- 先通过 MCP 或经过授权的本地能力解析 Zotero 当前真实路径，不信任旧 `local_path`；
- 采用 copy → verify → Zotero repoint → verify → metadata/alias 更新 → 可选清理的有序状态机；
- 通过原 attachment item key 的路径写回优先保持父项、子项、批注和关系；无法验证时拒绝 clone-and-repoint，不制造可能丢失笔记引用的替代条目；
- 对目标路径、旧源删除、配置根目录和 metadata 文件执行独立能力契约与 containment 校验。

ZotMoov 在 Zotero 插件内部还能迁移子项、批注、关系、full-text 索引并重写笔记引用；llm-wiki 不拥有这些内部 API，也不修改笔记正文。因此“负责搬迁”不等于假设外部 API 具备 ZotMoov 的全部能力。详细设计、Phase 0 API 门槛和失败恢复策略见 [Zotero 附件受控搬迁设计](ZOTERO_ATTACHMENT_RELOCATION.md)。

#### 实施入口与边界
1. **Phase 0 验证**：在隔离测试库确认现有 attachment item 的 `linkMode` / `path` 写回、item key 保持、子项/批注完整性及写后重读能力；未通过前只提供 dry-run/audit。
2. **受控搬迁**：新增独立命令和能力契约，默认关闭；目标路径永不覆盖既有文件，模板字段先清洗并按字节安全截断。
3. **本地层同步**：Zotero 写回成功后才更新 `metadata.yaml.local_path`，再幂等重建 alias/symlink；source alias 作为既有 wiki provenance 锚点默认不改名。
4. **恢复与清理**：跨 Zotero、文件系统和 YAML 不宣称真正原子事务；以可恢复状态机记录半完成状态。旧源删除必须显式启用、位于允许根目录且通过逐项引用检查。
5. **同步警示**：stored → linked 可能改变 Zotero File Sync 行为；Web-only、无法解析本地路径、已发生本地/Web 分叉和 group library 默认阻断，而不是静默降级。

---

## 3. 实施优先级路线图

| 阶段 | 优先级 | 优化内容 | 涉及模块 |
| :--- | :---: | :--- | :--- |
| **Phase 1** | **P0** | **路径清洗截断工具**：引入字节级文件名截断与非法字符清洗（前向兼容，仅约束新增命名） | `src/llm_wiki/sanitizer.py`, `core.py`, `scripts/zotero_sources.py` |
| **Phase 1** | **P0** | **Symlink 降级与 Linked File 支持**：按 C（metadata-only）→ B（只读副本）→ A（hardlink）顺序降级，并补逐条容错 | `scripts/zotero_sources.py`, `docs/FILE_HANDLING.md` |
| **Phase 1** | **P0** | **refresh 逐条容错**：`get_items` 改 `return_exceptions`，失效条目降级为待修复记录（自愈前置） | `src/llm_wiki/zotero_mcp_client.py`, `zotero_refresh.py` |
| **Phase 2** | **P1** | **条目死链自愈机制**：支持条目合并/变更时的自动 DOI/CiteKey 重映射 | `src/llm_wiki/zotero_refresh.py`, `zotero_ingest_verify.py` |
| **Phase 3** | **P2** | **冲突退避强化 + 双向关系补偿**：有界指数退避；`dc:relation` 失败补偿回滚（幂等重跑已可自愈，属整洁性增强） | `src/llm_wiki/zotero_local.py` |
| **暂缓** | **P2** | **别名级通配符模板**：仅 `alias_pattern`；wiki 页面命名模板暂缓 | `scripts/zotero_sources.py`, `config.yaml` |
| **Phase 0** | **P0** | **附件搬迁能力验证**：隔离测试库验证 attachment `linkMode` / `path` 写回、item key/子项/批注保持和写后重读；未通过前仅 dry-run/audit | `docs/ZOTERO_ATTACHMENT_RELOCATION.md`, `src/llm_wiki/zotero_attachment_adapter.py` |
| **Phase 1** | **P1** | **受控附件搬迁核心**：模板字段白名单、字节级清洗、目标 containment、冲突避让与 copy-verify-repoint-verify 状态机 | `src/llm_wiki/zotero_relocate.py`, `src/llm_wiki/capabilities.py` |
| **Phase 2** | **P1** | **Zotero 与本地来源层一致性**：原子更新 `metadata.yaml.local_path`、alias 修复、半完成状态 reconcile | `src/llm_wiki/zotero_relocate.py`, `scripts/zotero_sources.py` |
| **Phase 3** | **P2** | **附件路径漂移审计与受控清理**：权威路径重解析、旧源引用检查和显式允许根目录下的 cleanup-pending 恢复 | `src/llm_wiki/zotero_relocate.py`, `zotero_ingest_verify.py` |
| **Phase 3** | **P2** | **主题标签投影**：将 wiki 页面 `tags:` 映射为共享 `llm-wiki:<topic>` 托管标签（绑定标签只负责溯源，不负责主题聚类——2026-08-28 实测暴露） | `src/llm_wiki/zotero_plan.py` |

---

## 4. 兼容性与迁移原则

本方案各优化均为**前向兼容**设计，既有产出物默认零迁移：

1. **命名规则只约束新增**：既有 wiki 页面名与 `sources/zotero/` 别名是 `[[链接]]`、frontmatter `sources[]` / `sources_meta[].source_alias`、`metadata.yaml.source_alias` 三处的共同锚点。`sanitize` 接入后不改名既有文件；如确需规范化，应作为独立工具一次性同步三处引用并重建符号链接，而非默认行为。
2. **标识符保持稳定**：`zotero_item_key`、`llm-wiki:` 标签前缀、`metadata.yaml` / snapshot / allocation / write-plan 的 `version: 1` schema 均为兼容契约，变更须走版本升级并保留旧版读取。
3. **已知耦合风险**：`llm-wiki:<page_stem>` 标签把 wiki 页面名嵌入了 Zotero 标签——未来若重命名页面，对应标签将失配。长期应将关联主键固化为 `zotero_item_key`，标签仅作人类可读标记；页面重命名时需由 `zotero-writeback` 同步换标签。
4. **能力契约门禁**：现有命令无一拥有 `sources/` 写权限；任何实体化/改名类新命令必须先在 `src/llm_wiki/capabilities.py` 声明 write_scope（机制上只能收窄、不能放宽）。

---

*核对说明：本方案于 2026-08-28 对照 ZotMoov 源码（`src/00-zotmoov-wildcard.js`、`lib/01-zotlib.js`、`lib/02-sanitize-filename.js`、`src/02-zotmoov.js`、`src/02-zotmoov-menu-helper.js`、`src/01-zotmoov-notify-callback.js`）与 llm-wiki 现状（`core.py` `create_page`、`zotero_sources.py`、`zotero_mcp_client.py` `get_items`、`zotero_local.py`、`zotero_plan.py`）逐条核对修订。*
