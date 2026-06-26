# system-healthcheck

**OpenClaw 三级系统健康监控**

[English](SKILL.md) | 简体中文

---

## 功能特性

- **L1 快速检查** (<200ms): 定义文件存在性检查
- **L2 小时级检查** (<5s): 系统资源、服务状态、日志扫描
- **L3 日级审计** (<60s): 全面系统审计
- **心跳机制**: 正常时静默，异常时告警
- **国际化支持**: 自动检测语言（英文/中文）
- **零外部依赖**: 开箱即用

---

## 安装

```bash
clawhub install system-healthcheck
```

或手动安装：

```bash
git clone https://github.com/your-username/system-healthcheck.git ~/.openclaw/skills/system-healthcheck
```

---

## 快速开始

### 1. L1 快速检查（手动）

```bash
cd ~/.openclaw/skills/system-healthcheck
python scripts/l1_fast_check.py
```

### 2. L2 小时级检查（手动）

```bash
python scripts/l2_hourly_check.py
```

### 3. 配置 Crontab

```bash
cat templates/crontab_example.txt
# 复制并编辑 crontab
crontab -e
```

### 4. 心跳检查

```bash
python scripts/heartbeat.py
```

---

## 配置说明

编辑 `config/default_config.yaml`：

```yaml
# 国际化
i18n:
  auto_detect: true  # 自动检测系统语言
  # locale: zh-CN    # 或手动指定

# 检查阈值
thresholds:
  disk_warning: 80      # 磁盘警告 (%)
  disk_critical: 95     # 磁盘临界 (%)
  memory_warning_mb: 500  # 内存警告 (MB)
  log_size_mb: 100      # 日志大小警告 (MB)

# 心跳机制
heartbeat:
  enabled: true
  work_hours_start: 9    # 工作开始时间
  work_hours_end: 18     # 工作结束时间
  quiet_on_ok: true      # 全部正常时静默
```

---

## 输出示例

### L2 小时级检查

```
🦞 系统健康检查 · 2026-03-23 09:00:00

✅ 磁盘使用率：45% (阈值：80%)
✅ 内存使用：1.2GB / 8GB
✅ Cron 服务：运行中
✅ OpenClaw Gateway：正常
✅ 日志文件：12MB

━━━━━━━━━━━━━━━━━━━━━━━━
✅ 所有检查通过
耗时：1.2s
```

### 心跳检查（全部正常）

```
HEARTBEAT_OK
```

### 心跳检查（发现问题）

```
🦞 心跳检查 · 2026-03-23 14:30:00

⚠️ 磁盘使用率：85% (超过 80%)
✅ 内存使用：2.1GB / 8GB
...
```

---

## 脚本说明

| 脚本 | 功能 | 频率 |
|------|------|------|
| `l1_fast_check.py` | 定义文件检查 | 对话前自动 |
| `l2_hourly_check.py` | 系统健康检查 | 每小时 (cron) |
| `l3_daily_audit.py` | 全面审计 | 每日 08:00 (cron) |
| `heartbeat.py` | 工作心跳检查 | 每 30 分钟 (cron) |

---

## 命令行选项

```bash
# JSON 格式输出
python scripts/l2_hourly_check.py --json

# 静默模式（仅退出码）
python scripts/l2_hourly_check.py --quiet

# 强制输出（心跳）
python scripts/heartbeat.py --force
```

---

## 退出码

- `0`: 所有检查通过
- `1`: 一项或多项检查失败

---

## 国际化支持

支持的语言：
- `en` - English
- `zh-CN` - 简体中文

自动从系统 locale 检测。手动覆盖：

```bash
export OPENCLAW_LOCALE=zh-CN
python scripts/l2_hourly_check.py
```

---

## 系统要求

- Python 3.8+
- Linux 或 macOS
- 无外部依赖（可选：`rich` 彩色输出，`pyyaml` 配置解析）

---

## 文件结构

```
system-healthcheck/
├── SKILL.md                    # Skill 描述
├── README.md                   # 英文文档
├── README.zh-CN.md             # 中文文档
├── config/
│   └── default_config.yaml     # 默认配置
├── locales/
│   ├── en.yaml                 # 英文翻译
│   └── zh-CN.yaml              # 中文翻译
├── scripts/
│   ├── i18n.py                 # 国际化模块
│   ├── l1_fast_check.py        # L1 检查
│   ├── l2_hourly_check.py      # L2 检查
│   ├── l3_daily_audit.py       # L3 审计
│   └── heartbeat.py            # 心跳检查
└── templates/
    └── crontab_example.txt     # Crontab 示例
```

---

## 常见问题

### Q: 如何禁用某项检查？
A: 编辑 `config/default_config.yaml`，设置对应检查的 `enabled: false`

### Q: 如何修改检查阈值？
A: 编辑 `config/default_config.yaml` 中的 `thresholds` 部分

### Q: 心跳检查为什么没有输出？
A: 工作时间内全部正常时会输出 `HEARTBEAT_OK`（静默模式），非工作时间不输出

### Q: 如何添加新的检查项？
A: 在 `scripts/l2_hourly_check.py` 中添加检查函数，并在 `run_l2_check()` 中调用

---

## 许可证

MIT

---

## 贡献

欢迎贡献！请先阅读 CONTRIBUTING.md

---

## 更新日志

### v1.0.0 (2026-03-23)
- 初始版本
- L1/L2/L3 检查
- 心跳机制
- 国际化支持（英文/中文）
