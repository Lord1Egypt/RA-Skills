# 角色设计指南

基于 AutoNovel Writer v5.0 项目规划的角色设计最佳实践。

---

## 📖 角色设计原则

### 1. 角色弧光 (Character Arc)

每个主要角色都应该有清晰的成长轨迹：

```
初始状态 → 催化剂反应 → 适应期 → 中点转折 → 低谷期 → 领悟期 → 最终状态
```

### 2. 动机层次 (Motivation Layers)

| 层次 | 说明 | 示例 |
|------|------|------|
| **表面目标** | 角色声称想要的 | "我要成为最强者" |
| **深层目标** | 角色真正想要的 | "我要保护家人" |
| **内心冲突** | 阻碍角色的内在问题 | "力量与本心的平衡" |

### 3. 关系网络 (Relationship Web)

每个角色应该与其他角色有明确的关系：

```yaml
relationships:
  - name: 苏媚
    type: 女主角
    status: 暧昧
    description: 青云宗圣女，对林风有好感
    conflict: 身份差距
    arc: 陌生→相识→暧昧→恋人
```

---

## 🎭 角色类型模板

### 主角模板

```yaml
name: 林风
role: 主角
age: 16
gender: 男

# 核心特征
core_traits:
  - 坚韧不拔
  - 重情重义
  
# 致命弱点
fatal_flaw: 有时冲动

# 角色弧光
arc:
  start: 平凡少年，渴望力量
  midpoint: 发现身世之谜，陷入迷茫
  end: 接受使命，成长为强者

# 动机
motivation:
  surface_goal: 成为强者，保护重要的人
  deep_goal: 寻找父母失踪真相
  internal_conflict: 力量与本心的平衡
```

### 女主角模板

```yaml
name: 苏媚
role: 女主角
age: 17
gender: 女

# 独立目标（不依附于主角）
independent_goal: 成为宗门宗主

# 与主角的关系弧光
relationship_arc:
  - 阶段：初识
    态度：好奇
  - 阶段：相知
    态度：欣赏
  - 阶段：相爱
    态度：坚定

# 个人成长线
personal_arc: 圣女→宗主→道侣
```

### 反派模板

```yaml
name: 魂天帝
role: 反派
age: 未知
gender: 男

# 反派不是纯粹的恶
motivation:
  surface_goal: 统治世界
  deep_goal: 复活逝去的爱人
  justification: "为了她，我可以牺牲一切"

# 与主角的镜像关系
mirror_to_hero:
  - 相同点：都愿意为所爱的人牺牲
  - 不同点：主角选择守护，反派选择毁灭

# 悲剧性
tragedy: 曾经也是正义之士，因爱生恨
```

---

## 📊 角色一致性检查清单

### 创建角色时检查

- [ ] 角色有明确的表面目标和深层目标
- [ ] 角色有至少一个致命弱点
- [ ] 角色有清晰的成长弧光
- [ ] 角色与其他角色有明确关系
- [ ] 角色的行为符合其性格特征
- [ ] 角色有独立的动机（不依附他人）

### 更新角色时检查

- [ ] 新增事件与已有背景不冲突
- [ ] 角色成长符合弧光规划
- [ ] 关系变化有合理铺垫
- [ ] 动机变化有触发事件

---

## 🎯 常见角色设计错误

### ❌ 错误 1: 角色过于完美

```yaml
# 错误示例
traits:
  - 聪明
  - 勇敢
  - 善良
  - 帅气
  - 富有
# 没有弱点，角色不真实
```

```yaml
# 正确示例
traits:
  - 聪明（但有时过于自信）
  - 勇敢（但有时冲动）
  - 善良（但有时优柔寡断）
flaws:
  - 不愿示弱
  - 对敌人过于仁慈
```

### ❌ 错误 2: 角色弧光缺失

```yaml
# 错误示例
arc:
  start: 平凡少年
  end: 平凡少年  # 没有成长！
```

```yaml
# 正确示例
arc:
  start: 平凡少年，渴望力量
  midpoint: 发现身世之谜，陷入迷茫
  end: 接受使命，成长为强者
```

### ❌ 错误 3: 关系网络单薄

```yaml
# 错误示例
relationships:
  - name: 苏媚
    type: 女主角
    # 没有其他关系！
```

```yaml
# 正确示例
relationships:
  - name: 苏媚
    type: 女主角
    status: 暧昧
  - name: 萧炎
    type: 竞争对手
    status: 亦敌亦友
  - name: 药老
    type: 导师
    status: 师徒情深
```

---

## 📚 参考资源

- 《故事》- 罗伯特·麦基
- 《人物》- 罗伯特·麦基
- 《作家之旅》- 克里斯托弗·沃格勒
- 《 Save the Cat!》- Blake Snyder

---

**Version**: 1.0.0  
**基于**: AutoNovel Writer v5.0 项目规划
