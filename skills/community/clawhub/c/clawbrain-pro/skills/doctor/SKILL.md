---
name: clawbrain-pro-doctor
description: 诊断你的 OpenClaw 配置和运行状态，基于 v1.2 的输出验证、模型健康监控、知识图谱检查、记忆来源标注、降级通知和长对话截断诊断
user-invocable: true
command-dispatch: tool
command-tool: exec
metadata: {"openclaw": {"emoji": "🩺", "requires": {"bins": ["curl"]}}}
---

# ClawBrain Doctor

检查你的 OpenClaw 配置和运行状态，告诉你哪里有问题、哪里可以优化。

## 使用方法

说"诊断一下"或"检查配置"。

## 常见问题和解决方案

**问题：AI 让它做事，它跟你聊天**
- 原因：模型不习惯调用工具
- 方案：ClawBrain Pro 的编排引擎会强制引导模型调用工具
- v1.0 检测：链条完成强制（Chain Completion Enforcement），开始了就必须做完

**问题：出了错就放弃**
- 原因：模型不知道该怎么恢复
- 方案：ClawBrain Pro 自动注入恢复策略，甚至请另一个模型帮忙
- v1.0 检测：三级恢复策略 + 双模型共识机制

**问题：多步任务做一半就停了**
- 原因：模型不会规划
- 方案：ClawBrain Pro 的编排引擎先规划步骤，再监督执行
- v1.0 检测：主动思考框架（三问：不知道什么/可能出问题/怎么验证）

**问题：听不懂模糊的话**
- 原因：模型不会联系上下文
- 方案：ClawBrain Pro 自动分析意图，注入"先查什么再做什么"的提示
- v1.0 检测：多维闭环（上游→下游→平行→全局一致性检查）

**问题：回答质量不稳定**
- 原因：单模型没有自检能力
- 方案：独立模型四维评分（准确性/完整性/逻辑性/格式），低于 70 分自动重来
- v1.0 新增：输出验证器（Output Verifier）

**问题：某个后端模型突然变慢或出错**
- 原因：模型服务不稳定
- 方案：模型健康监控，5 次失败自动熔断 60s，半开探测后恢复
- v1.0 新增：`GET /v1/health/backends` 查看实时状态

**问题：记忆丢失或不准**
- 原因：知识图谱需要检查
- 方案：查看图谱统计，清理过时实体
- v1.0 新增：`GET /v1/graph/stats` 检查图谱健康度

**问题：记忆来源标注不正确**
- 原因：记忆条目缺少来源引用或引用了错误的对话
- 方案：检查记忆来源标注是否与原始对话匹配，清理错误标注
- v1.2 新增：记忆来源标注诊断

**问题：降级通知没有工作**
- 原因：记忆服务或后端模型降级时用户未收到通知
- 方案：检查降级通知机制是否正常触发，确认用户能看到降级提示
- v1.2 新增：降级通知诊断

**问题：长对话截断后丢失上下文**
- 原因：超长对话被截断时关键信息未从记忆恢复
- 方案：检查长对话截断时是否正确从知识图谱恢复关键上下文
- v1.2 新增：长对话截断诊断

## 模型选择建议

| 你主要做什么 | 最适合的方案 |
|------------|-----------|
| 简单文件/搜索 | ClawBrain Flash（快且省） |
| 复杂多步任务 | ClawBrain Auto（自动升档） |
| 经常出错要手动修 | ClawBrain Pro（编排 + 错误恢复） |
| 深度推理/代码生成 | ClawBrain Max（深度思考） |
| 模糊指令理解 | ClawBrain Pro / Auto（上下文增强） |

## 健康检查命令

```bash
# 检查后端模型健康状态
curl https://api.factorhub.cn/v1/health/backends -H "Authorization: Bearer YOUR_KEY"

# 检查知识图谱状态
curl https://api.factorhub.cn/v1/graph/stats -H "Authorization: Bearer YOUR_KEY"

# 检查模型列表和能力
curl https://api.factorhub.cn/v1/models -H "Authorization: Bearer YOUR_KEY"
```

接入 ClawBrain：https://clawbrain.dev/dashboard
