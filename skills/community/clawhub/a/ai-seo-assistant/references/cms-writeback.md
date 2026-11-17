# CMS / MCP 回写映射（通用）

当目标站为支持「写接口 / MCP」的 CMS，且已配置对应服务端点和凭证时，SEO 分析结果可回写到站点。本文件给出「分析建议 → 平台字段/操作」的通用映射；**具体字段名与方法以目标 CMS 的 MCP 工具参数为准（见 `references/mcp-tools.md`）**。

## 前置

- **先决条件**：仅当用户预期要执行修改时才索取凭证；纯体检分析不索取、不调用任何写工具（见 `SKILL.md` §1）。
- 索取并验证服务端点和凭证（如 MCP 完整地址 + Bearer Token）。未拿到前不调用任何工具；Token 仅由客户端放入 `Authorization: Bearer`，不回显、不落文件。
- 遵循所用 CMS 的「写操作确认基线」：任何回写前先展示目标 + 影响并取得用户确认。
- 若宿主封装因 schema 校验（如 `oneOf` / 类型强制）拦截写工具，按该 CMS 既定方式处理（例如直连后端 API 绕过宿主校验），并保留操作前快照便于回滚。

## 本 skill 限定的 MCP 工具

若目标 CMS 暴露本 skill 配套的 MCP 工具，TDK 读取与写回**只走以下工具**（参数与返回值详见 `references/mcp-tools.md`）：

| 用途 | 工具 | 读写 |
| --- | --- | --- |
| 列举页面、确认目标页 ID | `list_page` | 读 |
| 读取页面源码（离线分析用） | `get_page_info` | 读 |
| 读取整站 SEO 现状 | `get_site_seo` | 读 |
| 设置整站 SEO（title/keywords/description） | `edit_site_seo` | 写（部分更新） |
| 分页查询 产品/文章/分类/页面 的 SEO | `get_seo_list` | 读 |
| 设置指定 产品/文章/分类/页面 的 SEO | `edit_seo` | 写（整体覆盖 TDK） |
| 保存 SEO 批量生成规则 | `edit_seo_batch` | 写（批量模板） |
| 改写页面源码（仅 SEO 相关） | `save_ai_page` | 写（页面源码，受 SEO 约束） |

> 范围约束：本 skill 经 MCP **不调用任何上述之外的工具**（产品/文章/相册/表单/SQLite/批量导入等一律不在本 skill 范围内）。其中 `save_ai_page` 仅用于「SEO 相关的页面源码改写」，**严禁改动 `{{}}` / `{%%}` 数据标签及其上下文逻辑**；**仅修改 TDK 时必须优先 `edit_seo` / `edit_site_seo`，不得用 `save_ai_page` 只改标题/关键词/描述**。

## save_ai_page 使用约束（强制）

`save_ai_page` 用于「SEO 相关的页面源码改写」，是 B 级建议（`add_canonical`/`add_jsonld`/`add_viewport`/`add_lang`/`add_alt`/`expand_content`/`inject_keyword`/`add_internal_links`）的落地点。强制约束：

1. **只改 SEO 内容**：仅补/修 `<meta>`、canonical、JSON-LD、图片 `alt`、`viewport`/`lang` 等 SEO 相关片段；不得改写与 SEO 无关的业务逻辑或样式。
2. **不动数据标签**：严禁改动任何 `{{...}}` / `{%...%}`（含 `{{ }}`、`{%- %}`）数据标签及其上下文逻辑块（循环、条件、数据占位等）。改动前必须 diff，确认未触碰任何数据标签与平台绑定；不确定时先询问用户。
3. **TDK 优先 edit_seo**：若改动**只包含**标题/关键词/描述，禁止用 `save_ai_page`，必须走 `edit_seo` / `edit_site_seo`。
4. **基线 + 最小化**：先用 `get_page_info` 读出 `SourceCode` 作基线，`html` 必须回传**完整源码**，只做最小化 SEO 改动，不得丢失或重写任何既有内容。
5. **确认 + 回读**：写前展示目标 + 影响 + 差异摘要并取得确认；写后回读确认，保留修改前快照便于回滚。

## 字段映射（通用）

