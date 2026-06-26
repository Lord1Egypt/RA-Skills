---
name: etf-monitor
description: ETF 波动监控 - 实时跟踪 ETF 涨跌幅，超过阈值自动告警
homepage: https://github.com/openclaw/workspace
metadata: {
  "clawdbot": {
    "emoji": "📊",
    "requires": {
      "pip": ["requests"]
    },
    "bins": ["python3"]
  }
}
---

# ETF 波动监控技能

实时监控 ETF 价格波动，超过设定阈值时自动告警。

## 功能特点

- 📡 **实时行情**：使用腾讯财经 API，免费无需 Token
- 🎯 **多标的监控**：支持同时监控多只 ETF
- ⚠️ **智能告警**：波动超过阈值自动通知
- 🔇 **静默模式**：无告警时不打扰

## 快速使用

### 直接运行脚本

```bash
python3 /root/.openclaw/workspace/skills/etf-monitor.py
```

### 输出格式

**无告警时：**
```json
{"alerts": []}
```

**有告警时：**
```json
{
  "alerts": [
    {
      "code": "159985",
      "name": "豆粕 ETF",
      "current": 1.234,
      "percent": 1.5,
      "direction": "📈"
    }
  ]
}
```

## 配置说明

### 修改监控列表

编辑脚本中的 `ETF_LIST`：

```python
ETF_LIST = [
    ("sz159985", "159985", "豆粕 ETF"),
    ("sz159792", "159792", "港股通互联网 ETF"),
    ("sh515220", "515220", "煤炭 ETF"),
    # 添加更多 ETF...
]
```

### 调整波动阈值

```python
THRESHOLD = 1.0  # 波动阈值 1%
```

## 定时任务示例

每 5 分钟检查一次：

```bash
*/5 * * * * python3 /root/.openclaw/workspace/skills/etf-monitor.py
```

## 支持的 ETF 代码格式

- 深交所：`sz` + 6 位代码（如 `sz159985`）
- 上交所：`sh` + 6 位代码（如 `sh515220`）

## 注意事项

1. 需要网络连接访问腾讯财经 API
2. 行情数据可能有 1-2 分钟延迟
3. 建议阈值设置为 1%-3% 之间

---

**版本：** v5  
**最后更新：** 2026-03-18
