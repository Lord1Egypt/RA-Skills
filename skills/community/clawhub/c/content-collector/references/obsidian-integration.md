# Obsidian 集成(CLI + 同步规范)

## Obsidian CLI 集成

### 概述
使用 Obsidian CLI(`obsidian` 命令)直接操作 KaiVault,替代手动写文件。CLI 通过 IPC 连接运行中的 Obsidian App,写入后自动触发索引更新。

### 可用性检测与降级
每次收藏操作开始时,先检测 CLI 是否可用:
```bash
obsidian vault 2>/dev/null
```
- 返回 vault 信息 → CLI 可用,使用 CLI 写入
- 返回错误或超时 → Obsidian 未运行,**降级到直接写文件**(原有方式,写入 `<YOUR_OBSIDIAN_VAULT>/收藏/` 目录)

降级对用户无感,不需要提示。CLI 可用时优先用 CLI。

### 收藏前去重
在执行收藏流程之前,先用 CLI 搜索是否已收藏过:
```bash
obsidian search query="<domain/path>" total
```
- ⚠️ **去掉 `https://` 前缀**,只搜域名+路径(`https:` 会被 Obsidian 解析为操作符报错)
- 同时去掉 query params(`?utm_*` 等)
- 返回 > 0 → 已收藏,告知用户「📌 已存在:<标题>(之前已收藏过)」,不重复收藏
- 返回 0 → 继续收藏流程

CLI 不可用时降级到 `grep -rl "<url>" collections/`。

### CLI 写入 Obsidian
收藏文件写入 `collections/` 后,用 CLI 同步到 Obsidian(替代直接写文件):

```bash
# 创建笔记
obsidian create path="收藏/{中文目录}/{标题}.md" content="<完整内容>" overwrite

# 设置 frontmatter 属性
obsidian property:set path="收藏/{中文目录}/{标题}.md" name="aliases" value="[{title}]" type=list
obsidian property:set path="收藏/{中文目录}/{标题}.md" name="tags" value="[tag1,tag2]" type=list
obsidian property:set path="收藏/{中文目录}/{标题}.md" name="url" value="{url}" type=text
obsidian property:set path="收藏/{中文目录}/{标题}.md" name="source" value="{source}" type=text
obsidian property:set path="收藏/{中文目录}/{标题}.md" name="date_collected" value="{date}" type=date
```

**实际操作时**:优先用 `obsidian create` 一次性写入完整内容(含 frontmatter YAML 头),减少多次 CLI 调用。`property:set` 仅在需要**追加或修改**已有笔记属性时使用。

### Daily Note 联动
每次收藏成功后,追加一条记录到当天的 Daily Note:
```bash
obsidian daily:append content="- 📌 收藏了 [[{标题}]]({source})| {一句话摘要}"
```
CLI 不可用时跳过此步(不阻塞收藏流程)。

---

## Obsidian 同步规范

**优先使用 Obsidian CLI**(见上方)。CLI 不可用时降级到以下直接写文件方式。

每次写入 `collections/` 后,**必须**同时写入 Obsidian 版本。步骤:

1. 从刚写入的收藏文件读取 frontmatter
2. 构建 Obsidian 版本:
   - 保留 frontmatter 的 `title, source, url, author, date_published, date_collected, category, language, summary, duration, platform, bvid, tags`
   - 添加 `aliases: [title]`
   - 正文第一行加 `#tag1 #tag2 ...`(标签中的空格替换为 `_`)
3. 文件名 = `sanitize(title).md`(去掉 `<>:"/\|?*`,截断 80 字符)
4. 写入到 `<YOUR_OBSIDIAN_VAULT>/收藏/{中文目录}/`

### 目录映射
| collections 目录 | Obsidian 目录 |
|---|---|
| articles/ | 文章/ |
| videos/ | 视频/ |
| tweets/ | 推文/ |
| wechat/ | 公众号/ |
| ideas/ | 想法/ |

**注意**:Obsidian 版本是 collections 的只读镜像。编辑应在 collections 原文件上进行,然后重新同步。
