# Release Notes - v2.0.2

**发布日期**: 2026-03-08  
**类型**: 日志安全修复版本

---

## 📋 变更概述

v2.0.2 是针对 v2.0.1 的快速修复版本，解决用户反馈的两个安全问题：

1. **SKILL.md 元数据不完整** - 缺少环境变量声明
2. **日志文件权限未加固** - `run.log` 可能以默认权限创建

---

## 🔧 修复内容

### 1. 完善 SKILL.md 元数据

**问题**: SKILL.md 的 metadata 中未声明必需的环境变量

**修复**:
```yaml
# 修改前
metadata: {"clawdbot":{"emoji":"🐙","requires":{"bins":["python3"]},...}}

# 修改后
metadata: {
  "clawdbot":{
    "emoji":"🐙",
    "requires":{
      "bins":["python3"],
      "env":["BAZHUAYU_WEBHOOK_URL","BAZHUAYU_WEBHOOK_KEY"]
    },
    "primaryEnv":"BAZHUAYU_WEBHOOK_KEY",
    ...
  }
}
```

**影响**: 
- ✅ ClawHub/ClawDBot 现在能正确识别必需的环境变量
- ✅ 用户在安装时会看到明确的环境变量提示

### 2. 修复日志文件权限

**问题**: `run_daily.sh` 创建日志文件时未设置安全权限

**修复**:

**run_daily.sh**:
```bash
# 新增：确保日志文件存在并设置安全权限 (600)
touch "$LOG_FILE"
chmod 600 "$LOG_FILE"

# ... 运行日志记录 ...

# 新增：再次确保日志文件权限正确（防止被重新创建）
chmod 600 "$LOG_FILE"
```

**bazhuayu-webhook.py** (secure-check 命令):
```python
# 修改前：只检查不修复
if log_perms != '600':
    issues.append(f"日志文件 {log_file.name} 权限不安全 ({log_perms})")

# 修改后：自动修复
if log_perms != '600':
    try:
        os.chmod(log_file, stat.S_IRUSR | stat.S_IWUSR)
        print(f"✅ 已修复 {log_file.name} 权限 ({log_perms} → 600)")
    except Exception as e:
        issues.append(f"日志文件 {log_file.name} 权限不安全 ({log_perms}) 且无法自动修复")
```

**影响**:
- ✅ 日志文件自动设置为 600 权限（仅所有者可读写）
- ✅ `secure-check` 命令会自动修复日志权限问题
- ✅ 防止敏感日志信息泄露

---

## 📦 升级指南

### 从 v2.0.1 升级

直接覆盖文件即可：

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook

# 复制新文件（保留 config.json）
# 从 ClawHub 或手动复制更新的文件
```

### 手动修复日志权限

如果已有日志文件，建议手动修复权限：

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook
chmod 600 *.log

# 或运行安全检查自动修复
python3 bazhuayu-webhook.py secure-check
```

---

## ✅ 验证清单

升级后请验证：

- [ ] `python3 bazhuayu-webhook.py secure-check` 无警告
- [ ] `ls -la *.log` 显示权限为 600
- [ ] `./run_daily.sh` 运行后日志权限正确

---

## 🔄 版本规范

采用语义化版本号：

- **主版本**.x.x - 重大变更/不兼容更新
- x.**次版本**.x - 新功能/安全增强
- x.x.**修订号** - Bug 修复/小优化

下次发布版本号为 **v2.0.3**

---

**感谢用户反馈帮助改进！**
