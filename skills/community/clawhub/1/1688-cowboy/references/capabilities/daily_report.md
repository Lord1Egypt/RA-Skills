# daily_report（工作日报）

## 功能说明

查询接待助手的工作日报数据。当前为统一模式：按日期查询各项接待指标。

## CLI 调用

```bash
python3 cli.py daily_report --date today
python3 cli.py daily_report --date 2026-05-14
```

### TPP 接口

`POST /api/cowboy_daily_report/1.0.0`

请求体：
```json
{"date": "2026-05-14"}
```

### 完整参数表

| 参数     | 简写 | 说明                          | 默认值 |
| -------- | ---- | ----------------------------- | ------ |
| `--date` | `-d` | 查询日期：'today' 或 YYYY-MM-DD | today  |

## 输出格式

```json
{
  "success": true,
  "markdown": "## 接待助手工作日报（2026-05-14）\n\n| 指标 | 数值 | 较昨日 |\n...",
  "data": {
    "date": "2026-05-14",
    "elapsed_seconds": 0.3,
    "metrics": [
      {"name": "接待人数", "value": "15", "unit": "人", "yoy": "+12.5%"},
      {"name": "成交订单", "value": "3", "unit": "笔", "yoy": "-25.0%"},
      {"name": "成交客户", "value": "3", "unit": "人", "yoy": "-25.0%"},
      {"name": "询盘数量", "value": "28", "unit": "个", "yoy": "+8.3%"},
      {"name": "平均响应时间", "value": "45", "unit": "秒", "yoy": "-10.0%"},
      {"name": "转人工次数", "value": "5", "unit": "次", "yoy": "+25.0%"}
    ]
  }
}
```

### 字段映射（网关 → 项目内部）

| 网关字段 | 项目内部字段 | 说明 |
|----------|-------------|------|
| `metricName` | `name` | 指标名称 |
| `metricValue` | `value` | 指标数值 |
| `unit` | `unit` | 单位 |
| `yesterdayPercentage` | `yoy` | 同比变化（较昨日） |

## 注意事项

1. **双层 Result 包装**：网关返回的 `data` 字段是内层 `{"data": [...DTO...]}`，需剥两层才能拿到真正的 metrics 列表
2. **日期格式**：仅接受 ISO 格式 `YYYY-MM-DD`，斜杠格式 `YYYY/MM/DD` 不合法
3. **sellerUserId 不需传递**：网关会根据 AK 自动注入实际调用方 userId
4. metrics 列表为空时展示"今天没数据，可能日报还在统计中"

## 关联页面

执行 `daily_report` 后，Agent 可同时引导商家打开日报详情页查看。
