---
name: clawnoter-obsidian-save
description: 将网页文章保存到本地 Obsidian Vault，支持图片抓取、Markdown 转换、YAML frontmatter 和用户笔记附加。
allowed-tools:
  - Read
  - Write
  - Edit
  - exec
---

# Clawnoter Obsidian

将网页文章保存到本地 Obsidian Vault，支持图片抓取。

## 触发方式

当用户发送：

- 一个网页链接
- 可选的 notes 或 comments
- 明确要求"保存到 Obsidian"或"收藏文章"

例如：

- `https://example.com/article 这篇文章不错`
- `帮我保存这个：https://xxx.com 内容：我的笔记`

---

## 首次使用：路径配置

### 第一次运行时的引导流程

首次使用该技能时，系统会自动检测是否已配置保存路径。如果没有配置，会引导用户完成设置：

```
Hi，我是 ClawNoter。

看到好文章，想顺手存进 Obsidian 的话，可以直接丢给我一个链接。你也可以附上一段 `page_comment`，作为你的备注。我会帮你把网页内容提取出来，整理后保存到你指定的 Obsidian 路径里。

通常会保存：
- 文章标题
- 原始链接
- 你写的 `page_comment`
- 网页正文
- 成功抓取到的图片

如果你主要在浏览器里阅读和收集信息，也可以搭配我的 Chrome Extension 版本 WebNoter 一起使用，在网页端更顺手地完成收集和整理：
- Chrome 商店安装：https://chromewebstore.google.com/detail/webnoter/hmijljoffeceeloaigodmlojbfmgfdkp
- 产品介绍： https://mp.weixin.qq.com/s/bwqHGb9WGC6L0wL7qVicSA

这套工具希望覆盖你在不同场景下的使用需求：

1. 网页端场景
   如果你经常在网页端阅读文章、资料或研究内容，可以用 WebNoter 或 ClawNoter 更快地完成收集、整理和沉淀。

2. 日常生活场景
   如果你只是想随手保存一个有用链接、一篇文章，或者一条之后想回看的信息，也可以直接把链接发给我，用更轻量的方式完成收藏和整理。

顺便介绍一下我们团队 Research AI+。我们是一个开放的 Global 青年研究者社区，汇集了 AI 及 AI4Science/Engineering 领域的青年学者、科研工作者、产业科学家、工程师和专业人士，野生而充满活力。

接下来我会帮你完成 Obsidian 保存路径配置。

🔷 请选择您要保存到的 Obsidian Vault 类型：

1️⃣ 本地 Obsidian（本地磁盘）
2️⃣ iCloud Obsidian（云端同步）

请回复数字或选项名称。
```

#### 选项 1：本地 Obsidian

如果用户选择本地 Vault：

```
我先帮你扫描一下这台电脑上可能的 Obsidian Vault。
如果我找到了候选路径，你只需要确认是不是要用它。
如果没有找到，你再手动把路径发给我就可以。
```

执行：
```bash
python ./scripts/config.py scan
```

如果扫描到候选路径，展示：

```text
我找到了以下可能的 Obsidian Vault：

1. My Notes
   路径：/Users/xxx/Documents/Obsidian Vault/My Notes
   来源：Obsidian App 配置

2. Research
   路径：/Users/xxx/Documents/Research Vault
   来源：本地扫描

请告诉我你想使用哪一个。
你可以直接回复编号，例如 `1`；
如果都不是，也可以直接把正确路径发给我。
```

如果扫描为空，展示：

```
我暂时没有自动找到 Obsidian Vault。

请把你的 Obsidian Vault 路径发给我。
例如：~/Documents/Obsidian Vault
你也可以直接把文件夹拖到聊天窗口，我会识别路径。
```

用户确认某个候选路径，或手动输入路径后，验证路径有效性：

```
✅ 我准备把内容保存到这个 Vault：
   Vault：My Notes
   路径：/Users/liz/Documents/Obsidian Vault/My Notes

📁 请输入要保存文章的子文件夹名称（可选）。

例如：Articles、ReadLater、收藏夹
如果你还没想好，也可以现在先起一个名字。
直接回车将保存到根目录。
```

