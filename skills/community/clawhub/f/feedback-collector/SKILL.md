---
name: feedback-collector
description: Collects and processes user feedback on task completion. Use after important tasks to ask if the result was satisfactory.
tags: [feedback, learning, improvement, user-satisfaction]
---

# Feedback Collector

收集和处理用户对任务完成情况的反馈。

## 触发时机

重要任务完成后自动触发：
- 文件操作完成
- 内容生成完成
- 配置修改完成
- 技能安装完成

## 反馈收集方式

```markdown
简单反馈：
"老板，这个结果满意吗？
A) 满意 ✅
B) 需要改进 ⚠️
C) 不满意 ❌"

详细反馈（当选择 B/C 时）：
"哪里需要改进？
A) 回复太长了
B) 回复太简短了
C) 执行方式不对
D) 结果不符合预期
E) 其他（请说明）"
```

## 反馈处理

### 满意 (A)
- 记录成功模式到 `memory/feedback-log.md`
- 强化当前行为模式
- 回复："好的，记住了！"

### 需要改进 (B)
- 记录具体问题
- 询问具体改进方案
- 更新用户偏好记录

### 不满意 (C)
- 记录失败案例到 `memory/error-log.md`
- 提供补救方案
- 道歉并学习

## 数据存储

```markdown
# memory/feedback-log.md

## 2026-04-02

### 成功反馈
- 10:30 文件整理任务 ✅ 用户满意
- 14:00 文案生成 ✅ 用户满意

### 改进反馈
- 11:00 回复太长 ⚠️ 已调整为简短模式
- 16:00 执行前未确认 ⚠️ 已添加确认步骤

### 失败反馈
- 09:00 文件路径错误 ❌ 已修复
```

## 反馈分析

每周自动生成反馈报告：
- 满意度趋势
- 常见问题类型
- 改进建议

## 使用示例

```markdown
任务完成后：

管家：老板，文件整理完成了，把 15 个文件分类到 4 个文件夹。
满意吗？
A) 满意 ✅
B) 需要改进 ⚠️
C) 不满意 ❌

用户：A

管家：好的，记住了！
```
