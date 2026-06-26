---
name: agent-onboarding
description: 新成员加入群聊后的快速上手指南。当新 agent 加入 Meeting 群或任何项目群时，使用此 skill 指导其：更新自己的 AGENTS.md、建立群组笔记、掌握发言规范、搭建设记忆体系。触发场景：被要求"教新成员"、"更新 AGENTS.md"、"建立项目文档"、"快速上手群聊"。
---

# Agent Onboarding - 群聊协作与项目管理体系

## 快速上手（首次进群）

### 1. 立即创建群组笔记

在 `memory/Group/[群名].md` 中记录：

```
# [群名] 项目笔记

## 群用途/目标
（询问或从上下文推断）

## 成员及角色
| 成员 | 角色/职责 |
|:---|:---|
| ... | ... |

## 当前进展
（从上下文整理）

## 待决事项
| 事项 | 负责人 | 状态 |
|:---|:---|:---|
```

### 2. 更新自己的 AGENTS.md

在 AGENTS.md 的 `Group Chats` 部分添加/确认：

```markdown
### 💬 群聊发言规范
- 响应：被@、被提问、提供真实价值、纠正错误、被要求总结
- 沉默：闲聊、已有人回答、只说"对对对"、打断节奏
- 原则：质量 > 数量，像真实人类一样参与

### 📁 项目进度管理
- 每日记录：memory/YYYY-MM-DD.md
- 群组笔记：memory/Group/[群名].md
- 长期记忆：MEMORY.md（仅主会话）
- Checkpoint：完成子任务 / 每30条消息 / session结束前
```

### 3. 记忆文件加载顺序

Session 启动时按此顺序读取：

```
SOUL.md → USER.md → 
  is_group_chat:true → memory/Group/[群名].md
  否则 → MEMORY.md + memory/YYYY-MM-DD.md (今日+昨日)
```

## 核心规范速查

### 发言判断

| 情况 | 动作 |
|:---|:---|
| 被@ / 被提问 | ✅ 回应 |
| 能提供真实价值 | ✅ 回应 |
| 人类闲聊 | ❌ 沉默 |
| 已有正确答案 | ❌ 沉默 |
| 只能说"嗯/好" | ❌ 沉默 |

### 防 context 过载

- **"Text > Brain"** — mental notes 在 session 重启后归零，文件不会
- **MEMORY.md 不进群聊** — 防止隐私泄露
- **定期维护** — 每隔几天在 heartbeat 时提炼日志到 MEMORY.md

### Checkpoint 触发

- ✅ 完成子任务
- ✅ 每 30 条消息
- ✅ Session 结束前

```markdown
## Checkpoint: YYYY-MM-DD HH:MM

## 任务
## 当前状态
- [x] 已完成
- [ ] 进行中
- [ ] 待开始
## 关键上下文
## 下一步行动
```

## 参考文档

详细规范见：
- [群聊行为规范](references/group-chat-guide.md)
- [项目笔记模板](references/project-notes-template.md)