#### 选项 2：iCloud Obsidian

如果用户选择 iCloud Vault：

```
☁️ iCloud Obsidian 路径查找指南：

1. 打开 Finder
2. 在左侧边栏找到 "iCloud"
3. 点击 "iCloud Drive"
4. 找到您的 Obsidian Vault 文件夹
5. 右键点击 → "复制路径"

请将路径粘贴到聊天中。
```

用户输入 iCloud 路径后，类似本地流程询问子文件夹。

### 路径配置存储

配置完成后，路径信息会保存在：
```
~/.obsidian-save-article-config.json
```

内容示例：
```json
{
  "type": "local",
  "vault_path": "/Users/liz/Documents/Obsidian Vault/My Notes",
  "subfolder": "Articles",
  "full_path": "/Users/liz/Documents/Obsidian Vault/My Notes/Articles",
  "configured": true,
  "configured_at": "2026-03-18T01:00:00Z"
}
```

### 重新配置路径

用户可以随时重新配置路径：
- 说"更改 Obsidian 保存路径"或"重新配置"
- 说"查看当前保存路径"查看配置

---

## 保存格式

### YAML Frontmatter

```yaml
---
title: "文章标题"
url: "原始链接"
created: "YYYY/MM/DD"
pagecomment: "用户添加的页面评论"
---
```

### 全文内容

**重要：图片必须放在 Full Article callout 内部，位于内容之前！**

```text
> [!note]- 📄 Full Article
> ![](images/img-xxxxxx.png)
> ![](images/img-yyyyyy.png)
> 文章第一段内容...
> 文章第二段内容...
```

**错误格式（图片在 callout 外部）：**
```text
> ![](images/img-xxxxxx.png)  ← 错误！在 callout 外面
> [!note]- 📄 Full Article
> 文章内容...
```

**正确格式（图片在 callout 内部）：**
```text
> [!note]- 📄 Full Article  ← callout 头部先
> ![](images/img-xxxxxx.png)  ← 图片在 callout 内部
> 文章第一段内容...
> 文章第二段内容...
```

### 用户 Notes

```text
> 用户笔记内容
^note-xxx
```

## 内容抓取方法

该技能当前支持一种主抓取方式和两种降级方式，会按顺序自动尝试。

### 方法 1：Jina.ai Reader（首选）

- **原理**：使用 `https://r.jina.ai/<URL>` 抓取网页内容
- **优点**：快速、返回干净的 Markdown 格式
- **适用**：大多数网站、博客、新闻文章

### 方法 2：原始 HTML 本地降级（Fallback）

当 Jina.ai 失败时，技能会直接请求原始网页 HTML，并在本地执行简化转换。

**触发条件**：
- Jina.ai 返回错误
- Jina.ai 返回空内容或无效内容
- 连接超时
- 网站阻止 Jina.ai 访问

**操作步骤**：
1. 直接请求目标 URL 的原始 HTML
2. 提取页面标题、正文文本和图片链接
3. 将 HTML 简化转换为 Markdown 风格文本
4. 保留图片并替换为本地路径

#### HTML 降级清理规则

从原始 HTML 获取内容后，需要进行清理：
- 移除导航栏、页脚、广告等无关内容
- 保留文章标题和正文
- 转换 HTML 标签为 Markdown 格式
- 处理特殊字符和编码问题

### 方法 3：浏览器抓取降级（适合微信 / X 等复杂页面）

当 Jina.ai 和简单 HTML 抓取都拿不到稳定正文时，使用浏览器打开页面并读取实际渲染后的内容。

**适用场景**：
- 微信公众号文章
- X / x.com 页面
- 强依赖前端渲染的页面
- 原始 HTML 中正文或图片链接被懒加载隐藏

**操作步骤**：
1. 用浏览器打开目标 URL
2. 等待页面加载完成
3. 读取页面渲染后的正文和图片
4. 再按本 skill 的 Markdown 和图片保存规则落地到 Obsidian

