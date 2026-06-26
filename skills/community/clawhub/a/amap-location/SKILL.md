---
name: amap-location
description: 高德地图服务（路径规划、POI 搜索）
metadata: {"clawdbot":{"emoji":"🗺️"}}
---

# AMap Location - 高德地图服务

提供路径规划、POI 搜索、地理编码等高德地图服务。

## 配置

### API Key

已存储在 `/home/thor/.openclaw/settings/amap.env`

```bash
export AMAP_API_KEY="your_api_key"
```

### 加载环境变量

```bash
source /home/thor/.openclaw/settings/amap.env
```

## 功能

### 🗺️ 静态地图（推荐）

**搜索并生成带标记的地图**
```bash
amap-map-search "汉堡" "23.155254,113.346322" 3 1500
```
- 自动生成高清地图（1024x1024）
- 红点 A 标记您的位置
- 蓝点 B/C/D 标记搜索结果
- 自动发送并清理临时文件

### 📍 地理编码

**地址 → 坐标**
```bash
amap geocode --address="广州市天河区体育西路 100 号"
```

### 🏠 逆地理编码

**坐标 → 地址**
```bash
amap regeocode --location="113.346322,23.155254"
```

### 🚗 驾车路径规划

```bash
amap driving --origin="113.346322,23.155254" --destination="113.264434,23.129018"
```

### 🚶 步行路径规划

```bash
amap walking --origin="113.346322,23.155254" --destination="113.350000,23.160000"
```

### 🚌 公交路径规划

```bash
amap transit --origin="113.346322,23.155254" --destination="113.264434,23.129018"
```

### 🔍 POI 搜索

**搜索美食**
```bash
amap search --keywords="美食" --location="113.346322,23.155254" --radius=1000
```

**搜索酒店**
```bash
amap search --keywords="酒店" --location="113.346322,23.155254" --radius=2000
```

**搜索加油站**
```bash
amap search --keywords="加油站" --location="113.346322,23.155254" --types="加油站" --radius=3000
```

## 使用方式

### 方式 1：命令行

```bash
# 加载环境变量
source /home/thor/.openclaw/settings/amap.env

# 使用命令
amap driving --origin="起点坐标" --destination="终点坐标"
```

### 方式 2：直接跟我说

发送位置信息后，我会询问您想要：
- 🚗 路径规划（驾车/步行/公交）
- 🍽️ 搜索美食
- 🏨 搜索酒店
- ⛽ 搜索加油站
- 🏥 搜索医院
- 其他 POI 搜索

### 方式 3：包装脚本

```bash
# 搜索附近美食
amap-search-food "113.346322,23.155254"

# 规划驾车路线
amap-drive "起点坐标" "终点坐标"
```

## POI 类型参考

| 类型 | 关键词 | types 代码 |
|------|--------|-----------|
| 美食 | 美食、餐厅 | 餐饮服务 |
| 酒店 | 酒店、宾馆 | 住宿服务 |
| 加油站 | 加油站 | 加油站 |
| 医院 | 医院 | 医疗保健服务 |
| 银行 | 银行 | 金融服务 |
| 购物 | 购物、商场 | 购物服务 |
| 景点 | 景点、公园 | 风景名胜 |

## 示例

```bash
# 查询地址坐标
amap geocode --address="广州塔"

# 规划从当前位置到广州塔的驾车路线
amap driving --origin="113.346322,23.155254" --destination="113.325610,23.106500"

# 搜索附近 1 公里内的美食
amap search --keywords="美食" --location="113.346322,23.155254" --radius=1000
```

## API 限制

- 每日配额：根据 API Key 等级
- 并发限制：避免高频请求
- 超时设置：10 秒
