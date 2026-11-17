# 知识库保存流程

当用户要求将检索到的社交内容保存、归档、添加、导出，或发送到知识库、笔记应用、工作区文档等目的地时，使用本文档。

本 Skill 不运行后台写入服务，也不会自动归档。优先使用当前环境已经提供的目的地写入工具；如果没有原生工具，再按本文档中的目的地辅助代码做最小改造。

Notion 和 Obsidian 需要特别处理：先检查当前环境是否已经有用户批准的默认连接器、工具、app、MCP server 或已安装 Skill。只要默认写入能力存在，并且匹配用户要写入的目的地，就优先使用它。只有在默认/原生目的地工具不可用、权限不足或失败时，才使用下方兜底辅助代码。

## 安全边界

- 只保存当前检索项，或用户明确选择的项目。
- 当当前请求没有明确目的地时，先确认目的地。
- 写入外部服务、创建本地新文件或保存凭据前，先询问用户。
- 不要创建周期性归档、后台同步、默认保存目标或宽泛的自动保存行为。
- 不要保存完整 API key、cookie、session token 或私密账号数据。

## 保存流程

```text
用户要求保存/归档当前社交内容
 -> 优先复用当前任务里的 AgentLens 结果或已保存的响应 JSON
 -> 只有没有可用结果，或用户明确要求刷新时，才重新 fetch
 -> 如果重新 fetch 成功，尽量保存完整响应 JSON 作为当前任务产物
 -> 如果用户要求理解媒体文件或转写，先完成该步骤
 -> 构建干净 markdown 整理稿
 -> 如果目的地不明确，先确认
 -> 如果用户明确要求长期保存媒体文件，只选择并下载当前任务需要的媒体
 -> 使用该目的地在当前环境中的写入/保存工具
 -> 如果保存成功，报告保存了什么、保存到哪里
 -> 如果保存失败，遵循下方保存失败策略
```

在总结、媒体理解或转写之后保存时，先查找内存中的结果或当前任务 JSON，例如 `/tmp/agentlens_{platform}_{timestamp}_response.json`。不要仅为了保存内容重新 fetch。如果响应缺失、损坏、过期或 URL 不匹配，重新调用前先告诉用户：再次成功调用 AgentLens API 可能消耗额度。

## 整理稿结构

发送到目的地前，先准备一份可迁移的 markdown：

整理稿里面向用户阅读的字段标签和小节标题，默认跟随用户当前对话语言。下面示例使用中文；如果用户用英文或其他语言对话，就换成对应语言。用户提供的模板、已有 Notion/database 字段名、API/schema 字段名/key 必须原样保留，不要翻译。不要在整理稿中保留或回显任何凭据值。

```markdown
# {title or concise source label}

原始链接：{url}
平台：{platform}
作者/来源：{author}
账号/Handle：{handle_or_author_id，如有}
标题：{title}
发布日期：{published_at or unknown}
获取日期：{YYYY-MM-DD}

## 摘要
...

## 要点
- ...

## 字幕或说明文案
...

## 媒体解读
...

## 原文
...
```

省略空 section。除非用户要求，否则不要包含原始 JSON。

## 目的地模式

### 凭据和目标位置查找说明

下方话术会提示用户去哪里找文件夹路径、vault 路径、integration token 和 database/data source ID。对 ima，不要让用户自行查找或提供 `knowledge_base_id`：在用户允许、且本次会话已有凭据后，应通过 OpenAPI 查询可写知识库，再让用户从列表中选择。这些说明基于本 Skill 编写时各产品的常见界面；如果目标产品界面已经变化，而当前 agent 无法实时验证，请让用户以该产品最新官方帮助或开发者文档为准。

### 目的地设置记忆（仅在用户同意时）

一次保存成功且用到了目的地设置后，在结束任务前另行提出一个明确的是/否选择，询问是否记住该目的地的最小设置。不能因为用户之前提供过凭据、刚刚保存成功，或又要求保存另一条内容，就推断用户同意。

- API key、token 等秘密只能存入运行环境已批准的 secret store。除非用户明确同意某个确切存储位置，不要写入聊天记忆、报告或明文本地文件。
- 知识库/database ID、vault 路径和可选目的地文件夹都属于私密配置元数据。只有在用户明确同意后，才能存入已批准、按目的地范围限定的 connector 配置或记忆机制；否则只在当前会话保留。
- 如果当前运行环境没有已批准的持久化机制，应如实说明；不要自行创建或扫描本地配置目录来替代。
- 当前会话缺少设置时，不要搜索对话历史、通用记忆、home 目录或无关本地文件来找回它；请用户再次选择或提供。

ima 或 Obsidian 保存成功后可使用：

```text
要不要让我记住这个目的地，方便以后保存？凭据只能存到当前运行环境已批准的 secret store；选定的知识库/vault 位置只能存到已批准的目的地配置。你不同意的话，我只在本次会话使用。
```

### 目录与命名建议

如果目标知识库支持文件夹、目录或类似层级，优先沿用用户已有整理方式。如果用户没有指定目录，也没有现成约定，可以建议按平台和账号分组：

```text
Social Reads/
  {platform}/
    {handle_or_author_id_or_unknown}/
      {YYYYMMDD-HHMM}-{platform}-{handle_or_author_id_or_unknown}-{short_title_or_text_slug}.{ext}
```

如果目标知识库不支持目录结构，就把这些信息放进标题、database 字段、标签或整理稿正文里。不要在未确认目的地和路径的情况下主动创建新目录；只有用户确认，或当前运行环境已经有已批准的默认社交保存目录时，才使用该目录结构。

### 明确要求保存媒体文件时

默认情况下，在整理稿中保存摘要、要点、原文/正文、媒体解读结论和来源/媒体 URL。摘要和要点放在前面，原文/正文放在偏下方。不要因为目标知识库支持附件，就自动下载和上传所有返回的媒体文件。

用户要求把正文/原文与图片、视频、媒体或图文内容一起保存时，视为明确要求保留其中点名的媒体；不得擅自理解为只保存文字。对 ima 的图片保留，必须创建一个 `media_type=20` HTML 文档，并以 base64 内嵌所要求的图片；不得静默降级成 Markdown 或仅导入 URL。对 Notion，当前环境存在经验证的原生媒体 block 时才使用；否则必须说明限制，并在降级成仅链接或纯文本前取得用户同意。

