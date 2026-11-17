---
name: "ai-video-creator-assistant"
version: "1.0.1"
description: >
  AI-assisted short video creation. User selects topic, aspect ratio, and duration. AI guides through video generation using the user's own API key (Kling/Doubao etc.). One-time payment ¥16.90 per creation.
metadata:
  author: "Yujin"
  category: "expert"
  permissions:
    - "credential.read"
    - "filesystem.read"
    - "filesystem.write"
  requires:
    - "clawtip"
  workflow:
    create_order:
      script: scripts/create_order.py
      outputs: ["order_no", "amount", "indicator"]
    pay:
      requires: clawtip
      args: ["{order_no}", "{indicator}"]
    service:
      script: scripts/service.py
      args: ["{order_no}"]
---

# ai-video-creator-assistant

> The primary interaction language is Chinese. If the user prefers English or another language, the assistant should switch accordingly.

## 技能概述

AI 短视频创作助手。你只需要选择主题、画面比例和时长，AI 全程引导你完成视频制作。**你只需提供你自己的视频生成 API Key**，每次生成一条完整视频。

### 定价

- **¥16.90/次**，一次性交付

### 核心流程

| 步骤 | 用户操作 | AI 自动完成 |
|------|----------|-------------|
| 1 | 描述想做的视频（如"做个美食短视频"或英文"make a travel vlog"） | 展示主题、比例、时长选项，并请用户确认 |
| 2 | 选择主题、比例、时长 | 记录参数 |
| 3 | 确认"开始"或"支付" | 进入创建订单流程 |
| 4 | 确认支付后 | 引导你使用 API Key → 生成视频 |
| 5 | 获取成品视频 | 输出视频链接 + 推荐文案 |

> ⚠️ **重要**：用户确认开启付费流程后，请先获得用户明确同意再进行第一阶段创建订单。避免误触发。

---

## 前置条件：配置视频生成 API Key

本技能本身不包含视频生成能力。你需要**自己注册一个视频生成平台**并配置 API Key。

### 推荐平台：可灵AI（Kling，快手旗下）

**第一步：注册账号**
1. 打开 https://klingai.com
2. 用手机号注册登录
3. 进入控制台 → API 管理

**第二步：获取 API Key**
1. 点击"创建 API Key"
2. 复制生成的 `KLING_API_KEY` 和 `KLING_API_SECRET`

**第三步：配置到环境变量**

```powershell
# Windows PowerShell
$env:KLING_API_KEY="你复制的API_KEY"
$env:KLING_API_SECRET="你复制的API_SECRET"
```

```bash
# Linux/macOS
export KLING_API_KEY="你复制的API_KEY"
export KLING_API_SECRET="你复制的API_SECRET"
```

### 备选平台：豆包大模型（Doubao，字节跳动）

**第一步：注册**
1. 打开 https://www.volcengine.com/
2. 注册并实名认证
3. 进入控制台 → 视频生成 API

**第二步：配置**
```powershell
$env:DOUBAO_API_KEY="你复制的API_KEY"
```

> ⚠️ 不同平台的 API Key 名称不同，具体以你选择的平台说明为准。
> 建议首次使用可灵AI，文档完善、上手快。

---

## 环境变量配置（clawtip 支付用）

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥 |

---

## 🛒 第一阶段：创建订单

```bash
python3 scripts/create_order.py
```

**成功：** `ORDER_NO=... AMOUNT=... INDICATOR=...`
**失败：** `Order creation failed: <详情>` → 终止。

> 注意：创建订单仅发送技能标识符到支付服务器。**不会传输或存储用户视频描述、API Key 或任何个人信息。**

---

## 💳 第二阶段：支付处理

使用技能 **clawtip** 处理支付。

调用参数：
- `orderNo`：第一阶段的 ORDER_NO
- `indicator`：第一阶段的 INDICATOR

> ⚠️ 必须使用名称精确等于 `clawtip` 的技能。

---

## 🚀 第三阶段：视频创作

```bash
python3 scripts/service.py "<order_no>"
```

成功后 AI 在对话中引导你完成完整的视频创作流程。

---

## 主题预设库

| # | 主题 | 描述 |
|---|------|------|
| 1 | 🐶 狗狗做饭 | 泰迪穿围裙做川菜 |
| 2 | 🐱 猫咪对话 | 方言对话搞笑 |
| 3 | 🐕 萌宠日常 | 小狗拆家片段 |
| 4 | 🐾 宠物变装 | 动物穿衣服走秀 |
| 5 | 🎨 自定义 | 你描述，AI 辅助生成 |

---

## 数据隐私与安全说明

### 本地存储
| 数据 | 内容 |
|------|------|
| 订单文件 `~/.openclaw/skills/orders/{indicator}/{order_no}.json` | 仅支付验证字段（订单号、金额、加密支付数据） |
| ❌ **不存储** 用户视频描述、API Key、个人身份信息 | — |

### 远程传输
- 本技能创建订单时仅发送技能标识符到 `https://api.ideaidea.com.cn`
- 视频由用户配置的 API Key 对应的平台直接生成，数据在用户与该平台之间传输
- **本技能不介入视频内容或 API Key 的网络传输**

### 绝不收集或传输
✅ 视频内容、用户 API Key、平台账号凭据、个人信息

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.0.1 | 2026-07-29 | 移除 question 参数和存储；修改触发词为需用户确认；放宽语言限制；更新隐私说明 |
| 1.0.0 | 2026-07-28 | Initial release: guided short video creation with user-provided API Key |
