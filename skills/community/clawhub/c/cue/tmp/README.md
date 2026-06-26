# Cue v1.0.3 - 最终部署包 / Deployment Package

## 📦 完整文件清单 / File Structure

```
cue/
├── manifest.json              # 技能清单（tags 定义，确保与 SKILL.md 一致）
├── SKILL.md                   # 技能描述（双语）
├── package.json               # npm 配置
├── crontab.txt               # 监控调度配置
├── UPDATE_GUIDE.md           # 更新说明
├── PUBLISH_CHECKLIST.md      # 发布检查清单
├── README.md                 # 本文件
└── scripts/
    ├── cue.sh                # 主入口（智能路由、欢迎引导）
    ├── research.sh           # 研究执行（60分钟超时）
    ├── notifier.sh           # 完成通知（分享链接提取）
    ├── cuecue-client.js      # 内置 API 客户端
    ├── create-monitor.sh     # 监控项创建
    ├── monitor-daemon.sh     # 监控守护进程
    ├── monitor-notify.sh     # 监控触发通知
    ├── executor/
    │   ├── monitor-engine.sh   # 监控执行主控
    │   ├── search-executor.sh  # 搜索执行器
    │   └── browser-executor.sh # 浏览器执行器
    └── dev/                  # 开发用脚本（不在发布包中）
        ├── publish-check.sh  # 发布前检查
        └── test.sh           # 集成测试
```

## 🎯 核心功能 / Core Features

### 1. 深度研究 / Deep Research
- 40-60 分钟生成专业分析报告 / Generate professional analysis report in 40-60 minutes
- 支持多种研究视角 / Support multiple research perspectives (advisor/researcher/fund-manager)
- 60 分钟超时保护 / 60-minute timeout protection

### 2. 智能监控 / Smart Monitoring
```
研究完成
    ↓
AI 分析生成监控建议
    ↓
回复 Y 创建监控项
    ↓
监控守护进程每30分钟执行
    ↓
Search → Browser 级联获取数据
    ↓
条件评估 → 触发通知
```

### 3. 用户体验优化 / UX Enhancements
- 🎉 **首次欢迎 / First-time Welcome**：自动识别新用户，发送欢迎消息 / Auto-detect new users and send welcome message
- 📋 **注册引导 / Onboarding**：3步骤 API Key 配置引导 / 3-step API Key configuration guide
- 📊 **详细进度 / Detailed Progress**：4阶段进度说明 / 4-stage progress (0-10/10-30/30-50/50-60 min)
- 🔔 **简化通知 / Simplified Notification**：核心信息 + 监控建议 / Core info + monitoring suggestions
- 🔒 **数据隔离 / Data Isolation**：多用户时数据安全隔离 / Secure data isolation for multi-user

## 🚀 部署步骤 / Deployment Steps

### 步骤 1：安装技能 / Step 1: Install Skill

```bash
# 通过 clawhub 安装（推荐）
clawhub install cue

# 或手动复制到系统路径
cp -r cue /usr/lib/node_modules/openclaw/skills/
```

### 步骤 2：配置环境变量 / Step 2: Configure Environment Variables

必需 / Required：
```bash
export CUECUE_API_KEY="your-cuecue-api-key"
```

通知配置（复用 OpenClaw 环境）/ Notification (Reuse OpenClaw Env)：
```bash
# Skill 会自动使用你已配置的 OpenClaw Channel 设置
# 如需修改通知渠道，请配置 OpenClaw 环境变量：
# https://docs.openclaw.ai/configuration/channels
```

### 步骤 3：设置调度（监控功能必需）/ Step 3: Setup Scheduling (Required for Monitoring)

```bash
# 添加 crontab
cat cue/crontab.txt | crontab -

# 验证
crontab -l
```

### 步骤 4：检查依赖

```bash
# 必需
which jq || apt-get install -y jq
which curl || apt-get install -y curl

# 可选（用于提取分享链接）
npm install -g @playwright/test
npx playwright install chromium
```

### 步骤 5：重启 OpenClaw

```bash
openclaw restart
```

## ✅ 功能验证

### 基础功能测试
```bash
# 1. 首次使用（应显示欢迎消息）
/cue

# 2. 启动研究
/cue 宁德时代2024财报

# 3. 查看任务
/ct

# 4. 查看任务详情
/cs <task_id>
```

### 监控功能测试
```bash
# 1. 研究完成后回复 Y（应创建监控项）
Y

# 2. 手动执行监控检查
./scripts/monitor-daemon.sh

# 3. 查看监控日志
tail ~/.cuecue/logs/monitor-daemon.log
```

## 🔧 关键配置

### 核心参数
| 参数 | 值 | 说明 |
|------|-----|------|
| 研究超时 | 3600秒 (60分钟) | 深度研究时间上限 |
| 进度推送 | 300秒 (5分钟) | 进度更新频率 |
| 监控调度 | 30分钟 | 监控检查频率 |
| BASE_URL | https://cuecue.cn | 硬编码，无需配置 |

### 数据存储结构
```
~/.cuecue/
├── users/
│   └── ${chat_id}/
│       ├── .initialized
│       ├── tasks/           # 用户专属任务
│       └── monitors/        # 用户专属监控
└── logs/
    ├── cue-YYYYMMDD.log
    ├── research-YYYYMMDD.log
    └── monitor-daemon.log
```

## 📋 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 脚本无权限 | 未设置可执行 | `chmod +x scripts/*.sh scripts/executor/*.sh` |
| jq 未找到 | 缺少依赖 | `apt-get install -y jq` |
| 通知未发送 | Token 未配置 | 检查 FEISHU_BOT_TOKEN 等环境变量 |
| 监控不执行 | crontab 未设置 | 执行 `crontab crontab.txt` |
| 数据不隔离 | 旧版本数据 | 清理 ~/.cuecue/ 重新初始化 |

## 🔄 版本对比

### v1.0.3 vs v1.0.1

| 功能 | v1.0.1 | v1.0.3 |
|------|--------|--------|
| 产品名称 | 投研搭子 | **调研助理** |
| 首次欢迎 | ❌ | ✅ |
| API Key 引导 | ❌ | ✅ |
| 详细进度 | ❌ | ✅ |
| 数据隔离 | ❌ | ✅ |
| 监控执行引擎 | ✅ | ✅ |
| Y/N 自动创建 | ✅ | ✅ |
| 分享链接提取 | 部分 | ✅ 完整 |

## 📝 更新日志

### v1.0.3 (2026-02-24)

**Bug 修复：**
- 🔧 修复 API 调用错误（使用内置 cuecue-client.js）
- 🔧 修复 PID 获取污染问题（nohup + pgrep）
- 🔧 修复输出文件分离导致的 notifier 错误
- 🔧 修复退出码标记格式不一致
- 🔧 修复 JSON_RESULT 输出问题

**新增组件：**
- ✨ 内置 Node.js API 客户端（无额外依赖）

### v1.0.1 (2026-02-24)

**新增功能：**
- ✨ 产品定位：投研搭子 → 调研助理
- 🎉 首次欢迎消息和 API Key 注册引导
- 📊 4阶段详细进度描述
- 🔒 多用户数据隔离
- 🏷️ Tags 优化：7个核心标签

**优化改进：**
- ⏱️ 超时：30min → 60min
- 📢 进度推送：新增每5分钟推送
- 🔔 通知格式：简化信息展示
- 🔗 分享链接：Playwright + fallback

---

*Cue v1.0.3 - 让 AI 成为你的调研助理 (Powered by CueCue)*
