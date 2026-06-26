# AI搭子 Skill - 数据格式参考

## 日数据格式 (daily/*.json)

```json
{
  "date": "2026-03-20",
  "tokenUsage": {
    "totalInput": 12000,
    "totalOutput": 8000,
    "total": 20000
  },
  "modelFrequency": {
    "claude": 30,
    "gpt": 5,
    "gemini": 2
  },
  "sessionCount": 15,
  "activeHours": {
    "9": 3,
    "10": 5,
    "14": 7,
    "15": 4,
    "21": 2
  },
  "toolCallPreference": {
    "Node.js": 1,
    "Python": 1,
    "Terminal": 1,
    "VSCode": 1,
    "Docker": 1
  },
  "installedSkills": [
    "huashu-data-pro",
    "summarize",
    "ai-dazi-skill"
  ],
  "collectedAt": "2026-03-20T14:30:00.000Z"
}
```

## 用户画像格式 (profiles/latest.json)

```json
{
  "version": "1.0.0",
  "generatedAt": "2026-03-20T14:35:00.000Z",
  "dataRange": {
    "from": "2026-03-18",
    "to": "2026-03-20",
    "days": 3
  },
  "playerLevel": "Builder",
  "playerLevelLabel": "建造者",
  "playerLevelDescription": "善于用AI构建实际项目，产出稳定高质量",
  "activityScore": 65,
  "skillTags": ["编程", "数据分析", "写作"],
  "aiStyle": "重度工具流",
  "matchTags": [
    "Builder", "编程", "数据分析", "写作",
    "重度工具流", "claude-user", "晚间档"
  ],
  "summary": "这是一位建造者级别的AI玩家，核心能力集中在编程、数据分析领域...",
  "rawMetrics": {
    "totalTokens": 85000,
    "totalSessions": 45,
    "installedSkills": ["huashu-data-pro", "summarize"],
    "modelFrequency": { "claude": 30, "gpt": 5 },
    "toolPreference": { "Node.js": 1, "Terminal": 1 }
  }
}
```

## 玩家等级定义

| 等级 | 中文 | 活跃度阈值 | 描述 |
|------|------|-----------|------|
| Pioneer | 先锋玩家 | 80+ | 深度使用AI，探索前沿功能 |
| Builder | 建造者 | 50-79 | 善于用AI构建实际项目 |
| Explorer | 探索者 | 25-49 | 广泛尝试各种AI工具 |
| Observer | 观察者 | 0-24 | 初步接触AI |

## 活跃度评分维度

| 维度 | 最高分 | 计算方式 |
|------|--------|---------|
| 采集天数 | 30分 | 每天3分，上限30 |
| Token总量 | 25分 | 阶梯式：>100k=25, >50k=20, >10k=15, >1k=10 |
| Skill数量 | 15分 | 每个3分，上限15 |
| 模型多样性 | 15分 | 每种5分，上限15 |
| 活跃时段 | 15分 | 每个小时2分，上限15 |
