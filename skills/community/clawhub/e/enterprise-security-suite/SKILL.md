---
name: Enterprise Security
slug: enterprise-security
version: 1.0.0
description: 企业级安全套件 - 高危操作确认、自动备份、回滚机制、技能安检
author: Cloud
tags: [security, backup, rollback, vetting, enterprise]
---

# 企业级安全套件 (Enterprise Security)

**版本**: 1.0.0  
**作者**: Cloud  
**适用**: OpenClaw Agent / 企业级 / 个人开发者

---

## 🛡️ 功能

### 1. 高危操作确认

7 类高危操作前自动提示确认：
- ✅ 修改任何 MD 文件
- ✅ 安装/卸载/更新 skill
- ✅ 重启 Gateway
- ✅ 删除文件/目录
- ✅ 创建/修改/删除 cron 任务
- ✅ 修改环境变量/API 密钥
- ✅ 发送外部消息

### 2. 自动备份

修改文件前自动创建备份：
- 支持 .md/.json/.js/.ts/.py 等文件
- 命名格式：`文件名.YYYYMMDD.NNN.bak`
- 自动清理过期备份

### 3. 变更日志

自动记录所有高危操作到 CHANGELOG.md：
- 操作类型
- 修改原因
- 执行者
- 回滚方法

### 4. 回滚机制

支持从备份文件恢复：
- 一键回滚
- 自动备份回滚前状态
- 记录回滚日志

### 5. 技能安装安检

安装 skill 前自动检查：
- 来源验证
- 代码审查
- 依赖检查
- 权限评估
- 风险等级判定

---

## 🚀 安装

```bash
# 1. 安装 Skill
clawhub install enterprise-security

# 2. 激活（写入安全规则到记忆）
node ~/.openclaw/workspace/skills/enterprise-security/activate.js

# 3. 重启 Gateway
openclaw gateway restart
```

**完成！** AI 会自动执行安全检查。

---

## 🔧 使用

### 方式 1：AI 自动调用（推荐）

激活后，AI 会自动在执行高危操作前调用：

```
AI 准备修改文件 → 自动调用 confirmHighRisk → 用户确认 → 执行
```

### 方式 2：手动调用

```javascript
const security = require('./skills/enterprise-security');

// 高危操作确认
await security.confirmHighRisk({
  operation: 'modify_file',
  file: 'MEMORY.md',
  reason: '更新记忆系统'
});

// 自动备份
await security.autoBackup({
  filePath: '~/.openclaw/workspace/SOUL.md',
  reason: '修改前备份'
});

// 技能安检
const result = await security.checkSkill({
  skillName: 'new-skill',
  author: 'community-user',
  repository: 'github.com/user/new-skill'
});

if (result.risk === 'high') {
  throw new Error('高风险技能，拒绝安装');
}

// 回滚
await security.rollback({
  file: 'MEMORY.md',
  targetVersion: '20260311.001',
  reason: '用户要求回滚'
});
```

---

## 📝 配置

编辑 `config/rules.json`：

```json
{
  "high_risk_operations": [
    "modify_md_files",
    "install_skills",
    "restart_gateway",
    "delete_files",
    "modify_cron",
    "modify_env",
    "send_external_messages"
  ],
  "auto_backup": {
    "enabled": true,
    "file_types": [".md", ".json", ".js", ".ts", ".py"],
    "max_backups_per_file": 10
  },
  "changelog": {
    "enabled": true,
    "path": "memory/CHANGELOG.md"
  },
  "security_check": {
    "enabled": true,
    "whitelist": ["github.com/openclaw"]
  }
}
```

---

## 📊 API 参考

### confirmHighRisk(options)

高危操作确认

```javascript
await security.confirmHighRisk({
  operation: 'modify_file',  // 操作类型
  file: 'test.md',           // 涉及文件（可选）
  reason: '更新配置'          // 原因（可选）
});
```

### autoBackup(options)

自动备份

```javascript
await security.autoBackup({
  filePath: 'test.md',       // 文件路径
  reason: '修改前备份'        // 原因（可选）
});
```

### checkSkill(options)

技能安装安检

```javascript
const result = await security.checkSkill({
  skillName: 'new-skill',
  author: 'user',
  repository: 'github.com/user/skill',
  permissions: ['read_file'],
  dependencies: []
});

console.log(result.risk);  // low/medium/high
console.log(result.recommendations);
```

### rollback(options)

回滚操作

```javascript
await security.rollback({
  file: 'test.md',           // 文件路径
  targetVersion: '20260311.001',  // 目标版本
  reason: '用户要求回滚'      // 原因
});
```

---

## 📝 更新日志

### v1.0.0 (2026-03-11)
- ✅ 初始版本
- ✅ 高危操作确认
- ✅ 自动备份
- ✅ 变更日志
- ✅ 回滚机制
- ✅ 技能安装安检

---

## 📞 联系方式

- **作者**: Cloud
- **GitHub**: [待填写]

---

## 📄 许可证

MIT License
