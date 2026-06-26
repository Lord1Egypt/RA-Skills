# Feishu Auto-Report - 飞书自主汇报技能

## 🎯 技能定位

专为多 Agent 协作设计的消息发送工具。当 Agent-B/C 完成任务后，自动向用户汇报结果，无需 Agent-A 转发。

## ✨ 核心价值

- **自主汇报** - 执行 Agent 完成后主动通知用户
- **身份隔离** - 每个 Agent 显示独立机器人名称
- **零配置** - Agent 启动时自动扫描，智能判断调用时机

## 🚀 典型场景

```
用户 → Agent-A(统筹) → Agent-B(执行) → 用户
                              ↓
                      自主调用本技能汇报
```

## 📦 快速使用

```bash
# 私聊汇报
./send.sh agent-b ou_xxx open_id "任务已完成"

# 群聊汇报  
./send.sh agent-b oc_xxx chat_id "任务已完成"
```

完整文档参考 SKILL.md。
