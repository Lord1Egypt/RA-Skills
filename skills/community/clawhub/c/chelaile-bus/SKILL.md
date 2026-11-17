---
name: chelaile-bus
description: 北京/全国 480 城市公交实时到站查询。基于 chelaile MCP 服务（mcporter chelaile），免 API Key。典型场景："311 路还有几分钟到展春园"、"查 86 路现在到哪了"。
---

# chelaile-bus · 公交实时到站

## 是什么

车来了（chelaile）数据的 MCP 封装，**480 个城市**实时公交数据。maxclaw 上由 `mcporter chelaile` 提供；kimiclaw 上由 openclaw.json mcp.servers 原生注册（工具名 `chelaile__bus_*`）。npx 首次拉包约 23 秒。

## 工具

- `bus_list_cities` — 城市列表（北京=027）
- `bus_search` — 关键词搜线路/站点/POI（拿 lineId）
- `bus_get_line_detail` — 全站点 + 首末班 + **线上所有车辆实时位置**
- `bus_get_line_realtime` — 指定站点的实时车辆 + ETA
- `bus_get_nearby_stops` — 附近站点（WGS-84 + city_id）
- `bus_plan_transit` — A→B 公交换乘（吃 GCJ-02）

注：maxclaw 侧工具名前加 `chelaile.`（mcporter），kimiclaw 侧加 `chelaile__`（openclaw 原生），同一批函数。

## 标准流程

```
1. bus_list_cities → 拿 city_id（北京=027）
2. bus_search "311路" → 拿 line_id（如 010-311-0）
3. bus_get_line_detail → 看站点表、找目标站 order
4. bus_get_line_realtime(target_order, station_id, lat, lng) → 实时到站
```

## 常用线路速查（已实测）

- **311**：dir0=`010-311-0`，dir1=`010-311-1`，北科大北门 → 展春园西路北口 → 大屯路东
- **86**：待补
- **603**：待补（成府路口南 → 北下关，妈妈家→钻河公馆通勤线）

> 实际使用先跑 `bus_search` 拿最新 line_id，不要硬编码（线路 ID 可能调整）。

## 坐标系统（铁律）

- **stations / realtime 是 WGS-84**（GPS 直读）
- **pois / plan_transit 是 GCJ-02**（高德系）
- maxclaw 自己保存的常用坐标（钻河/北科大等）**默认 GCJ-02**（高德查询得来），喂给 realtime 时要转 WGS-84 或用 station 自己的 wgsLat/wgsLng 作 fallback

## 已知坑

1. **地铁不支持**：isSubway=true 返回空，换 `bus_plan_transit`
2. **首末班别用 `bus_get_timetable`**：interval 模式无逐趟数据，用 `bus_get_line_detail` 的 firstTime/lastTime
3. **target_order 全链关键**：从 search/detail 取，别自己编
4. **ETA 只有最近一辆有**：上游只预测即将进站的 1 辆，其他车列出位置但 ETA=null（不是 bug，是设计）
5. **车辆数据可能 1-2 分钟延迟**：上游数据源特性

## 实战示例

```bash
# 1. 找线路
mcporter call chelaile.bus_search city_id="027" keyword="311路"

# 2. 看完整数据
mcporter call chelaile.bus_get_line_detail city_id="027" line_id="010-311-0"

# 3. 查具体站实时
mcporter call chelaile.bus_get_line_realtime \
  city_id="027" line_id="010-311-0" \
  target_order="4" station_id="010-19233" \
  lat="39.9932" lng="116.3543"
```

## 配置文件位置

`/workspace/config/mcporter.json` → `chelaile` server

## kimiclaw 适配（v1.1.0，2026-09-22）

- `scripts/query-bus.py`：**MCP stdio 直连版**，spawn `npx chelaile-mcp-server` 走 JSON-RPC，不依赖 mcporter，也不依赖 openclaw 原生工具，任何有 node 的环境可跑
- `scripts/query-bus.sh`：兼容包装，内部调 query-bus.py
- kimiclaw 上优先用原生工具 `chelaile__bus_*`（openclaw.json mcp.servers 注册）；脚本用于 cron/独立 shell 场景
- 已实测：311 路展春园西路北口全链路通过（2026-09-22 23:39）

## kimiclaw 适配（v1.1.0，2026-09-22）

- `scripts/query-bus.py`：**MCP stdio 直连版**，spawn `npx chelaile-mcp-server` 走 JSON-RPC，不依赖 mcporter，也不依赖 openclaw 原生工具，任何有 node 的环境可跑
- `scripts/query-bus.sh`：兼容包装，内部调 query-bus.py
- kimiclaw 上优先用原生工具 `chelaile__bus_*`（openclaw.json mcp.servers 注册）；脚本用于 cron/独立 shell 场景
- 已实测：311 路展春园西路北口全链路通过（2026-09-22 23:39）

## 安装时间
2026-09-22 安装（kimiclaw 收编 + 修复 23:39）（kimiclaw 收编 + 修复 23:39）

## 参考

- 上游 MCP 包：`chelaile-mcp-server`（npm）
- 安装命令：`mcporter config add chelaile --command "npx" --arg "-y" --arg "chelaile-mcp-server" --transport stdio`
- kimiclaw 教学邮件：2026-09-22 14:36 UTC（`houxingze3897@agent.qq.com` 收件箱）