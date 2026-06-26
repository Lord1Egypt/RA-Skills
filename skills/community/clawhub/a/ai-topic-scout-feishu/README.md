# AI Topic Scout (Feishu Edition) - README

基于飞书多维表格的 AI 选题追踪系统。

## 快速开始

### 1. 安装依赖

```bash
# Python 工具
pip install yt-dlp

# 系统工具 (可选)
# macOS: brew install curl jq
# Linux: sudo apt install curl jq
```

### 2. 配置数据源

```bash
cd ~/.openclaw/skills/ai-topic-scout-feishu
cp config.example.yaml config.yaml
# 编辑 config.yaml，添加你要追踪的博主
```

### 3. 首次运行

与助手对话:
```
创建 AI 选题追踪表
```

系统会自动创建飞书多维表格并返回链接。

### 4. 抓取选题

```
抓取选题
```

系统会:
1. 抓取配置的 YouTube 和 Twitter 内容
2. 使用 AI 分析主题和热度
3. 写入飞书多维表格
4. 返回摘要报告

## 功能

- ✅ YouTube 视频抓取
- ✅ Twitter 推文抓取
- ✅ AI 主题分析
- ✅ 跨平台话题聚合
- ✅ 热度评分
- ✅ 飞书多维表格存储
- ✅ 自动去重
- ✅ 定时任务支持

## 目录结构

```
ai-topic-scout-feishu/
├── SKILL.md              # Skill 文档（OpenClaw 加载）
├── README.md             # 使用说明
├── package.json          # Skill 元数据
├── config.example.yaml   # 配置模板
├── config.yaml           # 实际配置（需自行创建）
└── scripts/
    ├── fetch_youtube.py  # YouTube 抓取工具
    └── fetch_twitter.py  # Twitter 抓取工具
```

## 配置说明

编辑 `config.yaml`:

```yaml
youtube:
  sources:
    - channel_id: "@AndrewYNg"
      name: "Andrew Ng"

twitter:
  sources:
    - username: "karpathy"
      name: "Andrej Karpathy"

fetch:
  days: 7                    # 抓取最近 7 天
  max_items_per_source: 20   # 每个源最多 20 条

analysis:
  model: "opus"              # 使用的 LLM 模型
  similarity_threshold: 0.75 # 主题相似度阈值
```

## 自动化运行

使用 OpenClaw cron 定时抓取:

```yaml
# 在 gateway config 中添加
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

## 数据表结构

### 1. YouTube 频道列表

| 字段 | 类型 | 说明 |
|------|------|------|
| 频道 ID | 文本 | @channelname 或 UCxxxxxx |
| 频道名称 | 文本 | 显示名称 |
| 订阅数 | 数字 | 频道订阅数（可选） |
| 最后抓取时间 | 日期 | 上次抓取时间 |
| 是否启用 | 复选框 | 是否参与抓取 |
| 备注 | 文本 | 额外说明 |

### 2. Twitter 博主列表

| 字段 | 类型 | 说明 |
|------|------|------|
| 用户名 | 文本 | 不含 @ 的用户名 |
| 显示名称 | 文本 | 账号显示名 |
| 粉丝数 | 数字 | 粉丝数量（可选） |
| 最后抓取时间 | 日期 | 上次抓取时间 |
| 是否启用 | 复选框 | 是否参与抓取 |
| 备注 | 文本 | 额外说明 |

### 3. 原始内容表

| 字段 | 类型 | 说明 |
|------|------|------|
| 平台 | 单选 | YouTube / Twitter |
| 博主名称 | 文本 | 内容创作者 |
| 内容标题/正文 | 文本 | 视频标题或推文内容 |
| 发布时间 | 日期 | 内容发布时间 |
| 互动数据 | 数字 | 观看/点赞/评论等 |
| 链接 | 超链接 | 原始内容链接 |
| 数据源 | 关联 | 关联到频道/博主列表 |
| 抓取时间 | 创建时间 | 记录创建时间 |

### 4. 选题分析表

| 字段 | 类型 | 说明 |
|------|------|------|
| 主题名称 | 文本 | 提炼的核心主题 |
| 关键词 | 多选 | 主题相关关键词 |
| 热度评分 | 数字 | 1-100 的热度分数 |
| 跨平台出现次数 | 数字 | 同一主题在多平台出现 |
| 选题建议 | 文本 | AI 生成的建议 |
| 相关内容 | 关联 | 关联到原始内容表 |
| 创建时间 | 创建时间 | 分析创建时间 |

## 热度评分算法

```
热度 = (互动数 × 平台权重) × 时间衰减系数

- 互动数: YouTube 观看数、点赞数、评论数 / Twitter 点赞、转发、回复
- 平台权重: YouTube=1.2, Twitter=1.0
- 时间衰减:
  - 0-7天: 1.0
  - 7-14天: 0.7
  - 14-30天: 0.4
```

## 故障排查

### yt-dlp 抓取失败

```bash
# 更新 yt-dlp
pip install -U yt-dlp

# 测试抓取
~/.openclaw/skills/ai-topic-scout-feishu/scripts/fetch_youtube.py "@AndrewYNg" 7 5
```

### 飞书授权过期

```
# 与助手对话
撤销飞书授权并重新授权
```

### Twitter 抓取不稳定

Twitter 抓取使用公开镜像站，可能不稳定。建议:
1. 配置 Twitter API Bearer Token
2. 降低抓取频率

## 示例

```
用户: "创建 AI 选题追踪表"
助手: ✅ 已创建多维表格 "AI 选题追踪"
      包含 4 个数据表:
      - YouTube 频道列表
      - Twitter 博主列表
      - 原始内容
      - 选题分析
      🔗 https://xxx.feishu.cn/base/xxxx

用户: "添加频道 @3blue1brown"
助手: ✅ 已添加到 YouTube 频道列表

用户: "抓取选题"
助手: ✅ 抓取完成
      
      📊 数据统计:
      - YouTube 视频: 12 条
      - Twitter 推文: 28 条
      - 新增主题: 7 个
      
      🔥 热门选题 Top 5:
      1. AI Agent 工作流优化 (热度: 89)
      2. OpenAI o3 模型解读 (热度: 85)
      ...

用户: "查看选题分析"
助手: [展示热度排序的选题列表]
```

## 进阶功能

- 自动生成脚本大纲
- 竞品监控
- 趋势预测
- 飞书消息通知

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 PR。
