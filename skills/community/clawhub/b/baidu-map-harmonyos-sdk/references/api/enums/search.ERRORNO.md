[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / ERRORNO

# Enumeration: ERRORNO

[search](../modules/search.md).ERRORNO

检索结果状态定义

## Table of contents

### Enumeration Members

- [NO\_ERROR](search.ERRORNO.md#no_error)
- [RESULT\_NOT\_FOUND](search.ERRORNO.md#result_not_found)
- [AMBIGUOUS\_KEYWORD](search.ERRORNO.md#ambiguous_keyword)
- [AMBIGUOUS\_ROURE\_ADDR](search.ERRORNO.md#ambiguous_roure_addr)
- [NOT\_SUPPORT\_BUS](search.ERRORNO.md#not_support_bus)
- [NOT\_SUPPORT\_BUS\_2CITY](search.ERRORNO.md#not_support_bus_2city)
- [ST\_EN\_TOO\_NEAR](search.ERRORNO.md#st_en_too_near)
- [KEY\_ERROR](search.ERRORNO.md#key_error)
- [PERMISSION\_UNFINISHED](search.ERRORNO.md#permission_unfinished)
- [NETWORK\_TIME\_OUT](search.ERRORNO.md#network_time_out)
- [NETWORK\_ERROR](search.ERRORNO.md#network_error)
- [POIINDOOR\_BID\_ERROR](search.ERRORNO.md#poiindoor_bid_error)
- [POIINDOOR\_FLOOR\_ERROR](search.ERRORNO.md#poiindoor_floor_error)
- [POIINDOOR\_SERVER\_ERROR](search.ERRORNO.md#poiindoor_server_error)
- [INDOOR\_ROUTE\_NO\_IN\_BUILDING](search.ERRORNO.md#indoor_route_no_in_building)
- [INDOOR\_ROUTE\_NO\_IN\_SAME\_BUILDING](search.ERRORNO.md#indoor_route_no_in_same_building)
- [MASS\_TRANSIT\_SERVER\_ERROR](search.ERRORNO.md#mass_transit_server_error)
- [MASS\_TRANSIT\_OPTION\_ERROR](search.ERRORNO.md#mass_transit_option_error)
- [MASS\_TRANSIT\_NO\_POI\_ERROR](search.ERRORNO.md#mass_transit_no_poi_error)
- [SEARCH\_SERVER\_INTERNAL\_ERROR](search.ERRORNO.md#search_server_internal_error)
- [SEARCH\_OPTION\_ERROR](search.ERRORNO.md#search_option_error)
- [REQUEST\_ERROR](search.ERRORNO.md#request_error)
- [NO\_ADVANCED\_PERMISSION](search.ERRORNO.md#no_advanced_permission)
- [INVALID\_DISTRICT\_ID](search.ERRORNO.md#invalid_district_id)
- [NO\_DATA\_FOR\_LATLNG](search.ERRORNO.md#no_data_for_latlng)
- [PARAMER\_ERROR](search.ERRORNO.md#paramer_error)

## Enumeration Members

### NO\_ERROR

• **NO\_ERROR** = ``0``

检索结果正常返回

___

### RESULT\_NOT\_FOUND

• **RESULT\_NOT\_FOUND** = ``1``

没有找到检索结果

___

### AMBIGUOUS\_KEYWORD

• **AMBIGUOUS\_KEYWORD** = ``2``

检索词有岐义

___

### AMBIGUOUS\_ROURE\_ADDR

• **AMBIGUOUS\_ROURE\_ADDR** = ``3``

检索地址有岐义

___

### NOT\_SUPPORT\_BUS

• **NOT\_SUPPORT\_BUS** = ``4``

该城市不支持公交搜索

___

### NOT\_SUPPORT\_BUS\_2CITY

• **NOT\_SUPPORT\_BUS\_2CITY** = ``5``

不支持跨城市公交

___

### ST\_EN\_TOO\_NEAR

• **ST\_EN\_TOO\_NEAR** = ``6``

起终点太近

___

### KEY\_ERROR

• **KEY\_ERROR** = ``7``

key有误

___

### PERMISSION\_UNFINISHED

• **PERMISSION\_UNFINISHED** = ``8``

授权未完成

___

### NETWORK\_TIME\_OUT

• **NETWORK\_TIME\_OUT** = ``9``

网络超时

___

### NETWORK\_ERROR

• **NETWORK\_ERROR** = ``10``

网络错误

___

### POIINDOOR\_BID\_ERROR

• **POIINDOOR\_BID\_ERROR** = ``11``

poi室内检索bid错误

___

### POIINDOOR\_FLOOR\_ERROR

• **POIINDOOR\_FLOOR\_ERROR** = ``12``

poi室内检索floor错误

___

### POIINDOOR\_SERVER\_ERROR

• **POIINDOOR\_SERVER\_ERROR** = ``13``

poi室内检索服务错误

___

### INDOOR\_ROUTE\_NO\_IN\_BUILDING

• **INDOOR\_ROUTE\_NO\_IN\_BUILDING** = ``14``

室内路线规划起点、终点不在支持室内路径规划的位置，
包括起终点在室内，但是该室内图不支持路线规划，对于该中场景，
可以通过判断点是否在室内区分。

___

### INDOOR\_ROUTE\_NO\_IN\_SAME\_BUILDING

• **INDOOR\_ROUTE\_NO\_IN\_SAME\_BUILDING** = ``15``

室内路线规划起终点不在同一个室内

___

### MASS\_TRANSIT\_SERVER\_ERROR

• **MASS\_TRANSIT\_SERVER\_ERROR** = ``16``

跨城公共交通服务器内部错误

___

### MASS\_TRANSIT\_OPTION\_ERROR

• **MASS\_TRANSIT\_OPTION\_ERROR** = ``17``

跨城公共交通错误码：参数无效

___

### MASS\_TRANSIT\_NO\_POI\_ERROR

• **MASS\_TRANSIT\_NO\_POI\_ERROR** = ``18``

跨城公共交通没有匹配的POI

___

### SEARCH\_SERVER\_INTERNAL\_ERROR

• **SEARCH\_SERVER\_INTERNAL\_ERROR** = ``19``

服务器内部错误

___

### SEARCH\_OPTION\_ERROR

• **SEARCH\_OPTION\_ERROR** = ``20``

参数错误

___

### REQUEST\_ERROR

• **REQUEST\_ERROR** = ``21``

请求错误

___

### NO\_ADVANCED\_PERMISSION

• **NO\_ADVANCED\_PERMISSION** = ``22``

没有高级权限

___

### INVALID\_DISTRICT\_ID

• **INVALID\_DISTRICT\_ID** = ``23``

区域编码无效

___

### NO\_DATA\_FOR\_LATLNG

• **NO\_DATA\_FOR\_LATLNG** = ``24``

经纬度所在地区无数据覆盖

___

### PARAMER\_ERROR

• **PARAMER\_ERROR** = ``25``

请求参数错误