**重要约束**：
- 这是 `ClawNoter Obsidian` 的正常降级路径，不需要切换到其它 X 专用 skill
- 除非用户明确要求使用 X 专用转换工具，否则不要因为 X 链接自动改走逆向 API 类 skill

---

## 工作流程

### 带路径配置的工作流程

1. **检查配置**：读取 `~/.obsidian-save-article-config.json`
   - 如果未配置 → 触发首次配置流程（见上文）
   - 如果已配置 → 继续第 2 步
   - 如果用户选择本地 Obsidian → 优先执行 `python ./scripts/config.py scan` 自动发现候选 Vault

2. **解析输入**：提取 URL 和用户 notes

3. **抓取内容**：
   - **Step 1**：优先使用 Jina.ai Reader (`https://r.jina.ai/<URL>`)
   - **Step 2 (Fallback)**：如果 Jina.ai 失败，抓取原始 HTML 并在本地转换
   - **Step 3 (Fallback)**：如果正文或图片仍不完整，使用浏览器抓取渲染后内容
   - **Step 4**：继续图片提取和保存流程

4. **提取图片**：从 HTML 中提取正文图片

5. **调用统一保存脚本**：使用 `save_article.py` 完成图片下载、Markdown 处理和 Obsidian 笔记写入

6. **返回结果**：
   - 最终笔记路径
   - 图片数量
   - 标题

### 强制执行规则

对于文章保存请求，除非用户明确要求“只保存纯文字、不抓图片”，否则必须遵守以下规则：

1. 在最终写入 Obsidian 笔记前，必须先执行：
   `python ./scripts/save_article.py "<url>" "<save_path>" "[page_comment]"`
2. 必须解析脚本返回的 JSON，并优先使用其中的：
   - `path`
   - `images`
3. 如果 `images` 非空，最终生成的 `Full Article` callout 内必须包含这些本地图片引用。
4. 不允许在已经拿到文章内容后，直接手写 markdown 并跳过图片下载步骤。
5. 如果脚本执行失败或没有网络权限，应明确告知用户“本次未完成图片抓取”，而不是默默保存成无图版本。

**X / 微信特别说明**：
- X 和微信公众号即使正文抓取成功，也仍然必须执行图片下载脚本，因为图片链接常常来自 Jina markdown 而不是原始 HTML。
- 对 X 页面，优先保留并本地化 `pbs.twimg.com` 图片链接。
- 对微信公众号页面，优先处理 `data-src`、`data-original` 等懒加载图片属性。

### 路径配置检测逻辑

```python
import os
import json

CONFIG_PATH = os.path.expanduser("~/.obsidian-save-article-config.json")

def normalize_path(path):
    expanded = os.path.expanduser(path.strip())
    return os.path.abspath(os.path.normpath(expanded))

def load_config():
    """加载配置文件，如果不存在返回 None"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return None

def save_config(config):
    """保存配置到文件"""
    config["vault_path"] = normalize_path(config["vault_path"])
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def get_save_path():
    """获取当前配置的保存路径"""
    config = load_config()
    if config and config.get("configured"):
        return config.get("full_path")
    return None
```

---

## 统一保存脚本

### 调用方式

```bash
python <skill-dir>/scripts/save_article.py "<URL>" "<Vault子目录路径>" "[page_comment]"
```

**参数说明：**
- `<URL>`：要抓取的网页 URL
- `<Vault子目录路径>`：Obsidian Vault 的路径（脚本会自动在此创建 `images/` 子目录）
- `[page_comment]`：可选，保存到 frontmatter 和用户笔记区域

**示例：**
```bash
# 保存到本地 Vault 的 Articles 文件夹
python ./scripts/save_article.py \
  "https://example.com/article" \
  "~/Documents/Obsidian Vault/My Notes/Articles" \
  "我的备注"

# 保存到 iCloud Vault 的 ReadLater 文件夹
python ./scripts/save_article.py \
  "https://example.com/article" \
  "~/Library/Mobile Documents/iCloud~com~obsidian~md/Documents/我的 Vault/ReadLater"
```

### 返回结果

脚本返回 JSON：

