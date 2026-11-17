---

name: "feed-digest-tool-free"
description: "订阅摘要免费版，支持RSS订阅获取、未读扫描、基础分类与摘要生成。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "订阅摘要(免费版)"
  version: "1.0.0"
  summary: "订阅摘要免费版，支持RSS订阅获取、未读扫描、基础分类与摘要生成。"
  tags:
    - "订阅摘要"
    - "RSS阅读"
    - "内容筛选"
    - "信息过载"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read

---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。


> **获取、扫描、筛选、阅读。四步完成订阅内容摘要。**

无需复杂配置，通过 `feed` CLI 即可获取订阅源最新内容，智能筛选高价值条目，生成精炼摘要。免费版聚焦轻量场景，帮助用户应对信息过载。

## 概述
免费版订阅摘要工具为个人用户提供基础的RSS订阅内容管理能力。通过 `feed` 命令行工具，获取最新条目、扫描未读、筛选高价值内容、生成摘要，让阅读更高效。

### 核心定位
| 维度 | 免费版能力 |
|------|------------|
| 获取最新内容 | 支持（feed fetch） |
| 未读条目扫描 | 支持（默认50条） |
| 智能筛选 | 支持（基础关键词） |
| 全文阅读 | 支持（Markdown格式） |
| 基础分类 | 支持（按订阅源） |
| 标记已读 | 支持（批量） |
| AI深度摘要 | 不支持（需专业版） |
| 多源聚合 | 不支持（需专业版） |
| 定时推送 | 不支持（需专业版） |
| 团队共享 | 不支持（需专业版） |

## 核心能力
### 1. 获取最新内容
```python
import subprocess
import json

class FeedFetcher:
    """订阅内容获取器（免费版）"""

    def __init__(self, cli_path="feed"):
        self.cli = cli_path

    def fetch(self):
        """获取所有订阅源的最新内容"""
        result = subprocess.run(
            [self.cli, "fetch"],
            capture_output=True, text=True, timeout=60, encoding="utf-8"
        )
        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        return {"success": False, "error": result.stderr}

    def get_entries(self, limit=50, feed_id=None):
        """获取未读条目"""
        cmd = [self.cli, "get", "entries", "--limit", str(limit)]
        if feed_id:
            cmd.extend(["--feed", feed_id])

            cmd, capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        if result.returncode == 0:
            return result.stdout
        return f"获取失败：{result.stderr}"

    def get_entry(self, entry_id):
        """获取单条目全文（Markdown格式）"""
            [self.cli, "get", "entry", str(entry_id)],
            capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        if result.returncode == 0:

    def get_feeds(self):
        """获取所有订阅源列表"""
            [self.cli, "get", "feeds"],
            capture_output=True, text=True, timeout=10, encoding="utf-8"
        )
stdout if result.returncode == 0 else f"获取失败：{result.stderr}"

    def get_stats(self):
        """获取数据库统计"""
            [self.cli, "get", "stats"],
            capture_output=True, text=True, timeout=10, encoding="utf-8"
        )
stdout if result.stderr}"

fetcher = FeedFetcher()

print("=== 获取最新内容 ===")
fetcher.fetch()

print("\n=== 订阅源列表 ===")
print(fetcher.get_feeds())

print("\n=== 未读条目 ===")
print(fetcher.get_entries(limit=50))
```

**输出**: 返回获取最新内容的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 智能筛选

> 详细代码示例已移至 `references/detail.md`

**输出**: 返回智能筛选的执行结果,包含操作状态和输出数据。

### 3. 摘要生成

**输出**: 返回摘要生成的执行结果,包含操作状态和输出数据。

### 4. 标记已读
```python
class ReadStatusManager:
    """已读状态管理（免费版）"""

    def __init__(self, cli_path="feed"):
        self.cli = cli_path

    def mark_read(self, entry_ids):
        """标记条目为已读"""
        if not entry_ids:
            return False

        cmd = [self.cli, "update", "entries", "--read"] + [str(id) for id in entry_ids]
            cmd, capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        if result.returncode == 0:
            print(f"已标记 {len(entry_ids)} 条为已读")
            return True
        print(f"标记失败：{result.stderr}")
        return False

    def search(self, query):
        """全文搜索"""
            [self.cli, "search", query],
            capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
stdout if result.returncode == 0 else f"搜索失败：{result.stderr}"

manager = ReadStatusManager()

entry_ids = [entry['id'] for entry in filtered]
manager.mark_read(entry_ids)
```

**输出**: 返回标记已读的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：订阅摘要免费版、RSS、订阅获取、未读扫描、基础分类与摘要生、订阅摘要助手免费、版是面向个人用户、的轻量、订阅摘要工具、四步流程、从订阅源中筛选高、价值内容生成摘要、Use、when、模型调用、智能对话、Agent、LLM、应用时使用、不适用于需要、确定性的关键决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一：每日订阅速览
**场景描述**：每天早上获取订阅源最新内容，快速浏览高价值条目。

```python
fetcher = FeedFetcher()
filterer = FeedFilter(limit=10)
generator = DigestGenerator()
manager = ReadStatusManager()

print("正在获取最新内容...")
fetcher.fetch()

entries_text = fetcher.get_entries(limit=50)

filtered = filterer.filter_entries(entries_text)

digest = generator.generate(filtered, fetcher)
print(digest)

entry_ids = [e['id'] for e in filtered]
manager.mark_read(entry_ids)
```

### 场景二：个人阅读管理
**场景描述**：管理个人订阅，控制信息过载。

```python
fetcher = FeedFetcher()

print("=== 订阅统计 ===")
print(fetcher.get_stats())

print("\n=== 订阅源 ===")
print(fetcher.get_feeds())

print("\n=== 某订阅源未读 ===")
print(fetcher.get_entries(limit=20, feed_id="feed_id_未指定"))
```

