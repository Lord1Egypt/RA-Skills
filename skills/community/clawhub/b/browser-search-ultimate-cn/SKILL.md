# browser-search-ultimate-cn - 国内搜索技能

## 实际功能描述

通过 Windows `curl.exe` 直接请求搜索引擎页面，正则提取搜索结果。输出核心答案摘要 + 详细结果列表。

## 引擎支持（2026-03-31 实测）

| 引擎 | 状态 |
|------|------|
| **Bing** (cn.bing.com) | ✅ 稳定可用 |
| **360** (so.com) | ❌ 被反爬 |
| **知乎** | ❌ 被反爬 |

**当前有效引擎**：Bing（主力，稳定出结果）

## 适用场景

- 国内中文信息查询
- 新闻、热点事件
- 通用搜索

## 使用方式

直接调用 Python 脚本：

```
run.py <关键词> [freshness] [count] [vertical]
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 搜索关键词 |
| freshness | string | 否 | 预留参数（暂未实现） |
| count | number | 否 | 返回数量，默认10条 |
| vertical | string | 否 | news/tech/ent/shop（引擎组合略有不同）|

### 输出示例

```
== [Search] 中东战争 ==

[Bing] +10

== [Core Answer] ==
  摘要内容1
  摘要内容2

== [Results: 10 | Bing + 360 + Zhihu] ==
1. [Bing] 标题
   摘要
   URL
```

## 技术实现

- 纯 Python 标准库（sys, io, subprocess, re, urllib, collections）
- `subprocess.run(['curl.exe', ...])` 发 HTTP 请求
- `re.finditer` 正则提取搜索结果
- `OrderedDict` 按 URL 去重
- 输出编码：`sys.stdout = io.TextIOWrapper(..., encoding='utf-8')` 解决 Windows GBK 问题

## 局限性

1. 依赖 `curl.exe` 在系统 PATH 中可用
2. 仅 Bing 稳定，其他引擎可能被反爬返回空结果
3. 不支持需要 JavaScript 渲染的页面（知乎、B站等）
4. 无广告过滤、无权威度排序
5. 摘要来自 HTML 原始文本，可能含噪声字符

## 修复记录

- **2026-03-31**：重写 run.py，移除对不存在的 `openclaw tool call` CLI 命令的依赖，改为直接用 curl 请求 Bing
- 原版 skill 声称支持 12 引擎 + OpenClaw CLI 集成，与实际代码不符，已更正