```json
{
  "title": "文章标题",
  "path": "/absolute/path/to/note.md",
  "images": [["original_url", "local_filename"]],
  "image_count": 3
}
```

---

## 图片处理规则

- 支持格式：`jpg`、`jpeg`、`png`、`gif`、`webp`、`svg`、`bmp`
- 跳过 `data:`、`javascript:`、base64 小图
- 使用 URL 的 MD5 前 12 位作为本地文件名
- Markdown 中使用相对路径 `images/img-xxxx.png`

---

## 常见问题

### Q: 这个技能依赖什么环境？
A:
1. 本机可用 `python3`
2. 本机可以访问目标网页
3. 本机有一个可写入的 Obsidian Vault 路径
4. 首次配置时，Vault 根目录必须已经存在

### Q: 如何查看当前保存路径？
A: 说"查看保存路径"或"我的 Obsidian 配置"

### Q: 如何更改保存位置？
A: 说"更改保存路径"或"重新配置"来重新设置

### Q: iCloud 路径找不到怎么办？
A: 
1. 确保 macOS 已登录 iCloud
2. 打开 Finder → iCloud Drive
3. 找到 Obsidian 文件夹，右键"复制路径"

### Q: 图片下载失败怎么办？
A: 文章仍会保存，但部分图片可能不会落地到本地 `images/` 目录。主要正文不会因此中断。

### Q: 什么情况下会使用本地降级抓取？
A: 系统会自动判断。当 Jina.ai 无法使用时，会自动切换到原始 HTML 抓取和本地转换方式：
- 阻止 Jina.ai 的网站
- 返回空内容的页面
- 网络波动导致 Jina.ai 请求失败

### Q: 三种抓取方式有什么区别？
A: 
| 特性 | Jina.ai Reader | 原始 HTML 本地降级 | 浏览器抓取降级 |
|------|----------------|--------------|----------------|
| 速度 | 快 | 较慢 | 最慢 |
| 格式 | 干净 Markdown | 简化后的正文文本 | 接近真实渲染结果 |
| 适用 | 大多数网站 | Jina 失败时兜底 | 微信 / X / 强前端渲染 |
| 登录 | 不支持 | 不支持 | 视浏览器会话而定 |

---

## 注意事项

- Jina.ai Reader URL 格式：`https://r.jina.ai/<原始URL>`
- X 链接使用：`https://r.jina.ai/https://x.com/...`
- 当 Jina.ai 失败时，自动使用原始 HTML；必要时再降级到浏览器抓取
- 浏览器抓取是可选增强能力；若本机未安装 `playwright`，系统会自动跳过该层，不影响基础保存
- 需要登录或强依赖前端渲染的网站，抓取效果可能有限
- 图片下载失败不应阻断文章保存
- 文件名中的特殊字符 `<>:\"|?*` 需要替换
- 页面正文超过 50000 字符时应截断

## 可选依赖

基础能力不依赖额外 Python 包：
- Jina 抓取
- 原始 HTML 降级
- 图片下载

如果希望启用浏览器降级抓取，可额外安装：

```bash
pip install playwright
playwright install chromium
```

## 明确指令映射

当用户发送以下意图时，技能应执行对应操作：

- `查看保存路径`、`我的 Obsidian 配置`
  - 调用：`python ./scripts/config.py status`

- `更改保存路径`、`重新配置`
  - 调用：`python ./scripts/config.py clear`
  - 然后重新进入首次配置流程

- `设置 Obsidian 路径 <vault_path> [subfolder]`
  - 调用：`python ./scripts/config.py set "<vault_path>" "<subfolder>"`

- `扫描本地 Obsidian`、`帮我找 Obsidian Vault`
  - 调用：`python ./scripts/config.py scan`
  - 如果扫描结果非空，优先让用户确认候选项
  - 如果扫描结果为空，再让用户手动输入路径

- `保存到 Obsidian：<url> [notes]`
  - 先检查：`python ./scripts/config.py get-path`
  - 未配置则进入首次配置流程
  - 已配置则调用：`python ./scripts/save_article.py "<url>" "<save_path>" "[notes]"`