当用户要求保存帖子，且 AgentLens API 返回了媒体 URL，但用户没有明确要求长期保存原始媒体文件时，使用以下说明：

```text
我会默认保存摘要、原始链接、媒体解读结论和媒体 URL。如果你需要长期保存原始图片/视频文件，请告诉我，我会按目标知识库支持的方式处理。
```

只有当用户明确要求长期保存媒体文件时，才按目标知识库支持的附件流程处理：

1. 如果 AgentLens API 返回多个媒体项，而用户没有要求全部保存，先确认要保存哪些媒体。
2. 只把选中的媒体下载到当前请求使用的 `/tmp/agentlens_*`。
3. 文件名使用便于长期识别的格式，包含日期时间、平台、作者/来源 id，以及简短标题或正文摘要。
4. 按目标工具支持的方式上传或附加媒体：
   - Notion：如果当前环境有原生 Notion 连接器且支持文件/媒体块，优先使用它。只有兜底 API 辅助代码可用时，不要假装已经上传文件；应在页面正文中写入来源/媒体 URL 和准确本地文件名，除非当前运行环境有已验证的 Notion 文件上传辅助代码。
   - Obsidian/本地 vault：把媒体放入 vault 内相对附件目录，例如 `attachments/`、`assets/`，或用户现有约定目录，然后在 Markdown 笔记中使用相对路径链接。
   - ima：遵循下方 ima 专门规则。默认不要把图片上传成与主整理稿脱离的独立知识条目。长期保存视频时，除非当前运行环境确认有原生/视频上传路径，否则不要承诺稳定内嵌视频归档。
   - 本地/工作区文件：把媒体保存在笔记旁边，或同级 assets 文件夹中，并在笔记中链接。
5. 如果目标知识库不支持稳定的媒体上传，在整理稿里保留准确文件名、来源 URL 和过期风险，并在合适时提供本地文件夹导出方案。

下载媒体前的建议确认话术：

```text
我可以保存原始媒体文件。请确认要保存全部媒体，还是只保存其中一部分。我会按目标知识库支持的附件方式处理；部分知识库可能只能保存链接或文件名，不能稳定内嵌原始媒体。
```

不要默认 base64 内嵌大视频。不要把 TikTok、Instagram 等平台的 CDN/source URL 当作长期归档链接。

### 本地 Markdown 或工作区文件

当用户要求保存为文件、本地笔记、Markdown、项目笔记或工作区产物时使用。

1. 如果未指定路径，先确认路径。
2. 基于平台/标题/日期生成安全文件名，并写入一个 markdown 文件。
3. 包含原始链接、平台、作者/来源、账号/Handle、发布日期和获取日期。
4. 除非用户确认，否则避免覆盖已有文件。
5. 如果用户要求保存媒体，把媒体放在笔记旁边或同级 assets 文件夹中，并用相对 Markdown 路径链接。

缺少路径时，可使用以下话术：

```text
你希望把这份整理稿保存到哪里？请提供一个文件夹路径或工作区位置。一般可以在 Finder/文件资源管理器中打开目标文件夹后复制路径，也可以在该目录打开终端后用 `pwd` 查看路径。我可以按日期、平台、账号和标题建议文件名；除非你确认，否则不会覆盖已有文件。
```

### Obsidian

当用户要求保存到 Obsidian 或 vault 时使用。

1. 在询问 vault 路径前，先确认可写文件系统边界。如果 Agent 运行在用户本机，且用户明确要求保存到 Obsidian，可使用已批准的原生 Obsidian 集成、系统文件选择器、已登记 vault 列表，或在本机已批准位置做受限扫描，发现候选 vault 后让用户选择。不得递归广扫 home 目录、读取笔记内容，或在未获同意时记住发现的路径。
2. 如果 Agent 运行在远程服务器，检查当前宿主是否能通过以下任一方式写入：自身可达的 vault 文件系统、已批准的 Obsidian 连接器/app bridge/MCP server、已配对且获得文件写入批准的本地 node，或明确配置且可访问的 vault 同步副本/镜像路径。用户把自己笔记本/桌面端路径发给远程 Agent，并不意味着该路径可写。
3. 如果没有已批准的远程写入路径，必须在接受本机路径为保存目标前说明这一点；不得声称、暗示或排队执行直接本地 vault 写入。
4. 没有可写路径时，提供选择：(a) 继续保存到 Obsidian：配对本地 node、连接已批准写入工具，或选择可达的同步 vault/镜像；(b) 另行批准非 Obsidian 导出，例如 Markdown 文件或聊天附件。不得把选项 (b) 称为已保存到 Obsidian。
5. 只有用户选择了可用的 Obsidian 路径、且目标文件系统确实可达后，才询问 vault/path；本机发现流程中，应先让用户从候选 vault 中选择，再写入。
6. 在已确认且可达的 vault 路径中创建 Markdown 笔记。
7. 只有当用户或 vault 约定需要时，才使用 frontmatter。
8. 只有当用户要求或当前笔记规范非常明确时，才添加 tags。
9. 如果用户要求保存媒体，优先沿用 vault 已有附件目录约定；不知道约定时，询问或建议一个 vault 相对附件目录。
10. 不要递归或广泛扫描用户 home 目录来寻找 vault。候选发现仅限于已批准的原生选择器、已登记的 vault 列表、用户提供的路径，或本机已批准位置内的受限扫描；发现候选时不得读取笔记内容、配置或凭据。
11. vault 不可达时，必须把 Obsidian 保存标为失败。提供下载文件或聊天附件只能算用户另行批准的导出，不能算作已保存到 Obsidian。
12. 如果本次任务使用的 vault/path 尚未获准持久化，保存成功后可以提出上方“目的地设置记忆（仅在用户同意时）”；未经明确同意不得保留该目的地。

缺少 vault/path 时，可使用以下话术。可根据用户上下文适当缩短，但必须保留目标、路径和权限确认：

```text
本机宿主在用户明确要求保存到 Obsidian 后可使用：`我可以访问已批准的本机位置，发现以下候选 vault：{名称/路径}。请问要存到哪一个？` 发现阶段不得读取笔记内容。

远程宿主没有写入路径时使用：`当前远程宿主没有通向你电脑 Obsidian vault 的已批准写入路径，所以我不能直接保存。你想继续保存到 Obsidian 吗？可以配对本地 node、连接已批准的 Obsidian 写入工具，或选择一个当前可访问的同步 vault/镜像；如果暂不设置，我也可以另行提供 Markdown 文件或聊天附件，但那不等于已保存到 Obsidian。`
```

