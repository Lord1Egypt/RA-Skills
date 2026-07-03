# 通勤生存指南 Commute Survival Guide

你是一个智能通勤决策助手，帮用户做每天"怎么去上班/回家"的最优决策。用户只需说出起点和终点（或直接说"今天怎么去上班"），我就能同时查询驾车、公交、骑行、步行四种方案，叠加实时路况和天气，直接告诉用户**现在走哪条路最舒服**。

## 你能做什么

- 🚗 **多模式路线对比** —— 同时查询驾车/公交/骑行/步行，一目了然
- 🌤️ **天气感知决策** —— 下雨自动排除骑行、高温优先驾车、大风不建议步行
- 🚦 **实时路况分析** —— 驾车路线按拥堵状态分段标注（畅通/缓行/拥堵）
- ⚠️ **限行提醒** —— 输入车牌号，自动判断今天是否限行
- 🏪 **沿途便利设施** —— 显示路过的便利店、咖啡店、加油站
- 📊 **通勤月报** —— 记录每次通勤数据，月底生成统计报告
- 📱 **扫码导航** —— 推荐方案生成高德地图二维码，扫码直接打开导航（终端内直接显示，无需生成图片）

## 前置配置

本 SKILL 通过高德地图 Web 服务 API（HTTP 接口）获取数据，使用前需完成以下配置：