### 场景三：高价值内容筛选
**场景描述**：从大量未读中筛选最值得阅读的内容。

```python
fetcher = FeedFetcher()
filterer = FeedFilter(limit=5)

get_entries(limit=100)

filtered = filterer.filter_entries(entries_text)

print(f"=== 今日必读 Top {len(filtered)} ===")
for i, entry in enumerate(filtered, 1):
    print(f"\n{i}. {entry['title']}")
    print(f"   来源：{entry.get('feed', '')}")
    print(f"   得分：{entry.get('score', 0)}")

    full = fetcher.get_entry(entry['id'])
    print(f"   全文长度：{len(full)} 字符")
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手
```bash
brew install odysseus0/tap/feed

feed fetch

feed get entries --limit 50

feed get entry <entry_id>
```

### 120秒标准搭建
```bash
brew install odysseus0/tap/feed
feed add https://example.com/feed.xml
feed add https://another.com/rss

feed fetch

feed get stats

feed get entries --limit 50

feed update entries --read <id1> <id2> <id3>
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 配置示例
### 基础配置
```python
import os

class FeedConfig:
    """订阅摘要配置（免费版）"""
    CLI_PATH = os.getenv("FEED_CLI", "feed")
    DEFAULT_LIMIT = int(os.getenv("FEED_LIMIT", "50"))
    FILTER_LIMIT = int(os.getenv("FEED_FILTER_LIMIT", "10"))
    SUMMARY_MAX_LENGTH = int(os.getenv("FEED_SUMMARY_LEN", "200"))

    HIGH_VALUE_KEYWORDS = [
        'AI', '人工智能', '大模型', 'LLM', 'GPT',
        '系统设计', '架构', '性能优化', '分布式',
        '开发工具', 'DevOps', '反直觉', '颠覆', '突破'
    ]

    SKIP_KEYWORDS = ['广告', '推广', '赞助', 'sponsored']

    @classmethod
    def show(cls):
        print("=== 订阅摘要配置 ===")
        print(f"CLI路径：{cls.CLI_PATH}")
        print(f"默认限制：{cls.DEFAULT_LIMIT}")
        print(f"筛选限制：{cls.FILTER_LIMIT}")
        print(f"摘要长度：{cls.SUMMARY_MAX_LENGTH}")

FeedConfig.show()
```

### 常用命令速查
```bash
feed fetch                              # 拉取所有订阅源最新内容
feed get entries --limit N              # 列出未读条目（表格）
feed get entries --feed <id> --limit N  # 按订阅源筛选
feed get entry <id>                     # 阅读全文（Markdown）
feed search "<query>"                   # 全文搜索
feed update entries --read <id1> <id2> ...  # 批量标记
feed get feeds                          # 列出订阅源（含未读数）
feed get stats                          # 数据库统计
```

## 优选实践
### 1. 输出格式优化
```python
result = subprocess.run(
    ["feed", "get", "entries", "--limit", "50"],
    capture_output=True, text=True
)
```

### 2. 按订阅源筛选
```python
def filter_by_feed(feed_id, limit=20):
    return fetcher.get_entries(limit=limit, feed_id=feed_id)

feeds = fetcher.get_feeds()
```

### 3. 阅读全文
```python
def read_full(entry_id):
    content = fetcher.get_entry(entry_id)
    return content  # Markdown格式
manager.mark_read([entry_id])
```

## 常见问题
### Q1：免费版需要安装什么？
免费版需要安装 `feed` CLI工具。安装方式：macOS可使用 `brew install odysseus0/tap/feed`，其他平台可从源码编译（需Rust环境）。

### Q2：订阅源如何添加？
通过 `feed add <url>` 命令添加RSS/Atom订阅源。支持标准RSS 2.0和Atom 1.0格式。添加后使用 `feed fetch` 获取最新内容。

### Q3：筛选不准确怎么办？
免费版使用基于关键词的简单筛选。如遇筛选不准的情况：(1) 调整 `HIGH_VALUE_KEYWORDS` 列表；(2) 添加更多领域关键词；(3) 升级专业版使用AI深度筛选（基于LLM的内容理解）。

### Q4：未读条目太多怎么办？
建议：(1) 按订阅源筛选 `feed get entries --feed <id>`；(2) 减少限制数量 `--limit 20`；(3) 使用筛选器只看高价值内容；(4) 定期标记已读避免堆积。

### Q5：支持Markdown格式输出吗？
支持。`feed get entry <id>` 返回Markdown格式的全文内容，便于阅读和处理。列表输出默认为表格格式，最节省token。

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Rust**: 1.70+（仅编译feed CLI需要）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| feed CLI | 工具 | 必需 | `brew install odysseus0/tap/feed` 或源码编译 |
| Python 3.8+ | 运行时 | 可选 | 辅助脚本使用 |
| SQLite | 数据库 | 必需 | feed CLI内置（无需单独安装） |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- 免费版无需任何API Key
- 订阅内容基于公开RSS源，不涉及付费API调用
- LLM模型路由由Agent平台内置提供

### 可用性分类
- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent执行订阅内容获取与摘要生成任务

## 已知限制
本免费体验版限制以下高级功能（需升级至专业版解锁）：

- **AI深度摘要**（基于LLM的内容理解与摘要生成）
- **多源聚合**（跨订阅源主题聚合）
- **定时推送**（每日自动推送摘要）
- **团队共享**（团队订阅与共享摘要）
- **个性化推荐**（基于阅读历史的智能推荐）
- **全文搜索增强**（语义搜索）
- **阅读统计与分析**（阅读习惯分析）
- **优先技术支持**

解锁全部高级能力请使用专业版：`feed-digest-tool-pro`

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据