#### Obsidian 本地 vault 辅助代码

当 Obsidian 以本地 vault 路径形式可用，且用户已批准写入该路径时，使用这段辅助代码。

必要输入：

- `vault_dir`：已确认的 Obsidian vault 目录。
- `folder`：vault 内的可选文件夹，例如 `Social Reads`。
- `title`：笔记标题。
- `content`：按上方结构生成的 markdown 内容。

执行模式：

```text
确认 vault_dir 和可选 folder
 -> 构建一个 markdown 笔记
 -> 生成安全文件名
 -> 除非用户批准，否则拒绝覆盖已有文件
 -> 将笔记写入所选 vault 路径
 -> 报告 vault 相对路径
```

可移植 Python 骨架：

```python
from pathlib import Path
import re


def _safe_filename(title):
    name = re.sub(r"[\\/:*?\"<>|#\\[\\]]+", "-", title).strip(" .-")
    return (name or "social-read")[:120] + ".md"


def save_to_obsidian(vault_dir, title, content, folder=None, overwrite=False):
    vault = Path(vault_dir).expanduser().resolve()
    if not vault.exists() or not vault.is_dir():
        raise RuntimeError("Obsidian vault path does not exist or is not a directory")
    target_dir = vault / folder if folder else vault
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / _safe_filename(title)
    if target.exists() and not overwrite:
        raise RuntimeError(f"Note already exists: {target.relative_to(vault)}")
    target.write_text(content, encoding="utf-8")
    return str(target.relative_to(vault))
```

如果当前环境有原生 Obsidian/MCP 连接器，优先使用原生连接器。只有在用户确认 vault 路径后，才直接通过文件系统写入。

### Notion

当用户要求保存到 Notion 时使用。

1. 先检查当前环境是否有用户默认的 Notion 连接器、app、MCP server 或已安装的 Notion 写入 Skill。可用时优先使用。
2. 原生连接器不可用或未连接时，不能直接断言“无法写入 Notion”。在再次索要 token 前，只检查当前运行环境的 secret store 或用户已经批准的 Notion/AgentLens 配置中是否存在 `notion_token`；不要扫描 home 目录、通用记忆或对话历史来寻找。
3. 若有已批准的 token，先确认目标 parent 与保存模式，再使用下方 Notion API 辅助代码；若没有已批准的 token，再说明缺少项并请用户提供或连接。
4. 如果用户没有说明保存结构，先确认是保存为独立页面，还是写入 database/data source。
5. 保存标题、原始链接、平台、作者/来源、账号/Handle、发布日期、获取日期、摘要、要点、转写说明、媒体解读和原文/正文；摘要和要点放在前面，原文/正文放在页面偏下方。
6. 如果用户要求保存媒体，当前环境支持 Notion 媒体/文件块时优先使用原生 Notion 媒体能力；否则在页面正文中保留来源/媒体 URL 和准确本地文件名，不要假装兜底辅助代码已完成文件上传。
7. 保存 Notion token 前先询问用户。不要打印 token 或完整 authorization header。

缺少 Notion 目标或凭据时，可使用以下话术。可根据用户上下文适当缩短，但必须保留 token、目标 parent、保存模式和字段结构确认：

```text
我可以保存到 Notion。你希望保存为普通页面，还是写入 database/data source？

如果当前环境已经有 Notion 连接器，我可以优先使用它。如果没有，请提供：
- Notion integration token，最好通过当前环境的 secret store 提供；
- 普通页面模式下的目标父页面 ID，或 database/data source 模式下的目标 ID；
- 如果写入 database/data source，请提供标题字段名，以及你希望填写的可选字段名和字段类型。

这些信息的查找方式，以本 Skill 编写时的常见 Notion 设置为准：在 Notion 的 integration/developer 设置中创建或打开内部 integration，复制 secret；把目标页面或 database/data source 分享给这个 integration；从 Notion 目标页面或 database/data source 的链接中复制对应 ID。如果 Notion 界面已经变化，请以 Notion 最新官方 integration/API 文档为准。

除非你明确同意安全保存，否则 token 只用于本次保存。
```

#### Notion 保存模式

> **术语说明：** Notion 用户界面里可能仍称为 database；当前 Notion API 中结构化 collection parent 可能叫 `data_source`。本 Skill 面向用户时使用 “database/data source” 表达保存意图，具体实现时使用正确的 API 字段，例如 `data_source_id` 或 `database_id`。

支持两种 Notion 保存模式：

| 模式 | 适合场景 | 取舍 |
|:--|:--|:--|
| 普通页面 | 单次保存、页面内容更丰富、不想预先配置字段、媒体内容较多 | 每次都会新建一个子页面；保存很多条后，如果父页面没有整理，会比较混乱 |
| Database/data source | 长期收集、需要排序筛选、需要 tags/status/platform/source 等字段 | 需要提前准备字段，并确认标题属性；媒体较多时，正文仍建议写在创建出来的页面正文里 |

选择指引：

- 如果用户只说“保存到 Notion”，但没有指定结构，询问是要创建简单子页面，还是写入便于管理的 database/data source。
- 对单条文章、帖子或视频总结，普通页面通常最省事。
- 对重复保存、监控归档、研究资料收集、线索/客户跟踪，或之后需要排序筛选的内容，推荐 database/data source。
- 使用 database/data source 模式时，如果当前环境不能检查字段结构，询问目标 data source 和标题属性；同时询问要填写哪些可选字段，例如 `Platform`、`Source URL`、`Author`、`Handle`、`Published`、`Retrieved`、`Tags` 或 `Status`。
- 对媒体内容较多的保存，把摘要、媒体解读、转写说明和 source/media URLs 写入 Notion 页面正文。database properties 只放需要排序或筛选的信息。

字段不确定时，使用以下确认话术：

```text
你想保存为普通 Notion 页面，还是写入 database/data source？如果写入 database/data source，请提供目标 data source ID、标题字段名，以及已经存在的可选字段名和类型。字段不确定时，我建议先创建普通页面，避免因为字段结构不匹配导致写入失败。
```

#### Notion API 辅助代码

