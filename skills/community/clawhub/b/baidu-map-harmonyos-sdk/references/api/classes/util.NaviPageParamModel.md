[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / NaviPageParamModel

# Class: NaviPageParamModel

[util](../modules/util.md).NaviPageParamModel

## Hierarchy

- `GeneralParamModel`

  ↳ **`NaviPageParamModel`**

## Implements

- [`NaviPageParam`](../interfaces/util.NaviPageParam.md)

## Table of contents

### Constructors

- [constructor](util.NaviPageParamModel.md#constructor)

### Properties

- [coord\_type](util.NaviPageParamModel.md#coord_type)
- [needLocation](util.NaviPageParamModel.md#needlocation)
- [isReducedAccuracyEnough](util.NaviPageParamModel.md#isreducedaccuracyenough)
- [popRoot](util.NaviPageParamModel.md#poproot)
- [location](util.NaviPageParamModel.md#location)
- [uid](util.NaviPageParamModel.md#uid)

### Accessors

- [getCoord\_type](util.NaviPageParamModel.md#getcoord_type)
- [getNeedLocation](util.NaviPageParamModel.md#getneedlocation)
- [getIsReducedAccuracyEnough](util.NaviPageParamModel.md#getisreducedaccuracyenough)
- [getPopRoot](util.NaviPageParamModel.md#getpoproot)
- [getLocation](util.NaviPageParamModel.md#getlocation)
- [getUid](util.NaviPageParamModel.md#getuid)

### Methods

- [setLocation](util.NaviPageParamModel.md#setlocation)
- [setUid](util.NaviPageParamModel.md#setuid)
- [setCoord\_type](util.NaviPageParamModel.md#setcoord_type)
- [setNeedLocation](util.NaviPageParamModel.md#setneedlocation)
- [setIsReducedAccuracyEnough](util.NaviPageParamModel.md#setisreducedaccuracyenough)
- [setPopRoot](util.NaviPageParamModel.md#setpoproot)

## Constructors

### constructor

• **new NaviPageParamModel**(`naviModel?`): [`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `naviModel?` | [`NaviPageParam`](../interfaces/util.NaviPageParam.md) |

#### Returns

[`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Overrides

GeneralParamModel.constructor

## Properties

### coord\_type

• **coord\_type**: [`CoordType`](../enums/base.CoordType.md)

#### Inherited from

GeneralParamModel.coord\_type

___

### needLocation

• **needLocation**: `string`

#### Inherited from

GeneralParamModel.needLocation

___

### isReducedAccuracyEnough

• **isReducedAccuracyEnough**: `string`

#### Inherited from

GeneralParamModel.isReducedAccuracyEnough

___

### popRoot

• **popRoot**: `string`

#### Inherited from

GeneralParamModel.popRoot

___

### location

• **location**: `string`

#### Implementation of

[NaviPageParam](../interfaces/util.NaviPageParam.md).[location](../interfaces/util.NaviPageParam.md#location)

___

### uid

• **uid**: `string`

#### Implementation of

[NaviPageParam](../interfaces/util.NaviPageParam.md).[uid](../interfaces/util.NaviPageParam.md#uid)

## Accessors

### getCoord\_type

• `get` **getCoord_type**(): [`CoordType`](../enums/base.CoordType.md)

#### Returns

[`CoordType`](../enums/base.CoordType.md)

#### Inherited from

GeneralParamModel.getCoord\_type

___

### getNeedLocation

• `get` **getNeedLocation**(): `string`

#### Returns

`string`

#### Inherited from

GeneralParamModel.getNeedLocation

___

### getIsReducedAccuracyEnough

• `get` **getIsReducedAccuracyEnough**(): `string`

#### Returns

`string`

#### Inherited from

GeneralParamModel.getIsReducedAccuracyEnough

___

### getPopRoot

• `get` **getPopRoot**(): `string`

#### Returns

`string`

#### Inherited from

GeneralParamModel.getPopRoot

___

### getLocation

• `get` **getLocation**(): `string`

#### Returns

`string`

___

### getUid

• `get` **getUid**(): `string`

#### Returns

`string`

## Methods

### setLocation

▸ **setLocation**(`value`): [`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`NaviPageParamModel`](util.NaviPageParamModel.md)

___

### setUid

▸ **setUid**(`value`): [`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`NaviPageParamModel`](util.NaviPageParamModel.md)

___

### setCoord\_type

▸ **setCoord_type**(`value`): [`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | [`CoordType`](../enums/base.CoordType.md) |

#### Returns

[`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Overrides

GeneralParamModel.setCoord\_type

___

### setNeedLocation

▸ **setNeedLocation**(`value`): [`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Overrides

GeneralParamModel.setNeedLocation

___

### setIsReducedAccuracyEnough

▸ **setIsReducedAccuracyEnough**(`value`): [`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Overrides

GeneralParamModel.setIsReducedAccuracyEnough

___

### setPopRoot

▸ **setPopRoot**(`value`): [`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`NaviPageParamModel`](util.NaviPageParamModel.md)

#### Overrides

GeneralParamModel.setPopRoot