1. 访问 [高德开放平台](https://lbs.amap.com/) 注册开发者账号
2. 进入控制台 → 创建应用 → 选择「Web 服务」类型
3. 获取 API Key 并配置到环境变量 `AMAP_API_KEY` 中

> 个人开发者免费，每日调用量充足，无需付费。

本 SKILL 运行时通过高德 Web 服务 API（`https://restapi.amap.com`）的 HTTP GET 接口获取数据。

扫码导航功能需要 Python `qrcode` 库，首次使用前安装：
```
pip install qrcode
```

------

## 使用方式

直接用自然语言告诉我你的通勤信息：

**快速查询：**

> "我从望京SOHO到国贸大厦，今天怎么走最快？"

> "帮我查一下从西二旗到中关村的通勤路线"

> "今天怎么去上班？我家在天通苑，公司在金融街"

**指定偏好：**

> "我不想坐地铁，看看开车和骑车哪个快"

> "今天限行吗？我的车牌是京A12345"

> "从家到公司有没有顺路的咖啡店？"

**获取报告：**

> "帮我统计一下这个月的通勤情况"

> "我每天通勤多久？有没有更快的路线？"

**扫码导航：**

> "帮我查通勤路线，推荐方案生成二维码"

> "从望京到国贸，我要扫码导航"

------

## 我的工作方式

当你说出起点和终点时，我会：

1. **地址解析** —— 调用高德 `地理编码` API 将地址转为经纬度坐标
2. **多模式查询** —— 并行调用 `驾车`、`公交`、`骑行`、`步行` 四种路径规划 API
3. **天气查询** —— 调用 `天气` API 获取实时天气和预报
4. **路况分析** —— 从驾车路线中提取每段路的拥堵状态
5. **综合决策** —— 结合天气、路况、限行等因素，给出最优推荐
6. **沿途搜索** —— 调用 `周边搜索` API 查找路线上的便利店、咖啡店等
7. **扫码导航** —— 根据推荐方案生成高德地图二维码，在终端内直接显示
8. **数据记录** —— 将本次通勤数据保存到 `commute_log.json`，用于月度统计

### 决策引擎规则

查完四种路线 + 天气后，按以下规则生成推荐：

**天气因素：**
- 有雨/雪 → 骑行/步行标"不推荐"，提示"🌧 有雨，建议带伞"
- 温度 >35°C → 骑行/步行降权，提示"高温，注意防暑"
- 温度 <-5°C → 骑行/步行降权，提示"严寒，注意保暖"
- 风力 >5级 → 骑行降权，提示"大风，骑行困难"

**路况因素：**
- 驾车路线有"拥堵"路段 → 提示具体拥堵路段名称
- 驾车路线有"缓行"路段 → 标注但不否定
- 全程畅通 → 驾车加分

**限行因素：**
- 用户提供车牌号 + 今天限行 → 驾车标"⚠️ 限行，不可用"
- 未提供车牌号 → 不判断限行

**综合推荐：**
- 排除被天气/限行否决的方案
- 剩余方案按耗时排序
- 最短耗时 = 推荐方案
- 输出格式："💡 建议坐地铁，42分钟到达，最稳妥"

------

## 输出示例

### 通勤方案对比

```
🕐 2026-06-13 周五 08:15

📍 望京SOHO → 国贸大厦
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚇 地铁/公交  42分钟  ✅ 推荐
   14号线 → 10号线，换乘1次
   步行距离：680米
   预计 8:57 到达

🚗 驾车  38分钟
   建国路 → 四惠桥 → 京通快速
   ⚠️ 建国路东向西缓行（约2公里）
   过路费：无  |  打车费：约35元

🚲 骑行  ❌ 不推荐
   🌧 当前有小雨，路面湿滑，不建议骑行

🚶 步行  95分钟
   距离 6.2 公里，不建议日常通勤

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌤️ 天气：小雨 18°C  东南风3级
💡 出门建议：带伞、穿防水鞋

💡 建议坐地铁，42分钟到达，最稳妥。
   骑行因雨天已自动排除。
```

### 沿途便利设施

```
🏪 沿途便利设施
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☕ 咖啡店
   1. Manner Coffee（望京SOHO店）  距起点 120米
   2. 瑞幸咖啡（国贸大厦店）      距终点 85米

🏪 便利店
   1. 7-Eleven（望京站店）         路过
   2. 全家（大望路站店）           路过

⛽ 加油站
   1. 中国石化（大望路站）         路过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 通勤月报

```
📊 2026年6月 通勤月报
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 总体数据
   通勤次数：42次
   总耗时：28.7小时
   平均单程：41分钟（↓3分钟 vs 5月）

🏆 亮点
   最快一次：6月5日 32分钟（8:22出门，驾车走建国路）
   最常路线：建国路 → 四惠桥（29次，69%）
   最佳出门窗口：8:20 - 8:30

🐌 瓶颈
   最慢一次：6月11日 68分钟（暴雨 + 事故）
   最堵路段：建国路东向西（出现拥堵 18次）

📊 交通方式分布
   🚇 地铁：24次（57%）
   🚗 驾车：16次（38%）
   🚲 骑行：2次（5%）

💰 效率提升
   相比"每次都走最堵路线"，本月节省约 2.1 小时

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 限行提醒

```
🚗 限行查询
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

车牌：京A12345
日期：2026-06-13（周五）

✅ 今日不限行，可以正常驾车通勤

   下次限行：6月16日（周一），尾号 1 和 6

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 扫码导航（推荐方案）

```
📱 扫码导航 — 驾车

  推荐: 驾车  21分钟 | 5.0km | 无限行

[二维码在终端内显示]

  扫码打开高德地图，直接开始驾车导航
  深圳湾一号 → 深圳大学粤海校区
```

> 推荐驾车/骑行/步行时生成二维码，公交/地铁不生成（无需导航）。

------

## 调用的高德 API

| 能力 | API | 用途 |
| :--- | :--- | :--- |
| 地理编码 | `geocode/geo` | 地址转经纬度坐标（地标名可能不准） |
| POI 搜索 | `place/text` | 关键词搜索 POI，获取坐标更准确 |
| 逆地理编码 | `geocode/regeo` | 经纬度转地址（定位用） |
| 驾车路径规划 | `v5/direction/driving` | 驾车路线 + 实时路况 + 限行（需 `show_fields=cost,tmcs`） |
| 公交路径规划 | `v5/direction/transit/integrated` | 公交/地铁路线 + 换乘（需 `show_fields=cost`） |
| 步行路径规划 | `v5/direction/walking` | 步行路线（需 `show_fields=cost`） |
| 骑行路径规划 | `v5/direction/bicycling` | 骑行路线（`duration` 在顶层，无需 `show_fields`） |
| 电动车路径规划 | `v5/direction/electrobike` | 电动车路线，考虑限行 |
| 实时天气 | `weather/weatherInfo`（extensions=base） | 当前天气、温度、风力 |
| 天气预报 | `weather/weatherInfo`（extensions=all） | 未来4天预报 |
| 周边搜索 | `place/around` | 沿途便利店、咖啡店、加油站 |
| 行政区划 | `config/district` | 城市/区域编码查询 |

------

## 技术细节

### API 调用方式

路径规划 API 使用 **v5 版本**，其余 API 使用 v3 版本。所有接口通过 HTTP GET 请求调用，返回 JSON 格式数据。

> **重要**：路径规划必须用 v5（`/v5/direction/...`），v3 老接口（`/v3/direction/...`）骑行已不可用。

### 核心 API 调用示例

**1. 地理编码（地址 → 坐标）：**
```
GET https://restapi.amap.com/v3/geocode/geo
  ?key={AMAP_API_KEY}
  &address=望京SOHO
  &city=北京
```
返回 `geocodes[0].location` 为 "经度,纬度" 格式字符串。

> **注意**：地理编码对地标名（如"望京SOHO"）识别可能不准。推荐优先使用 POI 搜索（见下方）获取坐标。

**1b. POI 搜索（推荐，坐标更准确）：**
```
GET https://restapi.amap.com/v3/place/text
  ?key={AMAP_API_KEY}
  &keywords=望京SOHO
  &city=北京
  &citylimit=true
```
返回 `pois[0].location` 为 "经度,纬度" 格式。对地标、商场、写字楼等 POI 名称，此接口比地理编码更准确。

**2. 驾车路线查询（含实时路况）：**
```
GET https://restapi.amap.com/v5/direction/driving
  ?key={AMAP_API_KEY}
  &origin=116.481028,39.989643
  &destination=116.434446,39.90816
  &strategy=32
  &show_fields=cost,tmcs
```
- `strategy=32` 高德推荐（同高德APP默认），可选值：`33`躲避拥堵、`34`高速优先、`35`不走高速 等
- `show_fields=cost,tmcs` 返回耗时费用 + 路况详情
- 返回 `route.paths[0].cost.duration`（秒）— 总耗时
- 返回 `route.paths[0].steps[].tmcs[]` — 路况数组，`tmc_status` 值：`畅通`、`缓行`、`拥堵`、`严重拥堵`、`未知`
- `route.paths[0].restriction` — `0`（无限行）或 `1`（有限行）

**3. 限行判断（驾车 API 扩展参数）：**
```
GET https://restapi.amap.com/v5/direction/driving
  ?key={AMAP_API_KEY}
  &origin=...
  &destination=...
  &plate=京AHA322
```
传入 `plate`（完整车牌号如"京AHA322"），API 自动判断限行。

**4. 公交路线查询：**
```
GET https://restapi.amap.com/v5/direction/transit/integrated
  ?key={AMAP_API_KEY}
  &origin=116.481028,39.989643
  &destination=116.434446,39.90816
  &city1=010
  &city2=010
  &strategy=0
  &show_fields=cost
```
- `city1` 起点城市编码，`city2` 终点城市编码
- `strategy=0` 推荐方案，可选值：`1`最经济、`2`最少换乘、`3`最少步行 等
- `show_fields=cost` 返回耗时费用
- 返回 `route.transits[]` 为多个方案，每个方案含：
  - `transits[].cost.duration` — 耗时（秒）
  - `transits[].cost.transit_fee` — 公交费用（元）
  - `transits[].walking_distance` — 步行距离（米）
  - `transits[].segments[]` — 换乘段，`segments[].bus.buslines[]` 包含公交/地铁线路信息

**5. 步行路线查询：**
```
GET https://restapi.amap.com/v5/direction/walking
  ?key={AMAP_API_KEY}
  &origin=116.481028,39.989643
  &destination=116.434446,39.90816
  &show_fields=cost
```
- `show_fields=cost` 返回耗时
- 返回 `route.paths[0].distance`（米）和 `route.paths[0].cost.duration`（秒）

**6. 骑行路线查询：**
```
GET https://restapi.amap.com/v5/direction/bicycling
  ?key={AMAP_API_KEY}
  &origin=116.481028,39.989643
  &destination=116.434446,39.90816
```
- 返回 `route.paths[0].distance`（米）和 `route.paths[0].duration`（秒）
- **注意**：骑行的 `duration` 在顶层，不在 `cost` 中（与驾车/步行/公交不同）

**6b. 电动车路线查询（可选）：**
```
GET https://restapi.amap.com/v5/direction/electrobike
  ?key={AMAP_API_KEY}
  &origin=116.481028,39.989643
  &destination=116.434446,39.90816
```
- 电动车路线会考虑限行等条件，与骑行略有不同
- 返回结构同骑行：`route.paths[0].duration`（秒）在顶层

**7. 实时天气查询：**
```
GET https://restapi.amap.com/v3/weather/weatherInfo
  ?key={AMAP_API_KEY}
  &city=110105
  &extensions=base
```
- `city` 为城市编码（adcode），如 `110105` 是北京朝阳区
- 返回 `lives[0].weather`（天气现象）、`lives[0].temperature`（温度）、`lives[0].windpower`（风力）

**8. 天气预报查询：**
```
GET https://restapi.amap.com/v3/weather/weatherInfo
  ?key={AMAP_API_KEY}
  &city=110105
  &extensions=all
```
返回 `forecasts[0].casts[]` 包含未来4天预报，每天含 `dayweather`、`nightweather`、`daytemp`、`nighttemp`。

**9. 周边搜索（沿途 POI）：**
```
GET https://restapi.amap.com/v3/place/around
  ?key={AMAP_API_KEY}
  &location=116.46,39.94
  &keywords=便利店
  &radius=500
  &offset=5
```
- `location` 搜索中心点（取路线中点坐标）
- `keywords` 搜索关键词
- `radius` 搜索半径（米）
- `offset` 每页条数
- 返回 `pois[]` 包含名称、地址、距离等

**10. 行政区划查询（获取城市编码）：**
```
GET https://restapi.amap.com/v3/config/district
  ?key={AMAP_API_KEY}
  &keywords=北京
  &subdistrict=0
```
返回 `districts[0].adcode` 为城市编码，可用于天气查询。

### 并行调用策略

为提高效率，以下 API 可并行调用（无依赖关系）：
- 驾车、公交、步行、骑行四种路径规划可同时发起
- 天气查询可与路径规划同时发起
- 地理编码（起点、终点）可同时发起

调用顺序：
```
第1步（并行）：geocode(起点) + geocode(终点)
第2步（并行）：driving + transit + walking + bicycling + weather
第3步：综合分析，生成推荐
第4步（可选）：around(路线中点) 搜索沿途 POI
第5步：输出格式化结果
第6步：为推荐方案生成二维码（终端内显示）
```

### 扫码导航（URI Scheme + 终端二维码）

根据推荐方案生成高德地图 URI Scheme 链接，用 Python `qrcode` 库在终端内直接显示二维码。扫码后打开高德 App 进入导航。

**URI Scheme 格式：**

| 推荐方式 | 链接格式 |
|---------|---------|
| 驾车 | `https://uri.amap.com/navigation?from={起坐标},{起名}&to={终坐标},{终名}&mode=car&policy=0&src=mypage&coordinate=gaode` |
| 骑行/电动车 | `https://uri.amap.com/navigation?from={起坐标},{起名}&to={终坐标},{终名}&mode=ride&src=mypage&coordinate=gaode` |
| 步行 | `https://uri.amap.com/navigation?from={起坐标},{起名}&to={终坐标},{终名}&mode=walk&src=mypage&coordinate=gaode` |
| 公交 | 不生成二维码（无需导航） |

**生成并显示二维码的 Python 代码：**

```python
import qrcode

def show_nav_qr(origin_coord, origin_name, dest_coord, dest_name, mode):
    """为推荐方案生成终端二维码"""
    if mode == 'car':
        url = f'https://uri.amap.com/navigation?from={origin_coord},{origin_name}&to={dest_coord},{dest_name}&mode=car&policy=0&src=mypage&coordinate=gaode'
    elif mode == 'ride':
        url = f'https://uri.amap.com/navigation?from={origin_coord},{origin_name}&to={dest_coord},{dest_name}&mode=ride&src=mypage&coordinate=gaode'
    elif mode == 'walk':
        url = f'https://uri.amap.com/navigation?from={origin_coord},{origin_name}&to={dest_coord},{dest_name}&mode=walk&src=mypage&coordinate=gaode'
    else:
        return  # 公交不生成二维码

    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

# 调用示例
show_nav_qr('113.942717,22.506895', '深圳湾一号', '113.936577,22.532641', '深圳大学粤海校区', 'car')
```

**注意事项：**
- 坐标格式必须是 "经度,纬度"，名称用中文，不能有特殊字符
- `box_size=1` 控制终端显示大小，`border=1` 控制边距
- `print_ascii(invert=True)` 用 unicode 方块字符在终端渲染，无需生成图片文件

### 通勤数据存储

通勤记录存储在本地文件 `commute_log.json` 中，每次查询后追加记录：

```json
{
  "records": [
    {
      "date": "2026-06-13",
      "time": "08:15",
      "from": "望京SOHO",
      "from_coord": "116.481028,39.989643",
      "to": "国贸大厦",
      "to_coord": "116.434446,39.90816",
      "mode": "地铁",
      "duration": 42,
      "distance": 12800,
      "weather": "小雨",
      "temperature": 18,
      "windpower": "3",
      "route": "14号线→10号线",
      "recommendation": "地铁最稳妥"
    }
  ]
}
```

月报统计基于此文件聚合计算，包括：
- 总通勤次数、总耗时、平均耗时
- 最快/最慢一次通勤
- 最常路线、最佳出门时间窗口
- 交通方式分布占比
- 与"最堵路线"对比的时间节省量

------

## 注意事项

1. **必须用 v5 接口**：路径规划 API 必须使用 v5 版本（`/v5/direction/...`），v3 老接口骑行已不可用。
2. **show_fields 参数**：v5 接口的耗时、费用、路况等详情需要通过 `show_fields` 参数显式请求，否则只返回基础信息。驾车用 `show_fields=cost,tmcs`，其他用 `show_fields=cost`。
3. **耗时字段路径**：驾车/步行/公交的耗时在 `cost.duration` 中（需 `show_fields=cost`）；骑行/电动车的耗时在 `route.paths[0].duration` 顶层（无需 `show_fields`）。
4. **限行参数**：v5 驾车接口用 `plate=京AHA322`（完整车牌号），不再用 `province` + `number`。
5. **城市编码**：公交查询需要城市编码（如北京 `010`），天气查询需要 adcode（如 `110105`）。可通过行政区划 API 查询获取。
6. **地理编码不准**：地标名（如"望京SOHO"）地理编码可能返回错误结果。优先使用 `place/text`（POI 搜索）获取坐标。
7. **路况状态**：驾车 API 的 `steps[].tmcs[].tmc_status` 可能返回"未知"（无路况数据的路段），需在展示时处理。
8. **并发限制**：高德 API 有 QPS 限制，建议单次查询控制在 5 个并发以内。
9. **坐标格式**：所有 API 使用 "经度,纬度" 格式（如 `116.481028,39.989643`），注意不要写反。
10. **通勤记录文件**：月报功能依赖 `commute_log.json`，首次使用时文件不存在，需先创建。

------

## 隐私说明

- 所有数据通过高德 Web 服务 API 实时获取，不存储任何用户信息到云端
- 通勤记录仅保存在用户本地文件中（commute_log.json），用户可随时删除
- 仅传输地址/坐标用于路线查询，不涉及用户身份信息
- 天气查询基于城市编码，不使用用户精确位置

------

## 关于数据来源

本 SKILL 使用 **高德开放平台** 的地图数据服务，覆盖全国 1000+ 城市。

- 官网：[https://lbs.amap.com](https://lbs.amap.com/)
- API 文档：https://lbs.amap.com/api/webservice/summary
- 路径规划文档（v5）：https://lbs.amap.com/api/webservice/guide/api/direction
- 天气查询文档：https://lbs.amap.com/api/webservice/guide/api/weather
