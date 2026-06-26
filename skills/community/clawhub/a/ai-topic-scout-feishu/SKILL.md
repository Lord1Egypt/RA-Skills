# AI Topic Scout (Feishu Edition)

**AI 短视频选题追踪系统 — 飞书多维表格版**

自动抓取指定 YouTube 博主视频和 Twitter 博主推文，分析内容，聚合跨平台热点主题，生成带热度评分和选题建议的分析报告，结果写入飞书多维表格。

---

## 功能

1. **抓取内容**
   - YouTube: 指定频道最新视频（标题、描述、观看数、发布时间）
   - Twitter/X: 指定账号最新推文（内容、互动数、发布时间）

2. **智能分析**
   - 提取核心主题和关键词
   - 跨平台话题聚合（发现同一主题在多个平台出现）
   - 热度评分（基于互动数据 + 发布时间）
   - 生成选题建议

3. **数据管理**
   - 自动写入飞书多维表格
   - 支持去重（避免重复抓取相同内容）
   - 按热度排序展示

---

## 使用场景

- 定时抓取 AI 领域博主内容
- 分析短视频选题热度
- 跨平台话题聚合
- 生成内容创作灵感

---

## 触发词

- "抓取选题"
- "分析选题"
- "选题 scout"
- "AI 选题追踪"
- "更新选题表"

---

## 配置

在使用前，需要配置:

### 1. 创建飞书多维表格

首次运行时，系统会自动创建一个名为 **"AI 选题追踪"** 的多维表格，包含以下 4 个数据表:

**数据表 1: YouTube 频道列表**
- 频道 ID (文本, 如 @channelname 或 UCxxxxxx)
- 频道名称 (文本)
- 订阅数 (数字)
- 最后抓取时间 (日期)
- 是否启用 (复选框)
- 备注 (文本)

**数据表 2: Twitter 博主列表**
- 用户名 (文本, 不含 @)
- 显示名称 (文本)
- 粉丝数 (数字)
- 最后抓取时间 (日期)
- 是否启用 (复选框)
- 备注 (文本)

**数据表 3: 原始内容**
- 平台 (单选: YouTube / Twitter)
- 博主名称 (文本)
- 内容标题/正文 (文本)
- 发布时间 (日期)
- 互动数据 (数字: 观看数/点赞数/评论数等)
- 链接 (超链接)
- 数据源 (关联字段 → YouTube频道列表 或 Twitter博主列表)
- 抓取时间 (创建时间)

**数据表 4: 选题分析**
- 主题名称 (文本)
- 关键词 (多选)
- 热度评分 (数字, 1-100)
- 跨平台出现次数 (数字)
- 选题建议 (文本)
- 相关内容 (关联字段 → 原始内容)
- 创建时间 (创建时间)

### 2. 配置数据源

**方式一: 直接在飞书多维表格中管理** (推荐)

在多维表格的 **"YouTube 频道列表"** 和 **"Twitter 博主列表"** 数据表中手动添加记录:

| 频道 ID | 频道名称 | 是否启用 |
|---------|----------|----------|
| @AndrewYNg | Andrew Ng | ✅ |
| @lexfridman | Lex Fridman | ✅ |

系统会自动读取表中**已启用**的数据源进行抓取。

**方式二: 通过配置文件初始化**

首次创建表格时，可在 `config.yaml` 中定义初始数据源:

```yaml
sources:
  youtube:
    - channel_id: "@channelname"
      name: "博主A"
    - channel_id: "@another"
      name: "博主B"
  
  twitter:
    - username: "username1"
      name: "推主A"
    - username: "username2"
      name: "推主B"
```

创建表格时会自动导入这些数据源。

### 3. API 密钥 (可选)

如果需要更高的抓取频率，可配置:
- YouTube Data API key
- Twitter API bearer token

---

## 工作流程

### 第一次运行

```
用户: "创建 AI 选题追踪表"
```

系统会:
1. 创建飞书多维表格 (4 个数据表)
2. 设置字段和关联关系
3. 导入初始数据源 (如果 config.yaml 中有定义)
4. 返回表格链接

### 管理数据源

**添加新数据源:**

```
用户: "添加 YouTube 频道 @3blue1brown"
```

系统会在 "YouTube 频道列表" 中插入新记录。

**禁用某个数据源:**

```
用户: "禁用 Twitter 账号 karpathy"
```

系统会将该记录的 "是否启用" 字段设为 false。

### 日常使用

```
用户: "抓取选题"
```

系统会:
1. 读取配置的数据源
2. 抓取最新内容（过去 7 天）
3. 分析主题和热度
4. 写入多维表格
5. 返回摘要报告

### 查看分析

```
用户: "查看选题分析"
```

系统会:
1. 读取多维表格中的选题分析
2. 按热度排序
3. 展示 Top 10 热门选题

---

## 技术实现

### 内容抓取

- **YouTube**: 使用 `yt-dlp` 或 YouTube RSS feed
- **Twitter**: 使用 `nitter.net` 公开接口或 Twitter API

### 分析引擎

使用 LLM 进行:
- 主题提取
- 关键词标注
- 跨平台相似度匹配
- 选题建议生成

### 热度评分算法

```
热度 = (互动数 × 平台权重) × 时间衰减系数
- 互动数: 观看/点赞/评论等
- 平台权重: YouTube=1.2, Twitter=1.0
- 时间衰减: 7天内=1.0, 7-14天=0.7, 14-30天=0.4
```

---

## 执行逻辑

### Step 1: 初始化检查