分析脚本（`seo_audit.py`）按 `fix.type` 输出建议。下表把每个 `fix.type` 映射到「本 skill 限定工具能否落地」，避免越界调用或假落地。

### A. 可由本 skill 工具直接落地的项

只有 TDK 三件套（标题 / 关键词 / 描述）能经 `edit_site_seo` / `edit_seo` 写回；真实参数名与 `mcp-tools.md` 一致，注意**不是** `seoTitle`/`seoDescription`/`seoKeywords`。**仅改 TDK 时禁止用 `save_ai_page`**（见上方 save_ai_page 约束）。

| `fix.type` | 落地点（工具 + 真实参数名） | 层级 | 关键约束 |
| --- | --- | --- | --- |
| `meta_title` | 整站：`edit_site_seo.title`；对象：`edit_seo.title` + `seoType`/`id` | 整站 / 对象 | 真实参数名是 `title`（非 `seoTitle`） |
| `meta_keywords`（关键词） | 整站：`edit_site_seo.keywords`；对象：`edit_seo.keywords` + `seoType`/`id` | 整站 / 对象 | 真实参数名是 `keywords`（非 `seoKeywords`）；无 SEO 许可时可能不写入，需先 `get_site_seo`/`get_seo_list` 核对 |
| `meta_description` | 整站：`edit_site_seo.description`；对象：`edit_seo.description` + `seoType`/`id` | 整站 / 对象 | 真实参数名是 `description`（非 `seoDescription`） |

> 说明（读/写字段名大小写不一致，易踩坑）：
> - 整站：`get_site_seo` **返回** `SeoTitle`/`SeoKeyword`/`SeoDescription`（大写 S 开头），但 `edit_site_seo` **接收**小写 `title`/`keywords`/`description`。
> - 对象级：`get_seo_list` **返回**大写 `Title`/`Keywords`/`Description`，但 `edit_seo` **接收**小写 `title`/`keywords`/`description`。
> 回写一律用**小写键名**。
> 当前 `seo_audit.py` 显式产出 `meta_title` 与 `meta_description`；关键词建议通常并入 TDK 写回时一并提供（三个字段在同一个写调用中提交）。

### B. 可经 `save_ai_page` 落地的项（受 SEO 约束 + 数据标签保护）

以下项需改动页面 HTML 源码，可由 `save_ai_page` 落地，但**必须**遵守上方「save_ai_page 使用约束」：① 先用 `get_page_info` 读 `SourceCode` 作基线；② 只做最小化 SEO 改动；③ 严禁改动 `{{}}` / `{%%}` 数据标签及其上下文逻辑；④ 写前展示差异+影响并取得确认，写后回读。

| `fix.type` | 需要的改动 | 落地方式 |
| --- | --- | --- |
| `add_canonical` | 注入 `<link rel=canonical>` | `save_ai_page` 补 `<head>` canonical；整站多由平台自动生成时确认即可 |
| `add_jsonld` | 在页面 `<body>` 末尾追加 JSON-LD `<script>` | `save_ai_page` 追加 JSON-LD（纯静态，不触碰数据标签） |
| `add_viewport` / `add_lang` | 补 `<head>` 元标签 | `save_ai_page` 补到 `<head>` |
| `add_alt` | 给 `<img>` 补 alt | `save_ai_page` 补 `alt`（注意不得改动 `src` 中的 `{{}}`/`{%%}` 变量） |
| `expand_content` | 扩充正文内容 | `save_ai_page` 增补正文（仅当正文为静态 HTML、不涉及数据标签循环时） |
| `inject_keyword` | 正文自然植入关键词 | `save_ai_page` 增补（同上，禁止改写数据标签内文案） |
| `add_internal_links` | 增加内链 | `save_ai_page` 增补静态内链（禁止改写由数据标签生成的链接） |

> 若 `expand_content` / `inject_keyword` / `add_internal_links` 涉及 `{{}}` / `{%%}` 生成的内容（如产品/文章列表循环），**不得**用 `save_ai_page` 改写，应转为人工处理或改用对应数据接口的 SEO 参数。

#### 落地时的 URL 拼接：获取当前域名与完整 URL

