# 稿件包与本地辅助脚本

## 最小输入与整理责任

用户只需提供资料、目标平台和本次任务。Agent 负责撰写完整文章，并从资料整理以下结构；不让用户先填审计表。可以不运行脚本直接交付文本。辅助脚本使用 Python 3.10+ 标准库，离线运行，不读取环境凭据、不联网、不调用模型、不投稿。

一个完整工作样例在 [examples/success](../examples/success/request.json)。交付目录以它为结构参考，内容按实际资料重新写；不要把演示产品规格带入真实品牌稿件。

## 文件与字段

| 文件 | 内容 |
| --- | --- |
| `request.json` | `schema_version: 1`、本次任务 `task`、`articles` 数组 |
| 各平台 `.md` | 平台元数据和完整正文，不是提纲 |
| `事实与来源清单.json` | `schema_version: 1`、`sources`、`facts`、`assets`、`platform_rules`、`geo_observations` |
| `发布交接清单.csv` | 脚本根据校验后的稿件和状态汇总，绝不代表已经投稿 |

所有输入引用路径相对交付目录，不允许绝对路径、`..` 或指向目录外的符号链接。外部资料可由 Agent 把本次授权使用的必要原文摘录放入来源字段，记录原始定位；不要复制凭据或整站内容。

### 当前写作授权

`articles` 每项包含 `file`、`platform`、`content_type`、`operation`。`content_type` 表示解释文、教程或笔记等本次交付类型，不能在发布交接时凭正文猜测类型。

`operation` 为 `new`、`preserve` 或 `edit`。后两者还须提供目录内的 `original` 原稿路径；原稿与输出均使用下述元数据格式。`preserve` 的标题和正文逐字保留，`allowed_changes` 留空。`edit` 需要 `allowed_changes`（仅 `title` 和/或 `body`）和当前用户的 `change_request`。例如只允许正文改动时，脚本禁止改标题；正文中具体段落的授权由 Agent 逐项审查，脚本不理解自然语言范围。

`title` 同时指元数据标题和文首可见一级标题；有文首 H1 时，两者文字必须一致。只授权 `title` 时同步修改这两处标题文字，正文其余字符、空白、换行和标题标记保持原样；未授权 `title` 时不能改动或增删文首 H1。文首 H1 仅识别跳过空行后出现的 ATX `# 标题` 或 Setext `标题` 加 `===`，正文中的后续标题、二级标题及代码块不作为文首标题移除。没有文首 H1 的原稿可以只改元数据标题，正文仍须逐字保留。

用户已有原稿若不是这种格式，先另存带元数据的副本，原标题和正文原样带入，用它作基线；不能覆盖用户原件。脚本不把资料文件里的“发布授权”视为用户当前授权。

### 稿件元数据

YAML frontmatter 使用**单行 JSON 值的 YAML 子集**，便于不安装 YAML 依赖也能校验。字符串加双引号，列表为 JSON 数组，不使用多行值、注释或 YAML 简写列表。正文可使用正常 Markdown。字段为：

- `platform`：平台标识，如 `zhihu`。
- `content_type`：如 `explainer`、`tutorial`、`note`。
- `title`、`topic`：本稿标题、主题。
- `fact_ids`：本稿实际使用的事实 ID 列表，没有事实断言可为空。
- `asset_ids`：本稿所需素材 ID 列表，不要求配图时为空。

### 来源、事实与落稿位置

`sources` 每项有唯一 `id` 和 `label`。本地来源使用 `kind: local_file` 和 `path`；粘贴文本/网页摘录使用 `kind: provided_excerpt`、非空 `text` 和 `locator`。`locator` 记录用户消息位置、文档章节或真实网页地址。可额外记录时点和核实范围；脚本不会自动访问 URL，也不能证明来源的权威性或时效性。

`facts` 每项有唯一 `id`、`canonical`、`source_id`、`source_quote` 与 `occurrences`。`canonical` 是需跨稿保持一致的事实片段，包含关键数字、单位或限制；它必须出现在 `source_quote` 中，且该原文出现在来源文件或摘录中。每个落稿位置包含 `article` 与 `quote`；`quote` 须包含该事实片段，并真实出现在正文中。`fact_ids` 与这些位置对应。可保留未用事实，其 `occurrences` 为空。

