---
name: amap-map
description: 高德地图 API 技能（搜索、周边、POI、导航、地理编码）。调用 /scripts/amap.py，支持关键词搜索、周边搜索、POI 详情、步行/骑行/驾车路径规划、地址转坐标。
---

# 高德地图技能 (Amap Map)

## 使用说明

**调用脚本**：
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py <功能> <参数>
python3 /root/.openclaw/skills/amap-map/scripts/amap.py --usage  # 查看使用统计
```

## 功能列表

### 1. 关键词搜索（text_search）
搜索 POI 地点信息
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py text_search "餐厅" "北京"
```

### 2. 周边搜索（around_search）
搜索指定位置周边的 POI
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py around_search "116.397428,39.90923" "餐厅" 1000
```
参数：经纬度，关键词，半径（米，默认 1000）

### 3. POI 详情（poi_detail）
获取 POI 详细信息
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py poi_detail "POI_ID"
```

### 4. 步行导航（walking）
步行路径规划
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py walking "116.397428,39.90923" "116.407428,39.91923"
```
参数：起点经纬度，终点经纬度

### 5. 骑行导航（bicycling）
骑行路径规划（支持 500km 内）
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py bicycling "116.397428,39.90923" "116.407428,39.91923"
```

### 6. 驾车导航（driving）
驾车路径规划
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py driving "116.397428,39.90923" "116.407428,39.91923"
```

### 7. 地理编码（geo）
地址转经纬度
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py geo "北京市天安门广场" "北京"
```
参数：地址，城市（可选）

### 8. 逆地理编码（regeocode）
经纬度转地址
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py regeocode "116.397428,39.90923"
```

### 9. 查看使用统计（--usage）
查看 API 调用统计和剩余配额
```bash
python3 /root/.openclaw/skills/amap-map/scripts/amap.py --usage
```

## 触发条件

- 用户询问路线、导航
- 查找附近的餐厅、景点、设施等
- 需要地址和坐标转换
- 查询 POI 详细信息

## 返回格式

JSON 格式，包含：
- `status`: "1" 表示成功，"0" 表示失败
- `info`: 状态说明
- 具体数据根据功能不同而异

## API 密钥配置

在 `~/.openclaw/openclaw.json` 中配置：
```json
{
  "skills": {
    "entries": {
      "amap-map": {
        "enabled": true,
        "apiKey": "你的高德 API Key"
      }
    }
  }
}
```

## 获取 API Key

1. 访问 https://lbs.amap.com/
2. 注册/登录开发者账号
3. 创建应用，获取 Web 服务 API Key
4. 启用相关服务（Web 服务 API）

## 使用统计说明

运行 `--usage` 可查看：
- 总调用次数、成功/失败次数
- 每日配额（5000 次/天）和今日剩余
- 最近 7 天每日调用记录

**配额说明**：高德个人开发者账号每日免费配额 5000 次，次日 0 点重置。

统计文件位置：`/root/.openclaw/workspace/skills/amap-map/.usage.json`
