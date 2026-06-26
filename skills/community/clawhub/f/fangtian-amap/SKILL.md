---
name: amap
description: '高德地图 API 调用工具，返回原始 JSON 数据。Use when users ask about 天气、地址、坐标、周边、路线、导航、打车、行程 in China. Commands: weather, geo, regeo, search, around, detail, route, distance, ip, navi, taxi, trip.'
compatibility: Requires curl (system built-in) and AMAP_API_KEY environment variable.
---

# 高德地图技能

直接调用高德 REST API，返回完整 JSON 响应。支持 15 个 API，共 12 个命令。

## 安装

```bash
cp amap ~/.local/bin/
chmod +x ~/.local/bin/amap
```

## 环境变量

```bash
export AMAP_API_KEY="your-api-key"
```

获取 API Key: https://console.amap.com/dev/key/app （选择 Web服务）

## 命令列表（12个）

### 位置服务

| 命令 | 说明 | 示例 |
|------|------|------|
| `weather` | 天气查询 | `amap weather 武汉` |
| `geo` | 地址转坐标 | `amap geo 黄鹤楼 武汉` |
| `regeo` | 坐标转地址 | `amap regeo 114.3,30.6` |
| `ip` | IP定位 | `amap ip 220.181.38.148` |

### 搜索服务
| 命令 | 说明 | 示例 |
|------|------|------|
| `search` | 搜索地点 | `amap search 黄鹤楼 武汉` |
| `around` | 周边搜索 | `amap around 学校 114.3,30.6 3000` |
| `detail` | POI详情 | `amap detail B001B0I4K0` |

### 天气服务
| 命令 | 说明 | 示例 |
|------|------|------|
| `weather` | 天气查询 | `amap weather 武汉` |

### 路线规划
| 命令 | 说明 | 示例 |
|------|------|------|
| `route` | 路线规划 | `amap route 114.3,30.6 114.4,30.7 driving` |
| `distance` | 距离测量 | `amap distance 114.3,30.6 114.4,30.7` |

### Schema 服务（生成 URI）
| 命令 | 说明 | 示例 |
|------|------|------|
| `navi` | 导航链接 | `amap navi 114.3,30.6 黄鹤楼` |
| `taxi` | 打车链接 | `amap taxi 114.3,30.6 黄鹤楼 114.4,30.7` |
| `trip` | 行程规划 | `amap trip "武汉游" '[{"title":"Day1","points":[...]}]'` |

## 输出格式

所有命令返回 JSON。

### REST API 命令

返回高德 API 原始 JSON，包含 status、info、核心数据。
```bash
amap weather 武汉
```
```json
{
  "status": "1",
  "forecasts": [{"city": "武汉市", ...}]
}
```
### Schema 命令
返回 URI 链接，点击可直接唤醒高德地图 APP。
```bash
amap navi 114.30234,30.54489 黄鹤楼
```
```json
{
  "status": "1",
  "uri": "https://uri.amap.com/marker?position=..."
}
```
## 调用示例
```bash
# 查天气
amap weather 武汉

# 地址转坐标
amap geo 黄鹤楼 武汉

# 搜索并获取详情
amap search 黄鹤楼 武汉
amap detail B001B0I4K0

# 周边搜索
amap around 学校 114.304569,30.593354 3000

# 路线规划
amap route 114.3,30.6 114.4,30.7 driving
amap route 114.3,30.6 114.4,30.7 walking

# 生成导航链接
amap navi 114.30234,30.54489 黄鹤楼

# 生成打车链接
amap taxi 114.30234,30.54489 黄鹤楼
```
## 解析示例
```bash
# 用 jq 解析
amap weather 武汉 | jq '.forecasts[0].casts'
amap geo 黄鹤楼 武汉 | jq '.geocodes[0].location'

# 用 Python 解析
amap search 黄鹤楼 | python3 -c "
import sys, json
data = json.load(sys.stdin)
for poi in data.get('pois', [])[:3]:
    print(poi['name'], poi['address'])
"
```
## 参数说明
- **坐标格式**：`经度,纬度`（经度在前）
- **半径单位**：米
- **路线方式**：driving（驾车）、walking（步行）、cycling（骑行）、transit（公交）
## 注意事项
- API Key 需要 Web服务 权限
- 每日调用有限制
- 仅支持中国境内
