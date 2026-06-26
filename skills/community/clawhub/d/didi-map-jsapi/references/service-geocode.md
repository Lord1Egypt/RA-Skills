---
outline: deep
---
 # GeoCodeService

**`地理编码服务`**

滴滴地图地理编码服务提供地址与坐标之间的双向转换能力，帮助开发者实现精确的位置定位和地址解析。

地理编码服务包含2个核心能力：

* 地理编码（[geoCode](#geocode)）：将地址信息转换为结构化的地理位置信息（经纬度等）。
* 逆地理编码（[reverseGeoCode](#reversegeocode)）：将经纬度坐标转换为结构化的地址信息，可获取坐标点所在的道路、门牌号、区域等信息。


## geoCode

**`地理编码`**

### 请求

#### 请求参数
| 参数名 | 必选 | 类型 | 描述 | 示例值 |
|--------|------|------|------|--------|
| city | 是 | string | 城市名称 | "北京市" |
| address | 是 | string | 地址信息 | "北京市海淀区西二旗东路1号" |

#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key",
}).then(async ({ DiMap }) => {
    const geoCodeService = new DiMap.GeoCodeService();
    const [err, res] = await geoCodeService.geoCode({
        city: "北京市",
        address: "北京市海淀区西二旗东路1号"
    });
    console.log("geoCode--res", res)
})
```
### 响应

#### 响应格式
成功响应为 **[GeocodeRPCResponse][4]** 模型的JSON格式。

#### 响应示例
```javascript
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0a885e2b691444b6bcbae6e40d0ab302",
    "results": {
        "count": 3,
        "geocodes": [
            {
                "adcode": "110108",
                "city": "北京市",
                "country": "中国",
                "district": "海淀区",
                "location": {
                    "lng": 116.302861,
                    "lat": 40.055095
                },
                "poi_id": "222769345256142011623105356677419489085",
                "province": "北京市"
            },
            {
                "country": "中国",
                "province": "北京市",
                "city": "北京市",
                "district": "海淀区",
                "adcode": "110108",
                "location": {
                    "lng": 116.30191,
                    "lat": 40.05454
                },
                "poi_id": "134885129598244948207287594764019661967"
            },
        ]
    }    
}
```

## reverseGeoCode

**`逆地理编码`**

### 请求

#### 请求参数
| 参数名 | 必选 | 类型 | 描述 | 示例值 |
|--------|------|------|------|--------|
| location | 是 | string | 经纬度坐标 | "116.302861,40.055095" |

#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key",
}).then(async ({ DiMap }) => {
    const geoCodeService = new DiMap.GeoCodeService();
    const [err, res] = await geoCodeService.reverseGeoCode({
        location: "116.302861,40.055095" 
    });
    console.log("reverseGeoCode--res", res);
})
```

### 响应

#### 响应格式
成功响应为 **[ReverseGeoResponse][5]** 模型的JSON格式。

#### 响应示例
```javascript
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0ab76ac4691450504ab9a4b20d6c0a02",
    "results": [
        {
            "adcode": "110108",
            "address": "北京市海淀区上地东路1号院1号(西二旗地铁站A1北入口步行290米)",
            "address_all": "北京市海淀区上地东路1号院1号(西二旗地铁站A1北入口步行290米)盈创动力园区A座南厅",
            "city": "北京市",
            "district": "海淀区",
            "location": {
                "lng": 116.302861,
                "lat": 40.055095
            },
            "name": "盈创动力园区A座南厅",
            "poi_id": "222769345256142011623105356677419489085",
            "province": "北京市"
        }
    ]
}
```


[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise

[4]:/web/guide/响应模型.html#geocoderpcresponse

[5]:/web/guide/响应模型.html#reversegeoresponse