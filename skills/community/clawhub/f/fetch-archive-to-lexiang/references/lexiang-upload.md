### Step 2：原文保存到乐享知识库

**在进入信息图生成流程之前，先将原文完整保存到乐享知识库**，确保素材归档和可追溯。

#### 配置文件与初始化

本 skill 的目标知识库等信息通过配置文件管理，**不在 SKILL.md 中硬编码**。

配置文件路径：**`config.json`**（位于 skill 根目录，即与本 SKILL.md 同级）

##### 对话式配置初始化（首次使用时自动触发）

当 `config.json` 中 `_initialized` 为 `false` 或 `space_id` 为空时，**在执行任何乐享操作前**，必须先通过对话引导用户完成配置。

**核心设计**：用户只需要粘贴一个乐享知识库链接，Agent 自动完成所有配置。

**链接格式**：`https://<domain>/spaces/<space_id>?company_from=<company_from>`
- 示例：`https://lexiangla.com/spaces/b6013f6492894a29abbd89d5f2e636c6?company_from=e6c565d6d16811efac17768586f8a025`
- 从链接中可解析出三个关键信息：**域名**（`lexiangla.com`）、**space_id**、**company_from**

---

**流程如下**：

**第一步：检测 MCP 连接**
1. 尝试调用任意一个 lexiang MCP 工具（如 `whoami`）检测 MCP 是否已连接
2. 如果调用成功 → MCP 已连接，进入第二步
3. 如果调用失败（MCP 未连接）→ 引导用户完成 MCP 鉴权：
   ```
   ⚠️ 乐享 MCP 尚未连接。请先完成鉴权配置：

   1. 访问 https://lexiangla.com/mcp 登录后获取 COMPANY_FROM 和 LEXIANG_TOKEN
   2. 按照你使用的 Agent 配置 MCP 连接：
      - CodeBuddy：在 MCP 管理面板中添加 lexiang server
      - OpenClaw：运行 claw install https://github.com/tencent-lexiang/lexiang-mcp-skill
      - 其他 Agent：在 MCP 配置文件中添加 lexiang server
   3. 完成后告诉我，我会继续配置流程。
   ```
   **不要继续后续步骤**，等待用户完成 MCP 连接后重试。

**第二步：请求用户提供知识库链接**
1. 向用户发送引导消息：
   ```
   🔧 首次使用，需要配置目标知识库。

   请粘贴你想用来归档文章的乐享知识库链接，格式如：
   https://lexiangla.com/spaces/xxxxx?company_from=yyyyy

   💡 获取方式：在乐享中打开目标知识库，复制浏览器地址栏中的链接即可。
   ```
2. **等待用户输入**，不要自行猜测或列举知识库

**第三步：解析链接并验证**
1. 从用户提供的链接中用正则解析出三个字段：
   - **domain**：链接的域名部分（如 `lexiangla.com`），用于生成后续访问链接
   - **space_id**：`/spaces/` 后面的路径段（如 `b6013f6492894a29abbd89d5f2e636c6`）
   - **company_from**：`company_from=` 参数值（如 `e6c565d6d16811efac17768586f8a025`）
2. 如果链接格式不正确（缺少 `space_id` 或 `company_from`）→ 提示用户重新粘贴正确的链接
3. 调用 `space_describe_space`（参数：`space_id=<解析出的 space_id>`）验证知识库是否存在
4. 如果验证失败 → 提示用户检查链接是否正确或是否有该知识库的访问权限

**第四步：写入配置并确认**
1. 将解析和验证得到的信息写入 `config.json`：
   - `lexiang.target_space.space_id` = 解析出的 space_id
   - `lexiang.target_space.space_name` = 从 `space_describe_space` 返回值获取的知识库名称
   - `lexiang.target_space.company_from` = 解析出的 company_from
   - `lexiang.access_domain.domain` = 解析出的域名
   - `lexiang.access_domain.page_url_template` = `https://<domain>/pages/{entry_id}?company_from={company_from}`
   - `lexiang.access_domain.space_url_template` = `https://<domain>/spaces/{space_id}?company_from={company_from}`
   - `_initialized` = `true`
2. 向用户确认配置结果：
   ```
   ✅ 配置完成！

   📚 目标知识库：<知识库名称>
   🔗 访问链接：https://<domain>/spaces/<space_id>?company_from=<company_from>

   后续抓取的文章将自动归档到此知识库。如需更换，告诉我「重新配置知识库」即可。
   ```

##### 重新配置

当用户说「重新配置知识库」、「切换知识库」、「更换目标知识库」等类似意图时：
1. 将 `config.json` 中 `_initialized` 设为 `false`
2. 重新执行上述对话式初始化流程（从第一步开始）

##### 用户输入容错

用户可能不会粘贴完美的链接，需要处理以下情况：

| 用户输入 | 处理方式 |
|---------|---------|
| 完整链接 `https://lexiangla.com/spaces/xxx?company_from=yyy` | 直接解析 ✅ |
| 不带 company_from 的链接 `https://lexiangla.com/spaces/xxx` | 提示：「链接中缺少 company_from 参数。请在乐享中重新复制完整链接（地址栏中通常会包含 ?company_from=xxx），或者访问 https://lexiangla.com/mcp 获取你的 COMPANY_FROM 值告诉我。」|
| 纯 space_id `b6013f6492894a29abbd89d5f2e636c6` | 提示：「请提供完整的知识库链接（包含 company_from 参数），我需要从链接中同时获取知识库 ID 和企业标识。」|
| 页面链接 `https://lexiangla.com/pages/xxx` | 提示：「这是一个页面链接，请提供知识库链接（格式：https://lexiangla.com/spaces/xxx?company_from=yyy）。你可以在乐享中进入目标知识库首页，复制地址栏链接。」|
| 返回的文档链接打不开/无权限 | 链接中缺少 `company_from` 参数。页面链接必须带 `?company_from=xxx`，格式：`https://lexiangla.com/pages/<entry_id>?company_from=<company_from>` |

