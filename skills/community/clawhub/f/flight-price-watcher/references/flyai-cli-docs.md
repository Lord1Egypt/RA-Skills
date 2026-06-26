# FlyAI CLI 使用文档

## 安装

```bash
npm i @fly-ai/flyai-cli
```

## 基础命令

### 查询机票价格

```bash
flyai flight search --from <出发地> --to <目的地> --date <日期> [选项]
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--from` | ✅ | 出发地（城市名或机场代码） | 北京/PEK |
| `--to` | ✅ | 目的地（城市名或机场代码） | 上海/SHA |
| `--date` | ✅ | 出行日期（YYYY-MM-DD） | 2026-04-15 |
| `--type` | ❌ | 航班类型 | direct/all |
| `--time` | ❌ | 时间段偏好 | morning/afternoon/evening |
| `--json` | ❌ | 输出 JSON 格式 | - |

### 输出示例

```json
{
  "flights": [
    {
      "flightNo": "CA1501",
      "airline": "中国国际航空",
      "departure": "08:00",
      "arrival": "10:30",
      "duration": "2h30m",
      "price": 850,
      "type": "direct",
      "available": true
    },
    {
      "flightNo": "MU5102",
      "airline": "中国东方航空",
      "departure": "09:15",
      "arrival": "11:50",
      "duration": "2h35m",
      "price": 780,
      "type": "direct",
      "available": true
    }
  ]
}
```

## 高级用法

### 筛选直飞航班

```bash
flyai flight search --from PEK --to SHA --date 2026-04-15 --type direct
```

### 指定时间段

```bash
# 早上航班（6:00-12:00）
flyai flight search --from PEK --to SHA --date 2026-04-15 --time morning

# 下午航班（12:00-18:00）
flyai flight search --from PEK --to SHA --date 2026-04-15 --time afternoon

# 晚上航班（18:00-24:00）
flyai flight search --from PEK --to SHA --date 2026-04-15 --time evening
```

### 输出 JSON 格式（便于程序处理）

```bash
flyai flight search --from PEK --to SHA --date 2026-04-15 --json
```

## 常见错误

### 1. 未安装 CLI

```
Error: flyai command not found
```

**解决**: `npm i @fly-ai/flyai-cli -g`

### 2. 参数缺失

```
Error: Missing required argument: --from
```

**解决**: 确保提供所有必填参数

### 3. 日期格式错误

```
Error: Invalid date format. Use YYYY-MM-DD
```

**解决**: 使用正确的日期格式，如 `2026-04-15`

### 4. 无航班数据

```
Warning: No flights found for the specified criteria
```

**解决**: 检查日期、航线是否正确，或尝试放宽筛选条件

## 最佳实践

1. **使用 JSON 输出** - 便于程序解析处理
2. **缓存结果** - 避免频繁调用 API
3. **错误处理** - 捕获 CLI 执行失败的情况
4. **限流** - 避免短时间内大量请求

## 相关资源

- [FlyAI 官方文档](https://flyai.alibaba.com/docs)
- [飞猪开放平台](https://open.fliggy.com/)
