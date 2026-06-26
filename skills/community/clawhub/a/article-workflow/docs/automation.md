# 文章分析自动化配置

## Heartbeat 触发规则

### 触发条件
- **频率：** 每 6 小时检查一次
- **来源：** 飞书群聊消息
- **触发词：** 包含 URL 且@机器人的消息

### 检查逻辑

```python
# 伪代码 - 配置示例
def check_pending_articles():
    # 1. 从配置文件读取 chat_id
    config = load_config()  # 从 config.json 读取
    chat_id = config.get("notification", {}).get("chat_id", "YOUR_CHAT_ID")
    
    # 2. 获取今天群聊消息
    messages = feishu_get_messages(
        chat_id=chat_id,  # ✅ 从配置读取，不硬编码
        relative_time="today"
    )
    
    # 3. 筛选包含 URL 的消息
    pending_urls = []
    for msg in messages:
        if contains_url(msg.body):
            url = extract_url(msg.body)
            
            # 4. 检查是否已处理（URL 去重）
            if not is_duplicate(url):
                pending_urls.append({
                    "url": url,
                    "message_id": msg.message_id,
                    "sender": msg.sender
                })
    
    # 5. 批量处理
    for item in pending_urls:
        process_article(item["url"])
    
    return len(pending_urls)
```

## 自动化工作流

```
Heartbeat 触发
    ↓
检查群聊消息（今天）
    ↓
筛选@机器人的 URL 消息
    ↓
URL 去重检查
    ↓
批量处理（Reader→Analyst→Librarian）
    ↓
生成汇总报告
    ↓
发送到群聊
```

## 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 检查频率 | 6 小时 | 每天 4 次 |
| 时间范围 | today | 仅处理今天的消息 |
| 批量上限 | 10 篇/次 | 避免过度消耗 |
| 超时设置 | 30 分钟 | 单次处理超时 |

## 汇总报告格式

```
📊 文章分析自动化报告

检查时间：2026-03-14 12:00
处理文章：3 篇

✅ 已处理：
1. [文章标题 1](文档链接)
2. [文章标题 2](文档链接)
3. [文章标题 3](文档链接)

⚠️ 跳过（重复）：
1. [文章标题](原因：已存在于知识库)

📈 知识库统计：
- 总记录数：15 篇
- 今日新增：3 篇
- 本周新增：8 篇
```

## 错误处理

| 错误类型 | 处理策略 |
|---------|---------|
| URL 无法访问 | 重试 2 次，失败则跳过 |
| 分析超时 | 标记为"处理中"，下次重试 |
| Bitable 写入失败 | 保存本地，稍后同步 |
| 飞书 API 限流 | 等待 60 秒后重试 |