##### 配置结构

```json
{
  "_initialized": false,
  "lexiang": {
    "target_space": {
      "space_id": "",
      "space_name": "",
      "company_from": ""
    },
    "access_domain": {
      "domain": "lexiangla.com",
      "page_url_template": "https://lexiangla.com/pages/{entry_id}?company_from={company_from}",
      "space_url_template": "https://lexiangla.com/spaces/{space_id}?company_from={company_from}"
    }
  }
}
```

> **`access_domain` 会从用户粘贴的链接中自动提取域名**，无需手动配置。适配自定义域名的乐享部署。

后续文档中所有 `<SPACE_ID>`、`<COMPANY_FROM>`、`<ACCESS_DOMAIN>` 等占位符，均指从 `config.json` 中读取的实际值。

#### 乐享 MCP 工具的调用方式（重要 — 多 Agent 适配）

本 skill 需要服务多个 Agent 产品（OpenClaw、CodeBuddy、Claude Desktop 等）。不同 Agent 连接乐享 MCP 的方式不同，但**暴露的工具名称和参数完全一致**（都是 lexiang MCP server 提供的标准工具）。

> **核心原则**：本 skill 只描述「调用哪个工具 + 传什么参数」，**不规定具体的 MCP 调用语法**。每个 Agent 按自己的方式调用即可。

**各 Agent 产品的 MCP 连接方式**：

| Agent 产品 | lexiang MCP 连接方式 | 工具调用方式 |
|-----------|---------------------|-------------|
| **CodeBuddy** | 在 `~/.codebuddy/mcp.json` 中配置 lexiang server，通过 IDE 的 MCP 管理面板启用连接 | 直接调用 `space_describe_space`、`file_apply_upload` 等 lexiang MCP 工具 |
| **OpenClaw** | `claw install https://github.com/tencent-lexiang/lexiang-mcp-skill`，加载 skill 时自动连接 MCP | 同上，通过 skill 暴露的 MCP 工具调用 |
| **Claude Desktop / 其他 MCP 兼容 Agent** | 在 Agent 的 MCP 配置文件中添加 lexiang server URL | 同上 |

**MCP 连接检测与降级**：

在执行乐享操作前，**必须先检测 lexiang MCP 是否已连接**：
1. 读取 `config.json`，检查 `_initialized` 和 `lexiang.target_space.space_id`
2. 如果未初始化 → 先触发对话式配置初始化（参见上方「对话式配置初始化」），初始化流程中会自动完成 MCP 连接检测
3. 如果已初始化，尝试调用 `space_describe_space`（参数：`space_id=<config 中的 space_id>`）验证 MCP 连接
4. 如果调用成功 → MCP 已连接，继续后续流程
5. 如果调用失败（MCP 未连接）→ **提示用户检查 MCP 连接**，给出对应 Agent 的操作指引：
   - CodeBuddy：「请在 MCP 管理面板中确认 lexiang server 已启用并显示为已连接状态」
   - OpenClaw：「请确认已安装 lexiang skill（`claw install https://github.com/tencent-lexiang/lexiang-mcp-skill`）」
   - 其他 Agent：「请确认 MCP 配置中已添加 lexiang server」

> **⚠️ 禁止降级为 curl 调用 REST API**：即使 MCP 未连接，也**不要**自行编写 curl 调用乐享 REST API，因为：(1) 认证信息硬编码在 curl 中不安全；(2) 不同 Agent 的执行环境差异大，curl 方式不通用；(3) REST API 的 URL 格式和鉴权方式可能变化。应该引导用户修复 MCP 连接。

**认证配置**（首次使用时需要）：

