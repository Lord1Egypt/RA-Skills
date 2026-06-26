---
version: "1.0.1"
name: dandan-multi-search
description: 多搜索引擎聚合搜索工具。集成17个搜索引擎（8个国内+9个国际），支持高级搜索语法、时间筛选、站内搜索、隐私引擎和 WolframAlpha 知识查询。无需 API Key。当用户要求搜索、多引擎搜索、聚合搜索、隐私搜索、或需要全面信息检索时触发。
metadata: {"openclaw": {"emoji": "🔍"}}
---


# Multi-Search Engine 🔍

多搜索引擎聚合，支持17个搜索引擎，跨平台支持（macOS/Linux/Windows）。

## 触发条件

- 用户说"搜索 X"、"帮我查一下"、"多引擎搜索"
- 需要全面信息检索时
- 要求隐私搜索时
- 需要 WolframAlpha 知识查询时
- 搜索国内/国际内容切换时

## 支持的搜索引擎

### 国内引擎（8个）
| 引擎 | URL | 用途 |
|------|-----|------|
| 百度 | https://www.baidu.com/s?wd= | 常规搜索 |
| 必应 | https://cn.bing.com/search?q= | 补充来源 |
| 搜狗 | https://www.sogou.com/web?query= | 补充来源 |
| 360 | https://www.so.com/s?q= | 补充来源 |
| 神马 | https://m.sm.cn/s?q= | 移动搜索 |
| 知乎 | https://www.zhihu.com/search?type=content&q= | 社区内容 |
| 微博 | https://s.weibo.com/weibo?q= | 社交内容 |
| B站 | https://search.bilibili.com/all?keyword= | 视频/专栏 |

### 国际引擎（9个）
| 引擎 | URL | 用途 |
|------|-----|------|
| Google | https://www.google.com/search?q= | 主引擎 |
| DuckDuckGo | https://duckduckgo.com/?q= | 隐私搜索 |
| Bing | https://www.bing.com/search?q= | 微软搜索 |
| Yahoo | https://search.yahoo.com/search?p= | 补充来源 |
| Startpage | https://www.startpage.com/do/search?q= | 隐私增强 |
| WolframAlpha | https://www.wolframalpha.com/input?i= | 知识计算 |
| GitHub | https://github.com/search?q= | 代码搜索 |
| Google Scholar | https://scholar.google.com/scholar?q= | 学术搜索 |
| PubMed | https://pubmed.ncbi.nlm.nih.gov/?term= | 医学搜索 |

## 跨平台用法

### macOS / Linux
```bash
# 单引擎搜索
open "https://www.google.com/search?q=关键词"

# 多引擎聚合（curl + grep）
curl -s "https://www.google.com/search?q=关键词" | grep -oP 'https?://[^"<>]+' | head -10

# 隐私搜索（DuckDuckGo）
curl -s "https://duckduckgo.com/html/?q=关键词"

# WolframAlpha 计算知识
curl -s "https://www.wolframalpha.com/input?i=公式"
```

### Windows (PowerShell)
```powershell
# 单引擎搜索
Start-Process "https://www.google.com/search?q=关键词"

# 多引擎聚合
(Invoke-WebRequest -Uri "https://www.google.com/search?q=关键词" -UseBasicParsing).Content -split "`n" | Select-String "href" | ForEach-Object { $_.Matches.Value } | Select-Object -First 10

# 隐私搜索
(Invoke-WebRequest -Uri "https://duckduckgo.com/html/?q=关键词" -UseBasicParsing).Content

# WolframAlpha
Start-Process "https://www.wolframalpha.com/input?i=公式"
```

## 高级搜索语法

### Google/百度 语法
```
"精确短语"          # 完全匹配
A OR B              # 或运算
A -B                # 排除词
site:github.com X   # 站内搜索
filetype:pdf X      # 指定文件类型
intitle:X           # 标题含关键词
inurl:X             # URL含关键词
```

### 时间筛选
```
&as_qdr=d        # 24小时内
&as_qdr=w        # 一周内
&as_qdr=m        # 一个月内
&as_qdr=y        # 一年内
```

## 使用决策树

```
1. 用户要求搜索？
   → 确定搜索意图和范围

2. 需要多引擎还是单引擎？
   → 重要/模糊主题 → 多引擎聚合
   → 明确简单查询 → 单引擎快速返回

3. 国内还是国际内容？
   → 国内 → 百度+必应+搜狗+360
   → 国际 → Google+DuckDuckGo+Bing
   → 学术 → Scholar+PubMed

4. 是否需要隐私保护？
   → 是 → DuckDuckGo / Startpage
   → 否 → Google / 百度

5. 是否需要知识计算？
   → 是 → WolframAlpha
   → 否 → 常规搜索
```

## 输出格式

```markdown
## 搜索结果：<关键词>

### 📊 引擎覆盖
- 国内：百度 ✅ | 必应 ✅ | 搜狗 ✅
- 国际：Google ✅ | DuckDuckGo ✅ | Bing ✅

### 🔍 主要发现
1. [来源标题](URL) — 摘要...
2. ...

### 📖 深度来源
- [标题](URL)
- ...

### 💡 WolframAlpha 补充
[如有计算结果]

### 🔗 原始链接
- [Google](链接)
- [百度](链接)
- [DuckDuckGo](链接)
```

## 注意事项

- 国内引擎在海外可能访问受限
- DuckDuckGo 无需 API Key，隐私友好
- WolframAlpha 适合数学/科学问题
- 多引擎搜索会增加请求时间，酌情使用
- 学术搜索优先使用 Google Scholar / PubMed
