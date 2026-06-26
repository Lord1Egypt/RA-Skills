# 持续学习套件
## Continuous Learning Kit

让OpenClaw AI助手具备**持续学习和自我进化**的核心能力。

---

## 🌟 核心特性

### 1. 智能新任务判断
- 自动识别话题切换
- 任务类型变化检测
- 关键词追踪

### 2. MemPalace自动记录
- 每日对话自动归档
- 语义化记忆存储
- 跨会话上下文保持

### 3. 做梦分析（02:00）
- MiniMax M2.7智能分析
- 自动去重降噪
- 精华提取到5个核心文档

### 4. 自我纠错机制
- ERROR/LEARNING记录
- 避免重复错误
- 持续改进

---

## ⚠️ 前置条件（必需）

本技能包**依赖MemPalace记忆系统**，使用前必须先安装。

### 安装MemPalace

通过ClawHub安装：

```bash
clawdhub install mempalace
```

或者手动克隆技能包到你的技能目录：

```bash
cd skills/mempalace
# 确保有以下文件：
# - SKILL.md
# - scripts/mcp_server.py
# - scripts/call.py
```

### 验证MemPalace

测试连接：
```bash
python skills/mempalace/scripts/call.py mempalace_status
```

如果返回类似：
```json
{
  "status": "ready",
  "drawer_count": 1,
  "wings": ["wing_xiaolong"]
}
```

则说明安装成功。

---

## 🚀 快速开始

### 5分钟快速安装

#### 1️⃣ 初始化文件

```bash
cd <你的工作区>
python skills/continuous-learning/setup/init_learning_files.py
```

#### 2️⃣ 配置（可选）

编辑 `skills/continuous-learning/config/dream_config.json`，添加你的MiniMax API Key：

```json
{
  "analysis": {
    "model": "minimax",
    "api_key": "your_minimax_api_key_here"
  }
}
```

#### 3️⃣ 安装定时任务

**所有平台（Windows/Linux/Mac）**:
```bash
python skills/continuous-learning/setup/install_cron.py
```

**Windows用户注意**：
- 如果提示权限问题，以管理员身份运行PowerShell/CMD
- 脚本会自动检测操作系统并配置相应的定时任务

#### 4️⃣ 测试

```bash
# 测试同步
python skills\continuous-learning\sync\sync_notification.py

# 测试做梦
python skills\continuous-learning\dream\dream_cycle.py
```

---

## 📊 工作流程

```
用户消息
    ↓
新任务判断
    ↓ Yes
读取文档（SOUL/AGENTS/MEMORY/TOOLS/ERRORS/LEARNINGS）
    ↓
执行任务
    ↓
记录到MemPalace
    ↓
23:00 自动同步今日聊天
    ↓
02:00 做梦分析 → 提取精华到文档 → WeChat通知
```

---

## 📁 技能包结构

```
continuous-learning/
├── SKILL.md                        # 技能说明
├── README.md                       # 本文件
├── config/
│   ├── dream_config.json          # 做梦配置
│   └── documentation_targets.json # 文档目标
├── bootstraps/
│   └── bootstrap_rules.md         # 启动规则（会话启动时自动加载）
├── sync/
│   └── sync_notification.py       # 同步脚本（23:00）
├── dream/
│   └── dream_cycle.py             # 做梦脚本（02:00）
├── notifications/
│   └── .notification_queue.json   # 通知队列（自动生成）
└── setup/
    ├── init_learning_files.py     # 初始化学习文件
    └── install_cron.py            # 定时任务安装（跨平台）
```

---

## 🎯 使用场景

### 场景1：多项目管理

```
用户：查LIMS样本 → 做周报 → 发邮件
     ↓
AI自动识别3个不同任务
     ↓
每次都重新读取相关配置
     ↓
无缝切换，不混乱
```

### 场景2：避免重复错误

```
第1天：犯错 → 记录ERRRORS.md
第23:00：同步
第02:00：做梦分析
第3天：类似任务 → 读取LEARNINGS.md → 避免错误！
```

### 场景3：用户偏好记忆

```
第一次：用户说"叫我xiaolong"
     ↓
记录到MemPalace
     ↓
做梦分析 → 提取到SOUL.md
     ↓
后续所有对话 → 自动用"xiaolong"
```

---

## 🔧 配置说明

### dream_config.json

```json
{
  "sync_schedule": "23:00",              // 同步时间
  "dream_schedule": "02:00",             // 做梦时间
  "notification": {
    "enabled": true,                     // 启用通知
    "channel": "openclaw-weixin"         // 通知渠道
  },
  "analysis": {
    "model": "minimax",                  // 分析模型
    "timeout_seconds": 120               // 超时时间
  }
}
```

### 通知配置

支持的通知渠道：
- `openclaw-weixin` - 企业微信
- `email` - 邮件
- `None` - 不通知

---

## 📈 效果指标

| 指标 | 传统AI | 持续学习AI |
|------|--------|-----------|
| 记忆持久 | 无 | 跨会话 |
| 错误重犯 | 高 | <10% |
| 学习能力 | 无 | 自动 |
| 用户偏好 | 不知道 | 自动记忆 |

---

## 🐛 故障排查

### 定时任务不执行

**Windows**:
```powershell
schtasks /query /tn "OpenClaw-ContinuousSync"
```

**Linux**:
```bash
crontab -l
```

### MemPalace写入失败

检查：
- ChromaDB路径
- 写入权限
- 日志文件

### 做梦无更新

检查：
- API Key有效性
- 记忆碎片数量
- 提示词配置

---

## 📚 相关技能

- **mempalace** - 记忆 palace（必需）
- **self-improving-agent** - 互补的自我改进功能

---

## 📝 格式示例

### ERRORS.md

```markdown
### 错误：API字段猜测
**错误**: 猜测用 sampleBaseUuid
**正确**: 应该用 sampleBaseTestingUuid
**教训**: 先验证，不要猜测
**日期**: 2026-04-10
```

### LEARNINGS.md

```markdown
### 学习：登录握手
**收获**: 先GET再POST
**应用**: LIMS登录、企业微信认证
**日期**: 2026-04-10
```

---

## 🤝 贡献

欢迎提交PR和Issue！

---

**版本**: 1.0.0
**作者**: 小麦 (Xiaomai) 🌾
**许可证**: MIT
**维护**: OpenClaw社区 Discord
