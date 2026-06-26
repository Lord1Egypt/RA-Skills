---
name: domestic-flight
description: 零配置即装即用，支持国内航班实时查询，可筛选直飞和中转航班，价格、时刻、航司信息一查即得，基于飞猪数据直连。
tags: [航班查询, 机票, 国内航班, 飞猪旅行, 飞猪机票, flight, domestic]
tools:
  - name: search_flight
    description: 查询国内航班实时价格与时刻表
    primaryEnv: FLIGGY_PROXY_URL
    env:
      - name: FLIGGY_PROXY_URL
        description: 飞猪代理URL（自动配置）
        required: false
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置）
        required: false
    parameters:
      - name: params
        type: string
        description: 结构化参数(origin/destination/dep_date)或自然语言查询
        required: true
---

# 国内航班查询

零配置即装即用的国内航班查询技能，查询实时票价、航班号、起降时间、直飞/中转筛选，飞猪数据直连。

## 能做什么

- **航班查询**：支持结构化参数（出发地/目的地/日期）和自然语言两种输入
- **直飞/中转筛选**：按航班类型筛选
- **价格排序**：支持按价格、时长、出发时间排序
- **舱位选择**：经济舱/商务舱/头等舱

## 使用示例

1. "上海到北京7月1号机票"
2. {"origin": "上海", "destination": "三亚", "dep_date": "2026-07-15"}
3. "成都到广州明天最便宜的航班"

## 注意事项

- 仅支持国内航班查询
- 价格实时变动，以实际预订页面为准
- 查询通过云端代理转发到飞猪旅行API，代理不存储用户数据