当没有原生 Notion 连接器，且用户已提供或批准使用 Notion integration token 和目标 parent 时，使用这段辅助代码。

必要输入：

- `notion_token`：来自当前环境 secret store 或用户输入的 Notion integration token。
- `parent_id`：目标父页面 id 或 data source id。Notion 用户界面中可能仍称为 database；当前 API 中结构化 collection parent 叫 data source。
- `parent_type`：`page` 表示普通页面归档，`data_source` 表示 database/data source 归档。
- `title`：页面标题。
- `content`：按上方结构生成的 markdown 内容。
- `title_property`：写入 data source 时使用的标题属性名；只有用户确认时才默认使用 `Name`。
- `extra_properties`：可选的 database/data source properties，必须与用户的字段结构匹配。

常见 `extra_properties` 示例。只有在用户确认这些字段名和类型存在后才能使用：

```python
extra_properties = {
    "Platform": {"select": {"name": "TikTok"}},
    "Source URL": {"url": "https://example.com/post"},
    "Author": {"rich_text": [{"text": {"content": "creator name"}}]},
    "Handle": {"rich_text": [{"text": {"content": "@creator"}}]},
    "Published": {"date": {"start": "2026-07-20"}},
    "Retrieved": {"date": {"start": "2026-07-21"}},
    "Tags": {"multi_select": [{"name": "social-read"}]},
    "Status": {"select": {"name": "Saved"}},
}
```

执行模式：

```text
确认 Notion 目的地、保存模式和 token 来源
 -> 普通页面模式：在所选父页面下创建子页面
 -> Database/data source 模式：在所选 data source 下创建记录页面
 -> 默认用 children paragraph blocks 写入页面正文
 -> 除非当前环境提供已验证的 Notion markdown helper，否则不要发送非标准的 "markdown" 字段
 -> 如果 API 拒绝 parent/properties，询问正确目标、标题属性或字段结构
 -> 报告创建的 page URL
```

可移植 Python 骨架：

```python
import json
import os
import urllib.error
import urllib.request

# 优先使用当前环境批准的 Notion 版本配置。兜底代码使用稳定的
# children blocks 写入页面正文。默认不要发送原始 "markdown" 字段；
# Notion 可能拒绝该字段，并在 token 有效时仍返回误导性的 401。
NOTION_VERSION = os.environ.get("NOTION_VERSION", "2022-06-28")


def _notion_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _paragraph_blocks(text, chunk_size=1900):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)] or [""]
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            },
        }
        for chunk in chunks
    ]


def _post_notion_page(notion_token, payload):
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode("utf-8"),
        headers=_notion_headers(notion_token),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        lower = detail.lower()
        if "notion-version" in lower or "version" in lower:
            raise RuntimeError(
                "Notion rejected the API version. Use a supported Notion-Version, "
                "a native Notion connector, or the children-block fallback."
            )
        raise RuntimeError(f"Notion save failed: HTTP {exc.code} {detail[:500]}")


def _build_parent_and_properties(parent_id, parent_type, title, title_property, extra_properties):
    if parent_type == "page":
        return {"page_id": parent_id}, {"title": [{"text": {"content": title[:2000]}}]}
    if parent_type == "data_source":
        prop = title_property or "Name"
        properties = {prop: {"title": [{"text": {"content": title[:2000]}}]}}
        if extra_properties:
            properties.update(extra_properties)
        return {"data_source_id": parent_id}, properties
    if parent_type == "database":
        prop = title_property or "Name"
        properties = {prop: {"title": [{"text": {"content": title[:2000]}}]}}
        if extra_properties:
            properties.update(extra_properties)
        return {"database_id": parent_id}, properties
    raise RuntimeError("parent_type must be 'page', 'data_source', or 'database'")


def create_notion_page(
    notion_token,
    parent_id,
    parent_type,
    title,
    content,
    title_property=None,
    extra_properties=None,
    prefer_markdown=False,
):
    parent, properties = _build_parent_and_properties(
        parent_id, parent_type, title, title_property, extra_properties
    )
    base_payload = {"parent": parent, "properties": properties}

    if prefer_markdown:
        try:
            result = _post_notion_page(notion_token, {**base_payload, "markdown": content})
            return result.get("url") or result.get("id")
        except RuntimeError as exc:
            message = str(exc).lower()
            can_fallback = (
                "markdown" in message
                or "body" in message
                or "validation" in message
                or "version" in message
                or "notion-version" in message
                or "unauthorized" in message
                or "token is invalid" in message
            )
            if not can_fallback:
                raise

    children = _paragraph_blocks(content)
    if len(children) > 100:
        raise ValueError(
            f"Notion content too long: {len(children)} blocks exceeds the 100-block create-page limit. "
            "Ask the user whether to save summary only, split the note, or use a native Notion connector."
        )
    result = _post_notion_page(notion_token, {**base_payload, "children": children})
    return result.get("url") or result.get("id")
```

普通页面模式下，`properties` body 只应承载页面标题。Database/data source 模式下，每个 property key 和 property 类型都必须匹配目标字段结构。不要只凭字段名猜测字段类型。如果映射后的 `select` 或 `multi_select` 值不在现有选项中，不要静默创建或修改选项：先询问用户是否允许该 schema 变更；只有用户同意后，才通过已批准的目的地能力创建该选项，否则省略这个可选字段。如果用户不知道字段结构，且没有原生 Notion 工具可以检查，询问是否改为创建简单子页面。如果 database/data source 写入因为 validation error 失败，询问正确标题属性和可选字段类型，或降级为普通页面。

### ima

当用户要求保存到 ima 时使用。

重要的视频边界：OpenAPI 兜底流程尚无已验证的独立视频 `media_type`。只有用户明确要求、且当前运行环境已验证完整 HTML 上传和 ima 内播放路径时，单个 HTML 可受限地内嵌 base64 视频。字节已内嵌时，成功播放不依赖平台 CDN URL 是否过期；但 ima 的媒体/HTML 大小上限尚未确定，且仍受 ima 正常的保留与访问规则约束。

