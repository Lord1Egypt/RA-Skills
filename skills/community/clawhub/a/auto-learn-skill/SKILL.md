---
name: auto-learn-skill
description: 自动学习技能 - 从对话中自动提取知识并创建技能。基于Memento-Skills的Read-Write循环机制。适用于AI Agent自进化、知识积累、技能自动创建等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [auto-learn, skill-creation, self-evolution, knowledge-extraction]
version: 1.0.0
author: laosi
source: local
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

- [x] frontmatter格式正确
- [x] 功能描述准确
- [x] 工作流程完整
- [x] 无语法错误

---

# Auto-Learn Skill - 自动学习技能

> 基于Memento-Skills的Read-Write循环机制
> 激活词: 自动学习 / 提取经验 / 创建技能

## 核心原理

```
对话 → 检测模式 → 提取知识 → 创建/更新技能
```

## 触发条件

### 自动触发
- 同一问题解决2次以上
- 发现新的工作流/工具
- 遇到错误并找到解决方案

### 手动触发
- 说"自动学习"
- 说"提取经验"
- 说"创建技能"

## 工作流程

### 1. 读取 (Read)
- 扫描最近对话历史
- 识别重复出现的模式

### 2. 分析 (Analyze)
```
重复问题特征:
- 问题类型相同
- 解决方案相似
- 可泛化到其他场景
```

### 3. 写入 (Write)
创建或更新技能文件

## 检测规则

### 高信号场景
| 场景 | 权重 |
|------|------|
| 解决新类型问题 | +2 |
| 重复问题≥2次 | +1 |
| 发现新工具 | +2 |
| 错误→解决 | +1 |

### 创建阈值
总分 ≥ 3 → 创建新技能

## 应用场景

1. **跨会话学习** - 从多次对话中提取通用模式
2. **技能自动创建** - 将解决方案转化为可复用技能
3. **错误模式识别** - 记录错误→解决的过程
4. **工具发现积累** - 记录新发现的有用工具

## 来源

- 老四AutoLearn系统: `D:\coze-local\simple-agent\skills_learned\auto_learn.md`