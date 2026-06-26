[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / base

# Module: base

## Table of contents

### Namespaces

- [AppMD5](base.AppMD5.md)

### Enumerations

- [CoordType](../enums/base.CoordType.md)

### Classes

- [WeightedLatLng](../classes/base.WeightedLatLng.md)
- [Bounds](../classes/base.Bounds.md)
- [Initializer](../classes/base.Initializer.md)
- [LatLng](../classes/base.LatLng.md)
- [LatLngBounds](../classes/base.LatLngBounds.md)
- [AlgorithmUtil](../classes/base.AlgorithmUtil.md)
- [MapEngineConfig](../classes/base.MapEngineConfig.md)
- [DeviceInfo](../classes/base.DeviceInfo.md)
- [SysOSAPI](../classes/base.SysOSAPI.md)
- [PermissionCheckResult](../classes/base.PermissionCheckResult.md)
- [PermissionCheck](../classes/base.PermissionCheck.md)
- [Point](../classes/base.Point.md)
- [CoordTrans](../classes/base.CoordTrans.md)
- [CoordUtil](../classes/base.CoordUtil.md)
- [CoordUtilConcurrent](../classes/base.CoordUtilConcurrent.md)
- [BMFileUtils](../classes/base.BMFileUtils.md)
- [BMLog](../classes/base.BMLog.md)
- [BMStringUtils](../classes/base.BMStringUtils.md)
- [BMThreadUtils](../classes/base.BMThreadUtils.md)
- [StringBuilder](../classes/base.StringBuilder.md)
- [MapLanguageStorageManager](../classes/base.MapLanguageStorageManager.md)

### Interfaces

- [BuildingInfo](../interfaces/base.BuildingInfo.md)
- [PermissionCheckResultListener](../interfaces/base.PermissionCheckResultListener.md)
- [LanguageChangeListener](../interfaces/base.LanguageChangeListener.md)

### Type Aliases

- [BMObject](base.md#bmobject)
- [Nullable](base.md#nullable)
- [UserInfoType](base.md#userinfotype)

### Functions

- [getAppContext](base.md#getappcontext)

## Type Aliases

### BMObject

Ƭ **BMObject**: `number` \| `string` \| `boolean` \| `number`[] \| `string`[] \| `boolean`[] \| `object` \| `Object` \| `ArrayBuffer` \| `JSON`

用于代替 any 类型

___

### Nullable

Ƭ **Nullable**\<`T`\>: `T` \| ``null``

#### Type parameters

| Name |
| :------ |
| `T` |

___

### UserInfoType

Ƭ **UserInfoType**: `Record`\<`string`, `Object`\>

## Functions

### getAppContext

▸ **getAppContext**(): `BMAppContext`

#### Returns

`BMAppContext`
