[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / RoutePlanError

# Enumeration: RoutePlanError

[walkridecommon](../modules/walkridecommon.md).RoutePlanError

算路失败错误码
1000-1999: 服务端和数据处理相关错误
2000-2999: 参数和距离相关错误
3000-3999: 功能支持相关错误,专门用于"不支持某功能"类型的错误
4000-4999: 引擎和导航状态错误,关于引擎和导航状态的各种错误
5000-5999: 系统和网络错误,SDK初始化、超时和通用错误

## Table of contents

### Enumeration Members

- [SERVER\_UNUSUAL](walkridecommon.RoutePlanError.md#server_unusual)
- [PARSE\_FAIL](walkridecommon.RoutePlanError.md#parse_fail)
- [NET\_ERR](walkridecommon.RoutePlanError.md#net_err)
- [FORWARD\_AK\_ERROR](walkridecommon.RoutePlanError.md#forward_ak_error)
- [INVAILD\_PERMISSION](walkridecommon.RoutePlanError.md#invaild_permission)
- [PARAM\_ERROR](walkridecommon.RoutePlanError.md#param_error)
- [DISTANCE\_LESS\_THAN\_30M](walkridecommon.RoutePlanError.md#distance_less_than_30m)
- [DISTANCE\_MORE\_THAN\_50KM](walkridecommon.RoutePlanError.md#distance_more_than_50km)
- [DISTANCE\_TOO\_CLOSE](walkridecommon.RoutePlanError.md#distance_too_close)
- [DISTANCE\_MORE\_THAN](walkridecommon.RoutePlanError.md#distance_more_than)
- [ROUTE\_DIS\_SAME](walkridecommon.RoutePlanError.md#route_dis_same)
- [IS\_NOT\_SUPPORT\_INDOOR\_NAVI](walkridecommon.RoutePlanError.md#is_not_support_indoor_navi)
- [IS\_NOT\_SUPPORT\_AR\_NAVI](walkridecommon.RoutePlanError.md#is_not_support_ar_navi)
- [ENGINE\_STATUS\_ERROR](walkridecommon.RoutePlanError.md#engine_status_error)
- [NAVI\_STATUS\_ERROR](walkridecommon.RoutePlanError.md#navi_status_error)
- [SDK\_NOT\_INITIALIZED](walkridecommon.RoutePlanError.md#sdk_not_initialized)
- [REQUEST\_TIMEOUT](walkridecommon.RoutePlanError.md#request_timeout)
- [ENGINE\_SEARCH\_ERROR](walkridecommon.RoutePlanError.md#engine_search_error)
- [INTERRUPTED](walkridecommon.RoutePlanError.md#interrupted)

## Enumeration Members

### SERVER\_UNUSUAL

• **SERVER\_UNUSUAL** = ``1000``

服务器异常

___

### PARSE\_FAIL

• **PARSE\_FAIL** = ``1001``

解析失败

___

### NET\_ERR

• **NET\_ERR** = ``1002``

网络错误

___

### FORWARD\_AK\_ERROR

• **FORWARD\_AK\_ERROR** = ``1010``

鉴权失败

___

### INVAILD\_PERMISSION

• **INVAILD\_PERMISSION** = ``1011``

权限未开通

___

### PARAM\_ERROR

• **PARAM\_ERROR** = ``2000``

参数错误

___

### DISTANCE\_LESS\_THAN\_30M

• **DISTANCE\_LESS\_THAN\_30M** = ``2001``

距离太近

___

### DISTANCE\_MORE\_THAN\_50KM

• **DISTANCE\_MORE\_THAN\_50KM** = ``2002``

距离太远

___

### DISTANCE\_TOO\_CLOSE

• **DISTANCE\_TOO\_CLOSE** = ``2003``

距离过近

___

### DISTANCE\_MORE\_THAN

• **DISTANCE\_MORE\_THAN** = ``2004``

距离过远

___

### ROUTE\_DIS\_SAME

• **ROUTE\_DIS\_SAME** = ``2005``

起终点相同

___

### IS\_NOT\_SUPPORT\_INDOOR\_NAVI

• **IS\_NOT\_SUPPORT\_INDOOR\_NAVI** = ``3000``

不支持该室内导航

___

### IS\_NOT\_SUPPORT\_AR\_NAVI

• **IS\_NOT\_SUPPORT\_AR\_NAVI** = ``3001``

API级别不支持AR步行导航

___

### ENGINE\_STATUS\_ERROR

• **ENGINE\_STATUS\_ERROR** = ``4000``

引擎状态错误

___

### NAVI\_STATUS\_ERROR

• **NAVI\_STATUS\_ERROR** = ``4001``

导航状态错误

___

### SDK\_NOT\_INITIALIZED

• **SDK\_NOT\_INITIALIZED** = ``5000``

SDK未初始化

___

### REQUEST\_TIMEOUT

• **REQUEST\_TIMEOUT** = ``5001``

请求超时

___

### ENGINE\_SEARCH\_ERROR

• **ENGINE\_SEARCH\_ERROR** = ``5002``

引擎检索错误

___

### INTERRUPTED

• **INTERRUPTED** = ``5003``

手动终止
