---
name: "clawhub-mirror-search-engine-setup"
description: "配置 ClawHub 国内镜像解决限流问题，并安装 Multi Search Engine 技能。当遇到 ClawHub 安装技能限流、访问慢、需要配置 cn.clawhub-mirror.com 镜像、安装多搜索引擎技能、或需要归档配置到知识库时使用。涵盖 CLI 参数指定镜像、环境变量配置、17 个搜索引擎使用策略、隐私搜索技巧及知识永久归档流程。即使未明确提及镜像，只要涉及 ClawHub 技能安装失败或慢，均应触发此技能。"
metadata: { "openclaw": { "emoji": "🦞" } }
---

# ClawHub 国内镜像配置与多搜索引擎技能安装

本技能指导你如何解决 ClawHub 海外服务器限流问题，通过配置国内镜像快速安装技能，并掌握 Multi Search Engine 的 17 个搜索引擎使用策略，最后将经验永久归档到知识库。

## 何时使用此技能

- 当使用 `clawhub install` 遇到速率限制（Rate Limit）或连接超时时
- 当需要安装 Multi Search Engine 或其他 ClawHub 技能且希望加速下载时
- 当用户询问如何使用多个搜索引擎（百度、Google、微信等）进行特定场景搜索时
- 当需要将配置经验永久记录到 `.learnings` 或知识库索引中时

## 步骤

### 1. 配置国内镜像（推荐 CLI 参数方式）

优先使用 CLI 参数指定镜像，无需修改全局环境变量，最简单直接。

```bash
clawhub install <skill-slug> --registry https://cn.clawhub-mirror.com
```

**为什么：** 避免环境变量配置后当前 Shell 会话未生效的问题，每次命令显式指定最可靠。

### 2. 备选方案：环境变量配置

如果需要永久配置，可设置环境变量，但必须重新加载配置。

```bash
export CLAWHUB_REGISTRY=https://cn.clawhub-mirror.com
export CLAWHUB_SITE=https://cn.clawhub-mirror.com
source ~/.bashrc
```

**为什么：** 环境变量配置后不会自动生效于当前会话，必须 `source` 或重新登录。

### 3. 安装 Multi Search Engine 技能

使用配置好的镜像安装技能。

```bash
clawhub install multi-search-engine --registry https://cn.clawhub-mirror.com
```

**为什么：** 该技能集成 17 个搜索引擎（8 国内 +9 国际），无需 API Key 即可使用。

### 4. 掌握搜索场景策略

根据用户意图选择引擎，不要只用一个搜索引擎。

- **技术教程：** Google + `site:github.com`
- **中文内容：** 百度 + 搜狗微信
- **隐私敏感：** DuckDuckGo / Startpage
- **知识查询：** WolframAlpha（货币、数学、股票）

**为什么：** 不同引擎收录内容不同，组合使用能提高信息覆盖率和准确性。

### 5. 永久归档到知识库

将配置方法记录到 `.learnings/` 目录，并更新索引文件。

1. 创建学习记录：`.learnings/YYYY-MM-DD-clawhub-mirror-config.md`
2. 更新索引：`LEARNINGS.md` 添加新记录编号
3. 更新速查：`TOOLS.md` 添加使用方法
4. 同步进化：同步到所有 agent 工作目录（main, echo, code, research）
5. Git 提交：推送变更到远程仓库

**为什么：** 确保所有 agent 实例都能访问此经验，避免重复解决相同问题。

## 陷阱与解决方案

❌ **配置环境变量后直接运行命令**
→ **为何失败：** 当前 Shell 会话未加载新环境变量，仍使用默认海外源
→ **✅ 正确做法：** 执行 `source ~/.bashrc` 或重新登录，或直接用 CLI 参数 `--registry`

❌ **使用默认 ClawHub 地址**
→ **为何失败：** `clawhub.ai` 位于海外，国内访问易触发限流或超时
→ **✅ 正确做法：** 始终指定 `https://cn.clawhub-mirror.com`

❌ **仅在当前工作目录记录配置**
→ **为何失败：** 其他 agent 工作目录（如 workspace-code）无法获取此知识
→ **✅ 正确做法：** 执行进化同步，更新所有 4 个 agent 工作目录并提交 Git

## 关键代码与配置

### 常用 ClawHub 命令（带镜像参数）

```bash
# 安装技能
clawhub install <skill-slug> --registry https://cn.clawhub-mirror.com

# 更新所有技能
clawhub update --all --registry https://cn.clawhub-mirror.com

# 搜索技能
clawhub search "query" --registry https://cn.clawhub-mirror.com
```

### 高级搜索操作符示例

```bash
# 站内搜索
site:github.com react tutorial
site:zhihu.com AI 大模型

# 文件类型
filetype:pdf machine learning report
filetype:ppt 人工智能 发展趋势

# 时间过滤
tbs=qdr:h AI news（过去 1 小时）
tbs=qdr:w python best practices（过去 1 周）

# 精确匹配/排除
"machine learning" tutorial
python -snake
```

### 核心搜索引擎 URL 模板

| 引擎 | 模板 | 场景 |
|------|------|------|
| 百度 | `baidu.com/s?wd={keyword}` | 中文通用 |
| 微信 | `wx.sogou.com/weixin?type=2&query={keyword}` | 公众号文章 |
| Google | `google.com/search?q={keyword}` | 技术/国际 |
| DuckDuckGo | `duckduckgo.com/html/?q={keyword}` | 隐私保护 |
| WolframAlpha | `wolframalpha.com/input?i={keyword}` | 知识计算 |

## 环境与前提

- **系统：** Linux / macOS (Bash Shell)
- **工具：** OpenClaw 环境，ClawHub CLI
- **网络：** 需能访问国内镜像 `cn.clawhub-mirror.com`
- **权限：** 用户主目录写入权限（用于配置环境变量）

## 伴随文件

- `.learnings/2026-04-01-clawhub-mirror-config.md` — 完整配置教程与故障排查记录
- `LEARNINGS.md` — 学习记录索引，包含记录编号 LRN-20260402-001
- `TOOLS.md` — 使用方法速查表

## 任务记录

**任务标题：** Multi Search Engine 安装与 ClawHub 国内镜像配置永久归档
**关键细节：**
- 国内镜像 URL：`https://cn.clawhub-mirror.com`
- 技能版本：Multi Search Engine v2.0.1
- Git 提交号：`4043539`
- 配置推荐度：CLI 参数（⭐⭐⭐）> 环境变量+source（⭐⭐）
- 同步范围：main, echo, code, research 四个工作目录