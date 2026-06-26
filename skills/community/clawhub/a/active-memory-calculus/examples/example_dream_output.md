# 梦境系统输出示例

## 梦境摘要示例

### 文件位置
`~/obsidian/calculus-memory/dreams/DREAMS_2026-04-12.md`

### 内容示例
```markdown
# 学习梦境摘要 2026-04-12

**生成时间**: 2026-04-12T18:30:00
**统计周期**: 2026-04-12T14:00:00 至 2026-04-12T18:00:00

## 关键发现

🎯 **mastery_breakthrough**: 学生在以下概念上取得突破: 极限, 导数
💡 **learning_style_identified**: 识别学习风格: visual
🔴 **persistent_error**: 发现高频错误模式: integral_limit_transform (出现3次)

## 概念掌握进展

✅ **极限**: 85% (proficient)
✅ **导数**: 80% (proficient)
⚠️ **定积分**: 55% (learning)
❌ **反常积分**: 30% (struggling)
❌ **级数**: 25% (struggling)

## 错误模式分析

🔴 **integral_limit_transform**: 出现 3 次
🟡 **derivative_chain_rule**: 出现 1 次

## 学习断层预警

⚠️ **反常积分**: 建议先强化: 极限
⚠️ **级数**: 建议先强化: 极限

## 学习建议

1. 优先强化薄弱概念: 反常积分, 级数
2. 针对高频错误'integral_limit_transform'进行专项练习
3. 建议先强化: 极限
4. 明日推荐学习: 定积分, 反常积分

## 知识图谱更新

```json
{
  "nodes": [
    {"id": "极限", "type": "concept", "mastery": 0.85, "status": "proficient"},
    {"id": "导数", "type": "concept", "mastery": 0.80, "status": "proficient"},
    {"id": "定积分", "type": "concept", "mastery": 0.55, "status": "learning"},
    {"id": "反常积分", "type": "concept", "mastery": 0.30, "status": "struggling"},
    {"id": "级数", "type": "concept", "mastery": 0.25, "status": "struggling"}
  ],
  "edges": [
    {"source": "极限", "target": "反常积分", "relation": "prerequisite", "strength": "strong"},
    {"source": "极限", "target": "级数", "relation": "prerequisite", "strength": "strong"}
  ],
  "gaps": ["反常积分", "级数"],
  "timestamp": "2026-04-12T18:30:00"
}
```
```

## 知识图谱可视化

```
                    [极限] 85%
                   /    \
                  /      \
                 v        v
           [导数] 80%   [反常积分] 30% ❌
              |           ^
              |           |
              v           |
         [定积分] 55% ----+
              |
              v
         [级数] 25% ❌
```

## 自动触发的干预措施

基于上述梦境摘要，系统自动触发以下干预：

1. **明日学习计划调整**
   - 推荐优先学习：极限概念复习（针对反常积分和级数的前置薄弱）
   - 推荐练习：定积分换元专项（针对高频错误）

2. **实时预警增强**
   - 下次涉及定积分换元时，自动显示检查清单
   - 下次涉及反常积分时，先进行极限概念快速复习

3. **资源推荐**
   - 自动调用 resource-harvester 搜索反常积分的可视化资源
   - 推荐难度适中的反常积分练习题
