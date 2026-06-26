# PDF / 双语 Markdown 包 → 乐享归档（归档侧）

> 🔀 **能力拆分（2026-06-24）**：PDF 的「图文提取 + 富元素识别 + 中英对照翻译 + 可移植排版」已抽离为独立 skill **`pdf-rich-translate`**（项目 `.cursor/skills/`）。
> **本文件只负责乐享归档侧**：把（pdf-rich-translate 产出的）可移植双语 markdown 包导入乐享、上传图片、把标注渲染成乐享专有块、转存后增量修正、归档侧对账。
> 提取/裁剪/翻译/清洗/标题层级等做法，**一律以 `pdf-rich-translate` 为准**，本文件不再重复。

## 组合流程总览

```
pdf-rich-translate（独立 skill）                 本 skill（fetch-archive-to-lexiang）
─────────────────────────────────              ──────────────────────────────────
PDF → 提取/裁剪/翻译/富元素标注          ──包──▶  导入乐享 + 三步传图 + 标注渲染成专有块
产出: <title>.md + images/ + 标注                + 转存后增量改块 + md↔线上对账
```

## Step 1 — 乐享内 PDF：取原文喂给 pdf-rich-translate

PDF 若存放在乐享条目内（`lexiangla.com/pages/xxx`），用桥接脚本一条命令拿到完整解析 + 原 PDF + 转存目标目录：

```bash
python3 scripts/lexiang_pdf_parse.py <entry_id> --download-pdf --out-dir <项目子目录>
```

产出 `parsed_raw.md`（解析原文）、`images.json`、`meta.json`（含 `parent_id` = 转存回的同目录）、`paper.pdf`。

> ✅ `entry_describe_ai_parse_content` 是读乐享内 PDF 原文的正确方式（实测返回 149K+ 字符，无 80K 限制）。
> ⚠️ 解析返回的 `/assets/xxx` 图片链接需浏览器 JWT 会话，**MCP token 下载会 401**——图片须从 `paper.pdf` 用 pymupdf 提取（由 `pdf-rich-translate` 负责）。

把 `paper.pdf`（及可选的 `parsed_raw.md`）交给 **`pdf-rich-translate`** 完成提取/翻译/排版，得到双语 markdown 包，再回到 Step 2 归档。**转存目标用 `meta.parent_id`（原 PDF 同目录），不新建日期目录。**

## Step 2 — 导入双语 markdown 包到乐享

```bash
# 有 LEXIANG_TOKEN（首选，一步到位，自动处理 ![](images/..)）
python3 scripts/md_to_page.py <双语.md> --parent-id <meta.parent_id 或日期目录ID> --name "<标题> 中英对照"
```

无 LEXIANG_TOKEN 时自动降级到 **MCP Direct HTTP Call**（见 SKILL.md「MCP 直接调用方法」/ [lexiang-upload.md](lexiang-upload.md)）。图片三步上传与位置定位同 SKILL.md Step 3，不再赘述。

## Step 3 — 把 pdf-rich-translate 的标注渲染成乐享专有块

`pdf-rich-translate` 用**可移植标注**表达富元素；归档时映射成乐享原生块：

| 标注（包内 markdown） | 乐享块 | 渲染要点 |
|---|---|---|
| `> [!stat] **N**` + EN + CN | `callout`（📊） | 容器块，内容放 `children` 子 p 块 |
| `> [!definition] **term**` + EN + CN | `callout`（📖） | 同上，图标区分 |
| HTML/markdown 表格 | 原生 `table` 块 | 用 `block_convert_content_to_blocks` 转 |
| `![](images/..)` | `image` 块 | 三步上传（见 SKILL Step 3） |

> markdown 无 callout 语法：`entry_import_content` 全量导入时这些标注会退化成 `> quote` 块。要得到真正的 callout，需在导入后用块工具**单独建 callout**（见下）。

