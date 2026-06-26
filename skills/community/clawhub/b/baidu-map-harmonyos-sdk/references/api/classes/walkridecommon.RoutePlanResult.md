[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / RoutePlanResult

# Class: RoutePlanResult

[walkridecommon](../modules/walkridecommon.md).RoutePlanResult

算路结果，算路完成的Msg中会带有这个信息 对应navi_engine_guidance_def.h中的NE_RoutePlan_Result_Enum

## Table of contents

### Constructors

- [constructor](walkridecommon.RoutePlanResult.md#constructor)

### Properties

- [SUCCESS](walkridecommon.RoutePlanResult.md#success)
- [SERVER\_UNUSUAL](walkridecommon.RoutePlanResult.md#server_unusual)
- [PARSE\_FAIL](walkridecommon.RoutePlanResult.md#parse_fail)
- [NET\_ERR](walkridecommon.RoutePlanResult.md#net_err)
- [INVALID](walkridecommon.RoutePlanResult.md#invalid)

## Constructors

### constructor

• **new RoutePlanResult**(): [`RoutePlanResult`](walkridecommon.RoutePlanResult.md)

#### Returns

[`RoutePlanResult`](walkridecommon.RoutePlanResult.md)

## Properties

### SUCCESS

▪ `Static` `Readonly` **SUCCESS**: ``0``

路线规划成功

___

### SERVER\_UNUSUAL

▪ `Static` `Readonly` **SERVER\_UNUSUAL**: ``16777216``

服务器异常

___

### PARSE\_FAIL

▪ `Static` `Readonly` **PARSE\_FAIL**: ``268435456``

解析失败

___

### NET\_ERR

▪ `Static` `Readonly` **NET\_ERR**: ``805306368``

网络错误

___

### INVALID

▪ `Static` `Readonly` **INVALID**: ``4294967295``

无效值
