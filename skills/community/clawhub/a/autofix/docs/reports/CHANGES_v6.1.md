# CHANGES v6.1 — OpenClaw v2026.5.20 兼容性升级

**发布日期:** 2026-05-22

## 概述

v6.1 是一次兼容性小版本升级，主要解决 OpenClaw v2026.5.20 下 `openclaw doctor` 挂死导致的诊断流水线瘫痪问题，并从根本上防止 Windows 平台上的僵尸子进程。

## auto_repair v1.1 改进

| 变更 | 说明 |
|------|------|
| `gateway restart` 改用 `taskkill + start` | 避免 `openclaw gateway restart` 在 v2026.5.20 下挂死 |
| 新增 `verify_repair()` 函数 | 修复后轮询验证（30s, 每 5s）取代 `time.sleep(3)` |
| 新增 Session 归档修复 | 检测 >100 session 时自动归档 >7 天的旧文件到 `archive/` |
| 新增 Gateway 内存告警修复 | 检测 >800MB 时建议重启 |
| 所有命令超时从 30s → 60s | 给 Gateway 重启留足够时间 |

## 核心问题

| 问题 | 严重性 | 表现 |
|------|--------|------|
| `openclaw doctor` 挂死 | 🔴 阻断 | 超过 60 秒无返回，导致诊断流水线完全无法使用 |
| Windows 僵尸进程 | 🟠 高 | `subprocess.run(..., timeout=N)` 杀掉 Python 父进程后，`shell=True` 启动的 cmd.exe 子进程残留 |
| Model 端点检查慢 | 🟡 中 | `runtime_health_check` 遍历所有 provider 端点，每个等待 5s 超时，累计超 30s |
| Watchdog 进程残留 | 🟢 低 | `watchdog_monitor.py --status`（原为非法参数）误启动守护进程，或残留进程未清理 |

## 文件变更

### 🔧 `scripts/diagnosis_formatter.py`

| 变更 | 说明 |
|------|------|
| `parse_doctor_output()` 超时 120s → **12s** | 避免死等 `openclaw doctor` |
| 新增 `_fallback_doctor_output()` | 超时后自动降级到 `gateway status --json` |
| 新增 `_safe_run()` 函数 | 所有子进程调用改用 Popen + `CREATE_NEW_PROCESS_GROUP` + `taskkill /T /F` |
| 新增 `_safe_kill()` 函数 | 杀死整个进程树，防止僵尸 |
| `runtime_health_check` 超时 60s → 20s | 3 个数据源各自独立超时 |
| `api_key_validator` 超时 60s → 20s | 同上 |

### 🔧 `scripts/runtime_health_check.py`

| 变更 | 说明 |
|------|------|
| `run_cmd()` 改用 `Popen` + `taskkill` | 从 `subprocess.run(shell=True)` 迁移到安全的进程树终止模式 |
| `check_disk_usage()` 跳过 `archive/sessions/node_modules` | os.walk 加速，避免扫大目录 |
| `check_model_connectivity()` 限 3 个 provider + 4s 超时 | 避免遍历所有端点累积超时 |
| Provider 连接增加 `Connection: close` 头 | 防止 keep-alive 挂起 |

### 🔧 `scripts/api_key_validator.py`

| 变更 | 说明 |
|------|------|
| `REQUEST_TIMEOUT` 5s → 3s | 减少每个 Key 验证的等待时间 |

### 🔧 `scripts/watchdog_monitor.py`

| 变更 | 说明 |
|------|------|
| 新增 `--status` 命令 | 读取 state 文件显示实时状态后正常退出 |
| 新增 `_cleanup_stale_watchdog_processes()` | 启动时自动查杀残留的 `--status` 进程 |
| 更新 `--help` 输出 | 包含新的 `--status` 选项 |

### 📄 `SKILL.md`

| 变更 | 说明 |
|------|------|
| 版本号 v6.0-M4 → v6.1 | 全文档更新 |
| 黄金路径增加 v2026.5.20 说明 | doctor 超时 + fallback 机制 |
| 新增 v6.1 功能特性表 | 列出所有新功能 |
| Watchdog 新增 `--status` 和进程清理说明 | 更新部署命令 |

## 兼容性

- ✅ OpenClaw v2026.5.20 — 完整支持
- ✅ Windows 10/11 — 完整支持（含进程树清理）
- ✅ Python 3.10+ — 所有脚本已验证
- ⚠️ `openclaw doctor` — 仍会超时，但已通过 12s 兜底+自动降级处理
- ✅ `health_dashboard.py --canvas` — 已验证可生成 Canvas embed

## 诊断流水线性能

| 阶段 | 超时前 | 超时后 | 实际耗时 |
|------|--------|--------|---------|
| `parse_doctor_output` | 120s（卡死） | 12s（降级到 fallback） | ~12s |
| `runtime_health_check` | 60s（可能卡死） | 20s（独立超时） | ~25-30s |
| `api_key_validator` | 60s（可能卡死） | 20s（独立超时） | ~10-18s |
| **全流水线** | **∞（卡死）** | **~52s** | **45-55s** |

## 验证

```powershell
# 一键诊断
python scripts\diagnosis_formatter.py --json

# 交互式仪表盘
python scripts\health_dashboard.py --canvas

# 基线保存
python scripts\diagnosis_formatter.py --save-baseline

# 回归对比
python scripts\diagnosis_formatter.py --compare

# Watchdog 状态查询
python scripts\watchdog_monitor.py --status
```

## Watchdog v6.1-M4 补丁（2026-05-22）

针对 Watchdog 双通道通知机制的 Bug 修复和隐私增强：

### 🐛 Bug 修复

| 问题 | 严重性 | 修复 |
|------|--------|------|
| `load_gateway_config()` 缓存bug | 🔴 阻断 | 第二次调用时 `mtime` 没变，跳过外层的 `if` 块，返回了重新初始化的 `defaults`（`token=None`）。修复：缓存命中时直接返回 `_config_cache` |
| WebChat 5s 超时 | 🔴 阻断 | `/v1/chat/completions` 需要 ~40s 模型首次加载，5s 永远超时。修复：后台线程 + 60s 超时 |
| `send_feishu()` 不记录堆栈 | 🟡 高 | 异常只记录 `logger.warning` 级别，无堆栈跟踪。修复：改用 `logger.error` + `exc_info=True` |
| `send_alerts()` 通道顺序颠倒 | 🟡 高 | 先尝试 WebChat（慢）再飞书（快），导致飞书延迟。修复：飞书即时为主通道，WebChat 异步后台 |

### 🔒 隐私改进

| 变更 | 说明 |
|------|------|
| `FEISHU_USER_ID` 硬编码 → 环境变量 | 从 `"ou_..."` 改为 `os.environ.get("WATCHDOG_FEISHU_USER_ID", "ou_placeholder")` |
| 移除运行时文件 | `watchdog_state.json`, `gateway_watchdog.log`, `__pycache__` 不在源码中 |

### 📄 文件变更

- `scripts/watchdog_monitor.py` — 配置缓存修复、异步 WebChat、飞书堆栈、隐私清理
- `SKILL.md` — 更新通知架构、通道优先级、v6.1 特性表
- `README.md` / `README_CN.md` — 新增飞书配置章节
- `INSTALL.md` — 更新环境变量配置说明
