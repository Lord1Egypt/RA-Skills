# 技能进化插件 v5.0 — 扩展模块参考

## 模块依赖关系

```
dream.py (主流程)
    │
    ├── [E1] work_review.WorkAnalyzer      # 工作复盘分析
    │         └── TomorrowPlanner           # 明日计划生成
    │
    ├── [E2] skill_evolution.SkillScorer   # 技能评分
    │
    ├── [E3] skill_evolution.DecayEngine  # 用进废退衰减
    │
    ├── [E4] skill_evolution.SkillRegistry # 技能注册表更新
    │
    ├── [E5] work_review.TomorrowPlanner   # 明日计划（依赖E1+E2）
    │
    ├── [E6] skill_explorer.GapDetector   # 技能缺口检测
    │         └── SkillLearner             # 自主学习
    │
    ├── [E7] skill_developer.SkillGenerator # 技能全自动生成
    │         ├── SkillTemplates           # 技能模板库
    │         └── SkillQualityAssessor     # 质量评估
    │
    └── [E8] reporter.DailyReporter        # 每日汇报生成
              └── SkillReportGenerator     # 技能专项报告
```

## 技能评分公式

```python
total_score = (
    frequency_score * 0.4 +    # 调用频率（对数衰减）
    recency_score * 0.3 +      # 最近使用时间
    success_score * 0.3        # 成功率
) * decay_factor

# 时间衰减因子
if days_since_call > 180: decay_factor = 0.0   # 归档
elif days_since_call > 90:  decay_factor = 0.2
elif days_since_call > 30:  decay_factor = 0.5
else:                       decay_factor = 1.0
```

## 数据存储路径

```
~/.openclaw/workspace/
└── memory/
    ├── dreams/
    │   ├── 2026-05-03.md              # 梦境报告
    │   └── daily-report-2026-05-03.md # 每日完整汇报
    └── ...

~/.skill_scoreboard/
└── scores.json                        # 技能积分榜数据
```

## skill_scoreboard 数据结构

```json
{
  "skills": {
    "weather": {
      "total_count": 4,
      "total_score": 54.12,
      "last_used": "2026-04-29T...",
      "last_score": 54.12,
      "quality_score": 1.0
    }
  }
}
```

## 技能等级阈值

```python
TIER_THRESHOLDS = {
    '🔥': 80,   # 高度活跃
    '📈': 60,   # 正常
    '💤': 40,   # 低活跃
    '🗄️': 20,   # 休眠
    '⚰️': 0,    # 已归档
}
```

## 技能生成触发条件

当 `GapDetector` 检测到以下情况时，触发 `SkillGenerator`：

1. 用户需求与现有技能不匹配（相似度 < 0.6）
2. 某类任务频繁出现但无对应技能
3. 技能缺口被重复识别（同一缺口出现 ≥3 次）
4. 新领域探索任务需要系统性支持

## 汇报模板（六大模块）

```
📊 每日汇报 — {date}
═══════════════════════════════════

## 📝 今日总结
### 工作完成情况
### 完成的任务 (N项)
### 未完成的任务 (N项)
### 阻碍因素

## 📋 明日计划
### 继续任务
### 新增任务
### 技能开发计划
### 执行优先级

## 🛠️ 技能开发
### 新开发的技能
### 技能改进
### 开发理由

## 📈 技能评分（用进废退）
### 技能活跃度排行
### 技能状态分布
### 需关注的技能
### 用进废退记录

## 🎯 精进点
### 今日学到的新东西
### 需要改进的地方
### 明日行动项

## 💭 个人感想
```
