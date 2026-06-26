---
name: Amber_Url_to_Markdown
description: 智能 URL 转 Markdown 工具（V4.0 可扩展架构）。**支持自动触发 Hook**，当用户发送 URL 链接时自动抓取内容并转换为 Markdown 格式。采用可扩展的分类处理架构，支持豆包、微信公众号、知乎、掘金等网站。
---

# Amber Url to Markdown

智能 URL 转 Markdown 工具，支持微信公众号、知乎、掘金、CSDN、GitHub、Medium 等 7+ 网站类型。

## 🚀 自动触发（V3.1 新增）

**安装技能后，启用 Hook 即可实现真正的自动触发！**

### 启用自动触发 Hook

```bash
# 1. 查看可用 Hook
openclaw hooks list

# 2. 启用 url-auto-fetch Hook
openclaw hooks enable url-auto-fetch

# 3. 检查 Hook 状态
openclaw hooks check
```

**启用后，当用户发送以下消息时会自动抓取：**

1. **纯 URL 消息**：
   ```
   https://mp.weixin.qq.com/s/xxx
   ```

2. **URL + 意图关键词**：
   ```
   帮我把这篇文章转成 Markdown：https://mp.weixin.qq.com/s/xxx
   解析这个链接：https://zhuanlan.zhihu.com/p/xxx
   ```

### Hook 工作原理

- 监听 `message:received` 事件
- 自动检测消息中的 URL 链接
- 判断是否为纯 URL 或包含意图关键词
- 自动调用 `amber_url_to_markdown.py` 脚本
- 异步执行，不阻塞消息处理

---

## 🎯 手动触发（AI 调用）

**如果未启用 Hook，AI 会在检测到以下条件时主动调用此技能：**

1. **纯 URL 消息** - 用户只发送了一个 URL 链接
   ```
   https://mp.weixin.qq.com/s/xxx
   ```

2. **URL + 意图关键词** - 消息包含 URL 且有以下关键词：
   - 解析、转换、转成、转为、生成、抓取、爬取、下载
   - markdown、md、文章、内容
   ```
   帮我把这篇文章转成 Markdown：https://mp.weixin.qq.com/s/xxx
   解析这个链接：https://zhuanlan.zhihu.com/p/xxx
   ```

**AI 行为约定：** 检测到上述条件时，自动执行脚本 `python3 scripts/amber_url_to_markdown.py <URL>` 并报告结果。

## 核心功能

- **智能识别**：自动识别链接类型，使用最优抓取策略
- **多网站支持**：支持微信公众号、知乎、掘金、CSDN、GitHub、Medium 等
- **图片下载**：自动下载所有图片到本地 images 目录
- **完整格式**：保留完整的 Markdown 格式，包括标题、列表、代码块等
- **自动降级**：三种抓取方案确保成功率（Playwright → Scrapling → API）

## 📦 安装

### 1. 安装技能

```bash
# 从 ClawHub 安装
clawhub install amber-url-to-markdown

# 或手动克隆
git clone https://github.com/OrangeViolin/amber-url-to-markdown.git
```

### 2. 安装依赖

```bash
# 安装核心 Python 库
pip install playwright beautifulsoup4 markdownify requests scrapling html2text

# 安装 Playwright 浏览器（必需）
playwright install chromium
```

### 3. 启用自动触发 Hook（可选但推荐）

```bash
# 查看可用 Hook
openclaw hooks list

# 启用 url-auto-fetch Hook
openclaw hooks enable url-auto-fetch

# 重启 Gateway
openclaw gateway restart
```

**启用 Hook 后，用户发送 URL 时会自动抓取，无需 AI 手动调用！**

## 使用方式

### 飞书聊天（推荐）

**AI 会自动识别并抓取**，以下两种方式都会触发：

1. **纯 URL 消息**（AI 会自动识别）：
   ```
   https://mp.weixin.qq.com/s/xxx
   ```

2. **URL + 意图说明**（更明确）：
   ```
   帮我把这篇文章转成 Markdown：https://mp.weixin.qq.com/s/xxx
   解析这个链接：https://zhuanlan.zhihu.com/p/xxx
   ```

**AI 行为约定：** 当检测到纯 URL 或 URL+ 意图关键词时，自动执行脚本并报告结果。

### 命令行

```bash
python3 scripts/amber_url_to_markdown.py <URL>
```

### Python 调用

```python
from amber_url_to_markdown import fetch_url_to_markdown

result = fetch_url_to_markdown("https://mp.weixin.qq.com/s/xxx")
print(f"文件已保存：{result['file']}")
```

## 支持的网站

| 网站 | 类型 | 状态 |
|------|------|------|
| 微信公众号 | wechat | ✅ 完美支持 |
| 知乎 | zhihu | ✅ 支持 |
| 掘金 | juejin | ✅ 支持 |
| CSDN | csdn | ✅ 支持 |
| GitHub | github | ✅ 支持 |
| Medium | medium | ✅ 支持 |
| 通用网页 | general | ✅ 支持 |

## 输出目录

**新的目录结构：**
```
/root/openclaw/urltomarkdown/
├── 文章标题 1.md              # MD 文件直接保存在根目录
├── 文章标题 2.md
└── images/
    └── knowledge_YYYYMMDD_HHMMSS/  # 图片按时间戳分组
        ├── img_001.jpg
        └── img_002.jpg
```

**命名规则：**
- **MD 文件**：`{文章标题}.md` - 直接保存在 `/root/openclaw/urltomarkdown/` 根目录
- **图片目录**：`images/knowledge_{时间戳}/` - 时间戳格式：YYYYMMDD_HHMMSS
- **图片文件**：`img_{序号：03d}.jpg`（如 `img_001.jpg`）
- **Markdown 中的图片引用**：`images/knowledge_时间戳/img_001.jpg`

**优势：**
- MD 文件集中管理，方便查找和整理
- 图片按文章分组，避免冲突
- 只有包含图片的文章才创建 images 目录

## 降级策略

1. **Playwright**（首选）- 无头浏览器，支持所有网站，最稳定
2. **Scrapling**（备选）- 快速轻量，支持所有网站
3. **第三方 API**（保底）- 仅支持微信公众号

## 技术特点

- 使用 Playwright 无头浏览器模拟真实访问
- 使用 BeautifulSoup 解析 HTML
- 使用 markdownify 转换为标准 Markdown
- 智能等待策略（networkidle）避免卡死
- 详细日志输出便于排查问题

## 注意事项

- 需要稳定的网络连接
- 部分网站可能需要登录（如腾讯文档、语雀等不支持）
- 图片默认下载到本地，使用相对路径引用
