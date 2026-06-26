# 🛡️ Autofix + Watchdog

**OpenClaw 故障诊断修复技能 + Gateway 健康监控守护进程。**

当组件出现问题时——Gateway 无法启动、工具返回错误、配置异常——本技能执行结构化的诊断流程来定位根因、修复、验证。可选的 Watchdog 守护进程在后台持续监控 Gateway 健康状态，发现异常时实时通知。

---

## ✨ 功能特性

### 自动诊断 (v6.1)
- **统一诊断流水线** — 3 个数据源一次搞定（`gateway status` + 运行时检查 + 密钥验证）
- **`openclaw doctor` 降级机制** — 12 秒超时后自动降级到 `gateway status --json`（解决 v2026.5.20 下 doctor 挂死问题）
- **安全子进程清理** — 所有命令使用 `taskkill /T /F` 防止 Windows 僵尸进程
- **交互式健康仪表盘** — HTML 仪表盘，支持 Canvas 嵌入（`health_dashboard.py --canvas`）
- **回归对比** — `--save-baseline` / `--compare` 追踪修复前后的变化

### 自动修复 (v1.1)
- **Gateway 安全重启** — 使用 `taskkill + start` 替代 `openclaw gateway restart`（后者在 v2026.5.20 下会挂死）
- **Session 归档** — 积压超过 100 个时自动归档 7 天前的文件到 `archive/`
- **Gateway 内存告警** — 超过 800MB 时建议重启
- **修复验证轮询** — 修复后每 5 秒检查一次 Gateway 状态（最多 30 秒）

### Watchdog 守护进程 *(可选)*
- **实时健康监控** — 每 60 秒轮询 Gateway
- **双通道通知** — WebChat 会话（异步，约40秒）+ **飞书直消息（即时）**
- **严重性分级** — 四等级告警（🟢/🟡/🟠/🔴）带噪音过滤
- **自动修复** — 低风险问题（CLI 路径、Session 归档）自动处理
- **残留进程清理** — 启动时自动查杀孤儿 daemon 进程
- **`--status` 命令** — 快速查看状态，不会误启动新实例
- **单实例保护** — Windows Mutex 防止重复运行
- **开机自启** — 注册到 `HKCU\Run`

---

## 🚀 快速开始

### 直接告诉你的 Agent：

```
run autofix self-check
check what's wrong with Gateway
auto repair
```

### 推荐的一键诊断：

```bash
python scripts/diagnosis_formatter.py --json       # 统一诊断
python scripts/health_dashboard.py --canvas         # 可视化仪表盘
```

> ⚠️ **v2026.5.20 注意：** `openclaw doctor` 会挂死。流水线 12 秒后自动降级到 `gateway status --json`。

---

## 📦 安装

```bash
clawhub install autofix
```

然后重启 OpenClaw 加载技能。

### Watchdog 守护进程 *(可选)*

```bash
pip install -r scripts/requirements.txt
python scripts/watchdog_monitor.py                  # 启动守护进程
python scripts/watchdog_monitor.py --status         # 查看状态
python scripts/watchdog_monitor.py --install        # 开机自启
```

详见 [`INSTALL.md`](./INSTALL.md) 完整安装说明。

---

## 🔔 飞书错误通知配置

当 Watchdog 检测到异常（Gateway 崩溃、RPC 故障等）时，会**即时**将详细错误信息发送到飞书。

### 1. OpenClaw 连接飞书

首先，在 OpenClaw 中配置飞书通道：

```bash
# 添加飞书通道
openclaw channels add feishu
```
按照交互提示完成认证。

验证通道是否正常工作：
```bash
openclaw message send --channel feishu --target "me" --message "来自 Watchdog 的测试消息"
```

### 2. 设置你的飞书 User ID

Watchdog 需要你的飞书 **open_id** 才能给你发私信。

**获取你的 open_id：**
```bash
openclaw message send --channel feishu --target "me" --message "test"
# 返回结果中包含你的 open_id（例如 "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"）
```

**通过环境变量配置：**

PowerShell（当前会话）：
```powershell
$env:WATCHDOG_FEISHU_USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
python scripts\watchdog_monitor.py
```

PowerShell（永久设置，配置文件）：
```powershell
[System.Environment]::SetEnvironmentVariable("WATCHDOG_FEISHU_USER_ID", "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "User")
```

命令提示符：
```cmd
set WATCHDOG_FEISHU_USER_ID=ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python scripts\watchdog_monitor.py
```

### 3. 通知流程

```
Gateway 崩溃 / 检测到错误
        │
        ├─► 飞书私信（即时，0 延迟）
        │    └─ 消息内容: "Watchdog: Gateway 已连续失败 3 次..."
        │       包括: 严重级别, 错误详情, 时间戳
        │
        ├─► WebChat 会话（异步，约 40 秒模型推理）
        │    └─ 后台线程发送，不阻塞监控主循环
        │
        └─► watchdog_state.json（本地日志）
             └─ 完整检查历史（最近 1440 条记录）
```

### 4. 你会收到什么

当出错时，飞书会收到类似这样的通知：

```
Watchdog

Gateway 不可达 (连续失败 3/5 次)
状态: cli_err

严重级别: 🟠 警告
错误详情: Gateway 无输出或返回异常

---
2026-01-15 14:30:00
```

v6.1 改进后，错误信息包含**完整的堆栈跟踪**和**详细诊断上下文**（不再是简单的 "Watchdog" 标题）。

---

## 📚 文档

| 文档 | 内容 |
|------|------|
| [`INSTALL.md`](./INSTALL.md) | 完整安装指南 |
| [`SKILL.md`](./SKILL.md) | 主文档（全部工作流） |
| [`docs/CHANGES_v6.1.md`](./docs/reports/CHANGES_v6.1.md) | v6.1 完整更新日志 |
| [`docs/MODULE_01_PreCheck.md`](./docs/MODULE_01_PreCheck.md) | 问题预检与上下文收集 |
| [`docs/MODULE_02_SearchChain.md`](./docs/MODULE_02_SearchChain.md) | 搜索策略：文档 → GitHub |
| [`docs/MODULE_03_ValidationAction.md`](./docs/MODULE_03_ValidationAction.md) | 决策与验证 |
| [`docs/MODULE_04_Finalization.md`](./docs/MODULE_04_Finalization.md) | 记忆更新与经验总结 |

---

## 🗺️ 诊断流水线

```
┌─ gateway status --json ────────┐
│  (约8秒)                       │
└────────┬───────────────────────┘
         ▼
┌─ runtime_health_check.py ──────┐
│  (25-30秒)                     │
│  gateway · 磁盘 · sessions     │
│  日志 · 模型(限3个)            │
└────────┬───────────────────────┘
         ▼
┌─ api_key_validator.py ─────────┐
│  (10-20秒)                     │
│  OpenAI · Tavily · GitHub 等   │
└────────┬───────────────────────┘
         ▼
┌─ diagnosis_formatter.py ───────┤
│  严重性排序报告                 │
│  --save-baseline / --compare   │
└────────────────────────────────┘
   总耗时: ~45-55秒（原为 ∞ 卡死）
```

---

## ⚙️ 环境要求

- **OpenClaw** 2025.x 或更高（v2026.5.20 完全支持）
- **Python 3.10+**（用于诊断脚本和 Watchdog）
- **pywin32**（Watchdog 单实例保护）
- **psutil**（可选，Watchdog 进程清理增强）

---

## 📄 开源协议

开源项目，欢迎 fork、修改和分享。
