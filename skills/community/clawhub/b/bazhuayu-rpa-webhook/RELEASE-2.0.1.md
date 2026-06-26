# Release Notes - v2.0.1

**发布日期**: 2026-03-08  
**类型**: 安全优化版本

---

## 📋 变更概述

v2.0.1 是针对 v2.0 的安全优化版本，主要解决用户反馈的以下问题：

1. **元数据不匹配** - 环境变量声明与实际要求不一致
2. **脚本过于侵入性** - 自动修改用户 shell 配置文件
3. **文档不够清晰** - 缺少手动配置指南

---

## 🔧 修复内容

### 1. 修复环境变量元数据

**问题**: `package.json` 中环境变量标记为"可选"，但实际为必需

**修复**:
```json
// 修改前
"env": [
  "BAZHUAYU_WEBHOOK_URL (可选)",
  "BAZHUAYU_WEBHOOK_KEY (可选)"
]

// 修改后
"env": [
  "BAZHUAYU_WEBHOOK_URL (必需)",
  "BAZHUAYU_WEBHOOK_KEY (必需)"
]
```

### 2. 移除脚本自动修改 shell 配置功能

**文件**: `setup-secure.sh`, `migrate-to-env.sh`

**变更**:
- ❌ 移除自动 `>> ~/.bashrc` / `~/.zshrc` 追加配置
- ❌ 移除自动 `sed -i` 修改 shell 配置文件
- ✅ 新增脚本开头警告提示，明确告知用户不会自动修改
- ✅ 新增生成 `.env.example` / `.env.migrated` 配置示例文件
- ✅ 新增明确的手动配置指引
- ✅ 保留可选的当前会话临时设置

### 3. 新增文档

**新增文件**:
- `MANUAL_SETUP.md` - 详细的手动配置指南（Linux/macOS/Windows）
- `CHANGES-v2.0.md` - 变更说明文档

**更新文件**:
- `SKILL.md` - 新增「⚠️ 使用前必读」章节
- `README.md` - 更新配置步骤说明
- `QUICKSTART.md` - 更新配置向导说明
- `.gitignore` - 新增 `.env.example` 和 `.env.migrated`

---

## 📦 升级指南

### 从 v2.0 升级

直接覆盖文件即可，配置保持不变：

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook

# 备份现有配置（可选）
cp config.json config.json.backup

# 复制新文件（保留 config.json）
# 从 ClawHub 或手动复制更新的文件
```

### 从 v1.x 升级

建议重新运行配置向导：

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook
./setup-secure.sh
```

---

## ✅ 验证清单

升级后请验证：

- [ ] `python3 bazhuayu-webhook.py secure-check` 无警告
- [ ] `python3 bazhuayu-webhook.py test` 成功
- [ ] 环境变量已正确设置

---

## 🔄 版本规范

从 v2.0.1 开始，采用语义化版本号：

- **主版本**.x.x - 重大变更/不兼容更新
- x.**次版本**.x - 新功能/安全增强
- x.x.**修订号** - Bug 修复/小优化

下次发布版本号为 **v2.0.2**

---

**感谢用户反馈帮助改进！**