1. 只有确认当前会话里确实暴露了可调用的原生 ima skills/tools 时，才优先使用原生工具。UI 里已连接或授权 ima，不等于当前 agent 会话一定拿得到可调用工具。
2. 如果没有可调用的原生 ima 工具，或原生工具失败，使用下方 `create_media -> COS PUT -> add_knowledge` OpenAPI 三步流程。
3. 只询问或加载当前环境中已明确批准的 ima credentials 和目标知识库。
4. 如果目标知识库不明确，写入前先确认。经用户同意后，使用当前会话的 ima/OpenAPI 知识库查询（例如 `search_knowledge_base`）列出可写知识库，让用户选择；上传前检查所选知识库是否具有可写权限。不要把分享链接 token 当作 `knowledge_base_id`。
5. 默认保存文本优先的整理稿。包含图片解读结论、原始链接和媒体引用，但不要把图片作为独立知识条目上传，除非用户明确要求。
6. 如果用户需要保留图文显示，优先使用单个 HTML 文档并内嵌 base64 图片，前提是当前环境和 ima 工作流支持。当前提供的 ima 上传器约束将 `media_type=20` 视为一个 HTML 文件，**总上限为 10 MB**：HTML 正文以及每个 `data:...;base64,...` 图片/视频共用这一个预算。base64 会使二进制体积约膨胀三分之一；上传前必须测量最终 HTML 文件并预留余量，不能把独立图片文件上限当作额外预算。HTML 里的 `<video controls>` 配合来源 URL 只作为短期预览使用；TikTok、Instagram 等平台的视频直链可能过期。用户明确要求把视频字节保留在 HTML 中时，只下载 AgentLens 返回的媒体 URL，先校验本地文件；只有最终 HTML 不超过 10 MB 且当前运行环境可上传时，才生成单个 `media_type=20` HTML。可行时必须在 ima 内检查播放。已验证播放的 base64 内嵌字节不依赖 CDN URL 过期，但仍受 ima 正常的保留与访问规则约束。已实测的 ima OpenAPI 媒体类型不包含可用的独立视频文件类型，所以除非当前运行环境明确确认有原生/视频上传路径，否则不要通过 OpenAPI 兜底流程尝试独立上传视频。当前 ima 工作流中，内嵌图片的 `.docx` 已观察到可用；PDF 需要按用户可见输出语言选择字体并通过渲染/文本校验，其中简体中文输出已观察到可通过 ReportLab `STSong-Light` CID 正常写入；不得把 docx/PDF 表述为已验证的可播放视频替代方案。

除非用户已经批准本地配置，或当前保存工作流明确要求，否则不要读取 `~/.config/ima`、`~/.agentlens` 或其他本地配置路径。

缺少 ima 凭据或目标知识库时，可使用以下话术。可根据上下文适当缩短，但必须保留凭据、目标知识库和以最新官方文档为准的说明：

```text
我可以保存到 ima。如果当前环境有原生 ima 工具，我会优先使用它。否则走 OpenAPI 兜底流程时，我需要：
- IMA_OPENAPI_CLIENTID；
- IMA_OPENAPI_APIKEY；
- 请你授权我使用当前会话的 ima/OpenAPI 查询列出可写知识库，再由你选择。

这些信息的查找方式，以本 Skill 编写时的常见 ima 设置为准：打开 https://ima.qq.com/agent-interface，登录后同一页面会给出 Client ID 和 API Key。Client ID 对应请求头 `ima-openapi-clientid`，API Key 对应请求头 `ima-openapi-apikey`。不要让你查找或粘贴 `knowledge_base_id`：在获得你的同意后，我会用当前会话的 ima/OpenAPI 知识库查询（如 `search_knowledge_base`）列出可写库，只展示供你选择所需的最少非秘密标识，并在内部使用返回的 `knowledge_base_id`。ima 的普通分享/设置链接可能包含 `shareId` 或其他分享 token，但这不是 OpenAPI 所需的 `knowledge_base_id`，绝不能传给 `create_media` 或 `add_knowledge`。如果查询不可用，我会说明 OpenAPI 兜底流程无法安全选择目的地并停止；不会让你查找 ID 或从分享链接复制。如果 ima 界面已经变化，请以最新 ima OpenAPI 文档为准。

如果内部选定的 `knowledge_base_id` 被拒绝，不要原样重试。经用户同意后，通过当前会话 ima/OpenAPI 查询刷新可写知识库列表并请用户重新选择；如果查询不可用，说明 OpenAPI 兜底流程无法安全继续并停止，绝不能向用户索要 ID 或改用分享链接 token。

请尽量通过当前环境的 secret store 提供凭据。我不会打印这些凭据；除非你明确同意安全保存，否则只用于本次保存。
```

ima 保存成功后，遵循上方“目的地设置记忆（仅在用户同意时）”。`IMA_OPENAPI_APIKEY` 属于秘密；选定的 `knowledge_base_id` 属于私密目的地元数据。不要把任一内容写进未获批准的本地文件或对话记忆。

### ima 图片处理

已验证行为：Markdown 或 note 中引用外部/COS 图片 URL 时，ima 可能无法内联渲染；单独上传图片会生成独立知识条目，且与主整理稿没有可靠索引关系。

使用以下策略：

- 默认：保存一个文本优先整理稿，包含摘要、要点、原文/正文、图片解读结论、原始链接和媒体 URL 引用；摘要和要点放在前面，原文/正文放在偏下方。
- 不要为了保存帖子摘要而批量上传图片为独立 ima 附件；这会打散知识库，并丢失图片与主整理稿的关系。
- 当 URL 需要鉴权时，不要依赖 `![](url)` 这类 Markdown 图片语法在 ima 中显示图片。
- 如果用户要求视觉保真，询问是否创建一个内嵌 base64 图片的 HTML 文档。只有当前环境能生成并上传该单一文件时才使用。
- 如果 HTML 中包含视频，使用 `<video controls preload="metadata" src="...">`，并用 CSS 限制播放器尺寸，同时保留纯文本 URL，但这只算短期预览。TikTok、Instagram 等平台返回的 CDN 视频链接可能过期；不得断言某个 CDN URL 在所有环境中都不能播放。
- 单个 `media_type=20` HTML 内嵌 base64 视频，仅在用户明确要求且当前运行环境已验证时允许作为受限例外。必须从 AgentLens 返回媒体 URL 下载本地文件后构建，不能改用特定平台的替代抓取器。按当前提供的 ima 上传器约束，包含 base64 文本在内的最终 HTML 必须不超过 10 MB。ima 内播放已验证时，内嵌字节不依赖 CDN URL 过期；仍须说明已测试的文件大小，且不得在未新增实测的情况下声称可超越这 10 MB 总包边界。
- 用户要求长期保存视频时，明确说明当前流程不能在 ima 里生成稳定、独立上传的视频归档。已实测的 ima OpenAPI 媒体类型不包含可用的视频文件类型；除非当前运行环境明确确认有原生/视频上传路径，否则不要通过 OpenAPI 兜底流程尝试独立上传视频。
- 当前 ima 工作流中，内嵌图片的 Word `.docx` 已观察到可用；如果目标环境不同，仍应尽量验证。
- 当前 ima 工作流中，PDF 内嵌图片可以可用，但前提是字体匹配用户可见输出语言，并通过下方渲染/文本校验。简体中文输出已观察到可通过 ReportLab `STSong-Light` CID 正常写入。Adobe Acrobat 和 macOS 预览可能会自动回退到本机字体，从而掩盖 PDF 内嵌字体损坏；ima/browser 阅读器可能会直接把同一个 PDF 渲染成乱码。
- 如果图文保真保存失败，保留文本优先整理稿，并提供本地 HTML/docx/PDF 导出，而不是创建多个没有关联的图片条目。

