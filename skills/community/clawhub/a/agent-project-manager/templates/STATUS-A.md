# 项目：[名称]
> 最后更新：[日期] | Git: [commit hash, 如果有] | PM: v2.5

## 🎯 核心目标
[一句话描述项目终极目标]

## ⏱️ 工时追踪
```yaml
estimated_hours: [预计工时，如 8]
actual_hours: null  # 🔴 项目完成时必须回填，供风险引擎「估时不准」规则使用
```

## 📅 时间线
```yaml
start_date: [YYYY-MM-DD]
estimated_end: [YYYY-MM-DD]
actual_end: null  # 项目完成时自动填写
milestones:
  - name: [里程碑 1 名称]
    date: [YYYY-MM-DD]
    status: pending  # pending / in-progress / completed
  - name: [里程碑 2 名称]
    date: [YYYY-MM-DD]
    status: pending
```

## 📍 当前状态
[当前处于什么阶段，刚完成了什么]

## 📋 待办事项
- [x] 已完成 1
- [ ] 待办 2（优先级高）
- [ ] 待办 3

## 🔗 关系管理
```yaml
# 【强依赖类型】有强制前后置关系
# - type: requires   # A必须依赖B才能开始
# - type: blocks     # A阻塞了B的进度
# - type: optional   # 可选增强，没有也能用

# 【弱关联类型】仅表示关联关系，无强制约束
# - type: related    # 两者相关联，共同推进
# - type: uses       # A使用了B的输出/能力
# - type: references # A参考了B的设计/文档

# - project: [关联项目名称]
#   type: requires
#   description: "描述关系"
#   status: satisfied  # satisfied / blocked / in-progress
```

## 🔑 关键上下文 / 决策
- 决策 1（为什么这么做）
- 约束 1（用户明确要求的事项）
- 链接（相关 URL / 文件路径）

## 🛑 暂停原因 / 待确认问题
[如果项目暂停，记录卡点或下次需要确认的问题]

## ⚠️ 风险日志
```yaml
# Auto-scanned by Project Manager v2.5
# - name: [风险名称]
#   level: high  # high / medium / low
#   trigger: 14 days no update  # 检测触发条件
#   status: active  # active / mitigated / resolved
#   description: "详细描述"
#   suggestion: "建议动作"
```
