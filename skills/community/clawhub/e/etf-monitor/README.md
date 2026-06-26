# ETF 波动监控技能

📊 实时监控 ETF 价格波动，超过阈值自动告警

## 安装

本技能已内置，无需额外安装。

依赖：
```bash
pip install requests
```

## 使用方法

### 1. 直接运行

```bash
python3 etf-monitor.py
```

### 2. 查看当前监控的 ETF

编辑 `etf-monitor.py`，查看 `ETF_LIST` 数组：

```python
ETF_LIST = [
    ("sz159985", "159985", "豆粕 ETF"),
    ("sz159792", "159792", "港股通互联网 ETF"),
    ("sh515220", "515220", "煤炭 ETF"),
    ("sh513310", "513310", "中韩半导体 ETF"),
    ("sh510050", "510050", "上证 50ETF"),
    ("sz159922", "159922", "中证 500ETF"),
    ("sz159919", "159919", "沪深 300ETF"),
]
```

### 3. 添加新的 ETF

在 `ETF_LIST` 中添加新行：

```python
("sz159996", "159996", "智能家居 ETF"),  # 示例
```

格式：`("市场代码", "纯数字代码", "中文名称")`

- 深交所 ETF：`sz` + 6 位代码
- 上交所 ETF：`sh` + 6 位代码

### 4. 调整告警阈值

```python
THRESHOLD = 1.0  # 改为 2.0 表示 2% 波动才告警
```

## 输出示例

### 正常情况（无告警）
```json
{"alerts": []}
```

### 触发告警
```json
{
  "alerts": [
    {
      "code": "159985",
      "name": "豆粕 ETF",
      "current": 1.234,
      "percent": 1.5,
      "direction": "📈"
    },
    {
      "code": "515220",
      "name": "煤炭 ETF",
      "current": 0.987,
      "percent": -1.2,
      "direction": "📉"
    }
  ]
}
```

## 集成到定时任务

### Linux crontab 示例

每 5 分钟检查一次：
```bash
*/5 * * * * python3 /path/to/etf-monitor.py >> /var/log/etf-monitor.log 2>&1
```

### OpenClaw 定时任务

在 OpenClaw 中配置 cron 任务，结合 QQ 通知技能发送告警。

## 故障排查

### 无法获取行情
- 检查网络连接
- 确认腾讯财经 API 可访问：`http://qt.gtimg.cn/q=sz159985`

### 数据不准确
- 行情数据可能有 1-2 分钟延迟
- 非交易时段返回的是收盘价

## 技术细节

- **数据源**：腾讯财经 API (`qt.gtimg.cn`)
- **编码**：GBK
- **更新频率**：实时（建议 30 秒以上间隔）

## 许可证

MIT License

---

**作者：** OpenClaw Workspace  
**版本：** v5  
**更新日期：** 2026-03-18