`add_canonical` / `add_jsonld` 等需要绝对地址的改动，域名部分**禁止写死**，用以下模板函数动态获取（源自平台 Twig 基础工具函数）：

| 需求 | 用法 | 返回示例 |
| --- | --- | --- |
| 当前网站域名（不含协议） | `{{ FnGetHost(0) }}` | `abc.com` |
| 当前网站域名（含协议） | `{{ FnGetHost(1) }}` | `http://abc.com` |
| 当前访问的完整 URL | `{{ FnGetCurrentUrl() }}` | 完整访问地址 |

- canonical / JSON-LD / `og:url` 中要求绝对地址的字段：用 `{{ FnGetHost(1) }}` 拼接站点前缀；需要当前页面完整地址时直接用 `{{ FnGetCurrentUrl() }}`。
- 本站内部链接**不要**用 `FnGetHost`，保持相对链接（或 `FnRewrite(...)` 生成的系统链接）。
- 这些 `{{ }}` 表达式是新增 SEO 内容，不触碰页面既有数据标签；写入仍须走 `save_ai_page` 使用约束。

### C. 仍需人工 / 超出 MCP 的项（收录开关与基础设施）

| `fix.type` | 需要的改动 | 为何本 skill 无法直接写 |
| --- | --- | --- |
| `remove_noindex` | 取消 noindex | 高风险，检查页面/栏目收录开关，超出本 skill 工具范围 |
| `enable_https` | 全站 HTTPS 跳转 | 服务器/证书层配置，非 MCP 写工具范围 |

### D. 批量规则（独立能力，非逐对象 TDK）

- `edit_seo_batch` 不是逐对象 TDK 写回，而是保存「产品 / 文章 SEO 批量生成规则模板」（如 `{{Name}} - {{SiteName}}`）。它适用于「用统一模板批量生成 TDK」的场景，与逐页 `edit_seo` 是两套不同机制；回写前需单独向用户说明启用状态、分隔符与变量对后续 SEO 的影响。

> 说明：旧版映射曾把上述 B/C 项写成「如 `seoTitle` / 详情页标题字段」「源码/模板原样回传」，与 `mcp-tools.md` 实际参数不一致，已修正为 A/B/C/D 分级，并开放 `save_ai_page` 落地 B 级（受 SEO 约束）。

## 低风险回写流程（TDK 三件套）

1. 读取现状：`get_site_seo`（整站）或 `get_seo_list`（对象），配合 `list_page` 确认目标 `id`。
2. 组装写参：
   - **整站**用 `edit_site_seo`（部分更新，可只传需改字段；未传字段保持原值）。
   - **对象级**用 `edit_seo`，**必须带 `seoType`**（`product`/`article`/`productClass`/`articleClass`/`page`）、`id`，且 `title`/`keywords`/`description` **三个字段都必填**（可传空串清空）—— 它是整体覆盖，不是部分更新。
3. 展示目标 + 原值 + 新值，取得确认后调用写工具。
4. 写工具成功后平台**会自动清缓存**；必要时再用读工具回读确认即可（无需额外调用清缓存工具）。

> 注意：本流程**不传页面源码**。`get_page_info` 只在「离线分析」阶段读取 `SourceCode` 用；TDK 写回走 `edit_site_seo`/`edit_seo`，二者不混用。

## 高风险回写

标题层级重构、内容重写、noindex 调整 —— 一律先按 `risk-classification.md` 请求确认。其中 `remove_noindex`/`enable_https` 属 C 级（超出本 skill 工具范围，需用户在源站后台处理）；A 级（TDK）与 B 级（`save_ai_page` 可落地的 SEO 源码改动）按确认基线执行即可。

## 离线分析（无写接口）

将页面源码存为本地 `.html`，用脚本单页分析：

```bash
python seo_audit.py page --url https://站点/路径 --file 页面.html --out 报告.json
```

据此生成建议（含 A/B/C/D 分级）；待用户提供写接口凭据后：A 级经 `edit_seo`/`edit_site_seo` 回写，B 级经 `save_ai_page` 回写（受 SEO 约束），C 级作为人工修改清单交付。
