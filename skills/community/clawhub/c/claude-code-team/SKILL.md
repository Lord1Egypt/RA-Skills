---
name: claude-code-team
description: Claude Code Team 模式 - 自动分配团队任务，**自动识别当前平台并分配最优模型**（百炼/火山/OpenAI 等）。**自动判断**：项目相关自动启动团队，日常问题自己回答。
version: 2.0.0
author: davidme6
triggers:
  # 团队触发词
  - 软件开发团队
  - 技术中台团队
  - 搞钱特战队
  - AI 研究团队
  - 创建一个团队
  - 团队模式
  # 项目触发词（自动启动团队）
  - 优化这个项目
  - 修复这个 bug
  - 开发一个
  - 做一个项目
  - 写代码
  - 实现功能
  # 角色触发词
  - 产品经理
  - 程序员
  - 设计师
  - 架构师
  - 测试员
  - 审查员
  - 运维师
  - 文档师

# ⚠️ 自动判断逻辑（核心）

**遇到以下情况自动启动团队：**
1. 用户说"团队"、"软件开发团队"等 → 直接启动
2. 用户说"优化这个项目"、"修复 bug" → 主动启动
3. 用户上传项目截图 + 任务 → 主动启动
4. 日常问题、聊天 → 自己回答，不启动团队

**判断逻辑：**
```
if (用户提到"团队" OR 用户说"优化项目" OR 用户上传项目 + 任务):
    自动启动团队
else:
    自己回答
```
---

# 🏢 Claude Code Team 模式（百炼模型版）

**完全套用 Claude Code Team 模式，自动分配百炼最优模型**

---

## ⚠️ 核心原则

1. **你说团队名，我自动创建**
2. **你说任务，我自动分配**
3. **每个角色自动使用百炼最优模型**
4. **记忆自动持久化**

---

## 🔄 百炼模型映射（核心）

| 角色 | 百炼最优模型 | 说明 |
|------|-------------|------|
| **产品经理** | `bailian/qwen-max` | 最强理解力，需求分析准确 |
| **设计师** | `bailian/qwen-plus` | 创意能力强，审美在线 |
| **程序员** | `bailian/glm-5` | 代码能力最强 |
| **架构师** | `bailian/qwen-max` | 全局视角，技术决策准 |
| **测试员** | `bailian/glm-5` | 细心，找 Bug 能力强 |
| **审查员** | `bailian/glm-5` | 代码审查、安全检查 |
| **运维师** | `bailian/glm-5` | 部署、性能优化 |
| **文档师** | `bailian/glm-5` | 文档编写规范 |

---

## 📋 标准团队配置

### 软件开发团队（8 人）

```json
{
  "name": "软件开发团队",
  "members": [
    { "role": "产品经理", "model": "bailian/qwen-max", "responsibility": "需求分析、用户体验、功能优先级" },
    { "role": "设计师", "model": "bailian/qwen-plus", "responsibility": "视觉设计、动画效果、颜色方案" },
    { "role": "程序员", "model": "bailian/glm-5", "responsibility": "代码实现、技术评估、性能优化" },
    { "role": "测试员", "model": "bailian/glm-5", "responsibility": "测试用例、质量检查、Bug 追踪" },
    { "role": "审查员", "model": "bailian/glm-5", "responsibility": "代码审查、安全检查、规范检查" },
    { "role": "架构师", "model": "bailian/qwen-max", "responsibility": "系统架构、技术选型、最终决策" },
    { "role": "运维师", "model": "bailian/glm-5", "responsibility": "部署运维、监控告警、性能优化" },
    { "role": "文档师", "model": "bailian/glm-5", "responsibility": "文档编写、API 文档、用户手册" }
  ]
}
```

### 技术中台团队（4 人）

```json
{
  "name": "技术中台团队",
  "members": [
    { "role": "技术总监", "model": "bailian/qwen-max", "responsibility": "统筹决策、技术方向" },
    { "role": "技术大拿", "model": "bailian/glm-5", "responsibility": "核心攻坚、技术难点" },
    { "role": "技术老人", "model": "bailian/qwen-coder-plus", "responsibility": "资深开发、带新人" },
    { "role": "技术新秀", "model": "bailian/qwen-coder-next", "responsibility": "执行任务、学习成长" }
  ]
}
```

### 搞钱特战队（10 人）

