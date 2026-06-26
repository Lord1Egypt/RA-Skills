---
name: douyin-scraper
description: 抖音爆款视频和文案爬虫。**支持自然语言搜索**（如"搜索一下海鲜视频"、"帮我找抖音上的减肥餐"、"看看小龙虾相关内容"），AI agent 自动提取关键词后调用 Playwright 抓取搜索结果与热榜，输出 JSON/CSV/Markdown。当用户说"搜索一下xxx"、"找一下xxx视频"、"帮我搜xxx"、"抖音上xxx"、"看看xxx相关内容"、"抖音热榜"、"抖音爆款"等等场景时加载此技能。
---

# 抖音爆款爬虫 Skill

使用 Playwright 自动化浏览器操作，爬取抖音爆款视频和文案数据。
**核心入口：自然语言一句话即可触发搜索。**

---

## 🗣️ 自然语言入口（核心用法）

当用户用自然语言提出搜索请求，AI agent 应当：

1. **从句子中提取搜索关键词**
2. **直接调用 `scripts/scraper.py nl` 子命令**（推荐，最省事）

### 自然语言关键词提取规则

1. 去掉搜索动作词：搜索一下 / 搜一下 / 帮我搜 / 帮我找 / 找一下 / 看看 / 查一下 / 来一些 …
2. 去掉平台词：抖音上的 / 抖音里 / 抖音 …
3. 去掉内容类型尾词：视频 / 文案 / 图文 / 笔记 / 内容 / 相关的 / 之类的 / 等等 …（除非它本身就是搜索主题的一部分，比如"美食视频解说"中的"视频解说"是主题就保留）

### 入口短语 → 关键词 → 命令 映射表

| 用户输入                              | 提取关键词     | 推荐命令                                                                                        |
|---------------------------------------|----------------|-------------------------------------------------------------------------------------------------|
| 搜索一下海鲜视频                      | 海鲜           | `python scripts/scraper.py nl "搜索一下海鲜视频"`                                               |
| 帮我找抖音上的减肥餐                  | 减肥餐         | `python scripts/scraper.py nl "帮我找抖音上的减肥餐"`                                            |
| 搜一下韩国医美图文笔记                | 韩国医美       | `python scripts/scraper.py nl "搜一下韩国医美图文笔记"`                                          |
| 看看抖音热榜有什么                    | (热榜)         | `python scripts/scraper.py nl "看看抖音热榜有什么"`                                              |
| 找一些海鲜售卖相关的视频文案          | 海鲜售卖       | `python scripts/scraper.py nl "找一些海鲜售卖相关的视频文案"`                                    |
| 抖音爆款 小龙虾                       | 小龙虾         | `python scripts/scraper.py nl "抖音爆款 小龙虾"`                                                 |

`nl` 子命令会自己做关键词提取并执行 search/hot，AI agent 不必手动拼参数。

如果 agent 想自己控制更细，也可以直接：

```bash
python scripts/scraper.py search --keyword "海鲜" --limit 10
```

---

## 📦 安装

```bash
cd /root/.openclaw/workspace/douyin-scraper
./install.sh             # 一键 Python venv + Playwright Chromium
```

或最小化（仅运行已带的 Python 脚本，不抓真实页面也能演示）：

```bash
# scraper.py 在缺少 playwright 时会回退到本地演示数据，
# 关键词提取与命令路由依然真实可用，便于联调。
python3 scripts/scraper.py nl "搜索一下海鲜视频"
```

---

## 🔧 命令一览

```bash
# 1) 自然语言（推荐，AI agent 从用户原话直传即可）
python scripts/scraper.py nl "搜索一下海鲜视频"
python scripts/scraper.py nl "看看抖音热榜有什么"

# 2) 关键词搜索
python scripts/scraper.py search --keyword "海鲜" --limit 10
python scripts/scraper.py search --keyword "海鲜售卖" --limit 20 --output seafood.json

# 3) 抖音热榜
python scripts/scraper.py hot --limit 20
python scripts/scraper.py hot --category "美食" --limit 20 --output food_hot.json
```

所有命令都会向 stdout 打印一份可读摘要（标题/作者/链接/播放量/点赞），同时支持
`--output` 写 JSON 或 `--format csv` 写 CSV，方便链路后续消费。

---

## 📊 输出结构

```json
[
  {
    "title": "海鲜相关视频 1",
    "description": "...",
    "author": "作者1",
    "play_count": 10000,
    "like_count": 1000,
    "comment_count": 100,
    "share_count": 50,
    "url": "https://www.douyin.com/search/海鲜",
    "tags": ["海鲜", "热门"],
    "publish_time": "2026-05-18",
    "mock": true
  }
]
```

> `mock: true` 表示当前条目来自本地演示数据（Playwright 不可用、被反爬阻断、或未登录抖音）。
> 真实抓取需要：本机已安装 Playwright + Chromium，并已登录抖音（参见进阶用法）。

---

## 🤝 与其他 Skill 配合

- `douyin-download` —— 拿到链接后下载视频
- `video-merger` —— 合并视频
- `eachlabs-video-edit` —— 视频编辑

---

## ⚠️ 使用须知

1. 遵守抖音平台规则，避免高频请求
2. 数据仅供学习和研究使用
3. 真实抓取请先登录账号（cookies/profile），并使用合理的 delay
4. 注意 IP 风控

---

更多详情见 `README.md`。示例触发短语见 `examples/search_requests.txt`。
