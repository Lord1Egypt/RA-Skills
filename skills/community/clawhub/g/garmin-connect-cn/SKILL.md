---
name: garmin-connect
description: |
  读取 Garmin Connect 手表/设备数据。
  触发场景：
  - "今天走了多少步"
  - "昨晚睡眠怎么样"
  - "最近有什么运动"
  - "心率怎么样"
  - "这周跑了多少次"
  - 查询任意日期的运动、睡眠、心率等健康数据
---

# Garmin Connect 数据查询

## 前置要求

- JWT Token（从浏览器获取，有效期约1个月）
- Python 3.8+

## 快速查询

```bash
python3 scripts/query.py <jwt_token> [日期 YYYY-MM-DD]
```

不传日期默认查今天。

## 数据类型

| 查询 | 字段 |
|------|------|
| 步数 | `totalSteps` |
| 距离(km) | `totalDistance / 1000` |
| 卡路里 | `activeKilocalories` |
| 爬楼层数 | `totalFloorsAscending` |
| 睡眠时长 | `sleepingDuration` |

## API 端点

详见 `references/api.md`

## Token 获取

1. 浏览器打开 https://connect.garmin.cn 并登录
2. F12 → Application → Cookies → `connect.garmin.cn`
3. 找到 `JWT_WEB`，复制 Value（`eyJ...` 开头）

## 注意

JWT 过期后需重新获取。每次查询前检查 Token 有效性。