```json
{
  "name": "搞钱特战队",
  "members": [
    { "role": "市场猎手", "model": "bailian/qwen-max", "responsibility": "发现赚钱机会" },
    { "role": "商业顾问", "model": "bailian/qwen-max", "responsibility": "评估可行性" },
    { "role": "技术专家", "model": "bailian/glm-5", "responsibility": "技术方案" },
    { "role": "流量操盘手", "model": "bailian/qwen-plus", "responsibility": "获客推广" },
    { "role": "内容专家", "model": "bailian/qwen-plus", "responsibility": "内容生产" },
    { "role": "财务管家", "model": "bailian/glm-5", "responsibility": "资金管理" },
    { "role": "风险控制官", "model": "bailian/qwen-max", "responsibility": "风险防控" },
    { "role": "美术设计师", "model": "bailian/qwen-plus", "responsibility": "视觉设计" },
    { "role": "质量把控员", "model": "bailian/glm-5", "responsibility": "质量检查" },
    { "role": "创意专家", "model": "bailian/qwen-plus", "responsibility": "创意策划" }
  ]
}
```

---

## 🚀 工作流程

### 方式 1：标准团队任务

```
用户说："软件开发团队，优化抖音 3D 算命项目"
    ↓
自动执行：
1. 识别团队名 → 软件开发团队
2. 加载团队配置 → 8 个角色
3. 为每个角色分配百炼模型
4. 启动 8 个 Agent（sessions_spawn）
5. 等待所有结果
6. 汇总汇报给董事长
```

### 方式 2：自定义团队

```
用户说："创建一个 AI 研究团队，包括 AI 专家、数据科学家、算法工程师"
    ↓
自动执行：
1. 创建新团队配置
2. 为每个角色分配百炼最优模型
3. 启动团队
4. 分配任务
```

---

## 🧠 记忆系统

### 团队记忆

**位置：** `memory/teams/{团队名}/MEMORY.md`

**自动记录：**
- 任务历史
- 决策记录
- 经验教训

### Agent 记忆

**位置：** `memory/agents/{角色名}/MEMORY.md`

**自动记录：**
- 个人经验
- 任务完成记录
- 技能成长

---

## ⚡ 性能优化

### Gateway 超时解决

| 问题 | 解决方案 |
|------|----------|
| 超时设置 | 120 秒 |
| 连接泄漏 | 任务完成后自动关闭 |
| 并发限制 | 动态调整（默认 10） |
| 内存压力 | 定期清理旧连接 |

### 模型成本优化

| 策略 | 说明 |
|------|------|
| **简单任务用 glm-5** | 成本低、速度快 |
| **复杂任务用 qwen-max** | 能力强、准确 |
| **创意任务用 qwen-plus** | 平衡成本与创意 |

---

## 📋 使用示例

### 示例 1：软件开发团队

```
用户：软件开发团队，优化抖音 3D 算命项目

贾维斯自动启动：
- 产品经理 (bailian/qwen-max) → 需求分析
- 设计师 (bailian/qwen-plus) → 视觉设计
- 程序员 (bailian/glm-5) → 代码实现
- 架构师 (bailian/qwen-max) → 技术决策

等待完成后汇总结果...
```

### 示例 2：技术中台团队

```
用户：技术中台团队，解决 Gateway 超时问题

贾维斯自动启动：
- 技术总监 (bailian/qwen-max) → 统筹决策
- 技术大拿 (bailian/glm-5) → 核心攻坚
- 技术老人 (bailian/qwen-coder-plus) → 经验建议
- 技术新秀 (bailian/qwen-coder-next) → 执行测试

等待完成后汇总结果...
```

### 示例 3：自定义团队

```
用户：创建一个 AI 研究团队，研究大模型应用

贾维斯自动：
1. 创建团队配置
2. 分配角色：AI 专家、数据科学家、算法工程师
3. 为每个角色分配百炼最优模型
4. 启动团队
5. 分配任务
```

---

## 🎯 验收标准

| 功能 | 验收标准 |
|------|----------|
| **团队创建** | 说团队名，自动创建配置 |
| **任务分配** | 说任务，自动分配给所有成员 |
| **模型分配** | 每个角色自动使用百炼最优模型 |
| **记忆持久** | 团队记忆自动保存到 memory/teams/ |
| **进度追踪** | 任务状态自动更新 |
| **Gateway 稳定** | 超时 120 秒 + 自动清理连接 |

---

## ⚠️ 注意事项

1. **Gateway 超时** - 复杂任务可能超过 120 秒，需手动延长
2. **记忆清理** - 定期清理旧记忆（建议每周）
3. **模型成本** - 多 Agent 同时运行，注意 API 成本
4. **并发限制** - 默认 10 个并发，大团队需调整

---

*版本：1.0.0*  
*状态：✅ 激活*  
*模型：百炼大模型*  
*创建时间：2026-04-03*