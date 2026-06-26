# OpenClaw Gateway 看门狗

这是项目的中文快捷入口。完整中文文档见 [README.zh-CN.md](README.zh-CN.md)，英文文档见 [README.md](README.md)。

最简单安装：

```bash
bash install-watchdog.sh
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File .\install-watchdog.ps1
```

默认配置即可启动；需要指定自己的通道地址时：

```bash
bash install-watchdog.sh --channel-url "https://你的通道地址/health"
```

安装后还有一个独立图形化控制台：

```text
http://127.0.0.1:18790/
```

它由 watchdog 自己提供，不依赖 OpenClaw Gateway。Gateway 挂掉时，这个页面仍然可以看状态、图表、策略、日志和诊断导出。Dashboard 支持中英文切换、主题切换、事件趋势图、异常分类图和受保护操作解锁。

安装后它会默认采集 OpenClaw 诊断快照和日志信号，包括 gateway status、health、models status、status --deep 和 `openclaw logs --plain` 的 WARN/ERROR 摘要。关键证据在：

```text
~/.local/state/openclaw-gateway-watchdog/watchdog.log
~/.local/state/openclaw-gateway-watchdog/last-openclaw-diagnostics.jsonl
~/.local/state/openclaw-gateway-watchdog/last-openclaw-log-signals.txt
```

可选模型探针默认关闭。需要排查模型 API 是否在某个时段超时时，可以在配置里显式开启 `MODEL_PROBE_ENABLED="1"`；它会发送极小的 `openclaw agent --json` 请求，并把结果写入 watchdog 日志和 `model-probe-history.jsonl`。默认动作仍是只记录证据，不会擅自改 OpenClaw 配置。
