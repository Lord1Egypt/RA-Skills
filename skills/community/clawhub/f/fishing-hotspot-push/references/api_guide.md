# API 密钥获取指南

## 高德地图 API Key

1. 访问 https://lbs.amap.com/
2. 注册/登录 → 控制台 → 应用管理 → 创建新应用
3. 添加 Key → 服务平台选择「**Web服务**」
4. 复制 Key

使用的 API:
- 地理编码: `/v3/geocode/geo`
- POI搜索: `/v3/place/text`
- 周边搜索: `/v3/place/around`

免费额度: 5000次/天

## 和风天气 API Key

1. 访问 https://dev.qweather.com/
2. 注册/登录 → 控制台 → 创建项目
3. 选择「**免费订阅**」(1000次/天)
4. 复制 Key

使用的 API:
- 城市搜索: `/v2/city/lookup`
- 7天预报: `/v7/weather/7d`
- 钓鱼指数: `/v7/indices/1d`

免费额度: 1000次/天

## 配置共享

`fishing-hotspot-push` 和 `fishing-trip-planner` 共用同一套 API Key。

如果已配置过 `fishing-trip-planner`，`fishing-hotspot-push` 会自动读取其配置，无需重复输入。
