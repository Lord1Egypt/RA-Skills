# API 配置指南

## 一、高德地图 API (Amap)

### 1. 申请 API Key

1. 访问 https://lbs.amap.com/ 注册/登录
2. 进入「应用管理 → 我的应用」创建应用
3. 添加 Key，选择「Web服务」类型
4. 复制生成的 Key

### 2. 接口说明

#### 地理编码 (地名→坐标)

```
GET https://restapi.amap.com/v3/geocode/geo
  ?key={AMAP_KEY}
  &address={地址}
  &city={城市}
```

返回: `{ geocodes: [{ location: "116.397428,39.90923" }] }`

#### 驾车路径规划

```
GET https://restapi.amap.com/v3/direction/driving
  ?key={AMAP_KEY}
  &origin={lon,lat}
  &destination={lon,lat}
  &extensions=all
  &strategy=10
```

strategy=10: 躲避拥堵 + 路程较短

#### 步行路径规划

```
GET https://restapi.amap.com/v3/direction/walking
  ?key={AMAP_KEY}
  &origin={lon,lat}
  &destination={lon,lat}
```

#### 公交路径规划

```
GET https://restapi.amap.com/v3/direction/transit/integrated
  ?key={AMAP_KEY}
  &origin={lon,lat}
  &destination={lon,lat}
  &city={城市编码}
```

## 二、和风天气 API (QWeather)

### 1. 申请 API Key

1. 访问 https://dev.qweather.com/ 注册
2. 进入控制台创建项目
3. 选择「免费订阅」(免费版: 每天1000次调用)
4. 复制 API Key (JWT Token)

### 2. 接口说明

**认证方式**: Header `Authorization: Bearer {QWEATHER_KEY}`

#### 城市搜索 (获取 LocationID)

```
GET https://geoapi.qweather.com/v2/city/lookup
  ?location={城市名}
  &key={QWEATHER_KEY}
```

**注意**: 城市搜索使用 `key` 参数，海洋API使用 JWT Bearer Token。

#### 7天天气预报

```
GET https://api.qweather.com/v7/weather/7d
  ?location={LocationID}
```

返回字段: `fxDate, tempMax, tempMin, textDay, windDirDay, windScaleDay, humidity, precip, pressure, vis, cloud`

#### 24小时逐小时预报

```
GET https://api.qweather.com/v7/weather/24h
  ?location={LocationID}
```

返回字段: `fxTime, temp, text, windDir, windScale, humidity, precip, pop(降水概率), pressure, cloud`

#### 潮汐数据

```
GET https://api.qweather.com/v7/ocean/tide
  ?location={潮汐站点ID}
  &date={yyyyMMdd}
```

Header: `Authorization: Bearer {QWEATHER_KEY}`

返回:
- `tideTable[]`: `fxTime, height(米), type(H=满潮/L=干潮)`
- `tideHourly[]`: `fxTime, height(米)`

#### 钓鱼指数

```
GET https://api.qweather.com/v7/indices/1d
  ?type=1   (1=钓鱼指数)
  &location={LocationID}
```

## 三、配置方式

### 方式一 (推荐): 交互式配置向导

```bash
python fishing_planner.py --setup
```

向导会引导你依次输入 API Key，自动验证并保存到 `~/.fishing-planner/config.json`。

### 方式二: 环境变量

在终端设置或写入 `~/.bashrc`:

```bash
export AMAP_KEY="your_amap_key_here"
export QWEATHER_KEY="your_qweather_key_here"
```

Windows PowerShell:

```powershell
$env:AMAP_KEY="your_amap_key_here"
$env:QWEATHER_KEY="your_qweather_key_here"
```

## 四、配置文件说明

配置文件位于 `~/.fishing-planner/config.json` (权限 600，仅所有者可读写):

```json
{
  "amap_key": "your_amap_key",
  "qweather_key": "your_qweather_key",
  "default_tide_station": "P2951",
  "user_name": "钓鱼人",
  "setup_at": "2026-06-10 12:00"
}
```

优先级: config.json > 环境变量 > 默认值

## 五、历史记录

每次规划自动保存到 `~/.fishing-planner/trips/` 目录：

```bash
# 查看历史
python fishing_planner.py --history

# 打开第N条记录
python fishing_planner.py --view 1

# 按ID打开
python fishing_planner.py --view 20260615
```

记录包含完整的 HTML 报告和行程元数据 (时间/路线/评分等)。

## 六、注意事项

1. **高德地图 Key** 需开通「Web服务」类型
2. **和风天气** 免费版每天1000次调用，请求需带 Gzip 压缩头
3. **潮汐数据** 仅覆盖沿海潮汐站点，内陆钓点不返回潮汐
4. 和风天气城市搜索用 `key` 参数，海洋API用 `Authorization: Bearer`，两者不同
5. **LocationID**: 潮汐站点ID需通过和风天气POI搜索获取，格式如 `P2951`
