# SKILL.md - OpenClaw Gateway Watchdog

> 让你的 OpenClaw Gateway 7/24 稳定运行

## 触发语

- "帮我 7/24 运行"
- "让 Gateway 持续运行"
- "设置 watchdog"
- "保持 Gateway 运行"

## 做什么

1. 检查是否有 `gateway_watchdog.py`，如果没有则从 GitHub 下载
2. 执行 `python gateway_watchdog.py start`
3. 反馈结果

## 快速开始

```bash
# 一键安装+启动
python install.py

# 或手动
python gateway_watchdog.py start
python gateway_watchdog.py status
python gateway_watchdog.py restart
python gateway_watchdog.py stop
```

## 输出示例

```
用户: 帮我7/24运行
-> 📥 正在下载 gateway_watchdog.py...
-> ✅ 下载完成
-> 🚀 启动 Gateway Watchdog...
-> ✅ Gateway Watchdog 已启动 (PID: 12345)
-> ✅ 完成！Gateway 将 7/24 运行
```

## 命令

| 命令 | 说明 |
|------|------|
| `python install.py` | 一键安装并启动 |
| `python gateway_watchdog.py start` | 启动 watchdog |
| `python gateway_watchdog.py status` | 查看状态 |
| `python gateway_watchdog.py restart` | 重启 Gateway |
| `python gateway_watchdog.py stop` | 停止 watchdog |

## 依赖

- Python 3.7+
- openclaw CLI

## 原理

**不要用 OpenClaw 自己的 cron 监控 Gateway。** Gateway 挂了，cron job 根本收不到 wake event，形成死锁。

外部 watchdog:
- Gateway 挂了 → 外部进程检测到 → 触发重启 → 恢复运行

---

🦞 小溪的作品
