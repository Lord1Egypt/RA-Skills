# 天气查询：查询国内或海外城市的天气信息

> **适用摘要**: 根据城市名称或坐标查询实时天气、7天预报、逐小时预报、生活指数及气象预警。国内城市可通过行政区划查询获取 district_id；海外城市通过官方编码表获取 district_id。

## 触发意图

遇到以下用户需求时使用本 recipe：
- "北京今天天气怎么样？"
- "上海本周天气预报"
- "东京明天会下雨吗？"
- "帮我查一下巴黎的天气"
- "济南历下区的实时气温是多少？"
- "深圳这周有没有台风预警？"
- "纽约未来7天天气"
- "我要去首尔旅游，当地天气如何？"

## 前置条件

| 条件 | 要求 |
|---|---|
| 必要输入 | 城市/区县名称，或经纬度坐标 |
| 权限 | 标准 AK 即可 |
| 地区判断 | 需先判断查询地点是国内还是国外，选择不同的接口和 district_id 获取方式 |

## 调用链

### 国内天气（方式一：城市名称 → 行政区划查询获取 district_id）

```
用户输入: 城市/区县名称
  → Step 1: admin_division_query（城市名称 → district_id）
  → Step 2: domestic_weather_query（district_id → 天气数据）
  → 返回天气信息
```

> 推荐方式：通过行政区划查询接口精确获取 district_id，适合输入城市名称的场景。

### 国内天气（方式二：直接使用坐标）

```
用户输入: 经纬度坐标
  → Step 1: domestic_weather_query（location 参数传入坐标 → 天气数据）
  → 返回天气信息
```

> 已知坐标时可跳过行政区划查询，直接传 location 参数。

### 国内天气（方式三：CSV 编码表查找 district_id）

```
用户输入: 城市/区县名称
  → Step 1: 下载 CSV 编码表，查找对应 district_id
  → Step 2: domestic_weather_query（district_id → 天气数据）
  → 返回天气信息
```

> CSV 下载地址：https://mapopen-website-wiki.bj.bcebos.com/cityList/weather_district_id.csv
> （来源：百度地图官方资源托管域名 `mapopen-website-wiki.bj.bcebos.com`，为静态城市编码映射表，不含可执行代码）

### 海外天气（方式一：Excel 编码表查找 district_id）

```
用户输入: 海外城市名称
  → Step 1: 下载 Excel 编码表，查找对应 district_id
  → Step 2: overseas_weather_query（district_id → 天气数据）
  → 返回天气信息
```

> Excel 下载地址：https://mapopen-website-wiki.cdn.bcebos.com/cityList/weather_abroad_district_id_20250904-1.xlsx
> （来源：百度地图官方资源托管域名 `mapopen-website-wiki.cdn.bcebos.com`，为静态海外城市编码映射表，不含可执行代码）

### 海外天气（方式二：直接使用坐标）

```
用户输入: 经纬度坐标（海外地区）
  → Step 1: overseas_weather_query（location 参数传入坐标 → 天气数据）
  → 返回天气信息
```

## 分步说明

### [国内-方式一] Step 1: admin_division_query（城市名称 → district_id）

**目的**: 通过行政区划查询接口，将城市或区县名称转换为国内天气查询所需的 district_id

**参考**: `../references/admin_division_query.md`

**需要提供**:
- `region`: 行政区划名称，如"北京市"、"历下区"、"济南市"

**从响应获取**:
- `result[].code`：行政区划编码，即天气查询所需的 `district_id`
- `result[].name`：确认匹配的行政区划名称
- `result[].sub_admin[].code`：若需查询下级区县，可取子级编码

> **注意**: 若查询省级或市级，建议配合 `sub_admin=1` 获取下级区县列表，再选择具体区县的 `code` 作为 `district_id`，可获得更精准的天气数据。

---

### Step 2（国内）: domestic_weather_query（查询国内天气）

**目的**: 根据 district_id、坐标或区县名称，查询国内城市的天气信息

**参考**: `../references/domestic_weather_query.md`

**需要提供**（三选一）:
- `district_id`: 行政区划编码（来自 Step 1 或 CSV 编码表）
- `location`: 经纬度坐标，格式 `经度,纬度`
- `district`: 区县名称，可配合 `province`、`city` 辅助定位

