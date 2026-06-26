# Follow-up Engine - 询盘跟进自动化引擎

🧠 **Wilson Evolution Phase 2 Skill**

自动化客户询盘跟进流程，基于规则引擎智能触发跟进邮件，集成 OKKI CRM 系统。

---

## 📋 功能概述

- **6 阶段客户生命周期管理**：新询盘 → 已报价 → 已样品 → 谈判中 → 成交 → 流失
- **智能规则引擎**：时间触发 + 条件判断 + 自动升级
- **自动草稿生成**：基于客户阶段自动生成个性化跟进邮件
- **OKKI 双向同步**：自动创建跟进记录，保持 CRM 数据最新
- **Discord 通知**：关键节点实时推送

---

## 📁 目录结构

```
follow-up-engine/
├── README.md              # 本文件
├── SKILL.md               # OpenClaw skill 定义
├── config/
│   ├── follow-up-rules.json      # 跟进规则配置（6 阶段、10 规则）
│   ├── stage-transitions.json    # 阶段流转模型（12 流转规则）
│   └── follow-up-strategies.json # 跟进策略模板（24 模板）
├── scripts/
│   ├── follow-up-scheduler.js    # 定时检测 + 草稿生成（400+ 行）
│   └── okki-integration.js       # OKKI 跟进记录集成（600+ 行）
├── drafts/                # 生成的跟进草稿
├── logs/                  # 运行日志
└── test/
    └── e2e.sh             # 端到端测试脚本
```

---

## 🚀 快速开始

### 1. 前置依赖

确保以下 skills 已安装并配置：
- `email-smart-reply` (task-001) - 邮件 intent 识别 + 模板系统
- `okki-email-sync` (task-002) - OKKI 双向同步

### 2. 配置检查

```bash
# 验证配置文件
node -e "JSON.parse(require('fs').readFileSync('config/follow-up-rules.json'))"
node -e "JSON.parse(require('fs').readFileSync('config/stage-transitions.json'))"
node -e "JSON.parse(require('fs').readFileSync('config/follow-up-strategies.json'))"
```

### 3. 运行定时调度器

```bash
# Dry-run 模式（预览将生成的草稿）
node scripts/follow-up-scheduler.js --dry-run

# 实际运行（生成草稿）
node scripts/follow-up-scheduler.js --mode auto

# 手动触发（立即执行）
node scripts/follow-up-scheduler.js --mode manual
```

### 4. 同步到 OKKI

```bash
# Dry-run 模式（预览将创建的 OKKI 记录）
node scripts/okki-integration.js --dry-run

# 实际同步
node scripts/okki-integration.js --sync
```

---

## ⚙️ 配置说明

### follow-up-rules.json

定义 6 个客户阶段和跟进规则：

| 阶段 ID | 名称 | 优先级 | 自动升级 |
|--------|------|--------|---------|
| new_inquiry | 新询盘 | high | 7 天无回复 → lost |
| quoted | 已报价 | high | 30 天无回复 → lost |
| sample_sent | 已样品 | medium | 14 天无反馈 → lost |
| negotiating | 谈判中 | high | 14 天停滞 → lost |
| closed_won | 成交 | low | - |
| lost | 流失 | low | - |

### follow-up-strategies.json

为每个阶段定义跟进序列：

```json
{
  "stage_id": "quoted",
  "follow_up_sequence": ["day_3", "day_7", "day_14", "day_30"],
  "templates": ["template-followup-quote-001", "..."],
  "escalation_rules": {...}
}
```

### global_settings

```json
{
  "working_hours": {
    "timezone": "Asia/Shanghai",
    "start_hour": 9,
    "end_hour": 18,
    "exclude_weekends": true
  },
  "max_follow_ups_per_stage": 3,
  "okki_sync_enabled": true,
  "require_wilson_approval_for_sending": true
}
```

---

## 📊 运行示例

### 场景 1：新询盘自动跟进

```bash
# 客户发送询盘邮件
# ↓ auto-capture.js 捕获邮件
# ↓ 客户阶段标记为 new_inquiry
# ↓ follow-up-scheduler.js 检测到 30 分钟无回复
# ↓ 生成首次回复草稿（template-inquiry-001）
# ↓ Discord 推送审阅通知
```

### 场景 2：报价后跟进序列

```bash
# 销售发送报价单
# ↓ 客户阶段更新为 quoted
# ↓ Day 3: 生成首次跟进草稿
# ↓ Day 7: 生成二次跟进草稿
# ↓ Day 14: 生成三次跟进草稿 + 升级提醒
# ↓ Day 30: 自动标记为 lost
```

### 场景 3：OKKI 同步

```bash
# follow-up-scheduler.js 生成草稿
# ↓ okki-integration.js 读取草稿
# ↓ 调用 OKKI API 创建跟进记录（trail_type=105）
# ↓ 更新草稿状态为 synced
# ↓ 记录同步日志
```

---

## 🔧 故障排查

### 问题：草稿未生成

```bash
# 检查配置文件
cat logs/scheduler-$(date +%Y-%m-%d).log

# 验证 OKKI 客户扫描
node scripts/follow-up-scheduler.js --dry-run --debug
```

### 问题：OKKI 同步失败

```bash
# 检查 OKKI CLI 连接
python3 /Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki.py --help

# 查看同步日志
cat logs/okki-integration-$(date +%Y-%m-%d).log
```

### 问题：阶段流转不正确

```bash
# 检查阶段流转规则
cat config/stage-transitions.json | jq '.transition_rules[]'

# 手动触发阶段更新
node scripts/follow-up-scheduler.js --force-stage-update
```

---

## 📈 效果指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 首次回复时间 | < 30 分钟 | 新询盘自动触发 |
| 跟进覆盖率 | 100% | 所有阶段客户 |
| OKKI 同步率 | > 95% | 草稿→跟进记录 |
| 人工审阅率 | 100% | 发送前必须确认 |

---

## 🛡️ 安全保证

- ✅ **严禁自动发送**：所有邮件发送必须经过 Discord 审阅确认
- ✅ **去重机制**：相同 UID 不重复创建跟进记录
- ✅ **工作时间限制**：仅在工作时间触发跟进（可配置）
- ✅ **日志完整**：所有操作记录到 logs/ 目录

---

## 📝 开发历史

- **2026-03-24**: Phase 2 首个 skill，6 次迭代完成
- **Subtask 1**: 跟进规则引擎配置（follow-up-rules.json）
- **Subtask 2**: 客户阶段流转模型（stage-transitions.json）
- **Subtask 3**: 跟进策略模板（follow-up-strategies.json）
- **Subtask 4**: 定时调度器（follow-up-scheduler.js）
- **Subtask 5**: OKKI 集成（okki-integration.js）

---

**Skill 版本**: 1.0  
**最后更新**: 2026-03-24  
**维护者**: Wilson Evolution System
