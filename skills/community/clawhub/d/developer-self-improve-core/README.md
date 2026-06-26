# 🛡️ developer-self-improve-core

**开发者自改进核心技能 - v1.1.9**

---

## 核心理念

> **AI 只提议，人类终审**

- ✅ AI 可自动反思、生成规则草案、提出清洗建议
- ✅ 绝不自动写入长期记忆、不自动删除/合并任何规则
- ✅ 所有涉及记忆修改的操作，必须经人类终审确认

---

## 🚀 快速开始

### 1. 安装

```bash
clawhub install developer-self-improve-core
```

### 2. 初始测试（推荐）

**首次安装后，默认已禁用自动化功能（安全模式）：**

```yaml
# config/config.yaml
enable_reminder: false      # 默认：false
enable_auto_cleanup: false  # 默认：false
```

**手动测试功能：**
```bash
./scripts/developer-self-improve-core.sh init
./scripts/developer-self-improve-core.sh pre-check "测试场景"
./scripts/developer-self-improve-core.sh post-check "测试内容" "测试"
```

### 3. 启用自动化（可选）

**测试确认无误后：**

1. **配置钉钉账号（如需定时提醒）：**
   ```bash
   vi config/config.yaml
   ```
   ```yaml
   dingtalk_target: "你的钉钉 ID"
   enable_reminder: true
   ```

2. **配置 crontab（如需定时提醒）：**
   ```bash
   crontab -e
   # 30 9 * * * cd /path/to/skill && ./scripts/daily-check.sh
   ```

---

## 📚 详细文档

- **SKILL.md** - 技能元数据和使用说明
- **SECURITY.md** - 安全说明和测试指导
- **config/config.yaml** - 配置文件

---

## 🔒 安全特性

| 特性 | 说明 |
|------|------|
| **人类终审** | 所有记忆修改需用户确认 |
| **默认禁用** | 定时提醒和自动清理默认禁用 |
| **透明操作** | 所有操作记录在日志中 |
| **可备份恢复** | 支持备份技能目录 |

---

## 📋 核心功能

- ✅ 多层次记忆管理（短期/临时提案/长期规则）
- ✅ AI 自动反思与规则草案生成
- ✅ 人类终审确认机制
- ✅ 定期记忆清洗（可选）
- ✅ 错误防重机制
- ✅ Token 优化策略
- ✅ 定时提醒（可选）

---

## 🛠️ 常用命令

```bash
# 初始化
./scripts/developer-self-improve-core.sh init

# 回答前检查
./scripts/developer-self-improve-core.sh pre-check "场景"

# 回答后检查
./scripts/developer-self-improve-core.sh post-check "内容" "场景"

# 确认规则
./scripts/developer-self-improve-core.sh confirm [规则 ID] 同意

# 清理记忆
./scripts/developer-self-improve-core.sh cleanup

# 切换平台
./scripts/developer-self-improve-core.sh switch-platform ios
```

---

## 📄 许可证

MIT License

---

**版本：** 1.1.9  
**作者：** lijiujiu