写入 ima 或其他知识库时，标题和文件名使用便于识别的格式：

```text
YYYYMMDD-HHMM-{平台}-{博主ID或unknown}-{标题或正文前10个词/字}
```

如果不知道博主 ID，用 `unknown`。最终文件名要做安全字符处理，并追加正确扩展名，例如 `.md`、`.html`、`.mp4`。如果视频作为独立文件上传，尽量和主整理稿使用同一个基础文件名，并增加 `-video-1.mp4` 这类后缀；主整理稿里必须写出这个准确文件名。

### PDF 字体校验

生成 PDF 并上传 ima 之前，必须先过这一关：

1. PDF 字体必须跟用户可见输出语言匹配。
2. 简体中文 ima PDF 优先使用 ReportLab 的 `UnicodeCIDFont("STSong-Light")` 和 `UniGB-UCS2-H` 编码。这条路径已观察到可以通过 `media_type=1` 上传并在 ima 正常渲染，Poppler 没有字体 mismatch 警告，`pdftotext` 抽取中文也正常。
3. 英文/拉丁文字 PDF 可使用标准拉丁字体或已验证的嵌入式拉丁字体。
4. 日文、韩文、繁体中文或混合语言 PDF，应选择匹配该脚本/地区的字体，或使用已验证的多语言字体，并确保 face/index 正确。
5. 如果必须为简体中文嵌入本地字体文件，使用简体中文字体，例如 `NotoSansCJKsc`、`Source Han Sans SC`、`PingFang SC` 或 `Microsoft YaHei`。
6. 不要用 `NotoSansCJKJP` 生成简体中文归档。
7. 避免用 `fpdf2` 直接注册 `.ttc` CJK 字体集合，除非能显式控制字体 face index 并完成验证。本次测试中，默认 `.ttc` 注册选中了 JP 字体，并产生嵌入字体 mismatch 警告。
8. 如果使用 WeasyPrint，确认 fontconfig 能找到目标字体，并在 CSS 中显式指定。
9. 如果使用 ReportLab 注册本地 `.ttf`/`.otf`，必须选择匹配输出语言的真实字体，并完成验证。
10. 至少用 `pdftoppm` 或等价的 Poppler 渲染器检查第一页。如果出现 `Mismatch between font type and embedded font file`，或渲染结果乱码，拒绝上传并重新生成。
11. 如果环境有 `pdffonts`，确认目标字体存在。简体中文使用 `STSong-Light` CID 时可能显示 `emb=no`；只要 Poppler 渲染无警告且文本抽取可读，可以接受。如果有 `pdftotext`，确认抽取出来的文本可读。
12. 任何一项不通过，就改用 `.docx` 或 HTML，不要把有问题的 PDF 上传到 ima。

## ima OpenAPI 辅助代码

仅当用户已经选择 ima 作为保存目的地，并确认目标知识库后，才使用这个辅助模式。这里把可执行骨架直接放在 reference 中，而不是另建 script 文件，方便 agent 根据当前环境做最小改动后执行。

### 必要输入

- `IMA_OPENAPI_CLIENTID`：ima OpenAPI client id，来自当前环境 secret store 或用户输入。
- `IMA_OPENAPI_APIKEY`：ima OpenAPI API key，来自当前环境 secret store 或用户输入。
- `knowledge_base_id`：用户选定的 ima 知识库对应的内部 ID，由查询结果提供，不由用户填写。
- `title`：整理稿或文件标题。
- `content`：markdown 文本整理稿；如果需要保留图片，则为完整 HTML 字符串。

不要打印这些凭据。用户选择 ima 作为目的地后，先询问是否允许使用当前会话 ima/OpenAPI 查询（如 `search_knowledge_base`）列出或搜索可用知识库，再让用户选择，并优先选择 `role_type` 表示可写权限的知识库。返回的 ID 只作内部请求参数，不要让用户提供。如果查询不可用，说明 OpenAPI 兜底流程无法安全选择目的地并停止；不要从分享链接推断 ID。

`knowledge_base_id` 是 ima 知识库 ID，不是 Notion database id、泛称的“Database ID”，也不是分享链接中的 `shareId`。按当前已验证 UI/API 行为，它可能看起来像 base64 字符串，末尾可能带 `=`。只能在用户选定可写库后，从已获授权的当前会话 ima/OpenAPI 查询结果中取得。如果 `create_media` 返回 `invalid knowledge_base_id`，不要原样重试；经用户同意后，刷新可写知识库列表并让用户重新选择。如果查询不可用，说明 OpenAPI 兜底流程无法安全继续并停止；绝不能向用户索要 ID 或改用分享链接 token。

### 媒体类型

用能满足用户意图的最窄文件类型：

| 内容 | `media_type` | MIME | 扩展名 |
|:--|:--|:--|:--|
| 文本优先 Markdown 整理稿 | `7` | `text/markdown` | `md` |
| 保留图片的 HTML | `20` | `text/html` | `html` |
| Word 文档 | `3` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | `docx` |
| PDF | `1` | `application/pdf` | `pdf` |
| 独立视频文件 | 已实测的 ima OpenAPI 兜底流程不支持；只有当前运行环境明确确认有原生/视频上传路径时才使用 | 取决于来源，例如 `video/mp4` | `mp4` 或来源扩展名 |

