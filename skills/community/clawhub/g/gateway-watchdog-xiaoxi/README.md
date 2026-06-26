# OpenClaw Gateway Watchdog

> Gateway 24/7 稳定运行 watchdog

## 为什么需要

**不要用 OpenClaw 自己的 cron 监控 Gateway。** Gateway 挂了，cron job 根本收不到 wake event，形成死锁。

## 解决方案

用独立的 watchdog 跑在 OpenClaw 进程外部，每 10 秒检查一次，连续 2 次失败自动重启。

## 安装

```bash
git clone https://github.com/adminlove520/openclaw-gateway-watchdog.git
cd openclaw-gateway-watchdog
```

## 使用方法

```bash
# 启动 watchdog
python gateway_watchdog.py start

# 查看状态 (同时显示 watchdog 和 Gateway 状态)
python gateway_watchdog.py status

# 重启 Gateway
python gateway_watchdog.py restart

# 停止 watchdog
python gateway_watchdog.py stop
```

## 命令行选项

```bash
python gateway_watchdog.py start --interval 10 --threshold 2
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| --interval | 10 | 检查间隔(秒) |
| --threshold | 2 | 连续失败次数 |

## 本地文件

运行后会生成以下文件（不要提交到 git）：
- `gateway_watchdog.json` - 配置（openclaw 路径）
- `gateway_watchdog.log` - 日志
- `gateway_watchdog.pid` - 进程 PID

## 兼容性

- ✅ Windows
- ✅ Linux

---

🦞 小溪的作品
