# 百度地图行政区划查询 API

## 服务概述

行政区划查询接口用于获取中国行政区划的详细信息。支持通过行政区划名称或adcode进行查询，返回结果包括行政区划的边界坐标、中心点、父级行政区划、行政区划级别等详细信息。该接口适用于需要行政区划数据的各类应用场景，如地图应用、数据分析、地址解析等。

- **版本**: 2.0.0
- **服务标识**: `region_search`
- **官方文档**: <https://lbs.baidu.com/faq/api?title=webapi/district-search/base>

### API调用

**GET** `https://api.map.baidu.com/api_region_search/v1/`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| ak | string | T | - | 开发者密钥，即API Key，用于身份验证和配额管理。 | E4805d16520de693a3fe707cdc962045 |
| keyword | string | T | - | 检索行政区划关键字。仅支持单关键字检索，可填写行政区名称（如“中国”“全国”、省/市/区/镇名称）或 adcode。 | 河北 |
| sub_admin | string |  | 0 | 行政区划显示子级级数。可填 0、1、2、3 等：0 不返回下级；1 返回下一级；2 返回下两级；3 返回下三级，以此类推。 | 2 |
| extensions_code | string (enum: 0, 1) |  | 0 | 是否召回国标行政区划编码，1 为召回，0 为不召回。 | 1 |
| boundary | string (enum: 0, 1) |  | 0 | 是否返回区划边界数据：0 不返回，1 返回。仅返回查询行政区划的边界，不返回子级边界；仅支持省/市/区边界，暂不支持乡镇/街道。 | 1 |
| boundarycode | string |  | - | 需要返回边界数据的行政区划编码。若输入 adcode 则返回该 adcode 边界；若未输入或输入错误，则返回 keyword 匹配到的第一个行政区划边界。 | 110112 |

### 响应结果

#### 响应示例 (供参考)

```json
{
  "result": {
    "name": "北京市",
    "level": "province",
    "adcode": "110000",
    "parent": {
      "name": "中国",
      "adcode": "100000"
    },
    "boundary": "116.123,39.123;116.456,39.456",
    "children": [
      {
        "name": "东城区",
        "level": "district",
        "adcode": "110101"
      }
    ],
    "location": {
      "lat": 39.929986,
      "lng": 116.395645
    }
  },
  "status": 0,
  "message": "ok"
}
```

#### 响应字段定义 (基于 Schema)

| 字段路径 | 类型 | 必填 | 说明 | 示例 |
|----------|------|------|------|------|
| `message` | string |  | 状态码对应的描述信息。 | ok |
| `result` | object |  | 查询结果对象。 | None |
| `result.adcode` | string |  | 行政区划代码。 | 110000 |
| `result.boundary` | string |  | 行政区划边界坐标，格式为经纬度坐标串，需设置 boundary=1 时返回。 | 116.123,39.123;116.456,39.456 |
| `result.children` | array |  | 子级行政区划列表，当 sub_admin 大于 0 时返回。 | None |
| `result.children[].adcode` | string |  | 子级行政区划代码。 | 110101 |
| `result.children[].level` | string |  | 子级行政区划级别。 | district |
| `result.children[].name` | string |  | 子级行政区划名称。 | 东城区 |
| `result.level` | string (enum: country, province, city... (共5个值)) |  | 行政区划级别，如 country、province、city、district、town 等。 | province |
| `result.location` | object |  | 行政区划的中心点坐标。 | None |
| `result.location.lat` | number |  | 中心点纬度。 | 39.929986 |
| `result.location.lng` | number |  | 中心点经度。 | 116.395645 |
| `result.name` | string |  | 行政区划名称。 | 北京市 |
| `result.parent` | object |  | 父级行政区划信息。 | None |
| `result.parent.adcode` | string |  | 父级行政区划代码。 | 100000 |
| `result.parent.name` | string |  | 父级行政区划名称。 | 中国 |
| `status` | integer |  | 返回结果状态码，0表示成功，其他值为错误码。<br/><br/>**枚举值说明：**<br/>`0`: ok：正常<br/>`1`: 服务器内部错误：服务器端出现未知错误，请稍后重试<br/>`2`: 请求参数非法：请求参数缺失或格式错误<br/>`3`: 权限校验失败：ak无效或没有权限<br/>`4`: 配额校验失败：访问超出配额限制<br/>`5`: ak不存在或被封禁：ak不存在或已被封禁，请检查ak状态<br/>`101`: 服务禁用：该服务已被禁用<br/>`102`: 不通过白名单或安全码不对：服务器没有开启白名单，或安全码不对 | 0 |

### 常见问题

**Q: 支持查询哪些级别的行政区划？**

A: 支持国家(country)、省(province)、市(city)、区/县(district)级别的行政区划查询

**Q: 如何获取行政区划的边界坐标？**

A: 设置 boundary=1 可返回边界坐标串（boundary 字段），格式为'经度,纬度;经度,纬度;...'

**Q: 如何获取下一级行政区划？**

A: 设置 sub_admin 大于 0 可返回子级行政区划；如 sub_admin=1 返回下一级，sub_admin=2 返回下两级

**Q: 边界坐标使用什么坐标系？**

A: 返回的边界坐标使用百度BD-09坐标系

**Q: 如何获取ak？**

A: 需要在百度地图开放平台控制台（https://lbsyun.baidu.com/）注册并创建应用获取API Key
