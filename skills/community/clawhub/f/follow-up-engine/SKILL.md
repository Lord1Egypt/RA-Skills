---
name: follow-up-engine
description: "Automated customer follow-up scheduling and execution engine for B2B sales. Generates personalized follow-up email drafts based on customer stage, last contact date, and follow-up strategy. Integrates with CRM systems (configurable) to sync follow-up records. Use when you need to automate outbound sales follow-ups, schedule reminders, or generate follow-up email content for dormant leads."
---
# Follow-up Engine - OpenClaw Skill 定义

## 技能描述

自动化客户询盘跟进规则引擎，基于配置的时间触发器和条件判断，智能生成跟进邮件草稿并同步到 OKKI CRM。

---

## 触发条件

### 定时触发（Cron）

```bash
# 每 30 分钟执行一次检测
*/30 * * * * cd $WORKSPACE/skills/follow-up-engine && node scripts/follow-up-scheduler.js --mode auto >> /tmp/follow-up-scheduler.log 2>&1

# 每小时执行一次 OKKI 同步
0 * * * * cd $WORKSPACE/skills/follow-up-engine && node scripts/okki-integration.js --sync >> /tmp/okki-integration.log 2>&1
```

### 事件触发

- **新询盘邮件到达** → 触发 new_inquiry 阶段跟进流程
- **报价单发送完成** → 触发 quoted 阶段跟进序列
- **样品寄送确认** → 触发 sample_sent 阶段跟进
- **OKKI 跟进记录创建** → 触发阶段流转检测

---

## 执行逻辑

### 1. Follow-up Scheduler 流程

```
1. 加载配置
   ↓
2. 扫描 OKKI 客户列表
   ↓
3. 识别每个客户当前阶段
   ↓
4. 计算下次跟进时间
   ↓
5. 匹配到期需要跟进的客户
   ↓
6. 生成跟进邮件草稿
   ↓
7. 保存到 drafts/ 目录
   ↓
8. 记录执行日志
```

### 2. OKKI Integration 流程

```
1. 读取 drafts/ 目录草稿
   ↓
2. 过滤已同步草稿（status != synced）
   ↓
3. 匹配 OKKI 客户（域名搜索 + 名称搜索）
   ↓
4. 调用 OKKI API 创建跟进记录
   ↓
5. 更新草稿状态为 synced
   ↓
6. 记录同步日志
```

---

## 输入输出

### 输入

| 来源 | 数据类型 | 说明 |
|------|---------|------|
| OKKI API | 客户列表 | 客户邮箱、公司名称、阶段 |
| follow-up-strategies.json | 配置 | 跟进序列、模板、升级规则 |
| task-001 email-smart-reply | 模板系统 | 邮件模板内容 |

### 输出

| 目标 | 数据类型 | 说明 |
|------|---------|------|
| drafts/ | JSON 文件 | 跟进邮件草稿 |
| OKKI API | 跟进记录 | trail_type=105 |
| logs/ | 日志文件 | 执行记录、错误信息 |
| Discord | 通知消息 | 待审阅草稿提醒 |

---

## 配置项

### 环境变量

```bash
# OKKI CLI 路径
export OKKI_CLI_PATH="$WORKSPACE/xiaoman-okki/api/okki.py"

# Discord Bot Token（通知用）
export DISCORD_BOT_TOKEN="your-discord-bot-token-here"

# 通知频道 ID
export DISCORD_CHANNEL_ID="<your-discord-channel-id>"
```

### 配置文件

| 文件 | 用途 | 必填 |
|------|------|------|
| config/follow-up-rules.json | 跟进规则定义 | ✅ |
| config/stage-transitions.json | 阶段流转模型 | ✅ |
| config/follow-up-strategies.json | 跟进策略模板 | ✅ |

---

## CLI 命令

### follow-up-scheduler.js

```bash
# Dry-run 模式（预览）
node scripts/follow-up-scheduler.js --dry-run

# 自动模式（定时触发）
node scripts/follow-up-scheduler.js --mode auto

# 手动模式（立即执行）
node scripts/follow-up-scheduler.js --mode manual

# 调试模式（详细日志）
node scripts/follow-up-scheduler.js --debug

# 强制更新阶段
node scripts/follow-up-scheduler.js --force-stage-update
```

### okki-integration.js

```bash
# Dry-run 模式（预览）
node scripts/okki-integration.js --dry-run

# 同步模式（实际创建 OKKI 记录）
node scripts/okki-integration.js --sync

# 批量同步（指定草稿文件）
node scripts/okki-integration.js --batch drafts/*.json

# 查看同步日志
node scripts/okki-integration.js --logs
```

---

## 依赖关系

### 上游依赖

| Skill | 用途 | 必须 |
|-------|------|------|
| email-smart-reply (task-001) | 邮件模板系统 | ✅ |
| okki-email-sync (task-002) | OKKI API 封装 | ✅ |

### 下游集成

| 目标 | 用途 | 必须 |
|------|------|------|
| OKKI CRM | 客户数据 + 跟进记录 | ✅ |
| Discord | 审阅通知 | ✅ |
| Obsidian | 日志归档 | ❌ |

---

## 错误处理

### 常见错误码

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| CONFIG_NOT_FOUND | 配置文件缺失 | 检查 config/ 目录 |
| OKKI_AUTH_FAILED | OKKI 认证失败 | 检查 okki.py 配置 |
| NO_CUSTOMERS_FOUND | 未找到客户 | 检查 OKKI 连接 |
| TEMPLATE_NOT_FOUND | 模板不存在 | 检查 email-smart-reply |

### 降级策略

1. **OKKI 不可用** → 使用本地缓存客户列表
2. **模板不可用** → 使用默认跟进模板
3. **Discord 不可用** → 日志记录 + 本地通知文件

---

## 测试

### 单元测试

```bash
# 测试配置文件
node -e "JSON.parse(require('fs').readFileSync('config/follow-up-rules.json'))" && echo "✓ follow-up-rules.json valid"
node -e "JSON.parse(require('fs').readFileSync('config/stage-transitions.json'))" && echo "✓ stage-transitions.json valid"
node -e "JSON.parse(require('fs').readFileSync('config/follow-up-strategies.json'))" && echo "✓ follow-up-strategies.json valid"
```

### 端到端测试

```bash
# 运行 E2E 测试
bash test/e2e.sh

# 预期输出：
# ✓ 配置文件验证通过
# ✓ 模拟客户创建成功
# ✓ 草稿生成成功（3 封）
# ✓ OKKI 同步成功（dry-run）
# ✓ 日志记录完整
```

---

## 性能指标

| 指标 | 目标值 | 实测值 |
|------|--------|--------|
| 客户扫描速度 | > 100 客户/秒 | TBD |
| 草稿生成时间 | < 1 秒/草稿 | TBD |
| OKKI 同步速度 | > 10 记录/秒 | TBD |
| 内存占用 | < 100MB | TBD |

---

## 安全规范

- ✅ 所有配置文件使用 JSON 格式（无代码注入风险）
- ✅ OKKI API 调用使用官方 CLI（不直接暴露 API Key）
- ✅ 日志脱敏处理（隐藏客户邮箱等敏感信息）
- ✅ 发送前必须人工审阅（严禁自动盲发）

---

**Skill 版本**: 1.0  
**创建日期**: 2026-03-24  
**维护者**: Wilson Evolution System