```python
# 检查是否已存在多维表格
if not table_exists():
    create_feishu_bitable()
```

### Step 2: 抓取内容

```python
# 从多维表格读取已启用的数据源
youtube_sources = get_enabled_sources("YouTube频道列表")
twitter_sources = get_enabled_sources("Twitter博主列表")

# YouTube
for source in youtube_sources:
    videos = fetch_youtube_latest(source["频道ID"], days=7)
    for video in videos:
        if not exists_in_table(video.url):
            insert_to_raw_content_table(video, source_id=source["记录ID"])
    
    # 更新最后抓取时间
    update_source_last_fetch_time(source["记录ID"])

# Twitter
for source in twitter_sources:
    tweets = fetch_twitter_latest(source["用户名"], days=7)
    for tweet in tweets:
        if not exists_in_table(tweet.url):
            insert_to_raw_content_table(tweet, source_id=source["记录ID"])
    
    # 更新最后抓取时间
    update_source_last_fetch_time(source["记录ID"])
```

### Step 3: 内容分析

```python
# 获取未分析的内容
raw_contents = get_unanalyzed_contents()

# 使用 LLM 批量分析
analysis_prompt = """
分析以下内容，提取:
1. 核心主题（一句话概括）
2. 关键词（3-5个）
3. 选题建议（为什么值得做？如何切入？）

内容列表:
{raw_contents}
"""

analysis_result = llm_analyze(analysis_prompt)

# 聚合相似主题
topics = aggregate_similar_topics(analysis_result)

# 计算热度并写入
for topic in topics:
    topic.heat_score = calculate_heat_score(topic)
    insert_to_topic_analysis_table(topic)
```

### Step 4: 返回报告

```python
# 生成摘要
summary = f"""
✅ 抓取完成

📊 数据统计:
- YouTube 视频: {youtube_count} 条
- Twitter 推文: {twitter_count} 条
- 新增主题: {new_topics_count} 个

🔥 热门选题 Top 5:
{top_5_topics_with_heat_score}

🔗 查看完整表格:
{feishu_bitable_url}
"""

return summary
```

---

## 自动化运行

可配置 OpenClaw cron 定时执行:

```yaml
# gateway config
cron:
  jobs:
    - name: "AI选题追踪"
      schedule:
        kind: cron
        expr: "0 9,21 * * *"  # 每天 9:00 和 21:00
        tz: "Asia/Shanghai"
      payload:
        kind: agentTurn
        message: "抓取选题"
        timeoutSeconds: 300
      sessionTarget: isolated
      delivery:
        mode: announce
```

---

## 依赖工具

- `feishu_bitable_app`: 管理多维表格 App
- `feishu_bitable_app_table`: 管理数据表
- `feishu_bitable_app_table_field`: 管理字段
- `feishu_bitable_app_table_record`: 读写记录
- `web_search`: 补充信息查询
- `exec`: 执行 yt-dlp 等工具

---

## 进阶功能 (可选扩展)

- **自动生成脚本大纲**: 基于选题分析生成短视频脚本框架
- **竞品监控**: 追踪同行业创作者的选题方向
- **趋势预测**: 基于历史数据预测未来热门话题
- **飞书通知**: 发现高热度选题时自动推送飞书消息

---

## 示例对话

```
用户: "创建 AI 选题追踪表"
助手: ✅ 已创建多维表格 "AI 选题追踪"
      包含 4 个数据表:
      - YouTube 频道列表
      - Twitter 博主列表  
      - 原始内容
      - 选题分析
      🔗 https://xxx.feishu.cn/base/xxxx

用户: "添加 YouTube 频道 @3blue1brown"
助手: ✅ 已添加到 YouTube 频道列表
      频道名称: 3Blue1Brown
      状态: 已启用

用户: "抓取选题"
助手: [执行抓取和分析流程]
      
      ✅ 抓取完成
      
      📊 数据统计:
      - YouTube 视频: 12 条 (来自 3 个频道)
      - Twitter 推文: 28 条 (来自 5 个账号)
      - 新增主题: 7 个
      
      🔥 热门选题 Top 5:
      1. AI Agent 工作流优化 (热度: 89)
      2. OpenAI o3 模型解读 (热度: 85)
      3. 本地部署 LLM 实战 (热度: 78)
      4. Prompt Engineering 新技巧 (热度: 72)
      5. AI 视频生成工具对比 (热度: 68)
      
      🔗 查看完整表格: [链接]

用户: "分析 'AI Agent 工作流' 这个选题"
助手: [从表格读取详细信息并展示]
```

---

## 注意事项

1. **频率控制**: YouTube/Twitter 有请求限制，建议每天运行 2-3 次
2. **去重逻辑**: 使用 URL 作为唯一标识，避免重复抓取
3. **隐私保护**: 不要抓取包含敏感信息的私有账号
4. **飞书授权**: 首次使用需完成用户 OAuth 授权

---

## 故障排查

**Q: 抓取失败，返回 403/429 错误**
A: 触发了平台限流，稍后重试或配置 API 密钥

**Q: 重复内容写入表格**
A: 检查去重逻辑，确保使用正确的唯一标识字段

**Q: LLM 分析结果不准确**
A: 调整 prompt 或使用更强的模型（如 opus）

**Q: 飞书多维表格写入失败**
A: 检查用户授权状态，运行 `feishu_oauth` revoke 后重新授权

---

## 作者 & 许可

改编自钉钉版 AI Topic Scout，适配飞书多维表格
License: MIT
