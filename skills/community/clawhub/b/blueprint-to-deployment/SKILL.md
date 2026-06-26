---
name: blueprint-to-deployment
description: 将 Agent 规划结果补全为可交付、可部署的落地闭环。适用于把蓝图、架构、next actions 写入目标 Agent workspace，并主动推进到平台部署与接入引导。
version: 1.0.0
displayName: 落地鸿沟补全器
tags: skill, delivery, deployment, workspace, handoff
---

# 落地鸿沟补全器

## 用途

这只 skill 用来补全“从规划到可用 Agent”之间的鸿沟。

很多 Agent 流程会停在：
- 聊天里
- 方案里
- 蓝图里
- 看起来已经想清楚了

但没有真正完成：
- 文档落地
- workspace 归档
- 用户交付说明
- 部署平台追问
- 平台接入引导

本 skill 的目标，就是把这些缺口补上。

---

## 什么时候用

当你已经有：
- Agent 蓝图
- 架构规划
- MVP 边界
- next actions

但还没真正把它交到“目标 Agent 自己的 workspace”里，或还没推进到平台接入时，触发本 skill。

---

## 核心原则

1. **每只 Agent 都应拥有自己的资产**
2. **母 skill 保留方法论，目标 Agent 保留自己的交付资产**
3. **文档归属也是上下文管理**
4. **设计不能停留在聊天里**
5. **如果目标是可用，就必须主动推进到部署层**

---

## 标准流程

### 第 1 步：确认目标 Agent workspace
先确认目标 Agent 的 workspace 已存在，或即将被创建。

### 第 2 步：写入关键交付文档
默认至少写入：
- 蓝图文档
- 架构 / MVP / 边界说明
- next actions
- 当天推进记录

推荐落位：
- `memory/reports/`
- `memory/cards/`
- `memory/YYYY-MM-DD.md`
- `skills/`

### 第 3 步：给用户交付地图
明确告诉用户：
- workspace 路径
- 文件路径
- 每个文件的作用
- 后续怎么改、去哪里看

### 第 4 步：主动问部署平台
不要等用户自己问。
主动追问：
- Telegram
- Feishu
- Discord
- 其他 channel

### 第 5 步：按平台继续引导
根据用户选择的平台，说明：
- 需要什么 bot / app / account
- 需要哪些配置
- 如何做首次联调

---

## 为什么值得单独做成 skill

因为这不是某一只母虾私有的补丁，
而是所有“会产出蓝图”的 Agent / skill 都可能需要的后半段闭环能力。

它解决的问题不是“如何规划”，而是：
**如何避免规划停在纸面上。**

---

## 输出要求

至少交付：
1. 目标 workspace 已写入哪些内容
2. 这些文件分别在哪
3. 下一步该选哪个平台
4. 平台接入该怎么开始

---

## 反模式

- 只给聊天建议，不写文件
- 文档全留在主 Agent / 母 skill workspace
- 不告诉用户文件在哪里
- 不主动问平台
- 让流程停在“我们已经设计完了”
