# Release Notes - v2.0.4

**发布日期**: 2026-03-08  
**类型**: 图文教程版本

---

## 📋 变更概述

v2.0.4 新增**Webhook 设置图文教程**，帮助用户快速了解如何在八爪鱼 RPA 中创建和配置 Webhook 触发器。

---

## 📸 新增内容

### 1. WEBHOOK_SETUP.md（新增文件）

详细的图文教程，包含：

- ✅ **步骤 1**：进入触发器管理
- ✅ **步骤 2**：创建 Webhook 触发器
- ✅ **步骤 3**：填写触发器信息（名称、机器人、应用）
- ✅ **步骤 4**：获取 Webhook URL 和签名密钥
- ✅ **步骤 5**：启动触发器
- ✅ **验证方法**：如何确认 Webhook 已生效
- ✅ **常见问题**：FAQ 和故障排查

### 2. 配套截图（images/ 目录）

| 文件 | 说明 |
|------|------|
| `webhook-setup-1.jpg` | 步骤 1：进入触发器管理 |
| `webhook-setup-2.jpg` | 步骤 2：创建触发器 |
| `webhook-setup-3.jpg` | 步骤 3：填写信息 |

### 3. 更新现有文档

| 文件 | 更新内容 |
|------|----------|
| `README.md` | 新增"第一步：获取 Webhook URL 和签名"章节 |
| `QUICKSTART.md` | 新增"第一步：获取 Webhook URL 和签名"章节 |
| `MANUAL.md` | 更新"配置八爪鱼 RPA 端"章节，添加详细步骤 |

---

## 📖 教程结构

```
bazhuayu-webhook/
├── README.md              # 包含 Webhook 获取步骤
├── QUICKSTART.md          # 包含 Webhook 获取步骤
├── WEBHOOK_SETUP.md       # ⭐ 完整图文教程（新增）
├── MANUAL.md              # 包含详细配置说明
└── images/
    ├── webhook-setup-1.jpg
    ├── webhook-setup-2.jpg
    └── webhook-setup-3.jpg
```

---

## 🎯 用户体验改进

### 修改前
- 用户需要自行查找如何创建 Webhook
- 缺少可视化指导
- 可能遗漏关键步骤（如"启动触发器"）

### 修改后
- ✅ 清晰的图文教程，步步引导
- ✅ 关键步骤有醒目标记（⚠️ 重要提示）
- ✅ 包含验证方法和故障排查
- ✅ 截图直观展示界面和操作

---

## 📦 升级指南

### 从 v2.x 升级

```bash
# 方式 1: ClawHub 更新
clawhub update bazhuayu-rpa-webhook

# 方式 2: 手动覆盖
cd ~/.openclaw/workspace/skills/
# 复制新文件到 bazhuayu-rpa-webhook 目录
```

---

## ✅ 验证清单

升级后请验证：

- [ ] `WEBHOOK_SETUP.md` 文件存在
- [ ] `images/` 目录包含 3 张截图
- [ ] `README.md` 包含 Webhook 获取步骤
- [ ] `QUICKSTART.md` 包含 Webhook 获取步骤

---

## 🔄 版本规范

采用语义化版本号：

- **主版本**.x.x - 重大变更/不兼容更新
- x.**次版本**.x - 新功能/安全增强
- x.x.**修订号** - Bug 修复/小优化

下次发布版本号为 **v2.0.5**

---

**图文教程，让配置更简单！** 🎉
