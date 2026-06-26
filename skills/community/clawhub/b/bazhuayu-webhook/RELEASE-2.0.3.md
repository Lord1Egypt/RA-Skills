# Release Notes - v2.0.3

**发布日期**: 2026-03-08  
**类型**: 名称优化版本

---

## 📋 变更概述

v2.0.3 是名称优化版本，在 skill 名称中添加 **RPA** 关键词，便于用户在 ClawHub 上搜索和发现。

---

## 🔧 修改内容

### 1. package.json

```json
// 修改前
{
  "name": "bazhuayu-webhook",
  "version": "2.0.2"
}

// 修改后
{
  "name": "bazhuayu-rpa-webhook",
  "version": "2.0.3"
}
```

### 2. SKILL.md

```yaml
# 修改前
name: bazhuayu-webhook

# 修改后
name: bazhuayu-rpa-webhook
```

### 3. 安装说明

```bash
# 修改前
clawhub install bazhuayu-webhook

# 修改后
clawhub install bazhuayu-rpa-webhook
```

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

### 目录名称

**建议**将目录重命名为 `bazhuayu-rpa-webhook`：

```bash
cd ~/.openclaw/workspace/skills/
mv bazhuayu-webhook bazhuayu-rpa-webhook
```

**注意**: 如果已有 crontab 或脚本引用旧目录名，需要同步更新。

---

## ✅ 验证清单

升级后请验证：

- [ ] `clawhub list` 显示 `bazhuayu-rpa-webhook@2.0.3`
- [ ] `python3 bazhuayu-rpa-webhook.py --help` 正常运行
- [ ] 更新 crontab 或脚本中的目录引用（如有）

---

## 🔄 版本规范

采用语义化版本号：

- **主版本**.x.x - 重大变更/不兼容更新
- x.**次版本**.x - 新功能/安全增强
- x.x.**修订号** - Bug 修复/小优化

下次发布版本号为 **v2.0.4**

---

**名称优化，便于搜索！** 🎉
