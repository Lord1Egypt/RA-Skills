---
name: flomo-random-walk
description: |
  随机漫步：从一条随机笔记出发，探索相关笔记，形成知识漫游路径。
  触发场景：用户说"随机漫步"、"flomo漫步"、"知识漫步"、"开始漫步"等。
---

# 随机漫步 — Flomo 知识探索

## 触发场景

用户说以下内容时调用：
- "随机漫步"
- "flomo漫步"
- "知识漫步"
- "开始漫步"
- "漫步一下"

## 核心流程

### 第一步：获取随机笔记

**方案A（推荐）：每日回顾随机**
调用 `get_daily_review` 获取今日推荐笔记，从中随机选择一条。

```bash
curl -X POST "https://flomoapp.com/mcp" \
  -H "Authorization: Bearer {FLOMO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_daily_review","arguments":{}}}'
```

从返回的 memos 数组中随机选一条。

**方案B（备选）：标签随机**
1. 调用 `tag_search` 搜索随机关键词获取标签
2. 用 `memo_search` 搜索该标签下的笔记
3. 随机选一条

### 第二步：展示笔记 + 相关推荐

1. 展示当前笔记内容
2. 调用 `memo_recommended` 获取相关笔记（最多10条）

```bash
curl -X POST "https://flomoapp.com/mcp" \
  -H "Authorization: Bearer {FLOMO_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"memo_recommended","arguments":{"id":"笔记ID","limit":10,"no_same_tag":false}}}'
```

参数说明：
- `id`: 当前笔记ID
- `limit`: 返回数量，默认10
- `no_same_tag`: 是否排除同标签笔记，false 更容易发现意外关联

### 第三步：用户选择继续

展示相关笔记列表（编号1-10），用户输入数字选择下一条。

```
📮 随机漫步 #1
━━━━━━━━━━━━━━━━━━━━

{当前笔记内容}

{标签}

━━━━━━━━━━━━━━━━━━━━
🔗 相关笔记：

1. {相关笔记1摘要}...
2. {相关笔记2摘要}...
...

💡 输入数字继续漫步，或输入"q"结束
```

### 第四步：循环漫步

用户选择后，以选中的笔记为新起点，重复第二步和第三步。

记录漫步路径：
```json
{
  "path": [
    {"id": "xxx", "content": "摘要", "tags": ["..."]},
    ...
  ],
  "started_at": "2026-04-23T23:00:00+08:00"
}
```

## 展示格式

### 当前笔记
```
📮 随机漫步 #{步数}
📅 {created_at 日期}

{content 内容}

🏷️ {tags 标签}
```

### 相关笔记列表

**展示逻辑**：
1. 取笔记前150字符
2. 将换行符替换为空格，让显示更紧凑
3. 超过150字显示 `...`
4. 显示 `word_count` 字段值（真实字数）

```
━━━━━━━━━━━━━━━━━━━━
🔗 发现 {count} 条相关笔记：

1. 最近感觉也没什么好记录的 昨天宝贝说车厘子很便宜，我寻思，小思不是水果店的么，就找他买了几箱、给妈妈、宝贝的妈妈...
   🏷️ #Resource/Dayone | 📝 783字
   
2. 用了政府在支付宝发的券 果然这个券是用来刺激消费的，因为我买的东西都是非基本品，而是享乐品。
   🏷️ #Resource/Dayone | 📝 84字
...
```

## 漫步结束

用户输入"q"或其他退出指令时，展示漫步路径：

```
🎯 本次漫步完成！

📍 路径回顾：
1. {笔记1摘要}... → 
2. {笔记2摘要}... → 
3. {笔记3摘要}...

💡 输入"再来"开始新的漫步
```

## 历史记录

记录到 `memory/flomo-random-walk-history.json`：
```json
{
  "walks": [
    {
      "date": "2026-04-23",
      "steps": 5,
      "path": ["id1", "id2", "id3", "id4", "id5"],
      "start_tag": "Resource/AI",
      "end_tag": "Project/出海"
    }
  ],
  "total_walks": 12,
  "total_steps": 47
}
```

## 注意事项

- 每步展示当前笔记全文，相关笔记只展示摘要（前50-80字）
- 相关笔记按相关性排序，用户选择任意一条继续
- 如果 `memo_recommended` 返回少于3条，提示用户可选择"换一批"
- 鼓励用户探索意外关联，不是只看同标签内容

## API 凭证

从 `SECRET.md` 读取：
- Token: `fmcp_P7Oq8XKWAEGE7544Rle0SWxkMPNhFWh3n-ExYX1rjes`
- MCP URL: `https://flomoapp.com/mcp`
