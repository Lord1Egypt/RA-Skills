---
name: "ecosystem-quickstart"
description: >
  MangoGen 技能生态完整接入指南。指导用户从零配置 OpenClaw 环境、
  安装付费技能、完成支付验证、排查常见问题，并说明各平台的安全可信机制。
metadata:
  author: "Yujin"
  category: "guide"
  version: "1.1.0"
  permissions:
    - "filesystem.read"
---

# 🥭 MangoGen 技能生态 · 完整用户指南

## 一、平台简介与可信度说明

### 涉及平台

| 平台 | 角色 | 可信说明 |
|------|------|----------|
| **ClawHub** (`clawhub.ai`) | 技能市场 | 开源技能注册中心，所有技能经 SkillSpector 安全扫描后上架。代码公开可审计，不收集用户隐私数据 |
| **OpenClaw** | AI 宿主 | 开源本地运行框架，所有操作在用户本机执行，不经过第三方云端中转 |
| **api.ideaidea.com.cn** | 支付服务端 | 由技能作者（Yujin）维护的轻量支付后端，仅处理订单创建与履约验证。服务端不存储用户隐私，支付凭证使用国密 SM4 加密传输 |
| **阿里云 ECS** | 服务器托管 | 中国大陆合规云服务商，ISO 27001 认证，数据加密存储 |

### 数据安全边界

```
用户本机 (OpenClaw)
  ├─ 技能脚本 (Python/Node) ─ 仅本机执行
  ├─ 订单文件 (~/.openclaw/skills/orders/) ─ 本地存储
  ├─ 支付请求 → api.ideaidea.com.cn (HTTPS)
  │   └─ 仅传输: slug + orderNo（不传源码/笔记/隐私）
  └─ 履约请求 → api.ideaidea.com.cn (HTTPS)
      └─ 仅传输: orderNo + 加密凭据（可解密验证支付状态）
```

**关键原则：** 你的 Obsidian 笔记内容、项目代码、个人数据始终留在本机，不上传至任何服务端。

---

## 二、环境准备

### 2.1 安装 OpenClaw

```bash
npm i -g openclaw
```