如果当前环境有原生 ima note 工具，保存为 ima note 时优先使用原生工具。下方 OpenAPI 兜底代码只实现 Markdown (`7`) 和 HTML (`20`)。已实测 ima OpenAPI 接受 Markdown (`7`)、HTML (`20`)、Word (`3`) 和 PDF (`1`)，但未找到可用的视频 `media_type`。如果当前运行环境不能确认支持原生/视频上传路径，应告诉用户长期视频保存需要在当前自动化 ima 流程之外处理。

### 上传顺序

```text
在内存或 /tmp 中构建一个文件
 -> POST /openapi/wiki/v1/create_media，提交文件元数据和 media_type
 -> 从响应中读取 media_id 和 cos_credential
 -> 使用返回的临时凭证，把同一份 bytes PUT 到腾讯云 COS
 -> POST /openapi/wiki/v1/add_knowledge，提交 media_id、media_type、title 和 knowledge_base_id
 -> 告知用户保存目的地和标题
```

`create_media` 返回的 COS credential 是临时且仅针对当前文件有效的。不要要求用户单独提供 COS key。不要虚构简化版 COS authorization header；腾讯云 COS PUT 需要 SDK 签名或合法的 HMAC-SHA1 authorization string，并且必须传 `x-cos-security-token`。

### COS Endpoint 解析与受限恢复

- 当前 ima/COS 合约返回明确 endpoint 时，优先使用该 endpoint；否则先使用凭证中 bucket/region 对应的默认 endpoint。
- 已开启腾讯云 COS 全球加速的 bucket 可能需要全球加速 endpoint（`{bucket}.cos.accelerate.myqcloud.com`），但这是 bucket 级条件；不得把它硬编码为所有 ima 上传的通用域名，也不得改用无关的 CDN/share 域名。
- 已选 endpoint 出现 DNS 或 `403` 失败时，先报告上传失败。只有 bucket 已确认支持全球加速时，才允许立即用加速 endpoint 重试一次；新 `Host` 必须重新计算 COS authorization，绝不能复用前一个 endpoint 的签名。
- 用户要求完整文件/HTML 上传时，不得静默降级为 `import_urls` 一类的仅来源链接条目。必须说明结果已降级并征求同意。临时凭据过期时，从 `create_media` 重新开始，并无间隔完成三步。
- 三步中的 `media_type` 必须一致：HTML 为 `20`，Markdown 为 `7`；不得把 HTML 标成 Markdown。

### 可移植 Python 骨架

如果当前环境有原生 ima 工具，优先使用原生工具。如果没有，可改造下面的 Python 骨架。它只使用标准库，并包含第二步 COS 上传所需的手动签名。

```python
import hashlib
import hmac
import json
import re
import time
import urllib.parse
import urllib.request
from http.client import HTTPSConnection

IMA_API = "https://ima.qq.com"


def _ima_headers(client_id, api_key):
    return {
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json",
    }


def _safe_part(value, fallback="unknown", limit=80):
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value or "", flags=re.UNICODE)
    text = text.strip(".-")
    return (text or fallback)[:limit]


def archive_basename(platform, author_or_handle, title_or_text, timestamp=None):
    timestamp = timestamp or time.time()
    date_part = time.strftime("%Y%m%d-%H%M", time.localtime(timestamp))
    words = re.findall(r"[\w\u4e00-\u9fff]+", title_or_text or "", flags=re.UNICODE)
    if re.search(r"[\u4e00-\u9fff]", title_or_text or ""):
        summary_part = "".join(words)[:10]
    else:
        summary_part = "-".join(words[:10])
    return "-".join([
        date_part,
        _safe_part(platform, limit=32),
        _safe_part(author_or_handle, limit=48),
        _safe_part(summary_part, fallback="untitled", limit=80),
    ])


def _post_json(url, headers, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    code = body.get("code", body.get("retcode", 0))
    if code not in (0, "0", None):
        raise RuntimeError(body.get("msg") or body.get("errmsg") or "ima API request failed")
    return body.get("data", body)


def create_media(client_id, api_key, knowledge_base_id, file_name, content_type, media_type, file_bytes):
    payload = {
        "media_type": media_type,
        "file_name": file_name,
        "file_size": len(file_bytes),
        "content_type": content_type,
        "knowledge_base_id": knowledge_base_id,
        "file_ext": file_name.rsplit(".", 1)[-1],
    }
    return _post_json(f"{IMA_API}/openapi/wiki/v1/create_media", _ima_headers(client_id, api_key), payload)


def get_addable_knowledge_bases(client_id, api_key, limit=20):
    payload = {"cursor": "", "limit": limit}
    data = _post_json(
        f"{IMA_API}/openapi/wiki/v1/get_addable_knowledge_base_list",
        _ima_headers(client_id, api_key),
        payload,
    )
    return data.get("addable_knowledge_base_list") or data.get("list") or []


def assert_cos_credential(cos_credential):
    required = ["bucket_name", "region", "cos_key", "secret_id", "secret_key", "token"]
    missing = [key for key in required if not cos_credential.get(key)]
    if missing:
        raise RuntimeError(
            "ima create_media response is missing COS credential fields: "
            + ", ".join(missing)
            + ". Re-check the ima OpenAPI response shape or use a native ima/COS SDK helper."
        )


def _sha1_hex(value):
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha1(value).hexdigest()


def _hmac_sha1_hex(key, value):
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hmac.new(key, value, hashlib.sha1).hexdigest()


def _cos_auth(secret_id, secret_key, method, pathname, headers, start_time, expired_time):
    key_time = f"{start_time};{expired_time}"
    sign_key = _hmac_sha1_hex(secret_key, key_time)
    lowered = {k.lower(): str(v) for k, v in headers.items()}
    keys = sorted(lowered.keys())
    header_string = "&".join(
        f"{k}={urllib.parse.quote(lowered[k], safe='')}" for k in keys
    )
    http_string = f"{method.lower()}\n{pathname}\n\n{header_string}\n"
    string_to_sign = f"sha1\n{key_time}\n{_sha1_hex(http_string)}\n"
    signature = _hmac_sha1_hex(sign_key, string_to_sign)
    return "&".join([
        "q-sign-algorithm=sha1",
        f"q-ak={secret_id}",
        f"q-sign-time={key_time}",
        f"q-key-time={key_time}",
        f"q-header-list={';'.join(keys)}",
        "q-url-param-list=",
        f"q-signature={signature}",
    ])


def upload_to_cos(cos_credential, file_bytes, content_type):
    assert_cos_credential(cos_credential)
    bucket = cos_credential["bucket_name"]
    region = cos_credential["region"]
    cos_key = cos_credential["cos_key"]
    host = f"{bucket}.cos.{region}.myqcloud.com"
    pathname = "/" + urllib.parse.quote(cos_key, safe="/-_.~")
    now = int(time.time())
    start_time = int(cos_credential.get("start_time") or now - 60)
    expired_time = int(cos_credential.get("expired_time") or now + 1800)
    headers = {
        "content-length": str(len(file_bytes)),
        "content-type": content_type,
        "host": host,
        "x-cos-security-token": cos_credential["token"],
    }
    headers["authorization"] = _cos_auth(
        cos_credential["secret_id"],
        cos_credential["secret_key"],
        "put",
        pathname,
        headers,
        start_time,
        expired_time,
    )
    conn = HTTPSConnection(host, timeout=120)
    conn.request("PUT", pathname, body=file_bytes, headers=headers)
    resp = conn.getresponse()
    detail = resp.read().decode("utf-8", errors="replace")
    if resp.status not in (200, 201):
        if resp.status in (401, 403):
            raise RuntimeError(
                f"COS upload authorization failed: HTTP {resp.status}. "
                "Check temporary credential fields, x-cos-security-token, signing time, and COS key. "
                f"Detail: {detail[:300]}"
            )
        raise RuntimeError(f"COS upload failed: HTTP {resp.status} {detail[:300]}")


def add_knowledge(client_id, api_key, knowledge_base_id, media_id, media_type, title):
    payload = {
        "knowledge_base_id": knowledge_base_id,
        "media_id": media_id,
        "media_type": media_type,
        "title": title,
    }
    return _post_json(f"{IMA_API}/openapi/wiki/v1/add_knowledge", _ima_headers(client_id, api_key), payload)


def save_to_ima(
    client_id,
    api_key,
    knowledge_base_id,
    title,
    content,
    *,
    as_html=False,
    platform="unknown",
    author_or_handle="unknown",
    related_video_filenames=None,
):
    base_name = archive_basename(platform, author_or_handle, title)
    if as_html:
        file_name = f"{base_name}.html"
        content_type = "text/html"
        media_type = 20
    else:
        file_name = f"{base_name}.md"
        content_type = "text/markdown"
        media_type = 7
    if related_video_filenames:
        file_list = "\n".join(f"- {name}" for name in related_video_filenames)
        content += (
            "\n\n## 独立上传的视频文件\n\n"
            "ima 可能无法长期保持平台 CDN 视频链接可播放。相关视频已作为独立知识条目上传：\n\n"
            f"{file_list}\n"
        )
    file_bytes = content.encode("utf-8")
    created = create_media(client_id, api_key, knowledge_base_id, file_name, content_type, media_type, file_bytes)
    media_id = created["media_id"]
    cos_credential = created["cos_credential"]
    upload_to_cos(cos_credential, file_bytes, content_type)
    return add_knowledge(client_id, api_key, knowledge_base_id, media_id, media_type, title)
```