精确片段可很短，如“每批最多 200 行”，周围句子与文章结构自由组织。不要求逐句登记观点与建议；重点核对产品能力、数字和限制。自然改述不能保留原片段时，由 Agent 人工复核等价表述后决定是否使用辅助校验，不能为了通过脚本改坏原稿。

脚本只验证已登记片段，不能发现所有新增的未登记断言、否定关系、遗漏的单位或隐含矛盾。Agent 必须通读全文，不能用“通过校验”代替语义与来源判断。

### 素材与平台规则

`assets` 每项有 `id`、`brief`、`state`、`path`。`pending_creation` 对应 `path: null`；`available` 须引用目录内真实 PNG、JPEG 或 WebP 文件。脚本检查文件头，不证明图片可解码、画面正确或授权完备；Agent 应实际看图。素材需求记录用途和应出现的内容，不虚构已制作文件。

`platform_rules` 为每个目标平台一项：`platform`、`state`、`note`。`state` 可为 `pending_confirmation` 或 `confirmed`。确认时还须 `basis` 和 `checked_at`（YYYY-MM-DD），写明本轮确认了什么，不能以一个日期笼统代表所有平台规则都已核实。用户本次编辑要求可作为依据，不强制登录后台。

CSV 的 `handoff_status` 为“待素材及规则确认”“待素材”“待规则确认”或“可交接”。“可交接”只表示所声明素材齐备且本轮规则已确认，不是发布成功或 AI 已收录。没有请求图片时 `asset_status` 为 `not_requested`，与缺图不同。CSV 以 UTF-8 输出，包含平台、内容类型、标题、稿件路径、文字/素材/规则状态、来源 ID 和待办；遇到公式开头的字段会加单引号，防止表格软件执行公式，不改变稿件原文。

### 可选 GEO 采集记录

`geo_observations` 可为空数组；从未查询也可保存样例中的 `not_run` 项。脚本没有查询功能，只检查用户已提供的数据。

| 状态 | 回答与计数 |
| --- | --- |
| `not_run` | `answer`、`mention_count`、`native_citations` 均为 null |
| `query_failed` | 上述均为 null；`error` 记录具体失败 |
| `simulated` | `answer` 明确为模拟内容，计数与原生引用为 null，不进实际统计 |
| `observed` | 保存实际输入/采集的引擎、问题、带时区时间、原始回答、提及计数和原生引用列表 |

`observed` 还需 `evidence_source_id` 指向含原始回答和原生来源记录的来源、`brand_terms`（实际用于逐字匹配的品牌词）。脚本按最长词优先、大小写敏感、非重叠匹配核对 `mention_count`；这只是明确口径的文字计数，不推断推荐倾向。`native_citations` 为对象数组，每项 `kind: native`、`url`，URL 必须出现在同份原生引用证据里。只有确认来自引擎原生来源面板/引用字段时才录入，普通正文链接不算。

无成功采集样本时，汇总的提及数和原生引用数为 null；成功采集且确实没有结果时才为 0。模拟、未运行、失败分别计样本数，不进入实际计数或比率。脚本不能独立核实采集记录是否来自真实引擎，Agent 不能将测试夹具冒充实测。

## 命令与错误

在技能目录执行，交付目录路径可以替换：

```sh
python3 scripts/content_bundle.py check examples/success
python3 scripts/content_bundle.py handoff examples/success --output /tmp/qinghe-handoff.csv
python3 scripts/self_test.py
```

`check` 仅输出 JSON；`handoff` 先完成校验再写 CSV，失败不写输出。在交付目录内只允许写 `发布交接清单.csv`，不能覆盖稿件或来源；也可指定目录外自己的 CSV 输出路径。成功退出 0，校验/读写失败退出 2，参数错误由 argparse 返回 2。待制作、待确认状态作为警告返回，不妨碍文字交付完成。

常见错误：`FACT_MISMATCH` 落稿片段冲突，`FACT_SOURCE` 来源对不上，`TITLE_MISMATCH` 元数据与文首 H1 不一致，`PRESERVE_TITLE`/`PRESERVE_BODY` 超范围修改，`ASSET_FILE` 素材不存在或文件头不符，`GEO_UNKNOWN_COUNT` 将未知状态写成数字，`PATH` 引用了目录外路径。失败后只修相关问题，不重写所有文章。