1. 访问 [https://lexiangla.com/mcp](https://lexiangla.com/mcp) 登录后获取 **`LEXIANG_TOKEN`**（访问令牌，格式：`lxmcp_xxx`）
   > `COMPANY_FROM` 无需手动获取 — 会从用户粘贴的知识库链接中自动解析

2. 配置方式（二选一）：
   - **环境变量**（推荐）：`export LEXIANG_TOKEN="lxmcp_xxx"`
   - **直接修改 MCP 配置**：将 MCP server URL 中的 `${LEXIANG_TOKEN}` 占位符替换为实际值

3. 详细配置步骤参见：[lexiang-mcp-skill setup.md](https://github.com/tencent-lexiang/lexiang-mcp-skill/blob/main/setup.md)

#### 目标知识库

从 `config.json` 的 `lexiang.target_space` 中读取：

- **知识库名称**：`config.lexiang.target_space.space_name`
- **知识库访问链接**：按 `config.lexiang.access_domain.space_url_template` 格式拼接
- **Space ID**：`config.lexiang.target_space.space_id`

> **⚠️ 访问链接域名**：用户可访问的乐享前端域名从 `config.lexiang.access_domain.domain` 读取（默认为 `lexiangla.com`），**不是** `mcp.lexiang-app.com`（后者是 MCP API 服务端域名，浏览器无法直接访问）。所有展示给用户的链接必须按 `config.lexiang.access_domain.page_url_template` 格式生成。

#### 目录组织方式

按**天维度**组织目录：
```
知识库根目录/
  2026-02-25/
    文章标题A      (图文文章，在线文档 page 类型，图片内嵌)
    文章标题B      (纯文本文章，在线文档 page 类型)
  2026-02-26/
    文章标题C      (在线文档 page 类型)
```

> **⚠️ 默认格式**：所有文章（无论是否含图片）**统一使用在线文档（page）格式上传**。在线文档支持在乐享中直接编辑、划词评论、全文检索，体验远优于 PDF。PDF 仅作为降级方案（`md_to_page.py` 失败时）或用户明确要求时使用。

#### 操作流程

> **⚠️ 严格按步骤顺序执行，不得跳步！** 必须完成步骤 0→1→2→3→4 的完整流程。尤其是**步骤 2（创建日期目录）不可跳过**——文档必须上传到当天日期命名的文件夹中，而不是直接上传到知识库根目录。如果跳过步骤 2 直接用 `root_entry_id` 作为上传目标，文档将错误地出现在根目录下。

通过 lexiang MCP 工具，按以下步骤完成转存：

**步骤 0：读取配置（含初始化检测）**
- 读取 skill 目录下的 `config.json` 文件
- 检查 `_initialized` 是否为 `true` 且 `lexiang.target_space.space_id` 非空
- 如果**未初始化**（`_initialized` 为 `false` 或 `space_id` 为空）→ **触发对话式配置初始化流程**（参见上方「对话式配置初始化」），完成后再继续
- 提取 `lexiang.target_space.space_id`、`lexiang.access_domain.page_url_template` 等配置项

**步骤 1：获取知识库根节点**
- 调用 `space_describe_space`（参数：`space_id=<config 中的 SPACE_ID>`）
- 从返回结果中提取 `root_entry_id`

**步骤 2：检查/创建当天日期目录（🚨 必须先查再建，禁止直接创建）**

> **🚨 这是本 skill 最常见的错误！** 2026-05-11 实战中，Agent 未查询直接创建了同名目录。每次执行到此步骤，**必须**严格按照下方决策树执行，绝对禁止跳过查询直接调用创建工具。

---

**🚨 执行前必读：两种常见错误**

| # | 错误做法 ❌ | 正确做法 ✅ |
|---|---|---|
| 1 | 直接调用 `mcp__lexiang__entry_create_entry` 创建文件夹 | 先调用 `mcp__lexiang__entry_list_children` 查询根目录 |
| 2 | 只匹配 `name=="2026-05-11"`，不检查 `entry_type` | 必须同时匹配 `name=="2026-05-11"` **且** `entry_type=="folder"` |

---

**决策树（必须逐条执行，不可跳步）：**

```
步骤 2a：查询根目录
  工具：mcp__lexiang__entry_list_children
  参数：{"parent_id": "<root_entry_id>"}

  遍历返回的 entries[] 数组：
    查找是否有 entry_type=="folder" 且 name=="当天日期" 的条目
    例如今天 2026-05-11 → 查找 name=="2026-05-11" 且 entry_type=="folder"

  如果找到 → 记录其 id → 【跳到步骤 3，不创建】
  如果没找到 → 【继续到步骤 2b】

步骤 2b：确认不存在后，才能创建
  调用：mcp__lexiang__entry_create_entry
  参数：{"entry_type": "folder", "parent_entry_id": "<root_entry_id>", "name": "当天日期"}

  🚨 创建后必须置顶（否则新目录会出现在末尾）：
  1. 先调用 entry_list_children 获取父目录当前第一个条目的 entry_id
  2. 调用 entry_move_entry，使用 **before** 参数传入第一个条目的 entry_id，将新目录移到它之前（即置顶）
  参数：{"entry_id": "<新建的entry_id>", "parent_id": "<root_entry_id>", "before": "<当前第一个条目的entry_id>"}
  
  ⚠️ 注意事项：
  - after="" 实测是移到末尾（非置顶），API 文档描述有误，禁止使用
  - 必须用 before=<第一个条目ID> 才能真正置顶
  - 这一步不可省略！创建目录后如果不执行 move，新目录会默认出现在最底部
```

> **📌 关于分页的说明**：日期目录按创建时间倒序排列，当天的目录如果存在一定在第一页，无需处理分页。但如果你在处理非日期目录的场景（如查找某个不确定的条目），应注意 `next_page_token` 的存在。

---

**❌ 错误示例（禁止这样做）：**

```
# 错误：直接创建，不查询
→ 调用 mcp__lexiang__entry_create_entry，参数 name="2026-05-11"
→ 结果：知识库中出现多个同名 "2026-05-11" 文件夹
```

**✅ 正确示例（必须这样做）：**

```
# 正确：先查询第一页，找到就用，找不到才创建
→ 调用 mcp__lexiang__entry_list_children，参数 {"parent_id": "<root_entry_id>"}
→ 遍历 entries，检查是否有 name=="2026-05-11" 且 entry_type=="folder"
→ 找到 → 记录 id，跳过创建，直接进入步骤 3
→ 没找到 → 调用 mcp__lexiang__entry_create_entry 创建
```

**步骤 3：去重检查**
- 调用 `entry_list_children`（参数：`parent_id=<日期目录ID>`）查询该日期目录下已有的条目
- 按「名称 + 类型」检查是否已存在同名文档，如果已存在则跳过上传并告知用户

**步骤 3.5：非中文文章翻译（🚨 强制检查，不可跳过）**

> **⚠️ 重要**：无论文章是通过 `fetch_article.py`、`web_fetch`、PDF 下载还是其他方式获取，在上传到乐享之前**都必须经过语言检测和翻译步骤**。这是一个**强制检查点**，不存在任何可以跳过的"简化路径"。
>
> **PDF 特别说明**：PDF 文件（包括英文学术论文）同样适用此规则。非中文 PDF 必须先翻译为中英对照格式后再转存乐享，详见上方「PDF 文件/链接处理」章节的 Step D。
>
> **常见遗漏场景**：
> 1. ❌ 用 `web_fetch` 抓取后直接转 PDF 上传 → 英文原文未翻译
> 2. ❌ 觉得文章"看起来不长"就跳过翻译 → 知识库中留下纯英文文档
> 3. ❌ 翻译脚本不可用就放弃翻译 → 应该由 Agent 直接在对话中翻译
> 4. ❌ PDF 是论文就不翻译 → 英文论文同样必须翻译
>
> **正确做法**：每篇文章上传前，**必须先执行语言检测**，非中文则翻译后再上传。

在上传到乐享之前，**必须检测原文语言**。如果原文不是中文，则需要先翻译为**中英对照格式**后再归档。

**语言检测规则**：
- 读取 `<原文标题>.md` 的前 500 个字符，统计中文字符（Unicode 范围 `\u4e00-\u9fff`）占比
- 中文字符占比 **≥ 30%** → 判定为中文文章，**跳过翻译**，直接进入步骤 4
- 中文字符占比 **< 30%** → 判定为非中文文章，**执行翻译**

**翻译排版格式（中英对照）**：
- 按段落逐段翻译，每段原文紧跟对应中文翻译
- **段落之间不加分隔线 `---`**，仅通过空行分隔
- **中文翻译段落开头不加国旗 emoji（🇨🇳）**，直接以中文开始
- 标题也需要翻译，保留原文标题 + 中文翻译标题
- 列表项、引用块等结构元素同样逐条翻译
- **保留原文中的图片引用**（`![](images/xxx.png)`），图片引用放在对应段落的上方或下方，确保图文对应关系不丢失

```markdown
# Original English Title
# 中文翻译标题

Original first paragraph text...

第一段的中文翻译...

![](images/img_01_xxx.png)

Original second paragraph text...

第二段的中文翻译...
```

**翻译方式（按优先级）**：
1. **🥇 Agent（当前运行的模型）直接翻译**（**默认方式**，无需任何 API Key）：由 Agent 在对话中逐段翻译全文，生成 `<原文标题>_translated.md`。这是最可靠的方式，因为 Agent 本身就是 LLM，翻译质量有保障且无外部依赖。
   - **长文翻译策略**（>5000 字符）：将原文按段落或 `---` 分隔符拆分为 3000-5000 字符的块，逐块翻译后拼接。每块翻译完成后立即写入文件（追加模式），避免丢失进度。
   - **短文翻译**（≤5000 字符）：一次性翻译整篇文章。
2. **translate_gemini.py 脚本**（仅当用户**明确要求**且 `GEMINI_API_KEY` 可用）：
   ```bash
   python3 scripts/translate_gemini.py "<原文标题>.md" "<原文标题>_translated.md"
   ```
   ⚠️ 分块失败会静默保留英文，译后须搜整段未翻译的英文并补译。

**翻译完成后**：
- 本地保存两个文件：`<原文标题>.md`（原文）和 `<原文标题>_translated.md`（中英对照版）
- **归档到乐享知识库的必须是翻译后的中英对照版本**（`_translated.md`），确保知识库中的内容对中文读者友好
- 乐享文档标题使用：`<原文标题中文翻译>（<原文标题>）`，如：`AI 原型精通阶梯（The AI Prototyping Mastery Ladder）`

**步骤 3.7：评价信息处理（可选）**

如果在转存前用户提供了对文章的评价（例如："这篇文章好在：1）... 2）..."），需要在上传时自动添加评价信息：

1. **检测评价信息**：在对话中识别用户是否提供了评价内容（关键词：好在、评价、优点、建议等）
2. **保存评价内容**：将评价信息保存到临时文件（如 `/tmp/evaluation.txt`）
3. **传入脚本参数**：调用 `md_to_page.py` 时，添加 `--evaluation-file /tmp/evaluation.txt` 参数
4. **脚本自动处理**：`md_to_page.py` 会自动在文档顶部插入评价信息（格式为 blockquote，乐享可能自动转换为 callout 组件）

**对于非在线文档格式（如视频）**：
- 由于 lexiang MCP 工具中**没有创建评论的 API**（只有查询评论的 `comment_list_comments` 和 `comment_describe_comment`），暂时无法自动添加评论到视频文件
- **建议**：转存完成后，手动在乐享中添加评论

**示例：用户提供评价后的处理流程**
```bash
# 1. 将用户评价保存到临时文件
cat > /tmp/evaluation.txt << 'EOF'
这篇文章好在：
1）把智能体Agent做了分类，每个分类定义了对应是适用场景；
2）列举了详实的案例说明；
3）通过构建的复杂度、技术架构、实现时长、运行成本、衡量成功等几个维度来系统化地综合判断Agent落地的优先级
4）未来关于Agent选型上，能够提供系统性的参考建议
EOF

# 2. 调用 md_to_page.py，传入评价文件
python3 scripts/md_to_page.py "<原文标题>_translated.md" \
  --parent-id <日期目录ID> --name "<文档标题>" \
  --evaluation-file /tmp/evaluation.txt \
  --token "$LEXIANG_TOKEN" --company-from "$COMPANY_FROM"
```

**评价信息格式说明**：
- 脚本会将评价信息格式化为 blockquote（以 `>` 开头的 Markdown 格式）
- 在乐享在线文档中，blockquote 可能被自动渲染为 callout 组件（带有左侧竖线或背景色）
- 如果需要真正的 callout 组件（特殊 block 类型），需要通过 `block_create_block_descendant` API 创建，但需要先了解 callout 的 block 结构

**步骤 3.8：页面内嵌视频检测与链接附加（⚠️ 不可跳过）**

在生成 PDF 或上传之前，**必须检测页面中是否包含嵌入视频**。嵌入视频（如 Wistia、YouTube、Vimeo、Loom 等 iframe 嵌入）在转为 PDF 时会完全丢失，因此需要将视频链接以文本形式附加到文档末尾，确保知识库读者能找到并观看原始视频。

**检测范围**（按优先级扫描）：
1. `<iframe>` 嵌入 — 匹配 `src` 中包含 `youtube`、`youtu.be`、`vimeo`、`loom`、`wistia`、`vidyard`、`player` 的 iframe
2. `<video>` 标签 — 提取 `src` 或内部 `<source>` 的 `src`
3. `<a>` 链接 — 匹配 `href` 指向 `youtube.com/watch`、`youtu.be/`、`vimeo.com/`、`loom.com/share` 等视频平台
4. 平台特定容器 — 如 readme.io 的 `rdmd-embed` 组件、`[class*="video"]` 容器等

**视频链接还原规则**：
- Wistia embed（`fast.wistia.net/embed/iframe/<id>`）→ 附加可观看链接 `https://fast.wistia.net/embed/iframe/<id>`
- YouTube embed（`youtube.com/embed/<id>`）→ 还原为 `https://www.youtube.com/watch?v=<id>`
- Vimeo embed（`player.vimeo.com/video/<id>`）→ 还原为 `https://vimeo.com/<id>`
- Loom embed（`loom.com/embed/<id>`）→ 还原为 `https://www.loom.com/share/<id>`
- 其他视频 URL → 原样保留

**附加格式**：在 Markdown 文档末尾（PDF 生成前）追加一个独立章节：

```markdown

---

## 📹 页面内嵌视频

本页面包含以下嵌入视频，PDF 中无法播放，请通过链接观看：

1. [视频] https://fast.wistia.net/embed/iframe/xxxxx
2. [视频] https://www.youtube.com/watch?v=yyyyy
```

如果使用 Playwright 直接生成 PDF（非 `fetch_article.py` 抓取），应在 `page.pdf()` 之前通过 `page.evaluate()` 在页面底部注入视频链接信息块。

**步骤 4：上传到乐享（统一使用在线文档格式）**

> **🚨 核心原则：所有文章默认使用在线文档（page）格式上传，不再默认转 PDF。**
> 在线文档的优势：支持编辑、划词评论、全文检索、移动端阅读体验好。
> PDF 仅在以下情况使用：(1) `md_to_page.py` 和 `entry_import_content` 都失败时的最终降级；(2) 用户明确要求 PDF 格式。

检查 `<原文标题>.md` 文件同目录下是否存在 `images/` 目录且包含图片文件：

> **🚨 图片判断 Checklist（必须逐条检查）**：
> 1. `images/` 目录是否存在且有图片？
> 2. Markdown 内容中是否有 `![](images/xxx)` 本地引用？（仅检查目录不够！如果 images/ 有图片但 Markdown 中无引用，说明抓取阶段出了问题——正文提取失败导致图片引用丢失，需要重新抓取）
> 3. 如果 Markdown 中只有外链图片（`![](https://...)`）而无本地引用，说明图片没有被下载到本地。`entry_import_content` 导入外链图片后，乐享中如果外链 CDN 有防盗链/过期，图片将不可见。此时应先下载图片到本地，再用 `md_to_page.py` 导入。
> 
> **判断结论**：
> - ✅ images/ 有图片 + Markdown 有 `![](images/xxx)` → **图文文章**，走图文路径
> - ⚠️ images/ 有图片 + Markdown 无本地引用 → **抓取异常**，需重新抓取或手动修复 Markdown
> - ⚠️ images/ 无图片 + Markdown 有外链图片 → **外链图片**，建议下载后转本地引用
> - ✅ images/ 无图片 + Markdown 无图片引用 → **纯文本文章**，走纯文本路径

- **有图片（图文文章）** → 使用 `scripts/md_to_page.py` 将 Markdown 图文导入为在线文档（图片内嵌到正文对应位置）：
  ```bash
  python3 scripts/md_to_page.py "<原文标题>.md" \
    --parent-id <日期目录ID> --name "<原文标题>" \
    --token "$LEXIANG_TOKEN" --company-from "$COMPANY_FROM"
  ```
  脚本会自动：按图片位置拆分 markdown → 分段导入文字（直传原始 markdown，不做 base64 编码）→ 逐张上传图片到 COS → 在正确位置插入 image block。
  
  **降级方案 A（🥈 首选降级 — MCP Direct HTTP Call，全自动，无需用户确认）**：

  当 `md_to_page.py` 因缺少 LEXIANG_TOKEN 无法运行时（如 mcp.json 中无 lexiang 配置，只有 connector 模式），**使用本方法**。
  
  > **🚨 本方法是 2026-06-21 实战验证的全自动图文上传路径。Agent 应直接执行完整流程（创建页面→导入全文→逐张上传图片→插入 block→删除占位符），禁止停下来问用户确认！**
  >
  > 完整流程见 SKILL.md Step 3「MCP 直接调用方法」章节（含 Python 调用模板和注意事项）。

  **快速参考**（核心步骤）：

  ```
  Token 获取：~/.workbuddy/connectors/<uuid>/mcp.json → connector:lexiang.headers.Authorization
  MCP 端点：https://mcp.lexiang-app.com/mcp?company_from=<COMPANY_FROM>

  1. entry_create_entry(page) → entry_id
  2. HTTP POST → entry_import_content(全文纯文字版, parent_id=日期目录) → page_entry_id
     （响应解析：json.loads(resp['result']['content'][0]['text'])['data']['entry']['id']）
  3. block_list_block_children(entry_id) → 定位占位 block 的 index + block_id
  4. 从后往前对每张图片：
     a. file_apply_upload → session_id + upload_url
     b. Python urllib.request.PUT 上传到 COS
     c. file_commit_upload(session_id)
     d. block_create_block_descendant(index=str(占位index), image.session_id)
  5. 从后往前删除占位 block：block_delete_block(block_id, entry_id)
  6. block_list_block_children 验证：image block 数量 == 原图数量
  ```

  > **⚠️ 图片上传路径优先级更新（2026-06-21）**：
  > 1. 🥇 `md_to_page.py`（LEXIANG_TOKEN 可用时）→ 自动交替导入文字+图片
  > 2. 🥈 **MCP Direct HTTP Call（本文档方法）** → 全自动，无需 TOKEN，无需用户确认 ← **新增**
  > 3. 🥉 MCP「先全文后补图」（通过 DeferExecuteTool/call_tool 逐工具调用）
  > 
  > **🚨 禁止使用 .md 文件上传作为降级方案**：.md 文件上传后乐享中图片引用不渲染为 inline 图片

  **降级方案 B（备选 — 通过 DeferExecuteTool / call_tool 包装器）**：
  
  > **🚨 推荐方式：先全文导入，再逐张补图（使用 block index 精确定位）**
  > 
  > 两种策略均可行：
  > 1. **先全文后补图**（✅ 推荐，效率更高）：用 `entry_import_content` 一次性导入全部文字（图片位置用占位标记），然后通过 `block_list_block_children` 获取 block 列表，找到占位 block 的 index，逐张在正确位置插入图片。
  > 2. **交替导入**（可选，更简单但更慢）：按「文字段→图片→文字段→图片→...」交替导入，每张图片 index=-1 自然落在末尾。但此方式每个文字段都要调用 `entry_import_content_to_entry`，容易触发限频。
  
  **执行流程（推荐：先全文后补图）**：
  
  ```
  步骤 A1：准备——识别图片位置
    读取 article.md 内容
    找出所有 ![xxx](images/yyy) 引用的位置和文件名
    将图片引用替换为占位标记 [图片: yyy]，得到纯文字版 Markdown
  
  步骤 A2：一次性导入全文文字
    entry_import_content（space_id, parent_id=<日期目录ID>, name="<原文标题>", content=<纯文字版>, content_type="markdown"）
    记录 entry_id
    ⚠️ 此接口无长度限制，30K+ 字符可一次性传入，无需分块
    🚨 content 中禁止包含任何图片语法（![alt](url) 或 <image src="url"/>），否则会产生空图片 block！
  
  步骤 A3：逐张上传图片并插入正确位置
    1. block_list_block_children（entry_id=<page_id>, with_descendants=False）获取 block 列表
       ⚠️ 大文档（300+ blocks）返回数据量很大，建议用 _mcp_fields 排除不需要的字段
       _mcp_fields 格式：逗号分隔字符串（如 "-blocks.text,-blocks.heading1"），不是 JSON array
    2. 在 block 列表中找到包含占位标记 [图片: yyy] 的 block，记录其 index
       锚点匹配技巧：
       - 提取每个 block 的文本内容（text/heading1/heading2 等字段的 elements[].text_run.content 拼接）
       - 用图片前后的关键短语作为锚点搜索（如"真正的威胁是趋势方向"）
       - 跨语言匹配：翻译后的文档用中文锚点搜索比英文锚点更可靠
       - 找到锚点 block 后，图片插入位置 = 该 block 的 index + 1
    3. 对每张图片：
       a. **先检测实际格式**：`sips -g format images/<文件名>` → 输出 `jpeg` 则 mime_type="image/jpeg"，输出 `png` 则 mime_type="image/png"
          ⚠️ 文件扩展名不一定反映实际格式！Substack CDN 会将 JPEG 图片保存为 .png 扩展名
          ⚠️ Content-Type 不匹配实际格式 → COS 返回 403 Forbidden
       b. block_apply_block_attachment_upload（entry_id, name=<文件名>, size=<字节数字符串>, mime_type=<检测到的实际格式>）→ session_id + upload_url
          ⚠️ size 参数必须是字符串类型（如 "54541"），传整数会导致参数校验失败
       c. **上传到 COS**（🚨 禁止用 curl，必须用 Python urllib.request）：
          ```python
          import urllib.request
          req = urllib.request.Request(upload_url, data=file_bytes, method='PUT')
          req.add_header('Content-Type', mime_type)
          req.add_header('Content-Length', str(size))
          resp = urllib.request.urlopen(req)
          ```
          ⚠️ curl 命令在 COS 上传时会出现 403（URL 含特殊字符 %2F/%3B 等，curl 处理有问题），必须用 Python urllib.request
       d. block_create_block_descendant（entry_id, parent_block_id=<page_root_block_id>, index=<占位block的flat_index+1>, descendant=[{block_type: "image", image: {session_id}}]）
          ⚠️ index 不等于 block_list 的直接子节点位置！API 使用包含嵌套子节点的扁平索引系统
          ⚠️ 估算公式：直接子节点位置 + 前面所有嵌套子节点数量（quote/callout/toggle 的 children 计入）
          ⚠️ 建议从后往前插入，避免前面插入影响后续 index
    5. 如遇限频，等待 5 秒后重试
  
  步骤 A3（替代）：交替导入方式（更简单但更慢）
    如果不想处理 block index 计算，也可以按交替方式：
    - 按 ![xxx](images/yyy) 位置拆分为 segments：[("text", "..."), ("image", "img_01.png"), ...]
    - is_first = true
    - for each segment:
        if text: entry_import_content_to_entry（entry_id, content, force_write=is_first）; is_first=false; sleep 10s
        if image: 三步上传 + block_create_block_descendant（index="-1"）
    ⚠️ 此方式每个文字段需间隔 10s 避免限频，47张图的文章可能需要 8+ 分钟
  ```
  
  > **⚠️ 图片上传路径优先级**：
  > 1. 🥇 `md_to_page.py`（LEXIANG_TOKEN 可用时）→ 自动交替导入文字+图片，无需手动计算 index，一步到位
  > 2. 🥈 MCP「先全文后补图」（LEXIANG_TOKEN 不可用时）→ 需手动计算 index，图片位置可能偏差，需要 trial-and-error 验证
  > 3. 🥉 MCP「交替导入」（极简但慢）→ 每段文字需 sleep 10s 避限频
  >
  > **⚠️ 为确保 md_to_page.py 可用，翻译时必须保留 `![alt](images/xxx)` 图片语法，禁止替换为 `[IMG_PLACEHOLDER]`！**
  > 
  > **⚠️ 小图片（<50KB 的 icon/分隔线/SVG 装饰图）可跳过**，只上传有信息量的关键图片（图表/截图/概念图）。
  
  > **⚠️ 得到 APP 文章特殊情况**：得到文章通常有 80-100+ 张图片，其中大部分是公式渲染图（3-10KB），真正有信息量的数据图表约 5-10 张（>50KB）。对得到文章，**必须**上传 >50KB 的关键图片（概念图、流程图、案例配图等），不需要逐张上传所有小图。
  
  > **⚠️ 得到文章完整转存流程（2026-05-09 实战验证）**：
  > 1. `fetch_article.py --cdp` 抓取全文 → 本地 article.md + images/
  > 2. 提取纯文字版（去掉 `![](images/...)` 引用 + 去掉得到APP UI噪声如"展开"、"分享"、点赞数、用户留言等）
  > 3. 创建 page → 分块导入纯文字（每块 ≤4000 chars）
  > 4. 筛选 >50KB 的关键图片（用 `find images/ -size +50k`）
  > 5. 排除 SVG 格式的 UI 图标（查看文件头是否为 `<?xml`）
  > 6. 逐张上传关键图片并插入文档对应位置
  
  **降级方案 B（最终降级）**：如果以上都失败 → 调用 `scripts/md_to_pdf.py` 转为 PDF，再通过三步上传流程上传：
  1. `file_apply_upload`（参数：`parent_entry_id=<日期目录ID>`, `name="<原文标题>.pdf"`, `size=<文件字节数>`, `mime_type="application/pdf"`, `upload_type="PRE_SIGNED_URL"`）
  2. 使用 `curl -X PUT` 将 PDF 文件上传到返回的 `upload_url`
  3. `file_commit_upload`（参数：`session_id=<上一步返回的session_id>`）
  
  > **🚨 绝对禁止**：不要用 `file_apply_upload` 直接上传 .md 文件！.md 上传后在乐享中会丢失所有图片信息，用户看到的只是含 `![](images/xxx)` 引用的纯文本，毫无可读性。

- **无图片（纯文本文章）** → 使用 `entry_import_content` 创建为**在线文档（page 类型）**：
  - 参数：`space_id=<config 中的 SPACE_ID>`, `parent_id=<日期目录ID>`, `name="<原文标题>"`, `content=<Markdown文件内容>`, `content_type="markdown"`
  - 在线文档支持在乐享中直接编辑
  - **⚠️ `entry_import_content` 没有长度限制**，31K+ 字符的长文可一次性传入，**不需要分块**

- **通过 `web_fetch` 抓取的文章（无本地图片文件）** → 直接使用 `entry_import_content` 创建在线文档，Markdown 内容中的外链图片在乐享中可能无法显示，但文字内容完整可编辑、可检索。

#### 长文导入最佳实践（🚨 重要性能优化）

> **核心原则：优先使用 `entry_import_content` 一次性创建带内容的页面，避免分块追加。**

**为什么不分块？**
- `entry_import_content` 接口声明没有长度限制，实测 30K+ 字符可一次性传入
- `entry_import_content_to_entry`（追加到已有页面）有**限频保护**（错误码 50130003），连续调用间隔需 ≥10 秒
- 分块导入 30K 文章需要 5-9 次调用 × 10s 间隔 = 至少 50-90 秒的等待时间

**最佳路径（一步到位）**：
```
entry_import_content（name="标题", content=<完整内容>, parent_id=<日期目录ID>, space_id=<SPACE_ID>）
```
这会**原子性地创建页面 + 写入全部内容**，只需一次 MCP 调用，无限频问题。

**何时才需要分块追加（`entry_import_content_to_entry`）？**
- 仅当需要在**已有页面**的**指定位置**追加内容时才用（如图文交替导入场景）
- 如果遇到限频 50130003：等待 10 秒后重试，**不要**连续快速重试
- 每次追加操作之间至少间隔 10 秒

#### 图片逐张上传策略（无需批量脚本）

> **核心原则：先导入全文文字，再逐张上传图片到正确位置。图片逐张处理即可，不需要批量工具或 LEXIANG_TOKEN。**

当文章含有图片（`images/` 目录非空），但无 `LEXIANG_TOKEN`（即 `md_to_page.py` 不可用）时，采用以下两步策略：

**第一步：一次性导入全文文字（去掉本地图片引用）**
1. 读取 article.md，将 `![xxx](images/yyy)` 替换为占位标记（如 `[图片: yyy]`），得到纯文字版
2. 用 `entry_import_content` 一次性创建页面并写入全部文字内容

**第二步：逐张上传图片并插入对应位置**
1. 调用 `block_list_block_children` 获取页面所有 block 列表
2. 找到图片占位文字对应的 block index
3. 对每张图片执行三步上传：
   - `block_apply_block_attachment_upload`（申请上传凭证）→ 获得 session_id + upload_url
   - `curl -X PUT "<upload_url>" -H "Content-Type: image/png" -H "Content-Length: <size>" --data-binary @<图片路径>`
   - `block_create_block_descendant`（在正确 index 插入 image block，传入 session_id）
4. 每张图片上传完成后，后续图片的 index 需要 +1（因为插入了新 block）

**图片上传间的限频应对**：
- `block_apply_block_attachment_upload` + `block_create_block_descendant` 通常不限频（不同于 `entry_import_content_to_entry`）
- 如果遇到 50130003，等待 5 秒后重试
- 47 张图片的文章：预计 3-5 分钟可全部上传完成（每张约 3-5 秒）

**可选优化——只上传关键图片**：
- 对于「演示幻灯片截图」类文章（如 talk/presentation 的文字版），幻灯片图片通常是辅助性的，文字内容已经完整涵盖了所有信息
- 可以只上传信息量大的图片（如架构图、流程图、数据图表），跳过纯装饰性/标题性的小图
- 判断标准：文件大小 > 50KB 的图片通常有实质信息量

**步骤 5：输出结果**
- 按 `config.json` 中的 `lexiang.access_domain.page_url_template` 格式拼接文档链接，告知用户
- 示例：`https://lexiangla.com/pages/<entry_id>?company_from=<company_from>`（域名和 company_from 从配置读取，**不要**硬编码）
- **⚠️ 链接必须包含 `company_from` 参数**，否则用户打开页面会跳转到登录页或显示无权限

#### 注意事项

- **配置初始化是前置条件**：首次使用时会自动通过对话引导完成知识库配置，无需手动编辑文件
- **MCP 连接是前置条件**：必须先确认 lexiang MCP 已连接才能执行操作。不同 Agent 的连接方式不同，参见上方「乐享 MCP 工具的调用方式」
- **访问链接域名**：展示给用户的链接一律按 `config.json` 中 `page_url_template` 格式生成（含 `company_from` 参数），**不要**使用 `mcp.lexiang-app.com`，**不要**省略 `company_from`
- **上传前自动去重**：按「文档名称 + 文档类型」在目标日期目录下查重，避免重复上传
- **默认使用在线文档（page）格式**：所有文章（含图文）统一以在线文档格式上传，支持编辑、检索、评论。PDF 仅作为最终降级方案
- 纯文本文章直接用 `entry_import_content`，图文文章优先用 `md_to_page.py`（图片内嵌），降级用 `entry_import_content`（图片不内嵌但文字完整）
- PDF 转换依赖 `pymupdf` 库（`pip3 install pymupdf`），仅在前两种方式都失败时使用
- 如果同一天多次处理不同文章，它们会归入同一个日期目录下

---

### 🚨 大文档上传通用策略（>30K 字符）

**核心问题**：Agent 通过 MCP connector 调用工具时，`content` 参数有大小限制（约 30K 字符）。超大文档直接传会失败并导致上下文腐化。

**通用解决方案**：使用 `scripts/upload_doc_to_lexiang.py`

```bash
# 有 LEXIANG_TOKEN（最佳体验，创建在线文档 page）
python3 scripts/upload_doc_to_lexiang.py <文件.md> \
    --parent-id <目录ID> --name "标题" --space-id <SPACE_ID>

# 无 LEXIANG_TOKEN（输出 Agent 执行指令）
python3 scripts/upload_doc_to_lexiang.py <文件.md> \
    --parent-id <目录ID> --name "标题" --mode instructions
```

**Agent 端操作（无 TOKEN 降级方案，3步完成）**：
1. `file_apply_upload(parent_entry_id, name, size, mime_type="text/markdown", upload_type="PRE_SIGNED_URL")` → 获取 `upload_url` + `session_id`
2. `curl -X PUT "<upload_url>" --data-binary @<文件>` → HTTP 200
3. `file_commit_upload(session_id)` → 完成

**禁止事项**：
- ❌ 禁止把 >30K content 塞进 MCP 工具参数（必定失败）
- ❌ 禁止分块追加 entry_import_content_to_entry（限频 + 重试 + 上下文腐化）
- ❌ 禁止在 Agent 对话中内联大段 markdown（消耗 token + 处理失败）
- 使用 `_mcp_fields` 参数可以减少返回数据量，如 `_mcp_fields=["id", "root_entry_id", "name"]`