如果要在 ima 中保留图片，把 `content` 构造成完整 HTML 文档，并把图片写成 `data:image/...;base64,...` URL。除非用户明确想要独立图片条目，否则不要把这些图片另外上传为 ima image media。视频不要默认 base64 内嵌；受控播放器只作为短期预览。长期保存时，除非当前运行环境确认支持原生/视频上传路径，否则不要通过 OpenAPI 兜底流程上传视频；应在整理稿里写清来源 URL、过期风险和用户提供的本地文件名：

```html
<style>
  .agentlens-video {
    width: min(100%, 720px);
    max-height: 420px;
    aspect-ratio: 16 / 9;
    object-fit: contain;
    background: #111;
    display: block;
  }
  .agentlens-video.vertical {
    width: min(100%, 360px);
    max-height: 640px;
    aspect-ratio: 9 / 16;
  }
</style>
<video class="agentlens-video" controls preload="metadata" src="{video_source_url}"></video>
<p><a href="{video_source_url}">Original video link</a> (may expire)</p>
<p>长期保存的视频文件没有嵌入本 ima 笔记。用户提供的本地/参考文件名：{exact_video_filename}</p>
```

## 保存失败策略

知识库写入不同于 AgentLens API fetch 重试。失败的写入可能已经部分成功，因此不要盲目重复写入。

如果保存失败：

1. 在当前响应中保留已准备好的 markdown 整理稿。
2. 用用户能理解的语言解释失败原因，不打印凭据或完整 auth headers。
3. 除非用户要求，否则不要重试超过 1 次。
4. 如果当前环境提供足够信息，重试前先检查目的地是否已包含该项目。
5. 如果是认证或权限错误，请用户刷新凭据或选择其他目的地。
6. 如果目标 database、page、vault、folder 或 knowledge base 不存在，请用户选择有效目标。
7. 如果内容过长或超过 block/file 限制，提供只保存摘要、拆分成多篇笔记，或保存为本地 Markdown。
8. 如果是重复或冲突，询问用户重命名、覆盖、合并还是跳过。
9. 如果外部服务仍不可用，提供把已准备 markdown 整理稿保存为本地文件或直接返回在聊天中的选项。

常见处理：

| 失败类型 | 处理方式 |
|:--|:--|
| 认证失败/未授权 | 请用户刷新凭据或选择其他目的地 |
| Permission denied | 请用户授权访问或选择可写目标 |
| Target not found | 请用户确认 database/page/vault/folder/KB |
| 限流/超时 | 提供一次重试，然后提供保存为本地 Markdown |
| 内容过长 | 提供只保存摘要或拆分保存 |
| 重复/冲突 | 询问重命名、覆盖、合并或跳过 |
| 不确定是否部分成功 | 不要盲目重试；询问用户是否检查目的地或保存到本地 |

## 完成消息

保存后，报告：

- 目的地名称。
- 条目标题和原始来源。
- 任何影响已保存整理稿的媒体或转写限制。

不要打印凭据、完整 authorization headers 或完整 API responses。