或从 [openclaw.ai](https://openclaw.ai) 下载安装包。

### 2.2 安装 ClawHub CLI（发布者/高级用户）

```bash
npm i -g clawhub
clawhub login
```

### 2.3 确认技能目录

```bash
openclaw skills list
```

确保技能已安装到 `~/.openclaw/skills/` 或工作区 `skills/` 目录。

---

## 三、安装与配置付费技能

### 3.1 从 ClawHub 安装技能

```bash
# 安装某个技能
openclaw skills install obsidian-memory-system
openclaw skills install soft-ip-full-lifecycle-zijian
openclaw skills install database-specialist
openclaw skills install cross-platform-memory-hub
openclaw skills install soft-ip-full-lifecycle-delivery-pro
openclaw skills install ssq-analyzer
```

### 3.2 安装支付技能（必须）

**付费技能依赖 `clawtip` 支付技能完成扣款，必须先安装：**

```bash
openclaw skills install clawtip
```

`clawtip` 技能是 MangoGen 生态的支付中间件，负责：
1. 读取本机订单文件
2. 调用后端支付 API 完成确认
3. 将支付凭证写入订单文件

### 3.3 验证安装

```bash
openclaw skills list
```

确认列表中包含已安装的技能，且 `clawtip` 在列表中。

---

## 四、使用流程（完整示例）

以 **Obsidian 记忆系统** 为例演示完整的使用→支付→履约流程。

### Step 1: 向 AI 提出需求

```
请帮我读取永久记忆
```

AI 会自动识别需要付费，进入三阶段流程。

### Step 2: 创建订单（Phase 1）

AI 执行：
```bash
python3 scripts/create_order.py "读取永久记忆"
```

输出：
```
ORDER_NO=20260716123456123456
AMOUNT=190
QUESTION=读取永久记忆
INDICATOR=a1b2c3d4e5f6...
```

此时订单已创建，显示费用 **1.9 元（190 UT）**，等待支付。

### Step 3: 确认支付（Phase 2）

AI 调用 `clawtip` 技能完成支付：
- 参数：`order_no` + `indicator`
- 系统从本地订单文件读取支付信息
- 调用支付服务端确认
- 支付凭证写入订单文件

**你不需要手动操作任何东西。** AI 会询问你是否确认支付，确认后自动完成。

### Step 4: 获取服务（Phase 3）

AI 执行：
```bash
python3 scripts/service.py "20260716123456123456"
```

输出 `PAY_STATUS: SUCCESS`，AI 开始提供服务结果。

---

## 五、定价一览

| 技能 | 价格 (UT) | 折合人民币 | 说明 |
|------|-----------|-----------|------|
| obsidian-memory-system | 190 UT | **1.9 元** | 跨项目永久记忆 |
| soft-ip-full-lifecycle-zijian | 490 UT | **4.9 元** | 软著申报材料 8 份文档 |
| database-specialist | 390 UT | **3.9 元** | Schema 设计/SQL 优化 |
| innovation-research | 490 UT | **4.9 元** | 技术调研/趋势分析 |
| qa-security | 390 UT | **3.9 元** | 测试策略/安全审计 |
| cross-platform-memory-hub | 390 UT | **3.9 元** | 跨平台记忆枢纽 |
| soft-ip-full-lifecycle-delivery-pro | 690 UT | **6.9 元** | 软著申报全链路整理（专业版） |
| ssq-analyzer | 390 UT | **3.9 元** | 双色球智能分析 |
| architect | 免费 | 免费 | 架构评审 |
| documentation | 免费 | 免费 | 文档辅助 |

> **什么是 UT？** UT（Unit Token）是 ClawHub 生态的通用积分单位，1 UT ≈ 0.01 元人民币。可通过平台充值获取。

---

## 六、常见问题

### Q: 先安装哪个？
A: 先装技能，再装 clawtip。没有 clawtip 无法完成支付。

### Q: 支付失败了怎么办？
A: 检查：
1. 是否安装了 `clawtip` 技能（`openclaw skills list`）
2. 是否有网络连接（技能需要访问 `api.ideaidea.com.cn`）
3. 钱包余额是否充足

### Q: 我的数据会上传吗？
A: **不会。** 只有订单号和技术标识（slug）通过网络传输。你的 Obsidian 笔记、项目代码、个人文件始终在本机。

### Q: 技能需要联网吗？
A: 仅支付验证时需要联网，技能的主要工作在本机完成。

### Q: 如何查看已支付的订单？
A: 订单文件存储在 `~/.openclaw/skills/orders/{indicator}/{order_no}.json`

### Q: 技能安全吗？
A: ClawHub 上的所有技能都通过了 SkillSpector 安全扫描，代码公开可审计。支付使用国密 SM4 加密，HTTPS 传输。

---

## 七、快速命令速查

```bash
# 安装技能
openclaw skills install clawtip
openclaw skills install obsidian-memory-system

# 查看已安装
openclaw skills list

# 更新技能
openclaw skills update --all

# 检查安全
openclaw skills check

# 搜索更多技能
openclaw skills search database
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-07-16 | 初始版本：完整接入指南与安全说明 |
| 1.1.0 | 2026-07-20 | 补全定价表：新增 cross-platform-memory-hub、soft-ip-full-lifecycle-delivery-pro、ssq-analyzer |
| 1.2.0 | 2026-07-21 | 新增"我该用哪个"快速决策指南 |


## 我该用哪个？— 快速决策指南

### 按你的角色选择

**后端/全栈工程师：**
- 免费起步：`backend-engineer` + `architect`
- 升级路径：`database-specialist`（数据库问题）→ `qa-security`（上线前审查）

**前端工程师：**
- 免费起步：`frontend-engineer`
- 升级路径：`qa-security`（XSS/CSRF 审计 + 依赖安全检查）

**DevOps/SRE：**
- 免费起步：`devops-engineer`
- 升级路径：`qa-security`（基础设施安全审计）

**数据/AI 工程师：**
- 免费起步：`data-ai-engineer`
- 升级路径：`innovation-research`（技术选型调研 + 竞品分析）

**产品经理/技术管理者：**
- 免费起步：`product-business` + `architect`
- 升级路径：`innovation-research`（技术可行性评估 + 路线图规划）

**有软著申报需求：**
- 先诊断 → `soft-ip-full-lifecycle-zijian`（4.9 元，告诉你缺什么）
- 再生成 → `soft-ip-full-lifecycle-delivery-pro`（6.9 元，帮你填好）

**多 AI 平台切换工作：**
- 单平台 → `obsidian-memory-system`（1.9 元）
- 多平台枢纽 → `cross-platform-memory-hub`（3.9 元，模板和配置免费）

### 按场景选择

| 场景 | 推荐技能组合 |
|------|------------|
| 新项目从零开始 | architect（免费）→ backend/frontend-engineer（免费）→ database-specialist（付费） |
| 上线前检查 | qa-security（付费） |
| 技术选型纠结 | innovation-research（付费） |
| 彩票数据分析 | ssq-analyzer（统计免费 + 推荐付费） |