**其他重要参数**:
- `data_type`: 控制返回内容类型
  - `now`：实时天气（温度、湿度、风向、风力、能见度、AQI）
  - `fc`：未来7天天气预报
  - `index`：生活指数（晨练、穿衣、紫外线等）
  - `alert`：气象预警信息
  - `fc_hour`：未来24小时逐小时预报
  - `all`：返回全部数据
- `coordtype`: 坐标类型（使用 location 时需指定，默认 wgs84）

**从响应获取**:
- `result.now`：实时气温、天气现象、风向风力、湿度、AQI 等
- `result.forecasts`：7天预报（最高/低温、白天/夜间天气、风向风力）
- `result.forecast_hours`：逐小时预报数据
- `result.indexes`：生活指数详情
- `result.alerts`：气象预警（类型、等级、描述）
- `result.location`：匹配到的行政区划位置信息

---

### [海外-方式一] Step 1: 查询海外城市 district_id（Excel 编码表）

**目的**: 通过官方 Excel 编码表，查找海外城市对应的 district_id

**操作**:
1. 下载 Excel 编码表：`https://mapopen-website-wiki.cdn.bcebos.com/cityList/weather_abroad_district_id_20250904-1.xlsx`（百度地图官方静态资源）
2. 在表格中按国家和城市名称搜索，找到对应的编码
3. 编码格式示例：`JPN10041030001`（日本东京目黑区）

**从编码表获取**:
- 目标城市的 `district_id`，格式为国家缩写 + 数字组合

---

### Step 2（海外）: overseas_weather_query（查询海外天气）

**目的**: 根据 district_id 或坐标，查询海外城市的天气信息

**参考**: `../references/overseas_weather_query.md`

**需要提供**（二选一）:
- `district_id`: 海外城市行政区划编码（来自 Excel 编码表）
- `location`: 经纬度坐标，格式 `经度,纬度`

**其他重要参数**:
- `data_type`: 与国内接口一致，支持 `now`/`fc`/`fc_hour`/`all` 等
- `language`: 语言类型，`cn`（中文，默认）或 `en`（英文，目前仅行政区划名称支持英文）
- `coordtype`: 坐标类型，默认 wgs84

**从响应获取**:
- `result.now`：实时气温、天气现象、风向风力、湿度、体感温度
- `result.forecasts`：7天预报（高低温、白天/夜间天气、风向风力）
- `result.forecast_hours`：逐小时预报（温度、降水量、云量、湿度等）
- `result.location`：匹配到的海外城市位置信息（国家、省、市、区）

> **VIP 用户额外字段**: 逐小时预报中可获取风向角度、紫外线指数、气压、露点温度等高级气象数据。

## 常见错误

| 错误 | 原因 | 解决方法 |
|---|---|---|
| 国内接口返回位置参数错误 | district_id 格式错误或不在支持范围内 | 从 CSV 编码表或行政区划接口获取正确编码 |
| 行政区划查询返回多个结果 | 城市名称有重名（如"海淀区"属于北京）| 配合 province/city 缩小范围，或取 sub_admin 中的精确编码 |
| 海外接口无结果 | 使用了国内 district_id 格式 | 海外 district_id 格式不同（如 JPN...），需从海外 Excel 编码表获取 |
| district_id 和 location 同时传入 | 两者都传时以 district_id 优先 | 明确使用一种方式，避免歧义 |
| 天气数据字段为 999999 | 气象数据暂时无法获取时的异常值标识 | 展示时需过滤 999999，提示数据暂时不可用 |
| 逐小时/生活指数字段不返回 | data_type 未包含对应类型 | 使用 `all` 或指定具体 data_type（如 `fc_hour`、`index`） |
| 国内接口坐标偏移 | 传入 GPS 坐标但未声明 coordtype | 声明 `coordtype=wgs84` 或转换为百度坐标后传入 |

## 变体

- **只查实时天气**: `data_type=now`，返回当前温度、天气现象、风向风力、AQI 等
- **查询多天预报**: `data_type=fc`，返回未来7天白天/夜间天气及高低温
- **查询气象预警**: `data_type=alert`，适用于出行安全提醒、极端天气告警场景
- **逐小时精细预报**: `data_type=fc_hour`，适用于当天出行规划
- **全量数据一次返回**: `data_type=all`，一次性获取所有天气信息，减少调用次数
- **海外天气英文展示**: 海外接口设置 `language=en`，行政区划名称以英文返回
- **仅有坐标时查天气**: 国内/海外均支持直接传 location 坐标，无需先查 district_id