> 🖼️ **image 块 caption 规范**：图注英中写在**同一行**（` / ` 分隔，如 `Figure 1: xxx / 图1：xxx`），不要另起独立段落当图注（会多出空行）。`block_update_block` **不能改 image 的 caption / session_id**——写错只能 `block_delete_block` 删除后用已有 `file_id` 重建（无需重新上传）。

**① callout 块（统计卡 / 定义卡）** —— `block_create_block_descendant`：

```python
descendant = [
  {"block_id":"c","block_type":"callout","callout":{"icon":"📊"},"children":["n","e","z"]},
  {"block_id":"n","block_type":"p","text":{"elements":[{"text_run":{"content":"73%","text_style":{"bold":True}}}]}},
  {"block_id":"e","block_type":"p","text":{"elements":[{"text_run":{"content":"<English line>"}}]}},
  {"block_id":"z","block_type":"p","text":{"elements":[{"text_run":{"content":"<中文行>"}}]}},
]
# children=["c"], index="<目标子索引>"；定义卡片把 icon 换成 📖、首行放加粗术语
```

**② 原生表格块（多列信息图 / 样式化对照表）** —— 先转后插：

1. 把内容写成 **markdown 表格**（中英同格，英文 `**加粗**` + 中文常规）。
2. `block_convert_content_to_blocks(content_type="markdown", content=<表格md>)` → 直接返回完整 `table`+`table_cell`+`p` 的 descendant（含 `row_size/column_size/header_row`），比手搓嵌套 JSON 可靠。
3. 把该 descendant 喂给 `block_create_block_descendant` 落库。
4. 样式化对照表还要**保留原图**：在表格上方插一张 `![原图](images/..)`（原图由 pdf-rich-translate 裁好）。

> 乐享 `entry_import_content` 的 markdown / html 两种 content_type 都会把内嵌 `<table>` 透传渲染成表格块（`rowspan`/`colspan` 生效）。简单表格直接嵌 HTML 表即可；复杂/需可编辑时走上面的转换法。

## Step 4 — 转存后的局部修正：用块工具增量更新（别重刷全文）

文档已上传后，若只需修个别问题（某标题层级、某段误成标题、某处换 callout/表格），**禁止重跑 `md_to_page.py` 全量覆盖**（重传几十上百块、极费 token）。用块级 MCP 工具精准改：

1. `block_list_block_children`（`_mcp_fields:"-staffs"` 减负）拉当前块，按返回顺序即文档顺序，定位目标块 `block_id` 与子索引。
2. 新建：`block_create_block_descendant`（`index` 是子块位置字符串；容器块内容放 `children`+`descendant`）。
3. 删除：`block_delete_block` / 批量 `block_delete_block_children(ids=[...], parent_block_id=根块)`（按 id 删，与位置无关，最稳）。
4. 改文本：`block_update_block` / 批量 `block_update_blocks`（`update_text_elements` 逐元素重建，**保留 `text_style`**）。
5. **乐享不能改块类型**（h2↔h3、p↔callout）：需删旧块 + 在原 index 重建为目标类型。
6. **多处编辑从文档后往前做**：删除按 id（不位移）、插入按 index（靠后先做，靠前块子索引不被位移影响）。
7. 改完同步本地 `.md`（callout 在 md 里用 `> [!stat]`/`> [!definition]` 标注表示，与 pdf-rich-translate 包格式一致）。

## Step 5 — 归档侧对账（三方对账的下半段）

`pdf-rich-translate` 已做 `PDF 图表数 == 本地 ![ 引用数` 两方对账；归档后再补一道：

- **`本地 md 的 ![ 引用数 == 线上 image block 数`**（`block_list_block_children` 统计 `block_type=="image"` 且有 `file_id`），凑成完整三方对账。
- 标注块核对：每个 `> [!stat]`/`> [!definition]` 都已渲染成 callout；每张样式化表都「原图 + 原生表格块」并存。
- 不相等就逐项定位补修（用 Step 4 增量手法）。

> 详细图片验证步骤见 SKILL.md Step 4「图片验证方法」。
