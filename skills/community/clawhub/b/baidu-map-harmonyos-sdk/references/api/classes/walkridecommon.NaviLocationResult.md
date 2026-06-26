[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / NaviLocationResult

# Class: NaviLocationResult

[walkridecommon](../modules/walkridecommon.md).NaviLocationResult

导航位置结果

**`Description`**

封装GPS和匹配后的位置信息

## Table of contents

### Constructors

- [constructor](walkridecommon.NaviLocationResult.md#constructor)

### Accessors

- [curRouteShapeIdx](walkridecommon.NaviLocationResult.md#currouteshapeidx)
- [gpsDirection](walkridecommon.NaviLocationResult.md#gpsdirection)
- [gpsSpeed](walkridecommon.NaviLocationResult.md#gpsspeed)
- [gpsLongitude](walkridecommon.NaviLocationResult.md#gpslongitude)
- [gpsLatitude](walkridecommon.NaviLocationResult.md#gpslatitude)
- [postDirection](walkridecommon.NaviLocationResult.md#postdirection)
- [postSpeed](walkridecommon.NaviLocationResult.md#postspeed)
- [postLongitude](walkridecommon.NaviLocationResult.md#postlongitude)
- [postLatitude](walkridecommon.NaviLocationResult.md#postlatitude)

### Methods

- [getGpsLocation](walkridecommon.NaviLocationResult.md#getgpslocation)
- [getPostLocation](walkridecommon.NaviLocationResult.md#getpostlocation)
- [toString](walkridecommon.NaviLocationResult.md#tostring)

## Constructors

### constructor

• **new NaviLocationResult**(): [`NaviLocationResult`](walkridecommon.NaviLocationResult.md)

#### Returns

[`NaviLocationResult`](walkridecommon.NaviLocationResult.md)

## Accessors

### curRouteShapeIdx

• `get` **curRouteShapeIdx**(): `number`

#### Returns

`number`

• `set` **curRouteShapeIdx**(`idx`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `idx` | `number` |

#### Returns

`void`

___

### gpsDirection

• `get` **gpsDirection**(): `number`

#### Returns

`number`

• `set` **gpsDirection**(`direction`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `direction` | `number` |

#### Returns

`void`

___

### gpsSpeed

• `get` **gpsSpeed**(): `number`

#### Returns

`number`

• `set` **gpsSpeed**(`speed`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `speed` | `number` |

#### Returns

`void`

___

### gpsLongitude

• `get` **gpsLongitude**(): `number`

#### Returns

`number`

• `set` **gpsLongitude**(`longitude`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `longitude` | `number` |

#### Returns

`void`

___

### gpsLatitude

• `get` **gpsLatitude**(): `number`

#### Returns

`number`

• `set` **gpsLatitude**(`latitude`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `latitude` | `number` |

#### Returns

`void`

___

### postDirection

• `get` **postDirection**(): `number`

#### Returns

`number`

• `set` **postDirection**(`direction`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `direction` | `number` |

#### Returns

`void`

___

### postSpeed

• `get` **postSpeed**(): `number`

#### Returns

`number`

• `set` **postSpeed**(`speed`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `speed` | `number` |

#### Returns

`void`

___

### postLongitude

• `get` **postLongitude**(): `number`

#### Returns

`number`

• `set` **postLongitude**(`longitude`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `longitude` | `number` |

#### Returns

`void`

___

### postLatitude

• `get` **postLatitude**(): `number`

#### Returns

`number`

• `set` **postLatitude**(`latitude`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `latitude` | `number` |

#### Returns

`void`

## Methods

### getGpsLocation

▸ **getGpsLocation**(): `Object`

获取GPS坐标

#### Returns

`Object`

| Name | Type |
| :------ | :------ |
| `longitude` | `number` |
| `latitude` | `number` |

___

### getPostLocation

▸ **getPostLocation**(): `Object`

获取匹配后的坐标

#### Returns

`Object`

| Name | Type |
| :------ | :------ |
| `longitude` | `number` |
| `latitude` | `number` |

___

### toString

▸ **toString**(): `string`

转换为字符串

#### Returns

`string`
