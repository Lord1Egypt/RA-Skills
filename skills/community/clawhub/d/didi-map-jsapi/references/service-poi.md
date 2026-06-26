---
outline: deep
---
 # PoiService

**`地点检索相关服务`**  

滴滴拥有近6千万的兴趣点 (POI: Point of Interest) 数据，开发者使用相关的API，可以获得这些数据来满足相关的场景需求。

地点相关的检索服务，包含3个核心能力：
* 关键词检索（[textSearch](#textsearch)）：通过输入关键字，返回兴趣点的具体信息。
* 周边搜索（[inputTips](#inputtips)）：通过输入一个坐标点，返回该坐标点附近的兴趣点信息。
* 输入提示（[aroundSearch](#aroundsearch)）：提供POI关键字联想功能。

对于返回结果中的相关分类信息，可参阅[兴趣点（POI）分类表](/web/guide/POI分类表.md)


## textSearch

**`关键词检索服务`**

### 请求

#### 请求参数

| 参数名       | 必选 | 类型   | 描述                                            | 示例值               |
| ------------ | ---- | ------ | ----------------------------------------------- | -------------------- |
| keywords     | 是   | string | 检索关键词                                      | 麦当劳               |
| city         | 否   | string | 查询城市                                        | 北京市               |
| location     | 否   | string | 坐标，经纬度，格式"lng,lat"                     | 116.424790,39.956953 |
| types        | 否   | string | POI过滤类型(每个类型6位数字)，支持传多个。全部POI编码参考[POI分类表](/web/guide/POI分类表.md)    | "101000,101020"             |
| show_fields | 否 | string | 返回结果的扩展信息，sub_poi_list:返回子点数据, 不传则不返回子点数据 | "sub_poi_list" |
| city_limit         | 否   | boolean | 是否限定在当前城市检索，默认false 不限定城市                                        | false               |

#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key"
}).then(async ({ DiMap }) => {
    const poiService = new DiMap.PoiService()
    const [err, res] = await poiService.textSearch({
        city: "北京市",
        keywords: "天安门"
    })
    console.log("textSearch--res", res)
})
```

### 响应

#### 响应格式
成功响应为 **[TextSearchResponse][6]** 模型的JSON格式。

#### 响应示例
```javascript
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0ab788326914300d4379d2380c8c8702",
    "results": [
        {
            "name": "天安门广场",
            "location": {
                "lng": 116.397827,
                "lat": 39.90374
            },
            "address": "东城区东长安街",
            "province": "北京市",
            "city": "北京市",
            "district": "东城区",
            "adcode": "110101",
            "address_all": "东城区东长安街天安门广场",
            "poi_id": "271035635698419621769621927699651214368",
            "type": "221000"
        },
        {
            "name": "天安门东-地铁站",
            "location": {
                "lng": 116.401574,
                "lat": 39.907776
            },
            "address": "地铁1号线八通线",
            "province": "北京市",
            "city": "北京市",
            "district": "东城区",
            "adcode": "110101",
            "address_all": "地铁1号线八通线天安门东-地铁站",
            "poi_id": "70713753404993906693064901477969483602",
            "type": "271014"
        }
    ]
}
```


## inputTips

**`输入提示服务`**

### 请求

#### 请求参数

| 参数名 | 必选 | 类型 | 描述 | 示例值 |
|-------|------|------|------|--------|
| keywords | 是 | string | 搜索关键词 | 星巴 |
| location | 否 | string | 坐标，经纬度，格式"lng,lat" | 116.434091,39.90923 |
| city | 否 | string | 城市名称 | 北京市 |
| types | 否  | string | POI过滤类型(每个类型6位数字)，支持传多个。全部POI编码参考[POI分类表](/web/guide/POI分类表.md)               | "101000,101020" |
| show_fields | 否  | string | 返回结果的扩展信息，sub_poi_list:返回子点数据, 不传则不返回子点数据 | "sub_poi_list" |
| city_limit | 否   | boolean | 是否限定在当前城市检索，默认false 不限定城市                                        | false               |

#### 请求示例
```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key"
}).then(async ({ DiMap }) => {
    const poiService = new DiMap.PoiService()
    const [err, res] = await poiService.inputTips({
        city: "北京市",
        keywords: "星巴"
    })
    console.log("inputTips--res", res)
})
```

### 响应

#### 响应格式
成功响应为 **[TextSearchResponse][6]** 模型的JSON格式。

#### 响应示例

```javascript
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0a885d7a691439cc65feea440cc93102",
    "results": [
        {
            "name": "星巴克咖啡(北京新世界店)",
            "location": {
                "lng": 116.418078,
                "lat": 39.898359
            },
            "address": "东城区崇文门外大街3号新世界百货一层",
            "province": "北京市",
            "city": "北京市",
            "district": "东城区",
            "adcode": "0",
            "address_all": "东城区崇文门外大街3号新世界百货一层星巴克咖啡(北京新世界店)",
            "poi_id": "339208638933202157406551275055023483319",
            "type": "161300"
        }
    ]
}
```

## aroundSearch

**`周边检索服务`**

### 请求

#### 请求参数

| 参数名 | 必选 | 类型 | 描述                            | 示例值           |
|-------|----|------|-------------------------------|---------------|
| keywords | 是  | string | 检索关键词                         | 麦当劳           |
| location | 否  | string | 坐标，经纬度，格式"lng,lat"            | 116.424790,39.956953 |
| max_distance | 否  | string | 以 location 为中心的最大检索范围的半径，单位为米，范围为0-50000，默认值为5000 | "1000"        |
| city | 否  | string | 用户选择的地点的city名字(城市名)          | 北京市           |
| sort_rule | 否 | string | 规定返回结果的排序规则。distance:按距离排序; weight:综合排序。 默认值为weight | "distance" |
| types | 否  | string | POI过滤类型(每个类型6位数字)，支持传多个。全部POI编码参考[POI分类表](/web/guide/POI分类表.md)                  | "101000,101020"  |
| show_fields | 否  | string | 返回结果的扩展信息，sub_poi_list:返回子点数据, 不传则不返回子点数据 | "sub_poi_list" |
| city_limit | 否   | boolean | 是否限定在当前城市检索，默认false 不限定城市                                        | false               |

#### 请求示例

```javascript
window.DiMapLoader.load({
  key: "您申请的服务端key"
}).then(async ({ DiMap }) => {
    const poiService = new DiMap.PoiService()
    const [err, res] = await poiService.aroundSearch({
        keywords: "故宫",
        max_distance: "1000",
        location: "116.397428,39.90923",
        sort_rule: "distance"
    })
    console.log("aroundSearch--res", res)
})
```

### 响应

#### 响应格式
成功响应为 **[TextSearchResponse][6]** 模型的JSON格式。

#### 响应示例

```javascript
{
    "status": 10000,
    "msg": "OK",
    "trace_id": "0a88098669143be9232b0e6b0ca3cf02",
    "results": [
        {
            "name": "端门",
            "location": {
                "lng": 116.39743,
                "lat": 39.91033
            },
            "address": "东城区故宫内",
            "province": "北京市",
            "city": "北京市",
            "district": "东城区",
            "adcode": "110101",
            "address_all": "东城区故宫内端门",
            "poi_id": "45573293031011243924784934532272048943",
            "type": "801010",
            "distance": 122
        }
    ]
}
```

[1]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[2]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Error

[5]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise

[6]:/web/guide/响应模型.html#textsearchresponse