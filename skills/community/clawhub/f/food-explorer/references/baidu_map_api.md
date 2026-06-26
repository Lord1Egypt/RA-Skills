# 百度地图API文档参考

## 地理编码 API

### 请求地址
```
https://api.map.baidu.com/geocoding/v3/?address={address}&output=json&ak={your-ak}
```

### 请求参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| address | string | 是 | 待解析的地址 |
| ak | string | 是 | 应用API Key |
| output | string | 否 | 输出格式，默认为json |
| city | string | 否 | 地址所在城市，提高解析精度 |

### 响应示例
```json
{
  "status": 0,
  "result": {
    "location": {
      "lng": 120.128,
      "lat": 30.259
    },
    "precise": 1,
    "confidence": 80,
    "level": "景点"
  }
}
```

## 周边搜索 API

### 请求地址
```
https://api.map.baidu.com/place/v2/search?query={query}&location={lat},{lng}&radius={radius}&output=json&ak={your-ak}
```

### 请求参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| query | string | 是 | 检索关键词 |
| location | string | 是 | 经纬度，格式：纬度,经度 |
| radius | int | 否 | 检索半径，单位米，默认1000 |
| ak | string | 是 | 应用API Key |
| output | string | 否 | 输出格式，默认为json |
| page_size | int | 否 | 返回记录数量，默认10，最大20 |
| page_num | int | 否 | 分页页码，默认为0 |

### 响应示例
```json
{
  "status": 0,
  "results": [
    {
      "name": "楼外楼",
      "location": {
        "lat": 30.259,
        "lng": 120.128
      },
      "address": "西湖区孤山路30号",
      "telephone": "0571-87969682",
      "detail_info": {
        "tag": "美食;中餐厅",
        "overall_rating": "4.5",
        "price": "120",
        "detail_url": "..."
      }
    }
  ]
}
```

## 错误码

| 错误码 | 含义 |
|--------|------|
| 0 | 正常 |
| 1 | 服务器内部错误 |
| 2 | 请求参数非法 |
| 3 | 权限校验失败 |
| 4 | 配额校验失败 |
| 5 | 服务不可用 |
| 101 | AK参数不存在 |
| 200 | 应用不存在 |
| 201 | 服务被禁用 |
| 302 | 天配额超额 |

## 官方文档
- https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
- https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
